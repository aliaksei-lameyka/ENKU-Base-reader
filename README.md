# ENKU Base Reader

ENKU Base Reader is an independently developed, compact **3.97-inch e-paper reader** built around a custom ESP32-S3 mainboard. The goal is an inspectable, repairable, local-first reading device with physical controls, removable storage, and no required cloud account or subscription for reading locally stored books.

> **Status: Base R0.1 — engineering / first-spin development.** The board has **not** passed its fabrication release gate. Files in this repository are not a PCBWay-ready production package.

## Base R0.1 at a glance

| Area | Current engineering baseline |
| --- | --- |
| Display | 3.97-inch, 800 × 480 e-paper panel interface; 24-pin FPC |
| MCU | ESP32-S3-WROOM-1-N16R8 |
| PCB | 4 layers; 54 × 94 mm current outline; portrait-first |
| Storage and connectivity | microSD, USB-C |
| Navigation | Four side-edge buttons, two per side, for configurable left/right-handed controls |
| Motion sensing | BMI270 IMU |
| Power | Li-ion charging, USB/dock power-path handling, 3.3 V regulation, hard power switch |
| Dock | Rear dock connection and detection interface |

A Hall sensor is **still present in the current R0.1 design**, but its necessity is under review: Base is not being designed around a magnetic cover. Its presence in the design files should not be interpreted as a committed product feature.

**Outside the Base R0.1 scope:** frontlight and wireless charging. A separate, more fully featured variant may address these later; no Pro hardware is released here.

## Current work and limitations

The KiCad schematics, PCB, project-local libraries, and structural validation scripts are available. Routing closure, display-flex geometry, component orientation, mechanical interfaces, and manufacturing-file review are still release blockers.

The engineering goals are low-power operation, repairability, and reproducibility; they are **design goals, not yet verified production specifications**. Firmware and enclosure sources are not yet published in this repository.

## Repository guide

- [KiCad source and validation scripts](hardware/mainboard/kicad/) — editable mainboard design and engineering checks
- [Mainboard notes](hardware/mainboard/README.md) — current hardware release scope
- [Hardware overview](docs/hardware.md) — interfaces, controls, and mechanical envelope
- [Validation and fabrication gate](docs/validation.md) — checks required before ordering boards
- [Manufacturing notes](docs/manufacturing.md) — release package expectations
- [CI workflows](.github/workflows/) — structural and native KiCad checks

Manufacturing outputs (Gerber, drill, BOM, CPL, and assembly notes) will be published under `hardware/mainboard/production/<revision>/` **only after** a revision is approved for fabrication.

## Running the lightweight checks

From the repository root, with Python 3:

```sh
python3 hardware/mainboard/kicad/check_schematics.py
python3 hardware/mainboard/kicad/check_pcb_placement.py
python3 hardware/mainboard/kicad/check_footprint_consistency.py
python3 hardware/mainboard/kicad/check_pcb_population.py
```

These scripts catch structural and placement regressions. **They are not substitutes for native KiCad ERC/DRC** or an electrical/mechanical review. The repository includes a native KiCad workflow for pull requests and manual execution; a passing workflow alone does not authorize fabrication. See the [release checklist](docs/validation.md).

## Revisions

| Revision | Purpose | Status |
| --- | --- | --- |
| Base R0.1 | First engineering board / EVT | In development |
| Base R0.2 | Bring-up and first-spin corrections | Planned |
| Base R1.0 | Production candidate | Planned |

## Licensing

ENKU Base Reader uses **different licenses for different types of work**:

- **Original hardware design** — [CERN-OHL-W-2.0](LICENSE), including the KiCad PCB/schematic design and ENKU-authored hardware files.
- **Software and automation scripts** — [MIT](LICENSES/MIT.txt), including the Python validation tools and any future firmware expressly released in this repository.
- **Original project documentation** — [CC BY 4.0](LICENSES/CC-BY-4.0.txt), including README files and `docs/`.

Read the [license scope and third-party exceptions](LICENSE.md) before redistributing files or manufacturing modified boards. Third-party materials keep their own terms. The ENKU name and logos are not granted as trademarks by these licenses.

## Related project

[ENKU Originals](https://github.com/aliaksei-lameyka/ENKU-Originals) is a separate, early-stage experiment in AI-assisted, human-edited short fiction and reader-first EPUB delivery. It is currently private. **Its stories and editorial content are not licensed by this repository.**
