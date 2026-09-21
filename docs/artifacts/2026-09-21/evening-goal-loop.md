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


### Diagnostic build and rejected debugger capture

Code144 `0.5.1-native-tls-input-capture` built successfully with optimized native
flags. Package identity, API29 minimum, ARM64/alignment checks and the existing
private signer passed. Every allocated native section matches retained symbols.
APK SHA256 `98a3036595bf42df96359a54c65f5494fe6b6bdd1c274a4cab37572f80a63fbc`;
native SHA256 `0dc3f97b77247e6c65177ff23b2e0046f625919bab075a1474925be44c8c2459`.
It is deliberately debuggable, so it is not a public release or a substitute for
the non-debuggable profiler acceptance gate. Installation preserved both ready
profiles. Before further diagnostics, both existing `rksys.dat` saves and all
five preference files were copied to a private host backup with per-file hashes.
No fixture or steering marker was present, and none was installed.

A bounded LLDB input trace attached without root and observed one Unified WPAD
read followed by one KPAD read in the same presentation frame. It then encountered
a Vulkan device loss (`vkQueueSubmit` / `VK_ERROR_DEVICE_LOST`) after debugger
pauses. The backtrace reaches Aurora's device-loss fatal path; the debugger was
detached and its port forwarding removed. Reject this run as stability,
performance or input-fix proof. The two neutral samples do not establish the
input-loss hypothesis. Further input tracing must avoid stop-the-world pauses.


Code145 adds bounded, private, marker-enabled logging without debugger pauses.
It passed the package audit and device-signer check and installed in place.
A 500 ms title A press was observed by both Unified and KPAD readers from
presentation frame1436 onward. KPAD generated Classic A trigger `0x10` at1436,
then reported A held through1458 and released at1462. The title did not advance.
Thus a consumed short edge does not explain this held-press failure; the next
trace observes the guest controller's stored raw state and UI output. No input
behavior has been changed. These transient diagnostics remain outside the PR.

Fresh preparation preserved file timestamps only after byte-for-byte equality
checks against the retained control: 857 unchanged files, with `kpad.cpp` alone
changed. Source verification still runs normally. This lets the native build
recompile the actual changed input unit without rebuilding unchanged translated
shards; it does not reuse changed source or weaken the preparation check.


Code146's additional read-only trace shows the guest controller connected and
retaining raw Classic A (`0x10`) across the held press. The title still does not
advance. UI fields sampled at the start of controller calculation are zero, but
the caller may clear those outputs before calculation; that is not evidence of
lost input. A further private trace samples the completed UI state at presentation
instead. This narrows the investigation beyond Android delivery and raw KPAD
consumption without introducing a speculative input fix.


Code147 samples after controller calculation at presentation. During the 500 ms
press it observes mapped UI A (`0x0001`) and raw Classic A (`0x0010`) through
frames1617–1644, then release at1645. The title still ignores the press. The
private trace initially named UI offset6 `trigger`; inspection of the translated
Classic controller shows that field copies raw buttons. It is not a trigger or
proof that the page handler received an edge. The next trace corrects that label
and inspects controller registration. No behavior fix or gameplay improvement
is claimed from these title-only runs.


Code148 passes the package/signature checks and installs in place. Its title
trace confirms the UI state is marked valid (`0x80`) while A is held, and the
player-one registration passes the game's current/expected-controller equality
check. The registered controller proxy still needs to be followed to its
selected pad; merely seeing A in the separately calculated Wii pad does not
prove it is the pad the menu reads. Latest PR checks at `70aeda9` all pass
(boundaries, receipts, regression).

Code149 follows the registered player-one proxy to its selected pad. It points
to the same Wii/Classic pad previously traced, with mapped A1, raw A16 and
valid128. Reject wrong-controller selection as the explanation for this run.
A subsequent private trace inspects active pages rather than changing the
Android button route. Codes148/149/150 are transient optimized debug captures,
not public binaries or FPS evidence.


### Apparent title input failure resolved as a test-state mistake

Code150's active-page trace reveals OpeningMovie (page89) above Title (page87),
although the screenshot still shows the title artwork. The held A press causes
page transitions and removes the movie page; it does not represent an ignored
button. Three short 300 ms A presses separated by 800 ms then reach the main
menu, with intervening screenshots retained privately. This corrects the earlier
claim that the title was ignoring A: delivery, selected-pad state, and page
transition all worked. No input behavior change is warranted from this run.

