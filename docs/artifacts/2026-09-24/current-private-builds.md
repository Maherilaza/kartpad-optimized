# Private build status — 24 September 2026

This records what the current unpublished builds have actually proved. It is
not a release note or a claim of device acceptance across platforms.

| Platform | Current private build | Evidence | Remaining gate |
|---|---|---|---|
| Android | Pixel retained build: `0.5.1-android-nightly.14`, code 208. New emulator candidate: `0.5.1-replaygen.1`, code 209. | Code 208's archived APK and the copy pulled after its in-place Pixel 9 Pro XL install have the same SHA-256, `a8b0d1867fe654d373b6044687b3b1e9593160163881c9be13aaa6f28e167579`. Candidate 203, whose source was rebuilt as 208, ran an active stationary 12-kart Cookie Land battle on that Pixel: 12.652 ms game-thread CPU per presented frame versus 14.70–14.79 ms for build 195 in comparable runs. Code 209 passed the release APK audit, installed over code 205 on the API 36 ARM64 emulator, and reached an active Luigi Circuit time trial twice. Its same-course second load logged pipeline replay again. | Code 209 has no physical-device comparison or smoothness measurement. The Pixel still has code 208; its package/readback check does not constitute a new measured gameplay run. Retro pipeline replay logged zero recorded and zero queued on the tested physical course. Driven races, Samsung/Adreno devices and online play remain open. |
| iPadOS | `0.5.1` build 66, signed development app; no IPA packaged | Built from the current iOS runtime with guarded DVD DMA copies and GX scene-generation repair. The physical iOS app audit and strict signing check passed. It installed in place over build 65 on the iPad Pro, reports build 66, and launched as PID 999. The game image and 34 state files were backed up and read back byte-identical. The earlier build 65 reached the KartPad launcher with both games Ready to play. | Build 66 has no visual KartPad launcher or game-boot check: another app was foreground on the iPad during the mirror inspection, and the build 66 process transcript only shows startup and health samples. Original, Retro, WFC, replay and performance still need physical gameplay checks. |

The source branches and submodules have moved beyond the physical-device
artifacts. Guarded DVD DMA bulk copies are in all four runtime submodules and
passed C++ syntax checks. Android code 209 includes that change and a
scene-generation fix in its Android runtime. The fix invalidates both GX
pipeline memos when a course load begins, allowing previously seen recipes to
reach the scene recorder again. The iOS source has the same fix; macOS and tvOS
have only the DVD change. The iPad build 66 includes the iOS changes, but has
not been driven into either game.

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

The build 66 iPad receipt is in `work/ios66-install-20260924/`. It was built
from a fresh stage of iOS runtime `0df334c` plus the build-number change later
committed as `e5902c8`. The unsigned executable SHA-256 is
`09d7af226fa11ec53d4228fdea1e5077896ff164d955b2a241da9e3ce6373db9`;
its Mach-O UUID is `4459EAE6-B408-301E-A257-D2E2FD3D5E85`. The existing
development profile and signing identity were reused. A fresh pre-install
backup and post-install readback matched for the 2.6 GB game file (SHA-256
`fc035e60610842da6860d23d4a30c1f1c0f019d492469deb8a2ac25ef5822331`)
and all 34 other files. The build 66 process transcript confirms PID 999 and
version `0.5.1` build 66, but contains no game boot. A wired mirror displayed
another app in the foreground, so KartPad was left undisturbed pending an
available iPad session.

The handoff's GX, Adreno and floating-point proposals remain
hypotheses or bounded experiments. In particular, the available shader evidence
does not prove an Adreno driver defect, and a lower game-thread CPU number does
not by itself establish smoother presentation.

Evidence: [Pixel comparison](../2026-09-23/android-copy-stream-loop.md),
[Android build 195 baseline](../2026-09-23/android-morning-report.md), and
[deep review](deep-review-handoff.md). The private receipts and APK are under
`work/android-optimization-20260923/`; the iPad install/readback receipts are
under `work/ios65-install-20260923/` and `work/ios66-install-20260924/`.
Those directories contain private or
game-derived material and are not release assets.
