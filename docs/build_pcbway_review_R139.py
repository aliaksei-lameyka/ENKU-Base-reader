"""Build a traceable R138 engineering-review packet. Never authorizes manufacture.

Requires Python fitz/PyMuPDF, reportlab and pypdf and pinned native KiCad 10.0.7.
Derived PDFs are review views; original main-run manufacturing bytes control.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

import fitz
import reportlab
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "81b34a97c765c0fdb5ded5e4c1d4ed22d06756cb"
PCB_SHA = "90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971"
ARTIFACT_SHA = "cb5c338dc288ed883bae2288700ec2108902754f391bf198a8afcc8f12f86f2b"
KICAD = ROOT / "hardware/mainboard/kicad"
LAYER_NAMES = ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu", "F.Mask", "B.Mask", "F.Paste", "B.Paste", "F.SilkS", "B.SilkS", "Edge.Cuts"]
FONT_DIR = Path(reportlab.__file__).resolve().parent / "fonts"
pdfmetrics.registerFont(TTFont("ENKUSans", str(FONT_DIR / "Vera.ttf")))
pdfmetrics.registerFont(TTFont("ENKUSansBold", str(FONT_DIR / "VeraBd.ttf")))

TESTS = [
    ("Q01", "EVT + each unit", "Inspection", "Check MPN, polarity, R67 DNP, solder/EP/USB joints and six fill/cap sites.", "Approved BOM and agreed assembly criteria; no unrecorded hardware rework.", "AOI/X-ray/joint photos, serial and lots"),
    ("Q02", "EVT + each unit", "Safe power", "Current-limited staged startup; monitor VBAT/VSYS/3V3/EN and supply current.", "All component limits met; proposed normal 3V3 target 3.10..3.50V; numeric current limits HOLD.", "Scope traces and measured currents"),
    ("Q03", "EVT / design validation", "Startup corners", "Blank flash, low pack, PCM-open, no battery; USB100 initial mode; slow ramps/rapid cycles.", "Repeatable boot or defined safe charge-only state; no reset loop or unauthorized source current.", "Rail/EN/BOOT traces and reset logs"),
    ("Q04", "EVT + each unit", "ROM / flashing", "Native USB both plug orientations and J7 UART; write approved images then verify.", "Correct chip/flash identity, approved offsets/hashes and normal boot; images not supplied yet.", "Tool logs, image hashes, MAC"),
    ("Q05", "EVT / design validation", "Recovery", "Use a recoverable invalid app / disabled USB on controlled sample; BOOT/EN/UART recovery.", "Restore approved image without soldering; do not burn eFuses or erase identity.", "Before/after flash and ROM logs"),
    ("Q06", "EVT + each unit", "Memory", "Read 16MB flash identity and test allocated 8MB Octal PSRAM patterns.", "Expected configuration and zero mismatches in approved test regions.", "Memory size and pattern logs"),
    ("Q07", "EVT + each unit", "USB", "C-C/A-C, both orientations, enumeration, hot-plug, suspend/resume and source policy.", "Stable communications, approved inrush/suspend/current limits; those limits require release.", "Host logs and input-current captures"),
    ("Q08", "EVT + each unit", "microSD", "Detect/write/read/checksum/remove/reinsert approved cards; qualify supported card range.", "Exact checksums, valid remount and safe error reporting.", "Card IDs, checksums, error logs"),
    ("Q09", "EVT / design validation", "USB MSC", "Exclusive host/reader SD ownership, interrupted writes, disconnect and reader remount.", "No simultaneous writers; recover without corrupting unrelated files; final FW required.", "Host/reader ownership and filesystem logs"),
    ("Q10", "EVT + each unit", "Display / HV", "Use exact approved panel/FPC, full patterns and refresh; scope all EPD rails and R37 stress.", "Correct display, approved panel voltage/timing/pulse limits; exact panel remains HOLD.", "Panel ID, photos, HV/pulse captures"),
    ("Q11", "EVT + each unit", "Controls / IMU", "Exercise every button/switch and BMI270 identity/orientation/interrupt; check ADC readings.", "All inputs register correctly; ADC calibration and IMU limits frozen before FCT.", "Input/IMU/ADC logs"),
    ("Q12", "EVT + each unit", "Load stability", "Wi-Fi TX + SD writes + EPD refresh; permitted 50mA..1A characterization steps.", "No brownout/reset/data error; rails/temperatures within approved limits. Source budget respected.", "Scope, reset, checksum and thermal logs"),
    ("Q13", "EVT / design validation", "Charging", "Final pack CC/CV, low-cell/precharge, termination, recharge and system-load sharing in actual case.", "Pack voltage/current/temperature limits met and charge completes; respect dynamic safety timers.", "Full cycle V/I/T curves and status logs"),
    ("Q14", "EVT / design validation", "NTC / faults", "Simulator first: sensor open/short/detached, R80/R81/R82 faults; then approved attachment tests.", "Document safe response and mitigation; floating TS and detached sensor remain unresolved.", "Fault matrix, TS/current traces and retention evidence"),
    ("Q15", "EVT + each unit", "NTC stimulus", "Fixture applies approved normal/cold/hot/open/short sensor values.", "Approved allow/inhibit behavior; values/tolerances and fixture require release.", "Stimulus values, TS/current/status logs"),
    ("Q16", "EVT + each unit", "Power states", "Hard OFF, sleep/wake, USB connected/disconnected; verify no fixture back-power.", "Reader load off as designed; numeric leakage/sleep/active budgets remain HOLD.", "State currents and wake/reset logs"),
    ("Q17", "EVT / design validation", "Mechanical / packs", "Final case, two thin PCM pack models, J1 polarity, NTC retention, USB/SD/button/FPC clearances.", "No case thickening, pouch compression or RF-metal intrusion; repeatable safe replacement.", "Approved CAD, measured envelopes and fit photos"),
    ("Q18", "EVT + each unit", "RF", "Wi-Fi/BLE communications; characterize in final enclosure and final battery arrangement.", "Agreed reference-fixture link performance; limits to be set from characterized golden unit.", "Link/RSSI/throughput logs"),
    ("Q19", "Design validation", "Endurance / EMC", "Proposed 24-72h combined workload, repeated power/USB cycles; lab ESD/EMC pre-compliance.", "No unexplained failures; counts/environment/levels and product criteria must be approved.", "Long-run logs, fault causes and lab reports"),
    ("Q20", "Each released unit", "Final image / log", "After diagnostics, install approved user firmware, verify and boot; bind identity and all FCT results.", "All required rows PASS with traceable raw evidence; missing image/fixture/limits means HOLD.", "Signed unit record and firmware SHA256")
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def write_csv(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(headers); w.writerows(rows)


def ref_key(ref):
    m = re.match(r"(\D+)(\d+)$", ref)
    return (m.group(1), int(m.group(2))) if m else (ref, 0)


def paragraph(text, kind="body"):
    styles = {
        "body": ParagraphStyle("body", fontName="ENKUSans", fontSize=9.5, leading=13, spaceAfter=7),
        "title": ParagraphStyle("title", fontName="ENKUSansBold", fontSize=21, leading=25, spaceAfter=16, textColor=colors.HexColor("#122c40")),
        "h": ParagraphStyle("h", fontName="ENKUSansBold", fontSize=13, leading=17, spaceBefore=9, spaceAfter=8, textColor=colors.HexColor("#122c40")),
        "small": ParagraphStyle("small", fontName="ENKUSans", fontSize=7.5, leading=10),
    }
    return Paragraph(escape(str(text)).replace("\n", "<br/>"), styles[kind])


def table(headers, rows, widths, small=True):
    data = [[paragraph(x, "small") for x in headers]] + [[paragraph(x, "small" if small else "body") for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6edf2")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fa")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#becad2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
    ]))
    return t


def page_footer(c, doc):
    c.saveState(); c.setFont("ENKUSans", 8); c.setFillColor(colors.HexColor("#495c6a"))
    c.drawString(44, 25, "ENKU Base Reader | physical R138 | engineering review only - NO FAB")
    c.drawRightString(A4[0] - 44, 25, str(doc.page)); c.restoreState()


def authored_pdf(path, story):
    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=44, rightMargin=44,
                      topMargin=42, bottomMargin=42, title="ENKU R138 engineering review",
                      author="ENKU project").build(story, onFirstPage=page_footer, onLaterPages=page_footer)


def content_rect(page):
    rects = []
    for d in page.get_drawings():
        if d["color"] is not None or (d["fill"] is not None and d["fill"] != (1.0, 1.0, 1.0)):
            rects.append(d["rect"])
    rects += [fitz.Rect(b[:4]) for b in page.get_text("blocks") if str(b[4]).strip()]
    if not rects:
        return None
    result = fitz.Rect(rects[0])
    for r in rects[1:]: result |= r
    return fitz.Rect(result.x0 - 5, result.y0 - 5, result.x1 + 5, result.y1 + 5) & page.rect


def frame_native(core_path, output_path, labels, same_frame=False):
    src = fitz.open(core_path); out = fitz.open()
    assert len(src) == len(labels)
    clips = [content_rect(p) for p in src]
    if same_frame:
        full = None
        for r in clips:
            if r is not None: full = fitz.Rect(r) if full is None else full | r
        clips = [full] * len(src)
    for i, label in enumerate(labels):
        p = out.new_page(width=A4[0], height=A4[1])
        p.insert_font(fontname="ENKU", fontfile=str(FONT_DIR / "Vera.ttf"))
        p.insert_text((36, 32), "ENKU Base Reader - physical R138", fontsize=14, fontname="ENKU")
        p.insert_text((36, 51), label, fontsize=10, fontname="ENKU")
        p.insert_text((36, 67), "KiCad 10.0.7 native view / auto-fit / NOT TO SCALE / NO FAB", fontsize=8, fontname="ENKU")
        if clips[i] is not None:
            p.show_pdf_page(fitz.Rect(36, 88, A4[0] - 36, A4[1] - 75), src, i, clip=clips[i])
        else:
            p.insert_text((70, 180), "Empty plotted layer; original Gerber controls.", fontsize=11, fontname="ENKU")
        p.insert_text((36, A4[1] - 54), "PCB SHA256: " + PCB_SHA, fontsize=7, fontname="ENKU")
        p.insert_text((36, A4[1] - 40), "Common front-view orientation; no mirroring. Original manufacturing files control.", fontsize=8, fontname="ENKU")
        if label == "B.Paste":
            p.insert_text((36, A4[1] - 26), "Native PDF hole glyphs are reference marks; verified B.Paste Gerber has no apertures.", fontsize=7, fontname="ENKU")
        else:
            p.insert_text((36, A4[1] - 26), f"Native plot page {i+1} / {len(src)}", fontsize=8, fontname="ENKU")
    out.save(output_path, deflate=True)


def review_pdf(out, boot):
    s = [paragraph("ENKU Base Reader\nPCBWay engineering review", "title"),
         paragraph("Physical board R138 / audit and test preparation R139", "h"),
         paragraph("ENGINEERING REVIEW ONLY - NO FAB. This packet requests a process/assembly/test review. It does not approve manufacturing, procurement or shipment to users."),
         table(["Item", "Evidence / status"], [
             ["Source", SOURCE], ["PCB SHA256", PCB_SHA],
             ["Actual main CI", "Run 38311804626; KiCad 10.0.7; zero DRC/ERC/opens/parity; 27 scopes, 20 effective rejection cases."],
             ["Manufacturing exports", "11 Gerbers, 2 drill files, IPC-D-356, 107 fitted BOM/CPL placements; exact accepted artifact bytes."],
             ["Recovery source audit", "PASS: UART/BOOT/EN/USB/strap paths checked in schematic and native physical geometry."],
             ["Physical product tests", "NOT RUN. No qualified real-pack/case/panel/firmware/fixture result is implied."]
         ], [114, 393]), Spacer(1, 12),
         paragraph("Release gates", "h"),
         paragraph("A: close design inputs and agree factory process. B: approved EVT samples and measured characterization. C: final-design validation with a golden unit, including endurance/ESD/EMC pre-compliance. D: approved images/fixture/limits and 100% functional testing of released units."),
         paragraph("Complete editable KiCad sources and local libraries are included. Filenames retain r0.1; this packet's R138 identity and PCB hash control. Historical trial layouts and private supplier correspondence are excluded."), PageBreak(),
         paragraph("Unclosed design and product risks", "title")]
    risks = [
        ("Startup / reset", "Initial high-Z source mode is USB100. Blank firmware, absent/low battery, PCM-open, slow ramps and rapid cycles need validation. The 10k/1uF EN RC follows reference values but is not a dynamic guarantee."),
        ("Charging completion", "445mA nominal, scenario 394.55..492.42mA; modeled BAT max 4.24V. Fast timer min/nominal 6.71825/8.725h. Full 2500mAh CC/CV/termination in the final case is unproved. TI dynamically slows timers in DPPM/VIN-DPM/thermal regulation; do not infer failure from wall time or bypass timers."),
        ("NTC fault response", "Nominal modeled window about 4.90..35.01C. R82-open leaves TS floating; detached sensor on a hot pouch can still allow charge. Guaranteed leakage/corners, safe fault behavior and attachment/strain relief are HOLD."),
        ("Capacitance / load", "Typical capacitor scenarios are not guaranteed minima. Validate bias/age/temp/lot effective capacitance, inrush, converter stability, EPD rails and R37 pulses under combined Wi-Fi/SD/EPD load."),
        ("Final mechanical parts", "Exact panel/FPC, complete current case CAD and two interchangeable thin 2000-2500mAh protected packs with China/Poland sourcing remain unqualified. Case thickness must not increase; 5.2mm AKY0156 is rejected."),
        ("Factory test release", "No validated diagnostic/release image set, flash offsets, fixture or final numeric acceptance budgets are supplied. The templates are NOT RUN, not an executable production procedure.")
    ]
    for h, text in risks: s += [paragraph(h, "h"), paragraph(text)]
    s += [PageBreak(), paragraph("Manufacturing response required", "title"),
          table(["Requirement", "Confirm before an EVT release"], [
              ["4-layer stack / USB", "59x101x1.6mm with side cutout. L1 F / L2 In1 / L3 In2 / L4 B. Submit material/dielectrics/finished copper/thickness/finish; validate B-side pair over In2 at 90-ohm differential."],
              ["91 small via bores", "0.50/0.20mm land/bore at nominal aspect 8. Agree finished drill, registration, thickness and barrel process; +10% board thickness would give 8.8."],
              ["6 resin-filled/capped", "Five U3 EP vias and one R28 pin-1 via. Front untented/back tented; exact process CSVs control. Ordinary tenting is not equivalent."],
              ["U1 EP grid", "Nine lands/windows and 12 intrinsic 0.30mm EP PTH holes, both-side tenting request. Separate from routed via counts. Agree solder-wicking/stencil/reflow and joint inspection."],
              ["J4 USB4215-03-A", "Four plated slots, 0.8mm short stakes on 1.6mm PCB, no locator holes. Agree paste-in-hole/reflow or controlled solder process and mechanical joints."],
              ["Assembly definition", "107 top fitted parts / R67 DNP / 19 BARE_PCB features. Approve alternates, stencil and polarity/orientation against manufacturer drawings. No silent substitutions."],
              ["Off-board items", "J1: PH-2 pin 1 VBAT, pin 2 GND. J8: bare hand-solder NTC pads. Pack, sensor retention, display, FPC and case are separate HOLD inputs."]
          ], [116, 391]), Spacer(1, 12),
          paragraph("Coordinates and inspection", "h"),
          paragraph("All manufacturing files share absolute 0,0 in mm: X=board X, Y=-board Y. CPL keeps native KiCad angles and top side. Verify component library zero-angle/pin-1 before placement. PDFs are auto-fit reference views, not scaled fabrication drawings. Request electrical net test, AOI and appropriate EP/USB joint inspection with agreed criteria."),
          PageBreak(), paragraph("Programming and recovery", "title"),
          paragraph("ESP32-S3-WROOM-1-N16R8: target 16MB Quad SPI flash and 8MB Octal PSRAM. Freeze tools, sdkconfig, partitions and image hashes after validation; no flash offsets or firmware binary are invented here."),
          table(["J7 pin", "Target signal / fixture"], [[k, v] for k, v in boot["J7_target_pinmap"].items()], [60, 447]), Spacer(1, 14),
          paragraph("Validate the fixture before use", "h"),
          paragraph("J7 is bare TC2030-compatible geometry with ENKU's own pin assignment. Target VREF is a measurement/reference, not an automatic power input. Use 3.3V-compatible UART and VREF-aware drive. Remove drive when target power is off; power through an agreed VBUS/battery-simulator path."),
          paragraph("Hold BOOT low before reset; drive EN low long enough to discharge its RC and meet 50us reset timing at the pin. Release EN only with stable rails; hold BOOT through the minimum 3ms strap sampling interval. Verify ROM identity, write the approved image set and verify it, then release BOOT and reset. Physical recovery is NOT RUN."),
          paragraph("USB ROM programming and J7 fallback must both work without soldering. Read security settings; do not burn eFuses during characterization. Test controlled invalid-app recovery. USB Serial/JTAG is fixed CDC/JTAG; MSC needs separate OTG firmware with exclusive SD ownership and safe write/unmount/remount behavior."),
          paragraph("Production release needs complete image files/offsets/SHA256, diagnostic commands, fixture drawing/software, calibrated instruments, numeric limits and a golden-unit record. After diagnostics, install and verify the user image and retain a per-unit PASS/FAIL log."), PageBreak()]
    for begin in range(0, len(TESTS), 5):
        end = begin + 5
        s += [paragraph(f"Physical qualification matrix {begin//5+1}/4", "title"),
              paragraph("All rows start NOT RUN. Characterization proposals and pending limits do not constitute production pass criteria."),
              table(["ID / scope", "Test / method", "Required result / evidence"], [
                  [t[0]+"\n"+t[1], t[2]+"\n"+t[3], t[4]+"\nEvidence: "+t[5]] for t in TESTS[begin:end]
              ], [81, 202, 224]), PageBreak()]
    s += [paragraph("Records, boundaries and sources", "title"),
          paragraph("Factory_Test_Log_NOT_RUN.csv binds each required result to unit serial/MAC, PCB/BOM/manufacturing lots, diagnostic/release hashes, fixture/software/calibration, numeric measurements and raw evidence. No empty log or unvalidated image can be marked PASS."),
          paragraph("AOI and bare-PCB electrical testing do not validate flashing, charging, data integrity or load stability. PCBWay asks the customer for steps, criteria, fixture and environment; functional testing and sponsorship scope require agreement."),
          paragraph("Fault tests start on current-limited simulators/dummy pouches. Actual packs are tested only within their approved limits. No intentional overheating of an unqualified live pouch. A hardware change or unrecorded bodge reopens qualification."),
          paragraph("Primary documentation checked 2026-10-13", "h")]
    sources = json.loads((ROOT / "docs/qualification/R139/boot_recovery_source_audit_R139.json").read_text())["primary_sources"] + [
        "https://www.ti.com/lit/ds/symlink/bq24072t.pdf",
        "https://www.ti.com/lit/ds/symlink/tps63802.pdf",
        "https://www.pcbway.com/pcb-assembly/pcb-assembly-testing.html"
    ]
    for url in sources: s += [paragraph(url, "small"), Spacer(1, 8)]
    authored_pdf(out, s)


def build(build_dir, app):
    build_dir.mkdir(parents=True, exist_ok=True)
    native = subprocess.check_output([str(app), "kicad-cli", "version"], text=True).strip()
    assert native == "10.0.7"
    assert sha((KICAD / "enku-mainboard-r0.1.kicad_pcb").read_bytes()) == PCB_SHA
    archive = ROOT / "docs/evidence/R138/main/native_server_R138.zip"
    assert sha(archive.read_bytes()) == ARTIFACT_SHA
    packet = build_dir / "ENKU_Reader_Base_R138_PCBWay_Engineering_Review_NO_FAB"
    assert not packet.exists(), "Use a fresh packet output directory; no partial/stale overwrites"
    packet.mkdir()
    manu = packet / "01_MANUFACTURING_REVIEW"
    assembly = packet / "02_ASSEMBLY_REFERENCE"
    pdfdir = packet / "03_PDF_REVIEW"
    testdir = packet / "04_QUALIFICATION_NOT_RUN"
    sources = packet / "05_EDITABLE_KICAD"
    proofdir = packet / "06_VERIFIED_SOURCE_EVIDENCE"
    for d in [manu, assembly, pdfdir, testdir, sources, proofdir]: d.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        original = json.loads(z.read("manufacturing_review_R138/manifest_R138.json"))
        for name, meta in original["files"].items():
            data = z.read("manufacturing_review_R138/" + name)
            assert sha(data) == meta["sha256"] and len(data) == meta["bytes"]
            target = manu / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        (manu / "manifest_R138.json").write_bytes(z.read("manufacturing_review_R138/manifest_R138.json"))
        g = json.loads(z.read("geometry.json")); af = json.loads(z.read("assembly_features.json"))
        netlist = ET.fromstring(z.read("netlist.xml"))
    assert len(original["files"]) == 24
    bom = list(csv.DictReader(io.StringIO((manu / "BOM_fitted_review.csv").read_text())))
    cpl = list(csv.DictReader(io.StringIO((manu / "CPL_native_mm.csv").read_text())))
    bom_refs = {r.strip() for row in bom for r in row["Designator"].split(",")}
    assert sum(int(row["Quantity"]) for row in bom) == 107 and len(bom_refs) == 107
    assert {row["Ref"] for row in cpl} == bom_refs and len(cpl) == 107
    assert "R67" not in bom_refs and all(row["Side"] == "top" for row in cpl)
    write_csv(assembly / "BOM_PCBWay_columns.csv", ["Designator", "Qty", "PartNumber", "Package", "Manufacturer", "Value", "Side"],
              [[r["Designator"], r["Quantity"], r["Manufacturer Part Number"], r["Footprint"], r["Manufacturer"], r["Value"], r["Side"]] for r in bom])
    write_csv(assembly / "CPL_PCBWay_columns_mm.csv", ["Designator", "Mid X", "Mid Y", "Layer", "Rotation", "Package", "Value"],
              [[r["Ref"], r["PosX"], r["PosY"], r["Side"], r["Rot"], r["Package"], r["Val"]] for r in cpl])
    afparts = {p["ref"]: p for p in af["footprints"]}; index = []
    for ref in sorted(g["footprints"], key=ref_key):
        fp = g["footprints"][ref]; meta = afparts[ref]
        status = "DNP" if meta["dnp"] else meta["fields"].get("Assembly", "")
        if not status: status = "FIT" if ref in bom_refs else "BARE_PCB"
        pads = [p for p in g["pads"] if p["ref"] == ref and p["number"]]
        preferred = [p for p in pads if p["number"] == "1"] or [p for p in pads if p["number"] == "A1"]
        first = preferred[0] if preferred else (sorted(pads, key=lambda p:p["number"])[0] if pads else None)
        x, y = fp["pos"]
        row = [ref, status, x, -y, fp["angle"], first["number"] if first else "",
               first["pos"][0] if first else "", -first["pos"][1] if first else "", meta["fields"].get("MPN", "")]
        index.append(row)
    assert len(index) == 127 and sum(r[1] == "BARE_PCB" for r in index) == 19
    write_csv(assembly / "ALL_REFERENCE_FIRST_PAD_INDEX_mm.csv", ["Ref", "Assembly", "Gerber X mm", "Gerber Y mm", "Native rotation deg", "Reference pad number", "Reference pad Gerber X mm", "Reference pad Gerber Y mm", "MPN"], index)
    write_csv(assembly / "CONNECTOR_PAD_NETMAP_mm.csv", ["Ref", "Pad", "Net", "Gerber X mm", "Gerber Y mm"],
              [[p["ref"], p["number"], p["net"], p["pos"][0], -p["pos"][1]] for p in g["pads"] if p["ref"].startswith("J") and p["number"]])
    write_csv(assembly / "MCU_PAD_GPIO_NETMAP.csv", ["Module", "Pad", "Pin function", "Net"],
              [["U1", node.get("pin"), node.get("pinfunction"), net.get("name")] for net in netlist.find("nets") for node in net if node.get("ref") == "U1"])
    write_csv(assembly / "OFFBOARD_ITEMS_PENDING.csv", ["Item", "Part / status", "Requirement", "Approved"], [
        ["Battery", "UNSELECTED / HOLD", "2000-2500mAh, 2-wire, PCM, approx 4mm, no case thickening; 2 qualified CN/PL interchangeable models", "False"],
        ["Battery cable", "UNRELEASED / HOLD", "PH-2 mating family; pin1 VBAT/pin2 GND, exact polarity/envelope/length/strain relief", "False"],
        ["External NTC", "Semitec 103JT-050 candidate", "Hand solder J8 bare pads; insulation, flat pouch retention, response/repairability and faults", "False"],
        ["Display / FPC", "UNRELEASED / HOLD", "Exact panel, FPC pinout, HV waveform and case fit", "False"],
        ["Case", "UNRELEASED / HOLD", "Current complete CAD, component/pack tolerances and unchanged thickness", "False"]
    ])
    for name in ["PRODUCT_QUALIFICATION_R139.md", "PCBWAY_MANUFACTURING_NOTES_R138.md", "FACTORY_FLASH_CONTRACT_R139.md"]:
        shutil.copy2(ROOT / "docs" / name, (testdir if "MANUFACTURING" not in name else manu) / name)
    boot = json.loads((ROOT / "docs/qualification/R139/boot_recovery_source_audit_R139.json").read_text())
    shutil.copy2(ROOT / "docs/qualification/R139/boot_recovery_source_audit_R139.json", proofdir)
    write_csv(testdir / "QUALIFICATION_MATRIX_NOT_RUN.csv", ["ID", "Stage", "Test", "Procedure", "Acceptance / hold", "Evidence", "Status"], [list(t)+["NOT RUN"] for t in TESTS])
    write_csv(testdir / "Factory_Test_Log_NOT_RUN.csv", ["Test_ID", "Test", "Stage", "Unit_serial", "MAC", "PCB_revision", "BOM_revision", "Manufacturing_lot", "Component_lots", "Diagnostic_FW_SHA256", "Release_FW_SHA256", "Fixture_revision", "Test_software_revision", "Instrument_calibration", "Ambient_C", "Cell_C", "Measurements", "Acceptance_revision", "Raw_evidence_path", "Operator", "UTC", "Status"],
              [[t[0], t[2], t[1]]+[""]*18+["NOT RUN"] for t in TESTS])
    write_json(testdir / "FACTORY_FLASH_MANIFEST_PENDING.json", {"status": "HOLD - NOT EXECUTABLE", "physical_PCB": "R138", "pcb_sha256": PCB_SHA, "target_module": boot["module"], "diagnostic_images": [], "release_images": [], "approved_offsets_and_SHA256": False, "pinned_build_and_flash_tools": None, "approved_fixture": None, "approved_numeric_limits": None, "production_test_release_approved": False})
    tracked = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", SOURCE], cwd=ROOT, text=True).splitlines()
    explicit = {"enku-mainboard-r0.1.kicad_pcb", "enku-mainboard-r0.1.kicad_pro", "enku-mainboard-r0.1.kicad_dru", "enku-mainboard-r0.1.kicad_sch", "power.kicad_sch", "mcu_io.kicad_sch", "epd_hv.kicad_sch", "connectors.kicad_sch", "ENKU.kicad_sym", "fp-lib-table", "sym-lib-table"}
    for path in tracked:
        prefix = "hardware/mainboard/kicad/"
        if not path.startswith(prefix): continue
        rel = path[len(prefix):]
        if rel in explicit or rel.startswith("ENKU.pretty/") or rel.startswith("standard-footprints/"):
            dest = sources / rel; dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(subprocess.check_output(["git", "show", SOURCE+":"+path], cwd=ROOT))
    assert sha((sources / "enku-mainboard-r0.1.kicad_pcb").read_bytes()) == PCB_SHA
    licdir = sources / "LICENSES"; licdir.mkdir()
    for name in ["LICENSE", "LICENSE.md"]:
        if (ROOT/name).exists(): shutil.copy2(ROOT/name, sources/name)
    for path in (ROOT / "LICENSES").iterdir():
        if path.is_file(): shutil.copy2(path, licdir / path.name)
    (sources / "README_SOURCE_IDENTITY.md").write_text("# Current editable R138 KiCad\n\nOpen enku-mainboard-r0.1.kicad_pro with KiCad 10.0.7. All five schematic sheets, embedded PCB footprints and project-local symbol/footprint tables/libraries are included. No historical PCB layout is included. External 3D models and final case CAD are not supplied. Source commit: "+SOURCE+". PCB SHA256: "+PCB_SHA+". ENGINEERING REVIEW ONLY - NO FAB.\n")
    shutil.copy2(archive, proofdir / archive.name)
    for name in ["GITHUB_MAIN_R138.json", "ANNULAR_REVIEW_R138.md", "BRINGUP_R138.md"]:
        shutil.copy2(ROOT / "docs" / name, proofdir / name)
    for name in ["run.json", "jobs.json", "artifacts.json", "source_commit.json", "comparison_R138.json"]:
        p = ROOT / "docs/evidence/R138/main" / name
        if p.exists(): shutil.copy2(p, proofdir / name)
    for name in ["pre_delivery_drc_R138.json", "pre_delivery_erc_R138.json"]:
        assert (build_dir/name).exists(), "Run native DRC/ERC before packaging"
        data = json.loads((build_dir/name).read_text())
        if "drc" in name: assert not data["violations"] and not data["unconnected_items"] and not data["schematic_parity"]
        else: assert not any(s["violations"] for s in data["sheets"])
        shutil.copy2(build_dir/name, proofdir/name)
    cores = build_dir / "tmp/pdfs"
    schematic = fitz.open(cores / "schematic-core.pdf")
    assert len(schematic) == 5
    for page in schematic:
        page.insert_font(fontname="ENKU", fontfile=str(FONT_DIR / "Vera.ttf"))
        page.insert_text((16, 10), "ENKU physical R138 | KiCad 10.0.7 | NO FAB | PCB SHA256 " + PCB_SHA, fontsize=6, fontname="ENKU")
    schematic.save(pdfdir / "SCHEMATIC_R138.pdf", deflate=True)
    frame_native(cores / "assembly-core.pdf", cores / "assembly-framed.pdf", ["Front footprints / numbered pads - native F.Fab / Edge.Cuts"])
    frame_native(cores / "layers-core.pdf", pdfdir / "NATIVE_LAYERS_R138.pdf", LAYER_NAMES, same_frame=True)
    story = [paragraph("Complete reference / pad index", "title"), paragraph("127 PCB references: 107 FIT, one DNP (R67), 19 BARE_PCB. Coordinates are absolute Gerber mm. The reference pad column uses pad 1 where present, otherwise A1 or the first numbered pad; it is an orientation aid, not an automatic polarity assertion. Native assembly plot may hide some references; this index includes all."), Spacer(1, 8)]
    for start in range(0, len(index), 32):
        if start: story += [PageBreak(), paragraph("Reference / pad index (continued)", "h")]
        rows = [[r[0], r[1], f"{r[2]:.3f}", f"{r[3]:.3f}", f"{r[4]:g}", r[5], (f"{r[6]:.3f}/{r[7]:.3f}" if r[5] else ""), r[8]] for r in index[start:start+32]]
        story += [table(["Ref", "State", "X", "Y", "Rot", "Pad", "Pad X / Y", "MPN"], rows, [32, 43, 38, 43, 29, 29, 76, 117])]
    authored_pdf(cores / "reference-index.pdf", story)
    w = PdfWriter()
    for p in [cores / "assembly-framed.pdf", cores / "reference-index.pdf"]:
        w.append(str(p))
    with (pdfdir / "ASSEMBLY_TOP_AND_REFERENCE_INDEX_R138.pdf").open("wb") as f: w.write(f)
    review_pdf(pdfdir / "ENGINEERING_REVIEW_AND_TEST_PLAN_R138.pdf", boot)
    readme = """# ENKU Base Reader R138 - PCBWay engineering review

