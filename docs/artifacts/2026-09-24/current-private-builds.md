# Private build status — 24 September 2026

This records what the current unpublished builds have actually proved. It is
not a release note or a claim of device acceptance across platforms.

| Platform | Current private build | Evidence | Remaining gate |
|---|---|---|---|
| Android | Pixel retained build: `0.5.1-android-nightly.14`, code 208. Latest emulator candidate: `0.5.1-framerate.1`, code 214. | Code 208's archived APK and the copy pulled after its in-place Pixel 9 Pro XL install have the same SHA-256, `a8b0d1867fe654d373b6044687b3b1e9593160163881c9be13aaa6f28e167579`. Candidate 203, whose source was rebuilt as 208, ran an active stationary 12-kart Cookie Land battle on that Pixel: 12.652 ms game-thread CPU per presented frame versus 14.70–14.79 ms for build 195 in comparable runs. Codes 209–211 passed release APK audits and each reached an active Luigi Circuit race on the API 36 ARM64 emulator. Code 212 passed a fatal-exit check; code 213 rejected a modified REL. Code 214 booted Original on the emulator and Android accepted a 60 Hz surface request. | Codes 209–214 have no physical-device comparison or smoothness measurement. The Pixel still has code 208; its package/readback check does not constitute a new measured gameplay run. Retro pipeline replay logged zero recorded and zero queued on the tested physical course. Driven races, Samsung/Adreno devices and online play remain open. |
| iPadOS | Installed: `0.5.1` build 66, signed development app. Latest compiled private app: unsigned build 69; no IPA packaged. | Build 66 passed the physical iOS app audit and strict signing check. It installed in place over build 65 on the iPad Pro, reports build 66, and launched as PID 999. The game image and 34 state files were backed up and read back byte-identical. Builds 67–69 compiled from newer iOS runtimes and passed full-game app audits; each executable and matching dSYM share a UUID. Build 69 includes the REL validation source. | Build 66 has no visual KartPad launcher or game-boot check: another app was foreground on the iPad during mirror inspection. Builds 67–69 have not been signed or installed. Original, Retro, WFC, replay and performance still need physical gameplay checks. |

The source branches and submodules have moved beyond the physical-device
artifacts. Guarded DVD DMA bulk copies are in all four runtime submodules and
passed C++ syntax checks. Android code 209 includes that change and a
scene-generation fix in its Android runtime. The fix invalidates both GX
pipeline memos when a course load begins, allowing previously seen recipes to
reach the scene recorder again. The iOS source has the same fix; macOS and tvOS
do not yet have it. The iPad build 66 includes the iOS changes through the GX
scene-generation repair, but has not been driven into either game.

Apple source revision `2a9a548` additionally ports Android's shared Aurora
render-mode lock, frame-owned debug marker/depth-peek mapping, GX GEN_MODE
first-write initialization, and alarm reschedule ordering to iOS, macOS and
tvOS. The six changed files match across the Apple runtimes; the three Aurora
implementation files passed a macOS host syntax check, and the alarm source
passed a separate syntax check. Android's surface-loss copy path was examined
but not ported because Apple's overlay draw has a different return contract.
Build 67 was compiled from the later iOS runtime revision `b07c4f3`, which
includes these ports and the guarded Yaz0 decoder. Its unsigned app is under
`build/ios67-20260924/xcode/Release-iphoneos/KartPad.app`; the maintained-source
stage verified against that runtime revision. The full-game iOS app audit
passed, `CFBundleVersion` is 67, and the executable SHA-256 is
`f839c613e1ca247cc7aab0160c7aa494c41cc1091969e1d5b7c6149a6f76805a`.
The executable and dSYM share Mach-O UUID
`0C713647-680E-3AB4-9A05-832C06609AD1`. The build log is private at
`work/ios67-build-20260924.log`. Build 66 predates these changes; build 67 has
not been installed or played, so neither validates the new decoder or ports on
an iPad.

