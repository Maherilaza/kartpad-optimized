#!/usr/bin/env python3
"""Package the generated base graph without user disc data or host paths."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import tarfile
from pathlib import Path


REQUIRED_FILES = (
    "RuntimeConfig.h",
    "data_sections_init.cpp",
    "data_sections_init_blobs.S",
    "functions/func_8000A440.cpp",
    "build_shards/shards.cmake",
)
OPTIONAL_FILES = ("guest_symbol_table.cpp",)
ARCHIVE_ROOT = "kartpad-runtime"


def payload_files(translation: Path) -> list[Path]:
    for directory in (
        translation,
        translation / "functions",
        translation / "build_shards",
    ):
        if not directory.is_dir() or directory.is_symlink():
            raise ValueError(f"generated runtime directory is invalid: {directory}")
    for relative in REQUIRED_FILES:
        path = translation / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing generated runtime file: {relative}")
    files = [translation / relative for relative in REQUIRED_FILES[:-1]]
    for relative in OPTIONAL_FILES:
        path = translation / relative
        if path.is_symlink():
            raise ValueError(f"generated runtime must not contain symlinks: {path}")
        if path.is_file():
            files.append(path)
    shard_root = translation / "build_shards"
    for path in sorted(shard_root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"generated runtime must not contain symlinks: {path}")
        if path.is_file():
            files.append(path)
    return sorted(set(files), key=lambda path: path.relative_to(translation).as_posix())


def relocatable_manifest(path: Path) -> bytes:
    text = path.read_text()
    shard_root = path.parent.resolve().as_posix()
    root_pattern = re.compile(
        r'^set\(MKW_TRANSLATED_SHARD_ROOT "[^"]+"\)$', re.MULTILINE
    )
    if not root_pattern.search(text):
        raise ValueError("translated shard manifest has no root declaration")
    text = root_pattern.sub(
        'set(MKW_TRANSLATED_SHARD_ROOT "${CMAKE_CURRENT_LIST_DIR}")',
        text,
        count=1,
    )
    text = text.replace(f'"{shard_root}/', '"${MKW_TRANSLATED_SHARD_ROOT}/')
    if shard_root in text:
        raise ValueError("translated shard manifest still contains its host path")
    if not re.search(r"^set\(MKW_BASE_FUNCTION_COUNT 29065\)$", text, re.MULTILINE):
        raise ValueError("translated shard manifest has the wrong base function count")
    if not re.search(r"^set\(MKW_RETRO_REWIND_FUNCTION_COUNT 0\)$", text, re.MULTILINE):
        raise ValueError("translated shard manifest is not the base-only graph")
    if not re.search(r"^set\(MKW_HAVE_RETRO_REWIND_SHARDS OFF\)$", text, re.MULTILINE):
        raise ValueError("translated shard manifest unexpectedly enables Retro Rewind")
    return text.encode()


def archive_bytes(
    repo: Path,
    translation: Path,
    source_commit: str,
) -> tuple[list[tuple[str, bytes]], str]:
    entries: list[tuple[str, bytes]] = []
    digest = hashlib.sha256()
    forbidden_paths = (
        translation.resolve().as_posix().encode(),
        repo.resolve().as_posix().encode(),
    )
    for path in payload_files(translation):
        relative = path.relative_to(translation).as_posix()
        data = (
            relocatable_manifest(path)
            if relative == "build_shards/shards.cmake"
            else path.read_bytes()
        )
        if any(prefix in data for prefix in forbidden_paths):
            raise ValueError(f"generated runtime exposes a host path: {relative}")
        digest.update(relative.encode() + b"\0" + data + b"\0")
        entries.append((f"{ARCHIVE_ROOT}/{relative}", data))
    content_sha256 = digest.hexdigest()
    manifest = {
        "schemaVersion": 1,
        "profileId": "mkwii-rmcp01-rev0-base",
        "sourceCommit": source_commit,
        "contentSHA256": content_sha256,
        "containsTranslatedGameCode": True,
        "containsDiscImage": False,
        "containsExtractedGameData": False,
        "redistributionRights": "not-cleared",
    }
    entries.append(
        (
            f"{ARCHIVE_ROOT}/kartpad-runtime-manifest.json",
            (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode(),
        )
    )
    return entries, content_sha256


def add_bytes(archive: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    archive.addfile(info, io.BytesIO(data))


def package(repo: Path, translation: Path, output: Path) -> str:
    source_commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD^{commit}"],
        text=True,
    ).strip()
    entries, content_sha256 = archive_bytes(
        repo.resolve(), translation.resolve(), source_commit
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    partial = output.with_name(output.name + ".partial")
    try:
        with partial.open("wb") as raw:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw, mtime=0
            ) as compressed:
                with tarfile.open(fileobj=compressed, mode="w") as archive:
                    for name, data in entries:
                        add_bytes(archive, name, data)
        partial.replace(output)
    finally:
        partial.unlink(missing_ok=True)
    return content_sha256


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--translation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        digest = package(
            args.repo.resolve(), args.translation.resolve(), args.output.resolve()
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"ERROR: {error}\n")
    print(f"Packaged translated runtime: {args.output}")
    print(f"Content SHA-256: {digest}")


if __name__ == "__main__":
    main()
