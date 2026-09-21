# Overnight maintenance and Android performance work

Status at September 22, 05:35 JST: work remains in progress. Public Android is
still **0.5.0 / code135**. None of the private profiling APKs below is a public
performance release. Apple build60 is a separate diagnostic-overhead mitigation.

## Issue review

All **63 open issues** have been read, classified and individually answered:
39 Android, 10 Apple, and 14 cross-platform/features or insufficient platform
detail. Follow-up evidence is being reviewed as it arrives. The
[issue inventory](open-issue-inventory.md) contains categories and reply links.
No ticket is closed on source tests alone, and repeated reporter evidence is
not being requested without a specific unresolved decision.

## Retained changes

| Change | Evidence | Remaining boundary |
|---|---|---|
| Android RVZ import through the picker descriptor | Physical DiscIO checks of synthetic ISO, plain/Zstd RVZ, borrowed descriptor lifetime/offset and malformed input | Full game RVZ picker/import acceptance |
| Bind internal native functions locally | Internal function jump slots reduced from 10,873 to zero; external imports and exports retained | No isolated FPS claim |
| Persist Dawn cache on backgrounding | Physical flush/relaunch and cache-hit evidence | Broader device/lifecycle coverage |
| Avoid unused vertex-format snapshot construction | 16,416 sanitizer-checked restore cases; physical profiles remove constructor samples | Small timing differences are workload-specific |
| Cache display-list CP-write effects | Same restore tests; ordered CP writes and cache invalidation retained | No independent overall FPS gain established |
| Resolve the audio sample TLS window once per voice | 786,432 sanitizer comparisons; ARM disassembly and two physical profiles remove per-sample TLS lookups | No general FPS or subjective audio-quality claim |
| Skip clocks for unused synthetic keys | 73,728 sanitizer-checked input comparisons; inactive 512-key poll uses zero clocks | Does not establish a fix for reported stale controller input |

Source is reviewable in [KartPad PR #315](https://github.com/chrissotraidis/kartpad/pull/315)
and [Android runtime PR #2](https://github.com/chrissotraidis/wiicompiled/pull/2).
The last source-changing root revision passed all three required CI jobs.

## Physical evidence and limits

Staff replay comparisons and short touch-driven Grand Prix movement were
recorded separately. Neither is represented as a human-completed race.
A private offline fixture subsequently completed a twelve-CPU Luigi Circuit
race and two Moo Moo Meadows races, with visible movement, items, lap progress
and results/post-race screens. Its cinematic camera differs from normal player
control. Code162's stationary-grid attempt is rejected.

The heavier fixture profiles expose roughly 13% of sampled self cycles in
scalar floating-point flag handling and roughly 5% in emulated TLS plus
`pthread_getspecific`. These are profiling shares, not attainable FPS gains.
Floating-point exception semantics remain unchanged. API28 remains the default;
fresh API29 and API28 CPU-fixture measurements overlap prior variation and
differ in thermal state, so no TLS-model speedup is established. A small audio
change resolves its existing thread-local sample window once per voice
instead of once per byte. Its 786,432 sanitizer-checked sample/state comparisons
pass; two physical captures remove the targeted lookup samples while whole-frame
timing remains within control variation.

The primary checkout and private game data are preserved. Private APKs, symbols,
recordings and save backups remain local. Before returning the phone to ordinary
play, remove the CPU-driver marker and install a normal non-debuggable build with
shell profiling disabled, then verify saves/settings and launch behavior.

For exact hashes, run counts, rejected candidates and current measurements, see
the [evidence ledger](evening-goal-loop.md). For the next engineering actions,
see the [Android handoff](../../ANDROID-PERFORMANCE-HANDOFF.md).