All private traces were saved as ignored patches and removed from maintained
source. The task-created InputTrace marker was removed. A normal non-debuggable
API29/TLS profiling candidate is rebuilding so title diagnostics cannot confound
the next gameplay measurement.

Preservation readback after150 matches all seven backed-up files byte-for-byte:
both saves and all five preference files. Code151 passes the non-debuggable
profiler audit, exact-symbol allocated-section comparison, API29 package audit,
and recipient-signer check. Its native SHA256 is identical to code143
(`06b454d263d187b3807c857b810a466c56587c802fc79befa67223725c20286d`),
confirming the private input instrumentation is absent. APK SHA256:
`b8dade7d86e4ede910c268dd584764ddc91a7f607ecc971d4ec5c5a6882e8adb`.


### Moving retail replay profile

Code151 reached Original → Time Trials → Luigi Circuit → Nin★sato 1:29.670 →
Watch Replay. Screenshots before and during capture show the translucent Luigi
ghost at different course positions. This is retail replay validation, not
human driving or player completion/save proof. At2x resolution, a29.9884-second
profile recorded3,394 samples with0 lost. Both thermal snapshots reported3.
Six five-second telemetry samples within the capture window gave median60.00FPS
and9.146ms main-thread CPU per present (range9.018–9.797ms). Window endpoints
are inferred from the recorder's completion timestamp, so this is initial
attribution rather than a precisely synchronized A/B benchmark.

Largest named self costs: GX display-list call4.33%, scalar-flag clear2.79%,
Aurora FIFO processing2.46%, scalar-flag capture2.32%, native TLS resolver2.16%.
The sample attribution supports testing the saved display-list array-reference
change. It does not justify changing floating-point semantics. Code152 builds
that single runtime change on the same API29/TLS configuration; source review
confirms cache-hit references are consumed before drawing/possible recursion,
and cache stores/evictions occur only in the miss branch before binding them.

Code152 passes the same release/profileability/symbol/signer audits and renders
the moving staff replay. Native SHA256:
`4453dd56927573fe69c4dc3b542f9821b47733fc8f35b2f8947b5e128fdf6ff9`.
Its29.9863-second capture has3,424 samples,0 lost. Thermal remains3. Seven
telemetry samples give median59.95FPS and9.540ms CPU/present, versus9.146ms
for151 in a different replay window. No performance benefit is established.
The display-list self share is4.11% versus4.33%; this difference alone is not
a speedup measurement. The array-reference change remains an uncommitted
experiment pending stronger evidence.

Mapping sampled instruction addresses to the exact retained152 symbols locates
substantial work in hash-bucket lookup and vertex-snapshot construction, rather
than assuming the five copies dominate. Cache telemetry shows about760 records
and only roughly22% front-table hits. Code153 is testing1,024 direct-lookup
slots instead of256 (12KiB additional thread-local storage), retaining full
identity/content validation and clearing the front table on eviction. It is
not yet accepted or included in the maintained runtime pin.


### Larger front-table measurement (September22, 02:52 JST)

Code153 passed release-package, non-debuggable shell-profileability, exact
allocated-section/symbol and recipient-signer audits, then installed in place.
The same Luigi Circuit staff replay rendered at2x before and after a29.98-second
capture:3,567 samples,0 lost, thermal status3 at both endpoints. Seven telemetry
samples in the device-timestamp window gave median59.98FPS and9.693ms CPU per
present (9.392–9.739ms). The front-hit fraction increased to47.19% from roughly22%
with256 slots, but GX display-list self cost remained4.08% and no CPU improvement
is established. These different replay windows do not constitute matched A/B
acceptance. Neither display-list experiment is included in the maintained pin.

APK SHA256: `3e4519b269dfdf3e4c726cf8b17956171cf869605c5bb1eec201bf4b851c258b`.
Exact native symbols and private screenshots/profile/thermal logs are retained
locally. Next: remove unnecessary vertex-snapshot default construction with
explicit state-restoration tests, then compare synchronized replay windows.
PR315 boundaries, receipts and regression checks all passed at this checkpoint.


### Vertex snapshot candidate (September22, 03:01 JST)

