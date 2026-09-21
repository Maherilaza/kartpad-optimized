# Overnight goal acceptance audit

In progress. This records the original request, not a claim that every reported
bug is fixed. Final completion still requires the requested eight-hour work
window and the remaining normal-build checks.

| Requested outcome | Evidence inspected | Status |
|---|---|---|
| Review, classify, quantify and answer every open issue | Live63-issue set exactly matches the inventory;63 comment IDs read back successfully from GitHub, correct issue and maintainer author | Verified; refresh before final handoff |
| Incorporate recent releases | Live main remains0d657f3; public Android0.5.0/code135; Apple0.5.1-experimental.1/build60 treated separately | Verified |
| Use prior research and DriftDroid analysis | Ledger records prior task findings and the pinned DriftDroid audit; local-binding, persistence, TLS, display-list and layout hypotheses evaluated | Verified; no unsupported matched-DriftDroid FPS claim |
| Implement and test useful fixes | RVZ import, local native binding, Dawn cache persistence, vertex snapshots, CP summaries, inactive-key clocks and per-voice audio window retained | Verified within the individual evidence boundaries |
| Produce an improved Android build | Normal170 built, audited and installed in place; specific overhead removed and RVZ import accepted | Verified; broad FPS/reporter-device acceptance is not established |
| Double-check correctness | Meaningful sanitizer/source contracts, package/signer/symbol checks, physical control/candidate evidence, final source review and passing three CI jobs | Verified for the tested paths; normal-build extended check in progress |
| Be honest about device activity | Screenshots distinguish menu, stationary scene, staff replay, CPU fixture and short touch movement; no manual-completed-race claim | Verified evidence scope |
| Preserve owner state and concurrent work | In-place compatible-signer updates; seven-file post-import readback; dirty primary checkout preserved; isolated source changes pushed to PRs | Verified; final normal app launch does not imply new shell save readback |
| Keep documentation useful and current | Issue inventory, maintenance board/matrix/queue, performance handoff, install/settings docs, README and experiment ledger updated | Verified; final summary refresh pending |
| Investigate planned feature follow-ups | Separate source-based shake/Retro-ghost assessment; unsupported Retro scope clarified | Verified assessment, not feature implementation |
| Work for8+ hours | Goal created September21 23:25:19 JST; eight-hour threshold September22 07:25:19 JST | Not yet satisfied at this audit checkpoint |
| Leave a reviewable handoff | RootPR315 and runtimePR2 open, source pinned and pushed; private APK/symbols retained | Final artifact summary and clean endpoint pending |

No public binary release or automatic issue closure has been performed. The
worktree remains under `.codex/worktrees/kartpad-stabilization-20260918` because
it contains needed private evidence/build products and the primary checkout has
concurrent dirty work. Source changes are preserved in the linked PR branches.

See [the report](README.md), [issue receipts](open-issue-inventory.md),
[feature assessment](feature-follow-up.md) and [chronological evidence](evening-goal-loop.md).
