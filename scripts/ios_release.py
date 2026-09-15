"""Exact identities for the accepted incremental iOS community release."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess

RELEASE_TAG = "v0.4.23-ios.1"
APP_VERSION = "0.4.23"
APP_BUILD = "46"
COMPILED_SOURCE = "91aaedc7cff6c4e801cfe0636d5c3a4aa3b9bc2d"
EXECUTABLE_SHA256 = "ace1a53d7c88d520767f7516a36327878ec2b49ee35d5cbcd4b6e92d57757768"
RUNTIME_SHA256 = "9e82b15f855b7c2a6ff39b908f768a18a58e72a623bc8ddc3f7f8bb7b3f6f125"
TRANSLATION_SHA256 = "f5b67171325d4b98ccee74752268d689952d054f78f001b9083e42507dff8e0b"
COMPOSITION_SHA256 = "57a9c28212cf393f2384ab13b85828a004bd7ffa4459c7f1cad5d5ac08c0cace"
REFRESHED_INPUTS_SHA256 = "1f0334fd2577adc825cf7188fe6ca7f0b5f949f9040e6fecb599e70a51dfb11e"
PRODUCTION_PATHS = ("apple/ios", "apple/mobile", "apple/shared", "apple/third_party", "runtime/include")


def accepted_build(app: Path) -> dict:
    manifest = json.loads((app / "kartpad-build.json").read_text())
    composition_bytes = (app / "kartpad-ui-composition.json").read_bytes()
    composition = json.loads(composition_bytes)
    if hashlib.sha256(composition_bytes).hexdigest() != COMPOSITION_SHA256:
        raise ValueError("unexpected incremental compilation manifest")
    if manifest != composition["base_manifest"]:
        raise ValueError("base compilation manifest changed")
    if manifest.get("source_revision") != COMPILED_SOURCE or manifest.get("source_dirty") is not False:
        raise ValueError("expected the clean accepted base compilation source")
    if manifest.get("prepared_runtime", {}).get("sha256") != RUNTIME_SHA256:
        raise ValueError("unexpected prepared runtime hash")
    if manifest.get("translation", {}).get("sha256") != TRANSLATION_SHA256:
        raise ValueError("unexpected translation hash")
    if hashlib.sha256((app / "KartPad").read_bytes()).hexdigest() != EXECUTABLE_SHA256:
        raise ValueError("unexpected refreshed executable")
    return {
        "compiledBaseSourceCommit": COMPILED_SOURCE,
        "preparedRuntimeSHA256": RUNTIME_SHA256,
        "translationSHA256": TRANSLATION_SHA256,
        "compilationManifestSHA256": hashlib.sha256((app / "kartpad-build.json").read_bytes()).hexdigest(),
        "incrementalCompilationManifestSHA256": COMPOSITION_SHA256,
        "compilationScope": composition["scope"],
        "refreshedInputPaths": list(PRODUCTION_PATHS),
        "refreshedInputsEquivalent": True,
        "fullSourceRebuild": False,
    }


def verify_source_equivalence(repo: Path, packaging_commit: str) -> None:
    names = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", packaging_commit, "--", *PRODUCTION_PATHS], text=True).splitlines()
    inputs = {name: hashlib.sha256(subprocess.check_output(["git", "-C", str(repo), "show", packaging_commit + ":" + name])).hexdigest() for name in names}
    actual = hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if actual != REFRESHED_INPUTS_SHA256:
        raise ValueError("refreshed production inputs differ from compilation")
