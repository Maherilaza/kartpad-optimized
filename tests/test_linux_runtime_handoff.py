import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/package-translated-runtime.py"
SPEC = importlib.util.spec_from_file_location("package_translated_runtime", SCRIPT)
PACKAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGER)


class LinuxRuntimeHandoffTests(unittest.TestCase):
    def make_translation(self, root: Path) -> Path:
        translation = root / "private/self-build/translation"
        shards = translation / "build_shards"
        (translation / "functions").mkdir(parents=True)
        (shards / "base_common").mkdir(parents=True)
        (translation / "RuntimeConfig.h").write_text("#pragma once\n")
        (translation / "data_sections_init.cpp").write_text("void InitData() {}\n")
        (translation / "data_sections_init_blobs.S").write_text(
            '.incbin "@MKW_TRANSLATED_BLOB_ROOT@/data_sections_init_blobs/_data.bin"\n'
        )
        (translation / "data_sections_init_blobs").mkdir()
        (translation / "data_sections_init_blobs/_data.bin").write_bytes(b"data")
        (translation / "guest_symbol_table.cpp").write_text("const int symbols = 0;\n")
        (translation / "functions/func_8000A440.cpp").write_text("void f() {}\n")
        shard = shards / "base_common/base.cpp"
        shard.write_text("void translated() {}\n")
        (shards / "shards.cmake").write_text(
            "# Translator-owned stable shard graph; do not edit.\n"
            f'set(MKW_TRANSLATED_SHARD_ROOT "{shards}")\n'
            "set(MKW_BASE_FUNCTION_COUNT 29065)\n"
            "set(MKW_SHARED_BASE_FUNCTION_COUNT 29065)\n"
            "set(MKW_PORTABLE_SHARED_BASE_FUNCTION_COUNT 29065)\n"
            "set(MKW_PROFILE_SENSITIVE_TARGET_COUNT 0)\n"
            "set(MKW_PROFILE_SENSITIVE_CALLER_COUNT 0)\n"
            "set(MKW_RETRO_REWIND_FUNCTION_COUNT 0)\n"
            "set(MKW_BASE_COMMON_SHARDS\n"
            f'  "{shard}"\n'
            ")\n"
            "set(MKW_BASE_PORTABLE_SENSITIVE_SHARDS\n)\n"
            "set(MKW_RETRO_PORTABLE_SENSITIVE_SHARDS\n)\n"
            "set(MKW_RETRO_MOD_SHARDS\n)\n"
            "set(MKW_BASE_REGISTRATION_SOURCES\n)\n"
            "set(MKW_RETRO_REGISTRATION_SOURCES\n)\n"
            "set(MKW_RETRO_EXTRA_SOURCES\n)\n"
            "set(MKW_HAVE_RETRO_REWIND_SHARDS OFF)\n"
        )
        (translation / "disc.rvz").write_bytes(b"must not be archived")
        (translation / "sys").mkdir()
        (translation / "sys/main.dol").write_bytes(b"must not be archived")
        return translation

    def test_archive_is_relocatable_private_and_reproducible(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            translation = self.make_translation(root)
            first = root / "first.tar.gz"
            second = root / "second.tar.gz"
            first_digest = PACKAGER.package(REPO, translation, first)
            PACKAGER.package(REPO, translation, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(
                hashlib.sha256(first.read_bytes()).hexdigest(),
                hashlib.sha256(second.read_bytes()).hexdigest(),
            )

            with tarfile.open(first, "r:gz") as archive:
                names = archive.getnames()
                self.assertIn(
                    "kartpad-runtime/build_shards/base_common/base.cpp", names
                )
                self.assertIn("kartpad-runtime/functions/func_8000A440.cpp", names)
                self.assertIn(
                    "kartpad-runtime/data_sections_init_blobs/_data.bin", names
                )
                self.assertNotIn("kartpad-runtime/disc.rvz", names)
                self.assertFalse(any("/sys/" in name for name in names))
                cmake = (
                    archive.extractfile("kartpad-runtime/build_shards/shards.cmake")
                    .read()
                    .decode()
                )
                self.assertIn(
                    'set(MKW_TRANSLATED_SHARD_ROOT "${CMAKE_CURRENT_LIST_DIR}")',
                    cmake,
                )
                self.assertIn(
                    '"${MKW_TRANSLATED_SHARD_ROOT}/base_common/base.cpp"',
                    cmake,
                )
                self.assertNotIn(str(translation), cmake)
                blob_assembly = (
                    archive.extractfile("kartpad-runtime/data_sections_init_blobs.S")
                    .read()
                    .decode()
                )
                self.assertIn("@MKW_TRANSLATED_BLOB_ROOT@", blob_assembly)
                self.assertNotIn(str(translation), blob_assembly)
                manifest = json.load(
                    archive.extractfile("kartpad-runtime/kartpad-runtime-manifest.json")
                )
                self.assertEqual(manifest["contentSHA256"], first_digest)
                self.assertTrue(manifest["containsTranslatedGameCode"])
                self.assertFalse(manifest["containsDiscImage"])
                self.assertFalse(manifest["containsExtractedGameData"])

    def test_archive_rejects_host_paths_in_generated_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            translation = self.make_translation(Path(temporary))
            (translation / "RuntimeConfig.h").write_text(
                f'#line 1 "{REPO}/private/input"\n'
            )
            with self.assertRaisesRegex(ValueError, "host path"):
                PACKAGER.package(REPO, translation, Path(temporary) / "runtime.tar.gz")

    def test_archive_rejects_symlinked_payloads(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            translation = self.make_translation(root)
            (translation / "guest_symbol_table.cpp").unlink()
            (translation / "guest_symbol_table.cpp").symlink_to("/etc/hosts")
            with self.assertRaisesRegex(ValueError, "symlink"):
                PACKAGER.package(REPO, translation, root / "runtime.tar.gz")

    def test_linux_scripts_use_portable_tools_and_validated_executables(self):
        prepare = (REPO / "scripts/prepare-disc.sh").read_text()
        translator = (REPO / "scripts/prepare-patched-translator.sh").read_text()
        translate = (REPO / "scripts/translate-base.sh").read_text()
        runtime_prepare = (REPO / "scripts/prepare-ios-game-runtime.sh").read_text()
        android_runtime_prepare = (
            REPO / "scripts/prepare-android-game-runtime.sh"
        ).read_text()
        project = (REPO / "tools/mkwii-rmcp01-base.yml").read_text()
        for extension in ("*.iso", "*.wbfs", "*.rvz"):
            self.assertIn(extension, prepare)
        for digest in (
            "fc035e60610842da6860d23d4a30c1f1c0f019d492469deb8a2ac25ef5822331",
            "80d18895b39c63bd80f457398bfcbb91b7d16ac116a41a88967e954080155b05",
            "16d9d146112541fefea701ecb5bc1a496f9d50e4a752fbb5b6778e7c6399f67d",
        ):
            self.assertIn(digest, prepare)
        self.assertIn("sha256sum", prepare)
        self.assertIn("KARTPAD_ALLOW_EQUIVALENT_DISC_CONTAINER", prepare)
        self.assertIn(
            "KARTPAD_ALLOW_EQUIVALENT_DISC_CONTAINER=1",
            (REPO / "scripts/generate-linux-runtime-archive.sh").read_text(),
        )
        self.assertTrue(translator.startswith("#!/usr/bin/env bash"))
        self.assertNotIn("/opt/homebrew", translator + translate)
        self.assertIn("scripts/resolve-dotnet.sh", translator + translate)
        self.assertIn(
            'if [[ "${prepare_only}" == "0" &&',
            runtime_prepare,
        )
        self.assertIn("sha256sum", runtime_prepare)
        self.assertIn(
            "Prepared integrated ${prepare_platform} runtime source", runtime_prepare
        )
        self.assertIn(
            'generated_stage="${runtime_source}-generated"', android_runtime_prepare
        )
        self.assertIn(
            'MKW_TRANSLATED_BLOB_ROOT="$generated_stage"',
            android_runtime_prepare,
        )
        self.assertIn("vendor/wiicompiled/projects/mkwii/MAP.txt", project)

    def test_android_source_preparation_reaches_graph_validation_on_linux(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            translation = root / "translation"
            (translation / "functions").mkdir(parents=True)
            (translation / "build_shards").mkdir()
            (translation / "functions/func_8000A440.cpp").write_text("invalid\n")
            (translation / "build_shards/shards.cmake").write_text("invalid\n")
            result = subprocess.run(
                [
                    REPO / "scripts/prepare-android-game-runtime.sh",
                    translation,
                    root / "runtime-source",
                    root / "runtime-build",
                    "base",
                ],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("func_8000A440", result.stderr)
            self.assertNotIn("requires arm64 macOS", result.stderr)


if __name__ == "__main__":
    unittest.main()
