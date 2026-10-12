"""Independent R134 primary connector/control and exact-preservation scopes."""
import collections,gzip,hashlib,itertools,json,math,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import Polygon,Point,box
from shapely.ops import unary_union
from pad_groups import partitions,assert_no_split
from native_svg_shapes_R130 import actual_shapes
from cad_text_R134 import symbol,pins
r,o=map(lambda x:Path(x).resolve(),sys.argv[1:3]);mode=sys.argv[3];c=r/'checks';repo=r.parents[2]
g=json.loads((o/'geometry.json').read_text());af=json.loads((o/'assembly_features.json').read_text());fps={x['ref']:x for x in af['footprints']};ap={x['uuid']:x for x in af['pads']};xml=ET.parse(o/'netlist.xml');nodes={(a.attrib['ref'],a.attrib['pin']):n.attrib['name']for n in xml.findall('./nets/net')for a in n.findall('node')};groups=partitions(g);sha=(o/'source_pcb.sha256').read_text().split()[0]
if mode=='connector':
 f=g['footprints']['J5'];assert f['pos']==[47,117.325]and f['angle']==0 and  f['lib']=='ENKU:USB4215_03_A_GCT_REVA';assert fps['J5']['fields']['MPN']=='USB4215-03-A'
 expected={'A1':(-3.2,'GND'),'B12':(-3.2,'GND'),'A4':(-2.4,'VBUS_USB'),'B9':(-2.4,'VBUS_USB'),'B8':(-1.75,None),'A5':(-1.25,'USB_CC1'),'B7':(-.75,'USB_DM_CONN'),'A6':(-.25,'USB_DP_CONN'),'A7':(.25,'USB_DM_CONN'),'B6':(.75,'USB_DP_CONN'),'A8':(1.25,None),'B5':(1.75,'USB_CC2'),'A9':(2.4,'VBUS_USB'),'B4':(2.4,'VBUS_USB'),'A12':(3.2,'GND'),'B1':(3.2,'GND')}
 ps=[p for p in g['pads']if p['ref']=='J5'];smd={p['number']:p for p in ps if p['attribute']==1};shell=[p for p in ps if p['number']=='S'];assert len(ps)==20 and  smd.keys()==expected.keys()and len(shell)==4 and  not any(p['attribute']==3 for p in ps)
 for n,(x,net)in expected.items():
  p=smd[n];w=.6 if n in {'A1','B12','A4','B9','A9','B4','A12','B1'}else .3;assert p['pos']==[round(47+x,6),114.325]and p['size']==[w,1.15]and p['shape']==1 and  p['angle']==0 and  p['drill']==[0,0]and p['layers']==[0]
  a=ap[p['uuid']];assert set(a['layers'])=={'F.Cu','F.Mask','F.Paste'}and not a['local_mask_margin_IU']and not a['local_paste_margin_IU']and not a['local_paste_ratio'];assert p['net']==nodes[('J5',n)]
  if net is None:assert p['net'].startswith('unconnected-')and not any(t['net']==p['net']for t in g['tracks'])
  else:assert p['net']==net and len(groups[net])==1
 for p in shell:
  x,y=p['pos'];front=y==118.9;assert x in [42.68,51.32]and y in [114.9,118.9]and p['size']==[1,2.2 if front else 1.8]and p['drill']==[.6,1.8 if front else 1.4]and p['shape']==2 and  p['attribute']==0 and  p['net']=='USB_SHIELD';assert not any('Paste'in l for l in ap[p['uuid']]['layers'])
 ox,oy=g['bbox'][:2];roi=box(43.35-ox,113.65-oy,50.65-ox,114.98-oy);target=unary_union([box(p['pos'][0]-p['size'][0]/2-ox,p['pos'][1]-p['size'][1]/2-oy,p['pos'][0]+p['size'][0]/2-ox,p['pos'][1]+p['size'][1]/2-oy)for p in smd.values()]);assert len(target.geoms)==12;plots={}
 for layer in ['F_Mask','F_Paste']:
  p=o/(layer+'.svg');actual=unary_union(actual_shapes(p,roi));assert actual.symmetric_difference(target).area<.0001 and  len(actual.geoms)==12
  norm,count=re.subn(rb'(<title>SVG Image created as [^<]* date )\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}( </title>)',rb'\1EXPORT_TIMESTAMP\2',p.read_bytes());assert count==1;plots[layer]=dict(physical_openings=12,area_mm2=actual.area,normalized_plot_sha256=hashlib.sha256(norm).hexdigest())
 assert re.search(r'\(thickness 1\.6\)',(r/'enku-mainboard-r0.1.kicad_pcb').read_text())
 report=dict(revision='R134',pcb_sha256=sha,primary_GCT_RevA26Apr2024_drawing_SHA256='1659ba00769b9b774a033fac72cb2f3bfc481a3272c53f34e87520f33635a9e1',MPN='USB4215-03-A',nominal_height_mm=3.16,mating_face_y_mm=121,real_locator_holes=0,actual_apertures=plots,short_stake_assembly_enclosure_and_impedance_qualified=False,fabrication_ready=False);name='USB_connector_audit_R134.json'
