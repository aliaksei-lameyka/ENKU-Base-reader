# PCBWay R144 review instructions - NO FAB

Use the R144 packet as a coherent set. Board59x101x1.6mm, four copper layers; absolute origin0,0, X=boardX, Y=-boardY in mm; envelope X18..77,Y-121..-20mm. Native top angles remain unchanged. Have the supplier return a BOM/CPL import preview; mapped column names do not establish rotation/origin correctness.

120 fitted top parts;19 bare PCB entries; R67 and R99 DNP and no paste. R97 FIT selects PWM; never fit both R97/R99. B.Paste intentionally empty. All473 native pad records include documentation/paste-only/mechanical objects; IPC356 contains456 emitted conductive pad records and384 via records. Separate PTH/NPTH drills contain four plated USB shell slots and nine NPTH holes.

Approve nominal0.20mm drills84 locations on1.6mm, finished dimensions/thickness/registration/copper plating and actual aspect limits.384 vias all have nominal ring >=0.15mm. All378 ordinary vias retain >=0.10mm clearance to SMD lands. The five U3 and one R28 exact process CSV sites require resin fill and copper cap, with agreed finish/flatness/voiding. Do not substitute tenting for fill/cap under paste.

Agree common U1/U3 stencil/reflow, U1 EP grid, solder-mask webs, dense pad/body/courtyard spacing and source-specific footprint orientation. GCT USB4215-03-A has four plated slots, short nominal0.8mm stakes on1.6mm board and no locator holes; agree hybrid soldering and retention. Approve actual90-ohm USB stack with tolerance and importer handling of solder-mask opening polarity.

Current logic/panel rail nominal3.220352V uses R14=27.4k, R98=402R, R15=5.11k precision feedback and TPS389001DSER reset. R95=16.5k/R96=10k, C40=100nF, C41=1nF C0G. U11 TI DSE0006A has six leads and no exposed pad; asymmetric SMD/NSMD mask/paste must be preserved. SD CMD/DAT0..3 use10k external pullups; DAT1/2 are bias-only. GPIO39 detection is separate. No dock or mainboard battery PCM is present. Require approved protected pack and separate bonded NTC.

Pin5 VDHR=VSH2 is supplier-confirmed; all24 J3 contacts and signal lands/paste pass the source-bound comparison. Remaining FPC/process holds include guaranteed0.27..0.33mm contact-end thickness or written Hirose acceptance, tongue/finger/coverlay registration, folded pin1/case pose and GDEM/GDEY CAD identity. J3 hold-down copper and paste are corrected to OEM0.40x0.80mm; qualify the actual common stencil/reflow process. Hirose peak<=250C, time above230C<=60s, recommended0.10mm stencil; do not close an empty actuator. See FPC_CONNECTOR_REVIEW_R144.md. Joint rail PFM/overshoot/load/lifetime, ceramic Ceff/HV/current/thermal, battery/NTC, firmware and actual FCT remain open. Read PRE_REVIEW_CHECKS_R144 and FCT_PLAN_R144. Generated files and computational passes do not release manufacture, purchasing or assembly.


R144 preserves the R143 J3 OEM correction. Initial and declared extra +/-0.1% solder-shift static reserves pass. Dynamic startup/ripple/load/OFF behavior and lifetime drift remain HOLD. TI U11 stencil example0.125mm and Hirose0.10mm guidance need an agreed common process. Review inputs only, NO FAB.
