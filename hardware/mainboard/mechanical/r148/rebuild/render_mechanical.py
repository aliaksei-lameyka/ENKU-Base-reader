"""CAD tessellation only; no generative imagery. CPU Matplotlib render and PIL layout."""
from pathlib import Path
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import json,math
P=Path(__file__).resolve().parent;(P/'qa').mkdir(exist_ok=True);O=P/'output';R=json.loads((O/'Mechanical_Provenance_and_Dimensions.json').read_text())
# Import the final exported assembly, preserving STEP leaf names through XCAF import.
assy=cq.importers.importStep(str(O/'ENKU_R148_Enclosure_Reference.step')).val()
# STEP solids are returned in assembly order; use one continuous solid group per recorded component.
solids=assy.Solids();offset=0;items=[]
colors={'PCB':(.055,.31,.22),'U1':(.65,.68,.69),'J2':(.72,.75,.77),'J3':(.22,.23,.24),'J1':(.91,.75,.43),'SW1':(.95,.59,.12),'L1':(.23,.24,.25),'L2':(.23,.24,.25),'J5':(.73,.75,.78)}
for r in R['parts']:
 n=r['solids'];items.append((r['ref'],cq.Compound.makeCompound(solids[offset:offset+n])));offset+=n
assert offset==len(solids)
meshes=[]
for ref,s in items:
 vv,ff=s.tessellate(.07,.3);v=np.array([p.toTuple()for p in vv]);meshes.append((ref,v[np.array(ff)]))
# Refine broad planar triangles for correct painter-depth order in a CPU-only renderer.
def refine(tri,max_edge=2.0):
 for iteration in range(10):
  e=np.stack([np.linalg.norm(tri[:,i]-tri[:,(i+1)%3],axis=1)for i in range(3)],axis=1).max(axis=1);mask=e>max_edge
  if not mask.any():return tri
  keep=tri[~mask];t=tri[mask];a,b,c=t[:,0],t[:,1],t[:,2];ab,bc,ca=(a+b)/2,(b+c)/2,(c+a)/2
  tri=np.concatenate([keep,np.stack([a,ab,ca],axis=1),np.stack([ab,b,bc],axis=1),np.stack([ca,bc,c],axis=1),np.stack([ab,bc,ca],axis=1)])
 return tri
meshes=[(ref,refine(tri))for ref,tri in meshes]
def render(n,elev,azim,w,h):
 fig=plt.figure(figsize=(w/160,h/160),dpi=160,facecolor='#f4f7fa');ax=fig.add_subplot(111,projection='3d',computed_zorder=True)
 alltri=np.concatenate([tri for ref,tri in meshes]);allcolors=np.concatenate([np.tile(colors.get(ref,(.45,.47,.49)),(len(tri),1))for ref,tri in meshes]);coll=Poly3DCollection(alltri,facecolors=allcolors,linewidth=0,antialiased=False,shade=True,lightsource=matplotlib.colors.LightSource(azdeg=315,altdeg=55));ax.add_collection3d(coll)
 ax.set(xlim=(-2,61),ylim=(-103,3),zlim=(0,8));ax.set_box_aspect((63,106,8));ax.set_proj_type('ortho');ax.view_init(elev=elev,azim=azim);ax.set_axis_off();ax.patch.set_alpha(0);fig.subplots_adjust(0,0,1,1);fig.savefig(P/'qa'/n,dpi=160,facecolor='#f4f7fa',bbox_inches='tight',pad_inches=0);plt.close(fig)
 im=Image.open(P/'qa'/n).convert('RGB');ar=np.asarray(im);mask=np.max(np.abs(ar.astype(int)-np.array([244,247,250])),axis=2)>20;ys,xs=np.where(mask);im.crop((max(0,xs.min()-12),max(0,ys.min()-12),min(im.width,xs.max()+13),min(im.height,ys.max()+13))).save(P/'qa'/n)
render('isometric.png',55,-58,1150,1450)
render('top.png',90,-90,1050,1650)
render('side.png',3,0,1650,420)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F=lambda sz:ImageFont.truetype(font,sz);B=lambda sz:ImageFont.truetype(bold,sz)
canvas=Image.new('RGB',(2300,2060),'#f4f7fa');d=ImageDraw.Draw(canvas)
d.text((70,40),'ENKU R148 | Mechanical enclosure reference',font=B(45),fill='#163149')
d.text((70,105),'59 x 101 x 1.6 mm PCB  |  Four mounting holes: diameter 2.2 mm  |  Units: mm',font=F(27),fill='#40566b')
iso=Image.open(P/'qa/isometric.png');iso.thumbnail((1130,1380));canvas.paste(iso,(45,260))
top=Image.open(P/'qa/top.png');top=top.resize((int(top.width*1400/top.height),1400));canvas.paste(top,(1340,250))
d.text((70,180),'ISOMETRIC - fitted parts / nominal envelopes',font=B(25),fill='#163149')
d.text((1260,180),'TOP - exact source placements',font=B(25),fill='#163149')
side=Image.open(P/'qa/side.png');side=side.resize((1050,int(side.height*1050/side.width)));canvas.paste(side,(70,1720))
d.text((70,1610),'SIDE PROFILE',font=B(25),fill='#163149')
for x,y,text in [(1250,1880,'OEM CAD: Hirose, E-Switch, Espressif'),(1250,1920,'Amber: nominal SW1; grey: package envelopes'),(70,1950,'STEP contains named separate bodies. Access zones are in a separate optional STEP.'),(70,1995,'Nominal engineering reference. SW1 datum, actual folded flex, wire clamp and case fit remain HOLD.')]:d.text((x,y),text,font=F(23),fill='#40566b')
canvas.save(O/'ENKU_R148_Mechanical_Preview.png')
print('Rendered verified final STEP',len(solids),'solids')
