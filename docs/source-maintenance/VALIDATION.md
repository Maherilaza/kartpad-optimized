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
- macOS native dual build and package audit passed. The audit's stale log-size
  expectation was corrected to match the unchanged baseline implementation.
  This was an evolving candidate build, not final clean-commit acceptance.

## Open gates

- Finish Android and iOS native builds and exact candidate artifact accounting.
- Remaining product preparation combinations and any build-profile discrepancy
  must be resolved against baseline, without changing runtime behavior silently.
- Physical macOS/iOS/iPadOS/Android gameplay and data-preserving installation.
  The iPad was unavailable and no Android device was attached at the last check.
- Experimental tvOS native/device acceptance is not established.
- Publish the reusable other-project plan only from accepted KartPad results.

Local evidence is under the isolated checkout's ignored
`build/source-migration/` directory. Private inputs and device identifiers are not
part of the public source or this ledger.
