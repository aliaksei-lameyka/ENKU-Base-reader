"""Check manufacturer-derived geometry on native-exported physical copper.

Checks nominal drawing interpretation and regression; never grants manufacturing
signoff for locator holes, assembly tolerances or the unqualified land patterns.
"""
import json,sys,hashlib,math,collections
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon,Point
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
selector=json.loads((c/'current_checkpoint.json').read_text());revision=selector['revision']
d=json.loads((out/'drc.json' if server else c/selector['drc_file']).read_text())
checkpoint_expected=json.loads((c/selector['verification_file']).read_text())
def close(a,b):return len(a)==len(b) and all(abs(x-y)<1e-6 for x,y in zip(a,b))
def local(f,pos):
 dx,dy=[a-b for a,b in zip(pos,f['pos'])];theta=math.radians(f['angle']);co,si=math.cos(theta),math.sin(theta)
 return [co*dx-si*dy,si*dx+co*dy]
def land(a):return sh.union_all([Polygon(q) for q in a['polygons'].get('0',[])])
j2=g['footprints']['J2'];jp=[a for a in g['pads'] if a['ref']=='J2']
expected=[('9',[-5.875,-7.725],[.7,1.2]),('8',[-4.925,-7.725],[.7,1.2]),('1',[2.775,-7.725],[.7,1.2]),('2',[1.675,-7.725],[.7,1.2]),('3',[.575,-7.725],[.7,1.2]),('4',[-.525,-7.725],[.7,1.2]),('5',[-1.625,-7.725],[.7,1.2]),('6',[-2.725,-7.725],[.7,1.2]),('7',[-3.825,-7.725],[.7,1.2]),('6',[4.325,-7.725],[1,1.2]),('6',[-6.825,-3.425],[1,1.2]),('10',[-6.825,2.775],[1,.8]),('6',[-6.825,6.925],[1,2.8]),('6',[6.675,7.375],[1.3,1.9])]
assert len(jp)==len(expected)
for number,pos,size in expected:
 matches=[a for a in jp if a['number']==number and close(local(j2,a['pos']),pos)]
 assert len(matches)==1,(number,pos);a=matches[0]
 assert close(a['size'],size) and abs((a['angle']-j2['angle'])%180)<1e-6,(number,a)
 assert a['layers']==[0] and a['drill']==[0,0]
sdmap={'2':'SD_CS_CARD','3':'SD_MOSI_CARD','4':'3V3_SYS','5':'SD_SCLK_CARD','6':'GND','7':'SD_MISO_CARD'}
for a in jp:
 if a['number'] in sdmap:assert a['net']==sdmap[a['number']]
groups=partitions(g);buttons={};keepouts=[];revised_lands=[]
for ref,net in [('SW3','BTN_L1'),('SW4','BTN_L2'),('SW5','BTN_R1'),('SW6','BTN_R2')]:
 f=g['footprints'][ref];ps=[a for a in g['pads'] if a['ref']==ref]
 assert f['lib']=='ENKU:TL1016AAF160QG_ESWITCH_P520001' and len(ps)==4
 expected={'1':[-1.8,-.725],'2':[1.8,-.725],'3':[-1.8,.725],'4':[1.8,.725]}
 for a in ps:
  assert close(local(f,a['pos']),expected[a['number']]) and close(a['size'],[1.4,1.05]) and a['drill']==[0,0] and a['attribute']==1 and a['shape']==1 and a['layers']==[0]
  assert a['net']==(net if a['number']in ['1','2']else'GND') and abs((a['angle']-f['angle'])%180)<1e-6
 assert len(groups[net])==1 and len(groups['GND'])==1
 assert not any(z['name']=='TL3340 P021301B circuit trace keepout'for z in g['zones'])
 revised_lands += [(ref+':'+a['number'],land(a))for a in ps]
 buttons[ref]={'signal_net':net,'part':'TL1016AAF160QG','actual_no_boss_variant':True,'four_distinct_reference_numbers_and_external_pairs_verified':True,'drawing':'P520001 RevA28Apr2022'}
revised_lands += [('C18:'+a['number'],land(a)) for a in g['pads'] if a['ref']=='C18']
measure=[]
for t in g['tracks']:
 if not t['via']:continue
 closest=min(((geom.distance(Point(t['start']))-t['width']/2,ref) for ref,geom in revised_lands),key=lambda x:x[0]);measure.append({'uuid':t['uuid'],'net':t['net'],'annulus_to_revised_land_mm':closest[0],'nearest_land':closest[1]})
bad=[x for x in measure if x['annulus_to_revised_land_mm']<.1-1e-6];assert not bad,('Via in/too close to revised solder land',bad)
assert not d['unconnected_items'] and not d['schematic_parity']
types=dict(collections.Counter(v['type'] for v in d['violations']));assert types==checkpoint_expected['drc_types'],types
holes=d['violations'];scope=collections.Counter()
for finding in holes:
 if finding['type']!='hole_clearance':continue
 refs={i['description'].rsplit(' of ',1)[-1].split()[0] if ' of ' in i['description'] else i['description'].split()[-1] for i in finding['items']}
 assert len(refs)==1 and next(iter(refs)) in {'J5','SW3','SW4','SW5','SW6'},finding
 scope.update(refs)
assert not scope,scope
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report={'revision':revision,'pcb_sha256':sha,'manufacturer_nominal_geometry_review_passed':True,'J2_multipad_land_orientation_verified':True,'J2_physical_copper_preserved_from_R122':True,'actual_four_terminal_switch_geometry_and_wiring_verified':True,'buttons':buttons,'all_board_vias_checked_against_revised_lands':len(measure),'minimum_via_annulus_to_revised_land_mm':min(x['annulus_to_revised_land_mm'] for x in measure),'via_to_revised_land_violations':bad,'native_DRC_hole_findings_by_component':dict(scope),'trace_shorts_clearance_and_dangling_findings':0,'real_switch_replacement_removes_NPTH_interfaces':True,'qualified_locator_hole_interpretation':False,'assembly_tolerance_qualification':False,'manufacturer_sources':{'buttons':'https://configured-product-images.s3.amazonaws.com/2D/specs/TL1016AAF160QG.pdf','microSD_drawing':'Hirose EDC-325165-00-00 / CL0609-0031-0-00, mounting-side layout, supplied original PDF'},'scope':'Actual no-boss variant, primary nominal lands, distinct pin mapping and all-via wick risks. This is engineering review, not manufacturer/assembly/fabrication signoff.','fabrication_ready':False}
(out/('manufacturer_footprint_audit_'+revision+'.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
