# Follow-up loop: texture-copy stalls and GPU memory — September 23

Status: in progress. Starts from private build 195 and the
[overnight ledger](android-optimization-loop.md). The owner reports that build
195 still stutters in Original and Retro Rewind without an observed regression.
The attached Pixel was not visible to adb when this loop began, so the first
cycles use retained logs, source review and the ROM-free Mac renderer probe.

**Correction (emulator evidence, below):** the streaming-copy exemption built
into 196 to 198 reproduces black vehicle thumbnails and is withdrawn in 199.
Copy textures are also not the source of the 2.5 GB GPU memory. The sections
that follow record the original reasoning; the emulator section supersedes
their conclusions.

## Findings from retained build 195 evidence

1. **Every gameplay pipeline stall comes from a texture-copy pass.** Ordinary
   passes skip unready shaders (try_pipeline); only passes marked
   requireReadyPipelines block. All logged waits report persistent=1
   (for example 123 ms Original, 97 ms and 105 ms Retro).
2. **KartPad made every GXCopyTex persistent.** Upstream WiiCompiled lets a
   destination copied in consecutive frames skip unready shaders. The code134
   black-thumbnail repair (see
   [thumbnail investigation](../2026-09-19/android-black-vehicle-thumbnails.md))
   correctly removed that because a scratch target reused for a few frames can
   be retained. Side effect: any per-frame copy of the gameplay scene now turns
   each new shader into a whole-frame compile stall.
3. **The 906 ms pipeline-cache flush is not a gameplay hitch.** It ran on
   WILL_ENTER_BACKGROUND during the Home/resume check.
4. **Runtime pipeline creation is served from the Dawn disk cache** (775/775
   hits), yet only 128 of 1,199 cached recipes are prewarmed and 244 to 353 more
   are created during play. Each still costs driver time.
5. **Post-battle app memory is about 2.9 GB, of which about 2.5 GB is GPU
   memory** (GL mtrack 2.51 to 2.58 GB across four candidates; native heap about
   72 MB). The fixed per-frame buffers total about 150 MB.
6. **The copy-texture pool never forgets a key.** acquire_copy_texture keeps up
   to three textures per (destination, size, format) key for the process
   lifetime unless the guest later flushes that exact range. This is a likely,
   still unmeasured, contributor to item 5. The file is byte-identical in the
   Android, iOS, macOS and tvOS runtimes.
7. **Staging-capacity splits are not reported.** A split marks every queued
   pass required-ready and waits for the frame worker; its counter existed but
   was never logged.

## Changes (all four maintained runtimes)

- Copy-texture pool: release a pooled spare only when nothing else references
  it and no copy has requested it for 300 frames. Spares are reuse-only, so
  release cannot change pixels.
- Streaming copies: a color copy produced in each of at least 120 consecutive
  frames may skip an unready shader for one frame. One-shot copies, shorter
  runs, size changes and all depth copies still wait.
- Android telemetry line KartPadGpuResources each telemetry interval: copy-pool
  entries and approximate MiB, released spares, persistent versus streaming
  copies and cumulative staging splits. Relaxed atomic counters only; no Dawn
  call from the game thread.
- Host unit-test stubs gained the four staging-capacity functions they were
  missing, so gx_fifo_tests links again (test-only).

## Verification so far

ROM-free real-renderer probe (Metal, Dawn validation, deterministic cold-shader
gate), fresh cache per case:

| Case | Result |
|---|---|
| Consecutive-destination copy (code134 regression) | pass |
| Capacity prefix followed by copy (code134 regression) | pass |
| Full renderer suite with shader skipping enabled | pass |
| New: 130 consecutive copies, then cold shader | skipped one frame without waiting; recovered next frame |
| Control: 60 consecutive copies, then cold shader | waited for the shader, as required |

The host gx_fifo_tests suite is stale independently of this change: with the
original copy code it fails the same three tests and crashes at the same two
points (a GXCopyTex stub path and an absl insert). It is not a usable gate until
repaired; the real-renderer probe is the gate used here.

Not yet established: whether gameplay copies reach the streaming threshold, how
much of the 2.5 GB the pool holds, and any frame-time change on the phone. Those
need build 196 on the Pixel.

