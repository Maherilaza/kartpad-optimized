#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
image="${1:-${repo_root}/ref/Mario Kart Wii.wbfs}"
output="${2:-${repo_root}/private/self-build/disc}"
expected_image_sha256="fc035e60610842da6860d23d4a30c1f1c0f019d492469deb8a2ac25ef5822331"
expected_dol_sha256="80d18895b39c63bd80f457398bfcbb91b7d16ac116a41a88967e954080155b05"
expected_rel_sha256="16d9d146112541fefea701ecb5bc1a496f9d50e4a752fbb5b6778e7c6399f67d"

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

image_lower="$(printf '%s' "${image}" | tr '[:upper:]' '[:lower:]')"
case "${image_lower}" in
  *.iso|*.gcm|*.gcz|*.ciso|*.wbfs|*.wia|*.rvz) ;;
  *) echo "ERROR: unsupported disc-image extension: ${image}" >&2; exit 64 ;;
esac
[[ -f "${image}" ]] || { echo "ERROR: missing disc image: ${image}" >&2; exit 66; }
[[ "${output}" == "${repo_root}/private/"* ]] || {
  echo "ERROR: extracted output must stay under ${repo_root}/private" >&2
  exit 64
}

nodtool="$(command -v nodtool || true)"
if [[ -z "${nodtool}" && -x "${CARGO_HOME:-${HOME}/.cargo}/bin/nodtool" ]]; then
  nodtool="${CARGO_HOME:-${HOME}/.cargo}/bin/nodtool"
fi
[[ -n "${nodtool}" ]] || {
  echo "ERROR: nodtool 2.0.0-alpha.9 is required (cargo install nodtool --version 2.0.0-alpha.9 --locked)" >&2
  exit 69
}
[[ "$(${nodtool} --version)" == "nodtool 2.0.0-alpha.9 " ||
   "$(${nodtool} --version)" == "nodtool 2.0.0-alpha.9" ]] || {
  echo "ERROR: expected nodtool 2.0.0-alpha.9" >&2
  exit 65
}

validate_output() {
  local root="$1"
  for relative in sys/boot.bin sys/bi2.bin sys/apploader.img sys/fst.bin \
      sys/main.dol files/rel/StaticR.rel; do
    [[ -f "${root}/${relative}" ]] || {
      echo "ERROR: extracted data is missing ${relative}" >&2
      return 1
    }
  done
  [[ "$(xxd -p -l 8 "${root}/sys/boot.bin")" == "524d435030310000" ]] || {
    echo "ERROR: extracted data is not RMCP01 disc 0 revision 0" >&2
    return 1
  }
  [[ "$(xxd -p -s 24 -l 4 "${root}/sys/boot.bin")" == "5d1c9ea3" ]] || {
    echo "ERROR: extracted data has an invalid Wii disc magic" >&2
    return 1
  }
  [[ "$(sha256_file "${root}/sys/main.dol")" == \
      "${expected_dol_sha256}" ]] || {
    echo "ERROR: extracted main.dol does not match the supported profile" >&2
    return 1
  }
  [[ "$(sha256_file "${root}/files/rel/StaticR.rel")" == \
      "${expected_rel_sha256}" ]] || {
    echo "ERROR: extracted StaticR.rel does not match the supported profile" >&2
    return 1
  }
}

image_sha256="$(sha256_file "${image}")"
if [[ "${image_sha256}" != "${expected_image_sha256}" &&
      "${KARTPAD_ALLOW_EQUIVALENT_DISC_CONTAINER:-0}" != "1" ]]; then
  echo "ERROR: disc-image SHA-256 is unsupported: ${image_sha256}" >&2
  echo "Use the Linux runtime handoff command for an equivalent ISO/WBFS/RVZ container." >&2
  exit 65
fi

if [[ -d "${output}" ]]; then
  validate_output "${output}"
  echo "Reused validated private RMCP01 extraction: ${output}"
  exit 0
fi
[[ ! -e "${output}" ]] || { echo "ERROR: output exists and is not a directory: ${output}" >&2; exit 73; }

mkdir -p "$(dirname "${output}")"
stage="${output}.partial.$RANDOM.$RANDOM"
[[ "${stage}" == "${repo_root}/private/"* ]]
cleanup() {
  if [[ -d "${stage}" && "${stage}" == "${repo_root}/private/"* ]]; then
    rm -rf -- "${stage}"
  fi
}
trap cleanup EXIT

# The Linux handoff may accept a differently encoded container, but only after
# extracting it read-only and validating the disc identity plus the exact
# executable inputs used by the translator.
"${nodtool}" extract --quiet "${image}" "${stage}"
validate_output "${stage}"
mv "${stage}" "${output}"
printf '{\n  "schema": 1,\n  "discId": "RMCP01",\n  "revision": 0,\n  "imageSHA256": "%s",\n  "mainDolSHA256": "%s",\n  "staticRelSHA256": "%s",\n  "extractor": "nodtool 2.0.0-alpha.9"\n}\n' \
  "${image_sha256}" "${expected_dol_sha256}" "${expected_rel_sha256}" \
  > "${output}/kartpad-disc-manifest.json"
echo "Prepared validated private RMCP01 extraction: ${output}"
