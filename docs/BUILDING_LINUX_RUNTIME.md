# Generate the private Android runtime on Linux

This workflow produces a handoff archive containing the translated `RMCP01`
revision-0 game logic needed to compile KartPad for Android. It does not put the
disc image, extracted tracks, textures, audio, saves, credentials, or signing
keys in the archive.

The generated archive still contains game-derived translated code. Keep it
private unless you have independently determined that you may redistribute it.

## Requirements

- A 64-bit Linux PC with substantial free disk space.
- Git, Python 3, `rsync`, ripgrep, Perl, `xxd`, Rust/Cargo, and the .NET 8 SDK.
- `nodtool` 2.0.0-alpha.9.
- Your legally obtained PAL `RMCP01` revision-0 ISO, WBFS, or RVZ image.

Install the pinned extractor:

```sh
cargo install nodtool --version 2.0.0-alpha.9 --locked
```

Verify that .NET 8 is available:

```sh
dotnet --list-sdks
```

If it is installed outside `PATH`, pass its executable explicitly:

```sh
DOTNET_BIN="$HOME/.dotnet/dotnet" \
  ./scripts/generate-linux-runtime-archive.sh /absolute/path/to/your-game.rvz
```

## Generate the archive

Clone the optimized repository and run the generator from its root:

```sh
git clone --recurse-submodules https://github.com/Maherilaza/kartpad-optimized.git
cd kartpad-optimized
./scripts/generate-linux-runtime-archive.sh /absolute/path/to/your-game.rvz
```

The tracked checkout must be clean so the archive's recorded source commit
identifies the translator and runtime code that produced it.

ISO and WBFS paths work the same way. The workflow:

1. extracts the image read-only under ignored `private/`;
2. verifies `RMCP01` revision 0 and the exact supported DOL/REL identities;
3. builds the maintained .NET translator;
4. generates and validates the base translated graph; and
5. writes `artifacts/KartPad-RMCP01-runtime-<commit>.tar.gz`.

The initial translation is CPU-, memory-, and disk-intensive. Set
`KARTPAD_TRANSLATION_JOBS` from 1 through 8 to control parallel work:

```sh
KARTPAD_TRANSLATION_JOBS=2 \
  ./scripts/generate-linux-runtime-archive.sh /absolute/path/to/your-game.iso
```

Only send the resulting `.tar.gz` handoff archive for an Android build. Do not
send or commit the original image, anything under `private/self-build/disc`,
saves, credentials, keystores, or password files.

The resulting custom APK uses its own signing identity unless the official
maintainer signs it. It therefore cannot update the official KartPad APK in
place.
