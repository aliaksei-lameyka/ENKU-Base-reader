"""TI DSE0006A drawing4220552/B Jan2024: independent three-layer actual lands."""
import copy,hashlib,json,sys
from pathlib import Path
import shapely as sh
from shapely.geometry import box
from shapely import affinity
from gerbonara import GerberFile
from gerbonara.graphic_objects import Flash
from full_copper_R138 import object_shape
r,o=map(lambda v:Path(v).resolve(),sys.argv[1:3]);g=json.loads((o/'geometry.json').read_text());fp=g['footprints']['U11'];assert fp['pos']==[44.5,67.5]and fp['angle']==0
# Rounded rectangles constructed from drawing dimensions, not footprint polygons.
def rr(x,y,w,h,radius):return box(x-w/2+radius,y-h/2+radius,x+w/2-radius,y+h/2-radius).buffer(radius,quad_segs=128)
centres=[(-.55,-.5),(-.6,0),(-.6,.5),(.6,.5),(.6,0),(.6,-.5)];expect={}
for layer in ['F_Cu','F_Mask','F_Paste']:
 shapes=[]
 for i,(x,y)in enumerate(centres):
  if layer=='F_Cu':w,h,rad=(.9 if i==0 else .8,.35,.1)if i<3 else(.7,.25,.05)
  elif layer=='F_Mask':w,h,rad=(.8 if i==0 else .7,.25,.05)if i<3 else(.75,.30,.075)
  else:w,h,rad=(.8 if i==0 else .7,.25,.05)if i<3 else(.7,.25,.05)
  shapes.append(rr(x+44.5,y+67.5,w,h,rad))
 expect[layer]=sh.union_all(shapes)
actual={};counts={}
for layer in expect:
 f=GerberFile.open(o/'manufacturing_review_R144/gerber'/f'enku-mainboard-r0.1-{layer}.gbr');objects=[a for a in f.objects if isinstance(a,Flash)and ((a.attrs.get('.P')or[''])[0]=='U11'if layer=='F_Cu'else(a.attrs.get('.C')or[''])[0]=='U11')];counts[layer]=len(objects);assert len(objects)==6,(layer,len(objects));actual[layer]=affinity.scale(sh.union_all([object_shape(a)for a in objects]),1,-1,origin=(0,0))
def contract(images):
 for layer,expected in expect.items():
  a=images[layer];assert a.difference(expected.buffer(.0002)).area<1e-7 and expected.difference(a.buffer(.0002)).area<1e-7,(layer,'OEM land mismatch')
contract(actual);faults=[]
for layer,label,kind in [('F_Cu','left_pin1_narrowed','cut'),('F_Cu','unrequested_exposed_pad','add'),('F_Mask','left_SMD_mask_expanded','expand'),('F_Paste','left_paste_missing','cut'),('F_Paste','oversized_right_paste','expand')]:
 images=dict(actual)
 if kind=='cut':images[layer]=images[layer].difference(box(43.45,66.85,44.4,67.15))
 elif kind=='add':images[layer]=images[layer].union(box(44.35,67.35,44.65,67.65))
 else:images[layer]=images[layer].buffer(.025)
 try:contract(images)
 except AssertionError:faults.append(dict(fault=label,detected=True))
 else:raise AssertionError('Ineffective fault '+label)
(o/'supervisor_OEM_R144.json').write_text(json.dumps(dict(revision='R144',pcb_sha256=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),primary_source='https://www.ti.com/lit/ds/symlink/tps3890.pdf',drawing='DSE0006A 4220552/B 01/2024 pages25-26',six_leads_no_EP=True,actual_Gerber_flashes=counts,all_three_layers_match=True,comparison_tolerance_mm=.0002,effective_faults=faults,common_stencil_process='HOLD',physical_test='NOT RUN',fabrication_ready=False),indent=2)+'\n');print('PASS TI DSE0006A actual copper/mask/paste and5 effective faults')
