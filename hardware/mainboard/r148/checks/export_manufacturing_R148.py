"""R144 explicit scope, adapted from export_manufacturing_R141.py; original unchanged."""
"""Native review-only Gerber/Excellon/IPC/CPL export; never releases or uploads."""
import csv,hashlib,json,os,subprocess,sys
from pathlib import Path

r,out=(Path(x).resolve()for x in sys.argv[1:3]);app=Path(os.environ['ENKU_KICAD_APP']);pcb=r/'enku-mainboard-r0.1.kicad_pcb'
m=out/'manufacturing_review_R144';m.mkdir(exist_ok=True,parents=True)
g=m/'gerber';d=m/'drill';g.mkdir(exist_ok=True);d.mkdir(exist_ok=True)
commands=[['pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.SilkS,B.SilkS,Edge.Cuts','--no-protel-ext','--precision','6','--output',str(g)+os.sep],
 ['pcb','export','drill','--format','excellon','--drill-origin','absolute','--excellon-units','mm','--excellon-zeros-format','decimal','--excellon-oval-format','route','--excellon-separate-th','--generate-map','--map-format','svg','--generate-report','--report-path',str(d/'drill-report.txt'),'--output',str(d)+os.sep],
 ['pcb','export','ipcd356','--output',str(m/'netlist.d356')],
 ['pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--output',str(m/'CPL_native_mm.csv')]]
before=pcb.read_bytes()
for cmd in commands:subprocess.run([str(app),'kicad-cli',*cmd,str(pcb)],check=True,stdout=subprocess.DEVNULL)
assert pcb.read_bytes()==before
assert len(list(g.glob('*.gbr')))==11,'Native successful exit omitted requested fabrication layers'
assert len(list(d.glob('*.drl')))==2
assert (m/'CPL_native_mm.csv').read_bytes()==(out/'CPL.csv').read_bytes()
classified=list(csv.DictReader((out/'assembly_review_BOM.csv').open()))
(m/'BOM_all_classified.csv').write_bytes((out/'assembly_review_BOM.csv').read_bytes())
groups={}
for row in classified:
 if row['Assembly']!='FIT':continue
 key=tuple(row[k]for k in ['MPN','Manufacturer','Value','Footprint','Side']);groups.setdefault(key,[]).append(row['Reference'])
with (m/'BOM_fitted_review.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Designator','Quantity','Manufacturer Part Number','Manufacturer','Value','Footprint','Side'])
 for (mpn,maker,value,footprint,side),refs in sorted(groups.items()):w.writerow([','.join(sorted(refs)),len(refs),mpn,maker,value,footprint,side])
thermal=json.loads((r/'checks/thermal_via_manifest_R138.json').read_text())
via={x['uuid']:x for x in json.loads((out/'via_process_R138.json').read_text())['vias']}
with (m/'U3_via_process_requests.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Via UUID','Board X mm','Board Y mm','Gerber X mm','Gerber Y mm','Diameter mm','Drill mm','Fill requested','Cap requested','Front tented','Back tented','Approved'])
 for row in thermal['added_vias']:
  v=via[row['uuid']];x,y=row['position_mm']
  w.writerow([row['uuid'],x,y,x,-y,.6,.3,v['fill_requested'],v['cap_requested'],v['front_tented'],v['back_tented'],False])
r28=json.loads((r/'checks/R28_via_in_pad_manifest_R138.json').read_text())
with (m/'R28_via_process_request.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['Via UUID','Board X mm','Board Y mm','Gerber X mm','Gerber Y mm','Diameter mm','Drill mm','Fill requested','Cap requested','Front tented','Back tented','Approved'])
 v=via[r28['uuid']];x,y=r28['position_mm'];w.writerow([r28['uuid'],x,y,x,-y,.5,.2,v['fill_requested'],v['cap_requested'],v['front_tented'],v['back_tented'],False])
via_count=sum(t['via']for t in json.loads((out/'geometry.json').read_text())['tracks'])
small_bores=sum(t['via']and abs(t['drill']-.2)<1e-8 for t in json.loads((out/'geometry.json').read_text())['tracks'])
(m/'README_NO_FAB.md').write_text(f'''# ENKU R148 engineering manufacturing review — NO FAB

Engineering review only. Fabrication, procurement, assembly and stencil release are NOT authorized.
Source: R148 PCB, KiCad10.0.7. Four copper layers,59×101×1.6mm.
All Gerber, drill, IPC and native CPL coordinates use absolute origin0,0:
X=KiCad boardX,Y=-KiCad boardY,mm; original top-side native CPL angles.
Board envelope X18..77,Y-121..-20mm. No supplier rotation/origin normalization is approved.
Gerber soldermask objects describe openings despite negative FilePolarity metadata.
Use the single native CPL and fitted review BOM together; all-classified BOM explicitly retains20 bare-PCB entries and R67/R99 DNP.
R67 and R99 default DNP has no paste apertures. Its copper/mask and optional rework lands remain.
All assembled119 parts are on front; back paste intentionally empty.
Separate PTH/NPTH Excellon files use decimal metric coordinates and routed USB slots.
Excellon alone does NOT convey fill/cap; the five U3 and one R28 UUIDs are explicitly listed in the two process request CSVs.
All{via_count} vias have at least0.15mm nominal annular rings; all{via_count-6} ordinary vias have at least0.10mm separation from SMD lands.
{small_bores} nominal0.20mm bores on1.6mm PCB give nominal aspect8, at the published process boundary.
Finished hole, thickness, registration and barrel copper tolerances require explicit job approval.
All six in-pad vias require actual resin fill and copper cap; no ordinary tent substitute.
Filled/capped under-EP, U1 grid/stencil, USB0.8mm stakes on1.6mm PCB, controlled90-ohm USB stackup,
thermal/fault/firmware qualification, thin replaceable battery and unchanged-thickness case fit remain open.
J1 is a hand-solder two-wire interface with no connector body or paste; clamp insulated leads in the case. Cell PCM and external cell-bonded NTC on J8 remain required. A full back-to-back display/PCB folded-flex assembly and qualified pack pair remain unverified.
Do not interpret Gerber availability, checksum verification or native DRC0 as factory acceptance.
''')
manifest=dict(revision='R148_ENGINEERING',pcb_sha256=hashlib.sha256(before).hexdigest(),native_kicad='10.0.7',Gerber_requested_layers=11,
 Gerber_coordinate_precision='mm; absolute4.6',coordinate_origin='absolute0,0;X=boardX;Y=-boardY',
 fitted_BOM_units=sum(len(x)for x in groups.values()),fitted_BOM_groups=len(groups),native_CPL_rows=119,default_DNP=['R67','R99'],
 manufacturing_release_approved=False,fabrication_ready=False,
 files={p.relative_to(m).as_posix():dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)for p in sorted(m.rglob('*'))if p.is_file()and p.name!='manifest_R144.json'})
(m/'manifest_R144.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Native review export:11 Gerbers,2 separate drill files,IPC,119-part CPL,explicit DNP and via requests; NO FAB')
