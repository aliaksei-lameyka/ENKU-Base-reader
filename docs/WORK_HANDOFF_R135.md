# R135 native source checkpoint — NO FAB

Branch `engineering/r135-switch-ntc-review`, parent verified R134 d8677378bef58f3e76ef6b6839883fb09286cd18. Canonical source has actual full-severity KiCad10.0.7 DRC0/unconnected0/schematic-parity0/ERC0. No rules/severities/exclusions were reduced. Complete independent audits, assembly plots and fresh server proof are pending and are not claimed here.

Four TL3340 switches are replaced by actual E-Switch TL1016AAF160QG AA no-boss/no-ground-terminal variant, primary P520001 RevA28Apr2022 (PDF SHA2569f1097ea8591bbf730ee905ba186e0c6c0d48cfc573395d0ab7f9704a20e5a75). All four distinct numbered SMD pads are externally connected:1/2 button signal,3/4 GND, no virtual jumpers. Same Y73/85mm button locations; X moved inward0.05mm per side to preserve the nominal actuation-tip plane19.45/75.55mm. Body is lower; round/rectangular actuator and vertical axis differ, so the internal case pusher requires validation within the unchanged external thickness. No mechanical drop-in is claimed.

R80=40.2k1%,R81=33.2k1%, unchanged10k Semitec sensor and100k series R82. Nominal interpolation gives4.90–35.01°C window; bounded R81-open at45°C now inhibits with modeled350.9nA leakage budget. Actual guaranteed RT/TS leakage, attachment/detachment and bench qualification remain open. GPIO/current mode, charger/ISET/timer, PH2/NTC architecture, thin2000–2500mAh battery requirement, board59×101×1.6mm and case-thickness ceiling are preserved.

Finite source changes and native repair plans are retained in checks/applied_*_R135.json. Earlier source and proof remain intact on R134. No production, orders or outbound supplier messages.
