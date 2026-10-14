# PCBWay R142 review instructions - NO FAB

Use the R142 packet as a coherent set. Board59x101x1.6mm, four copper layers; absolute origin0,0, X=boardX, Y=-boardY in mm; envelope X18..77,Y-121..-20mm. Native top angles remain unchanged. Have the supplier return a BOM/CPL import preview; mapped column names do not establish rotation/origin correctness.

114 fitted top parts;19 bare PCB entries; R67 DNP and no paste. B.Paste intentionally empty. All453 native pad records include documentation/paste-only/mechanical objects; IPC356 contains439 emitted conductive pad records and373 via records. Separate PTH/NPTH drills contain four plated USB shell slots and nine NPTH holes.

Approve nominal0.20mm drills84 locations on1.6mm, finished dimensions/thickness/registration/copper plating and actual aspect limits.373 vias all have nominal ring >=0.15mm. All367 ordinary vias retain >=0.10mm clearance to SMD lands. The five U3 and one R28 exact process CSV sites require resin fill and copper cap, with agreed finish/flatness/voiding. Do not substitute tenting for fill/cap under paste.

Agree common U1/U3 stencil/reflow, U1 EP grid, solder-mask webs, dense pad/body/courtyard spacing and source-specific footprint orientation. GCT USB4215-03-A has four plated slots, short nominal0.8mm stakes on1.6mm board and no locator holes; agree hybrid soldering and retention. Approve actual90-ohm USB stack with tolerance and importer handling of solder-mask opening polarity.

Current logic/panel rail nominal3.24549V uses exact precision feedback parts, with TLV803EA30DBZR reset. SD CMD/DAT0..3 use10k external pullups; DAT1/2 are bias-only. GPIO39 detection is separate. No dock or mainboard battery PCM is present. Require approved protected pack and separate bonded NTC.

Release holds include panel pin5 VDHR/VSH2/contact-side/FPC/case confirmation, joint rail PFM/overshoot/load/lifetime margins, ceramic Ceff/HV/current/thermal, battery/NTC faults, firmware and actual FCT. Read PRE_REVIEW_CHECKS_R142 and FCT_PLAN_R142. Generated files and computational passes do not release manufacture, purchasing or assembly.
