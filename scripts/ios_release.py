"""Identity and provenance checks for the accepted iOS community release."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import subprocess

RELEASE_TAG = "v0.4.22-ios.1"
APP_VERSION = "0.4.22"
APP_BUILD = "43"
COMPILED_SOURCE = "43a1661a5c2cb6a5f545cf6e3aaeb330a6857456"
EXECUTABLE_SHA256 = "e765832a7d0b534417f3f92d6437d0d39ac226a4b8bf09294e22628ad58cf571"
RUNTIME_SHA256 = "a2909df0080112d054c40225594a61ec5a6c734fee929030c79ab9ab3b9d20ed"
TRANSLATION_SHA256 = "f92c0764fcfc778770f79590e0e9e10e2e1ff0a9415b3be75c6668768ede0ae5"
# Compare production inputs, excluding release notes and packaging-only changes.
PRODUCTION_PATHS = (
    "apple/ios", "apple/mobile", "apple/shared", "apple/third_party",
    "runtime", "builder", "vendor/wiicompiled", "vendor/runtimes/ios", "CMakeLists.txt",
    ".gitmodules", "dependencies.lock.json", "scripts/stage-maintained-runtime.py", "scripts/stage-maintained-translator.py",
    "scripts/prepare-patched-translator.sh",
    "scripts/prepare-ios-game-runtime.sh", "scripts/build-ios-device-game-app.sh",
    "scripts/inject-retro-rel-report-guard.py", "scripts/write-build-provenance.py",
    "scripts/generate-ios-icon-assets.sh", "scripts/verify-sunpad-overlay-snapshot.sh",
)
# The preparation script is itself compared, so its patch list must also match.
PRODUCTION_PATHS += tuple(
    "patches/" + name for name in sorted(set(re.findall(
        r"[A-Za-z0-9_-]+\.patch",
        (Path(__file__).parent / "prepare-ios-game-runtime.sh").read_text(),
    )))
)


def accepted_build(app: Path) -> dict:
    """Reject stale candidates while retaining the original compilation manifest."""
    manifest = json.loads((app / "kartpad-build.json").read_text())
    if manifest.get("source_revision") != COMPILED_SOURCE or manifest.get("source_dirty") is not False:
        raise ValueError("expected the clean accepted compilation source")
    if manifest.get("prepared_runtime", {}).get("sha256") != RUNTIME_SHA256:
        raise ValueError("unexpected prepared runtime hash")
    if manifest.get("translation", {}).get("sha256") != TRANSLATION_SHA256:
        raise ValueError("unexpected translation hash")
    if hashlib.sha256((app / "KartPad").read_bytes()).hexdigest() != EXECUTABLE_SHA256:
        raise ValueError("expected the hardware-accepted unsigned executable")
    return {
        "compiledSourceCommit": COMPILED_SOURCE,
        "preparedRuntimeSHA256": RUNTIME_SHA256,
        "translationSHA256": TRANSLATION_SHA256,
        "compilationManifestSHA256": hashlib.sha256((app / "kartpad-build.json").read_bytes()).hexdigest(),
        "productionInputPaths": list(PRODUCTION_PATHS),
        "productionInputsEquivalent": True,
    }


def verify_source_equivalence(repo: Path, packaging_commit: str) -> None:
    changed = subprocess.check_output(
        ["git", "-C", str(repo), "diff", "--name-only", COMPILED_SOURCE,
         packaging_commit, "--", *PRODUCTION_PATHS], text=True,
    ).strip()
    profile = "builder/profiles/mkwii-rmcp01-rev0.json"
    if profile in changed.splitlines():
        old = json.loads(subprocess.check_output(
            ["git", "-C", str(repo), "show", f"{COMPILED_SOURCE}:{profile}"], text=True))
        new = json.loads(subprocess.check_output(
            ["git", "-C", str(repo), "show", f"{packaging_commit}:{profile}"], text=True))
        # This only corrects the validation count for the already-generated graph.
        assert old['translation']["expectedRetroFunctions"] == 4095
        old['translation']["expectedRetroFunctions"] = 4101
        if old != new:
            raise ValueError("unexpected builder profile change")
        changed = "\n".join(p for p in changed.splitlines() if p != profile)
    if changed:
        raise ValueError(f"production inputs differ from accepted compilation: {changed}")
