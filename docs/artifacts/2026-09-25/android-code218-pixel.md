# Android build 218 — installed on Pixel, performance unverified

## Current state

On 25 September 2026 at 09:19 JST, private build 218
(`0.5.1-gx-nodraw.2`) installed successfully over build 208 on the Pixel 9 Pro
XL using `adb install -r`. No uninstall, data clear, downgrade or identity
reset was performed. The package retains its original first-install date.
The owner authorized the update for testing. Work is now focused on Android;
Apple build and gameplay work is deferred.

The APK pulled from the phone after installation matches the audited candidate:
`601f6e57479546af14fafb3b9c069a1ddae41e962164612c0813cfa8e018ee1f`.
Its signing certificate matches installed build 208:
`61dfb51411efe50b2e7fb8d280fcfbba766792c275d1024013940760caa3afaf`.
The old installed APK was archived before replacement with SHA-256
`a8b0d1867fe654d373b6044687b3b1e9593160163881c9be13aaa6f28e167579`.

The release app denies `run-as`, so no fresh private save/config/identity
backup or byte-for-byte readback was obtained. The phone was in active use;
its screen was left alone during installation. In-place package replacement
is verified; game-data readiness, the existing licence, and identity continuity
still need an app-level check. No physical game launch or performance result
is claimed for 218.

## Changes since 208

| Builds | Change | Intended benefit |
|---|---|---|
| 209 | Guarded block DVD copies; course-generation pipeline recording | Reduce copying overhead and record pipelines for subsequent course visits |
| 210 | Guarded host-buffer Yaz0 decoding | Reduce asset decompression overhead |
| 211 | Eight-handle per-thread DVD file cache | Avoid repeated opens for reads of the same files |
| 212 | Ordered fatal-exit handling | Preserve the original error and stop workers without a secondary destructor abort |
| 213 | StaticR module hash validation | Reject incompatible game code before launching |
| 214 | Native Android display-rate hint | Request a display rate matching the selected game output |
| 215 | Adjacent XF loads batched within a direct burst | Reduce graphics-command call overhead while preserving ordering boundaries |
| 216 | Direct handling of the translated three-write display-list command | Reduce calls in the graphics path identified in the Pixel profile |
| 217–218 | Bounded register-only list classification cache; expanded entry limit | Avoid repeating classification scans; retain an 8 MiB copied-command limit |

Source also adds module-prolog failure context for #196 and clarifies the
setting label as Touch auto-accelerate. Neither is a performance improvement.

## Verification and limits

The exact APK passed the release package audit again immediately before
installation. Shared runtime parity and the production GX burst host test
passed again. Earlier emulator checks established races for 209–211, an
ordered fatal exit for 212, modified-module rejection for 213, acceptance of
the rate hint for 214, and title rendering/cache reuse for 216–218.
Those checks do not establish a physical Android speedup or an Adreno fix.

Private receipts are under `work/android-pixel-comparison-20260925/`:
`install-receipt.json`, `package-after.txt`, `code218-audit.log`, and the
before/after installed APKs. The candidate is
`work/kartpad-code218-gx-nodraw-bound.apk`, built from Android runtime `27074c2`.
No public release or merge was performed.

## Next Android gates

1. Open Original and Retro; confirm existing data and licence remain available.
2. Check active gameplay for visual regressions, crashes, and audio problems.
3. Measure stationary Original Cookie Land Balloon Battle at 2x with 11 CPU
   opponents: game-thread CPU/present, compositor intervals, and thermal state.
   The archived build-203/208 result of 12.652 ms CPU/present is historical;
   there is no fresh same-session build-208 baseline from this installation.
4. If a fresh A/B is needed, rebuild the baseline source under a higher version
   code and install in place. Do not downgrade or remove the app.
5. Investigate measured regressions or remaining hotspots before another
   optimization round. Adreno rendering and Retro/WFC require their own checks.