elif mode=='control':
 wanted={'CHG_EN1_CMD':{('U1','9'),('R86','1')},'CHG_EN2_CMD':{('U1','38'),('R87','1')},'CHG_CE_CMD':{('U1','31'),('R88','1')},'CHG_EN1':{('U3','6'),('R86','2'),('R84','1')},'CHG_EN2':{('U3','5'),('R87','2'),('R85','1')},'CHG_CE_N':{('U3','4'),('R88','2'),('R10','1')}}
 ns={n.attrib['name']:{(a.attrib['ref'],a.attrib['pin'])for a in n.findall('node')}for n in xml.findall('./nets/net')}
 for n,v in wanted.items():assert ns[n]==v and {(p['ref'],p['number'])for p in g['pads']if p['net']==n}==v and len(groups[n])==1
 for ref,val,mpn in [('R84','2.2k 1%','RC0603FR-072K2L'),('R85','2.2k 1%','RC0603FR-072K2L'),('R86','1k 1%','RC0603FR-071KL'),('R87','1k 1%','RC0603FR-071KL'),('R88','1k 1%','RC0603FR-071KL')]:
  assert fps[ref]['value']==val and fps[ref]['fields']['MPN']==mpn and not fps[ref]['dnp'];assert g['footprints'][ref]['lib']=='ENKU:R_RC0603_YAGEO_REFLOW';ps=[p for p in g['pads']if p['ref']==ref];assert len(ps)==2 and  all(p['size']==[.9,.8]and p['layers']==[0]and p['drill']==[0,0]for p in ps)
 assert nodes[('R84','2')]==nodes[('R85','2')]==nodes[('U3','8')]==nodes[('U3','17')]=='GND';assert nodes[('U3','13')]=='VBUS_USB'
 for text,n,cache in [((r/'ENKU.kicad_sym').read_text(),'BQ24072T_RGT',False),((r/'power.kicad_sch').read_text(),'ENKU:BQ24072T_RGT',True)]:
  _,_,s=symbol(text,n,cache);p=pins(s)
  for num,label,kind in [('5','EN2','input'),('6','EN1','input'),('8','VSS','passive'),('4','CE_N','input')]:assert '(name "'+label+'"'in p[num][2]and p[num][2].startswith('(pin '+kind+' ')
 def model(pd):
  h=[];l=[]
  for v,s,p in itertools.product([3,3.6],[990,1010],[pd*.99,pd*1.01]):h.append((.8*v-1e-5*s)/(1+s/p));l.append((.1*v+1e-6*s)/(1+s/p))
  return dict(conditional_high_min_V=min(h),conditional_low_max_V=max(l),high_Z_max_V=1e-6*pd*1.01)
 models={'EN':model(2200),'CE':model(100000)};assert all(x['conditional_high_min_V']>1.4 and  x['conditional_low_max_V']<.4 and  x['high_Z_max_V']<.4 for  x in models.values())
 report=dict(revision='R134',pcb_sha256=sha,native_primary_GPIO16_pad9_GPIO2_pad38_GPIO38_pad31_and_control_sets_verified=True,BQ_EN2_pin5_VSS_pin8_verified=True,conditional_models=models,voltage_assumption='ESP DC table is3.3V/25C/high-impedance measurement; extension to3.0..3.6V and loaded control is conditional.',loaded_GPIO_boot_ROM_brownout_and_USB_policy_qualified=False,mode_order='EN2,EN1',mode_table={'00':'USB10090/95/100mA','01':'USB500450/475/500mA','10':'ILIM_R8_max493.45mA','11':'USB suspend'},OFF_high_Z_max_input_mA=100,OFF500mA_or_automatic_BC1p2_PD_implemented=False,CE_does_not_detect_detached_NTC=True,fabrication_ready=False);name='USB_current_control_audit_R134.json'