Code154 returns to the maintained256-slot/cache-array-copy behavior and changes
only vertex snapshots: format/array storage holds object bytes without default
constructing208 formats, and capture fills its destination directly. Descriptor
storage stays typed because the fallback vertex submitter reads it directly;
the full Android compiler caught that dependency in the first draft, which was
corrected before packaging. Partial restoration still uses the original presence
flags and format-row mask. Trivially-copyable assertions guard the copied types.

The production capture/restore functions pass16,416 isolated state cases under
ASan/UBSan:32 state patterns, full restoration, every CP register, and all256
format-row combinations including duplicate writes and empty writes. This does
not substitute for renderer acceptance. Full dual-runtime Android build passes,
as do release/signer/profileability/exact-symbol audits. The ARM64 display-list
function is0x1a3c bytes. Code154 is installed in place and reaches the menus;
longer replay performance comparison remains pending. Fourth issue refresh still
shows62 open issues and no new reporter update since the previous review cycle.

APK SHA256: `fed37223970738e7c25a2ceb5147481b4e7d603180d22e1145e6bbd925c6acff`.
Native SHA256: `bb13961dd3f9ec7302c3fa4e8ddba48856ebdcbf113fdb97a615bb25bff7b224`.
Runtime change and the new contract test remain local experiments pending device
comparison; the maintained child pin is unchanged.


Code154's89.9943-second retail staff replay capture records12,186 samples,0 lost.
Before/during/after screenshots show the ghost at different course positions.
Excluding the first6 seconds of telemetry to avoid a partial initial interval,
17 samples give median59.88FPS and9.828ms CPU/present (8.666–10.471ms), with
thermal status3 before/after. GX display-list self share is3.20%. This is a
longer attribution capture, not yet evidence of an overall speedup. The exact
function shrinks from0x1c9c bytes in151 to0x1a3c bytes in154.

Control155 is built and audited, with native SHA256 byte-identical to151. Its
APK SHA256 is `67f8678e4374c74cc49b13ed4bbc98488dbbf8a2686b7f1deee99e615eb6c53c`.
It is not installed at this checkpoint. The child checkout is temporarily back
at its clean maintained source for that control build; the154 candidate source,
patch, prepared tree, symbols and package are retained locally. The contract
test is pending alongside that experiment and expects the candidate signatures.
Next step: install155 in place and collect the same longer staff-replay profile,
then repeat the candidate before accepting or rejecting it.


### Snapshot candidate/control/repeat (September22, 03:15 JST)

All three runs use Original, the same Luigi Circuit staff ghost,2x resolution,
API29 native TLS, non-debuggable profileable packaging, and thermal status3 at
both endpoints. Each records90 seconds at99Hz. Telemetry excludes the initial6
seconds to avoid counting an initial partial five-second interval. The replay
loops; these are retail staff-replay observations, not driven races or save proof.

| Build | Native behavior | CPU median ms/present | FPS median | GX DL self share | Samples/lost |
| --- | --- | ---: | ---: | ---: | ---: |
|154|Snapshot candidate|9.828|59.88|3.20%|12186/0|
|155|Original snapshot control|10.070|59.99|3.86%|10636/0|
|156|Byte-identical candidate repeat|9.947|59.89|2.76%|9883/0|

The control's45 samples in vertex-format default constructors disappear in both
candidate captures. Estimated sampled display-list cycles fall from6.260 billion
in the control to5.243 billion in154;156 again has lower display-list self cost.
The source change removes that work rather than changing guest state semantics.
CPU medians are1.2–2.4% lower in the two candidate runs, but this is a small local
observation with unsynchronized replay phase, variable scheduling/clocks, and
one device/course. It is not a general Android FPS improvement claim. Whole-game,
Retro Rewind and reporter-device acceptance remain outside this evidence.

Retain the snapshot optimization in the Android runtime pin, with the16,416-case
ASan/UBSan restoration test wired into shared-runtime CI. The earlier array-reference
and1,024-slot experiments remain excluded. Code156 APK SHA256:
`920e8047eb97f1bb678fe5a4700034a1ffc55670c631f3aa852ebbdc9cc1c3c5`;
its native SHA256 is identical to154. Next measure the retained change in the
API28/default build and separate native-TLS effects using the same replay method.


