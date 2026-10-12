"""Exact native R135 export/audit suite. Freeze is explicit local preparation only."""
import collections,gzip,hashlib,json,os,subprocess,sys,zipfile,re
from pathlib import Path
r=Path(sys.argv[1]).resolve();o=Path(sys.argv[2]).resolve();o.mkdir(exist_ok=True,parents=True);c=r/'checks';repo=r.parents[2];app=Path(os.environ.get('ENKU_KICAD_APP',str(repo/'.native-runtime/AppDir/AppRun')));freeze='--freeze'in sys.argv
os.environ['KIPRJMOD']=str(r)
def call(*a):subprocess.run([str(app),*map(str,a)],check=True,stdout=subprocess.DEVNULL)
def audit(name,*a):subprocess.run([sys.executable,str(c/name),str(r),str(o),*a],check=True,stdout=subprocess.DEVNULL);print('PASS',name,*a,flush=True)
pcb=r/'enku-mainboard-r0.1.kicad_pcb';project=(r/'enku-mainboard-r0.1.kicad_pro').read_bytes();source=hashlib.sha256(pcb.read_bytes()).hexdigest();(o/'source_pcb.sha256').write_text(source+'  enku-mainboard-r0.1.kicad_pcb\n');(o/'source.kicad_pro').write_bytes(project)
version=subprocess.check_output([str(app),'kicad-cli','version']).decode().strip();assert version=='10.0.7';(o/'version.txt').write_text(version+'\n')
call('kicad-cli','pcb','drc','--severity-all','--all-track-errors','--schematic-parity','--refill-zones','--save-board','--format','json','--output',o/'drc.json',pcb)
call('python3.11',c/'native_board.py','export',pcb,o/'geometry.json')
call('kicad-cli','sch','erc','--severity-all','--format','json','--output',o/'erc.json',r/'enku-mainboard-r0.1.kicad_sch')
call('kicad-cli','sch','export','netlist','--format','kicadxml','--output',o/'netlist.xml',r/'enku-mainboard-r0.1.kicad_sch')
for name,out in [('export_reference_planes.py','reference_planes_active.json.gz'),('export_via_process_R133.py','via_process_R135.json'),('export_thermal_planes_R133.py','thermal_planes_R135.json.gz'),('export_assembly_features.py','assembly_features.json'),('export_orientation_R130.py','orientation.json')]:call('python3.11',c/name,pcb,o/out)
call('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--output',o/'CPL.csv',pcb)
for name,layer in [('F_Mask','F.Mask'),('F_Paste','F.Paste'),('B_Mask','B.Mask'),('B_Cu','B.Cu'),('F_Cu','F.Cu')]:call('kicad-cli','pcb','export','svg','--layers',layer,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','0','--output',o/(name+'.svg'),pcb)
(r/'enku-mainboard-r0.1.kicad_pro').write_bytes(project);assert hashlib.sha256(pcb.read_bytes()).hexdigest()==source,'Native refill changed the committed source'
guards=['audit_usb.py','audit_geometry_R135.py','audit_q1_pin_order_R135.py','audit_manufacturer_footprints_R135.py','audit_sw1_pin_map.py','audit_active_IC_R135.py','audit_assembly_R135.py','audit_component_lands_R130.py','audit_component_pass_R135.py','audit_power_budget_R135.py','audit_U1_EP_grid_R130.py','audit_U1_plot_R130.py','audit_IC_stencil_R135.py','audit_intrinsic_holes_R135.py','audit_parts_R135.py','audit_charge_R135.py','audit_source_R135.py','audit_U3_thermal_R135.py','audit_temperature_FMEA_R135.py','audit_switch_apertures_R135.py']
for name in guards:audit(name)
for mode in ['connector','control']:audit('audit_extension_R135.py',mode)
g=json.loads((o/'geometry.json').read_text());d=json.loads((o/'drc.json').read_text());e=json.loads((o/'erc.json').read_text());assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']and not any(s['violations']for s in e['sheets'])
if freeze:
 cp=dict(revision='R135',native_kicad=version,pcb_sha256=source,opens=0,erc=0,parity=0,drc_types={},pads=len(g['pads']),footprints=len(g['footprints']),copper_items=len(g['tracks']),independent_guards_passed=22,server_verified=False,fabrication_ready=False)
 (c/'verification_checkpoint_R135.json').write_text(json.dumps(cp,indent=2)+'\n');(c/'geometry_checkpoint_R135.json.gz').write_bytes(gzip.compress((o/'geometry.json').read_bytes(),mtime=0))
 for a,b in [('drc.json','drc_checkpoint_R135.json'),('erc.json','erc_checkpoint_R135.json'),('netlist.xml','netlist_R135.xml'),('assembly_features.json','assembly_features_R135.json'),('orientation.json','orientation_R135.json'),('CPL.csv','native_CPL_R135.csv'),('assembly_review_BOM.csv','assembly_review_BOM_R135.csv')]:(c/b).write_bytes((o/a).read_bytes())
audit('verify_native_checkpoint.py')
if freeze:
 reports=[]
 for p in o.glob('*.json'):
  j=json.loads(p.read_text())
  if isinstance(j,dict)and j.get('pcb_sha256',j.get('committed_pcb_sha256'))==source:(c/('local_R135_'+p.name)).write_bytes(p.read_bytes());reports.append(p.name)
 assert len(reports)==23,reports
 with zipfile.ZipFile(c/'native_local_R135.zip','w',zipfile.ZIP_DEFLATED)as z:
  for p in sorted(o.iterdir()):
   if p.is_file():z.write(p,p.name)
print('PASS R135 full native0,22 independent scopes and checkpoint comparison; NO FAB',flush=True)
