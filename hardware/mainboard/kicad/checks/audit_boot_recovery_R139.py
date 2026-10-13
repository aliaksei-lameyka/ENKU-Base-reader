"""Source-only recovery review of the frozen R138 board; no hardware test claim."""
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PCB_SHA = "90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971"
ARTIFACT_SHA = "cb5c338dc288ed883bae2288700ec2108902754f391bf198a8afcc8f12f86f2b"


def main():
    pcb = ROOT / "hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pcb"
    archive = ROOT / "docs/evidence/R138/main/native_server_R138.zip"
    assert hashlib.sha256(pcb.read_bytes()).hexdigest() == PCB_SHA
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == ARTIFACT_SHA
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        g = json.loads(z.read("geometry.json"))
        af = json.loads(z.read("assembly_features.json"))
        xml = ET.fromstring(z.read("netlist.xml"))
    comps = {c.get("ref"): c for c in xml.find("components")}
    pins = {(node.get("ref"), node.get("pin")): net.get("name")
            for net in xml.find("nets") for node in net}
    pads = {(p["ref"], p["number"]): p for p in g["pads"]}
    partitions = {uuid: i for i, group in enumerate(g["components"]) for uuid in group}
    af_parts = {p["ref"]: p for p in af["footprints"]}

    def connected(net, *points):
        groups = set()
        for point in points:
            assert pins[point] == net, (point, pins.get(point), net)
            assert pads[point]["net"] == net, (point, "physical pad net")
            groups.add(partitions[pads[point]["uuid"]])
        assert len(groups) == 1, (net, "physical connected partition")

    def value(ref, text):
        assert comps[ref].findtext("value") == text

    value("U1", "ESP32-S3-WROOM-1-N16R8")
    value("R17", "10k")
    value("R18", "10k")
    value("C15", "1uF")
    connected("3V3_SYS", ("J7", "1"), ("U1", "2"), ("R17", "1"), ("R18", "1"))
    connected("GND", ("J7", "2"), ("U1", "1"), ("C15", "2"), ("SW2", "2"))
    connected("UART_TX", ("J7", "3"), ("U1", "37"))
    connected("UART_RX", ("J7", "4"), ("U1", "36"))
    connected("BOOT", ("J7", "5"), ("U1", "27"), ("R18", "2"), ("SW2", "1"))
    connected("ESP_EN", ("J7", "6"), ("U1", "3"), ("R17", "2"), ("C15", "1"))
    connected("USB_DM", ("U1", "13"), ("R65", "2"))
    connected("USB_DP", ("U1", "14"), ("R64", "2"))
    for pin in ["15", "16", "26", "28", "29", "30"]:
        assert pins[("U1", pin)].startswith("unconnected-")
        assert pads[("U1", pin)]["net"] == pins[("U1", pin)]
    assert af_parts["SW2"]["fields"]["MPN"] == "TL3342F160QG"
    assert af_parts["J7"]["fields"]["Assembly"] == "BARE_PCB"
    for ref in ["R64", "R65"]:
        assert af_parts[ref]["fields"]["MPN"] == "RC0603JR-070RL"
        assert af_parts[ref]["fields"]["Assembly"] == "FIT"
    result = {
        "audit_revision": "R139", "physical_board_revision": "R138",
        "pcb_sha256": PCB_SHA, "main_artifact_sha256": ARTIFACT_SHA,
        "source_connectivity_checks": "PASS", "native_geometry_version": g["version"],
        "module": "ESP32-S3-WROOM-1-N16R8",
        "firmware_target_to_verify_on_samples": {"flash_MB": 16, "flash_bus": "Quad SPI", "PSRAM_MB": 8, "PSRAM_bus": "Octal SPI"},
        "J7_target_pinmap": {
            "1": "3V3_SYS target voltage reference; do not power automatically from fixture",
            "2": "GND", "3": "UART_TX / GPIO43 (fixture RX)",
            "4": "UART_RX / GPIO44 (fixture TX)", "5": "BOOT / GPIO0", "6": "ESP_EN"
        },
        "reset_RC": {"R17": "10k", "C15": "1uF", "dynamic_timing_qualified": False},
        "GPIO46_GPIO45_GPIO3_and_reserved_GPIO35_36_37_externally_unconnected": True,
        "USB_DM_GPIO19_DP_GPIO20": True,
        "fitted_USB_series_resistors_ohm": 0,
        "factory_firmware_bound_to_this_PCB": "NOT PROVIDED / NOT VALIDATED",
        "USB_MSC_requires_separate_OTG_firmware_and_exclusive_SD_ownership": True,
        "physical_ROM_programming_recovery_flash_PSRAM_USB_and_load_tests": "NOT RUN",
        "slow_ramp_and_frequent_power_cycle_monitor_review": "HOLD",
        "fabrication_ready": False, "consumer_release_ready": False,
        "primary_sources": [
            "https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html",
            "https://docs.espressif.com/projects/esptool/en/latest/esp32s3/advanced-topics/boot-mode-selection.html",
            "https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf",
            "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/usb-serial-jtag-console.html"
        ]
    }
    out = ROOT / "docs/qualification/R139/boot_recovery_source_audit_R139.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: frozen R138 source/netlist/native physical recovery paths; physical tests NOT RUN")


if __name__ == "__main__":
    main()
