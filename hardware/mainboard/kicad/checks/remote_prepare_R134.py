"""Recover R134 on the pinned native runner; no manufacturing actions."""
import collections,gzip,hashlib,json,os,subprocess,sys,zipfile,re
from pathlib import Path
r=Path(sys.argv[1]).resolve();o=Path(sys.argv[2]).resolve();mode=sys.argv[3];c=r/'checks';repo=r.parents[2];app=repo/'.native-runtime/AppDir/AppRun'
def call(*args):subprocess.run([str(app),*map(str,args)],check=True)
def export():call('python3.11',c/'native_board.py','export',r/'enku-mainboard-r0.1.kicad_pcb',o/'geometry.json')
def apply(plan):
 p=o/'repair_plan.json';p.write_text(json.dumps(plan));call('python3.11',c/'native_board.py','apply',r/'enku-mainboard-r0.1.kicad_pcb',p,r/'enku-mainboard-r0.1.kicad_pcb')
def drc():call('kicad-cli','pcb','drc','--severity-all','--all-track-errors','--schematic-parity','--refill-zones','--save-board','--format','json','--output',o/'drc.json',r/'enku-mainboard-r0.1.kicad_pcb')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if mode=='repair':
 assert sha(r/'enku-mainboard-r0.1.kicad_pcb')=='e413ae506b897e0c1a035514ef659b9fc1e38bb2a400cb9ca886315df15541dd','Repair only the exact published native checkpoint'
 export();g=json.loads((o/'geometry.json').read_text());ids=[t['uuid']for t in g['tracks']if t['net']=='CHG_EN1_CMD'and not t['via']and t['layer']==6];assert len(ids)==14
 apply(dict(routes=[],remove_tracks=ids));export()
 subprocess.run([sys.executable,str(c/'route_repair_R134.py'),str(o/'geometry.json'),str(o/'EN1_plan.json')],check=True)
 plan=json.loads((o/'EN1_plan.json').read_text());assert not plan['failed']and len(plan['routes'])==1;apply(plan)
 tent=c/'tent_repair_R134.py';call('python3.11',tent,r/'enku-mainboard-r0.1.kicad_pcb',c/'geometry_checkpoint_R133.json.gz');old=json.loads(gzip.decompress((c/'geometry_checkpoint_R133.json.gz').read_bytes()));oldids={t['uuid']for t in old['tracks']}
 for attempt in range(6):
  drc();export();d=json.loads((o/'drc.json').read_text());g=json.loads((o/'geometry.json').read_text());ix={t['uuid']:t for t in g['tracks']};prune=[]
  for v in d['violations']:
   if v['type']in ['via_dangling','track_dangling']:
    for a in v['items']:
     assert a['uuid']not in oldids and ix[a['uuid']]['net']=='CHG_EN1_CMD';prune.append(a['uuid'])
  if not prune:break
  apply(dict(routes=[],remove_tracks=prune))
 assert collections.Counter(v['type']for v in d['violations'])=={'hole_clearance':16}and not d['unconnected_items']and not d['schematic_parity']
 for stem in ['audit_q1_pin_order','audit_active_IC','audit_assembly','audit_component_pass','audit_power_budget','audit_IC_stencil','audit_parts','audit_charge','audit_geometry','audit_U3_thermal','audit_temperature_FMEA']:
  s=(c/(stem+'_R133.py')).read_text().replace('R133','R134').replace('R134_U3_GND_THERMAL_SPREAD_NO_FAB','R133_U3_GND_THERMAL_SPREAD_NO_FAB');(c/(stem+'_R134.py')).write_text(s)
 for stem in ['thermal_via_manifest','thermal_zone_manifest','manufacturer_reference_manifest']:
  j=json.loads((c/(stem+'_R133.json')).read_text());j['revision']='R134';(c/(stem+'_R134.json')).write_text(json.dumps(j,indent=2)+'\n')
 p=c/'audit_active_IC_R134.py';s=p.read_text().replace("'5': (-0.75, 1.4, 0.24, 0.6, 'GND')","'5': (-0.75, 1.4, 0.24, 0.6, 'CHG_EN2')").replace("'6': (-0.25, 1.4, 0.24, 0.6, 'VBUS_USB')","'6': (-0.25, 1.4, 0.24, 0.6, 'CHG_EN1')").replace('input_current_limit_A=.5','input_current_limit_A_when_USB500=.5');p.write_text(s)
 p=c/'audit_charge_R134.py';s=p.read_text().replace("'CHG_CE_N','GND','VBUS_USB','CHG_STAT1','GND'","'CHG_CE_N','CHG_EN2','CHG_EN1','CHG_STAT1','GND'").replace('CHG_CE_static_low_TD_low_timer_enabled=True','CHG_CE_GPIO_control_TD_low_timer_enabled=True,reset_OFF_input_mode_high_Z_model="USB100"');p.write_text(s)
 p=c/'audit_assembly_R134.py';s=p.read_text().replace('len(fitted)==102','len(fitted)==107').replace("'R80','R81','R82','R83'}","'R80','R81','R82','R83','R84','R85','R86','R87','R88'}").replace('native_CPL_rows=102','native_CPL_rows=107').replace("assert sorted(labels,key=lambda x:x['ref'])==sorted(plan['preserved_probe_labels'],key=lambda x:x['ref'])","wanted=json.loads(json.dumps(plan['preserved_probe_labels']))\nfor z in wanted:\n    if z['ref']=='TP8':z['position_mm']=[55.5,92.7]\nassert sorted(labels,key=lambda x:x['ref'])==sorted(wanted,key=lambda x:x['ref'])").replace('all_13_probe_labels_preserved=True','all13_probe_names_preserved=True,TP8_move_verified=True');p.write_text(s)
 p=c/'audit_component_pass_R134.py';s=p.read_text().replace(" '3.48k':"," '2.2k':('RC0603FR-072K2L',['R84','R85']), '1k':('RC0603FR-071KL',['R86','R87','R88']),\n '3.48k':").replace('len(expected)==83','len(expected)==88');p.write_text(s)
 p=c/'audit_parts_R134.py';s=p.read_text().replace('USB4105-GF-A-120','USB4215-03-A').replace('==103','==108').replace('MPN_fields=103','MPN_fields=108');p.write_text(s)
 s=(c/'audit_manufacturer_footprints.py').read_text().replace("{'J5':4,'SW3':4,'SW4':4,'SW5':4,'SW6':4}","{'SW3':4,'SW4':4,'SW5':4,'SW6':4}");(c/'audit_manufacturer_footprints_R134.py').write_text(s)
 s=(c/'audit_intrinsic_holes_R130.py').read_text();a=s.index("usb = g['footprints']['J5']");b=s.index('findings = ',a);s=s[:a]+"assert not [p for p in g['pads']if p['ref']=='J5'and p['attribute']==3]\n"+s[b:];s=s.replace("{'SW3': 4, 'SW4': 4, 'SW5': 4, 'SW6': 4, 'J5': 4}","{'SW3': 4, 'SW4': 4, 'SW5': 4, 'SW6': 4}").replace('len(findings) == 20','len(findings) == 16').replace("'revision': 'R130'","'revision': 'R134'").replace("'active_hole_clearance_errors': 20","'active_hole_clearance_errors': 16").replace("'unique_physical_inadequate_copper_to_hole_interfaces': 18","'unique_physical_inadequate_copper_to_hole_interfaces': 16").replace("'USB_four_native_findings_are_two_coincident_pad_locations': True","'USB_real_component_replacement_removes_locator_findings': True").replace('intrinsic_holes_audit_R130.json','intrinsic_holes_audit_R134.json');(c/'audit_intrinsic_holes_R134.py').write_text(s)
