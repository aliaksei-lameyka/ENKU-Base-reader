"""English documentation edition and flat Gerber ZIP; verified hardware unchanged."""
from pathlib import Path
import csv,hashlib,json,re,shutil,zipfile
import fitz
repo=Path(__file__).resolve().parents[1];r=repo/'hardware/mainboard/r144';old=r/'pcbway';p=r/'pcbway_en';out=repo.parent/'deliverables-r144-en';out.mkdir(exist_ok=True);sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest();pcb_sha='676c157fb58c1d5b689b4a6841749d8be283982745ce40580c0a33308f7e2d2c'
original=json.loads((old/'PACKET_MANIFEST_R144.json').read_text())
for name,meta in original['files'].items():assert sha(old/name)==meta['sha256'],name
for folder in ['01_fabrication','02_assembly','04_editable_kicad','05_verification','06_qualification']:
 before={q.relative_to(old/folder).as_posix():sha(q)for q in(old/folder).rglob('*')if q.is_file()};after={q.relative_to(p/folder).as_posix():sha(q)for q in(p/folder).rglob('*')if q.is_file()};assert before==after,folder
assert sha(r/'kicad/enku-mainboard-r0.1.kicad_pcb')==pcb_sha
review=p/'03_drawings/ENKU_R144_Board_Review_EN_NO_FAB.pdf';doc=fitz.open(review);assert len(doc)==6;assert not re.search(r'[А-Яа-яЁё]',''.join(q.get_text()for q in doc))
for name,pages in [('ENKU_R144_Layers_Assembly_NO_FAB.pdf',10),('ENKU_R144_Schematics_NO_FAB.pdf',5)]:assert len(fitz.open(p/'03_drawings'/name))==pages and sha(p/'03_drawings'/name)==sha(old/'03_drawings'/name)
gerbers=sorted((p/'01_fabrication/gerber').glob('*.gbr'));drills=sorted((p/'01_fabrication/drill').glob('*.drl'));assert len(gerbers)==11 and len(drills)==2
expected={'Copper,L1,Top','Copper,L2,Inr','Copper,L3,Inr','Copper,L4,Bot','Soldermask,Top','Soldermask,Bot','Paste,Top','Paste,Bot','Legend,Top','Legend,Bot','Profile,NP'}
functions={re.search(r'%TF\.FileFunction,([^*]+)\*%',f.read_text())[1]for f in gerbers};assert functions==expected,functions
readme='''# ENKU Base R144 - English engineering review package

**NO FAB. Physical tests: NOT RUN.** Proposed pilot:5-10 boards, with the first1-2 assemblies evaluated before the remainder.

Board:59 x101 x1.6mm, four copper layers. Verified source commit609f8ac00357b9b0c6b3c43c381469c498453a11. PCB SHA256:676c157fb58c1d5b689b4a6841749d8be283982745ce40580c0a33308f7e2d2c. Source-pinned GitHub Actions run38693384483 passed. The English edition changes documentation only; all manufacturing, assembly, editable KiCad and verification inputs are byte-identical to the verified R144 package.

## Files to use

- `ENKU_R144_GERBER.zip`: separate flat archive for CAM review. All11 Gerber layers, separate PTH/NPTH drills, Gerber job, drill maps/report, IPC356 and the two fill/cap request CSVs are in its root. The archive is also supplied separately.
- `01_fabrication`: original paired Gerber/drill/IPC356 set in its reviewed folder structure.
- `02_assembly`:62 fitted BOM groups,120 top placements,141 classified references, complete473-pad map, first-pad index, CSV process requests and the English BOM/CPL workbook.19 bare-PCB entries, R67/R99 DNP, R97 FIT. Never populate R97 and R99 together.
- `03_drawings`:six-page English board review,10 layer/assembly pages and5 schematic pages. CAM uses the actual Gerber/drill files; PDFs support review.
- `04_editable_kicad`:68 byte-identical source files.
- `05_verification`:actual native/independent reports, source manifest and unchanged source-pinned server artifact.
- `06_qualification`:English manufacturing instructions, FPC review, executed checks, startup risks and per-board FCT plan.

Coordinates:millimetres, absolute0,0, X=KiCad board X and Y=-KiCad board Y. All fitted components are top side. Native top angles require supplier import/rotation approval. B.Paste is intentionally empty.

## Items still requiring closure

Initial and declared extra+/-0.1% solder-shift static reserves pass. Lifetime adverse-shift scenarios and measured startup/ripple/load/OFF behavior remain HOLD. Qualify the actual FPC contact-end dimensions/folded pin1, protected PH2 battery and cell-bonded NTC,90-ohm USB stackup,84 nominal0.20mm bores on1.6mm, six resin-fill/copper-cap sites, short USB stakes, common stencil/reflow, exact BOM/CPL import, effective capacitance/EPD power and reproducible FCT firmware. Physical tests have not been run.

All384 vias have nominal annular ring>=0.15mm;378 ordinary vias have SMD separation>=0.10mm. The five U3 and one R28 sites require resin fill/copper cap. Excellon does not encode this process: review the included request CSVs. No factory order or manufacturing release is made by this package.

Use PACKET_MANIFEST_R144_EN.json for exact file hashes. Do not mix revisions.
'''
(p/'README_PCBWAY_R144_EN_NO_FAB.md').write_text(readme)
def archive(path,items):
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for name,file in sorted(items):z.write(file,name)
 with zipfile.ZipFile(path)as z:
  assert z.testzip()is None and len(z.namelist())==len(items)
  for name,file in items:assert hashlib.sha256(z.read(name)).hexdigest()==sha(file)
