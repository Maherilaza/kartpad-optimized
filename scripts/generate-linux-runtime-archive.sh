#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
image="${1:-}"
short_commit="$(git -C "${repo_root}" rev-parse --short=12 HEAD)"
output="${2:-${repo_root}/artifacts/KartPad-RMCP01-runtime-${short_commit}.tar.gz}"

usage() {
  echo "Usage: scripts/generate-linux-runtime-archive.sh /absolute/path/game.(iso|wbfs|rvz) [output.tar.gz]" >&2
}

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "ERROR: this runtime handoff workflow requires Linux" >&2
  exit 1
fi
if [[ -z "${image}" ]]; then
  usage
  exit 64
fi
image="$(realpath "${image}")"
[[ -f "${image}" ]] || {
  echo "ERROR: missing disc image: ${image}" >&2
  exit 66
}
for command in git python3 rsync rg perl realpath xxd; do
  command -v "${command}" >/dev/null 2>&1 || {
    echo "ERROR: missing required command: ${command}" >&2
    exit 69
  }
done
if [[ -n "$(git -C "${repo_root}" status --porcelain --untracked-files=no)" ]]; then
  echo "ERROR: tracked source changes are present; generate the handoff from a clean commit" >&2
  exit 65
fi
"${repo_root}/scripts/resolve-dotnet.sh" >/dev/null

nodtool="$(command -v nodtool || true)"
if [[ -z "${nodtool}" && -x "${CARGO_HOME:-${HOME}/.cargo}/bin/nodtool" ]]; then
  nodtool="${CARGO_HOME:-${HOME}/.cargo}/bin/nodtool"
fi
[[ -n "${nodtool}" ]] || {
  echo "ERROR: nodtool 2.0.0-alpha.9 is required; install it with:" >&2
  echo "  cargo install nodtool --version 2.0.0-alpha.9 --locked" >&2
  exit 69
}

KARTPAD_ALLOW_EQUIVALENT_DISC_CONTAINER=1 \
  "${repo_root}/scripts/translate-base.sh" "${image}"
python3 "${repo_root}/scripts/package-translated-runtime.py" \
  --repo "${repo_root}" \
  --translation "${repo_root}/private/self-build/translation" \
  --output "${output}"

echo "Safe handoff archive created without the disc image or extracted game data:"
echo "${output}"
