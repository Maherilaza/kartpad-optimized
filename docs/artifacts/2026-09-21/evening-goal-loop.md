# Evening issue and Android optimization loop

Started 2026-09-21 JST. Owner: Codex task `01a0c45b-6553-7c03-82bf-ab9d6d0fcf25`.
The user requested sustained useful work for eight or more hours, all-open-issue
review and replies, small tested fixes, and Android optimization informed by
the prior DriftDroid audit. The active task goal retains the full request.

## Baseline and ownership

- Current fetched main: `0d657f3`; latest stable release: 0.5.0.
- Apple build60 experimental release disables accidental forced diagnostics;
  it is a mitigation awaiting matched device evidence, not a proven FPS fix.
- Initial GitHub snapshot: 62 open issues, including new #313 and #314.
- Reuse the clean existing `kartpad-stabilization-20260918` worktree on
  `codex/evening-android-20260921`. Preserve the dirty primary checkout.
- Android maintained runtime starts at `295f4507fe1fd706f2edfa09055b815f425ed919`.
- Pixel 9 Pro XL is attached. No race or performance observation has yet been
  made by this task. Private device identifiers stay out of tracked evidence.

## Repeated cycle

1. Read every open issue and its comments; classify platform, symptom, supplied
   evidence, shipped scope, next engineering action and remaining acceptance.
   Reply specifically, acknowledge existing evidence, avoid repeated log requests,
   and record the actual comment URL. Refresh edited/new reports before posting.
2. Check recent task findings and release source before selecting one candidate.
   Prioritize actionable regressions and safe small enhancements alongside the
   sustained Android CPU work; do not substitute repeated audits for changes.
3. State one falsifiable hypothesis. Preserve a hashed baseline and relevant
   settings/data. Make the smallest source change and run meaningful checks.
4. Inspect the emitted artifact. Use matched control/candidate measurements on
   the attached device when feasible; retain scene screenshots and exact settings.
   Distinguish chooser, menus, attract/demo footage, gameplay and completed races.
5. Keep improvements with supporting evidence; reject or defer candidates with
   recorded reasons. Never convert symbol counts or microbenchmarks into FPS.
6. Update this evidence record and the existing maintenance records, commit
   reviewable changes, and continue the next useful cycle. Build/package success
   and affected-reporter acceptance remain separate. No automatic issue closure.

## Initial engineering sequence

- Verify current release linkage; test function-only local binding without
  changing Android's minimum supported API or scalar FP semantics.
- Verify Dawn cache persistence and add a safe explicit flush if still missing.
- Independently evaluate API29 native TLS; retain API28 compatibility by default
  until an explicit supported-release decision and real measurements exist.
- Review small display-list cache-copy reductions with ownership/invalidation
  checks; reprofile before selecting deeper scalar or asynchronous GX work.
- Investigate Android shake-to-trick and ghost discovery as bounded feature work.

Track actual elapsed work and outcomes. Eight hours is a requested working
window, not evidence of completion or justification for idle polling. Missing
one device or reporter does not stop other available engineering work.

## Completed first cycle

- Reviewed and replied to all 62 open issues; a fresh post-reply snapshot found
  no missing or newly opened tickets. Reply receipts are linked in the inventory.
  No issues were closed automatically. Maintenance queue tests: 65 passed.
- Commit `fe83144` adds Android RVZ picker-descriptor support. The actual Android
  DiscIO probe passed ISO plus uncompressed/Zstd RVZ byte equality, borrowed
  descriptor lifetime/offset preservation, and truncated-input rejection on the
  attached Pixel. Fixtures are synthetic; no actual game RVZ import is claimed.
- Re-linked the exact retained code135 objects as an unchanged control and with
  function-only local binding. The unchanged control reproduces the public native
  BuildID `ce82326003e7b0db832e931282f3f815195e60f2`. Candidate BuildID is
  `e27f23dbfca8367520ae8fd205787dbccd18c07a`.
