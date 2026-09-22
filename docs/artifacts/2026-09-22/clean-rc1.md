# Clean release candidate 1 — 22 September 2026

All candidates identify clean source `2886684b7ec994e685dc0bc9f097dbbdc953551e`.
Android code174 (0.5.1-rc.1), iOS/iPadOS build63 and macOS build63 compile and
pass package audits. Android uses the existing community release certificate;
Apple IPA remains unsigned. No attached mobile device was accessed.

Android and iOS embed the same recursive source fingerprint:
`cb5fa319707713a03c2c1e0c1a08ce75fa2749cabe2f137e93d42c481201db00`,
covering 7,346 files, with source_dirty=false. Mac packaging records the same
compilation revision. Every prepared runtime was checked against its maintained
source; an outdated staged Mac test was synchronized before that check passed.

The coordinated source packager verified the clean APK/IPA fingerprints and Mac
revision against the recursive core snapshot before composing the 85-member
source delivery. All delivery-member hashes/sizes and final asset checksums were
then independently read back. The archive includes the verified dependency
source delivery and current rebuild instructions, not just the core snapshot.

29 fetched CMake dependency source trees across Android, iOS and Mac were compared
file-by-file against archived dependency sources. All match except the expected
iOS SDL UIKit text observer correction. Applying the tracked
cmake/PatchSDLUIKitTextFocus.cmake to the archived SDL source reproduces that
built file exactly. Apple/Android use SDK zlib rather than the unused upstream
zlib source-download fallback. Android's separately supplied SDL AAR remains
3.4.4, with corresponding source in the delivery.

Artifacts live in the ignored build/release-051-rc1-20260922 directory: public-
signer APK, unsigned IPA, Mac ZIP, complete source archive, notices ZIP and
SHA256SUMS.txt. Matching Android symbols, iOS dSYM and the unsigned AAB are
retained privately. Exact hashes and executable comparisons are in
[clean-rc1-packages.json](clean-rc1-packages.json).

## Acceptance boundary and next work

This resolves the dirty-source packaging/provenance gap, not the iPad 94020
login failure or reporter-specific Android geometry/performance defects.
Previous emulator135-to173 preservation evidence and Mac62 synthetic migration
proof remain separately labelled; neither is presented as a physical174/63 race.

Next loop: verify the final174 public upgrade/chooser path, finish release
metadata and investigate #301 idle/input-dependent guest progress using host
evidence. Review native code equivalence before deciding which prior correctness
checks need repeating. Do not publish solely because archives and CI pass.
