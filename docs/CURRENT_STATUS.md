# ENKU Base Reader - current status

Updated13October2026. **Physical PCB R138 / qualification and documentation R139 / NO FAB.** [Canonical KiCad](../hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro). PCB SHA256 `90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971`.

| Area | Current evidence | Release status |
| --- | --- | --- |
| Electrical/layout source | Actual native10.0.7 DRC/ERC/opens/parity zero,27 scopes,20 effective rejection cases | Computationally verified |
| Manufacturing files |11 Gerbers,2 drill files,IPC,107 fitted BOM/CPL; full copper/stencil/process checks | Engineering-review inputs verified |
| Programming/recovery |J7 UART/BOOT/EN/VREF and USB/strap source audit passes | Physical flashing/recovery NOT RUN |
| PCBWay packet |128 files,4 PDFs/30 pages; original24 manufacturing files byte-identical; CRC/SHA/semantics/visual QA pass | Engineering review only |
| Factory process |91 nominal0.20mm bores on1.6mm,6 fill/cap sites,U1 EP grid,USB short stakes,stack/90-ohm pair/stencil | Job-specific acceptance HOLD |
| Battery/case |2-wire1S PCM,PH-2,separate NTC;2000-2500mAh/about4mm/no thicker case | No qualified interchangeable CN/PL pair or final fit |
| Startup/load/charging |Models and procedures; USB100 weak/absent-cell start,EN ramps/cycles,Ceff,combined loads,CC/CV/timers/NTC faults unresolved | Physical qualification NOT RUN |
| Display/FPC |Supplier pin5 clarification exists; actual controlled panel/connector/contact/bend mapping still needs validation | Integration HOLD |
| Firmware/FCT |Recovery contract,20 test groups and blank unit logs | No approved image set/offsets/fixture/numeric criteria bound to R138 |
| Consumer release |Final HW/BOM/case/packs/FW and measured validation required | HOLD |

Next engineering work: resolve startup/source/reset and NTC electrical/retention faults; finalize actual thin protected pack envelopes/two purchase channels/current case CAD; validate panel/FPC drawings; agree factory processes and validated diagnostic/release images/fixture/limits; then perform measurements on user-approved EVT samples and establish per-unit FCT.

[Latest battery review](BATTERY_STATUS_R139.md). Current charger: BQ24072T,445mA nominal, modeled max492.42mA/BAT max4.24V. Original BQ25185/300mA RFQs are obsolete. No mail sent during this pass.

## Exact engineering-review archive

`ENKU_Reader_Base_R138_PCBWay_Engineering_Review_NO_FAB.zip`,2732875bytes,SHA256 `c113ffdac4c2613a2f8736acf692a01c063a4e41b7f521715bab50e7373a3b00`. [Packet record](qualification/R139/PCBWAY_PACKET_R138.json), [process instructions](PCBWAY_MANUFACTURING_NOTES_R138.md), [test plan](PRODUCT_QUALIFICATION_R139.md), [flash contract](FACTORY_FLASH_CONTRACT_R139.md). The archive is supplied separately; hashes/build instructions are retained here.

Documentation integration does not change that packet's physical source. Supplier updates retain battery HOLD and do not change Gerber/BOM/CPL. Current main-run verification is recorded separately from historical R138 source2601e16 proof.

## Actual consolidated main verification

Source `43a19802074b249ef29fd31211ede7e863c8e204`, tree `8e71ef7f14c0aa7bd95865c8c435e6ee9b9e4ed1`: [actual GitHub run38356800482](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38356800482) completed successfully with all11 job steps. Native KiCad10.0.7 verified27 scopes and20 effective rejection cases; DRC/ERC/opens/parity are zero.

The downloaded artifact11792769984 is1147016bytes with79 unique CRC-verified members and SHA256 `2abc4456ac89f04aa4e9937c4a0c8dd6fd67be49100cc161c2d754dfb0d958dc`. Independent comparison verified28 PCB-bound reports,8 native SVGs and all24 manufacturing files against the retained local native result; only explicit export timestamps were normalized. [Proof record](GITHUB_MAIN_R139.json) / [exact artifact and API records](evidence/R139/main/native_server_R138.zip). Subsequent proof/documentation changes retain exactly the same hardware and workflow source.

Physical qualification remains **NOT RUN**, consumer release and fabrication **HOLD**. A successful native run does not qualify a battery, firmware image or factory process.

[Index](README.md), [handoff](WORK_HANDOFF_R139.md), [consolidation](REPOSITORY_CONSOLIDATION_R139.md), [hours ledger](DEVELOPMENT_HOURS_READER.json). Hours are a measured lower bound excluding interruptions; no historical total is invented.
