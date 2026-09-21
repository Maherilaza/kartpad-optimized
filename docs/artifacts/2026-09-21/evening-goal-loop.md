# Evening issue and Android optimization loop

Started 2026-09-21 JST. Owner: Codex task `01a0c45b-6553-7c03-82bf-ab9d6d0fcf25`.
The user requested sustained useful work for eight or more hours, all-open-issue
review and replies, small tested fixes, and Android optimization informed by
the prior DriftDroid audit. The active task goal retains the full request.

## Baseline and ownership

- Current fetched main: `0d657f3`; latest stable release: 0.5.0.
- Apple build60 experimental release disables accidental forced diagnostics;
  it is a mitigation awaiting matched device evidence, not a proven FPS fix.
- Initial GitHub snapshot: 62 open issues, including new #313 and #314.
- Reuse the clean existing `kartpad-stabilization-20260918` worktree on
  `codex/evening-android-20260921`. Preserve the dirty primary checkout.
- Android maintained runtime starts at `295f4507fe1fd706f2edfa09055b815f425ed919`.
- Pixel 9 Pro XL is attached. No race or performance observation has yet been
  made by this task. Private device identifiers stay out of tracked evidence.

## Repeated cycle

1. Read every open issue and its comments; classify platform, symptom, supplied
   evidence, shipped scope, next engineering action and remaining acceptance.
   Reply specifically, acknowledge existing evidence, avoid repeated log requests,
   and record the actual comment URL. Refresh edited/new reports before posting.
2. Check recent task findings and release source before selecting one candidate.
   Prioritize actionable regressions and safe small enhancements alongside the
   sustained Android CPU work; do not substitute repeated audits for changes.
3. State one falsifiable hypothesis. Preserve a hashed baseline and relevant
   settings/data. Make the smallest source change and run meaningful checks.
4. Inspect the emitted artifact. Use matched control/candidate measurements on
   the attached device when feasible; retain scene screenshots and exact settings.
   Distinguish chooser, menus, attract/demo footage, gameplay and completed races.
5. Keep improvements with supporting evidence; reject or defer candidates with
   recorded reasons. Never convert symbol counts or microbenchmarks into FPS.
6. Update this evidence record and the existing maintenance records, commit
   reviewable changes, and continue the next useful cycle. Build/package success
   and affected-reporter acceptance remain separate. No automatic issue closure.

## Initial engineering sequence

- Verify current release linkage; test function-only local binding without
  changing Android's minimum supported API or scalar FP semantics.
- Verify Dawn cache persistence and add a safe explicit flush if still missing.
- Independently evaluate API29 native TLS; retain API28 compatibility by default
  until an explicit supported-release decision and real measurements exist.
- Review small display-list cache-copy reductions with ownership/invalidation
  checks; reprofile before selecting deeper scalar or asynchronous GX work.
- Investigate Android shake-to-trick and ghost discovery as bounded feature work.

Track actual elapsed work and outcomes. Eight hours is a requested working
window, not evidence of completion or justification for idle polling. Missing
one device or reporter does not stop other available engineering work.

## Completed first cycle

- Reviewed and replied to all 62 open issues; a fresh post-reply snapshot found
  no missing or newly opened tickets. Reply receipts are linked in the inventory.
  No issues were closed automatically. Maintenance queue tests: 65 passed.
- Commit `fe83144` adds Android RVZ picker-descriptor support. The actual Android
  DiscIO probe passed ISO plus uncompressed/Zstd RVZ byte equality, borrowed
  descriptor lifetime/offset preservation, and truncated-input rejection on the
  attached Pixel. Fixtures are synthetic; no actual game RVZ import is claimed.
- Re-linked the exact retained code135 objects as an unchanged control and with
  function-only local binding. The unchanged control reproduces the public native
  BuildID `ce82326003e7b0db832e931282f3f815195e60f2`. Candidate BuildID is
  `e27f23dbfca8367520ae8fd205787dbccd18c07a`.
- Internal jump slots fall from 10,873 to zero; remaining external slots: 610.
  Defined dynamic exports match. Stripped native size falls from 99,942,816 to
  99,168,352 bytes. Android API28 and scalar floating-point semantics are retained.
  These artifact changes do not establish a gameplay speed improvement.
- Built and audited 0.5.1-evening.1/code136 containing both changes. The attached
  device's code135 APK has identical ZIP entry contents and native digest to the
  published control, but uses the existing private test signer. A separate copy
  of code136 was signed with that verified matching identity and installed with
  `adb install -r`; installation succeeded without removing app data. Both game
  profiles still show Ready to play afterward. Public signing copy is separate.
- Physical control observations so far: Original title screen and automatic
  attract footage. The overlay visibly accepts a held A press, but the title
  screen did not advance. No user-controlled race or FPS gain has been verified.
  Input-path diagnosis and matched scene measurements remain in progress.

Private build products are under `build/evening-20260921/` in the retained
worktree; raw screenshots, reports and receipts remain ignored task-local data.
No APK release has been published by this loop.

### Continued device navigation and review

Draft PR: https://github.com/chrissotraidis/kartpad/pull/315 (receipts CI passed).
A broader Android contract selection also passed: 65 tests.

A private, temporary code137 input probe confirmed that a held A press reaches
both the JNI publisher and native consumer with matching state. A fresh run
advanced through the existing license, Single Player and VS selection screens.
The earlier failed presses are not an established source defect; their cause
remains undetermined. Temporary logging was restored out of tracked source.
Uninstrumented code138 reproduces the exact code136 native SHA256
`719c336fa56c12185c4b2e33ded09e40583a9449f3d801b651ab674a936df002`.
No race measurement has yet been made. Continue matched scene work before
making any speed claim.