## Private candidates (not installed; phone not visible to adb)

| Build | Version | APK SHA-256 | Contents |
|---|---|---|---|
| 196 | 0.5.1-android-nightly.2 | 62137ab8824e52d0601ae8d1d80cfb8899678f21c6ebba6660f0a2f39ee8e0de | pool release, streaming copies, pool/copy/split telemetry |
| 197 | 0.5.1-android-nightly.3 | f01a59599462102e4f875df09a1362a0fedc13091b40ca400a5ce72ec6453328 | 196 plus live copy-cache count and size |
| 198 | 0.5.1-android-nightly.4 | 59100c76b205e248db9f523f02a1b29415f65d1a1d9592b16919223e6bf3449d | 197 plus unobserved FP status (section below) |
| 199 | 0.5.1-android-nightly.5 | 65700ffd045ca01217e989febc15c053b6b8acfea28c3afe388c568f093fd9c4 | 198 without the streaming-copy exemption (current candidate) |

196 to 198 are superseded: their streaming exemption reproduces black thumbnails.

Both pass the release package audit and carry the same signing certificate as
build 195 (SHA-256 61dfb514…3afaf), so an in-place install keeps app data. 197 is
the intended device candidate. Runtime commits: Android 0cca4d2, iOS 890e84f,
macOS 7de7da2, tvOS 0905167. Build 197's prepared source matches the committed
Android file. APKs and build/audit logs are private under
work/android-optimization-20260923; they contain game-derived code and are not
release assets.

## Device plan when the Pixel is reconnected

1. Preserve current logs, then adb install -r build 197 (no uninstall or data
   clear); read back version and both games Ready.
2. Repeat the build 195 stationary Original Cookie Land battle windows (2x, 11
   CPUs, first and warmed) and the Retro Chain Chomp Wheel pair.
3. Compare displayed FPS, intervals over 25/40 ms, maximum interval and
   KartPadPipelineWait counts against 195. Read copies_streaming to confirm
   gameplay copies actually reach the threshold.
4. Capture dumpsys meminfo after the same battle; compare GL mtrack with 195's
   2.51 to 2.58 GB and with the pool and live-copy telemetry.
5. Owner check: vehicle/character select thumbnails on first entry after the
   update, and any one-frame missing objects during races.

## CPU: unobserved floating-point status (candidate 198)

Retained build 194 battle profile: flag clear 5.78%, capture 4.16%, finish
1.97% of cycles; TLS lookups (emutls, pthread_getspecific, CurrentCpuContext)
about 5.3% more. Earlier candidates 191 to 193 reduced capture samples without
lowering total guest CPU, but all of them still read and wrote the host FPSR
around every operation.

What the guest can observe. The 29,637 translated functions contain six mffs
reads in four functions and no mcrfs. 801A1D40 and 801A24A4 store FPSCR into an
OS thread context. 801A278C and 801A2A14 (the only callers of 8012E5E8) enable
the FPU and mask/restore FPSCR in OS FPU-exception handling. 800209E8, called
from 80020A30, stores FPSCR to memory in what appears to be the crash-dump path.
None is race logic. The Retro Rewind mod sources contain no mffs.

What host flags affect. In the scalar, square-root and fused evaluators, host
overflow/underflow/inexact flags only add the sticky OX/UX/XX bits (and FX).
They can change a result or register write only if the guest sets OE/UE/XE.

Change: with KARTPAD_ANDROID_UNOBSERVED_FP_STATUS (Android app only), those
three evaluators skip the pre-clear and capture while the current FPSCR has
OE, UE and XE clear. With any of them set, the unchanged exact path runs.

Verification: tests/native/fp_status_differential/run.sh compiles the previous
and new headers into one binary and compares them over random, special,
subnormal, near-overflow and single-precision operands, all four rounding
modes, NI, random enable bits and arbitrary pre-set host flags.

| Run | Cases | Result |
|---|---|---|
| Enable bit set: exact comparison | 656,715 | 0 mismatches |
| Enables clear: all bits except FX/OX/UX/XX | 2,343,285 | 0 mismatches |
| Control: exact status required everywhere | 300,000 | 164,765 mismatches (detected) |

