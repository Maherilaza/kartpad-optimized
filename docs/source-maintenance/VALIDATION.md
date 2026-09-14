# Migration validation ledger

Status: source migration implemented in an isolated candidate. Promotion and
physical device/gameplay acceptance remain open. Existing releases are unchanged.

- Baseline main: `dd79c936e5f32dde2d5a003798163cf615935c0d`.
- Upstream remains `1912292c804ff9b1b79938de89369ec4496f9fff`.
- Full local APFS backup verified: 1,136 tracked/non-ignored files matched SHA-256
  and mode. Git bundle restoration succeeded in an independent repository.
  This is local rollback protection, not an off-device disaster backup.
- Translator preparation: all 1,108 files match the previous preparation.
- Translator Release build and 624 tests passed. The full PPC semantic script
  passed, including differential, sanitizer and Dolphin float-oracle checks.
- Fresh Original translation: 29,637 generated functions and 72 base_common
  compiled shards match the old translator output byte-for-byte.
- Runtime preparation parity passed: macOS 850 files, iOS/iPadOS 849,
  Android 853, tvOS 849. Only patch-utility `.orig`/`.rej` debris was excluded.
  These comparisons used Original for macOS/iOS/Android and dual for tvOS.
- Tracked staging tests: runtime 10 passed; translator 3 passed. They cover stale
  output refusal, pinned identity and tracked edits rather than untracked source.
- Recursive source fingerprint/archive/offline-restore tests: 7 passed.
- Build provenance tests, including submodule source coverage: 3 passed.
- Runtime contracts: 110 passed. Focused Metal/CPU/serial/REL checks: 21 passed.
- Maintenance loop: 54 passed. Builder: 25 run, one existing skip, no failures.
- macOS controller, VSync/config and Apple guest-memory checks passed.
- Translator consumer revert, synthetic subtree update and focused upstream
  contribution rehearsal passed in disposable worktrees.
- Runtime integration commit `6b034975dd4191c1bcec313bbf137018fd67e7a2`
  reverted cleanly in a disposable worktree; all four old preparers matched exactly.
- The real 61,378,201-byte candidate source archive restored offline to that
  exact KartPad commit and all four exact runtime commits. Archive SHA-256:
  `3d1559416378374151fb596551e26029c332cc2764d717da5be7fe8a5f464d4e`.
- macOS native dual build, final incremental build, staging verification and
  final package audit passed. Runtime bytes stayed unchanged across the final
  incremental build. The audit's stale log-size expectation was corrected to
  match the unchanged baseline implementation.
- iOS/iPadOS native dual build and full app audit passed. The audit parser was
  corrected to read the platform field rather than matching the word in a path.
  A private unsigned IPA was packaged and its ZIP integrity verified.
- Android native dual build, final clean-source incremental build, APK package
  audit and APK signature verification passed. Candidate version code is 92.
- The old-preparer translator independently generated 4,101 Retro Rewind records;
  its entire source bundle matches the migrated translator byte-for-byte
  (`e9c09b39f3cf21b8fed8bbe578bd706244a77761bc04d4f2a091870aadbb264a`).
  The stale 4,095 builder guard was corrected; 11 guard tests and validation of
  the actual fresh graph passed. This changes validation, not generated code.
- Retired all 99 migrated patches after source parity and native build checks.
  No active script, test, builder or workflow references those patch filenames.
  Builder (25, one existing skip) and maintenance tests (54) still pass.
- A full rollback rehearsal through retirement commit `a938d8a` restored the
  exact pre-runtime-integration tree, then reverted the translator consumer.
  All 99 patch files and all five original preparers were restored exactly.
- Source preparation's product selection only chooses the build target; it does
  not select different runtime patches. Dual native candidates cover Original
  and Retro Rewind code; per-product gameplay remains a separate hardware gate.

## Private candidate artifacts

These are development artifacts, not accepted public releases or installation proof.
Paths are relative to the isolated checkout's `build/source-migration/` directory.

| Platform | Artifact | SHA-256 / source evidence |
|---|---|---|
| Android | `KartPad-source-migration-android.apk` | `4ff90de21de40cfc237837b3cca9ab33f2baea0f9db607abe0ff50c5b036d547`; clean source `a938d8a` |
| iOS/iPadOS | `KartPad-source-migration-ios-unsigned.ipa` | `858c8ff39809e6a7affe1a275846fceecdab110289f144b23cc2ddb158ddf321`; clean compiled source `43a1661` |
| macOS | `final/KartPad.app` | unsigned runtime `c375c03a319d3076daaf32555fa853b63079753a6e4f402d53c09dbe3e5d1ef1`; final staging and package audit passed |

## Open gates

- Physical macOS/iOS/iPadOS/Android gameplay and data-preserving installation.
  The iPad was unavailable and no Android device was attached at the last check.
- Experimental tvOS native/device acceptance is not established.
- Publish the reusable other-project plan only from accepted KartPad results.

Local evidence is under the isolated checkout's ignored
`build/source-migration/` directory. Private inputs and device identifiers are not
part of the public source or this ledger.
