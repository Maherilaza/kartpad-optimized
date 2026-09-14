# iOS anonymous guest RAM

The #196 build39 microstackshot reported 4,336.72 MB of file-backed dirtiness, with frequent guest zero-fill frames. Its fatal missing-function dispatch is separately unresolved. The iOS allocator mapped guest RAM through unlinked temporary files with MAP_SHARED, so ordinary RAM writes dirtied file-backed pages.

The allocator now uses anonymous writable host pages and public `vm_remap` aliases with `copy=FALSE` inside its reserved guest address range. This removes temporary files from guest RAM backing while preserving coherent physical/cached/uncached views and independently protected guest pages. macOS retains its existing shared-memory backing. A separate follow-on patch is applied by Apple preparation; Android explicitly skips it before layering its existing allocator patches, preserving Android patch compatibility. Initialization rejects invalid/overlapping layouts before fixed overwrites and releases reservations, aliases and backing resources after partial failure. Successful allocation remains process-lifetime, as before.

## Executed validation

Run on Apple Silicon Darwin:

```sh
python3 scripts/test-apple-guest-memory-aliases.py --runtime-include /path/to/prepared-apple-runtime/include
```

The harness extracts the actual implementation from the patch and uses the prepared runtime's public header. A TargetConditionals shim selects the iOS branch on the host. Real kernel calls test:

- Host and three guest mirrors share writes, including page boundaries and nonzero section offsets; MEM1/MEM2 and independently owned sections stay isolated.
- Guest page protection blocks reads without blocking the host or another mirror; unprotection restores access.
- Same-layout initialization zeros backing without relocating it; different layouts fail while preserving live state.
- Invalid, empty-sized, out-of-range and overlapping regions fail before allocation. An injected second-remap failure leaves no live reservation or retained sections, and initialization can retry.
- Three complete allocate/release cycles and the real WiiDefaults sizes (24 MiB MEM1, 128 MiB MEM2, 2 MiB overlay, locked cache) pass.
- `VM_REGION_EXTENDED_INFO.external_pager` identifies the old unlinked-file mapping as file-backed and the new host/guest mappings as anonymous, including after full-size writes. This is a positive control for the backing change, not a gameplay measurement.

The actual implementation also compiles and links for arm64 iOS 17 with the iPhoneOS 26.5 SDK, using its public `vm_remap` declaration/export. Its macOS branch compiles with warnings as errors. `mach_vm_remap` was deliberately not used: the iPhone SDK does not support its header.

No hardware gameplay, speed improvement, reduced on-device write count, or correction of #196's missing indirect target is claimed. The remaining release check is launch/race/relaunch of an iOS candidate and confirmation that the new backing remains permitted in the signed device app. No saves, game assets or user identities are modified by this allocator change.