The retained Android runtime is nowb864121, integrated in root0dae4bf. All three
PR checks pass, including the new snapshot test on Linux CI. PR315 and childPR2
descriptions now include the actual replay results and limitations. Code157
builds the retained optimization with the normal API28 minimum/native target;
release, profileability, signer and exact allocated-section audits pass. APK:
`a76da8c2ea689c6d547c707137ff99893c2dca1616c957dd91a8f1d49d40e491`. Native:
`a408a49316dc5c7b596be2b40c3acf31c4c25396daed07d50df9ef03d19a26b3`. It is retained locally and not yet installed;156 remains
on the phone. Next: API28 replay comparison against156's native-TLS snapshot.


### Default API28 replay (September 22, 03:27 JST)

Code157 installed in place and rendered the same Original Luigi Circuit staff
replay at 2x. The native Android identity note reports API28 (0x1c), matching the
manifest minimum. This ran on the attached Android17 phone, not Android9 hardware.
A 90.0104-second capture recorded 10,259 samples with zero lost. Thermal status
was 3 before and after. Seventeen telemetry intervals after the six-second
initial exclusion give median CPU 9.975ms/present and FPS 59.94. The previous
API29 snapshot repeat gave 9.947ms: this comparison does not establish a useful
native-TLS whole-frame improvement. Default API28 support stays intact.

Do not hide the outlier: one FPS telemetry sample was 44.18, p99 149.03ms, worst
175.16ms. The neighboring present-phase aggregate reports present_call maximum
173.387ms and main CPU 8.860ms/present. No pipelines were queued. This locates a
presentation stall in that interval but does not prove its cause or attribute it
to the TLS configuration. Replay phase is not synchronized across builds.

API28 self samples include emutls 2.17%, pthread_getspecific 1.04% (not exclusively
attributable to emutls), and GX display-list 3.31%. Code158 is built and passes
release/profileability/signer/exact-symbol audits; its native library is byte-for-
byte identical to156. APK SHA256:
`95cd9f1d52b349c6b9074fac45b427efb59afc3f047e2789853cfa693f46f934`.
It is not installed at this checkpoint;157 remains on the phone. Next install158
for the API29 repeat, then investigate remaining profiled GX costs with the same
state-preservation and device-evidence requirements.


### API29 repeat and CP-effects candidate (September 22, 03:40 JST)

Code158, native-byte-identical to156, rendered the same staff replay at2x.
The89.98-second capture recorded10,072 samples with zero lost; thermal status3
before and after. Seventeen telemetry intervals give CPU median9.461ms/present
and FPS60.01 (lowest interval56.67). This is5.2% below the intervening API28
code157 median, but earlier identical API29 code156 gave9.947ms. That within-build
variation prevents attributing the difference to TLS. Default API28 remains
unchanged; native TLS stays opt-in. Screenshots show staff replay movement, not
human driving or a completed player race.

Candidate159 computes the CP-write effect mask once when storing a validated
display-list cache record, avoiding the classification loop on subsequent hits.
It still replays every CP write in order. Identity, digest/generation validation,
eviction and nested-list exclusion are unchanged. The summary adds8 bytes per
record, at most64KiB for8,192 entries. The16,416-case ASan/UBSan state restoration
test passes; the full API28 Android build and package/profileability/signer/exact
allocated-section audits pass. APK SHA256:
`93fca44e28d3956486be31a9c94f0be4d8bb1e6c640b27a552fdfc44b2bc7ea7`;
native SHA256:
`5eebfc9548bbe7389df5911313c28e04b03f26713e2c53d5d1aca857ba558ead`.
The experiment remains uncommitted pending physical comparison with API28 code157.


A follow-up attribution of code158's clock samples identifies68 under
`IsKeyDown` (KPAD keyboard polling),101 under VI `SleepPreciselyUntil`, and21
under diagnostic thread-CPU sampling. The KPAD path scans all SDL scancodes
and compares every synthetic expiry against `SDL_GetTicksNS()`, even when
its atomic expiry is zero. A zero-expiry short circuit is the next bounded
experiment; no input behavior change or issue197 fix is claimed. VI waiting
samples are not automatically a useful-work bottleneck and will not be removed
merely to reduce the sampled percentage. Private attribution is retained as
`tls158-clock-callers.json`.


### CP-effects replay and keyboard candidate (September 22, 03:47 JST)

