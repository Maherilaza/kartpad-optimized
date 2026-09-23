# Overnight Pixel handoff (ends 06:00 JST, September 24, 2026)

Purpose: measure the private Android candidates on the attached Pixel 9 Pro XL,
keep what is better, and leave a clearly identified build installed by 06:00 JST.
Every Android candidate since 195 has only been tested on an emulator. The phone
is the missing evidence; get that before writing more code.

## Hard rules

- Stop new work by 05:30 JST. Use the last 30 minutes to leave the phone at the
  KartPad launcher with no game running, then write the ledger and a short report.
- Never uninstall, clear data or `pm clear`. Install in place only
  (`adb install -r`). The phone holds the owner's game data, saves, licences and
  console identity.
- **Downgrades are not possible.** The builds are non-debuggable release builds on
  a user phone, so `adb install -d` fails without an uninstall. Once 203 is
  installed you cannot return to 195. If a candidate regresses, rebuild the
  preferred source with a higher version code (for example 206) and install that.
- Do not publish releases, post on GitHub or Discord, or push to a public branch.
- Report honestly. Emulator, host and title-screen results are not phone
  gameplay evidence. Driving the phone with taps has been unreliable in earlier
  sessions: confirm every navigation step with a screenshot, and never claim a
  race or battle happened unless a screenshot shows it.
- Leave the unrelated dirty file `docs/artifacts/2026-09-22/clean-rc2.md` alone.

## Where things are

- Worktree: `/Users/chrissotraidis/.codex/worktrees/kartpad-stabilization-20260918`,
  branch `codex/upstream-all-platforms-20260922` (commit 4016b11 or later).
- Pixel adb serial: `47181FDAS005KL` (check `adb devices -l`; it was absent all
  of September 23 afternoon). adb: `~/Library/Android/sdk/platform-tools/adb`.
- APKs, all signed with the same private key (signer SHA-256 `61dfb514…3afaf`),
  in `work/android-optimization-20260923/`:

| Code | File | SHA-256 | What it adds |
|---|---|---|---|
| 195 | KartPad-code195-private.apk | 3c929e6a6de15e6455754bfc5dcb52d13e8d3ac70ffe21e0dcb627b84744ea32 | last phone-tested build; believed installed |
| 203 | KartPad-code203-private.apk | ec7a4bd7a84ea7f9bedb507cac292c02436470c115f99484880793e49e557101 | copy-texture pool release, FP status skip, course-scoped pipeline replay, system-bar fix, game-thread Performance Hint |
| 205 | kartpad-205-nightly11.apk | 2491fb4e3cfa4d247df85a85be07a2b27051855161f51ac8eace91235616f23d | 203 plus game-thread context slot (removes emulated TLS lookups) |

Skip 204: the compiler kept the TLS call, so it is identical in effect to 203.
Details and emulator results: [copy-stream ledger](../2026-09-23/android-copy-stream-loop.md).

## Measurement tools (already written, Pixel-specific)

In `work/android-optimization-20260923/`:

- `battle-capture.py <label> <layer>`: with a battle already started and
  confirmed on screen, it waits 25 s, takes a before screenshot, captures 120 s of
  compositor frame timing for the SurfaceView layer via `capture-surface.py`,
  then takes an after screenshot and thermal state. It writes `<label>/summary.json`
  (presented FPS, intervals over 25 and 40 ms, max) and logcat. Read
  `app-summary.json` for `median_cpu_ms_per_present` (game-thread CPU).
- Find the layer with `adb shell dumpsys SurfaceFlinger --list | grep SurfaceView`
  after the game is running; it changes after resume.
- Do not screenshot, profile or touch the phone during the 120 s window.

## Baseline to beat (build 195, warmed stationary Cookie Land battle, 2x)

| Run | Presented FPS | Intervals > 25 ms | > 40 ms | Max | Game CPU/present |
|---|---|---|---|---|---|
| 195 warm | 59.07 | 109 | 2 | 133 ms | 14.70 ms |
| 195 repeat | 59.42 | 74 | 0 | 33 ms | 14.79 ms |
| 195 Retro chain warm | 58.43 | 169 | 10 | 133 ms | 14.75 ms |

