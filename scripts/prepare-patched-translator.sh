#!/usr/bin/env bash
set -euo pipefail

repo="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
source="${repo}/vendor/wiicompiled"
stage="${repo}/build/wiicompiled-fpscr"

# Keep the established output path for translator and native-registration callers.
# Maintained source lives in Git; this command never replays translator patches.
[[ -f "${source}/translator/src/Translator.Cli/Translator.Cli.csproj" ]] || {
  echo "ERROR: missing tracked WiiCompiled translator source" >&2
  exit 1
}
python3 "${repo}/scripts/stage-maintained-translator.py" "${stage}"

dotnet_bin="$("${repo}/scripts/resolve-dotnet.sh")"
project="${stage}/translator/src/Translator.Cli/Translator.Cli.csproj"
"${dotnet_bin}" build "${project}" -c Release
