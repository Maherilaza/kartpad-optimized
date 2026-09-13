# Issue 248: isolated Kamek continuation candidate

Status: source-tested candidate only; not release-ready. No upstream dependency pin bump, runtime build, hardware run, or public issue response.

## Evidence

KartPad main `1fe6364` still prepares WiiCompiled `1912292` with six translator patches; none includes upstream [PR 182](https://github.com/patchzyy/Wiicompiled/pull/182), merge `25c69ae28e46a127d87db8d394f857e34da54f99`. Comparing the prepared translator confirms `linkedHookLrBasesByTarget` only includes RetroWFC hooks, and its LR-offset scanner only recognizes `mtctr`/`bctr`, not `mtlr`/`blr`.

Android 80's release CMake cache at `/private/tmp/kartpad-android-017-device/android/app/.cxx/RelWithDebInfo/3r384b1v/arm64-v8a/CMakeCache.txt` selects `private/translation-main-017/build_shards/shards.cmake` and prepared source `build/verify-fps-runtime-source-20260913-111027-final2`. That manifest includes both inspected Retro mod shards.

The compiled-graph input contains an item-window hook call at `0x807EF168` to `0x8183ADD8` with LR `0x807EF16C`. There is no generated resume label or registration for `0x807EF16C`. However, this exact hook's generated body returns normally or tail-calls `0x80860AF0`; absence of a resume label alone does **not** reproduce the reporter's abort. Upstream issue 83 originally concerns Deluxe X Blue, and issue 248's reporter has not run KartPad. Do not describe that exact crash as confirmed on KartPad.

There is a separate concrete skip-return defect in the actual graph: `rr_kamek_8180C6E4` saves incoming LR `0x807A1A58` in r31, tests the callback via `func_800213E4`, adds 20 when absent, restores LR from r31, and returns. Its caller in `shard_36c0daa3778847680f24436e.cpp` ignores changed LR and continues into the callback call at `0x807A1A68`, rather than skipping to `0x807A1A6C`. This matches PR 182's Item Rain cause at source level; runtime triggering remains untested.

## Candidate and regression

`patches/wiicompiled-kamek-skip-return.patch` is the exact upstream PR 182 diff, including its tests. `prepare-patched-translator.sh` applies it after existing KartPad translator patches. It applies cleanly to KartPad's prepared translator. The upstream planner handles path-sensitive LR offsets and saved-register restoration; CLI wiring includes Kamek BranchLink targets in continuation discovery and caller dispatch.

In an isolated translator copy, the original CLI scanner was exposed in Core with only a signature adapter (`FunctionTranslationResult` to its instruction list) so the upstream regression tests could exercise the old implementation. Result: **20 failed, 13 passed** LR-relative tests, including saved nonvolatile LR surviving a helper call. This was a behavioral failure, not merely the expected missing-API compilation failure. After the actual backport, the complete translator suite passed: **607 passed, 0 failed** (including the binary-free LR continuation code-generation regression). Test fixture project configuration was copied into the isolated tree so root-discovery tests could run; no game binaries were copied into the patch or commit.

Local logs: `/private/tmp/kartpad-issue248-old-tests.log` and `/private/tmp/kartpad-issue248-new-tests.log`.

## Required next gate

Do not merge or release this candidate based on unit tests alone. Upstream [PR 218](https://github.com/patchzyy/Wiicompiled/pull/218) reports PR 182 increases Retro Rewind generated mod size by roughly 42%, with pathological compilation in an aggregate shard. PR 218 is open, and the issue 83 commenter reports its filtering removes the `0x807EF16C` resume point. Neither a broad pin bump nor unexamined adoption of PR 218 is justified.

Regenerate the exact supported Retro Rewind profile in isolation, measure functions/continuations/lines and per-shard growth, verify `0x807A1A6C` dispatch and `0x807EF16C` handling, then choose a scoped backport or conservative sharding mitigation. Only after graph review should a native build and item-change/Item Rain gameplay check become the acceptance gate. The current Android 80 runtime has not been changed by this investigation.
