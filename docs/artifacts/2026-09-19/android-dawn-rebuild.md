# Android Dawn rebuild and production dependency preparation

The tested startup changes now have a fresh build and a portable dependency
archive. The normal Android dependency loader reads the Android URL, size,
archive hash, library hash, target-metadata hash and Dawn cache identity from
`dependencies.lock.json`. Apple retains its existing dependency entries.

## Source and build evidence

The fresh source seed matched all 85,128 regular files in the hash-verified
upstream Dawn archive at `13abc3bc8ea2d3c2050f9e77a12d012108ceee24`.
All 19 populated dependency checkouts matched their DEPS revisions with clean
tracked source. The checked build helper now enforces those dependency checks.
It applies the two reviewed Vulkan patches and the explicit cache-version file,
then builds Android arm64/API28 with NDK 29.0.14206865.

The fresh build passes. Its stable Dawn identity remains
`b0fd045b0a694eb07ac3fcf0d741f8697b935856`. The full unstripped archive hash is
`881728a6fcddc2207fe3cc336730b14db2c0b456a1e2e57f7e47324dc8f448c3`.
This is a fresh successful build, not a claim of bit-identical compiler output
to the earlier prototype: the build directories differ and the resulting
archives differ. Both originals remain preserved with their symbols.

## Portable package

`package-dawn-android.py` removes only debug sections from a copy of the static
library, changes its CMake liblog dependency to logical `log`, and includes
notices, patches, the build recipe and source/dependency identities. It checks
for remaining personal/CI builder paths and reads back every archive member.
The package is 10,785,820 bytes, with 72 regular files. Two independent package
invocations over these inputs produce the same archive checksum.

| Artifact field | SHA-256 |
| --- | --- |
| Portable archive | `c6b4efde6de30f341c46b65a1679914142059b360856d38e32f40dd55cae7fc1` |
| Static library after removing debug sections | `26f5e7e057b2c622dab22a86e17cbf9f461d25825e1704853c2835e106f9afb3` |
| Portable DawnTargets.cmake | `f914f68fa00893267e91cd64a9d91a05f0882ea6880dc48f296ca6711b11e3db` |

The package was extracted into a new directory and consumed by a fresh Android
CMake project through its exported Dawn target. As in the application, the
consumer explicitly includes the verified package and resolves Threads first;
an initial generic find_package attempt was rejected by Android's rooted
package search. No global root-mode relaxation was needed.

Both a direct link to the fresh library and the portable-package consumer pass
all eight `gpu_batch_probe.cpp` workloads on the disposable API36 ARM64 Vulkan
SwiftShader emulator. Each workload submits 769 indexed draws, with one, 154,
385 or 769 batches and repeated three-slot mapping/reuse. Overwrite and additive
outputs match the independent expected pixels and unsplit controls, with zero
GPU validation errors. This is software Vulkan execution of the synthetic probe,
not handset performance or complete Aurora/gameplay acceptance.

The normal dependency preparation script passes against this locally staged
hash-verified archive, checking every extracted member against the locked
archive and separately checking its library, metadata and cache identity.

## Publication boundary

The Android lock currently names the planned maintained-fork dependency asset
at tag `dawn-android-20260919.1`. Publication and anonymous download verification
are still required before merging or releasing this dependency change. A local
cache supplied the archive during the recorded preparation; it does not prove
the public URL is available. Full application rebuild and package validation
against the normal dependency path are the next gate. Code130/build54 predate
this package and the EFB readback corrections.

This does not extend supported device limits to PowerVR, establish the S24
corruption cause, repair fixed-capacity admission, or measure warmed Android FPS.
Private source/build controls and transcripts remain under
`work/aurora-capacity-20260919`.
