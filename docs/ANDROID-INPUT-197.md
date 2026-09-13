# Android issue #197: A input investigation

Status: unresolved. This is a maintainer test plan, not a device acceptance
record or a claim that Android build 80 fixes the report.

[Report and follow-up](https://github.com/chrissotraidis/kartpad/issues/197):
Moto g200 5G, reported 0.4.16, ipega controller in Xbox mode; A stops activating
track-selection and online-room menu actions on both controller and touch after
controller use. Gameplay still responds, with automatic acceleration observed.
Default-mode A/B failures are a separate mapping observation. The reporter has
already been asked for a fresh offline touch-only comparison; do not duplicate
that request.

## Source evidence at cf1f59a

- `KartPadOverlayView.beginGasPress` deliberately locks touch A after 1,000 ms.
  The A control turns cyan; another touch A press unlocks it. This state publishes
  A continuously. It is not evidence that the reporter enabled it.
- `clearTouchInput` cancels the hold generation, clears the lock and pointer
  owners, and calls native clear, which also clears pending touch edges.
  `KartPadActivity` calls this on pause/focus loss and when controller handoff
  detects a connected game controller. Android's device count is not proof of
  SDL assignment or a delivered SDL detach event.
- `wiicompiled-android-touch-input.patch` ORs touch and physical classic buttons
  into the same hold mask. The KPAD trigger calculation introduced in
  `wiicompiled-apple-runtime.patch` uses `classicHold & ~previousClassic`.
  A continuously held from either source can therefore suppress a fresh A edge
  from the other source. This mechanism fits the two symptoms but does not
  establish their cause on the reported device.
- `aurora-android-gamepad-event-cache.patch` retains button-down state until
  button-up, samples SDL state at add/remap, and erases the controller on removal.
  The lifecycle suspension masks snapshots and stops rumble but does not reset
  cached button state. A missed release across focus loss is a candidate to
  reproduce; ordinary delivered down/up and detach should recover. Clearing
  cached state blindly could instead lose correctly held controls on resume.

## Maintainer reproduction and negative controls

Use an authorized test device and the exact recorded APK/profile/controller
mode. Follow [the physical handoff runbook](ANDROID-PHYSICAL-HANDOFF.md) for
artifact identity and capture. Work offline first; do not interrupt an online
session to run this matrix. Keep saves, installation and controller mappings.

| Trial | Action | Observation that distinguishes the path |
| --- | --- | --- |
| Baseline | With no controller attached, use short touch A taps in the same offline track menu. | Record whether A works before any controller use. This is the already-requested reporter comparison. |
| Intentional touch lock | Hold touch A over one second, note cyan A, then test short taps; unlock with another A press. | Establish the visible lock signature and recovery. A matching signature supports the touch-lock path; absence alone does not prove the SDL path. |
| Normal controller use | In Xbox mode, repeatedly press and fully release A, then tap touch A with the overlay visible. | Both sources should produce new menu activations after release. This controls for button mapping without lifecycle changes. |
| Held versus released focus loss | Compare background/foreground after A is fully released with background while A is held, release while away, then return. | Failure only in the latter isolates a possible lost-release boundary. Record whether a fresh controller A press/release recovers it. |
| Held versus released detach | Compare unplug/disconnect after release with disconnect while holding A; wait for handoff before touch A. | A delivered SDL removal erases cached state. Persistent failure after real removal points away from that controller cache alone. |
| Default mode | Separately check A and B in the controller configuration screen, then the same offline menu. | Capture the exact ipega model and recognized SDL button behavior before changing mappings; do not combine this with Xbox-mode results. |

For each failure, record menu item, input sequence, cyan-lock visibility,
controller presence, whether acceleration persists, and which recovery works:
touch unlock, physical A down/up, disconnect, or cold relaunch. Record the
first successful recovery rather than applying all of them before observing.
Controller reconnect and focus loss also clear touch input, so recovery by
those actions alone cannot identify which source was held.

Only if a maintainer capture reproduces a stale physical A should a runtime
fix be selected. Its regression test should cover a lost release at the actual
boundary plus normal held input, short taps between guest samples, and detach.
Host touch/contract tests validate their own code paths; they do not reproduce
this ipega report or prove menu acceptance.
