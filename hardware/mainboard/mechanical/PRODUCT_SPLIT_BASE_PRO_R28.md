# ENKU Reader — Product boundary decision R28 (2026-10-08)

**Owner-approved architecture: Base and Pro have physically DIFFERENT production PCBs.** No DNP or shared-universal-PCB compromise to carry Pro features on Base.

## Base Reader
- **Dedicated Base PCB**, not Pro PCB without components. Keep pocket form factor, non-touch physical controls, BMI270, Good Display `GDEY0397T81P` monochrome 3.97-inch (pending real flex fold), USB-C, microSD, protected 1S battery, hard mechanical power off.
- No magnet/cover sensing or Hall U6; **remove U6, C20 and HALL_INT entirely** instead of depopulating. Former ESP32 GPIO is free/NC for this Base variant.
- **No wireless charging receiver IC, rectifier, Qi coil, ferrite shield or charge-route copper**. Existing USB charging may remain subject to power integrity audit.
- **No frontlight LED/driver/connector on Base PCB**. The current selected Good Display screen has no frontlight assembly.
- No magnetic case/cover dependency, dock and accessory roadmap are independently reviewable. Base must fit in the smallest viable pocket shell.
- R28 experiment `enku-mainboard-r0.5-base-only.kicad_pcb` is the first no-Hall PCB copy; R27 mechanical work preserved for comparison.

## Pro Reader — new, distinct hardware project (not implemented as a DNP variant)
- **Different e-paper/display assembly with frontlight**, final manufacturer and size UNSELECTED. Cannot reuse Base J3 FPC footprint/pinout by assumption. Prefer adjustable frontlight including warm white if chosen module supports it.
- Dedicated **Qi wireless charging receiver IC and receiving coil + ferrite shield**, battery charger/power-path and thermal design that match chosen Qi supply; a lone coil is NOT a charger. Shield MCU RF/magnetometer if any; control heat near LiPo and display.
- **Separate Pro PCB** with its own layout, schematic, BOM, assembly variants and manufacturing/DRC tests. May share ESP32-S3 code, software architecture, building blocks, mechanical design language and connector *principles*, not production Gerbers.
- Hall sensor is a **potential Pro accessory/cover feature**, not mandated until Pro cover, magnet polarity, and actual magnet-to-sensor assembly geometry are defined.
- Pro board outline, battery, height, dock arrangement, and mechanical control positions are **not constrained to Base 59×101mm**: they depend on new screen + frontlight light-guide + coil Z stack.
- Pro requires independent power-budget, RF/Qi coexistence, battery charging and heating, FPC pin mapping, frontlight driver noise, PCBWay production and safety checks.

## Branch / ownership rules

- **This repository: `ENKU-Base-reader` is the BASE hardware source of truth.** Use `engineering/r28-base-dedicated-pcb` as working branch. Legacy R0.1 and R25–R27 are research/history not approved for manufacturing.
- Pro PCB must be a **separate KiCad project (ideally separate `ENKU-Pro-reader` repository once created by owner)**. Do not add Pro footprints, Qi keepout sketches or parts to Base board. A *common reusable footprint library* may be shared with separate versioned releases.
- Hardware features cannot sneak back into Base through status docs/BOM/legacy F.SilkS. Regulatory and prototype qualification is product-specific.
- Firmware can share ENKU Core, with **explicit per-board compile-time target/config** (`ENKU_BASE` vs `ENKU_PRO`); do not probe absent Hall/frontlight/Qi on Base at runtime as a mandatory feature.

## Implementation in R28 research branch
- A new Base-only PCB copy drops **U6 DRV5032FBDBZR and its sensor-only C20 100nF**; therefore 122 → **120 physical footprints**. Keep BMI270.
- Active schematic sheet removes U6, C20 and magnetic-cover sensor labels; replaces former MCU `HALL_INT` pad label with `no_connect`. `check_schematics.py` now rejects Hall returning to dedicated Base active circuit instead of requiring it.
- A Base segregation checker compares complete 120-footprint list to frozen R27 reference, excluding those exact two components and forbids Qi text/features. It does not certify KiCad native ERC/DRC, schematic/PCB parity or manufacturing.
- Note: historical KiCad project root and old PCB files remain intact in repo for forensic study and may no longer match the **active variant**; a clean production Base KiCad project and BOM/CPL will be assembled after FPC constraints are frozen.

**No Base or Pro Gerbers are approved for ordering as of this decision.**
