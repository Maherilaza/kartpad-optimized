# iPad build57 shader-compilation crash — September 20

Owner testing found a real failure after installation. At 09:58:06 +0900,
KartPad 0.5.0/build57 terminated with SIGABRT. The crash UUID matches the
retained build57 symbols. This is an app crash; the report records about
410,000 seconds of device uptime and the retrieved inventory has no matching
new panic or Jetsam report.

The faulting pipeline worker entered operator new, threw through __cxa_throw,
and reached the C++ terminate handler. Its callers are Tint uniformity graph
construction, Dawn shader-module creation, Aurora build_shader/create_pipeline,
and compile_pending_pipeline. This establishes an unhandled allocation failure
while compiling a shader, not the previously corrected partial-startup cleanup
fault.

The session enabled six background compilation workers. Physical footprint grew
from 1,633,896,416 to 2,518,289,000 bytes over ten seconds; the last frame sample
still had 777 pipelines queued. The failure therefore occurred during continued
background compilation, even if the visible loading screen had finished.
Parallel compilation pressure is a strong lead, not yet a proven complete cause.

The subsequent session completed 2,244 prewarm pipelines in 2.6 seconds, reported
5,152 cache hits, and recorded approximately 60 presentation FPS for over a
minute. This is consistent with a warmer cache making the retry less expensive;
it does not clear the failed initial-start case or establish race performance.

The prepared physical-iOS source retains six background workers on this device;
only Simulator worker count is capped to one there. Android has separate bounded
prewarm controls. The next correction should bound physical-iOS speculative
compilation and verify a cold-cache launch without changing the owner's saves,
settings or active session. Do not treat a warm retry as the regression test.

Build57 is blocked from release pending correction and verification. Raw device
reports and logs are private in work/ipad-build57-20260920/incident. No app,
cache, save, configuration or running session was changed during this inspection.
