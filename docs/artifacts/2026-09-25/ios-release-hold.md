# Apple release hold — 25 September 2026

The owner withdrew release approval after severe iPad menu/loading stutter.
Do not publish the prepared 0.5.1 assets. Build73 package audits do not resolve
this report; its iOS runtime is the same pin as installed build72.

Read-only device inspection confirmed 0.5.1 build72 on the physical iPad Pro.
Latest captured session selected the base game, Metal/M2, Immediate presentation,
interpolation off, normal renderer diagnostics, nominal thermal status and
power-save off. The displayed resolution scale was 4.0. No configuration or
save data was changed during collection.

The runtime logs only a one-second rolling timing window every 300 presents.
Consequently one 300-present interval lasted 11.250 seconds while the sampled
window reported 60.003 FPS. Other intervals lasted 6.819 and 6.517 seconds.
These intervals include loading/pause time and are not isolated race benchmarks.
The logs cannot attribute their full duration to a particular subsystem.
Pipeline creation increased during transitions; shader waits are a hypothesis,
not an established root cause. No fix or gameplay acceptance is claimed.

Next private candidate adds rate-limited long-present and pipeline-wait logging
without enabling expensive renderer validation. Preserve the launcher's sun/moon
and filled Retro button changes. Identify the blocking path before changing
pipeline scheduling, rendering correctness, or user settings.

Private evidence: release worktree `work/ipad-stutter-20260925/`.
Do not publish the device logs, configuration, or app inventory.
