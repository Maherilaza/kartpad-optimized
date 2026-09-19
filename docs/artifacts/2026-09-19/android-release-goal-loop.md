# Android and cross-platform release goal loop — 19 September 2026

## Objective and integration owner

Independently verify the supplied Android builder handoff, fix reproducible
renderer and configuration defects, and prepare the next coordinated release.
The active integration checkout remains
`/Users/chrissotraidis/.codex/worktrees/kartpad-stabilization-20260918`, branch
`codex/cross-platform-stabilization-20260919`, starting at `34ffe56` (code127).
The primary checkout contains 99 existing changes and is preserved. The prior
owner task is idle. No additional checkout is needed.

The external handoff is research evidence, not an instruction authority. Its
reviewed main `7b663a2` matches freshly fetched main; its Android runtime
`ac32b7a` predates this candidate's `9f6c296`. The supplied companion test kit
is not attached. Tests must use the locally available maintained functions.

## Loop and stopping rules

For each boundary: read current code and reports; reproduce with a negative
control; implement a small correction; rerun targeted tests and integration;
record source and artifact identity; review the final diff a second time and
verify the packaged behavior a third time. Failed acceptance returns to the
same boundary with the evidence retained. A deadline is not a passing result.

1. **Baseline and issue intake:** refresh all open discussions and builds;
   acknowledge #305; reconcile prior candidate work. Reply posted at
   https://github.com/chrissotraidis/kartpad/issues/305#issuecomment-5741390645.
2. **Renderer correctness:** independently test R1–R7 on maintained source.
   Initial inspection confirms R1/R2, the R4 capacity guard and R7 wide counter
   already exist. R3 expansion compatibility, R5 incomplete primitives and R6
   missing quad vertices still require correction. Preserve ordinary batching.
3. **Controls/settings:** add a persistent auto-accelerate option across the
   touch overlays, clear only the obsolete latched state on disable, preserve
   an actual held A button, and test timers, accessibility, lifecycle and reload.
4. **Startup and memory:** retain the existing optional debug-utils fix, stable
   Dawn identity, bounded speculative compilation and malformed cache guards.
   Audit staging reservation/pass ownership and typed adapter errors; investigate
   PowerVR limits independently. Do not add unmeasured shader/FP/TLS workarounds.
