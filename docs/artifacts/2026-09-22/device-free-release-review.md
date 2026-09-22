# Device-free release preparation — 22 September 2026

The owner declared both physical mobile devices unavailable. This pass uses
source review, host tests, packaged binaries and a new isolated Android emulator.
No Android/iPad hardware was accessed.

## Live GitHub review

63 open issues; every issue maps to the existing inventory. The latest issue
activity is the September 21 21:40 UTC Retro-startup confirmation in #216. No
new issue or later reply was found beyond the previous review snapshot. Recent
responses and supplied evidence were rechecked; no repeat diagnostic requests
or speculative issue closures were sent.

| Primary family | Open tickets |
|---|---:|
| Android cup exit | 2 |
| Android geometry | 9 |
| Android input / display | 4 |
| Android launch / compatibility | 11 |
| Android mixed performance / exit / saves | 2 |
| Android online | 2 |
| Android sustained performance | 9 |
| Apple startup / performance / rendering | 8 |
| Compatibility / feature scope | 6 |
| Content installation / build inputs | 4 |
| Insufficient symptom or platform | 2 |
| Mac physical controller | 2 |
| Save / ghost / identity | 2 |

## Engineering implications

- #216: Galaxy A9+ code135 now has reporter-confirmed Original and Retro startup.
  Missing models and performance remain separate unresolved symptoms.
- #215: Xiaomi reporter confirms startup; unspecified build prevents attributing
  it to one correction.
- #301: separate missing models, transition compilation stalls, and input/idle
  frozen gameplay. A live presentation FPS counter is not guest progress.
- #211/#104/#316/#308: device-specific missing/displaced geometry remains open.
  Generic CPU changes and new package versions are not proof of a fix.
- #306: actual Classic extension mapping reads SDL raw buttons and emits KPAD
  Classic bits. The native controller remapping panel edits PAD (GameCube)
  bindings, which this physical Wii Remote path bypasses. This explains why
  those remaps do not apply; it does not explain physical Bluetooth latency.
  All 65,536 synthetic two-byte Classic button combinations pass through the
  built SDL driver's actual button table and the maintained runtime's actual
  mapping, including each D-pad direction, diagonals and release. No D-pad
  mapping patch is justified by this test; physical behavior remains unaccepted.
- #314: retain prior complete RVZ extraction/preservation proof; the importer
  change remains unreleased.
- #295: Original export accepted; Retro transfer still separate feature work.
- #234: restoring a save alone cannot migrate its server-bound console identity.
  The new legacy-identity upgrade fix is not a general cross-console transfer.

## Public Android upgrade blocker corrected locally

The private code173 APK uses a different certificate from public 0.5.0/code135.
It must never be substituted for the public update asset. Located the existing
release key without changing it and derived a universal APK from the corrected
code173 AAB through the normal release script. Its certificate matches the public
release identity. All four native libraries are byte-identical to private173.

A newly created isolated API36 ARM64 emulator accepted public135, then public173
with install -r. The app UID and four synthetic identity/save/preference byte
sentinels survived the update and subsequent chooser launch. UI hierarchy shows
Mario Kart Wii and Retro Rewind. The harness was corrected to check the separate
:launcher process and the actual Mario Kart Wii label; neither mismatch was an
app crash. No game was imported or raced in this emulator.

Mac profile persistence/virtual SDL mapping, port assignment and host scheduler
tests pass; scheduler sanitizer tests also pass. These are host correctness
checks, not claims of improved latency or phone FPS.

## Remaining loop work

1. Audit complete dependency/source delivery against the exact binaries; the
   core source snapshot alone is not the full release source package.
2. Finish notices, reproducibility receipts and source/package provenance for
   the public-signing Android candidate.
3. Investigate #301 guest-progress/idle behavior using deterministic host inputs
   and source evidence. Retain graphics compatibility limits rather than merging
   an unproven driver workaround.
4. Keep iPad 94020 unresolved; device unavailability does not turn it into a
   server-side finding. Continue host protocol investigation where useful.

Work remains in the existing stabilization worktree and PR #317; no public
release was published. Private logs/fixtures are under
work/mobile-network-repair-20260922.
