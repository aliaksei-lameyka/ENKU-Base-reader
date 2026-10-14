"""Immutable validation of an isolated actual R141 candidate, leaving R138 intact."""
import hashlib,json,os,subprocess,sys
from pathlib import Path

def main(root,out):
 root=root.resolve();out=out.resolve();out.mkdir(parents=True,exist_ok=True);canonical=Path(__file__).resolve().parents[1];c=canonical/'checks';app=os.environ['ENKU_KICAD_APP'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();accepted='90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971'
 assert root!=canonical and not root.is_relative_to(canonical);assert sha(canonical/'enku-mainboard-r0.1.kicad_pcb')==accepted
 source=sha(root/'enku-mainboard-r0.1.kicad_pcb');project=(root/'enku-mainboard-r0.1.kicad_pro').read_bytes();os.environ['KIPRJMOD']=str(root)
 def native(*args):subprocess.run([app,*map(str,args)],check=True,stdout=subprocess.DEVNULL)
 def python(name,*args):subprocess.run([sys.executable,str(c/name),str(root),str(out),*map(str,args)],check=True,stdout=subprocess.DEVNULL)
 try:
  native('python3.11',root/'checks/proposal_native_R141.py','preview',root,out)
  native('kicad-cli','sch','erc','--severity-all','--format','json','--output',out/'erc.json',root/'enku-mainboard-r0.1.kicad_sch')
  native('kicad-cli','sch','export','netlist','--format','kicadxml','--output',out/'netlist.xml',root/'enku-mainboard-r0.1.kicad_sch')
  for name,filename in [('export_reference_planes.py','reference_planes_active.json.gz'),('export_via_process_R133.py','via_process_R138.json'),('export_thermal_planes_R133.py','thermal_planes_R138.json.gz'),('export_assembly_features.py','assembly_features.json'),('export_orientation_R130.py','orientation.json'),('export_silkscreen_R137.py','silkscreen_native_R138.json')]:native('python3.11',c/name,root/'enku-mainboard-r0.1.kicad_pcb',out/filename)
  native('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--output',out/'CPL.csv',root/'enku-mainboard-r0.1.kicad_pcb')
  for name,layer in [('F_Mask','F.Mask'),('F_Paste','F.Paste'),('B_Mask','B.Mask'),('B_Cu','B.Cu'),('F_Cu','F.Cu'),('B_Paste','B.Paste'),('In1_Cu','In1.Cu'),('In2_Cu','In2.Cu')]:native('kicad-cli','pcb','export','svg','--layers',layer,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','0','--output',out/(name+'.svg'),root/'enku-mainboard-r0.1.kicad_pcb')
 finally:(root/'enku-mainboard-r0.1.kicad_pro').write_bytes(project)
 assert sha(root/'enku-mainboard-r0.1.kicad_pcb')==source,'Verification changed proposed source';(out/'source.kicad_pro').write_bytes(project)
 d=json.loads((out/'drc.json').read_text());e=json.loads((out/'erc.json').read_text());assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']and not any(s['violations']for s in e['sheets'])
 guards=['audit_usb.py','audit_q1_pin_order_R138.py','audit_manufacturer_footprints_R136.py','audit_sw1_pin_map.py','audit_active_IC_R136.py','audit_assembly_R137.py','audit_component_lands_R130.py','audit_component_pass_R137.py','audit_power_budget_R136.py','audit_U1_EP_grid_R130.py','audit_U1_plot_R130.py','audit_IC_stencil_R138.py','audit_intrinsic_holes_R136.py','audit_charge_R136.py','audit_U3_thermal_R138.py','audit_temperature_FMEA_R136.py','audit_switch_apertures_R136.py','audit_capacitance_R136.py']
 for name in guards:python(name);print('PASS inherited actual-source guard',name,flush=True)
 for mode in ['connector','control']:python('audit_extension_R136.py',mode);print('PASS extension',mode,flush=True)
 python('export_manufacturing_R141.py');subprocess.run([sys.executable,str(c/'audit_proposal_R141.py'),str(root),str(canonical),str(out)],check=True);python('audit_exports_R141.py')
 import review_routing_R140 as review
 review.PCB_SHA=source;review.review(root,out,out/'routing');rp=out/'routing/routing_review_R140.json';j=json.loads(rp.read_text());j.update(audit_revision='R141',physical_revision='R141_PROPOSED',physical_source_modified=True,accepted_checkpoint_updated=False);rp.write_text(json.dumps(j,indent=2)+'\n')
 assert all(r['both_inner_GND_centerline_gap_mm']<1e-8 for r in j['inventory']if r['category']=='FAST'),'Fast trace lacks both ground planes'
 assert sha(canonical/'enku-mainboard-r0.1.kicad_pcb')==accepted
 report=dict(revision='R141_PROPOSED',pcb_sha256=source,native_kicad='10.0.7',DRC=0,ERC=0,opens=0,parity=0,actual_source_inherited_guards_passed=guards+['extension connector','extension control'],invariant_and_independent_complete_four_copper_images='PASS',independent_11_layer_drill_IPC_mask_paste_BOM_CPL='PASS',accepted_canonical_R138_source_unchanged=True,old_checkpoints_regenerated=False,physical_qualification='NOT RUN',fabrication_ready=False)
 (out/'verification_R141.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS full actual-source R141 verification and exports; NO FAB',flush=True)
if __name__=='__main__':main(*(Path(v)for v in sys.argv[1:3]))