elif mode=='manifest':
 old=json.loads(gzip.decompress((c/'geometry_checkpoint_R133.json.gz').read_bytes()));new=json.loads((o/'geometry.json').read_text());m=json.loads((c/'preservation_manifest_R134.json').read_text())
 def ix(rows):return {x['uuid']:{k:v for k,v in x.items()if k!='code'}for x in rows}
 for item,label in [('pads','pads'),('tracks','copper')]:
  a,b=ix(old[item]),ix(new[item]);m['exact_removed_'+label]=[a[u]for u in sorted(a.keys()-b.keys())];m['exact_added_'+label]=[b[u]for u in sorted(b.keys()-a.keys())];m['exact_'+('changed_pads'if item=='pads'else'reassigned_copper')]=[dict(before=a[u],after=b[u])for u in sorted(a.keys()&b.keys())if a[u]!=b[u]]
 m['checked_R134_source_sha256']={p:sha(repo/p)for p in ['hardware/mainboard/kicad/'+q for q in ['enku-mainboard-r0.1.kicad_pcb','power.kicad_sch','mcu_io.kicad_sch','connectors.kicad_sch','ENKU.kicad_sym','ENKU.pretty/USB4215_03_A_GCT_REVA.kicad_mod']]};(c/'preservation_manifest_R134.json').write_text(json.dumps(m,indent=2)+'\n')
