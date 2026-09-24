# KartPad deep review and handoff — 24 September 2026

Audience: the next agent continuing KartPad Android/iOS work. Read this whole
file before acting. It is a source-and-evidence review; nothing below was
built, installed or run on a device during this review, and no public reply,
release or PR change was made.

## 1. Plain-English summary

- The previous loops were careful and mostly right, but they optimized small
  per-instruction costs while three **structural** problems stayed untouched:
  (a) the whole GX front end runs on the game thread, (b) the four platform
  runtimes are hand-synchronised forks, and (c) nothing tested so far isolates
  the Adreno character-geometry failure on an actual Adreno device.
- The best measured Android improvements (FIFO presentation, build 203/208
  CPU reduction, course pipeline replay) are **not public**. They sit in
  unpushed runtime commits and an unmerged PR while 0.5.1 waits on an unrelated
  iPad WFC login gate.
- New concrete bugs found in this review: every fatal/exit path on mobile turns
  into SIGABRT through a static destructor (hides real crash causes, including
  #196); auto-accelerate only works for touch input (#319); Android never
  declares its frame rate to the OS; texture caches have entry-count limits
  but no byte budget; the Android performance hint only covers one thread and
  only exists on API 33+.
- Honest limit: phones like the Kirin 710 / Helio G85 class need 5–10× less
  game-thread CPU. No optimisation in this document gets them to 60 FPS.

## 2. Where things stand (verified 24 Sep 2026)

| Item | State |
|---|---|
| Public builds | Android 0.5.0/code135; Apple 0.5.1-experimental.1/build60 |
| Primary checkout `/Users/chrissotraidis/GitHub/kartpad` | Old branch `codex/candidate-cpu-handoff-record`, 381 commits behind `origin/main`, ~100 dirty files. **Do not use or clean it**; it is the owner's. |
| Working tree | `/Users/chrissotraidis/.codex/worktrees/kartpad-stabilization-20260918`, branch `codex/upstream-all-platforms-20260922` (PR #317). Remote head `927e01c`; **18 local commits unpushed** (Pixel 203/208 work, handoff docs). `docs/artifacts/2026-09-22/clean-rc2.md` is dirty and not ours — leave it. |
| Runtime checkouts | `vendor/runtimes/{android,ios,macos,tvos}` are four separate clones of `chrissotraidis/wiicompiled`, each at a detached HEAD **not on any remote**: android `a193cf4` (5 unpushed: FIFO presentation `8a9e885`, copy-spare release, streaming-copy withdrawal, course replay `c59e33b`, perf hint `a193cf4`); ios `059d193` (3); macos `d4d7459` (2); tvos `39cf763` (2). |
| Other open PRs | #315, #292, #291, #289 (older Android experiments) |
| 0.5.1 release gate | Held on iPad Retro WFC login for profile 2 (see `2026-09-22/release-confidence.md`). |
| Open issues | 62 (see `gh issue list`) |
| Stale worktrees | ~30 `/private/tmp/kartpad-*` entries marked prunable in `git worktree list` of the primary checkout |

## 3. Findings, ranked by user impact

### F1. Adreno character/geometry corruption (#102, #104, #137, #166, #193, #211, #216 Tab A9+, #301, #308, #316)

Evidence gathered:
- Broken GPUs: Adreno 619, 750 (driver 512.762.41), 829 (512.842.36), 840
  (512.842.19). Reported without geometry complaints: Adreno 650 (#103),
  730 (#278), 732 (#166 control), 740 (#169), 830 (#195/#204). Mali Pixels
  and Apple are fine. So it is not "all Adreno"; driver branch is a lead, not
  proven (working devices never reported driver strings).
- Symptom split: parts using a **per-vertex matrix index** (skinned character
  bodies, Mii bodies) fail; rigid parts using the current matrix (eyes, karts,
  bikes, tracks) are fine.
- The real failing recipes are saved at
  `/Users/chrissotraidis/.codex/worktrees/kartpad-diagnostics-20260917/build/platform-investigation/actual-shaders/`.
  Android and iOS WGSL are **byte-identical**. Recipe `58866e32bada1f83` uses a
  **7-byte vertex** of eight-bit indices (pnmtx, tex1mtx, tex2mtx, pos, nrm,
  clr, tex0) read by `raw_fetch_u8_1` at every byte lane, then fetches
  positions/normals from `abuf` through `ubuf.array_start[]` (a
  `array<u32,12>` inside a uniform block, relying on relaxed uniform layout).
- Build121 "literal" variant replaced only position/normal matrix indexing by
  a switch whose default is `vec3f(0)`; the S24 still showed eyes-only bodies.
  Collapse-to-zero under the literal variant and explosions under the dynamic
  variant are both what a **wrong index value** would produce. So the leading
  hypothesis is: the per-vertex index/attribute bytes or the array-offset
  uniform are mis-read by these drivers — not the matrix indexing itself.
- Normal builds enable Dawn `skip_validation` + `disable_robustness`
  (`vendor/runtimes/android/aurora-main/lib/webgpu/gpu.cpp` ~L721–756).
  Dawn already applies its Qualcomm workarounds (`PhysicalDeviceVk.cpp`
  ~L1004–1033, `ShaderModuleVk.cpp` ~L345 pass-matrix-by-pointer).

What to do, in order:
1. **Get a physical Snapdragon 8 Gen 3 / 8 Elite (Gen 5) phone.** A Pixel is
   Mali and cannot reproduce this. This is the single largest unblocker.
2. Build one diagnostic APK with a restart-only selector of four variants for
   PNMTX draws only, each a small, reviewable change in
   `aurora-main/lib/gx/shader.cpp`:
   - A: control (current).
   - B: CPU repack of per-vertex index bytes into a 4-byte-aligned, u32-per-
     attribute layout before upload (removes sub-word byte extraction).
   - C: move `array_start`, `postex_mtx`, `nrm_mtx` into a read-only storage
     buffer read as explicit `vec4f` rows (removes relaxed-layout UBO and
     dynamic UBO indexing).
   - D: **CPU pre-skinning fallback**: in the Aurora draw path, for draws whose
     PNMTX mask has more than one slot, transform positions/normals on the CPU
     with the XF matrices already held in `g_gxState`, emit direct F32 view-
     space vertices, and draw with an identity current matrix and no PNMTXIDX.
   Whichever variant fixes the Adreno phone identifies the layer; D is also a
   shippable device-gated fix if the driver bug cannot be pinned (cost is
   roughly 12 racers × a few thousand vertices per frame on flagship CPUs).
3. Add an **automatic self-test**: render recipe 58866e32bada1f83 once
   offscreen with a fixed synthetic 7-byte skinned mesh, write clip-space
   position to a float render target, read back, compare with a CPU
   reference. Log pass/fail with GPU + driver string; if it fails, enable D.
   This gives every reporter's log a decisive line without new requests.
4. Do not ask reporters for more generic logs. One targeted result per
   variant from one willing Adreno reporter is enough if no phone is bought.

### F2. The GX front end runs on the game thread (all "races slow, menus fine" reports)

Evidence: Pixel profile (`work/android-optimization-20260923/profile207-cookie30-report.txt`,
12-kart Cookie Land battle): game thread ≈75% of samples, of which
`HleFifoWrite` 12.9% and `GX__CallDisplayList` 12.0% (children) — roughly a
third of game-thread time. `HleFifoWrite`
(`runtime/src/hle/gx/gx_fifo.cpp` ~L348) is called **per gather-pipe word**
and incrementally parses as it goes. Only encode/submit is on the Aurora
worker. Reports match the scaling: S25 Ultra 60 FPS in time trials but 41 in
12-racer VS (#195); S25+ 20–50 FPS in battle but perfect 4× time trials
(#204); Retroid Pocket 5 / SD865 40–45 FPS where **Dolphin runs faster and
cooler** (#103); POCO F6 Pro / 8 Gen 2 runs MKWii at 60 in Dolphin (#169).
Dolphin's dual-core mode runs FIFO decode, vertex loading and draw building
on a separate GPU thread; KartPad does not.

What to do:
1. Step 1 (no threading): make `HleFifoWrite` a pure append into a buffer and
   parse in bulk at natural boundaries (display-list call, GXFlush, draw
   done, XFB copy, buffer high-water mark). Measure game CPU/present on the
   Pixel Cookie Land battle against build 208.
2. Step 2: move parse + draw building to a dedicated GX thread with a bounded
   ring. Deferral is as safe as real hardware (the Wii GPU also reads memory
   asynchronously) **provided** every sync point makes the GX thread catch up
   first: GXDrawDone/GXWaitDrawDone, draw-sync tokens, EFB peeks, EFB copies
   read by the CPU, XFB/VI copy, GX FIFO status reads, display-list memory
   writes (existing snapshot/NotifyWrite hooks), and shutdown/background.
   Ship it off by default behind a toggle, then default on per device after
   matched measurements. DriftDroid's optional async GX decoding is the prior
   art; its earlier audit's safety requirements still apply
   (`docs/artifacts/2026-09-20/driftdroid-audit/REPORT.md`).
3. Acceptance: matched Pixel battle and one Samsung flagship VS race; game
   CPU/present, p95/p99 frame time, no rendering differences in
   character/vehicle select thumbnails, minimap, results screen, EFB-copy
   effects, and Home/resume.

### F3. Unshipped Android improvements and release process

- FIFO presentation (`8a9e885`, ~75% fewer >25 ms display intervals on the
  Pixel), build 203/208 (≈2.1 ms lower game CPU/present in Cookie Land) and
  course pipeline replay are not public. Push the runtime commits to
  `chrissotraidis/wiicompiled` branches first (they exist only on this Mac),
  then push the 18 KartPad commits to PR #317.
- Decouple Android from the iPad WFC gate: ship an Android 0.5.1 (or nightly)
  with the Pixel-verified changes and honest notes, while the iPad profile-2
  WFC diagnosis continues. Close or refresh stale PRs #289/#291/#292/#315.

### F4. Fatal exits become SIGABRT and lose the reason (#196 and every fatal path)

`ProcessTranscriptState` (ios `runtime/src/main.cpp` ~L171; same in all four
runtimes) is a function-local static holding two joinable `std::thread`s.
Fatal paths call `std::exit` without `ShutdownProcessTranscript()`:
`RuntimeCrash::FatalMissingGuestTarget` (ios main.cpp ~L812–836), OS panic
and `OSResetSystem`/`exit` (`hle/os/os_reset.cpp` ~L52, 115, 130, 149),
`hle/os/os_init.cpp` L78, `hle/storage/dvd.cpp` L138, `include/nand_path.h`
L49, `include/abi_bridge.h` L642. Static destruction of a joinable thread
calls `std::terminate` → `abort`. The #196 build60 `.ips` shows exactly
`exit → __cxa_finalize → ~ProcessTranscriptState → std::terminate → abort`.
Effects: Android exit history records a native crash for controlled exits;
buffered stderr (including "target 0x… not translated") can be lost.
`OSResetSystem` also unmaps guest memory (`Memory::Reset`) before exiting
while render/audio workers may still run.

Fix: one `[[noreturn]] RuntimeTerminate(int code)` helper that flushes,
calls `ShutdownProcessTranscript()`, stops Aurora/audio workers, then
`_Exit(code)` (or `std::quick_exit`); route every path above through it.
For fatal errors on Apple, also put target address and LR into the abort
message (e.g. `abort_with_reason` / crash annotation) so the `.ips` users
already paste contains them. Test: host test that triggers each path and
asserts exit code and transcript tail.

### F5. #196 iPhone 17 Pro Max / iOS 27.2 beta Retro startup crash

Symbolicated build60 stack (dSYM UUID 4BD45C7C… matches
`build/experimental-051-20260921/KartPad-build60.app.dSYM`):
`RuntimeMain → func_800060A4_retro_rewind → func_80008EF0 →
rr_overlay_8000951C → func_8023AE60 → func_800079D0 → func_8000A3F8 →
InvokeIndirectCpu → FatalMissingGuestTarget`. `func_800079D0` is the
per-frame system update; `func_8000A3F8(table, index)` loads
`*(table + 28 + 4*index)` and calls the pointer at `+0x34` of that object.
The target address is not in the `.ips`.

Rejected: Code.pul mismatch (iOS validates size + SHA-256 before every launch,
`apple/ios/KartPadRetroRewindInstaller.mm` ~L226–274); silent guest-memory
alias failure (`guest_flat_memory_apple.cpp` throws on failure).

Next: apply F4 so the address reaches the report; send the reporter the next
build that includes the upstream translator integration (29,637 base and
4,102 Retro functions retranslated) and ask only whether Retro opens. If it
still fails, the popup/`.ips` will name the target; add it to the translation
graph or registration and write a regression test.

### F6. Low-end Android: CPU-bound far beyond reach (#167, #198, #207, #236, #275, #296, #313, #320)

#320 diagnostics (Huawei Y9 Prime 2019, Kirin 710 / Mali-G51, public 135):
race frames 40–160 ms game CPU/present with zero queued pipelines; 0.5×
resolution changed nothing; 2.2–2.4 s spikes coincide with scene loads;
128-pipeline prewarm took 11 s; audio blocks drop. The Pixel does comparable
work in ~12.6 ms. What helps at the margin:
- F2 (largest).
- Android frame-rate declaration and hint coverage (F8).
- A value-exact scalar FP codegen mode: translator emits plain register
  arithmetic (keep Force25Bit, single rounding, NI handling, NaN slow path)
  with no `volatile`, no FPRF/FPCC bookkeeping and no redundant
  `(void)PpcCompareStateInline` before `SetCRFloatResident`. Precondition:
  prove no record-form FP instructions (CR1 copies FPSCR bits) and keep the
  six OS-context `mffs` sites exact. Note 191–193 fast paths were already
  tried without reliable gains — only try this as one bounded experiment.
- Publish a plain minimum-spec statement in README/INSTALL_ANDROID
  (e.g. "Snapdragon 8 Gen 1 / Dimensity 8000 class or newer for full-speed
  races; older chips run below 60 FPS"). This is a product decision for the
  owner; do not publish without approval.

### F7. Runtime fork drift (architecture)

Four clones of the same runtime, 17–24 differing files per pair, platform
branches like `codex/stabilization-ios-20260918`. Android-only fixes that are
platform-neutral (e.g. BP GEN_MODE first-write cache fix in `gx.hpp`,
surface-loss present handling in `gx_copy.cpp`, display-list front cache)
land on one platform only. Recommendation: one shared runtime branch with
platform code isolated behind `#if`/adapter files; until then, a CI check
that diffs the four trees and fails on unexpected divergence in
`aurora-main/lib/gx`, `aurora-main/lib/gfx`, `runtime/src/hle`.

### F8. Smaller concrete items

- **Frame rate declaration (Android):** no `ANativeWindow_setFrameRate` /
  `Surface.setFrameRate` anywhere. Declare 60 (or the interpolation target)
  with `FIXED_SOURCE` on API 30+. Relevant to steady 41 FPS on Samsung
  120 Hz panels (#195) and Samsung game-mode behaviour.
- **Performance hint:** `runtime/src/hle/vi.cpp` ~L70–110 creates a session
  for the game thread only, reports thread CPU time, and is unavailable below
  API 33. Include the Aurora frame worker, presenter and audio mix threads;
  report wall-clock work per frame. Consider raising game-thread priority.
- **Texture memory:** `aurora-main/lib/gx/gx.cpp` ~L612 and ~L680 prune
  static texture source caches only by entry count (512/256) and only
  unreferenced handles; object caches (1,024) keep references. Pixel measured
  ~2.5 GB GPU memory after a battle (`2026-09-23/android-copy-stream-loop.md`).
  Add byte accounting to `KartPadGpuResources` telemetry first, then a
  byte-budgeted LRU scaled to device RAM. Also bound background pipeline
  compilation memory (Pixel code125 Scudo OOM in Tint,
  `2026-09-19/pixel-code125-memory-crash.md`).
- **iOS memory:** no entitlements file for iOS; no
  `com.apple.developer.kernel.increased-memory-limit`; the host does not log
  `os_proc_available_memory()`. #310 (iPad, crash ~every 10 min, no .ips
  posted) is consistent with jetsam. Log available memory + memory warnings
  in the session transcript; evaluate the entitlement with sideloading tools
  before adding it (unsupported entitlements can block install).
- **Auto-accelerate (#319):** implemented only in the touch overlay
  (`android/app/src/main/java/dev/kartpad/android/KartPadOverlayView.kt`
  ~L1223–1240; checks touch pointer owners). Physical controllers never get
  it. Either implement hold-to-lock in the native pad path for all sources or
  label the switch "Touch controls only". Check Apple parity.
- **Retro course replay recorded 0 pipelines** on the Pixel even though Retro
  arenas load from `RetroRewind6/BT/Tracks/*.szs`, which matches the
  `tracks` folder rule in `hle/storage/dvd.cpp` ~L402–433. Unresolved; log
  the DVD path and scene key once per load to find out why.

## 4. Hypotheses checked and rejected in this review

- Dawn device-wide lock serialising background pipeline compilation: rejected
  (CreateRenderPipeline/CreateShaderModule are "no autolock").
- Frame interpolation corrupting Android characters: rejected (default off;
  character-select preview also fails).
- Code.pul mismatch causing #196: rejected (hash-validated per launch).
- #309 iPad 9 "Play Game" crash being the F4 exit bug: rejected (it is the
  already-fixed ImGui cleanup after a graphics-startup failure).

## 5. Suggested order for the next agent

1. Push runtime commits and the 18 KartPad commits; ship Android with FIFO +
   203/208 + replay as a clearly labelled release candidate (owner approval
   for publication).
2. F4 fatal-exit fix in all four runtimes (small, testable on host).
3. F8 quick wins: setFrameRate, hint coverage, auto-accelerate scope, texture
   byte telemetry, iOS memory logging.
4. F1 variant APK + self-test; get an Adreno 750/840 device.
5. F2 step 1 (bulk FIFO parse) with matched Pixel measurement, then step 2.
6. F7 convergence plan.

## 6. Standing constraints (from owner history)

- Never uninstall, clear data, downgrade or reset identity on devices; use
  in-place installs with higher version codes, back up and read back data.
- Report physical-device evidence separately from emulator/host/package
  evidence; never call a candidate a fix without the named device result.
- Respond to reporters with specific, privacy-bounded asks; do not repeat
  generic log requests. Do not publish or reply without owner approval.
- Keep the primary checkout untouched; work in this worktree.
- Do not suggest Figma.
