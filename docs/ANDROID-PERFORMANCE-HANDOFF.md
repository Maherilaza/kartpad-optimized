# Android investigation handoff

Refreshed September21,2026. Current public baseline: **Android 0.5.0/code135**. Apple 0.5.1-experimental.1/build60 is a separate diagnostic-overhead mitigation and does not update Android. See the [current issue inventory](artifacts/2026-09-21/open-issue-inventory.md), [evening evidence](artifacts/2026-09-21/evening-goal-loop.md) and [maintenance board](MAINTENANCE-BOARD.md). Older code63/code73/code83 assignments are historical.

## First: sustained frame time

#198 already supplied three captures and agreed to a profiler handoff. Its Helio G85 report is 25–29 FPS after the pipeline queue reaches zero, with 94–97% main-thread occupancy and 2.3–2.6 ms measured presentation. This supports CPU sampling; it does not identify the expensive function. GX CPU work outside the presentation timer remains a possibility.

Prepare a current, non-debuggable, shell-profileable diagnostic with exact native symbols and a compatible signer. The release signing key location is resolved. The retained code73 Debug-signed profiler cannot update a Community-signed installation. Confirm the recipient's installed version/signer and concrete private delivery route before handing off a diagnostic. Keep credentials, symbols and private game inputs out of public artifacts.

Capture a bounded approximately 20-second, 99-Hz symbolized sample during a warmed driven slowdown. Separate guest execution, GX CPU preparation and waits before choosing one correction. Use the owner's phone for a local baseline when available; it cannot establish Helio acceptance. Do not repeat #198's willingness/log requests, #167's completed resolution/aspect sweep or #103's already supplied build/settings questions. #204 is Cookie Land **battle**, not time trial. #135 A10X performance is an Apple comparison with no proven shared cause.

For baseline/candidate, hold scene, settings, normal power mode and thermal range comparable. Record frame-time tails and gaps, effective cadence, audio and health; separate cold shader compilation. Prefer three matched runs per artifact. Improvement must exceed baseline variation without graphics, audio, save or lifecycle regressions. Finish with profiling disabled.

## Second: actual failing character draw

Use the current maintained runtime and retained PNMTX evidence, rather than reconstructing the obsolete code83 candidate. #104 reports corrupt characters on code135 at1x/Normal with empty sampled shader queues. #211 independently reports failure on S24 Ultra while characters appear on Galaxy A32. Preserve selected-draw and pipeline identity, disable diagnostic draw merging when capturing, and compile the actual generated vertex shaders. Finite CPU matrices and generic passing probes do not validate the failing shader. Do not request another ISO replacement, mode sweep or duplicate log.

Use an affected device for dynamic → selected literal → dynamic comparison on the same observed character draw. A Pixel pass cannot accept corruption on affected Adreno devices. Only after the comparison discriminates the cause should a narrow correction be tested on affected and known-working hardware.

## Native TLS experiment

Ordinary builds retain Android API28. Set `KARTPAD_ANDROID_NATIVE_TLS_EXPERIMENT=1`
and an explicit `KARTPAD_ANDROID_VERSION_NAME` containing `-native-tls` to build
an API29-only candidate. Gradle uses that minimum for both the manifest and NDK
target; changing `targetSdk` alone does not enable native TLS. Use a fresh native
configuration and retain the API28 control and exact native symbols.

Package/bundle audits default to API28. Set `KARTPAD_ANDROID_EXPECTED_MIN_SDK=29`
only when auditing this experiment. Also inspect the actual native Android note,
TLS sections and `R_AARCH64_TLSDESC` relocations before attributing a result to TLS.
Use matching scene/settings and thermal range, with both profiles and lifecycle
checks. This option is not a decision to drop Android9 from the public release,
and build or relocation evidence alone is not a performance improvement.

## Ownership and release gate

Refresh issue comments and current build/device ownership before acting. One operator owns native builds and the device session. Preserve saves, profiles, identities and signing; never uninstall or clear data to cross a signer mismatch. Keep source-only experiments isolated from concurrent work.

Every handoff identifies source, version/code, APK hash, native payload, signer, exact operation and completion condition. Host checks, installation, startup, driven gameplay and online endurance are distinct evidence. Build a new public release only for a verified correction; a diagnostic is not a performance-fix release.

[Build instructions](../android/README.md) · [Physical procedures](ANDROID-PHYSICAL-HANDOFF.md) · [Performance notes](PERF.md)