The expected gains are in game-thread CPU (FP status skip, then TLS in 205) and
in the number of long intervals on repeat visits (course replay).

## Plan in priority order

1. **Check the phone.** Confirm it is visible, record the installed version
   (`dumpsys package dev.kartpad.android | grep version`) and the installed APK's
   SHA-256 (`pm path`, then pull it and hash it). If it is not 195, stop and work
   out the right baseline before installing anything.
2. **Install 203 in place.** Check `versionCode=203` and hash readback, launch,
   and confirm the launcher still shows both games Ready with the existing licence.
3. **203 Cookie Land battle, same scene as the baseline.** Do one warm-up battle
   so the course replay records the scene, then two clean captures. Compare with
   the 195 rows. Also note race-start behaviour on the second visit.
4. **Install 205 in place** and repeat step 3 with the same settings. Emulator
   timing showed no difference (both 8.12 ms mean), so this is the Pixel's chance
   to show one. Keep 205 only if its game-thread CPU is lower by more than the
   195 run spread, with no new long intervals or faults.
5. **Retro Rewind course replay.** Play the same Retro track or battle twice.
   On a non-debuggable build, logs come from the in-app export (Help → Report a
   Problem → Save Diagnostic Log). Look for `Pipeline scene replay` lines in the
   console log. This has never been seen on a Retro track.
6. **Lifecycle check on the build you keep.** Home and resume mid-battle, pause and
   continue, return to the launcher. Same PID before and after, rendering resumes.
7. If time remains and the phone results are clear, build a profileable variant
   (`KARTPAD_ANDROID_PROFILEABLE=1`, next version code, e.g. 206) and take one
   30 s `simpleperf record --app dev.kartpad.android` capture during a battle to
   see what the game thread spends time on now. Symbolize with the matching
   unstripped `libmain.so` under
   `android/app/build/intermediates/cxx/RelWithDebInfo/*/obj/arm64-v8a/`
   (match the build ID). Profiling runs are not timing runs.

## Build command (only if a new build is needed; about 15 minutes)

```
KARTPAD_DISCIO_JNI_ROOT=$PWD/build/evening-20260921/discio-jni \
KARTPAD_ANDROID_VERSION_CODE=<N> \
KARTPAD_ANDROID_VERSION_NAME=0.5.1-android-nightly.<X> \
KARTPAD_ANDROID_PACKAGE_FORMAT=apk-release \
bash scripts/build-android-game-app.sh private/android-context-control-20260923/translation \
  build/<fresh>/runtime build/<fresh>/native
```

Then audit with `KARTPAD_ANDROID_EXPECTED_VERSION_NAME`,
`KARTPAD_ANDROID_EXPECTED_VERSION_CODE` and `KARTPAD_ANDROID_REQUIRE_RELEASE=1`
set, running `scripts/audit-android-package.sh <apk>`. Commit runtime changes in
`vendor/runtimes/android` first; the build stages the committed submodule.
Disk is tight (about 130 GiB free); each fresh native build adds a large
`android/app/.cxx` directory.

## Context worth knowing

- #195 (S25 Ultra): 60 FPS in time trials, about 41 in VS, Original and Retro.
  The emulator shows 12 karts nearly double game-thread CPU. The Performance Hint
  in 203 targets this; a Pixel cannot prove a Samsung fix.
- Already tried and rejected (do not repeat without new evidence): API 29 native
  TLS, explicit scalar context through the generator, larger front cache,
  function reordering, startup CPU affinity, streaming-copy exemption (black
  thumbnails). See [ANDROID-PERFORMANCE-HANDOFF.md](../../ANDROID-PERFORMANCE-HANDOFF.md).
- Apple build 65 (same replay and FP skip) is installed on the iPad with data
  verified but has not launched yet because the iPad was locked. Not part of this
  Android session.

## Finish

Append a dated section to the copy-stream ledger: installed build and hash,
each capture's summary numbers against the 195 rows, what was kept or rejected
and why, and anything not verified. Commit on the branch (docs and code only;
private captures stay under `work/`). End with a short plain-language report for
Chris: what is installed, what got measurably better on the phone, what did not,
and what still needs his hands (for example a Samsung report).