ENGINEERING REVIEW ONLY - NO FAB / NO ASSEMBLY RELEASE.
Please review the DFM, component sourcing, special-via/USB/stencil/stackup and
proposed functional-test requirements. Manufacturing and purchases need the
customer's separate approval after the documented holds are closed.

01_MANUFACTURING_REVIEW: exact verified Gerber/drill/IPC/BOM/CPL and process CSVs.
02_ASSEMBLY_REFERENCE: PCBWay-column aliases, complete 127-reference/first-pad
index, actual connector pad net map and explicitly pending off-board items.
03_PDF_REVIEW: all 5 schematic sheets, front assembly plus complete index,
11 native layer views and engineering review/test plan. PCB views are auto-fit,
NOT TO SCALE. Schematic pages retain their native drawing-sheet dimensions.
04_QUALIFICATION_NOT_RUN: qualification/FCT templates, recovery instructions,
and a pending firmware manifest. No validated factory binary is supplied.
05_EDITABLE_KICAD: only the current project, local libraries and licenses.
06_VERIFIED_SOURCE_EVIDENCE: original main native artifact and proof, plus fresh
native DRC/ERC and source-only recovery audit. Physical tests remain NOT RUN.

Physical PCB revision: R138. Audit/document preparation: R139.
The current filenames retain r0.1; the packet revision and PCB hash control.
107 top FIT placements; R67 DNP; 19 BARE_PCB references are not purchased parts.
All manufacturing coordinates: absolute 0,0, mm; X=boardX, Y=-boardY.
Do not independently change origin/angles or silently substitute components.
The battery, separate hand-attached NTC, exact panel/FPC and current case are
not released off-board assemblies. Two thin interchangeable CN/PL packs remain
unqualified; case thickness must not increase.