Input FPSCR summaries are generated consistently (VX and FEX recomputed), as
the architecture maintains them; inconsistent random summaries otherwise
differ because the old path recomputes them on every recorded exception.

Limits: this is host (Apple Silicon) arithmetic with host stand-ins for the two
Android helpers; the Android build compiles the same header. The whole-game
CPU effect is unmeasured until 198 is compared with 197 on the Pixel.

Build confirmation: the translated code only sets NI (mtfsb1 29) and restores
whole saved values (mtfsf 255), so OE/UE/XE stay clear during play. In build
198's unstripped library, PpcFmulsStateInline now tests the guest FPSCR against
0x68 (OE|UE|XE) and branches around both helper calls; build 197's calls the
clear helper unconditionally. Build 198 passes the release package audit with
the same signer.

Remaining limits: the change is inert if the guest ever enables OE/UE/XE, and a
whole-game gain is not established until the matched 197/198 comparison.
The first-loop decision not to import DriftDroid's reduced arithmetic stands:
results are unchanged here.

## Emulator validation (supersedes the streaming conclusions)

Environment: development AVD KartPad_API_36_ARM64 (host GPU, gfxstream), not
release evidence and not the owner's device. Its previous private build (code
99, same signer) had no game data. Build 198 was installed in place; the local
extracted game files were staged as in the earlier emulator procedure; config
offline, 1x, FPS overlay. A new licence was created in this disposable emulator.

Findings on 198:

- **Black thumbnail reproduced.** On first entry to Mario's vehicle select, the
  Classic Dragster thumbnail was a black silhouette and stayed black; re-entry
  showed it in colour. After moving only the Dawn and pipeline caches aside
  (the bundled seed cache and saves retained), a second cold first entry
  reproduced the same black thumbnail.
- **Why:** menus make about 12 texture copies per frame and races about 10, all
  to recurring destinations. Thumbnail bakes therefore passed the 120-frame
  threshold and were allowed to skip cold shaders, and the incomplete result was
  retained. A long run of copies to one destination does not prove the same
  content is redrawn. The streaming exemption is withdrawn in all four runtimes;
  every copy waits for its shaders again, as in 195.
- **Copy memory is small.** In a Luigi Circuit race: pool 57 entries (5.4 MiB),
  51 live copies (3.9 MiB) at 1x. Even scaled to 2x this is tens of MB, not the
  2.5 GB measured on the Pixel. The idle-spare release is kept (correct, cheap)
  but is not a meaningful memory fix. The large allocation is elsewhere (Dawn or
  driver heaps, static textures or pipeline objects) and still needs device
  attribution.
- **Race-start stalls confirmed:** persistent pipeline waits of 392, 210, 67,
  218, 121, 45, 178 and 83 ms while the race loaded and started from a cold
  Dawn cache. Emulator timing is distorted (a build was compiling on the host),
  so only the pattern, not the durations, is evidence.
- No staging splits occurred in menus or the race (staging_splits=0).

Probe change: the --stream-copy case is replaced by --long-copy-run, which
requires a 130-frame run of copies to one destination to still wait for a cold
shader and keep every pixel. With the exemption removed, copy-only,
capacity-copy, long-copy-run and the full suite pass.

Next direction for item 1: since every copy pass must wait, stalls can only be
removed by having shaders ready before they are needed — for example preparing
the recipes a course used previously during its loading screen. The 256-recipe
global prewarm was already rejected; a scene-targeted prewarm has not been tried.

Matched control on 199: the same cold procedure (Dawn and pipeline caches moved
aside, seed cache and saves kept, identical input timing) shows all three
vehicle thumbnails in colour on first entry, at both 10 and 15 seconds. 198
showed the black Classic Dragster in both of its cold runs. 199 then started
and ran a Luigi Circuit race at 60 FPS in the emulator with correct HUD and
minimap and no fatal signal in the log. This is emulator correctness evidence,
not Pixel performance; 199 passes the release package audit with the same
signer and is the only candidate intended for the Pixel.
