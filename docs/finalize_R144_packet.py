"""Validate paired source and manufacturing/assembly files, then create review ZIPs."""
from pathlib import Path
import csv,hashlib,json,shutil,sys,zipfile,xml.etree.ElementTree as ET
repo=Path(__file__).resolve().parents[1];r=repo/'hardware/mainboard/r144';p=r/'pcbway';out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True);sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
proof=json.loads((repo/'docs/GITHUB_R144.json').read_text());assert proof['source_manifest_sha256']==sha(r/'source_manifest_R144.json')
manifest=json.loads((r/'source_manifest_R144.json').read_text());source=r/'kicad';copy=p/'04_editable_kicad';assert len(manifest['files'])==68
for folder in [source,copy]:
 assert set(manifest['files'])=={q.relative_to(folder).as_posix()for q in folder.rglob('*')if q.is_file()}
 for name,meta in manifest['files'].items():assert sha(folder/name)==meta['sha256']and(folder/name).stat().st_size==meta['bytes'],name
g=json.loads(zipfile.ZipFile(p/'05_verification/R144_actual_server_verification.zip').read('candidate/geometry.json'));assert len(g['footprints'])==141 and len(g['pads'])==473 and sum(t['via']for t in g['tracks'])==384
rows=lambda n:list(csv.DictReader((p/'02_assembly'/n).open()))
bom=rows('BOM_PCBWay_R144.csv');cpl=rows('CPL_PCBWay_R144.csv');classified=rows('BOM_all_classified.csv');assert sum(int(a['Quantity'])for a in bom)==120 and len(cpl)==120 and len(classified)==141
assert {a['Reference']for a in classified if a['Assembly']=='DNP'}=={'R67','R99'}and len([a for a in classified if a['Assembly']=='BARE_PCB'])==19
assert len(rows('Complete_pad_map_R144.csv'))==473 and len(rows('Reference_first_pad_index_R144.csv'))==141
assert {a['Designator']for a in cpl}=={ref for a in bom for ref in a['Designator'].split(',')}and all(a['Layer']=='Top'for a in cpl)
for a in cpl:
 fp=g['footprints'][a['Designator']];assert abs(float(a['Mid X'])-fp['pos'][0])<1e-6 and abs(float(a['Mid Y'])+fp['pos'][1])<1e-6 and abs(float(a['Rotation'])-fp['angle'])<1e-6
assert len(list((p/'01_fabrication/gerber').glob('*.gbr')))==11 and len(list((p/'01_fabrication/drill').glob('*.drl')))==2
z=zipfile.ZipFile(p/'02_assembly/ENKU_R144_BOM_CPL_NO_FAB.xlsx');assert z.testzip()is None
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for n in [1,2]:
 sheet=ET.fromstring(z.read(f'xl/worksheets/sheet{n}.xml'));cell=sheet.find(".//m:c[@r='B4']",ns);assert float(cell.find('m:v',ns).text)==120 and cell.find('m:f',ns)is not None
 for cell in sheet.findall('.//m:c',ns):assert cell.attrib.get('t')!='e'
# Every checksum covers delivered bytes. Authoring caches and signed upload data are excluded.
assert not list(p.rglob('*.pyc'))and not list(p.rglob('*.inspect.ndjson'))and not list(p.rglob('*.lck'))
for q in p.rglob('*'):
 if q.is_file():assert q.suffix.lower()not in ['.step','.stp'],q
files={q.relative_to(p).as_posix():dict(bytes=q.stat().st_size,sha256=sha(q))for q in sorted(p.rglob('*'))if q.is_file()and q.name!='PACKET_MANIFEST_R144.json'}
record=dict(revision='R144',pcb_sha256=sha(source/'enku-mainboard-r0.1.kicad_pcb'),source_commit=json.loads((repo/'docs/GITHUB_R144.json').read_text())['source_commit'],files=files,source_files_identical=68,fitted_parts=120,BOM_groups=len(bom),native_pads=473,vias=384,physical_tests='NOT RUN',fabrication_ready=False)
(p/'PACKET_MANIFEST_R144.json').write_text(json.dumps(record,indent=2)+'\n')
def archive(path,entries):
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for name,file in sorted(entries):z.write(file,name)
 with zipfile.ZipFile(path)as z:
  assert z.testzip()is None
  for name,file in entries:assert hashlib.sha256(z.read(name)).hexdigest()==sha(file)
full=out/'ENKU_Reader_Base_R144_PCBWay_Engineering_Review_NO_FAB.zip';archive(full,[(q.relative_to(p).as_posix(),q)for q in p.rglob('*')if q.is_file()])
fab=out/'ENKU_Reader_Base_R144_Gerber_Drill_IPC_NO_FAB.zip';subset=[(q.relative_to(p/'01_fabrication').as_posix(),q)for q in(p/'01_fabrication').rglob('*')if q.is_file()]+[('README_PCBWAY_R144_NO_FAB.md',p/'README_PCBWAY_R144_NO_FAB.md'),('U3_via_process_requests.csv',p/'02_assembly/U3_via_process_requests.csv'),('R28_via_process_request.csv',p/'02_assembly/R28_via_process_request.csv')];sm=out/'FAB_MANIFEST_R144.json';sm.write_text(json.dumps(dict(revision='R144',pcb_sha256=record['pcb_sha256'],fabrication_ready=False,files={n:dict(sha256=sha(q),bytes=q.stat().st_size)for n,q in subset}),indent=2)+'\n');archive(fab,subset+[('FAB_MANIFEST_R144.json',sm)])
for q in(p/'03_drawings').glob('*.pdf'):shutil.copy2(q,out/q.name)
shutil.copy2(p/'02_assembly/ENKU_R144_BOM_CPL_NO_FAB.xlsx',out)
result=dict(revision='R144',package_files=len(files)+1,source_files=68,BOM_groups=len(bom),CPL_parts=120,checks='PASS',files={q.name:dict(bytes=q.stat().st_size,sha256=sha(q))for q in out.iterdir()if q.suffix in ['.zip','.pdf','.xlsx']},physical_tests='NOT RUN',fabrication_ready=False);(out/'DELIVERABLES_R144.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
