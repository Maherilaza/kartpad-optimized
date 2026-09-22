# Device-free preparation audit

Current candidate: RC2, Android175 and Apple64, compiled at f8e295a.
This records the requested preparation scope separately from publication approval.

| Requirement | Current evidence | Result |
|---|---|---|
| Review recent issues and replies | Fresh GitHub list has63 open issues; all63 numbers occur in the issue inventory; latest activity remains #216 on September21. Detailed reporter implications are in device-free-release-review.md. | Reviewed; no new closure evidence |
| Address actionable defects | Public Android signing corrected; all-platform captured send-error defect reproduced and corrected; identity migration retained. | Implemented and host-tested |
| Verify upgrade preservation | Public135→173→174→175 emulator updates retain UID and four synthetic sentinels. Exact Mac64 initializes settings from a synthetic legacy serial and preserves the legacy file. | Verified within synthetic/offline scope |
| Verify shared runtime behavior | Four-platform migration/sanitizer checks; four-platform send-error test; iOS receive/loopback/privacy tests; Android event-service test; Mac controller contracts. Both hosted jobs pass at c9cf501. | Host evidence; not physical acceptance |
| Audit exact packages/source | APK, IPA, Mac ZIP, source and notices hashes read back; clean source fingerprint matches APK/IPA; Mac commit matches;84 listed source members plus manifest verified; native/Maven dependency coverage audited. | Verified for RC2 |
| Document release blockers | release-confidence.md holds publication for unresolved iPad94020; graphics/controller limitations and unfinished features remain explicit in release notes. | Documented; not resolved |
| Avoid unavailable devices/unverified publication | Only dedicated emulator and isolated Mac fixtures used; PR317 remains draft; artifacts remain local. | Preserved |

The release notes and confidence document now identify RC2 consistently.
The source archive remains tied to its actual compilation commit; subsequent
documentation changes do not relabel it.

## Work not established by this audit

- Exact Mac RC2 Retro startup is now visually observed with a newly downloaded,
  hash-verified6.12.8 fixture; see clean-rc2.md. Android/iOS final-candidate Retro
  startup remains separate. Older local Retro extracts were not substituted.
- There is no new iPad WFC attempt with diagnostics, no explanation of94020 and
  no proven repair of the second Android profile's registration mismatch.
- Android GPU geometry and Moto G85 idle behavior remain reporter-specific open
  defects. SwiftShader observations cannot establish Adreno driver acceptance.
- Source PR reconciliation/merging and public release promotion remain separate
  work after acceptance; no formal release is authorized by this audit alone.

Continue with a version-matched isolated Retro fixture where obtainable. Keep the
physical/online evidence gaps explicit and do not replace them with passing unit
tests, build success or an increased package version.
