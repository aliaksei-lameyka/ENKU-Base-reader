"""Connectivity from independently parsed four Gerber images and plated barrels.
No KiCad connectivity decisions; physical geometry mutations prove detection.
"""
import hashlib,json,math,sys
from pathlib import Path
import shapely as sh
from shapely.geometry import Point,LineString,Polygon,box
from shapely import affinity
from gerbonara import GerberFile
from full_copper_R138 import layer_shape
from hirose_regions_R143 import POLYGONS,transform
r,o=[Path(s).resolve()for s in sys.argv[1:3]];g=json.loads((o/'geometry.json').read_text());layers=[0,4,6,2];names=['F_Cu','In1_Cu','In2_Cu','B_Cu'];tol=.0002
images={l:affinity.scale(layer_shape(GerberFile.open(o/'manufacturing_review_R143/gerber'/f'enku-mainboard-r0.1-{n}.gbr')),1,-1,origin=(0,0))for l,n in zip(layers,names)}
def graph(img):
 parts={l:list(sh.get_parts(img[l].buffer(tol)))for l in layers};trees={l:sh.STRtree(parts[l])for l in layers};parent={(l,i):(l,i)for l in layers for i in range(len(parts[l]))};labels={};missing=[]
 def root(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 def join(a,b):parent[root(b)]=root(a)
 def at(point,ls):return [(l,int(i))for l in ls for i in trees[l].query(Point(point),predicate='intersects')]
 def assign(point,ls,net,identity,barrel=False):
  nodes=at(point,ls)
  if not nodes:missing.append(dict(identity=identity,net=net,position=point));return
  if barrel:
   for node in nodes[1:]:join(nodes[0],node)
  for node in nodes:
   if net and not net.startswith('unconnected-'):labels.setdefault(node,set()).add(net)
 for a in g['pads']:
  if not a['number']or a['attribute']==3:continue
  ls=[l for l in layers if str(l)in a['polygons']];assign(a['pos'],ls,a['net'],a['ref']+'.'+a['number'],a['attribute']==0 and max(a['drill'])>0)
 for a in g['tracks']:
  if a['via']:assign(a['start'],layers,a['net'],a['uuid'],True)
 connected={}
 for node,nets in labels.items():connected.setdefault(root(node),set()).update(nets)
 shorts=[dict(island=list(k),nets=sorted(v))for k,v in connected.items()if len(v)>1];nets={}
 for k,ns in connected.items():
  for net in ns:nets.setdefault(net,[]).append(list(k))
 opens={n:v for n,v in nets.items()if len(v)>1};allroots={root(n)for n in parent};unknown=len(allroots-set(connected))
 return dict(shorts=shorts,opens=opens,missing_lands=missing,named_nets=len(nets),conductive_islands=sum(map(len,parts.values())),barrel_joined_roots=len(allroots),unlabelled_roots=unknown)
actual=graph(images);assert not actual['shorts']and not actual['opens']and not actual['missing_lands'],actual;print('PASS independent Gerber connectivity',actual['named_nets'],'nets',flush=True)
mut=dict(images);mut[0]=mut[0].union(LineString([(39.45,62.8),(39.45,64.7)]).buffer(.12));short=graph(mut);assert any({'GND','ESP_EN'}<=set(x['nets'])for x in short['shorts']),'Injected short not detected'
mut=dict(images);mut[0]=mut[0].difference(box(42.25,63,42.5,64.5));opened=graph(mut);assert len(opened['opens'].get('3V3_SYS',[]))>=2,'Injected physical open not detected'
f=g['footprints']['J2'];region=sh.union_all([Polygon([transform(p,f)for p in pp])for pp in POLYGONS]);area=images[0].intersection(region).area;assert area<1e-8
route=json.loads((o/'routing/routing_review_R140.json').read_text());fast=[dict(net=a['net'],total_tree_length_mm=a['total_track_length_mm'],tree_flight_time_upper_scenario_ns=a['total_track_length_mm']/299.792458*math.sqrt(4.6))for a in route['inventory']if a['category']=='FAST']
resistance=[]
for net in ['VBUS_USB','VBAT','VSYS','SYS_EN','3V3_SYS']:
 track=[a for a in g['tracks']if not a['via']and a['net']==net]
 for um in [18,35]:
  ohm=sum(1.724e-8*math.dist(a['start'],a['end'])*.001/(a['width']*.001*um*1e-6)for a in track);resistance.append(dict(net=net,copper_thickness_scenario_um=um,total_tree_resistance_ohm=ohm,drop_at500mA_V=.5*ohm))
nom=json.loads((o/'independent_electrical_R143.json').read_text())['reset']['nominal_output_V'];ceff=44*.8*.85*.9*.5;steps=[]
for current in [.1,.5,.75]:
 for delay in [1,5,10,25,50,100]:
  for esr in [.01,.05]:
   dv=current*esr+current*delay/ceff;steps.append(dict(load_step_A=current,control_response_delay_scenario_us=delay,ESR_scenario_ohm=esr,droop_V=dv,below_3V0=nom-dv<3.))
report=dict(revision='R143',pcb_sha256=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),method='Gerbonara image polarity + Shapely conductor islands + explicit plated-barrel joins + source labels independently IPC356-checked',geometric_tolerance_mm=tol,actual=actual,effective_negative_tests=[dict(case='U11 GND to RESET copper bridge',detected_shorts=short['shorts']),dict(case='U11 supply branch physical cut',detected_open_roots=opened['opens']['3V3_SYS'])],Hirose_surface_copper_intersection_mm2=area,flight_time_scenarios=fast,DC_copper_scenarios=resistance,DC_model_limits='Total segment-tree upper bound, not solved current path; planes, pad copper, barrels and tolerances omitted',capacitor_only_load_steps=steps,effective_capacitance_scenario_uF=ceff,load_model_limits='Charge balance only, no converter control-loop simulation and no manufacturer guaranteed capacitance envelope',IBIS_stackup_dynamic_and_physical_tests='NOT RUN',fabrication_ready=False)
(o/'independent_Gerber_graph_R143.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS injected physical open/short detection and OEM surface copper exclusion; physical HOLD',flush=True)
