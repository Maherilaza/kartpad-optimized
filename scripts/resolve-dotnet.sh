#!/usr/bin/env bash
set -euo pipefail

dotnet_bin="${DOTNET_BIN:-$(command -v dotnet || true)}"
if [[ -z "${dotnet_bin}" || ! -x "${dotnet_bin}" ]]; then
  echo "ERROR: .NET 8 SDK is required; install it or set DOTNET_BIN" >&2
  exit 69
fi
if ! "${dotnet_bin}" --list-sdks | rg -q '^8\.[0-9]+\.[0-9]+ '; then
  echo "ERROR: .NET 8 SDK is required; found: $(${dotnet_bin} --version 2>/dev/null || echo unknown)" >&2
  exit 65
fi

printf '%s\n' "${dotnet_bin}"
