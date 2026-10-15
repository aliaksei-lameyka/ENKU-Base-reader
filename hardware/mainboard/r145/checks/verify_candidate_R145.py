"""Read-only exact-source R145 acceptance; inherited R144 helper names retained. Proposal builders are never invoked."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
def main(root,out,reference,scope):
 root,out,reference,scope=map(lambda p:p.resolve(),[root,out,reference,scope]);out.mkdir(parents=True,exist_ok=True);c=root/'checks';app=os.environ['ENKU_KICAD_APP'];name='enku-mainboard-r0.1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected=json.loads(scope.read_text());source=sha(root/(name+'.kicad_pcb'));assert source==expected['current_pcb_sha256'];assert sha(reference/(name+'.kicad_pcb'))==expected['reference_R144_pcb_sha256'];before={p.relative_to(root).as_posix():sha(p)for p in root.rglob('*')if p.is_file()and'checks'not in p.parts and p.suffix not in ['.kicad_prl','.lck']};project=(root/(name+'.kicad_pro')).read_bytes();os.environ['KIPRJMOD']=str(root)
 def native(*args):subprocess.run([app,*map(str,args)],check=True,stdout=subprocess.DEVNULL)
 def python(script,*args):subprocess.run([sys.executable,str(c/script),str(root),str(out),*map(str,args)],check=True);print('PASS',script,flush=True)
 try:
  native('kicad-cli','pcb','drc','--severity-all','--all-track-errors','--schematic-parity','--refill-zones','--save-board','--format','json','--output',out/'drc.json',root/(name+'.kicad_pcb'))
  assert sha(root/(name+'.kicad_pcb'))==source,'Refill changed source'
  native('kicad-cli','sch','erc','--severity-all','--format','json','--output',out/'erc.json',root/(name+'.kicad_sch'))
  for folder,filename in [(root,'netlist.xml'),(reference,'reference_R144_netlist.xml')]:
   os.environ['KIPRJMOD']=str(folder);native('kicad-cli','sch','export','netlist','--format','kicadxml','--output',out/filename,folder/(name+'.kicad_sch'))
  os.environ['KIPRJMOD']=str(root)
  for folder,filename in [(root,'geometry.json'),(reference,'reference_R144_geometry.json')]:native('python3.11',c/'native_board.py','export',folder/(name+'.kicad_pcb'),out/filename)
  native('python3.11',c/'export_assembly_features.py',reference/(name+'.kicad_pcb'),out/'reference_R144_assembly.json')
  for script,filename in [('export_native_copper_R138.py','native_copper_R138.json.gz'),('export_reference_planes.py','reference_planes_active.json.gz'),('export_via_process_R133.py','via_process_R138.json'),('export_thermal_planes_R133.py','thermal_planes_R138.json.gz'),('export_assembly_features.py','assembly_features.json'),('export_orientation_R130.py','orientation.json'),('export_silkscreen_R137.py','silkscreen_native_R138.json'),('audit_layers_R141.py','layer_visibility_audit_R144.json')]:native('python3.11',c/script,root/(name+'.kicad_pcb'),out/filename)
  native('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--output',out/'CPL.csv',root/(name+'.kicad_pcb'))
  for short,layer in [('F_Mask','F.Mask'),('F_Paste','F.Paste'),('B_Mask','B.Mask'),('B_Cu','B.Cu'),('F_Cu','F.Cu'),('B_Paste','B.Paste'),('In1_Cu','In1.Cu'),('In2_Cu','In2.Cu')]:native('kicad-cli','pcb','export','svg','--layers',layer,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','--drill-shape-opt','0','--output',out/(short+'.svg'),root/(name+'.kicad_pcb'))
 finally:(root/(name+'.kicad_pro')).write_bytes(project)
 (out/'source_pcb.sha256').write_text(source+'  '+name+'.kicad_pcb\n');(out/'source.kicad_pro').write_bytes(project)
 d=json.loads((out/'drc.json').read_text());e=json.loads((out/'erc.json').read_text());assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']and not any(s['violations']for s in e['sheets']);lv=json.loads((out/'layer_visibility_audit_R144.json').read_text());assert not lv['unnamed_layers']and not lv['disabled_documentation_layers']and not lv['copper_graphics_without_net_semantics'];print('PASS native DRC/ERC/opens/parity zero and layer inventory',flush=True)
 python('audit_rule_engine_R144.py')
 guards=['audit_usb.py','audit_q1_pin_order_R138.py','audit_manufacturer_footprints_R136.py','audit_sw1_pin_map.py','audit_component_lands_R130.py','audit_U1_EP_grid_R130.py','audit_U1_plot_R130.py','audit_IC_stencil_R138.py','audit_intrinsic_holes_R136.py','audit_U3_thermal_R138.py','audit_switch_apertures_R136.py']
 for script in guards:python(script)
 for mode in ['connector','control']:python('audit_extension_R136.py',mode)
 for script in ['audit_startup_R144.py','audit_electrical_R144.py','audit_active_IC_R144.py','audit_component_pass_R144.py','audit_assembly_R144.py','audit_power_budget_R144.py','audit_capacitance_R144.py']:python(script)
 python('audit_source_R145.py',reference,scope)
 python('export_manufacturing_R144.py');python('audit_copper_R144.py');python('audit_exports_R145.py')
 import review_routing_R144 as review
 review.PCB_SHA=source;review.review(root,out,out/'routing');rp=out/'routing/routing_review_R140.json';j=json.loads(rp.read_text());j.update(audit_revision='R145',physical_revision='R145',accepted_checkpoint_updated=False);rp.write_text(json.dumps(j,indent=2)+'\n');assert all(a['both_inner_GND_centerline_gap_mm']<1e-8 for a in j['inventory']if a['category']=='FAST');print('PASS fast return ground geometry',flush=True)
 for script in ['audit_Gerber_graph_R144.py','audit_supervisor_OEM_R144.py','audit_requested_review_R144.py']:python(script)
 subprocess.run([sys.executable,str(c/'audit_connector_R145.py'),str(root),str(out),str(out),str(out/'manufacturing_review_R144/gerber'/f'{name}-F_Paste.gbr')],check=True)
 assert all(sha(root/p)==v for p,v in before.items());assert sha(reference/(name+'.kicad_pcb'))==expected['reference_R144_pcb_sha256']
 report=dict(revision='R145',pcb_sha256=source,native_kicad='10.0.7',DRC=0,ERC=0,opens=0,parity=0,complete_independent_manufacturing_checks='PASS',source_hashes_unchanged=True,reference_R144_unchanged=True,historical_goldens_regenerated=False,custom_rule_execution='PASS',independent_Gerber_connectivity_and_effective_open_short_faults='PASS',physical_qualification='NOT RUN',fabrication_ready=False)
 (out/'verification_R145.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS full R145 offline verification; NO FAB',flush=True)
if __name__=='__main__':main(*(Path(v)for v in sys.argv[1:5]))