Code 209 was built from Android runtime `f1677be`, with the private translated
shards, as `work/android-replaygen-20260924/kartpad-code209-replaygen.apk`.
SHA-256: `e34fc03afdb821dc641641323b8b017921b04a6c9cc5c52ad77a13f42f50cc61`.
The release audit verified version code 209/name `0.5.1-replaygen.1`; its APK
signer SHA-256 is `61dfb51411efe50b2e7fb8d280fcfbba766792c275d1024013940760caa3afaf`.
The emulator retained its app data through `adb install -r`. In one console
session, the first Luigi Circuit course load logged scene `c245398c16435baa`
with **213 recorded, 172 queued**. Selecting Change Course and the same Luigi
Circuit again logged the **same scene** with **342 recorded, 0 queued**; the
second race reached active gameplay. Restart within the race did not log a new
scene load, so it is not a replay-path check. The emulator already held a cache
from prior builds, and an empty second queue does not establish a startup or
frame-time improvement. The console and screenshots are in the same private
`work/android-replaygen-20260924/` directory.

Code 210 was built from Android runtime `97cdc9a`, with the same private
translated shards, as `work/android-yaz0-20260924/kartpad-code210-yaz0.apk`.
SHA-256: `8d1bbd8495579e54f3e8bb88cf94886a45530f51368ed3d3b439936b531df570`.
The release audit verified version code 210/name `0.5.1-yaz0.1`; its signer
SHA-256 is `61dfb51411efe50b2e7fb8d280fcfbba766792c275d1024013940760caa3afaf`.
It adds a guarded host-buffer Yaz0 decode to all four runtime source copies.
The host path requires mapped contiguous input/output, checks for protected
executable writes and deferred reads, and notifies GX of the completed write;
otherwise it uses the former scalar guest-memory path. An actual-source host
harness passed literal and back-reference cases on both paths plus checked
memory, executable-guard and deferred-read fallbacks. The four runtime source
files matched by hash, and all passed C++ syntax checks. These checks do not
measure a load-time or frame-time gain.

On the existing API 36 ARM64 emulator, code 210 kept app data through
`adb install -r`, opened Original, and loaded Luigi Circuit through Time Trials
to an active race. The private `work/android-yaz0-20260924/` directory holds
the audited APK, build log, console transcript and countdown/running-race
screenshots. The transcript identifies build 210 and shows no fatal or abort
through that run. The emulator was stopped without wiping its data. No physical
Android device was connected for code 210. Apple build 66 predates this Yaz0
change, so it does not validate the new decoder on iPadOS.

Code 211 was built from Android runtime `0ce6a52`, with the same private
translated shards, as `work/android-dvd-cache-20260924/kartpad-code211-dvdcache.apk`.
SHA-256: `21fd4b127bdf3e1df303d5b00eedfad8b8fac13e27383eadef65732c04889b13`.
The release audit verified version code 211/name `0.5.1-dvdcache.1`; its signer
SHA-256 is `61dfb51411efe50b2e7fb8d280fcfbba766792c275d1024013940760caa3afaf`.
All four runtime copies now use a bounded eight-handle, per-thread DVD file
cache for repeated exact reads. It checks modification time on reuse and
evicts the least recently used handle; the read bounds and output-on-success
contract remain in place. An actual-source host harness passed repeated,
zero-length, boundary, replacement, truncation, deletion, eviction and
concurrent-caller cases. A synthetic host benchmark of 20,000 local 4 KiB
reads took 224.708 ms with fresh opens versus 39.7558 ms with the cache. That
measures host file-open overhead, not game frame time.

On the existing API 36 ARM64 emulator, code 211 installed over 210 with
`adb install -r`; app files remained at 2.5 GB and 2,107 files. Original
booted, the saved license and menus opened, and a 50cc Luigi Circuit Grand
Prix race reached active gameplay. The private directory above holds the
audited APK, build log, console transcript and race screenshot. The transcript
identifies build 211 and showed no fatal or abort through the race check. The
emulator was stopped without wiping app data. No physical Android device was
connected, and this run is not a matched performance comparison. Apple build
67 predates the file-cache change; no Apple app with this change has been
built or tested on device.

