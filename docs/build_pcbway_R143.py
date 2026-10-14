"""Package actual R143 exports and evidence; no factory transfer or release."""
from pathlib import Path
import csv,json,hashlib,shutil,sys,zipfile
repo=Path(__file__).resolve().parents[1];v=Path(sys.argv[1]).resolve();r=repo/'hardware/mainboard/r143';p=r/'pcbway';p.mkdir(exist_ok=True)
for n in ['01_fabrication','02_assembly','03_drawings','04_editable_kicad','05_verification','06_qualification']:(p/n).mkdir(exist_ok=True)
m=v/'manufacturing_review_R143';shutil.copytree(m/'gerber',p/'01_fabrication/gerber',dirs_exist_ok=True);shutil.copytree(m/'drill',p/'01_fabrication/drill',dirs_exist_ok=True);shutil.copy2(m/'netlist.d356',p/'01_fabrication')
for n in ['BOM_all_classified.csv','BOM_fitted_review.csv','CPL_native_mm.csv','U3_via_process_requests.csv','R28_via_process_request.csv']:shutil.copy2(m/n,p/'02_assembly'/n)
shutil.copy2(m/'BOM_fitted_review.csv',p/'02_assembly/BOM_PCBWay_R143.csv')
rows=list(csv.DictReader((m/'CPL_native_mm.csv').open()))
with (p/'02_assembly/CPL_PCBWay_R143.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
 for a in rows:w.writerow([a['Ref'],float(a['PosX']),float(a['PosY']),'Top',float(a['Rot'])])
g=json.loads((v/'geometry.json').read_text());af=json.loads((v/'assembly_features.json').read_text());fit={a['Ref']for a in rows};pads=g['pads']
with (p/'02_assembly/Complete_pad_map_R143.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Reference','Pad','Net','Board X mm','Board Y mm','Gerber X mm','Gerber Y mm','Angle deg','Size X mm','Size Y mm','Drill X mm','Drill Y mm','Native attribute','Copper layer IDs','UUID'])
 for a in pads:w.writerow([a['ref'],a['number'],a['net'],*a['pos'],a['pos'][0],-a['pos'][1],a['angle'],*a['size'],*a['drill'],a['attribute'],','.join(map(str,a['layers'])),a['uuid']])
with (p/'02_assembly/Reference_first_pad_index_R143.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Reference','Fitted','Footprint','Board X mm','Board Y mm','Native top angle deg','First pad label','First pad X mm','First pad Y mm','Native angle is supplier-approved'])
 for ref,fp in sorted(g['footprints'].items()):
  pp=[a for a in pads if a['ref']==ref and a['number']];first=next((a for a in pp if a['number']=='1'),pp[0]if pp else None);w.writerow([ref,ref in fit,fp['lib'],*fp['pos'],fp['angle'],first['number']if first else'',*(first['pos']if first else['','']),False])
shutil.copytree(r/'kicad',p/'04_editable_kicad',dirs_exist_ok=True)
for q in v.rglob('*'):
 if not q.is_file()or 'manufacturing_review_R143'in q.parts:continue
 if q.suffix in ['.json','.gz','.xml','.csv','.sha256','.png']:dest=p/'05_verification'/q.relative_to(v);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(q,dest)
for n in ['PRE_REVIEW_CHECKS_R143.md','FCT_PLAN_R143.md','PCBWAY_MANUFACTURING_NOTES_R143.md','FPC_CONNECTOR_REVIEW_R143.md']:shutil.copy2(repo/'docs'/n,p/'06_qualification'/n)
for n in ['FPC_connector_audit_R143.json','J3_pin_map_R143.csv']:shutil.copy2(v/n,p/'05_verification'/n)
shutil.copy2(r/'checks/audit_connector_R143.py',p/'05_verification/audit_connector_R143.py')
shutil.copy2(repo/'docs/STARTUP_RISKS_R143.md',p/'06_qualification/STARTUP_RISKS_R143.md')
(p/'README_PCBWAY_R143_NO_FAB.md').write_text('''# ENKU Base R143 - preliminary PCBWay engineering review

**NO FAB.** Review inputs only. Source revision R143; native10.0.7;59x101x1.6mm, four copper layers.

01_fabrication contains11 Gerber layers, separate PTH/NPTH decimal metric drills, four routed USB shell slots, IPC356 and drill maps/report. No copper-only substitute.
02_assembly contains114 fitted top placements, grouped fitted BOM, all134 classified references including19 bare entries and R67 DNP, all453 native pad rows and first-pad index. Native and mapped CPL use X=board X and Y=-board Y in mm, absolute0,0 origin and original top angle. Supplier import/rotation approval is pending. R67 has no paste; B.Paste is empty.
03_drawings contains board review, ten layer/assembly pages and five schematic sheets. PDF imagery is explanatory; fabrication uses the actual Gerber/drill set.
04_editable_kicad is byte-identical to current R143 source.05_verification contains actual native and independent reports.06_qualification specifies remaining physical and manufacturer evidence.

Five U3 vias plus one R28 via require resin fill and copper cap with approved finish/flatness/voiding. CSV requests are not process acceptance; Excellon does not encode fill/cap.373 total vias,367 ordinary vias, nominal annular ring at least0.15mm.84 nominal0.20mm bores on1.6mm give nominal8:1 aspect before process tolerances. Approved stackup/90-ohm USB, stencil and USB short stake assembly remain open.

EVT BUILD BLOCKED: joint logic/panel nominal supply3.24549V has only8.195mV upper and10.727mV reset release static margin in PWM; actual MODE permits PFM. See STARTUP_RISKS_R143.md. Felix's10Oct reply closes pin5 VDHR=VSH2 and specifies bendR1-1.5mm/glass clearance>=2mm. All24 J3 contacts and signal lands/paste pass. S1/S2 copper and paste are corrected to OEM0.40x0.80mm. Guaranteed FPC thickness/width and finger/coverlay acceptance, folded pin1, GDEM/GDEY CAD identity and common J3 stencil/reflow process remain open; see FPC_CONNECTOR_REVIEW_R143.md. Protected battery PCM/NTC, case fit, firmware, SD/EPD/USB-MSC and physical tests remain open. No factory upload/order/payment or production firmware release has been made.

Check PACKET_MANIFEST_R143.json for source hash and exact per-file SHA256. Use only this revision's paired files; historical reports are comparison controls, not current factory inputs.
''')
print('Packaged current R143 source, fabrication, assembly and evidence')

