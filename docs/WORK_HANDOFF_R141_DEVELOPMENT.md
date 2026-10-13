# R141 — isolated layout development / NO FAB

Current accepted physical source remains R138. R140's whole-board audit is retained at commit 9852221013c1edcc3d2967d4e1eeab6da8140d34.

The user requested continuing the actual layout fixes. The local execution environment disconnected after real KiCad charger development. Last observed local preview at 2026-10-13T16:44Z: PCB SHA256 268921f24c81d6b0a727ce4e4b1c4d5db161acdd192d07db8c655c8b7bebf1f3, eight dangling tracks, one dangling via, one hole-to-hole finding and one remaining connection. This is observed progress, not a clean or published PCB checkpoint. The raw local files were not remotely saved before the environment disconnected.

The explicit recipes reconstruct the intended changes from the immutable accepted R138 seed: C5 at47.75,94.9/-90deg, C7 at44.5,91/180deg, C8 at52.5,91/0deg; short F.Cu supply paths and short GND returns; remove long VBAT In2 routing and interfering VBUS In1 routing; reconnect actual native pad groups. More recent proposal masks preserve the actual EP region and all five cap barrels, keep USB/SPI reference projections, and guard hole spacing even for same-net vias.

The GitHub development workflow first verifies unchanged canonical R138 with all27 scopes and all20 negative cases. It then applies the explicit proposal recipe **only in an isolated RUNNER_TEMP copy**, never in the canonical checkout. Existing R138 guards, checkpoints, approved source and manufacturer data remain unchanged. This is a development computation, not a CI repair of the verification source or baseline regeneration.

The process retains a ZIP, source hash, actual Native DRC state, routing measurements and review images under docs/evidence/R141. A failed or unfinished proposal remains explicitly incomplete. It does not replace the previously supplied PCBWay files or authorize manufacture. Inspect development_state_R141.json and its exact source hashes; retained local observations above do not substitute for a real server result.

After a native-clean charger stage: compact L2/D1/Q1/C25 and the negative charge pump, retain local C31 input decoupling, repair SPI return/reference issues, then establish and verify a new complete hardware checkpoint. Current script phase EPD/SPI is deliberately pending, and must not be described as completed.

No order, purchase, factory upload, supplier mail or consumer release was authorized or performed. Case thickness must not increase. Physical startup, battery/NTC faults, loads, firmware and factory qualifications remain open.
