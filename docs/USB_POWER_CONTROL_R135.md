# R135 charger/current control contract

R134 GPIO and USB architecture is retained. GPIO16/modulepad9→R86(1k)→EN1/U3pin6; GPIO2/pad38→R87(1k)→EN2/pin5; GPIO38/pad31→R88(1k)→CE/pin4. EN2pin5/VSSpin8 are correct in library/cache. R84/R85=2.2k pull-downs; R10=100k CE pull-down. Loaded GPIO margins, ROM/reset/brownout/hold and USB policy still require qualification.

EN2/EN1 order:00 USB10090/95/100mA;01 USB500450/475/500mA;10 R8ILIM max493.45mA model;11 suspend. These are input limits including reader load. CE high disables charging without disconnecting OUT. SW1 removes reader load; charger remains connected. Reset/OFF high-Z modelsUSB100/CE-low; fastOFF500mA and automatic BC1.2/PD are not implemented. Select higher modes only within the connected source's authorized budget; review non-simultaneous GPIO transitions and actual suspend/disconnect behavior.

PGOOD=CHG_STAT1, CHG=CHG_STAT2,10k pull-ups on3V3_SYS. GPIO levels are invalid whileOFF. CHG alone is not a charging-current/SOC proof. No automatic CE restart to bypass timer faults.

R80/R81=40.2k/33.2k1%, Semitec103JT-050 and100k R82 retained. Healthy nominal window4.90–35.01°C; bounded R81-open-at45°C model inhibits. Guaranteed full R/T/leakage and attachment/detachment/R82 faults remain open. Nominal445mA ISET and8.725h timer are unchanged and do not prove a full loaded2000–2500mAh cycle. [Fault/design evidence](SWITCH_NTC_R135.md).

USB4215-03-A, long data pair/reference and ESP GPIO19/20 remain source-checked. Full stackup/impedance, short-stake soldering/case fit and firmware/bench qualification remain HOLD. [Unchanged detailed R134 GPIO calculations](USB_POWER_CONTROL_R134.md) are conditional; its old TS-bias paragraphs are superseded here. No manufacturing/purchasing permission.
