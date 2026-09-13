# KartPad and WiiCompiled reports

KartPad builds on [WiiCompiled](https://github.com/patchzyy/Wiicompiled), created
by [patchzyy](https://github.com/patchzyy). WiiCompiled supplies the original
Mario Kart Wii static translator and runtime. KartPad maintains its modified
Apple/Android integration, controls, installation and packaging. The projects
are independently maintained.

## Choose a destination

- **Using WiiCompiled directly:** use the
  [WiiCompiled issue chooser](https://github.com/patchzyy/Wiicompiled/issues/new/choose)
  and its log instructions.
- **Using KartPad:** use the
  [KartPad issue chooser](https://github.com/chrissotraidis/kartpad/issues/new/choose)
  for app/install/touch-control problems and when the cause is uncertain.
- **A known or suspected shared runtime problem:** search
  [WiiCompiled's existing issues](https://github.com/patchzyy/Wiicompiled/issues)
  too. Link a matching report in your KartPad issue. If contributing evidence
  upstream, clearly state that it came from KartPad, with its exact version
  and modifications/baseline if known. Follow that project's instructions.

A crash during a race or a graphics problem can involve KartPad changes too;
the symptom alone does not establish ownership. You do not need to diagnose
the source code to ask for help. Maintainers should connect related reports
and explain which released KartPad build contains an upstream correction.

WiiCompiled's current forms ask about its latest release and include Windows
log paths. Do not check a statement that is untrue for your KartPad build.
If the form does not fit, keep the evidence in KartPad and link the upstream
issue for coordination. No general upstream acceptance of KartPad reports is
being claimed.

## Collect once, review, then attach

Use the [platform collection steps](SUPPORT.md#collect-a-useful-report).

| Platform | Start here |
| --- | --- |
| Android | **Report a Problem…** for a short report; **Export Private Diagnostics…** for runtime logs. |
| iPhone / iPad | **••• → Report a Problem…**; review/share the file and attach it manually on GitHub. |
| macOS | **Help → Save Diagnostics Report…**; review the saved report before attaching. |
| Experimental tvOS | Use the [tvOS testing guide](TVOS-TESTING.md) and its diagnostic collection script. There is no promised mobile-style sharing flow. |

A report ID is not an upload. Opening GitHub does not attach a file. Share the
same reviewed evidence when adding information to a linked upstream report;
do not create duplicate issues merely to copy the logs.

Include the exact app/build, device and OS, Original or Retro Rewind and pack
version, steps, and the session/time of the failure. Runtime `console.log` and
`crash_*.txt` files, when present, are different from a short app summary or an
OS exit record. Keep their startup/version information and relevant failure
context. Do not label an old log with the version installed when exporting it.
Mark missing runtime revision or stock-WiiCompiled reproduction as **unknown**
or **not tested**; do not infer either from the current repository.

Review text before sharing: omit game data, saves, NAND, credentials, console
identities, personal paths and network/account identifiers. The private Android
archive is for local inspection, not automatic public upload. Keep your
installation and saves intact while troubleshooting.

## Maintainer coordination and next implementation

The immediate changes make the relationship and destinations visible and carry
more existing report context through GitHub. They do not change who accepts
reports upstream, and require a new tested build to reach installed apps.

### 1. Finish one reusable runtime report

Improve the existing exporters rather than add a new reporting system. Offer
the most recent game session with its start time and profile visible; let the
player choose an earlier session when that is the one that failed. A new app
launch or recent file modification must not silently replace the failed run.

The reviewed export should contain a short cover sheet and that session's
runtime console/crash text when available. Preserve startup/version information
and a bounded failure tail; clearly mark omissions or truncation. Keep OS exit
records separate and include only a matching record when one can be identified.
Missing crash text is not evidence that the run did not crash.

Record KartPad build/source revision, WiiCompiled baseline, device/OS and game
profile from that session's recorded build information. New builds should stamp
the verified upstream baseline during preparation/build. For older logs, show
unknown rather than substitute today's checkout or currently installed build.
Reproduction on unmodified WiiCompiled is **yes / no / not tested**.

Use this same report for saving, attaching to an existing issue, or preparing a
new issue. Opening GitHub never uploads it. Keep the report ID stable, keep raw
logs out of URL parameters, and require review before public sharing.

### 2. Direct destinations, no mandatory maintainer relay

The selected direction is direct user submission of suspected WiiCompiled
runtime problems, with explicit KartPad origin. The repository issue chooser
links directly to WiiCompiled's existing forms. This needs no fork conversion,
new upstream form, or mandatory coordination conversation.

Keep KartPad as the app/platform destination and fallback for uncertainty.
Do not assume every gameplay or rendering symptom proves an upstream defect.
Users must follow the receiving form honestly: never auto-check latest/stock
WiiCompiled or reproduction claims. The creator still controls his tracker and
can redirect or close reports; a direct link is not a support guarantee.

The app implementation still needs to carry its prepared report to a choice
of destination. The current branch improves context and project visibility;
its app submission buttons still create KartPad drafts. Finish that destination
selection without auto-posting, copying old issues, or uploading raw logs.
Users should review and submit once to their selected tracker, with the same
session evidence. Repository migration remains separate; see
[Fork connection options](FORK-OPTIONS.md).

### 3. Validate and ship in small steps

The attribution, chooser links and reporting improvements already prepared in
source can be reviewed independently of the exporter work. Publish only checked
documentation; links in packaged apps must resolve when those apps ship.

Implement session selection on Android first, where the existing multi-session
ZIP causes confusion, then use the same report fields in the existing Mac and
iPhone/iPad exporters. Keep platform-specific collection code. tvOS remains a
separate script-based collection path with the same origin/session labels.

For each platform test a normal run, a failed run followed by relaunch, missing
logs, and an older session from a different build. Verify the report keeps the
correct session/build and does not include unrelated sessions or private files.
Then check review, save/share, browser handoff and cancellation on the actual
platform. These reporting tests do not establish gameplay stability.

After release, review the next ten reports that use the new flow: could the
maintainer identify the build and relevant session without another generic log
request, and did related upstream evidence reach the agreed destination? Use
the existing issues for this check; no analytics service or extra ticket store.