- Internal jump slots fall from 10,873 to zero; remaining external slots: 610.
  Defined dynamic exports match. Stripped native size falls from 99,942,816 to
  99,168,352 bytes. Android API28 and scalar floating-point semantics are retained.
  These artifact changes do not establish a gameplay speed improvement.
- Built and audited 0.5.1-evening.1/code136 containing both changes. The attached
  device's code135 APK has identical ZIP entry contents and native digest to the
  published control, but uses the existing private test signer. A separate copy
  of code136 was signed with that verified matching identity and installed with
  `adb install -r`; installation succeeded without removing app data. Both game
  profiles still show Ready to play afterward. Public signing copy is separate.
- Physical control observations so far: Original title screen and automatic
  attract footage. The overlay visibly accepts a held A press, but the title
  screen did not advance. No user-controlled race or FPS gain has been verified.
  Input-path diagnosis and matched scene measurements remain in progress.

Private build products are under `build/evening-20260921/` in the retained
worktree; raw screenshots, reports and receipts remain ignored task-local data.
No APK release has been published by this loop.

### Continued device navigation and review

Draft PR: https://github.com/chrissotraidis/kartpad/pull/315 (receipts CI passed).
A broader Android contract selection also passed: 65 tests.

A private, temporary code137 input probe confirmed that a held A press reaches
both the JNI publisher and native consumer with matching state. A fresh run
advanced through the existing license, Single Player and VS selection screens.
The earlier failed presses are not an established source defect; their cause
remains undetermined. Temporary logging was restored out of tracked source.
Uninstrumented code138 reproduces the exact code136 native SHA256
`719c336fa56c12185c4b2e33ded09e40583a9449f3d801b651ab674a936df002`.
No race measurement has yet been made. Continue matched scene work before
making any speed claim.

### Second cycle: physical scene and cache candidate

- Uninstrumented code138 navigated through license, Single Player, VS, Mario,
  Standard Kart M, manual drift, and Luigi Circuit. Rules were read without
  changing them: 100cc, Normal CPUs, all vehicles, recommended items, four races.
  Existing resolution scale is 2x.
- Started an offline race and left the player stationary at the grid while CPUs
  circulated. Screenshots show the course introduction, lap1/time16.930, and
  eventually 12th-place results after CPUs finished. This is not a driven or
  player-completed race. Results returned to course selection successfully.
- Initial 50-second capture: nine FPS samples, median57.23 (43.63–59.66),
  ten main-thread CPU samples median14.4065ms/present, all sampled shader queues
  empty. Thermal status changed from1 before the race to2 during/after it.
  A later capture crossed toward automatic results, so it cannot support a
  matched race comparison. No linker speedup is established from these numbers.
- Built code139 with the unchanged native control; its native SHA256 exactly
  reproduces public code135 (`fd457f61e1e4ef1884ee876f8d6fc7cebd2807bcbaf002ef3f16d2a5b36a475d`).
  Installed in place. Title-screen A presses initially failed again. Returning to the native menu
  and resuming allowed input to advance; this remains an unresolved lifecycle/input
  observation, not a proven linker fix.
- Runtime branch `codex/android-evening-20260921`, commit `802bee0`, adds the
  missing static-Dawn Android Vulkan idle flush and a renderer-mutex-serialized
  background event-pump flush. Existing startup prewarm limits remain unchanged.
  Both modified files compiled with the current Android toolchain; the full native
  build completed successfully. Packaging/device cache validation is in progress. Idle-flush timing/blob-store counters will support real
  cache validation. A GitHub504 archive fetch was recovered using retained
  dependency archives and their existing CMake hash checks, then native configure.

- Control code139 reached the same stationary Luigi Circuit 100cc scene. The
  first capture had 11 FPS samples (median60.01, range36.89–60.47) and 12 CPU
  samples (median14.2935ms/present). Screenshots at race times3.018 and29.575
  confirm stationary race state. Thermal status was3 before and after, versus
  candidate1→2; captures include different amounts of loading/countdown time.
  These sequential, thermally unmatched samples establish no performance win.