On 25 September, all four runtime copies gained a central `RuntimeTerminate`
path for the named fatal exits, including missing guest targets, OS panic and
reset, guest exit, DVD/NAND root failures, and malformed Yaz0. It records a
reason, writes fallback artifacts if needed, stops audio and Aurora workers,
closes the transcript pump, flushes streams and exits without running static
thread-owning destructors. Other low-level abort sites remain outside this
change. The GX batching suggestion was inspected but not implemented: HLE
applies CP/BP state immediately while Aurora defers XF/INDX work, so batching
requires an explicit ordering contract at each synchronization point.

Android code 212 (`0.5.1-exit.1`) was built from the new runtime and private
translation into `work/android-termination-20260925/kartpad-code212-exit.apk`.
SHA-256: `4526f6f029aacced47fb6bcdea0dbe7d80fe41b9f67b85ad5c939166e7808a26`.
The release audit passed; signer SHA-256 remains
`61dfb51411efe50b2e7fb8d280fcfbba766792c275d1024013940760caa3afaf`.
On the existing API 36 ARM64 emulator, `adb install -r` preserved 2,109 app
files, 2.5 GB of data, and the exact `Config.toml` hash. Original booted into
the game's running attract sequence. A temporary invalid DVD root, launched
directly through `KartPadActivity`, produced `crash_dvd_root.txt`, an exit-1
reason in `console.log`, and `[runtime] process transcript ended`. The original
config was restored and read back with SHA-256
`e1e85a1693ebf504679f7d54123f38568e3a217ae315b0c214277ce9f04fe63f`.
The emulator was stopped without a wipe. This checks one fatal path, not all
fatal paths or an active race; code 212 was not installed on a physical phone.

Unsigned iOS build 68 was compiled from the same termination change and the
newer file-cache runtime at
`build/ios68-termination-20260925/xcode/Release-iphoneos/KartPad.app`.
Its full-game app audit passed, `CFBundleVersion` is 68, executable SHA-256 is
`b6d3cb66fb29b4226ec994ce5346ac5abcdf30d8f5703d2508506f59aaa76dde`,
and executable/dSYM UUID is `0A4C83E0-8F09-3F9C-8662-76EA46A50B37`.
Build 68 has not been signed, packaged as an IPA, installed or played on iPad.

The handoff's claim that extracted-folder imports do not hash executable game
files was incomplete: Android, iOS, macOS and tvOS already checked `main.dol`
in their game-data readiness paths. The actual gap was `StaticR.rel` on all
four platforms. The same readiness paths validate extracted staging after a
disc-image import, so the Android and iOS disc-image paths also gain the REL
check without duplicating hashing inside the extractors. The profile's pinned
REL hash matched the retained emulator's clean file. Rather than keep a
size/time cache that could accept a changed file, the readiness check hashes
the 4.9 MB REL on launch alongside the existing DOL check. No frame-loop hash
was added.

Android code 213 (`0.5.1-imagecheck.1`) built from this source, passed the
release APK audit, and has SHA-256
`ac0888f54f6e47657a0bd1f6590bffc9d4cb0ab26290df8e3f7994903b124f9f`.
Its signer remains
`61dfb51411efe50b2e7fb8d280fcfbba766792c275d1024013940760caa3afaf`.
On the existing API 36 ARM64 emulator, `adb install -r` preserved 2,114 app
files, `Config.toml`, and the clean REL hashes. The launcher showed “Ready to
play” and Original began booting. A one-byte modified REL, staged only after
pulling a byte-identical backup, changed the launcher to “Setup needed” and
displayed the clean-dump message. Restoring the backup read back to SHA-256
`16d9d146112541fefea701ecb5bc1a496f9d50e4a752fbb5b6778e7c6399f67d`
and restored “Ready to play.” Screenshots, build/audit logs and the private
APK are under `work/android-imagecheck-20260925/`. The emulator was stopped
without wiping data. This is a launcher/boot check, not a driven race or a
physical-device test. The macOS and tvOS source checks have not yet been built
or run.

