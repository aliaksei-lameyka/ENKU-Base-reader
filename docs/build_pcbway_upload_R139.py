"""Package the accepted main-run manufacturing bytes for PCBWay review.

Prepare reuses the hash-verified previous packet's unchanged native PDF views.
The report is regenerated after the J4 -> J5 documentation correction. Finalize
requires the Artifact Tool BOM workbook and never authorizes fabrication.
"""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "5f0d269f36333bc86190adaa1ad059912c93a5db"
CI_SOURCE = "43a19802074b249ef29fd31211ede7e863c8e204"
PCB_SHA = "90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971"
OLD_SHA = "c113ffdac4c2613a2f8736acf692a01c063a4e41b7f521715bab50e7373a3b00"
NATIVE_SHA = "2abc4456ac89f04aa4e9937c4a0c8dd6fd67be49100cc161c2d754dfb0d958dc"
PACKET = "ENKU_Base_R138_PCBWay_Full_Review_NO_FAB"
GERBERS = "ENKU_Base_R138_PCBWay_Gerbers_NO_FAB.zip"
BOM = "ENKU_Base_R138_PCBWay_BOM"
CPL = "ENKU_Base_R138_PCBWay_CPL_mm.csv"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def csv_rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def csv_write(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def safe_zip(z):
    assert z.testzip() is None
    assert len(z.namelist()) == len(set(z.namelist()))
    assert all(not n.startswith("/") and ".." not in Path(n).parts for n in z.namelist())


def prepare(retained, output):
    assert sha(retained.read_bytes()) == OLD_SHA
    native = ROOT / "docs/evidence/R139/main/native_server_R138.zip"
    assert sha(native.read_bytes()) == NATIVE_SHA
    assert sha((ROOT / "hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pcb").read_bytes()) == PCB_SHA
    proof = json.loads((ROOT / "docs/GITHUB_MAIN_R139.json").read_text())
    assert proof["verified_source_commit"] == CI_SOURCE and proof["run_id"] == 38356800482
    assert proof["DRC"] == proof["ERC"] == proof["opens"] == proof["schematic_parity"] == 0
    assert proof["all_24_manufacturing_files_verified"] and not proof["fabrication_ready"]
    for p in ["hardware", ".github", "LICENSE", "LICENSE.md", "LICENSES"]:
        rev = lambda ref: subprocess.check_output(["git", "rev-parse", ref + ":" + p], cwd=ROOT)
        assert rev("HEAD") == rev(SOURCE) == rev(CI_SOURCE), p
    output.mkdir(parents=True, exist_ok=True)
    packet = output / PACKET
    assert not packet.exists(), "Use a fresh output directory"
    packet.mkdir()
    with zipfile.ZipFile(retained) as z:
        safe_zip(z)
        assert len(z.namelist()) == 128
        prefix = z.namelist()[0].split("/")[0] + "/"
        old = json.loads(z.read(prefix + "MANIFEST.json"))
        for rel, meta in old["files_excluding_manifest_and_checksums"].items():
            raw = z.read(prefix + rel)
            assert sha(raw) == meta["sha256"] and len(raw) == meta["bytes"], rel
        for name in z.namelist():
            rel = name[len(prefix):]
            if rel in ["MANIFEST.json", "SHA256SUMS.txt"]:
                continue
            dest = packet / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(z.read(name))
    evidence = packet / "06_VERIFIED_SOURCE_EVIDENCE"
    evidence.rename(packet / "06_RETAINED_R138_REFERENCE")
    ref = packet / "06_RETAINED_R138_REFERENCE"
    (ref / "README_RETAINED_REFERENCE.md").write_text(
        "# Earlier accepted R138 evidence\n\nThese records refer to the original R138 source and previous review packet, not this upload package. The current main evidence is in 07_CURRENT_MAIN_EVIDENCE.\n")
    json_write(ref / "PREVIOUS_PACKET_MANIFEST.json", old)
    current = packet / "07_CURRENT_MAIN_EVIDENCE"
    current.mkdir()
    for f in (ROOT / "docs/evidence/R139/main").iterdir():
        if f.is_file():
            shutil.copy2(f, current / f.name)
    shutil.copy2(ROOT / "docs/GITHUB_MAIN_R139.json", current)
    with zipfile.ZipFile(native) as z:
        safe_zip(z)
        original = json.loads(z.read("manufacturing_review_R138/manifest_R138.json"))
        assert len(original["files"]) == 24
        manu = packet / "01_MANUFACTURING_REVIEW"
        for rel, meta in original["files"].items():
            data = z.read("manufacturing_review_R138/" + rel)
            assert sha(data) == meta["sha256"] and len(data) == meta["bytes"], rel
            dest = manu / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        (manu / "manifest_R138.json").write_bytes(z.read("manufacturing_review_R138/manifest_R138.json"))
        features = json.loads(z.read("assembly_features.json"))
        geometry = json.loads(z.read("geometry.json"))
    bom = csv_rows((manu / "BOM_fitted_review.csv").read_bytes())
    cpl = csv_rows((manu / "CPL_native_mm.csv").read_bytes())
    classified = csv_rows((manu / "BOM_all_classified.csv").read_bytes())
    fitted = {ref.strip() for row in bom for ref in row["Designator"].split(",")}
    assert len(bom) == 58 and sum(int(row["Quantity"]) for row in bom) == len(fitted) == 107
    assert {row["Ref"] for row in cpl} == fitted and len(cpl) == 107
    assert all(row["Side"] == "top" for row in cpl) and "R67" not in fitted
    assert len(classified) == 127
    assert {r["Reference"] for r in classified if r["Assembly"] == "DNP"} == {"R67"}
    assert sum(r["Assembly"] == "BARE_PCB" for r in classified) == 19
    fp = {f["ref"]: f for f in features["footprints"]}
    assert fp["J5"]["fields"]["MPN"] == "USB4215-03-A" and "J4" not in fp
    assert all(fp[r]["attributes"] & 2 for r in fitted), "Centroid must contain SMD-mountable parts"
    assert all(r["Manufacturer Part Number"] and r["Manufacturer"] for r in bom)
    headers = ["Designator", "Quantity", "Manufacturer Part Number", "Footprint", "Manufacturer", "Description", "Type", "Notes"]
    rows = []
    for row in bom:
        refs = [r.strip() for r in row["Designator"].split(",")]
        assert len(refs) == int(row["Quantity"])
        types = []
        for r in refs:
            pads = [p for p in features["pads"] if p["ref"] == r]
            types.append("Hybrid" if any(p["attribute"] == 0 and any(p["drill_mm"]) for p in pads) else "SMD")
        assert len(set(types)) == 1
        notes = ""
        if "J5" in refs:
            notes = "USB-C J5: plated short stakes; solder process needs written acceptance. See manufacturing notes."
        elif "U1" in refs:
            notes = "SMD module with intrinsic EP PTH holes; preserve EP copper/mask/paste grid and agreed joint process."
        elif "U3" in refs:
            notes = "Five EP vias require resin fill and copper cap; exact process CSV controls."
        elif "R28" in refs:
            notes = "Pin-1 via requires resin fill and copper cap; exact process CSV controls."
        rows.append([row["Designator"], int(row["Quantity"]), row["Manufacturer Part Number"], row["Footprint"], row["Manufacturer"], row["Value"], types[0], notes])
    csv_write(output / (BOM + ".csv"), headers, rows)
    json_write(output / "bom_workbook_input.json", {"headers": headers, "rows": rows})
    cpl_headers = ["Designator", "Mid X", "Mid Y", "Layer", "Rotation", "Package", "Value"]
    csv_write(output / CPL, cpl_headers, [[r["Ref"], r["PosX"], r["PosY"], r["Side"], r["Rot"], r["Package"], r["Val"]] for r in cpl])
    assembly = packet / "02_ASSEMBLY_REFERENCE"
    for obsolete in ["BOM_PCBWay_columns.csv", "CPL_PCBWay_columns_mm.csv"]:
        (assembly / obsolete).unlink()
    shutil.copy2(output / (BOM + ".csv"), assembly)
    shutil.copy2(output / CPL, assembly)
    notes = (ROOT / "docs/PCBWAY_MANUFACTURING_NOTES_R138.md").read_text()
    notes = notes.replace("81b34a97c765c0fdb5ded5e4c1d4ed22d06756cb", SOURCE).replace("2601e16abb754564580adb28c202337e69d8b1ab", CI_SOURCE)
    assert "USB J5" in notes and "USB J4" not in notes
    (manu / "PCBWAY_MANUFACTURING_NOTES_R138.md").write_text(notes)
    for name in ["BATTERY_STATUS_R139.md", "CURRENT_STATUS.md"]:
        text = (ROOT / "docs" / name).read_text()
        def portable(m):
            href = m.group(1)
            if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", href) or href.startswith("#"):
                return m.group(0)
            target = (ROOT / "docs" / href.split("#", 1)[0]).resolve().relative_to(ROOT)
            return "](https://github.com/aliaksei-lameyka/ENKU-Base-reader/blob/" + SOURCE + "/" + target.as_posix() + ")"
        (current / name).write_text(re.sub(r"\]\(([^\s)]+)\)", portable, text))
    (packet / "05_EDITABLE_KICAD/README_SOURCE_IDENTITY.md").write_text(
        f"# Current editable physical R138\n\nSource snapshot: {SOURCE}. Native CI source: {CI_SOURCE}. Hardware and workflow trees are identical. Open enku-mainboard-r0.1.kicad_pro with KiCad10.0.7; all five schematic sheets and project-local libraries are included. PCB SHA256: {PCB_SHA}. External 3D models and final case CAD are not supplied. ENGINEERING REVIEW ONLY - NO FAB.\n")
    spec = importlib.util.spec_from_file_location("review", ROOT / "docs/build_pcbway_review_R139.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    boot = json.loads((ROOT / "docs/qualification/R139/boot_recovery_source_audit_R139.json").read_text())
    module.review_pdf(packet / "03_PDF_REVIEW/ENGINEERING_REVIEW_AND_TEST_PLAN_R138.pdf", boot,
                      source_commit=SOURCE, main_run_id=38356800482)
    readme = f"""# ENKU Base Reader R138 - PCBWay upload package

QUOTE AND ENGINEERING REVIEW ONLY. NO FAB / NO ASSEMBLY RELEASE.

Upload {GERBERS} to the Gerber field. For assembly upload
{BOM}.xlsx (or the matching CSV) as BOM and {CPL} as centroid.
Send this complete package for assembly/process review, including all PDFs and
the manufacturing instructions. Do not upload a GitHub source ZIP as Gerber.

Physical PCB R138, documentation R139. Source snapshot {SOURCE}; actual
native CI source {CI_SOURCE}, run38356800482. The physical board is unchanged.
PCB SHA256 {PCB_SHA}. Four layers,59x101mm bounding box with side cutout,
nominal1.6mm. Stackup/material/copper/finish/impedance need job acceptance.

01_MANUFACTURING_REVIEW contains the exact24 current-main manufacturing
payloads:11 Gerbers,2 Excellon PTH/NPTH drill files,drill maps/report,IPC-D-356,
native BOM/CPL and the six fill/cap requests. Empty back paste is intentional.
02_ASSEMBLY_REFERENCE contains the import BOM/CPL,full reference/pad indices,
connector/MCU maps and pending off-board items. The Excel BOM has one import
sheet with headers in row1 and58 groups/107 fitted parts per board.
03_PDF_REVIEW contains five-sheet schematic,assembly/reference drawing,
11 native layer views and the corrected9-page engineering/test report.
04_QUALIFICATION_NOT_RUN contains test templates and flash contract.
05_EDITABLE_KICAD contains the canonical project,local libraries and licenses.
06_RETAINED_R138_REFERENCE is earlier accepted evidence,not current inputs.
07_CURRENT_MAIN_EVIDENCE contains actual run/API records and the exact artifact.

USB-C is J5 / GCT USB4215-03-A. The previous instruction's J4 label was wrong;
the physical PCB/BOM/pad map have the correct J5. R67 is DNP;19 BARE_PCB
features are excluded from procurement/placement. J7 is a bare fixture contact
array;J8 is bare hand-solder NTC pads. No socket/connector is fitted at J7/J8.

All native coordinates share absolute origin0,0 in mm:X=boardX,Y=-boardY.
Centroid values and native angles are unchanged;all107 fitted parts are on top.
Agree library zero-angle and pin1 against drawings before assembly. Do not
independently shift the Gerber/CPL origin or silently substitute components.

Written process acceptance is required for91 nominal0.20mm bores on1.6mm,
five U3 resin-filled/copper-capped EP vias and one R28 filled/capped via,
U1 EP grid/12 intrinsic PTH holes,and J5 short plated stakes/stencil process.
The exact process CSVs control;ordinary tenting does not replace fill/cap.

Battery and external NTC,display/FPC,case and validated firmware/fixture are
excluded from the107-part PCB-mounted BOM and remain HOLD. Thin protected
2000-2500mAh packs and China/Poland alternatives are not qualified;case
thickness must not increase. No factory binary or completed physical test is
invented. Physical qualification is NOT RUN;consumer release remains HOLD.

No order,payment,purchase or factory upload was made while building this package.
PCBWay file-format reference:https://www.pcbway.com/assembly-file-requirements.html
"""
    (packet / "00_README_FIRST_NO_FAB.md").write_text(readme)
    json_write(output / "build_context.json", {"source": SOURCE, "ci_source": CI_SOURCE,
               "packet": PACKET, "native_artifact_sha256": NATIVE_SHA,
               "original_manufacturing_files": original["files"], "fitted_parts": 107,
               "bom_groups": 58, "pdf_visual_QA": "PENDING"})
    print("Prepared exact24 current-main payloads,58 BOM groups/107 top placements,and corrected J5 report")


def inspect_xlsx(path, expected):
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        safe_zip(z)
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            strings = ["".join(s.itertext()) for s in ET.fromstring(z.read("xl/sharedStrings.xml"))]
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        rows = []
        for r in sheet.findall("s:sheetData/s:row", ns):
            cells = []
            for c in r.findall("s:c", ns):
                assert c.find("s:f", ns) is None, "Manufacturing import must contain literal source fields"
                t = c.get("t"); v = c.find("s:v", ns)
                if t == "s": value = strings[int(v.text)]
                elif t == "inlineStr": value = "".join(c.find("s:is", ns).itertext())
                else: value = v.text if v is not None else ""
                cells.append((c.get("r"), value))
            rows.append(cells)
        matrix = dict(cell for row in rows for cell in row)
        for ri, row in enumerate([expected["headers"], *expected["rows"]], 1):
            for ci, value in enumerate(row):
                address = chr(65 + ci) + str(ri)
                actual = matrix.get(address, "")
                assert str(value) == actual or isinstance(value, int) and float(actual) == value, (address, value, actual)
        assert len(rows) == 59
        assert sheet.find("s:sheetViews/s:sheetView/s:pane", ns) is not None


def finalize(output):
    packet = output / PACKET
    context = json.loads((output / "build_context.json").read_text())
    expected = json.loads((output / "bom_workbook_input.json").read_text())
    inspect_xlsx(output / (BOM + ".xlsx"), expected)
    shutil.copy2(output / (BOM + ".xlsx"), packet / "02_ASSEMBLY_REFERENCE")
    manu = packet / "01_MANUFACTURING_REVIEW"
    for rel, meta in context["original_manufacturing_files"].items():
        raw = (manu / rel).read_bytes()
        assert sha(raw) == meta["sha256"] and len(raw) == meta["bytes"], rel
    assert context["pdf_visual_QA"] == "PASS"
    small = {}
    for base in ["gerber", "drill"]:
        for p in (manu / base).iterdir():
            if p.suffix in [".gbr", ".drl", ".gbrjob"] or p.name == "drill-report.txt":
                assert p.name not in small
                small[p.name] = p.read_bytes()
    for name in ["netlist.d356", "U3_via_process_requests.csv", "R28_via_process_request.csv", "PCBWAY_MANUFACTURING_NOTES_R138.md"]:
        small[name] = (manu / name).read_bytes()
    small["README_FIRST_NO_FAB.md"] = (packet / "00_README_FIRST_NO_FAB.md").read_bytes()
    assert sum(n.endswith(".gbr") for n in small) == 11 and sum(n.endswith(".drl") for n in small) == 2
    json_write(packet / "MANIFEST.json", {**context,
        "status": "QUOTE AND ENGINEERING REVIEW ONLY - NO FAB",
        "physical_pcb_revision": "R138", "documentation_revision": "R139",
        "pcb_sha256": PCB_SHA, "generated_utc": datetime.now(timezone.utc).isoformat(),
        "DRC": 0, "ERC": 0, "opens": 0, "schematic_parity": 0,
        "physical_tests": "NOT RUN", "factory_images_supplied": False,
        "fabrication_ready": False, "consumer_release_ready": False,
        "files_excluding_manifest_and_checksums": {p.relative_to(packet).as_posix():
            {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
            for p in sorted(packet.rglob("*")) if p.is_file()}})
    (packet / "SHA256SUMS.txt").write_text("".join(sha(p.read_bytes()) + "  " + p.relative_to(packet).as_posix() + "\n" for p in sorted(packet.rglob("*")) if p.is_file()))
    def archive(path, members):
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name, raw in sorted(members.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 10, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, raw, compresslevel=9)
        with zipfile.ZipFile(path) as z:
            safe_zip(z)
            assert set(z.namelist()) == set(members)
            for name, raw in members.items(): assert z.read(name) == raw, name
    archive(output / GERBERS, small)
    archive(output / (PACKET + ".zip"), {PACKET + "/" + p.relative_to(packet).as_posix(): p.read_bytes()
            for p in packet.rglob("*") if p.is_file()})
    paths = [output / (PACKET + ".zip"), output / GERBERS, output / (BOM + ".csv"), output / (BOM + ".xlsx"), output / CPL]
    record = {"source_snapshot": SOURCE, "native_ci_source": CI_SOURCE, "native_run_id": 38356800482,
              "pcb_sha256": PCB_SHA, "Gerber_files": 11, "drill_files": 2,
              "BOM_groups": 58, "fitted_parts_per_board": 107, "CPL_placements": 107,
              "all_reference_rows": 127, "DNP": ["R67"], "bare_pcb_features": 19,
              "fill_cap_process_requests": 6, "usb_reference": "J5",
              "original_24_current_main_payloads": "BYTE IDENTICAL",
              "XLSX_values_vs_native_BOM": "PASS", "PDF_visual_QA": "PASS",
              "ZIP_CRC_unique_members_and_all_bytes": "PASS", "physical_tests": "NOT RUN",
              "factory_images_supplied": False, "fabrication_ready": False,
              "created_utc": datetime.now(timezone.utc).isoformat(),
              "files": [{"name": p.name, "bytes": p.stat().st_size, "sha256": sha(p.read_bytes()),
                         **({"members": len(zipfile.ZipFile(p).namelist())} if p.suffix == ".zip" else {})}
                        for p in paths]}
    json_write(output / "PACKAGE_QA.json", record)
    json_write(ROOT / "docs/qualification/R139/PCBWAY_UPLOAD_PACKAGE_R139.json", record)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["prepare", "finalize"])
    ap.add_argument("--retained", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.mode == "prepare": prepare(args.retained, args.output)
    else: finalize(args.output)
