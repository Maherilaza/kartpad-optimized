# WiiCompiled integration across platforms — 22 September 2026

## Scope and acceptance

Candidate source integrates upstream `83463764b8acda394e058b0c689a10b8561fc380`
into the translator subtree and all four maintained runtime branches. This is
114 upstream commits after the previous baseline, not 114 newly fixed issues.
Selected changes were already backported. Package and physical acceptance are
separate from source ancestry.

The owner accepted Android code170 and iPad build60 before this integration.
Those installed builds have not been replaced by this candidate. Their acceptance
does not cover the upstream update. Existing game data, saves and preferences
remain preserved. No public release or reporter issue closure is implied.

## Shared and platform changes

- Upstream translator continuation/Kamek changes, host contexts, ARM64 runtime,
  filesystem/NAND, input bindings and Wii Remote support are integrated for
  validation. Platform-specific build files and memory backends remain maintained
  adapters; this is not replacement by an unmodified desktop runtime.
- All four runtimes now include the reviewed display-list snapshot reduction,
  CP-write summary, inactive synthetic-key clock avoidance and per-voice AX sample
  window. These were previously retained only in the Android candidate.
- Android retains its importer, local native-symbol binding, persistent shader
  cache, mapped Classic-controller routing and scheduler-side SDL event service.
- Apple retains native settings, touch controls, sandbox paths and the iOS
  anonymous guest-memory allocator. NAND initialization continues through
  KartPad's translated save path, including redirects.
- Android assembly normalization handles both earlier COFF output and the updated
  translator's Mach-O assembly when translation runs on a Mac.

## Evidence so far

- Translator: 655 tests pass.
- Private owned-game graph regenerated with the updated translator: 29,637 base
  functions translated, 29,065 active base functions, 4,102 Retro Rewind functions,
  zero mod C++ translation failures. Existing verified Code.pul and production
  payload inputs retained; game-derived outputs remain private.
- Seven upstream host suites pass: NAND saves, NAND settings, SC serial, input
  expressions, host contexts, Darwin context ABI and platform paths.
- Each platform source passes sanitizer differential checks: 16,416 snapshot
  restoration cases, 73,728 key/axis expiry comparisons and 786,432 AX sample/state
  comparisons. These exercise actual extracted source on the host, not phone FPS.
- Native Mac settings reload and controller-profile tests pass. Installed and
  portable Mac storage-layout checks pass.
- ARM64 paired-single arithmetic passes 110,000 scalar differential cases plus
  signed-zero and single-NaN payload checks, with a separate ASan/UBSan pass.
  The tested arithmetic header is identical across all four runtimes.
- Apple guest-memory alias/protection/failure-cleanup tests pass; the actual iOS
  allocator links with the device SDK. The upstream Mac alias test also passes
  against KartPad's maintained backend.
- Android code171, iOS/iPadOS build61, macOS build61 and experimental tvOS compile.
  iOS, macOS and tvOS application package audits pass. Android final package and
  bundle auditing and candidate archives remain in progress.
- The exact packaged macOS executable visibly reached the Original title screen
  using a private portable NAND/configuration, then exited cleanly. An initial
  setup failure required creating the explicitly configured empty test NAND
  directory. No owner saves were used. This is startup evidence, not a race test.
- New Discord Rich Presence support defaults off in KartPad.
- No new physical mobile gameplay, online compatibility or universal performance
  improvement is claimed.

## Requested enhancements and issue claims

RVZ import is implemented and locally validated in Android code170. Original
ghost export already has reporter confirmation. Retro Rewind ghost transfer and
Android shake-to-trick remain unfinished; see the
[feature follow-up](../2026-09-21/feature-follow-up.md). They must not appear as
completed enhancements merely because the upstream source was refreshed.

The prior [issue inventory](../2026-09-21/open-issue-inventory.md) and
[acceptance audit](../2026-09-21/acceptance-audit.md) remain the issue-level record.
No count of users fixed can be derived from commits or successful builds. Link
each release claim to a concrete source change and its actual acceptance result.

## Remaining release gates

1. Finish Android, iOS/iPadOS, macOS and experimental tvOS native builds; audit
   package contents, diagnostics defaults, symbols and source provenance.
2. Review merged input routing and ARM64 behavior; run Original and Retro smoke
   checks with isolated data, then preservation-safe device validation.
3. Publish reviewed runtime commits before exposing parent gitlinks, update the
   source archive and release documentation, and retain known driver/online and
   sustained-performance limitations.

Work is isolated in the existing stabilization worktree on
`codex/upstream-all-platforms-20260922`; the primary checkout and accepted packages
remain intact. Detailed build logs are private under
`work/upstream-all-platforms-20260922`.
