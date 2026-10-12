"""Guard the approved SW1 electrical map and reviewed nominal physical lands.

A successful regression check does not resolve the manufacturer's A0/X1
land-pattern conflict, unspecified body/peg datum, or latching suffix.
"""
import json, sys, hashlib, math, xml.etree.ElementTree as ET
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon, Point, LineString
from pad_groups import partitions

r=Path(sys.argv[1]).resolve(); c=r/'checks'; server=len(sys.argv)>2
out=Path(sys.argv[2]).resolve() if server else c
selector=json.loads((c/'current_checkpoint.json').read_text()); revision=selector['revision']
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
d=json.loads((out/'drc.json' if server else c/selector['drc_file']).read_text())
f=g['footprints']['SW1']; ps=[a for a in g['pads'] if a['ref']=='SW1']
assert f['pos']==[40,22] and f['angle']==180
assert f['lib']=='ENKU:GSWITCH_MK12C03_G015_DRAWING_REVIEW' and len(ps)==9
def close(a,b): return len(a)==len(b) and all(abs(x-y)<1e-6 for x,y in zip(a,b))
def local(pos):
 dx,dy=[a-b for a,b in zip(pos,f['pos'])]; t=math.radians(f['angle'])
 return [math.cos(t)*dx-math.sin(t)*dy,math.sin(t)*dx+math.cos(t)*dy]
def land(a): return sh.union_all([Polygon(q) for q in a['polygons'].get('0',[])])
numbered={a['number']:a for a in ps if a['number']}
expected={'1':('GND',[-2.25,-1.75]),'2':('PWR_GATE',[.75,-1.75]),'3':('unconnected-(SW1-OFF_UNUSED-Pad3)',[2.25,-1.75])}
for n,(net,pos) in expected.items():
 a=numbered[n]
 assert a['net']==net and close(local(a['pos']),pos) and close(a['size'],[.7,1.5])
 assert a['layers']==[0] and a['drill']==[0,0] and a['attribute']==1
 vs=[local(v) for q in a['polygons']['0'] for v in q]
 assert close([min(v[0] for v in vs),min(v[1] for v in vs),max(v[0] for v in vs),max(v[1] for v in vs)],[pos[0]-.35,-2.5,pos[0]+.35,-1])
holes=[a for a in ps if max(a['drill'])]; mounts=[a for a in ps if not a['number'] and not max(a['drill'])]
assert len(holes)==2 and all(a['drill']==[.9,.9] and a['attribute']==3 for a in holes)
assert all(any(close(local(a['pos']),[x,0]) for a in holes) for x in [-1.5,1.5])
assert len(mounts)==4 and all(a['net']=='' and a['layers']==[0] and close(a['size'],[.55,.85]) for a in mounts)
assert all(any(close(local(a['pos']),[x,y]) for a in mounts) for x in [-3.375,3.375] for y in [-1.075,1.075])
groups=partitions(g)
assert len(groups['PWR_GATE'])==1 and len(groups['GND'])==1
assert not any(t['net']==expected['3'][0] for t in g['tracks'])
tree=ET.parse(out/'netlist.xml' if server else c/('netlist_'+revision+'.xml'))
component=tree.find("./components/comp[@ref='SW1']")
assert component.findtext('value')=='MK-12C03-G015' and component.findtext('footprint')==f['lib']
actual={node.attrib['pin']:net.attrib['name'] for net in tree.findall('./nets/net') for node in net.findall('node') if node.attrib['ref']=='SW1'}
assert actual=={n:v[0] for n,v in expected.items()},actual
lands=[(a['number'] or 'bracket',land(a)) for a in ps if not max(a['drill'])]
measures=[]
for t in g['tracks']:
 if not t['via']: continue
 gap,name=min((geom.distance(Point(t['start']))-t['width']/2,name) for name,geom in lands)
 measures.append({'uuid':t['uuid'],'net':t['net'],'nearest_SW1_land':name,'annulus_to_SW1_land_mm':gap})
assert all(m['annulus_to_SW1_land_mm']>=.1-1e-6 for m in measures)
board=sh.union_all([Polygon(q) for q in g['board_outline']]); edge=min(geom.distance(board.boundary) for _,geom in lands)
assert edge>=.5-1e-6 and all(board.covers(geom) for _,geom in lands)
for z in g['zones']:
 if z['rule'] and z['no_pads']:
  area=sh.union_all([Polygon(q) for q in z['polygons']])
  for a in ps:
   if set(a['layers'])&set(z['layers']): assert not land(a).intersects(area),('SW1 intrudes into a pad keepout',a['uuid'])
assert not d['unconnected_items'] and not d['schematic_parity']
assert not any(any(i['uuid'] in {a['uuid'] for a in ps}|{f['uuid']} for i in v['items']) for v in d['violations']), 'Active SW1 native finding'
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
plan=json.loads((c/'applied_SW1_R124.json').read_text())
report={'revision':revision,'pcb_sha256':sha,'approved_MPN':'G-Switch MK-12C03-G015','manufacturer_common_pin_2_verified':True,'native_netlist_and_physical_pin_map_verified':True,'contact_map':{n:{'net':v[0],'physical_position_mm':numbered[n]['pos']} for n,v in expected.items()},'unused_pin_3_has_no_routed_copper':True,'reviewed_signal_lands':3,'locator_holes':2,'mechanical_solder_lands':4,'upper_edge_pose':f,'minimum_SW1_copper_to_board_edge_mm':edge,'all_board_vias_checked_against_SW1_lands':len(measures),'minimum_via_annulus_to_SW1_land_mm':min(m['annulus_to_SW1_land_mm'] for m in measures),'RF_keepout_preserved':True,'SW1_native_findings':0,'source_documents':plan['source_documents'],'mixed_revision_land_pattern':True,'land_pattern_revision_resolved':False,'body_to_locator_Y_datum_qualified':False,'latching_suffix_and_external_slide_states_confirmed':False,'nominal_actuator_projection_beyond_upper_edge_mm':.875,'actuator_projection_scope':'Nominal drawing envelope assumes peg line at body centre; enclosure fit and slide direction require a qualified mechanical datum and sample.','enclosure_and_assembly_qualified':False,'fabrication_ready':False}
(out/('sw1_pin_map_audit_'+revision+'.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='source_documents'},indent=2))
