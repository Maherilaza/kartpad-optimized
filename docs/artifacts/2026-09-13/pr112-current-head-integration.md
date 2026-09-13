# PR #112 integration correction — 13 September 2026

Reviewed contributor head `74fe75c8e7c4fdbb9ca68546ca683e5f4a803dc9`, whose parents are the previously reviewed `a332264` and main `615225b`. GitHub reports the PR mergeable. This correction descends directly from that contributor merge and retains contributor attribution.

Fresh source preparation exposed two integration failures:

- The merge omitted the patch invocation before `aurora-viewport-interpolation.patch`; the shell would execute the non-executable patch file instead of applying it.
- `wiicompiled-macos-unified-settings.patch` still expected `DrawFpsOverlay` immediately after the removed graphics settings. Main now inserts an Android FPS-scale declaration there, so one of twelve hunks failed.

Restore the missing invocation and refresh the second patch's context while preserving the Android conditional declaration. No native UI or controller behavior is changed by these corrections.

## Validation

The exact preparation script's source-copy and patch section was executed against fresh disposable copies of the locally pinned upstream runtime and Aurora. All patches applied successfully after both corrections. This check stops before dependency downloads, translation, CMake, linking and packaging.

Passed against that fresh corrected source:

- Native controller/profile harness, including keyboard cancellation, Escape, close/reopen, focus loss, alternate character layouts, ISO/special keys, repeat/invalid handling, virtual SDL input and corrupt-profile preservation. Five existing harness/dependency warnings remain.
- Controller assignment and displacement, cached fallback, unassignment and player four.
- Native graphics/audio settings bridge, coalescing, fullscreen failure fallback and resolution limits.
- All 200 final PADStatus trigger output combinations.
- All eight `test_macos*.py` contract tests.
- Diff whitespace validation.

Contributor Original gameplay evidence is recorded at `a332264` in PR #112; the latest comment says ready to merge without giving a new Retro result. These host checks do not establish owner gameplay acceptance or Retro gameplay. No app was built, installed, published or relabelled, and no owner settings/saves were used. Two-player rendering issue #127 and VSync request #250 remain separate.
