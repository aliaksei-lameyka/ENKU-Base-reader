"""Package actual R144 exports and evidence; no factory transfer or release."""
from pathlib import Path
import csv,json,hashlib,shutil,sys,zipfile
repo=Path(__file__).resolve().parents[1];v=Path(sys.argv[1]).resolve();r=repo/'hardware/mainboard/r144';p=r/'pcbway';p.mkdir(exist_ok=True)
for n in ['01_fabrication','02_assembly','03_drawings','04_editable_kicad','05_verification','06_qualification']:(p/n).mkdir(exist_ok=True)
m=v/'manufacturing_review_R144';shutil.copytree(m/'gerber',p/'01_fabrication/gerber',dirs_exist_ok=True);shutil.copytree(m/'drill',p/'01_fabrication/drill',dirs_exist_ok=True);shutil.copy2(m/'netlist.d356',p/'01_fabrication')
for n in ['BOM_all_classified.csv','BOM_fitted_review.csv','CPL_native_mm.csv','U3_via_process_requests.csv','R28_via_process_request.csv']:shutil.copy2(m/n,p/'02_assembly'/n)
shutil.copy2(m/'BOM_fitted_review.csv',p/'02_assembly/BOM_PCBWay_R144.csv')
rows=list(csv.DictReader((m/'CPL_native_mm.csv').open()))
with (p/'02_assembly/CPL_PCBWay_R144.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
 for a in rows:w.writerow([a['Ref'],float(a['PosX']),float(a['PosY']),'Top',float(a['Rot'])])
g=json.loads((v/'geometry.json').read_text());af=json.loads((v/'assembly_features.json').read_text());fit={a['Ref']for a in rows};pads=g['pads']
with (p/'02_assembly/Complete_pad_map_R144.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Reference','Pad','Net','Board X mm','Board Y mm','Gerber X mm','Gerber Y mm','Angle deg','Size X mm','Size Y mm','Drill X mm','Drill Y mm','Native attribute','Copper layer IDs','UUID'])
 for a in pads:w.writerow([a['ref'],a['number'],a['net'],*a['pos'],a['pos'][0],-a['pos'][1],a['angle'],*a['size'],*a['drill'],a['attribute'],','.join(map(str,a['layers'])),a['uuid']])
with (p/'02_assembly/Reference_first_pad_index_R144.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Reference','Fitted','Footprint','Board X mm','Board Y mm','Native top angle deg','First pad label','First pad X mm','First pad Y mm','Native angle is supplier-approved'])
 for ref,fp in sorted(g['footprints'].items()):
  pp=[a for a in pads if a['ref']==ref and a['number']];first=next((a for a in pp if a['number']=='1'),pp[0]if pp else None);w.writerow([ref,ref in fit,fp['lib'],*fp['pos'],fp['angle'],first['number']if first else'',*(first['pos']if first else['','']),False])
shutil.copytree(r/'kicad',p/'04_editable_kicad',dirs_exist_ok=True)
for q in v.rglob('*'):
 if not q.is_file()or 'manufacturing_review_R144'in q.parts or q.name in ['geometry.json','assembly_features.json','reference_R143_geometry.json','reference_R143_assembly.json','reference_R143_netlist.xml','netlist.xml']:continue
 if q.suffix in ['.json','.gz','.xml','.csv','.sha256','.png']:dest=p/'05_verification'/q.relative_to(v);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(q,dest)
for n in ['PRE_REVIEW_CHECKS_R144.md','FCT_PLAN_R144.md','PCBWAY_MANUFACTURING_NOTES_R144.md','FPC_CONNECTOR_REVIEW_R144.md']:shutil.copy2(repo/'docs'/n,p/'06_qualification'/n)
for n in ['FPC_connector_audit_R144.json','J3_pin_map_R144.csv']:shutil.copy2(v/n,p/'05_verification'/n)
shutil.copy2(r/'checks/audit_connector_R144.py',p/'05_verification/audit_connector_R144.py')
shutil.copy2(repo/'docs/STARTUP_RISKS_R144.md',p/'06_qualification/STARTUP_RISKS_R144.md')
for n in ['REPORT_CLARIFICATIONS_R144.md','GITHUB_R144.json']:
 shutil.copy2(repo/'docs'/n,p/'06_qualification'/n)
shutil.copy2(r/'scope_R144.json',p/'05_verification')
shutil.copy2(r/'source_manifest_R144.json',p/'05_verification')
shutil.copytree(r/'checks',p/'05_verification/R144_checks',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
(p/'README_PCBWAY_R144_NO_FAB.md').write_text((r/'README_PACKET_R144.md').read_text())
print('Packaged current R144 source, fabrication, assembly and evidence')

shutil.copy2(v.parent.parent/'R144_actual_server_verification.zip',p/'05_verification/R144_actual_server_verification.zip')