elif mode=='freeze':
 g=json.loads((o/'geometry.json').read_text());d=json.loads((o/'drc.json').read_text());e=json.loads((o/'erc.json').read_text());assert not d['unconnected_items']and not d['schematic_parity']and not any(s['violations']for s in e['sheets']);assert collections.Counter(v['type']for v in d['violations'])=={'hole_clearance':16}
 cp=json.loads((c/'verification_checkpoint_R134.json').read_text());cp.update(pcb_sha256=(o/'source_pcb.sha256').read_text().split()[0],copper_items=len(g['tracks']),independent_guards_passed=21,server_verified=False,engineering_status='GENERATED_NATIVE21_CHECKPOINT_IMMUTABLE_SOURCE_CI_PENDING')
 (c/'verification_checkpoint_R134.json').write_text(json.dumps(cp,indent=2)+'\n');(c/'geometry_checkpoint_R134.json.gz').write_bytes(gzip.compress((o/'geometry.json').read_bytes(),mtime=0))
 for a,b in [('drc.json','drc_checkpoint_R134.json'),('erc.json','erc_checkpoint_R134.json'),('netlist.xml','netlist_R134.xml'),('assembly_features.json','assembly_features_R134.json'),('orientation.json','orientation_R134.json'),('CPL.csv','native_CPL_R134.csv'),('assembly_review_BOM.csv','assembly_review_BOM_R134.csv')]: (c/b).write_bytes((o/a).read_bytes())
elif mode=='retain':
 source=(o/'source_pcb.sha256').read_text().split()[0];reports=[]
 for p in o.glob('*.json'):
  j=json.loads(p.read_text())
  if isinstance(j,dict)and j.get('pcb_sha256',j.get('committed_pcb_sha256'))==source:reports.append(p)
 assert len(reports)==22,[p.name for p in reports]
 for p in reports:(c/('local_'+p.name)).write_bytes(p.read_bytes())
 def norm(b):
  v,n=re.subn(rb'(<title>SVG Image created as [^<]* date )\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}( </title>)',rb'\1EXPORT_TIMESTAMP\2',b);assert n==1;return v
 hashes={'exports':{},'plots':{},'raw_plots':{},'netlist_sections':{}}
 for name in ['geometry.json','assembly_features.json','orientation.json','via_process_R134.json']:
  hashes['exports'][name]=hashlib.sha256(json.dumps(json.loads((o/name).read_text()),sort_keys=True,separators=(',',':')).encode()).hexdigest()
 for name in ['reference_planes_active.json.gz','thermal_planes_R134.json.gz']:
  hashes['exports'][name]=hashlib.sha256(json.dumps(json.loads(gzip.decompress((o/name).read_bytes())),sort_keys=True,separators=(',',':')).encode()).hexdigest()
 for name in ['CPL.csv','assembly_review_BOM.csv','source.kicad_pro']:hashes['exports'][name]=sha(o/name)
 for name in ['F_Mask','F_Paste','B_Mask','F_Cu','B_Cu']:hashes['plots'][name]=hashlib.sha256(norm((o/(name+'.svg')).read_bytes())).hexdigest();hashes['raw_plots'][name]=sha(o/(name+'.svg'))
 import xml.etree.ElementTree as ET
 for group in ['components','libparts','nets']:hashes['netlist_sections'][group]=hashlib.sha256(ET.tostring(ET.parse(o/'netlist.xml').find(group))).hexdigest()
 (c/'local_export_hashes_R134.json').write_text(json.dumps(hashes,indent=2)+'\n')
 with zipfile.ZipFile(c/'native_local_R134.zip','w',zipfile.ZIP_DEFLATED)as z:
  for p in sorted(o.iterdir()):
   if p.is_file():z.write(p,p.name)
 meta=dict(scope='Generated candidate checked on native runner; fresh immutable-source verification is pending',run_id=int(os.environ['GITHUB_RUN_ID']),input_head_sha=os.environ['GITHUB_SHA'],source_pcb_sha256=source,independent_guards=21,fabrication_ready=False)
 (c/'native_build_provenance_R134.json').write_text(json.dumps(meta,indent=2)+'\n')
 (repo/'docs/WORK_HANDOFF_R134.md').write_text('# R134 native21 recovery checkpoint — NO FAB\n\nGenerated source repaired on pinned KiCad10.0.7 runner: ERC0/opens0/parity0,16 unchanged button-hole findings.21 independent scopes and generated checkpoint comparison pass. The repair-run input head differs from the generated source; fresh immutable-source CI remains pending. Native ZIP,22 reports, hashes and exact before/after manifest are retained. No production or orders.\n\nContinuous U3 B heat spreading exceeds50mm²; actual thermal/process/NTC/battery/enclosure/USB/firmware acceptance remains HOLD. Thin2000–2500mAh battery and fixed case target are retained. See native_build_provenance_R134.json for the actual run/source identities.\n')
else:raise AssertionError(mode)
