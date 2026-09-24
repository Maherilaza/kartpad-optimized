# Private build status — 24 September 2026

This records what the current unpublished builds have actually proved. It is
not a release note or a claim of device acceptance across platforms.

| Platform | Current private build | Evidence | Remaining gate |
|---|---|---|---|
| Android | Pixel retained build: `0.5.1-android-nightly.14`, code 208. New emulator candidate: `0.5.1-replaygen.1`, code 209. | Code 208's archived APK and the copy pulled after its in-place Pixel 9 Pro XL install have the same SHA-256, `a8b0d1867fe654d373b6044687b3b1e9593160163881c9be13aaa6f28e167579`. Candidate 203, whose source was rebuilt as 208, ran an active stationary 12-kart Cookie Land battle on that Pixel: 12.652 ms game-thread CPU per presented frame versus 14.70–14.79 ms for build 195 in comparable runs. Code 209 passed the release APK audit, installed over code 205 on the API 36 ARM64 emulator, and reached an active Luigi Circuit time trial twice. Its same-course second load logged pipeline replay again. | Code 209 has no physical-device comparison or smoothness measurement. The Pixel still has code 208; its package/readback check does not constitute a new measured gameplay run. Retro pipeline replay logged zero recorded and zero queued on the tested physical course. Driven races, Samsung/Adreno devices and online play remain open. |
| iPadOS | `0.5.1` build 65, signed development app; no IPA was packaged from this build | The installed app passed signing checks. Thirty-five owner files were backed up and read back byte-identical after the in-place install. On 24 September, a fresh launch succeeded and a screenshot showed the KartPad launcher with both games Ready to play and the Ask every time preference. Source adds the iOS course replay and unobserved FP status work; a host FP differential passed 3 million cases. | Four earlier launch attempts were denied because the iPad was locked. The successful launch proves the app reaches its launcher, not that Original or Retro boot, play, connect to WFC, or replay pipelines. Verify those paths with the existing profiles before packaging an IPA or making a performance claim. |

The source branches and submodules have moved beyond the physical-device
artifacts. Guarded DVD DMA bulk copies are in all four runtime submodules and
passed C++ syntax checks. Android code 209 includes that change and a
scene-generation fix in its Android runtime. The fix invalidates both GX
pipeline memos when a course load begins, allowing previously seen recipes to
reach the scene recorder again. The iOS source has the same fix; macOS and tvOS
have only the DVD change. No Apple package or device run includes these changes.

Code 209 was built from Android runtime `f1677be`, with the private translated
shards, as `work/android-replaygen-20260924/kartpad-code209-replaygen.apk`.
SHA-256: `e34fc03afdb821dc641641323b8b017921b04a6c9cc5c52ad77a13f42f50cc61`.
The release audit verified version code 209/name `0.5.1-replaygen.1`; its APK
signer SHA-256 is `61dfb51411efe50b2e7fb8d280fcfbba766792c275d1024013940760caa3afaf`.
The emulator retained its app data through `adb install -r`. In one console
session, the first Luigi Circuit course load logged scene `c245398c16435baa`
with **213 recorded, 172 queued**. Selecting Change Course and the same Luigi
Circuit again logged the **same scene** with **342 recorded, 0 queued**; the
second race reached active gameplay. Restart within the race did not log a new
scene load, so it is not a replay-path check. The emulator already held a cache
from prior builds, and an empty second queue does not establish a startup or
frame-time improvement. The console and screenshots are in the same private
`work/android-replaygen-20260924/` directory.

The handoff's GX, Adreno and floating-point proposals remain
hypotheses or bounded experiments. In particular, the available shader evidence
does not prove an Adreno driver defect, and a lower game-thread CPU number does
not by itself establish smoother presentation.

Evidence: [Pixel comparison](../2026-09-23/android-copy-stream-loop.md),
[Android build 195 baseline](../2026-09-23/android-morning-report.md), and
[deep review](deep-review-handoff.md). The private receipts and APK are under
`work/android-optimization-20260923/`; the iPad install/readback receipts are
under `work/ios65-install-20260923/`. Those directories contain private or
game-derived material and are not release assets.
