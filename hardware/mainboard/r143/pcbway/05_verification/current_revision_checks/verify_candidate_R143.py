"""Read-only actual R143 review, with immutable R138 and R141 references."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
def main(root,out,canonical,reference):
 root,out,canonical,reference=[p.resolve()for p in [root,out,canonical,reference]];out.mkdir(parents=True,exist_ok=True);c=root/'checks';app=os.environ['ENKU_KICAD_APP'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();accepted='90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971';refsha='b656abcf65c55cdb425a09468ef379187b561e764ad1257d2b2761e4f95451fe'
 assert root!=canonical and not root.is_relative_to(canonical);assert sha(canonical/'enku-mainboard-r0.1.kicad_pcb')==accepted;assert sha(reference/'enku-mainboard-r0.1.kicad_pcb')==refsha
 source=sha(root/'enku-mainboard-r0.1.kicad_pcb');project=(root/'enku-mainboard-r0.1.kicad_pro').read_bytes();os.environ['KIPRJMOD']=str(root)
 def native(*args):subprocess.run([app,*map(str,args)],check=True,stdout=subprocess.DEVNULL)
 def python(name,*args):subprocess.run([sys.executable,str(c/name),str(root),str(out),*map(str,args)],check=True,stdout=subprocess.DEVNULL);print('PASS',name,flush=True)
 try:
  native('python3.11',c/'proposal_native_R143.py','preview',root,out)
  native('kicad-cli','sch','erc','--severity-all','--format','json','--output',out/'erc.json',root/'enku-mainboard-r0.1.kicad_sch')
  for folder,name in [(root,'netlist.xml'),(reference,'reference_R141_netlist.xml')]:
   os.environ['KIPRJMOD']=str(folder);native('kicad-cli','sch','export','netlist','--format','kicadxml','--output',out/name,folder/'enku-mainboard-r0.1.kicad_sch')
  os.environ['KIPRJMOD']=str(root)
  native('python3.11',c/'native_board.py','export',reference/'enku-mainboard-r0.1.kicad_pcb',out/'reference_R141_geometry.json')
  native('python3.11',c/'export_assembly_features.py',reference/'enku-mainboard-r0.1.kicad_pcb',out/'reference_R141_assembly.json')
  for name,filename in [('export_reference_planes.py','reference_planes_active.json.gz'),('export_via_process_R133.py','via_process_R138.json'),('export_thermal_planes_R133.py','thermal_planes_R138.json.gz'),('export_assembly_features.py','assembly_features.json'),('export_orientation_R130.py','orientation.json'),('export_silkscreen_R137.py','silkscreen_native_R138.json'),('audit_layers_R141.py','layer_visibility_audit_R143.json')]:native('python3.11',c/name,root/'enku-mainboard-r0.1.kicad_pcb',out/filename)
  native('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--output',out/'CPL.csv',root/'enku-mainboard-r0.1.kicad_pcb')
  for name,layer in [('F_Mask','F.Mask'),('F_Paste','F.Paste'),('B_Mask','B.Mask'),('B_Cu','B.Cu'),('F_Cu','F.Cu'),('B_Paste','B.Paste'),('In1_Cu','In1.Cu'),('In2_Cu','In2.Cu')]:native('kicad-cli','pcb','export','svg','--layers',layer,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','0','--output',out/(name+'.svg'),root/'enku-mainboard-r0.1.kicad_pcb')
 finally:(root/'enku-mainboard-r0.1.kicad_pro').write_bytes(project)
 assert sha(root/'enku-mainboard-r0.1.kicad_pcb')==source,'Verification changed source';(out/'source.kicad_pro').write_bytes(project)
 d=json.loads((out/'drc.json').read_text());e=json.loads((out/'erc.json').read_text());assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']and not any(s['violations']for s in e['sheets']);print('PASS native DRC/ERC/opens/parity zero',flush=True)
 guards=['audit_usb.py','audit_q1_pin_order_R138.py','audit_manufacturer_footprints_R136.py','audit_sw1_pin_map.py','audit_component_lands_R130.py','audit_U1_EP_grid_R130.py','audit_U1_plot_R130.py','audit_IC_stencil_R138.py','audit_intrinsic_holes_R136.py','audit_U3_thermal_R138.py','audit_switch_apertures_R136.py']
 for name in guards:python(name)
 for mode in ['connector','control']:python('audit_extension_R136.py',mode)
 scopes=['audit_electrical_R143.py','audit_active_IC_R143.py','audit_component_pass_R143.py','audit_assembly_R143.py','audit_power_budget_R143.py','audit_capacitance_R143.py']
 for name in scopes:python(name)
 subprocess.run([sys.executable,str(c/'audit_source_R143.py'),str(root),str(reference),str(out)],check=True)
 python('export_manufacturing_R143.py');python('audit_copper_R143.py');python('audit_exports_R143.py')
 import review_routing_R143 as review
 review.PCB_SHA=source;review.review(root,out,out/'routing');rp=out/'routing/routing_review_R140.json';j=json.loads(rp.read_text());j.update(audit_revision='R143',physical_revision='R143',accepted_checkpoint_updated=False);rp.write_text(json.dumps(j,indent=2)+'\n');assert all(a['both_inner_GND_centerline_gap_mm']<1e-8 for a in j['inventory']if a['category']=='FAST');print('PASS fast return ground geometry',flush=True)
 python('audit_Gerber_graph_R143.py')
 python('audit_requested_review_R143.py')
 assert sha(canonical/'enku-mainboard-r0.1.kicad_pcb')==accepted and sha(reference/'enku-mainboard-r0.1.kicad_pcb')==refsha and sha(root/'enku-mainboard-r0.1.kicad_pcb')==source
 report=dict(revision='R143',pcb_sha256=source,native_kicad='10.0.7',DRC=0,ERC=0,opens=0,parity=0,actual_source_guards=guards+scopes,canonical_R138_unchanged=True,reference_R141_unchanged=True,historical_goldens_regenerated=False,complete_copper_and_manufacturing_exports='PASS',independent_Gerber_connectivity_and_effective_open_short_faults='PASS',physical_qualification='NOT RUN',fabrication_ready=False)
 (out/'verification_R143.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS full R143 offline verification; NO FAB',flush=True)
if __name__=='__main__':main(*(Path(v)for v in sys.argv[1:5]))
