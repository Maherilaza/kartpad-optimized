# Staging-map lifecycle correction

This continues the active release goal after the clean code129/build53 candidate.
PR #307 was open/draft at `6f7820a`, with all three checks passing, when this
work began. The existing integration worktree was clean.

## Reproduction and correction

The maintained renderer stored every asynchronous map result in one global
atomic enum. Resetting that enum did not distinguish requests. A delayed
callback from an old slot/lifecycle could therefore publish Mapped or Unmapped
while a newer request was pending. The frame-begin loop also called
`ProcessEvents()` continuously until the enum changed.

All four runtime pins now assign a generation to each map request. Completion
changes the state only when its generation is still pending. Reset invalidates
old callbacks before staging buffers are released. A small condition variable
wakes the waiting thread immediately for spontaneous completion; a one-millisecond
bounded wait still services implementations requiring ProcessEvents. The callback
uses its own short lock, never the renderer GPU mutex held by frame begin.

Frame begin also checks the existing device-loss handler while mapping is
pending. A loss report can now reach that handler even if the map callback never
arrives. This preserves the existing fatal device-loss behavior; it is separate
from the earlier graceful startup rejection. The success, ordinary cancellation,
buffer rotation, EFB and interpolation ownership paths retain their contracts.

## Evidence

`tests/test_staging_map_lifecycle.py` extracts the actual request callback and
frame-begin waiting block. Dawn service delivery is controlled in this test;
the request-state helper is production code. Baseline files were copied before
editing and retained privately.

| Host ARM64 case | Before | Corrected |
| --- | --- | --- |
| Old request completes after reset/new request | Incorrectly changes new request state on every platform | Old success, abort, cancellation and error are ignored |
| 30 ms delayed callback | 1.93–2.07 million ProcessEvents calls; 30.9–33.1 ms process CPU | About 25–28 calls; less than 1 ms process CPU |
| Callback dispatched by ProcessEvents | Completes | Completes after one dispatch |
| Current request cancelled then retried | Completes on retry | Completes on retry |
| Device lost with no map callback | Existing loop has no loss observation | Dispatches existing loss handler during the wait |

The corrected cases pass ASan/UBSan and a separate ThreadSanitizer run across
Android/iOS/macOS/tvOS source pins. CPU figures describe an injected wait, not
race FPS, GPU execution time, or a reporter's measured bottleneck.

The real Metal `gpu_batch_probe.cpp` now uses the production request-state helper
with spontaneous callbacks. On Apple M3 Max, all eight overwrite/additive
workloads pass, including repeated three-slot reuse and 769 one-draw submissions.
Every readback is byte-identical to its unsplit control and expected pixels,
with zero WebGPU validation errors. This exercises real mapping, copying,
submission and readback; it is not the full Aurora FIFO/EFB/interpolation path.

Full Android code130, Mac build54 and iOS physical-SDK build54 pass. The initial
direct Android invocation stopped at configuration because its SDK environment
was missing; the checked prototype entry point supplied that environment and
the rerun passed. Clean-source packaging is tied to `df39712`; source parity,
APK audit, iOS app audit, matching ELF/Mach-O symbols, and Mac package/ZIP
readback checks pass. Exact hashes and limits are in
[`staging-map-candidate-build.json`](staging-map-candidate-build.json).

The maintained runtime branches and parent commit are published to draft PR
#307. All three checks pass on `df39712` (boundaries 51s, regression 25s,
receipts 10s). Public release signing and dependency promotion remain pending.

## Native game integration

A separately identified, ad-hoc signed portable copy of the audited Mac app
used copied test data with networking disabled. No normal application defaults,
saves or installed game data were changed. The copy reached Original's license
creation, character and vehicle selection, and a 12-racer 50cc Luigi Circuit
race. Pause, resume and quitting the race back to the main menu worked. Visible
rendering and sampled presentation telemetry remained around 60 FPS. This was
a stationary player with active CPU racers, not a completed race or a matched
performance comparison; results, awards, Retro and endurance remain pending.

The automation's short key presses previously failed to advance the default
keyboard configuration. For this test only, an actual-format saved binding file
disabled the duplicate GameCube keyboard port, allowing the existing Classic
keyboard path to receive the presses. No input runtime code or production
defaults were changed. This narrows a keyboard-path discrepancy and permits GPU
integration checks; it does not establish normal keyboard acceptance or resolve
the Wii Remote/Classic Pro report #306.

One early menu session ended cleanly before the next automation action; its
bounded session record confirms clean shutdown but the initiator is unknown.
The next session ran the race checks and was explicitly closed with Command-Q.
An initial sampling command targeted the exited process and failed; the retry
sampled the verified live process. Its physical footprint was about 1.2 GB,
with a 2.3 GB peak. This single sample is neither a memory plateau nor an Android
memory estimate. No fatal, assertion or WebGPU validation error was found in
the two retained runtime transcripts.

## Remaining work

This removes the busy wait and stale-callback hazard. It does not fix fixed
staging capacity, introduce safe draw subdivision, prove a memory plateau, or
establish an overall timeout policy for a driver that reports neither completion
nor device loss. Arbitrary timeout/retry must not silently discard persistent
bakes or touch unmapped storage. Transactional admission and complete pass
ownership remain the next capacity work, with actual gameplay acceptance and
the coordinated public release still pending.

Private source controls, sanitizer output, builds and Metal readbacks are under
`work/staging-lifecycle-20260919`. Existing code129/build53 artifacts remain
preserved independently.
