# Imported into the standalone ENKU Base Reader repository; Base-only checks remain authoritative.
#!/usr/bin/env python3
"""ENKU R0.1 KiCad schematic structural gate.

This is deliberately dependency-free. It does not replace KiCad ERC; it catches
repository-level damage before ERC is run: malformed S-expressions, missing
hierarchical sheets, missing critical references/nets, and accidental return of
old block placeholders.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
FILES = {
    "root": ROOT / "enku-mainboard-r0.1.kicad_sch",
    "power": ROOT / "power.kicad_sch",
    "mcu": ROOT / "mcu_io.kicad_sch",
    "epd": ROOT / "epd_hv.kicad_sch",
    "connectors": ROOT / "connectors.kicad_sch",
}

REQUIRED_REFS = {
    "power": [
        "U2", "U3", "U4", "J1", "SW1",
        "R8", "R9", "L1", "R14", "R15", "R16", "TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "TP7", "TP8",
    ],
    "mcu": [
        "U1", "J2", "U5", "SW2",
        "SW3", "SW4", "SW5", "SW6",
        "R26", "R27",
    ],
    "epd": [
        "J3", "L2", "Q1", "R37",
        "D1", "D2", "D3",
        "C22", "C23", "C24", "C25",
        "C26", "C27", "C28",
        "C29", "C30", "R38", "C31", "TP9", "TP10", "TP11", "TP12", "TP13", "TP14",
    ],
    "connectors": [
        "J5", "U8", "R62", "R63",
        "J6", "J7",
    ],
}

REQUIRED_NETS = {
    "power": [
        "VBUS_USB", "VBUS_DOCK", "VBUS_EXT", "VBAT", "VSYS",
        "3V3_SYS", "SYS_EN", "BAT_TS", "CHG_STAT1",
    ],
    "mcu": [
        "3V3_SYS", "USB_DM", "USB_DP", "SPI_MOSI", "SPI_MISO", "SPI_SCLK",
        "SD_CS", "EPD_CS", "EPD_DC", "EPD_RST", "EPD_BUSY",
        "I2C_SDA", "I2C_SCL", "IMU_INT1",
        "BAT_ADC", "DOCK_DETECT",
    ],
    "epd": [
        "EPD_GDR", "EPD_RESE", "EPD_SW", "EPD_CP_NEG",
        "EPD_VGH", "EPD_VGL", "EPD_VSH1", "EPD_VSH2",
        "EPD_VSL", "EPD_VCOM", "EPD_VDD", "EPD_VCI",
    ],
    "connectors": [
        "VBUS_USB", "USB_DP", "USB_DM", "VBUS_DOCK",
        "DOCK_DETECT", "UART_TX", "UART_RX", "BOOT", "ESP_EN",
    ],
}

BANNED_BLOCK_NAMES = [
    "TPS2121_BLOCK",
    "BQ25185_BLOCK",
    "TPS63031_BLOCK",
    "EPD_HV_NETWORK",
    "TPS923610_BLOCK",
    "FL_REMAP",
]

EXPECTED_CHILDREN = [
    "power.kicad_sch",
    "mcu_io.kicad_sch",
    "epd_hv.kicad_sch",
    "connectors.kicad_sch",
]


def balanced_sexpr(text: str) -> tuple[bool, str]:
    depth = 0
    in_string = False
    escaped = False
    for idx, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False, f"unexpected ')' at byte {idx}"
    if in_string:
        return False, "unterminated quoted string"
    if depth != 0:
        return False, f"parenthesis depth ends at {depth}"
    return True, "ok"


def contains_reference(text: str, ref: str) -> bool:
    return f'(property "Reference" "{ref}"' in text


def contains_net(text: str, net: str) -> bool:
    return f'(global_label "{net}"' in text or f'(label "{net}"' in text


def fail(errors: list[str], message: str) -> None:
    errors.append(message)
    print(f"ERROR: {message}")


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}

    for key, path in FILES.items():
        if not path.is_file():
            fail(errors, f"missing schematic: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[key] = text
        ok, reason = balanced_sexpr(text)
        if not ok:
            fail(errors, f"{path.name}: malformed S-expression: {reason}")
        if "(kicad_sch" not in text:
            fail(errors, f"{path.name}: missing kicad_sch header")
        if "(sheet_instances" not in text:
            fail(errors, f"{path.name}: missing sheet_instances")

    root = texts.get("root", "")
    for child in EXPECTED_CHILDREN:
        if f'(property "Sheetfile" "{child}"' not in root:
            fail(errors, f"root: missing child sheet {child}")

    for key, refs in REQUIRED_REFS.items():
        text = texts.get(key, "")
        for ref in refs:
            if not contains_reference(text, ref):
                fail(errors, f"{FILES[key].name}: missing critical reference {ref}")

    for key, nets in REQUIRED_NETS.items():
        text = texts.get(key, "")
        for net in nets:
            if not contains_net(text, net):
                fail(errors, f"{FILES[key].name}: missing critical net {net}")

    # KiCad hierarchical instance paths must end in the placed symbol UUID.
    # A sheet UUID here makes ERC deceptively clean while native netlist export
    # reports annotation errors and yields an unusable schematic source-of-truth.
    for key in ("power", "mcu", "epd", "connectors"):
        text = texts.get(key, "")
        pattern = re.compile(
            r'\(symbol \(lib_id[\s\S]*?\(uuid "([^"]+)"\)[\s\S]*?'
            r'\(instances\s+\(project "enku-mainboard-r0\.1"\s+'
            r'\(path "([^"]+)" \(reference "([^"]+)"\)'
        )
        for symbol_uuid, instance_path, ref in pattern.findall(text):
            if instance_path.rsplit("/", 1)[-1] != symbol_uuid:
                fail(errors, f"{FILES[key].name}: {ref} instance path does not end in symbol UUID")

    all_text = "\n".join(texts.values())
    for old in BANNED_BLOCK_NAMES:
        if old in all_text:
            fail(errors, f"obsolete block placeholder returned: {old}")


    epd = texts.get("epd", "")
    if epd.count('property "Value" "MBR0530"') < 3:
        fail(errors, "EPD HV must contain three MBR0530 rectifiers")
    if 'property "Value" "2.2R 1% 0805"' not in epd:
        fail(errors, "EPD HV missing frozen 2.2R RESE current-sense value")
    if "10uH TYS5040100M-10" not in epd:
        fail(errors, "EPD HV must use current 3.97-inch 10uH inductor baseline")
    if 'property "Value" "1M 1%"' not in epd:
        fail(errors, "EPD HV missing 1M GDR pulldown")
    if 'property "Reference" "C31"' not in epd:
        fail(errors, "EPD HV missing local booster input capacitor")

    power = texts.get("power", "")
    if 'property "Value" "18k 1%"' not in power:
        fail(errors, "power sheet missing 18k BQ25185 ILIM/VSET baseline")
    if 'property "Value" "1k 1%"' not in power:
        fail(errors, "power sheet missing 1k BQ25185 ISET baseline")
    if "TPS63802DLAR" not in power:
        fail(errors, "power sheet must use TPS63802DLAR first-spin 3V3 regulator")
    if "TPS63031DSKR" in power or 'lib_id "ENKU:TPS63031' in power or 'symbol "ENKU:TPS63031' in power:
        fail(errors, "obsolete TPS63031 remains in active power schematic")
    if "DFE201612E-R47M=P2" not in power:
        fail(errors, "power sheet missing 0.47uH DFE201612E TPS63802 inductor")
    if 'property "Value" "511k 1%"' not in power or 'property "Value" "91k 1%"' not in power:
        fail(errors, "TPS63802 3.3V feedback divider must be 511k/91k")
    if power.count('property "Value" "22uF 10V"') < 2:
        fail(errors, "TPS63802 output needs both 22uF baseline capacitors")

    mcu = texts.get("mcu", "")
    # The dedicated Base schematic MUST NOT contain Hall as a DNP or populated circuit.
    if '(symbol (lib_id "ENKU:DRV5032FB")' in mcu or '(property "Reference" "U6"' in mcu:
        fail(errors, "BASE must not contain U6 Hall sensor, even as DNP")
    if '(property "Reference" "C20"' in mcu:
        fail(errors, "BASE must not retain U6-only C20 decoupling")
    if 'HALL_INT' in mcu:
        fail(errors, "BASE MCU sheet still exposes Pro-only HALL_INT")
    if '(global_label "USB_VBUS_VALID" (shape input) (at 60.96 81.28' not in mcu:
        fail(errors, "BASE GPIO17 must be USB_VBUS_VALID, never Hall")
    if '(number "40"' not in mcu or '(number "41"' not in mcu:
        fail(errors, "MCU sheet must include ESP32-S3-WROOM-1 pins 40 and 41")
    if "Hirose DM3AT-SF-PEJM5" not in mcu:
        fail(errors, "MCU sheet missing exact Hirose microSD MPN")

    conn = texts.get("connectors", "")
    if "GCT USB4105-GF-A-120" not in conn:
        fail(errors, "connector sheet missing exact GCT USB-C MPN")

    exact_bindings = {
        "power": ("ENKU:TPS2121_RUX0012A", "ENKU:BQ25185_DLH0010A"),
        "mcu": ("ENKU:BMI270_Bosch_LGA14",),
        "epd": ("ENKU:FH34SRJ-24S-0.5SH",),
    }
    for sheet, tokens in exact_bindings.items():
        for token in tokens:
            if token not in texts.get(sheet, ""):
                fail(errors, f"{FILES[sheet].name}: exact local footprint binding missing: {token}")

    if '(number "S1"' not in epd or '(number "S2"' not in epd:
        fail(errors, "EPD connector symbol must include grounded S1/S2 retention tabs")

    if errors:
        print(f"\nENKU schematic structural gate: FAIL ({len(errors)} issue(s))")
        return 1

    print("ENKU schematic structural gate: PASS")
    for key, path in FILES.items():
        print(f"  {key:10s} {path.name:36s} {path.stat().st_size:7d} bytes")
    print("  Base-only scope: Pro frontlight/Qi sheets are deferred")
    print("  obsolete block placeholders: 0")
    print("\nNOTE: this structural gate does not replace KiCad ERC/DRC.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