- Runtime cache change is reviewable in [wiicompiled PR2](https://github.com/chrissotraidis/wiicompiled/pull/2),
  stacked on the previously pinned maintained runtime. Code140 `0.5.1-cache.1`
  completed the native build and release bundle/package audit. Native SHA256:
  `9baeca49234bc808fe21500c2d47cac5a47a0552d18e0fe0f05cb3a94214f119`.
  Private device APK SHA256:
  `45654d257d6280d528dc0b8306efde99d80056c7604b1651e404136ca9f9b2a2`.
  This is a private test artifact, not a published release.
- Refreshed all-open-issue snapshot: still62. New #215 startup success and #211
  S24 Ultra/A32 comparison were acknowledged and added to the inventory/queue.
  All65 maintenance tests passed after those updates.

### Cache lifecycle correction found by physical testing

Code140 launched with both installed profiles retained. Boot-prewarm idle flush
ran in9.989ms and recorded one blob-store callback. This confirms execution and a
store attempt, not yet successful database persistence/reuse. Home/resume worked
but two observed transitions produced no background flush.

SDL3.4.4 `SDL_SendAppEvent` dispatches application lifecycle events only to event
watchers, never to the normal event queue. The first candidate's normal event
handler was therefore unreachable. Runtime commit `3850952` moves only this
infrequent idle flush into the Android background watcher under the renderer
mutex, before the Android event pump blocks. It does not reconfigure surfaces.
It also includes cumulative blob lookup/hit counts for warm-relaunch validation.
Code141 is building; lifecycle success is not yet claimed.

Source evidence: [SDL events](https://github.com/libsdl-org/SDL/blob/release-3.4.4/src/events/SDL_events.c)
and [Android event pump](https://github.com/libsdl-org/SDL/blob/release-3.4.4/src/video/android/SDL_androidevents.c).

### Verified cache boundaries and TLS experiment preparation

Code141 `0.5.1-cache.2` passed clean build, unsigned-bundle and release-APK
audits. Its native SHA256 is
`f0176ca0fde6f072c7f844da338618739b7cbe9d0e784b9dc814b360129cc04b`;
private APK SHA256 is
`d2da47df7e21b65918dfa9aabd819078ffb4d1a1c780f66164aa0c40af3a4867`.
The first wrapper run had a post-Gradle syntax error because its script was edited
while running; rerunning the unchanged wrapper succeeded in25s with cached native
outputs. Do not edit active build scripts.

Physical code141 evidence:
- Both installed profiles remained present. Boot completed with303/303 Dawn blob
  lookups hitting; idle flush0.338ms, zero new store callbacks.
- Home at01:03:13 was followed by a background flush at01:03:14, before resume
  at01:03:18. Flush0.007ms, no new store callback. Screenshots confirm Android
  Home and a restored game title, not a race.
- After navigating into game menus, Home triggered a154.370ms flush and one
  blob-store callback (785hits/800lookups), followed by successful resume.
  This validates the corrected hook and demonstrates warm cache reads plus
  new-store activity; no isolated load-time/FPS improvement is claimed.
- A1200ms title A hold advanced but engaged the existing gas-lock feature. A
  subsequent short press released that lock before navigation. Earlier shorter
  title-input observations remain ambiguous; no input fix is claimed.

Code142 is a non-debuggable, shell-profileable API28 control. Its native hash
exactly matches code141; the profiler audit verifies every allocated ELF section
against retained unstripped symbols and verifies the device-compatible signer.

Commit `c36187b` adds an explicit, default-off API29 native-TLS experiment. Both
manifest minimum and native target change together; test version names must
contain `-native-tls`. Invalid switch/name combinations fail before building,
and the API29 package audit correctly rejects the API28 control. Ordinary builds
remain API28. Code143 is compiling in a separate native configuration; all236
translated-shard commands target Android29 without forcing emulated TLS. Final
ELF/package and physical measurements are still pending.


### Native TLS artifact and initial CPU attribution

Code143 `0.5.1-native-tls.1` completed the full build and passed bundle, APK,
profileability, signer and allocated-symbol-section audits. Native SHA256:
`06b454d263d187b3807c857b810a466c56587c802fc79befa67223725c20286d`.
Private APK SHA256:
`7006a823ef95dd783d097000c5485898d44d233fd8d99a678277392c05d4d49b`.
The ELF Android note reports API29, with `.tdata`/`.tbss` and 152 TLSDESC
relocations. The API28 control has no TLS sections or TLSDESC relocations.
This proves the intended compiler/linker change, not a performance gain.
Code143 installed in place with the existing signing identity; no app data was
cleared. Physical runtime validation is next.

Code142's exported session confirms 128 pipeline recipes warmed in 0.8 seconds,
with 303/303 blob hits, zero stores and 4.7 MiB loaded. The same session contains
native KPAD A-button edges despite intermittent title-screen navigation failure.
No input fix is claimed. Its debug-only RKG fixture path is unavailable in this
non-debuggable release candidate.

A 19.987-second code142 **title/attract sequence** simpleperf capture recorded
1,822 CPU-cycle samples with zero samples lost. This is not a race benchmark.
Build-ID-matched unstripped symbols identify the largest self-costs as translated
functions `801B4DA8` (13.02%), `801B5234` (5.83%) and `801B5B74` (4.43%).
Emulated TLS lookup was 1.41%, with `pthread_getspecific` at 1.09%; these are
sampled shares in this sequence, not predicted whole-game speedups. Frame-pointer
unwinding reported 30.4% erroneous callchains, so inclusive/caller attribution is
not reliable enough for conclusions. Self samples provide the next investigation
targets. The supported `simpleperf record --app` path works without rooting or
changing kernel security settings.

A separate uncommitted display-list experiment replaces five per-hit array copies
with const references to the thread-local cache record. Cache insertion/eviction
remains confined to the miss branch, which uses local scratch arrays. Both versions
compile with the production API28 flags; the affected function's machine code is
7,216 bytes before and 7,172 bytes after. Runtime correctness and performance are
still pending; this experiment is not in a pinned candidate or public release.


Code143 physical follow-up: both profiles remained ready, Original launched and
rendered the title/attract sequence, and a second 19.986-second CPU profile captured
1,817 samples with zero lost. The same three translated functions were largest
self costs (17.94%, 9.46%, 4.47%). Emulated TLS lookup fell to two samples/0.10%
and `pthread_getspecific` had no self samples in this capture. Scene timing,
thermal conditions and sample counts are insufficient to infer a whole-game
speedup. Callchain errors were 2.37% in this capture, versus 30.4% in code142;
do not attribute that difference to TLS without a controlled unwinding test.
Title A navigation remained intermittent with both 500 ms and 1,200 ms presses;
the latter's intentional cyan gas lock was cleared with a short tap. No race
was reached on codes142/143. The next optimization work should retain this
boundary while investigating the measured translated CPU hotspots.


### Profile interpretation corrected before optimization

The public [RMCP01 symbol map](https://github.com/doldecomp/mkw/blob/main/config/RMCP01/symbols.txt)
identifies the three title-profile hotspots as `__THPInverseDCTNoYPos`,
`__THPInverseDCTY8`, and `__THPHuffDecodeDCTCompY`. They decode the THP movie;
they are not evidence of the race simulation bottleneck. Keep this profile as
startup/movie attribution and obtain an actual race or explicit retail replay
profile before selecting gameplay optimizations.

The existing September 3 Android replay investigation also rejects assuming
that injected RKG player input naturally completes a race: it diverged on three
courses. Retail Watch Replay was useful rendering evidence but did not prove
player results/save. An optimized private capture build is being prepared for
input inspection and repeatable scene selection, preserving the normal native
runtime and installed data. The display-list array experiment was saved to an
ignored patch and removed from the maintained source while building this control,
so it cannot confound the input/TLS investigation.
