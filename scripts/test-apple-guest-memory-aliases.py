#!/usr/bin/env python3
"""Run the patched iOS allocator on Darwin; also compile against the iPhone SDK.

Pass --runtime-include from a prepared Apple runtime to use its real public header.
The host run selects the iOS branch using a TargetConditionals shim; only Mach API
fault injection is substituted, and successful remaps use the real kernel API.
"""
import argparse
import pathlib
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--runtime-include', required=True, type=pathlib.Path)
args = parser.parse_args()
repo = pathlib.Path(__file__).resolve().parent.parent
patch = (repo / 'patches/wiicompiled-apple-runtime.patch').read_text()
section = patch.split('+++ b/src/apple/guest_flat_memory_apple.cpp', 1)[1].split('diff -ruN', 1)[0]
source = '\n'.join(line[1:] for line in section.splitlines() if line.startswith('+')) + '\n'
with tempfile.TemporaryDirectory(prefix='kartpad-apple-ram-') as directory:
    root = pathlib.Path(directory)
    (root / 'src/apple').mkdir(parents=True)
    (root / 'src/apple/guest_flat_memory_apple.cpp').write_text(source)
    subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-d', str(root), '-i',
                    str(repo / 'patches/wiicompiled-ios-anonymous-memory.patch')], check=True)
    (root / 'guest_flat_memory_apple.cpp').write_text((root / 'src/apple/guest_flat_memory_apple.cpp').read_text())
    (root / 'TargetConditionals.h').write_text('#pragma once\n#undef TARGET_OS_IPHONE\n#define TARGET_OS_IPHONE 1\n')
    subprocess.run(['xcrun', 'clang++', '-std=c++20', '-Wall', '-Wextra', '-Werror',
                    '-I', str(root), '-I', str(args.runtime_include),
                    str(repo / 'scripts/tests/apple_guest_memory_alias_harness.cpp'),
                    '-o', str(root / 'aliases')], check=True)
    subprocess.run([str(root / 'aliases')], check=True)
    # No shim in the device build: SDK TargetConditionals selects the platform.
    (root / 'TargetConditionals.h').unlink()
    sdk = subprocess.check_output(['xcrun', '--sdk', 'iphoneos', '--show-sdk-path'], text=True).strip()
    subprocess.run(['xcrun', '--sdk', 'iphoneos', 'clang++', '-std=c++20',
                    '-target', 'arm64-apple-ios17.0', '-isysroot', sdk,
                    '-Wall', '-Wextra', '-Werror', '-I', str(args.runtime_include),
                    '-dynamiclib', str(root / 'guest_flat_memory_apple.cpp'),
                    '-o', str(root / 'guest_flat_memory_apple.dylib')], check=True)
    subprocess.run(['xcrun', 'clang++', '-std=c++20', '-Wall', '-Wextra', '-Werror',
                    '-I', str(args.runtime_include), '-c', str(root / 'guest_flat_memory_apple.cpp'),
                    '-o', str(root / 'guest_flat_memory_macos.o')], check=True)
    print('Actual allocator links for arm64 iOS 17 with the iPhone SDK; macOS branch compiles.')
