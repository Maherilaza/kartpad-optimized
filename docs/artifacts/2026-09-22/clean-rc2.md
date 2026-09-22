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

## Acceptance still required

RC2 has not been installed on any device or emulator. RC1's synthetic upgrade and
title/attract-mode observations remain RC1 evidence. The corrected code has host
sanitizer coverage for send-error preservation; that does not identify or resolve
the owner's iPad WFC94020 failure. Android geometry and Moto G85 idle reports also
remain unresolved. Neither unavailable physical device was accessed.

Next: test the exact RC2 upgrade/startup path in the isolated emulator and check
the exact Mac package with isolated data. Keep the WFC publication hold; do not
turn those offline checks into claims of online or physical-device acceptance.
