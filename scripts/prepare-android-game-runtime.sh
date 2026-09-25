#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
absolute_from_repo() {
  case "$1" in
    /*) printf '%s\n' "$1" ;;
    *) printf '%s/%s\n' "$repo_root" "$1" ;;
  esac
}

translation_root="$(absolute_from_repo "${1:-private/g8-full-translation}")"
runtime_source="$(absolute_from_repo "${2:-build/android-game-runtime-source}")"
runtime_build="$(absolute_from_repo "${3:-build/android-game-runtime-build}")"
product="${4:-base}"

case "$product" in
  base|retro-rewind|dual) ;;
  *) echo "ERROR: product must be base, retro-rewind, or dual" >&2; exit 64 ;;
esac
if [[ ! -f "$translation_root/build_shards/shards.cmake" ]]; then
  echo "ERROR: missing private translated graph: $translation_root" >&2
  exit 1
fi
if [[ -e "$runtime_source" || -e "$runtime_build" ]]; then
  echo "ERROR: output already exists; choose fresh output paths" >&2
  exit 1
fi

# Reuse only profile/header/dependency preparation. Android's maintained source
# is selected directly; no Apple or Android patch stack is replayed.
KARTPAD_PREPARE_PLATFORM=android KARTPAD_PREPARE_ONLY=1 "$repo_root/scripts/prepare-ios-game-runtime.sh" \
  "$translation_root" "$runtime_source" "$runtime_build" "$product"
cp "$repo_root/runtime/include/kartpad/android/trace_scope.h" \
  "$runtime_source/aurora-main/lib/kartpad_android_trace_scope.h"

generated_link="$(dirname "$runtime_source")/generated"
generated_stage="${runtime_source}-generated"
if [[ -e "$generated_link" && ! -L "$generated_link" ]]; then
  echo "ERROR: generated path exists and is not a symlink: $generated_link" >&2
  exit 1
fi
if [[ -e "$generated_stage" || -L "$generated_stage" ]]; then
  echo "ERROR: generated staging path already exists: $generated_stage" >&2
  exit 1
fi
mkdir "$generated_stage"
while IFS= read -r -d '' entry; do
  name="${entry##*/}"
  if [[ "$name" == data_sections_init_blobs.S ]]; then
    cp "$entry" "$generated_stage/$name"
    MKW_TRANSLATED_BLOB_ROOT="$generated_stage" perl -0pi -e \
      's/\@MKW_TRANSLATED_BLOB_ROOT\@/$ENV{MKW_TRANSLATED_BLOB_ROOT}/g' \
      "$generated_stage/$name"
    if grep -Fq '@MKW_TRANSLATED_BLOB_ROOT@' "$generated_stage/$name"; then
      echo "ERROR: failed to resolve translated blob root in $entry" >&2
      exit 1
    fi
  else
    ln -s "$entry" "$generated_stage/$name"
  fi
done < <(find "$translation_root" -mindepth 1 -maxdepth 1 -print0)
ln -sfn "$generated_stage" "$generated_link"

echo "Prepared integrated Android runtime source: $runtime_source"
