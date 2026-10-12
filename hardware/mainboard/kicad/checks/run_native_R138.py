"""Exact native R138 export/audit suite. Freeze is explicit local preparation only."""
import collections,gzip,hashlib,json,os,subprocess,sys,zipfile,re
from pathlib import Path
r=Path(sys.argv[1]).resolve();o=Path(sys.argv[2]).resolve();o.mkdir(exist_ok=True,parents=True);c=r/'checks';repo=r.parents[2];app=Path(os.environ.get('ENKU_KICAD_APP',str(repo/'.native-runtime/AppDir/AppRun')));freeze='--freeze'in sys.argv
if freeze and os.environ.get('GITHUB_ACTIONS')=='true':raise SystemExit('CI must verify immutable baselines; freeze is forbidden')
os.environ['KIPRJMOD']=str(r)
os.environ['ENKU_KICAD_APP']=str(app)
def call(*a):subprocess.run([str(app),*map(str,a)],check=True,stdout=subprocess.DEVNULL)
def audit(name,*a):subprocess.run([sys.executable,str(c/name),str(r),str(o),*a],check=True,stdout=subprocess.DEVNULL);print('PASS',name,*a,flush=True)
pcb=r/'enku-mainboard-r0.1.kicad_pcb';project=(r/'enku-mainboard-r0.1.kicad_pro').read_bytes();source=hashlib.sha256(pcb.read_bytes()).hexdigest();(o/'source_pcb.sha256').write_text(source+'  enku-mainboard-r0.1.kicad_pcb\n');(o/'source.kicad_pro').write_bytes(project)
version=subprocess.check_output([str(app),'kicad-cli','version']).decode().strip();assert version=='10.0.7';(o/'version.txt').write_text(version+'\n')
try:
 call('kicad-cli','pcb','drc','--severity-all','--all-track-errors','--schematic-parity','--refill-zones','--save-board','--format','json','--output',o/'drc.json',pcb)
 call('python3.11',c/'native_board.py','export',pcb,o/'geometry.json')
 call('kicad-cli','sch','erc','--severity-all','--format','json','--output',o/'erc.json',r/'enku-mainboard-r0.1.kicad_sch')
 call('kicad-cli','sch','export','netlist','--format','kicadxml','--output',o/'netlist.xml',r/'enku-mainboard-r0.1.kicad_sch')
 for name,out in [('export_reference_planes.py','reference_planes_active.json.gz'),('export_via_process_R133.py','via_process_R138.json'),('export_thermal_planes_R133.py','thermal_planes_R138.json.gz'),('export_assembly_features.py','assembly_features.json'),('export_orientation_R130.py','orientation.json')]:call('python3.11',c/name,pcb,o/out)
 call('python3.11',c/'export_silkscreen_R137.py',pcb,o/'silkscreen_native_R138.json')
 call('python3.11',c/'export_native_copper_R138.py',pcb,o/'native_copper_R138.json.gz')
 call('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--output',o/'CPL.csv',pcb)
 for name,layer in [('F_Mask','F.Mask'),('F_Paste','F.Paste'),('B_Mask','B.Mask'),('B_Cu','B.Cu'),('F_Cu','F.Cu'),('B_Paste','B.Paste'),('In1_Cu','In1.Cu'),('In2_Cu','In2.Cu')]:call('kicad-cli','pcb','export','svg','--layers',layer,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','0','--output',o/(name+'.svg'),pcb)
finally:
 (r/'enku-mainboard-r0.1.kicad_pro').write_bytes(project)
assert hashlib.sha256(pcb.read_bytes()).hexdigest()==source,'Native refill changed the committed source'
if freeze and not (c/'verification_checkpoint_R138.json').exists():
 # This preparation placeholder is intentionally rejected by the dispatcher.
 # Only a fully passing local suite below may record27 reviewed guards.
 (c/'verification_checkpoint_R138.json').write_text(json.dumps(dict(revision='R138',pcb_sha256=source,native_kicad=version,drc_types={},independent_guards_passed=0,server_verified=False,fabrication_ready=False),indent=2)+'\n')
guards=['audit_usb.py','audit_geometry_R138.py','audit_q1_pin_order_R138.py','audit_manufacturer_footprints_R136.py','audit_sw1_pin_map.py','audit_active_IC_R136.py','audit_assembly_R137.py','audit_component_lands_R130.py','audit_component_pass_R137.py','audit_power_budget_R136.py','audit_U1_EP_grid_R130.py','audit_U1_plot_R130.py','audit_IC_stencil_R138.py','audit_intrinsic_holes_R136.py','audit_parts_R138.py','audit_charge_R136.py','audit_source_R138.py','audit_U3_thermal_R138.py','audit_temperature_FMEA_R136.py','audit_switch_apertures_R136.py','audit_capacitance_R136.py']
for name in guards:audit(name)
for mode in ['connector','control']:audit('audit_extension_R136.py',mode)
subprocess.run([sys.executable,str(c/'export_manufacturing_R138.py'),str(r),str(o)],check=True)
if freeze and not (c/'copper_Gerber_baseline_R138.json').exists():
 from full_copper_R138 import normalize_copper
 baseline=dict(revision='R138',native_kicad=version,pcb_sha256=source,only_creation_timestamps_normalized=True,normalized_copper_sha256={key:hashlib.sha256(normalize_copper((o/'manufacturing_review_R138/gerber'/('enku-mainboard-r0.1-'+key+'.gbr')).read_bytes())).hexdigest()for key in ['F_Cu','In1_Cu','In2_Cu','B_Cu']},fabrication_ready=False)
 (c/'copper_Gerber_baseline_R138.json').write_text(json.dumps(baseline,indent=2)+'\n')
for name in ['audit_silkscreen_R138.py','audit_exports_R138.py','audit_annular_R138.py','audit_copper_R138.py']:audit(name)
g=json.loads((o/'geometry.json').read_text());d=json.loads((o/'drc.json').read_text());e=json.loads((o/'erc.json').read_text());assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']and not any(s['violations']for s in e['sheets'])
if freeze:
 cp=dict(revision='R138',native_kicad=version,pcb_sha256=source,opens=0,erc=0,parity=0,drc_types={},pads=len(g['pads']),footprints=len(g['footprints']),copper_items=len(g['tracks']),independent_guards_passed=27,server_verified=False,fabrication_ready=False)
 (c/'verification_checkpoint_R138.json').write_text(json.dumps(cp,indent=2)+'\n');(c/'geometry_checkpoint_R138.json.gz').write_bytes(gzip.compress((o/'geometry.json').read_bytes(),mtime=0))
 for a,b in [('drc.json','drc_checkpoint_R138.json'),('erc.json','erc_checkpoint_R138.json'),('netlist.xml','netlist_R138.xml'),('assembly_features.json','assembly_features_R138.json'),('orientation.json','orientation_R138.json'),('CPL.csv','native_CPL_R138.csv'),('assembly_review_BOM.csv','assembly_review_BOM_R138.csv')]:(c/b).write_bytes((o/a).read_bytes())
audit('verify_native_checkpoint.py')
if freeze:
 reports=[]
 for p in o.glob('*.json'):
  j=json.loads(p.read_text())
  if isinstance(j,dict)and j.get('pcb_sha256',j.get('committed_pcb_sha256'))==source:(c/('local_R138_'+p.name)).write_bytes(p.read_bytes());reports.append(p.name)
 assert len(reports)==28,reports
 with zipfile.ZipFile(c/'native_local_R138.zip','w',zipfile.ZIP_DEFLATED)as z:
  for p in sorted(o.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(o).as_posix())
print('PASS R138 full native0,27 independent scopes and checkpoint comparison; NO FAB',flush=True)
