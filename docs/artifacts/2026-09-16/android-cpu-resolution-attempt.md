# CPU-context reuse and subnative resolution attempt

The owner selected CPU work reduction and lower resolution, and deferred PGO.
This experiment preserves Android API28 support and the existing 1× default.

## Changes

- Android scalar floating-point adapters reuse one validated CPU context across
  evaluation and commit. This adopts the earlier `535924a` experiment, with
  arithmetic and guest exception semantics unchanged. Local runtime commit:
  `5ced89d`.
- Android's Render Resolution menu adds 0.75× and 0.5×. Existing 1×–4× choices
  remain available. Preferences preserve valid existing values and reject
  non-finite values. The per-frame Android settings consumer now permits scales
  down to 0.5×. Local runtime commit: `a8b6889`.
- Apple runtime pins and Apple settings paths are unchanged. No PGO, native TLS,
  automatic memory trimming, worker-count or floating-point accuracy change.

Source inspection confirmed that framebuffer sizing, viewport/scissor mapping,
EFB-copy destination sizing and depth snapshot coordinates use target/logical
dimensions rather than requiring an integer scale. EFB RAM copies resample back
to guest dimensions. This supports the experiment but does not replace visual
and gameplay checks, especially effects and fine HUD detail at 0.5×.

## Executed checks

On the attached Pixel 9 Pro XL, the actual baseline/candidate scalar adapter
harness passed 448,000 differential cases, including special/random values,
guest FPSCR, host flags, rounding, suppressed writes, nested contexts and two
concurrent threads. The API28 ARM64 test executable uses O2 with strict FP flags.

A six-round alternating-order single-add microbenchmark reported paired time
reductions of 19.43%, -1.10%, 15.97%, 4.10%, 10.04% and 9.67% (median 9.86%).
This is one synthetic operation, not a game instruction mix, not thermally
controlled, and not an FPS result. One round was slower. It supports taking the
candidate into a game comparison, not advertising a 10% gameplay improvement.

The new executable framebuffer test exercises the actual renderer sizing code
at every offered scale, wide and portrait aspects, fractional rounding, tiny
dimensions and allocation limits. All 35 existing touch-overlay contracts pass.
The scalar harness also builds without modifying the maintained runtime tree;
it uses the preparation cache's SHA-256-verified sse2neon dependency.

Reproduce sizing checks with `scripts/test-android-subnative-resolution.sh`.
Reproduce scalar checks with `scripts/test-android-scalar-context.py`, supplying
the baseline header saved before the patch and an explicitly authorized ADB
target only when execution is intended. Raw private evidence stays under
`build/android-cpu-resolution/`.

## Comparison requirements

First compare baseline and CPU candidate at the same 1× resolution in a full,
demanding race. Builds must match native configuration, API target, settings,
assets and workload; the older API29 release-style private103 package is not a
matched control for an API28 debug candidate. Do not count a capped 60 FPS replay
as evidence that demanding races improved.

Then compare 1×, 0.75× and 0.5× within one binary, including a return to 1× to
expose temperature/cache drift. Capture actual render dimensions, warm shader
queue, game speed, frame-time windows, temperature and memory. Preserve the
owner's settings and saves. The phone was connected but locked during the
initial build; an unlock request was sent while independent work continued.

No new full-race performance gain is established by the checks above.
