# R135 first-board test plan

**Planned; NOT RUN.** Execute the twelve-stage [R134 fixture/bring-up sequence](BRINGUP_R134.md) with the [current R135 contract](USB_POWER_CONTROL_R135.md). Begin with unpowered inspection and current-limited/sink-capable emulators, then approved PCM packs only after fixture gates. Capture source SHA, assembled BOM/pack and firmware revisions, calibrated fixture, ambient, scope/current logs and verdict.

R135 amendments: verify all four distinct switch pads/contact pairs and lower rectangular actuator/pusher/stroke; measure healthy nominal4.90–35.01°C window using actual controlled sensor/input corners. Inject R81-open at45°C and require inhibit under the reviewed leakage/RT envelope; detached sensor remains a known separate failure. Test R82/fault isolation and polarity/clamping. The inherited old R81-open unsafe-model prediction is superseded, not hidden. Measure actual full2000/2500mAh charge cycles, heat, OFF/boot/current/suspend transitions, both Type-C orientations, peripherals, USB MSC exclusive SD ownership and hotplug/replacement stress.

No physical outcome is inferred from native success. Design/factory gates precede an approved EVT submission; tests requiring boards follow delivery and precede production. [Current fabrication gates](DFM_REVIEW_R135.md). No manufacture, orders or supplier messages.
