# Issue 248: isolated Kamek continuation candidate

Status: source-tested candidate only; not release-ready. No upstream dependency pin bump, runtime build, hardware run, or public issue response.

## Evidence

KartPad main `1fe6364` still prepares WiiCompiled `1912292` with six translator patches; none includes upstream [PR 182](https://github.com/patchzyy/Wiicompiled/pull/182), merge `25c69ae28e46a127d87db8d394f857e34da54f99`. Comparing the prepared translator confirms `linkedHookLrBasesByTarget` only includes RetroWFC hooks, and its LR-offset scanner only recognizes `mtctr`/`bctr`, not `mtlr`/`blr`.

Android 80's release CMake cache at `/private/tmp/kartpad-android-017-device/android/app/.cxx/RelWithDebInfo/3r384b1v/arm64-v8a/CMakeCache.txt` selects `private/translation-main-017/build_shards/shards.cmake` and prepared source `build/verify-fps-runtime-source-20260913-111027-final2`. That manifest includes both inspected Retro mod shards.

The compiled-graph input contains an item-window hook call at `0x807EF168` to `0x8183ADD8` with LR `0x807EF16C`. There is no generated resume label or registration for `0x807EF16C`. However, this exact hook's generated body returns normally or tail-calls `0x80860AF0`; absence of a resume label alone does **not** reproduce the reporter's abort. Upstream issue 83 originally concerns Deluxe X Blue, and issue 248's reporter has not run KartPad. Do not describe that exact crash as confirmed on KartPad.

There is a separate concrete skip-return defect in the actual graph: `rr_kamek_8180C6E4` saves incoming LR `0x807A1A58` in r31, tests the callback via `func_800213E4`, adds 20 when absent, restores LR from r31, and returns. Its caller in `shard_36c0daa3778847680f24436e.cpp` ignores changed LR and continues into the callback call at `0x807A1A68`, rather than skipping to `0x807A1A6C`. This matches PR 182's Item Rain cause at source level; runtime triggering remains untested.

## Candidate and regression

`patches/wiicompiled-kamek-skip-return.patch` is the exact upstream PR 182 diff, including its tests. `prepare-patched-translator.sh` applies it after existing KartPad translator patches. It applies cleanly to KartPad's prepared translator. The upstream planner handles path-sensitive LR offsets and saved-register restoration; CLI wiring includes Kamek BranchLink targets in continuation discovery and caller dispatch.

In an isolated translator copy, the original CLI scanner was exposed in Core with only a signature adapter (`FunctionTranslationResult` to its instruction list) so the upstream regression tests could exercise the old implementation. Result: **20 failed, 13 passed** LR-relative tests, including saved nonvolatile LR surviving a helper call. This was a behavioral failure, not merely the expected missing-API compilation failure. After the actual backport, the first staging-copy suite passed 607 tests, but exact-profile regeneration exposed that the staging source lacked KartPad's existing Kamek-v2 patch. That preliminary result is superseded by a fresh reconstruction from the pinned upstream translator plus all six patches in `prepare-patched-translator.sh` order, followed by this candidate: **622 passed, 0 failed**. The signature-adapted original scanner was rerun in this fresh stack and again produced **20 failures, 13 passes**. The fixed source was restored and its full suite rerun. Test fixture project configuration was copied into the isolated tree so root-discovery tests could run; no game binaries were copied into the patch or commit.

Fresh logs: `/private/tmp/kartpad-issue248-graph/exact-old-tests.log` and `/private/tmp/kartpad-issue248-graph/exact-tests.log`. Fresh translator: `/private/tmp/kartpad-issue248-exact-translator`. The preliminary logs remain separately preserved; they do not establish current-stack verification.

## Exact-profile regeneration result

The fresh translator regenerated only the mod and shard graph, reading the frozen Android 80 base manifest, functions, metadata, Code.pul, and saved Retro-WFC payload. Output was isolated under `/private/tmp/kartpad-issue248-graph`; no original translation or runtime source was regenerated. The Code.pul SHA-256 is `88cd25ff08121f7c4ddb40538703f40c270f414f2dbc55a6b4b6767e62db7253`, matching the released base-awareness record. Region is P and module guest base is `0x81800000`. Native shard registration input was the exact configured runtime source's `src` directory. The frozen base is valid to reuse because this backport changes mod continuation planning and leaves base translation unchanged.

Translation completed with **4,101 mod functions and zero C++ failures**, versus 4,095 mod functions in the released shard manifest. Six continuation functions were added. The planner reported 81 continuations. The candidate explicitly checks LR after the collision hook and includes local dispatch to `0x807A1A6C`, plus a standalone `rr_continue_807A1A6C`. It also emits `case 0x807EF16Cu: goto loc_807EF16C` and the local resume label. These are generated-source results, not gameplay acceptance.

| Measurement | Android 80 graph | Candidate graph |
| --- | ---: | ---: |
| Retro mod shards | 48 | 48 |
| Retro mod C++ lines | 1,430,752 | 2,021,781 (+41.3%) |
| Retro mod C++ bytes | 34,304,688 | 50,313,490 (+46.7%) |
| Largest Retro shard lines | 48,875 | 183,361 (3.75x) |
| All shard C++ lines | 10,931,923 | 11,522,976 (+5.4%) |
| All shard C++ bytes | 288,511,425 | 304,522,059 (+5.5%) |

The biggest individual overlay, `rr_overlay_8062C3A4`, expands from 25,675 to 154,388 lines (6.0x); `rr_overlay_8056F7F0` expands from 16,483 to 82,323. Moving functions between shards cannot remove this single-function growth. The correctness dispatch gate passed, but the growth gate failed. No native compilation was attempted.

Reproduction uses the fresh CLI's `translate-mod` with the frozen release base manifest/metadata, exact Code.pul, saved local payload, `--emit-cpp --threads 2`, then `emit-build-shards` with the frozen base functions and selected runtime native sources. The private project file, complete commands' outputs, and numeric comparisons are at `/private/tmp/kartpad-issue248-graph/{project.yml,translate.log,shards.log,released-stats.json,candidate-stats.json,function-growth.json}`. Generated sources and game-derived inputs must remain private.

## Required next gate

Do not merge or release this candidate based on unit tests alone. Upstream [PR 218](https://github.com/patchzyy/Wiicompiled/pull/218) reports PR 182 increases Retro Rewind generated mod size by roughly 42%, with pathological compilation in an aggregate shard. PR 218 is open, and the issue 83 commenter reports its filtering removes the `0x807EF16C` resume point. Neither a broad pin bump nor unexamined adoption of PR 218 is justified.

The exact-profile regeneration now confirms both dispatch behavior and the substantial growth risk. Before merge, develop and regression-test narrower continuation code generation that preserves both addresses and all six added continuations; simply increasing the shard count is insufficient for the largest expanded function. Only after graph review should a native build and item-change/Item Rain gameplay check become the acceptance gate. The current Android 80 runtime has not been changed by this investigation.


## Shared-dispatch mitigation

A follow-up `wiicompiled-shared-lr-dispatch.patch` addresses the multiplication directly without adopting upstream PR 218's target filter. When a function contains multiple continuation-aware calls, each call retains its register reload and normal-return LR guard, but changed LR branches to one shared dispatch tail. That tail preserves the complete local address switch and registered external continuation fallback. Single-call code generation remains unchanged. The shared tail is outside block-local scopes and after an explicit return, preventing accidental normal fallthrough.

Fresh exact-profile regeneration under `/private/tmp/kartpad-issue248-shared-graph` yields:

| Measurement | Released | PR 182 alone | Shared dispatch |
| --- | ---: | ---: | ---: |
| Retro mod lines | 1,430,752 | 2,021,781 | 1,666,963 |
| Retro mod bytes | 34,304,688 | 50,313,490 | 39,915,562 |
| Largest Retro shard lines | 48,875 | 183,361 | 65,837 |
| Overlay `8062C3A4` lines | 25,675 | 154,388 | 37,286 |

Remaining mod line growth is **16.5%**, down from 41.3%. The formerly sixfold overlay expansion is now 45.2%; the largest shard is 34.7% larger than the released graph. This reduces the pathological expansion without claiming native compilation cost is proven acceptable.

All **4,101** generated function names and their distinct case-address sets match the PR 182-only graph. All **107** emitted `rr_continue` symbols are preserved, including the six additions over the released graph. The planner still reports 81 continuations, and both `0x807A1A6C` and `0x807EF16C` have local dispatch cases. Translation reports zero C++ failures.

Two new binary-free regression cases exercise 2 and 20 continuation calls: both fail against PR 182 alone and pass with shared dispatch. They require one switch, a guard and shared-tail jump for every call, preserved local and external dispatch, and normal fallthrough before the dispatch tail. The full fresh translator suite passes **624 tests**. Patch reverse-application and preparation-script syntax checks pass.

The generated two-call synthetic function was also compiled with Clang C++17 at both `-O0` and `-O2`, using `-Wall -Wextra -Werror` and minimal runtime stubs. Each binary executed nine scenarios covering normal return, skipping at the first or second call, local resumption, registered external dispatch, and an unregistered external return. Assertions checked call counts and final register state. Both binaries passed. Synthetic harness and logs remain in the isolated graph directory; no real game code was compiled in this check.

Next gate: focused native compilation of the largest changed generated overlays and their actual runtime headers, followed by the full candidate native build if bounded compiler behavior holds. Actual item-change/Item Rain gameplay remains necessary. No full native build, device operation, or merge was performed in this mitigation pass.