Code 159 installed in place with verified version/minimum and rendered the
Original Luigi Circuit staff replay at 2x. The 89.9967-second capture recorded
10,368 samples, zero lost, thermal status 3 before/after. Seventeen telemetry
intervals give CPU median 9.535ms/present and FPS median 60.03 (minimum 59.75).
GX display-list self share is 3.25%, 242 samples. The old classification loop
no longer appears; the preserved CP-write replay loop still accounts for 32
samples. Total GX cost is close to API28 code 157's 3.31%, and unsynchronized
phase/clock variation still prevents a broad performance claim. Captured frames
show no obvious geometry failure; this is bounded staff-replay validation.

The separate code 160 candidate adds an inactive synthetic-key expiry short
circuit. A held physical key returns immediately. A zero synthetic expiry skips
the clock; nonzero expiries retain the exact strict-greater-than comparison and
atomic acquire load. Synthetic stick scale is unchanged. An extracted-production
ASan/UBSan test passes 73,728 key/axis comparisons, including exact expiry, maximum
timestamps, physical input, both stick scales and an event arriving between
polls. A fresh inactive 512-scancode sweep makes zero clock reads. Full Android
packaging is in progress; no device result or issue197 resolution is claimed.
Both experiments remain uncommitted at this checkpoint.


Code160 full build finished successfully in58s. Package, minimum API28, private
signer, profileability and exact-symbol audits pass. APK SHA256:
`600b0a0d641da6d8c3d623ee7a042e196857623b558ad001b9b9b94fe6c39cc0`;
native SHA256:
`1fb20d16901c1535d58f0b4a0ea4628042f2c9b695dab00e2842e21c74ef7aec`.
It is retained locally, not yet installed. Code159 remains on the phone in
staff replay. Next install160 in place, test menu input and replay CPU/clock
samples, then broaden to moving multi-kart and Retro Rewind scenarios.

The03:48 issue refresh found63 open tickets. New316 has been reviewed and
answered with one decision-specific screenshot request;275's latest reply is
an acknowledgment. The inventory now contains63 individual response links.
The8+ hour goal remains active, with about4h25 elapsed at this checkpoint.


### Input clock avoidance accepted (September 22, 03:55 JST)

Code160 installed in place, with version160/minimum28 confirmed. Short touch
presses navigated the normal menus into the same Luigi Circuit staff replay.
The89.9839-second sample recorded10,202 samples, zero lost, thermal status3
before/after. Seventeen intervals give CPU median9.397ms/present and FPS60.08
(minimum59.82), versus code159's9.535ms/60.03. That1.4% timing difference remains
a single-device, unsynchronized-phase observation, not a broad FPS claim.

The targeted mechanism is directly visible:57 sampled clock calls attributed
to `IsKeyDown` in159 become zero in160. VI pacing clock samples remain102/103,
which is consistent with specifically removing unnecessary input polling work.
The production-function test passes73,728 comparisons under ASan/UBSan; existing
controller-routing tests pass3/3. Normal menu touch input and the staff replay
remain functional. Physical keyboard/controller and broader race acceptance
remain separate. No issue197 fix is claimed.

Retain the CP-effects summary as childb0e3349 and keyboard clock avoidance as
child51b4c45. Both retainAPI28 and guest state/input semantics. The snapshot and
keyboard contract tests are wired into CI. The built160 native source matches
these changes; source receipts still reflect its pre-commit build. Next broaden
physical validation to multi-kart and Retro Rewind scenes before final packaging.


Root integration e43c208 pins Android51b4c45. All three CI checks pass, including
the new keyboard sanitizer test on Linux. RootPR315 and childPR2 now describe
the CP-summary and input changes,63 issue responses, and the inconclusive TLS
comparison. Both worktrees are clean. Code160 remains installed; the staff
replay/menu navigation is being exited for the next broader scene. No completed
player race or broader acceptance is claimed at this checkpoint.


### Replay-exit acceptance boundary (September 22, 04:01 JST)

After profiling160, touch Start opens the replay menu and Down/left-stick input
visibly selects End Replay. A subsequent short touch A returns selection to
Continue Replay without leaving the replay. This was observed repeatedly and
is not accepted as successful exit. Earlier controls were replaced in place
between captures, so their replay-exit behavior has not been established.
Next compare this exact operation on the earlier maintained baseline before
attributing it to either new optimization. Preserve this observation rather
than claiming broader input acceptance from successful main-menu navigation.
Private screenshots `input160-replay-exit-select.png` and
`input160-exit-selected.png` retain the before/after selection. Code160 remains
installed in that replay menu; no profiler or build is running.