# Flat root: actual Gerber/drill bytes, with no directory prefix.
flat=[(q.name,q)for q in(p/'01_fabrication').rglob('*')if q.is_file()]+[(n,p/'02_assembly'/n)for n in ['U3_via_process_requests.csv','R28_via_process_request.csv']]
assert len({n for n,q in flat})==len(flat)
note=out/'README_GERBER_R144_NO_FAB.txt';note.write_text('ENKU Base R144 - CAM review only / NO FAB\nPCB SHA256: '+pcb_sha+'\n11 Gerber layers and separate PTH/NPTH drills, in millimetres.\nSix resin-fill/copper-cap sites require process acceptance; see both included CSVs.\nPhysical tests NOT RUN. Use the complete English review package for assembly and qualification.\n')
flat.append((note.name,note));manifest=out/'GERBER_MANIFEST_R144.json';manifest.write_text(json.dumps(dict(revision='R144',pcb_sha256=pcb_sha,Gerber_layers=11,drill_files=2,flat_root=True,fabrication_ready=False,files={n:dict(bytes=q.stat().st_size,sha256=sha(q))for n,q in flat}),indent=2)+'\n');flat.append((manifest.name,manifest));g=out/'ENKU_R144_GERBER.zip';archive(g,flat)
with zipfile.ZipFile(g)as z:assert all('/'not in n for n in z.namelist())and len([n for n in z.namelist()if n.endswith('.gbr')])==11 and len([n for n in z.namelist()if n.endswith('.drl')])==2
shutil.copy2(g,p/g.name)
files={q.relative_to(p).as_posix():dict(bytes=q.stat().st_size,sha256=sha(q))for q in sorted(p.rglob('*'))if q.is_file()and q.name!='PACKET_MANIFEST_R144_EN.json'}
record=dict(revision='R144',language='English',pcb_sha256=pcb_sha,verified_source_commit='609f8ac00357b9b0c6b3c43c381469c498453a11',hardware_and_manufacturing_unchanged=True,files=files,physical_tests='NOT RUN',fabrication_ready=False);(p/'PACKET_MANIFEST_R144_EN.json').write_text(json.dumps(record,indent=2)+'\n')
full=out/'ENKU_Reader_Base_R144_PCBWay_Review_EN_NO_FAB.zip';archive(full,[(q.relative_to(p).as_posix(),q)for q in p.rglob('*')if q.is_file()]);shutil.copy2(review,out/review.name)
result=dict(revision='R144',language='English',review_pages=6,package_files=len(files)+1,Gerber_layers=11,drill_files=2,all_Gerber_and_drill_bytes_equal_verified_R144=True,files={q.name:dict(bytes=q.stat().st_size,sha256=sha(q))for q in [full,g,out/review.name]},physical_tests='NOT RUN',fabrication_ready=False);(out/'DELIVERABLES_R144_EN.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
