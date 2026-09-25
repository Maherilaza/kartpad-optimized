#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
# shellcheck source=android-toolchain-versions.sh
source "$repo_root/scripts/android-toolchain-versions.sh"

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "ERROR: the Android CI fixture lane requires Linux x86_64" >&2
  exit 1
fi

sdk_root="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-}}"
if [[ -z "$sdk_root" ]]; then
  echo "ERROR: ANDROID_SDK_ROOT or ANDROID_HOME must name the Android SDK" >&2
  exit 1
fi

sdkmanager="${ANDROID_SDKMANAGER:-}"
if [[ -z "$sdkmanager" ]]; then
  sdkmanager="$(command -v sdkmanager || true)"
fi
if [[ -z "$sdkmanager" ]]; then
  for candidate in \
    "$sdk_root/cmdline-tools/latest/bin/sdkmanager" \
    "$sdk_root/cmdline-tools/$KARTPAD_ANDROID_CMDLINE_TOOLS_REVISION/bin/sdkmanager"; do
    if [[ -x "$candidate" ]]; then
      sdkmanager="$candidate"
      break
    fi
  done
fi
if [[ ! -x "$sdkmanager" ]]; then
  echo "ERROR: sdkmanager is unavailable in the configured Android SDK" >&2
  exit 1
fi

"$sdkmanager" --sdk_root="$sdk_root" \
  "platforms;android-$KARTPAD_ANDROID_COMPILE_SDK" \
  "build-tools;$KARTPAD_ANDROID_BUILD_TOOLS" \
  "ndk;$KARTPAD_ANDROID_NDK" \
  "cmake;$KARTPAD_ANDROID_CMAKE"

prepare_output="$("$repo_root/scripts/prepare-android-dependencies.sh")"
echo "$prepare_output"
export DAWN_ANDROID_ROOT
export MINIZIP_ANDROID_ROOT
export MBEDTLS_ANDROID_ROOT
DAWN_ANDROID_ROOT="$(printf '%s\n' "$prepare_output" | sed -n 's/^DAWN_ANDROID_ROOT=//p')"
MINIZIP_ANDROID_ROOT="$(printf '%s\n' "$prepare_output" | sed -n 's/^MINIZIP_ANDROID_ROOT=//p')"
MBEDTLS_ANDROID_ROOT="$(printf '%s\n' "$prepare_output" | sed -n 's/^MBEDTLS_ANDROID_ROOT=//p')"
if [[ -z "$DAWN_ANDROID_ROOT" || -z "$MINIZIP_ANDROID_ROOT" ||
      -z "$MBEDTLS_ANDROID_ROOT" ]]; then
  echo "ERROR: dependency preparation did not report native dependency roots" >&2
  exit 1
fi

version_code="${KARTPAD_ANDROID_VERSION_CODE:?KARTPAD_ANDROID_VERSION_CODE is required}"
version_name="${KARTPAD_ANDROID_VERSION_NAME:?KARTPAD_ANDROID_VERSION_NAME is required}"
export ANDROID_SDK_ROOT="$sdk_root"

"$repo_root/android/gradlew" --project-dir "$repo_root/android" --no-daemon \
  -PkartpadVersionCode="$version_code" \
  -PkartpadVersionName="$version_name" \
  :app:assembleDebug

apk="$repo_root/android/app/build/outputs/apk/debug/app-debug.apk"
KARTPAD_ANDROID_EXPECTED_VERSION_CODE="$version_code" \
KARTPAD_ANDROID_EXPECTED_VERSION_NAME="$version_name" \
  "$repo_root/scripts/audit-android-package.sh" "$apk"

echo "ANDROID_FIXTURE_APK=$apk"
