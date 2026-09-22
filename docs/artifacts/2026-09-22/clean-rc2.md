# Clean RC2 — captured socket-send errors

Android code175 (0.5.1-rc.2), iOS/iPadOS build64 and macOS build64 compiled from
clean source f8e295a2fce61a1649768840f6f051e564f8e5f3. All prepared runtimes were
verified against their maintained pins before compilation. Both hosted CI jobs
pass for this source revision.

These candidates include the [socket send-error correction](socket-send-error.md).
Android uses the existing public release signer and passes bundle/APK audits.
The unsigned Apple app and Mac app pass their platform audits. Package ZIP CRCs
pass. Matching Android unstripped symbols and iOS dSYM are retained privately.

The public IPA publication script remains pinned to an older accepted release and
correctly rejects build64. The same local-candidate packaging path used for RC1
was used here; no public acceptance gate was relaxed. No release was published.

The coordinated source packager verifies the clean APK/IPA source fingerprint and
Mac source commit against the recursive core snapshot. Independent readback then
verified SHA256 and size for all 84 listed payload members (85 total including the
source manifest). The previously audited native and Maven dependency sources are
unchanged. Final APK, IPA, Mac ZIP, full source and notices checksums pass readback.

Local artifacts are in build/release-051-rc2-20260922. Exact hashes and the shared
source fingerprint are recorded in [clean-rc2-packages.json](clean-rc2-packages.json).
RC1 and its symbols remain intact as comparison artifacts.

## Exact-package follow-up

The isolated API36 ARM64 emulator accepted the exact public-signer APK as an
in-place174-to175 update. App UID and all four synthetic identity, Original-save,
Retro-save and preference sentinels remained unchanged through chooser launch.
After that check, the two byte-asserted synthetic save files were removed only
from the disposable emulator so they could not act as invalid game saves.
Previously staged private owned game data remained in place; this was not an
importer test. The game reached the Original title and then attract-mode scenes
without injected game input during a60-second observation. The same process
remained alive at all five checkpoints. Screenshots were inspected directly;
this is not a driven race or a physical GPU benchmark.

An exact copy of the packaged Mac app was started alongside isolated portable
userdata with networking disabled. It seeded managed NAND settings from the
synthetic legacy serial123456789, kept ConsoleIdentity.txt unchanged, stayed alive
20seconds and exited with status0. This checks migration/startup, not online play.
The test fixtures are outside the release directory; the public archives were
not modified. Private evidence is under work/mobile-network-repair-20260922.

GitHub's latest issue activity remains #216 on September21; no new reporter
result supports closing the renderer tickets. Both hosted CI jobs passed at the
preceding documentation revision bbe7ddf.

## Acceptance still required

The corrected code has host sanitizer coverage for send-error preservation;
these offline package checks do not identify or resolve the owner's iPad WFC94020
failure. Android geometry and Moto G85 idle reports remain unresolved. Neither
unavailable physical device was accessed. The emulator was shut down after the
observation. Keep the WFC publication hold and retain RC1 as a comparison artifact.
