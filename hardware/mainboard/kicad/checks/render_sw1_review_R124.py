"""Render exact exported copper/holes with an explicitly provisional body."""
import json, gzip, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle
r=Path(sys.argv[1]); c=r/'checks'
g=json.loads((c/'geometry_current.json').read_text()) if (c/'geometry_current.json').exists() else json.loads(gzip.decompress((c/'geometry_checkpoint_R124.json.gz').read_bytes()))
fig,ax=plt.subplots(figsize=(11,7));ax.set_facecolor('#f4f6f8')
for z in g['zones']:
 if z['rule'] and z['no_pads']:
  for q in z['polygons']:ax.add_patch(Polygon(q,fc='#f1d4d4',ec='#bb6565',hatch='///',alpha=.6))
for a in g['pads']:
 if not (26<a['pos'][0]<50 and 18<a['pos'][1]<33):continue
 if max(a['drill']):ax.add_patch(Circle(a['pos'],max(a['drill'])/2,fc='white',ec='#292c30',lw=1.2))
 else:
  for q in a['polygons'].get('0',[]):ax.add_patch(Polygon(q,fc='#deb574' if a['ref']=='SW1' else '#a2b2b7',ec='#805622' if a['ref']=='SW1' else '#718389',lw=.7))
for t in g['tracks']:
 if not (min(t['start'][0],t['end'][0])<50 and max(t['start'][0],t['end'][0])>26 and min(t['start'][1],t['end'][1])<33 and max(t['start'][1],t['end'][1])>18):continue
 color='#187ab7' if t['layer']==2 else '#cc6a37'
 if t['via']:
  ax.add_patch(Circle(t['start'],t['width']/2,fc=color,ec='black',lw=.4));ax.add_patch(Circle(t['start'],t['drill']/2,fc='white',ec='none'))
 else:ax.plot([t['start'][0],t['end'][0]],[t['start'][1],t['end'][1]],color=color,lw=t['width']*7,alpha=.9)
for a in g['pads']:
 if a['ref']=='SW1' and a['number']:ax.text(*a['pos'],a['number'],ha='center',va='center',fontsize=10,fontweight='bold',color='#422e1a')
for pos,w,h in [((36.7,20.625),6.6,2.75),((38.6,19.125),2.8,1.5)]:ax.add_patch(Rectangle(pos,w,h,fill=False,ec='#9c3850',ls='--',lw=1.3))
ax.axhline(20,color='#141f27',lw=2);ax.text(47.5,19.7,'Board edge',ha='right',fontsize=10)
ax.text(40,18.55,'SW1: MK-12C03-G015',ha='center',fontsize=12,fontweight='bold');ax.text(29,22.5,'H1',ha='center',va='center',fontsize=9)
ax.text(27,32,'RF keepout lies to the left',fontsize=9,color='#8e4141')
ax.set_xlim(26,49);ax.set_ylim(33,18);ax.set_aspect('equal');ax.set_xlabel('x, mm');ax.set_ylabel('y, mm');ax.grid(alpha=.16)
ax.set_title('R124 — native copper and holes\nDashed body / actuator datum is unqualified; NO FAB',fontsize=12,pad=15)
fig.text(.5,.015,'Contacts: 1 = GND   |   2 = COM / PWR_GATE   |   3 = unused.  Orange: F.Cu; blue: B.Cu.',ha='center',fontsize=10)
fig.tight_layout(rect=[0,.035,1,1]);fig.savefig(c/'SW1_native_geometry_R124.png',dpi=130)