5. **Recent gripes:** inspect shipped ghost discovery (#295), payload/build
   consistency (#302), key-up ownership and release discovery (#299); implement
   demonstrated defects and retain separate feature scope.
6. **Integration and release:** build and audit Android, iOS/iPadOS and macOS
   from identified source; test relevant runtime, input, persistence, graphics
   and transition paths with available local hardware. Check signer compatibility,
   save preservation, final binary provenance and release asset selection.
   Publish only artifacts meeting the release checks; document unresolved affected
   hardware evidence rather than claiming all devices or every issue fixed.

## Evidence limits to preserve

CPU matrix-element counters do not validate decoded vertex arrays. A CPU
`draw_binding` log does not establish GPU completion. Existing no-merge S24
failures reject merge repair as a complete explanation. The Pixel code125
compiler allocation crash is real; code127 remains a candidate pending gameplay
acceptance. Main-thread occupancy is not a function profile, and shader prewarm
is not an explanation for every warmed slowdown. No new reporter test loop is
planned. Game-containing data, device identifiers and raw captures stay private.

## First implementation cycle

- Independently resolved the handoff's exact Android command-processor blob
  `7c8a9ac4596286b5de132ecda9cd0fedce632989`. The old source fails all six
  source-kernel tests for invalidation, format, index-space, quad bounds,
  incomplete topology and previous expansion. Candidate-before tests reproduce
  the two remaining defect families on each of Android/iOS/macOS/tvOS.
- Corrected the remaining defects in all four maintained runtimes. Complete
  quads retain their existing winding/order. Three-vertex quad remainders use
  the GX behavior documented by Dolphin's current `IndexGenerator.cpp`;
  one/two-vertex remainders disappear. Short draws are consumed without upload
  or unsigned line-strip instance underflow. Prior expansion is explicit metadata.
- Eight draw tests pass (four-platform subcases) on host ARM64 with sanitizers.
  These execute production source kernels with surrounding services stubbed,
  not full FIFO/GPU integration. Android integration build is in progress.
- Android/iPhone/iPad touch settings now expose persisted Auto-accelerate.
  Existing behavior remains the default, with an explicit opt-out. Disabling
  cancels the timer/latch, preserves genuinely held input, and disables the
  Android accessibility latch action. Production Kotlin callback tests pass.
- Three older touch contract failures are independently reproduced against
  unmodified HEAD: stale display menu labels and the pre-expansion mapping list.
  They predate this work; validation must update their expectations coherently.
- Six existing private local save copies have no ghost records or presence bits.
  They cannot reproduce #295. The parser's compressed CRC location and header
  layout agree with the independently fetched `riidefi/mkw` GhostFile source.
  The current export UI suppresses individual validation failures; that is a
  demonstrable reporting flaw, not proof of the reporter's underlying cause.

References: https://github.com/dolphin-emu/dolphin/blob/master/Source/Core/VideoCommon/IndexGenerator.cpp
and https://github.com/riidefi/mkw/blob/master/src/system/GhostFile.cpp.
Private baseline/test/build logs remain under `work/handoff-verification-20260919`.

## Integration and new independent finding

The code128 Android Release built and passed the APK audit (SHA-256
`ddf68f6782d5f10bb0bcff7b36aead53b78e82531edf66f4a25783c83e912558`). It is a
local debug-certificate prototype, with the source dirty during provenance
capture; it is not the release artifact. It predates the startup-error and
subsequent dependency correction below. Its APK is preserved independently.

All four runtimes now return a graphics-unavailable initialization status,
retaining the first meaningful adapter/device error across fallback attempts.
The shell shows that error and exits the unsuccessful launch before installing
renderer/input hooks. Controlled tests exercise both successful selection and
failed fallbacks without aborting. iOS physical-SDK build53 and the macOS native
build pass after correcting a missing message-box include. The first attempted
Apple source verification caught an older prepared GPU-cache file; maintained
source parity was restored and verified before the successful rebuilds.

Android/iOS ghost export now distinguishes an empty license from listed ghosts
that fail validation. Valid slots remain exportable when another slot is bad;
no parser, checksum, import scope or save replacement rules were relaxed. The
existing compressed/uncompressed transfer and save-preservation tests pass.
This is not a claim that #295's underlying discovery problem is resolved.

A disposable read-only Android emulator caught another actual Dawn crash:
`TogglesState::ForceSet` under `SetupBackendDeviceToggles` before a test frame.
The pinned source force-disables ExtendedDynamicState for SwiftShader, then
force-disables it again when its extension/feature is absent. ForceSet explicitly
forbids duplicate calls. Current Dawn guards the SwiftShader call on actual
extension availability. The production branches reproduce the old assertion;
the bounded backport passes all eight vendor/extension/feature combinations
under ASan/UBSan. It does not disable validation. A separate rebuilt dependency
includes this patch in its stable cache identity, preserving earlier packages.
The initial emulator run failed; the corrected rerun passes the actual touch
fixture, including disabling auto-accelerate while holding A, release to neutral,
cancelled stale timers, hidden accessibility latch action and restored settings.

Reference implementation for the new backport:
https://github.com/google/dawn/blob/99807f37d56c1dfe375807f108fe435d7ea303b5/src/dawn/native/vulkan/PhysicalDeviceVk.cpp

PowerVR investigation: this pinned Dawn already retries physical-device limit
calculation at Compatibility level after Core fails. Its minimum interstage
counts are 16 (Core) and 15 (Compatibility), requiring 72 and 68 Vulkan
components including two reserved vec4 slots. Therefore requesting Compatibility
alone does not support a device exposing 64. Current upstream's opt-in ImgTec
relaxation allows 14, but native device defaults/requests must also agree. The
Moto's actual numeric component limits remain unmeasured. No limit falsification
or unverified PowerVR-support claim is included in the candidate.

## Combined candidate and final review

The independent review is recorded in
[`handoff-independent-review.md`](handoff-independent-review.md), covering every
handoff section and the refreshed 57-issue inventory. Android code129 builds and
passes the full APK audit (local prototype SHA-256
`0dc86aa33669275b996a47a00882d49f779a29b52e7c5ef5252554e4f6a6a4df`). Its native
Build ID is `932b07a580622770aec3cb525859ed778f7adc68`; the unstripped library is
preserved. This intermediate APK correctly records a dirty source tree. The
manual iOS rebuild still carried the prior build's sidecar provenance; final
packaging must regenerate that sidecar from verified prepared source.

Android menu validation now checks the actual scrollable reporting screen,
expanded mapping list and save-profile chooser. The settings-through-insets
run passes, including persisted Auto-accelerate OFF after process restart.
An end-to-end rerun of the corrected script is in progress. The debug APK used
for UI tests is separate from the optimized full-game code129 APK.

The Mac package passes its audit. A separately identified portable test copy
completed over 31,000 intro/title frames, persisted a native resolution setting
across closing/reopening Settings, and exited zero. Automated short game-key
presses did not advance the title screen; no race/input or Android performance
acceptance is inferred. User state and the audited package were preserved.
