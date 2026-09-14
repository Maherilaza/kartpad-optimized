# Migration validation ledger

Status: translator candidate implemented; runtime migration and device acceptance
remain open. Nothing in this ledger authorizes reusing an old accepted binary as
proof of a newly compiled source layout.

- Baseline main: `dd79c936e5f32dde2d5a003798163cf615935c0d`.
- Upstream remains `1912292c804ff9b1b79938de89369ec4496f9fff`.
- Full local APFS backup completed; 1,136 tracked/non-ignored files matched by
  SHA-256 and mode. Portable Git bundle verified and restored into a separate
  repository. Private backup paths are kept in the local recovery ledger.
- Entire old translator preparation output compared with the candidate subtree:
  1,108 source files matched byte-for-byte, including native registration source.
- Candidate translator Release build passed.
- Translator suite: 624 passed, zero failed/skipped.
- Builder suite: 25 run, one existing skip, no failures.
- Generated G6 semantic function matches the tracked expected C++ exactly.
- Runtime baseline attempt: cached private graphs failed the existing REL-report
  verification before preparation. They were preserved. A fresh private base
  graph is being generated; this failure is not a migrated runtime regression.

Remaining evidence: restored consumer rollback, subtree merge/export rehearsal,
source cache invalidation and source-archive checks, fresh real-title comparison,
platform source equivalence, native builds and device/gameplay acceptance.
