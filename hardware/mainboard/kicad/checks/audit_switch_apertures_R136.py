"""Independent P520001 AA lands, actual native solder windows and actuator datum."""
import json,sys,math
from pathlib import Path
from shapely.geometry import box
from shapely.ops import unary_union
from native_svg_shapes_R130 import actual_shapes
r,o=map(lambda s:Path(s).resolve(),sys.argv[1:3]);g=json.loads((o/'geometry.json').read_text());af=json.loads((o/'assembly_features.json').read_text());fps={f['ref']:f for f in af['footprints']};ox,oy=g['bbox'][:2];rows=[]
for ref,net,x,y,angle,tip in [('SW3','BTN_L1',21.55,73,-90,19.45),('SW4','BTN_L2',21.55,85,-90,19.45),('SW5','BTN_R1',73.45,73,90,75.55),('SW6','BTN_R2',73.45,85,90,75.55)]:
 f=g['footprints'][ref];assert f['pos']==[x,y]and f['angle']==angle and f['lib']=='ENKU:TL1016AAF160QG_ESWITCH_P520001';assert fps[ref]['fields']['MPN']=='TL1016AAF160QG'
 ps={p['number']:p for p in g['pads']if p['ref']==ref};assert ps.keys()=={'1','2','3','4'}
 for n,xx,yy in [('1',-1.8,-.725),('2',1.8,-.725),('3',-1.8,.725),('4',1.8,.725)]:
  a=math.radians(angle);pos=[round(x+xx*math.cos(a)+yy*math.sin(a),6),round(y+yy*math.cos(a)-xx*math.sin(a),6)];p=ps[n]
  assert p['pos']==pos and p['size']==[1.4,1.05]and (p['angle']-angle)%360==0 and p['shape']==1 and p['attribute']==1 and p['drill']==[0,0]and p['net']==(net if n in ['1','2']else'GND')
 # Four separate physical apertures, including formerly unused duplicated contacts.
 target=unary_union([box(p['pos'][0]-.525-ox,p['pos'][1]-.7-oy,p['pos'][0]+.525-ox,p['pos'][1]+.7-oy)for p in ps.values()]);roi=box(x-3-ox,y-2.7-oy,x+3-ox,y+2.7-oy);plots={}
 for layer in ['F_Mask','F_Paste']:
  actual=unary_union(actual_shapes(o/(layer+'.svg'),roi));assert actual.symmetric_difference(target).area<.0001,(ref,layer);assert len(actual.geoms)==4;plots[layer]=dict(apertures=4,area_mm2=actual.area)
 assert abs(x+(2.1 if angle==90 else-2.1)-tip)<1e-6
 rows.append(dict(ref=ref,actuation_tip_x_mm=tip,button_y_mm=y,native_windows=plots))
report=dict(revision='R136',pcb_sha256=(o/'source_pcb.sha256').read_text().split()[0],primary_P520001_RevA28Apr2022_SHA256='9f1097ea8591bbf730ee905ba186e0c6c0d48cfc573395d0ab7f9704a20e5a75',actual_AA_no_boss_four_distinct_pads_verified=True,rows=rows,nominal_body_height_mm=1.35,old_body_height_mm=3.3,vertical_actuator_axis_and_case_pusher_drop_in_qualified=False,case_thickness_increased=False,assembly_and_lifetime_bench_qualified=False,fabrication_ready=False)
(o/'switch_apertures_R136.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
