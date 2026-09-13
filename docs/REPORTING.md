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

Next, improve the existing exporters to select one identifiable game session,
preserve its version header and failure tail, and label the report as KartPad.
Use the packaged source revision and recorded WiiCompiled baseline when
available; explicitly show unknown for older builds. Keep the same report ID
and session evidence across save/share/GitHub. Do not add automatic uploads or
a second ticket database.

Before enabling a dedicated upstream-submission flow, coordinate with patchzyy
on whether to accept derivative reports, which evidence is useful, and whether
to add a form that does not require a stock/latest WiiCompiled build. KartPad
can maintain the platform-specific log collection instructions. Reproduction
on an unmodified upstream build must remain an explicit yes/no/not-tested fact.

Acceptance for reporting changes: check report preparation, review, save/share,
browser handoff and cancellation on Android, iPhone/iPad and Mac; verify report
ID, build/profile metadata and attachment instructions remain consistent.
Check tvOS collection separately. Host tests do not prove those device flows.