elif mode=='preserve':
 m=json.loads((c/'preservation_manifest_R134.json').read_text())
 for path,h in m['unchanged_parent_repo_files'].items():assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==h,path
 for path,h in m['checked_R134_source_sha256'].items():assert (sha if path.endswith('.kicad_pcb')else hashlib.sha256((repo/path).read_bytes()).hexdigest())==h,path
 old=json.loads(gzip.decompress((c/'geometry_checkpoint_R133.json.gz').read_bytes()));assert old['bbox']==g['bbox']and old['board_outline']==g['board_outline'];assert collections.Counter(json.dumps(z,sort_keys=True)for z in old['zones'])==collections.Counter(json.dumps(z,sort_keys=True)for z in g['zones'])
 for ref,f in old['footprints'].items():
  want=dict(f)
  if ref=='J5':want['lib']='ENKU:USB4215_03_A_GCT_REVA'
  if ref=='TP8':want['pos']=[55.5,94.5]
  assert g['footprints'][ref]==want,ref
 assert g['footprints'].keys()-old['footprints'].keys()=={'R84','R85','R86','R87','R88'}
 def ix(rows):return {x['uuid']:{k:v for k,v in x.items()if k!='code'}for x in rows}
 a,b=ix(old['tracks']),ix(g['tracks']);removed={x['uuid']:x for x in m['exact_removed_copper']};added={x['uuid']:x for x in m['exact_added_copper']};changed={x['before']['uuid']:x for x in m['exact_reassigned_copper']};assert len(removed)==77 and  len(changed)==2
 approved={x['uuid']if isinstance(x,dict)else x for x in m['initial_declared_removed_copper']};rec=json.loads((c/'routing_recovery_R134.json').read_text());approved.update(rec['exact_obsolete_EN1_VBUS_copper_to_remove']);approved.update(x['uuid']for x in rec['exact_corridor_segments_to_remove_and_reconnect']);ops=json.loads((c/'applied_control_routing_R134.json').read_text())
 for op in [ops['local_routes'],ops['pruned_duplicate_tail'],ops['pruned_obsolete_supply_stub']]:approved.update(op.get('remove_tracks',[]))
 assert a.keys()-b.keys()==removed.keys()==approved&a.keys()
 for u,v in a.items():
  if u in removed:assert removed[u]==v;continue
  want=dict(v)
  if u in changed:assert u in {'07602f23-8d85-4b06-8579-e9430194f3fe','4f25235c-8c53-4c82-9dff-1aad5eed32f6'};want['net']='CHG_EN2'
  assert b[u]==want,u
 assert b.keys()-a.keys()==added.keys()and all(added[u]==b[u]and b[u]['width']>=.2 for  u in added)
 expected={('U1','9'):'CHG_EN1_CMD',('U1','38'):'CHG_EN2_CMD',('U1','31'):'CHG_CE_CMD',('U3','5'):'CHG_EN2',('U3','6'):'CHG_EN1'}
 a,b=ix(old['pads']),ix(g['pads']);gone=a.keys()-b.keys();assert len(gone)==2 and  all(a[u]['ref']=='J5'and a[u]['attribute']==3 for u in gone)
 for u,p in a.items():
  if u in gone or p['ref']=='J5':continue
  want=dict(p);key=(p['ref'],p['number'])
  if key in expected:want['net']=expected[key]
  if p['ref']=='TP8':assert b[u]['pos']==[55.5,94.5]and b[u]['net']==p['net']and b[u]['size']==p['size']and b[u]['drill']==p['drill']
  else:assert b[u]==want,u
 adjusted=json.loads(json.dumps(old))
 for p in adjusted['pads']:
  if(p['ref'],p['number'])in expected:p['net']=''
 assert_no_split(adjusted,g)
 oldaf={a['uuid']:a for a in json.loads((c/'assembly_features_R133.json').read_text())['pads']};newaf={a['uuid']:a for a in af['pads']}
 for u,a in oldaf.items():
  if a['ref']=='J5':continue
  want=dict(a)
  if a['ref']=='TP8':want['position_mm']=[55.5,94.5]
  assert newaf[u]==want,u
 oldnodes={(a.attrib['ref'],a.attrib['pin']):n.attrib['name']for n in ET.parse(c/'netlist_R133.xml').findall('./nets/net')for a in n.findall('node')}
 for key,n in oldnodes.items():assert nodes[key]==expected.get(key,n),key
 base=json.loads((c/'drc_checkpoint_R133.json').read_text());d=json.loads((o/'drc.json').read_text())
 def finding(v):return(v['type'],v['severity'],v['description'],tuple(sorted(a['uuid']for a in v['items'])))
 assert collections.Counter(finding(v)for v in d['violations'])==collections.Counter(finding(v)for v in base['violations']if not any(' of J5'in a['description']for a in v['items']));assert not d['unconnected_items']and not d['schematic_parity']and d['ignored_checks']==base['ignored_checks']
 report=dict(revision='R134',pcb_sha256=sha,unchanged_parent_repo_files=930,exact77_authorized_old_copper_removals_verified=True,exact2_EN2_escape_reassignments=True,new_copper=len(added),old_core_positions_outline_stack_RF_rules_and_zones_preserved=True,single_bare_TP8_move_verified=True,native16_same_button_findings_no_new_DRC=True,fabrication_ready=False);name='source_preservation_R134.json'
else:raise AssertionError(mode)
(o/name).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