Unsigned physical-iOS build 69 compiled the iOS REL validator from runtime
`4eab579` and the pinned translation into
`build/ios69-imagecheck-20260925/xcode/Release-iphoneos/KartPad.app`. The
full-game app audit passed, `CFBundleVersion` is 69, executable SHA-256 is
`fb855175603064281da2125b146bcc4fe870bd8f99e17f391eb4013f6e425028`,
and executable/dSYM UUID is `6A0F8393-834C-38B4-BD04-B71FA6EA1358`. The
build log confirms `KartPadRuntimeOverlayHost.mm` compiled, and the binary
contains the modified-data message. Its `kartpad-build.json` records the four
runtime commits and translation fingerprint; `source_dirty=true` reflects the
owner's unrelated dirty document plus the staged iOS gitlink at build time.
The app is unsigned and has no IPA. It has not been installed or played on an
iPad; compilation does not prove the new rejection flow on Apple hardware.

The build 66 iPad receipt is in `work/ios66-install-20260924/`. It was built
from a fresh stage of iOS runtime `0df334c` plus the build-number change later
committed as `e5902c8`. The unsigned executable SHA-256 is
`09d7af226fa11ec53d4228fdea1e5077896ff164d955b2a241da9e3ce6373db9`;
its Mach-O UUID is `4459EAE6-B408-301E-A257-D2E2FD3D5E85`. The existing
development profile and signing identity were reused. A fresh pre-install
backup and post-install readback matched for the 2.6 GB game file (SHA-256
`fc035e60610842da6860d23d4a30c1f1c0f019d492469deb8a2ac25ef5822331`)
and all 34 other files. The build 66 process transcript confirms PID 999 and
version `0.5.1` build 66, but contains no game boot. A wired mirror displayed
another app in the foreground, so KartPad was left undisturbed pending an
available iPad session.

The handoff's GX, Adreno and floating-point proposals remain
hypotheses or bounded experiments. In particular, the available shader evidence
does not prove an Adreno driver defect, and a lower game-thread CPU number does
not by itself establish smoother presentation.

The 25 September GX source check narrowed the proposed first batching step.
`GX__CallDisplayList_80172f64` does not rescan every list on every call: it
has a bounded scan cache keyed by guest address, bytes and vertex layout, with
write-generation and content-digest validation; register-only lists bypass the
index scan. The retained Pixel log shows 203,218 probes and 73,144 validated
hits in one five-second interval, with no eviction. `HleFifoWrite` applies
CP/BP writes immediately, while XF/INDX packets are sent to Aurora and draws
depend on the resulting order. Any batch across those boundaries needs a
separate ordering proof and matched gameplay measurement; no GX batching was
shipped from this source review.

Android code 214 (`0.5.1-framerate.1`) requests the output rate on its native
window at surface creation and reconfiguration: 60 Hz normally, or the selected
interpolation target. It loads `ANativeWindow_setFrameRate` dynamically so
API 28–29 remain supported. The pinned NDK header recommends default
compatibility for game content; the handoff's fixed-source suggestion is for
video. The private release APK passed the package audit, retains the code 213
signer, and has SHA-256
`e6d71a721b4aaf5ddb00cf5c055fc9ae6687d27958bb8c97c27c2ae49bd044fc`.
`adb install -r` over 213 preserved 2,115 app files and the same config and
REL hashes. On the API 36 ARM64 emulator, Original reached its opening
sequence and the session transcript recorded
`Android surface frame-rate request 60 Hz: 0` followed by Vulkan FIFO mode.
The zero return shows Android accepted the hint; it does not prove that a
physical display switched rates or that gameplay became smoother. The private
APK, build/audit logs, transcript and screenshot are under
`work/android-frame-rate-20260925/`. A matched 120 Hz Samsung race and Pixel
battle comparison remain necessary before retaining this as a performance
improvement.

Evidence: [Pixel comparison](../2026-09-23/android-copy-stream-loop.md),
[Android build 195 baseline](../2026-09-23/android-morning-report.md), and
[deep review](deep-review-handoff.md). The private receipts and APK are under
`work/android-optimization-20260923/`; the iPad install/readback receipts are
under `work/ios65-install-20260923/` and `work/ios66-install-20260924/`.
Those directories contain private or
game-derived material and are not release assets.
