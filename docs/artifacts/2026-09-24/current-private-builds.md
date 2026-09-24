# Private build status — 24 September 2026

This records what the current unpublished builds have actually proved. It is
not a release note or a claim of device acceptance across platforms.

| Platform | Current private build | Evidence | Remaining gate |
|---|---|---|---|
| Android | `0.5.1-android-nightly.14`, code 208, rebuilt from retained candidate 203 | The archived APK and the copy pulled after its in-place Pixel 9 Pro XL install have the same SHA-256, `a8b0d1867fe654d373b6044687b3b1e9593160163881c9be13aaa6f28e167579`. The installed version and both Ready to play launcher entries were checked. Candidate 203 ran an active, stationary 12-kart Cookie Land battle on that Pixel; its measured game-thread CPU was 12.652 ms per presented frame, versus 14.70–14.79 ms for build 195 in comparable runs. Home/resume and pause/continue returned to active gameplay. | Build 208 itself is a package/readback check of the retained 203 source, not a new measured gameplay run. Retro pipeline replay logged zero recorded and zero queued on the tested course. Smoothness, driven races, Samsung/Adreno devices and online play remain open. |
| iPadOS | `0.5.1` build 65, signed development app; no IPA was packaged from this build | The installed app passed signing checks. Thirty-five owner files were backed up and read back byte-identical after the in-place install. On 24 September, a fresh launch succeeded and a screenshot showed the KartPad launcher with both games Ready to play and the Ask every time preference. Source adds the iOS course replay and unobserved FP status work; a host FP differential passed 3 million cases. | Four earlier launch attempts were denied because the iPad was locked. The successful launch proves the app reaches its launcher, not that Original or Retro boot, play, connect to WFC, or replay pipelines. Verify those paths with the existing profiles before packaging an IPA or making a performance claim. |

The source branches and submodules have moved beyond these exact artifacts.
The current unbuilt DVD DMA bulk-copy candidate is in the four runtime
submodules; it has passed C++ syntax checks, but has no package or device
measurement. The handoff's GX, Adreno and floating-point proposals remain
hypotheses or bounded experiments. In particular, the available shader evidence
does not prove an Adreno driver defect, and a lower game-thread CPU number does
not by itself establish smoother presentation.

Evidence: [Pixel comparison](../2026-09-23/android-copy-stream-loop.md),
[Android build 195 baseline](../2026-09-23/android-morning-report.md), and
[deep review](deep-review-handoff.md). The private receipts and APK are under
`work/android-optimization-20260923/`; the iPad install/readback receipts are
under `work/ios65-install-20260923/`. Those directories contain private or
game-derived material and are not release assets.