Source and exports are computationally checked. Startup/charging/NTC faults,
loads, recovery/MSC, endurance, final case and per-unit FCT are not physically
qualified. The packet is complete for engineering REVIEW, not for production.
No factory upload, order, payment or supplier message was performed.
"""
    (packet / "00_README_FIRST_NO_FAB.md").write_text(readme)
    files = {p.relative_to(packet).as_posix(): {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size} for p in sorted(packet.rglob("*")) if p.is_file()}
    pdf_pages = {p.name: len(PdfReader(p).pages) for p in pdfdir.glob("*.pdf")}
    assert len(pdf_pages) == 4 and pdf_pages["SCHEMATIC_R138.pdf"] == 5 and pdf_pages["NATIVE_LAYERS_R138.pdf"] == 11
    manifest = {"packet": packet.name, "status": "ENGINEERING REVIEW ONLY - NO FAB", "generated_utc": datetime.now(timezone.utc).isoformat(), "physical_revision": "R138", "audit_revision": "R139", "frozen_hardware_source_commit": SOURCE, "native_verified_source_commit": "2601e16abb754564580adb28c202337e69d8b1ab", "pcb_sha256": PCB_SHA, "main_native_artifact_sha256": ARTIFACT_SHA, "native_kicad": native, "original_manufacturing_files_exact": 24, "Gerber_files": 11, "drill_files": 2, "fitted_placements": 107, "all_reference_index_rows": 127, "fill_cap_process_requests": 6, "PDF_pages": pdf_pages, "physical_tests": "NOT RUN", "factory_images_supplied": False, "fabrication_ready": False, "consumer_release_ready": False, "files_excluding_manifest_and_checksums": files}
    write_json(packet / "MANIFEST.json", manifest)
    all_files = sorted(p for p in packet.rglob("*") if p.is_file())
    (packet / "SHA256SUMS.txt").write_text("".join(sha(p.read_bytes())+"  "+p.relative_to(packet).as_posix()+"\n" for p in all_files))
    output = build_dir.parent / (packet.name + ".zip")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(packet.rglob("*")):
            if p.is_file(): z.write(p, packet.name+"/"+p.relative_to(packet).as_posix())
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        assert all(not n.startswith("/") and ".." not in Path(n).parts for n in z.namelist())
        for name, meta in files.items():
            data = z.read(packet.name+"/"+name); assert sha(data)==meta["sha256"] and len(data)==meta["bytes"]
        assert sum(n.endswith(".gbr") for n in z.namelist()) == 11
        assert sum(n.endswith(".drl") for n in z.namelist()) == 2
    record = {"archive_name": output.name, "sha256": sha(output.read_bytes()), "bytes": output.stat().st_size, "archive_members": len(all_files)+1, "CRC_and_file_hashes": "PASS", "semantic_checks": "PASS", "visual_PDF_QA": "PENDING", "physical_tests": "NOT RUN", "manufacturing_release_approved": False, "manifest": manifest}
    write_json(ROOT / "docs/qualification/R139/PCBWAY_PACKET_R138.json", record)
    print(json.dumps({k:v for k,v in record.items() if k!="manifest"}, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--build-dir", required=True, type=Path); ap.add_argument("--app", required=True, type=Path)
    args = ap.parse_args(); build(args.build_dir.resolve(), args.app.resolve())
