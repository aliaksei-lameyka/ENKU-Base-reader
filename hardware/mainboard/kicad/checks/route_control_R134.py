"""Bounded routing proposals using actual native connectivity and geometry.
Host Python, Shapely/SciPy. This is a proposal, never a substitute for KiCad DRC.
Uses native KiCad10 layers F0/B2/In1=4/In2=6, unchanged0.2mm clearance.
All new vias kept at least0.105mm from every SMD copper land.
Usage: script GEOMETRY OUTPUT_PLAN; full native DRC required afterwards.
"""
import heapq, json, math, sys, time
from collections import defaultdict
from pathlib import Path
import numpy as np
import shapely as sh
from shapely.geometry import Point, LineString, Polygon, box
from scipy.spatial import cKDTree
from pad_groups import components
g=json.loads(Path(sys.argv[1]).read_text());output=Path(sys.argv[2])
# Bound includes retained corridor anchors; USB data/RF footprint unchanged.
lo=np.array([25.,34.]);hi=np.array([65.,107.]);step=.05
nx,ny=(np.rint((hi-lo)/step).astype(int)+1).tolist();layers=[0,2,4,6]
xs=lo[0]+np.arange(nx)*step;ys=lo[1]+np.arange(ny)*step
xx,yy=np.meshgrid(xs,ys,indexing='xy')
items=g['pads']+g['tracks']; groups=components(g)
by_net=defaultdict(list)
for group in groups:
 valid=[a for a in group if a['net'] and not a['net'].startswith('unconnected-')]
 if valid:by_net[valid[0]['net']].append(valid)
foreign=defaultdict(list);land_polys=[]
for a in g['pads']:
 if not a['polygons']:continue
 for layer,ps in a['polygons'].items():
  z=sh.union_all([Polygon(poly) for poly in ps]);foreign[(a['net'],int(layer))].append(z)
  if a['number'] and not max(a['drill']):land_polys.append(z)
for t in g['tracks']:
 z=Point(t['start']).buffer(t['width']/2) if t['via'] else LineString([t['start'],t['end']]).buffer(t['width']/2)
 for l in layers if t['via'] else [t['layer']]:foreign[(t['net'],l)].append(z)
all_land=sh.union_all(land_polys).buffer(.355) # via radius.25 + copper gap.105
all_land_mask=sh.contains_xy(all_land,xx,yy)
# Protect actual USB trace projections and the previously accepted1mm reference strip.
usb=[t for t in g['tracks'] if t['net'].startswith('USB_D')]
voids=sh.union_all([Point(t['start']).buffer(t['width']/2+.26) for t in usb if t['via']])
center=LineString(json.loads((Path(__file__).parent/'accepted_usb_add.json').read_text())['centerline'])
reference_required={4:sh.union_all([LineString([t['start'],t['end']]).buffer(t['width']/2).difference(voids) for t in usb if not t['via'] and t['layer']==0]),
 6:sh.union_all([center.buffer(.5,join_style=2)]+[LineString([t['start'],t['end']]).buffer(t['width']/2).difference(voids) for t in usb if not t['via'] and t['layer']==2])}
added=[];plan={'revision':'R134','grid_mm':step,'bounds_mm':[lo.tolist(),hi.tolist()],
 'layers':layers,'clearance_mm':.2,'same_net_via_land_gap_mm':.105,'routes':[],'failed':[],'fabrication_ready':False}
def grid(pos):return tuple(np.rint((np.array(pos)-lo)/step).astype(int))
def inside(pos):return all(lo[i]-.0001<=pos[i]<=hi[i]+.0001 for i in range(2))
def world(i,j):return [round(float(xs[i]),6),round(float(ys[j]),6)]
def candidates(group):
 cs=[]
 for a in group:
  if 'pos' in a:
   if not inside(a['pos']):continue
   for l in a['layers']:
    if l in layers:cs.append((layers.index(l),*grid(a['pos']),a['pos']))
  else:
   for pos in [a['start'],a['end']]:
    if not inside(pos):continue
    for l in layers if a['via'] else [a['layer']]:
     if l in layers:cs.append((layers.index(l),*grid(pos),pos))
 return list({(v[0],v[1],v[2]):v for v in cs}.values())
def masks(net,width):
 others={l:[] for l in layers}
 for (n,l),ps in foreign.items():
  if n!=net and l in others:others[l]+=ps
 for n,l,z in added:
  if n!=net:others[l].append(z)
 obs={l:sh.union_all(ps) if ps else Polygon() for l,ps in others.items()}
 track=np.stack([sh.contains_xy(obs[l].buffer(width/2+.205),xx,yy) for l in layers])
 via=all_land_mask.copy()
 for rule in g['zones']:
  if not rule['rule']:continue
  z=sh.union_all([Polygon(p)for p in rule['polygons']])
  if rule['no_tracks']:
   for l in rule['layers']:
    if l in layers:track[layers.index(l)]|=sh.contains_xy(z.buffer(width/2+.005),xx,yy)
  if rule['no_vias']:via|=sh.contains_xy(z.buffer(.255),xx,yy)
 for t in g['tracks']:
  if t['via']:via|=sh.contains_xy(Point(t['start']).buffer(.555),xx,yy)
 for route in plan['routes']:
  for pos in route['vias']:via|=sh.contains_xy(Point(pos).buffer(.555),xx,yy)
 for l in layers:via|=sh.contains_xy(obs[l].buffer(.455),xx,yy)
 # Existing same-net through vias may change routing layers without drilling another hole.
 # Only exact grid centers are reused; native apply skips identical net/position vias.
 for t in g['tracks']:
  if t['via'] and t['net']==net and inside(t['start']):
   i,j=grid(t['start'])
   if world(i,j)==t['start'] and all(Point(t['start']).distance(obs[l])>=.45-1e-6 for l in layers):via[j,i]=False
 if net!='GND':
  for l,z in reference_required.items():track[layers.index(l)]|=sh.contains_xy(z.buffer(width/2+.265),xx,yy)
  via|=sh.contains_xy(sh.union_all(list(reference_required.values())).buffer(.515),xx,yy)
 if net.startswith('CHG_EN')or net=='CHG_CE_CMD':
  thermal=box(46.8,89.6,50.15,93.3)
  track[layers.index(2)]|=sh.contains_xy(thermal.buffer(width/2+.205),xx,yy)
  via|=sh.contains_xy(thermal.buffer(.455),xx,yy)
 if net=='CHG_STAT2':track[layers.index(2),:,:]=True # Keep new B thermal spread continuous
 return track,via,obs
def astar(s,z,blocked,via):
 sl,si,sj=s[:3];tl,ti,tj=z[:3]
 if blocked[sl,sj,si] or blocked[tl,tj,ti]:return None
 goal=(tl,ti,tj);start=(sl,si,sj);pq=[(0.,0.,start)];dist={start:0.};prev={}
 def heuristic(l,i,j):
  di,dj=abs(i-ti),abs(j-tj)
  return max(di,dj)+(math.sqrt(2)-1)*min(di,dj)+(30 if l!=tl else 0)
 visited=0;closed=set()
 while pq:
  _,cost,u=heapq.heappop(pq)
  if cost>dist.get(u,math.inf)+1e-8 or u in closed:continue
  closed.add(u)
  if u==goal:
   path=[u]
   while u in prev:u=prev[u];path.append(u)
   return list(reversed(path))
  visited+=1
  if visited>180000:return None
  l,i,j=u
  for di,dj,dc in [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,math.sqrt(2)),(-1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,-1,math.sqrt(2))]:
   ii,jj=i+di,j+dj
   if not (0<=ii<nx and 0<=jj<ny) or blocked[l,jj,ii]:continue
   if di and dj and (blocked[l,jj,i] or blocked[l,j,ii]):continue
   v=(l,ii,jj);nd=cost+dc
   if nd<dist.get(v,math.inf)-1e-8:dist[v]=nd;prev[v]=u;heapq.heappush(pq,(nd+heuristic(*v),nd,v))
  if not via[j,i]:
   for ll in range(len(layers)):
    if ll==l or blocked[ll,j,i]:continue
    v=(ll,i,j);nd=cost+60
    if nd<dist.get(v,math.inf)-1e-8:dist[v]=nd;prev[v]=u;heapq.heappush(pq,(nd+heuristic(*v),nd,v))
 return None
def route_path(net,width,path,s,z,obs):
 segs=[];vias=[];points=[path[0]];before=None
 for prev,cur in zip(path,path[1:]):
  direction=(cur[0]-prev[0],cur[1]-prev[1],cur[2]-prev[2])
  if cur[0]!=prev[0]:
   if points[-1]!=prev:points.append(prev)
   points.append(cur);before=None
  elif direction!=before:
   if points[-1]!=prev:points.append(prev)
   before=direction
 if points[-1]!=path[-1]:points.append(path[-1])
 # Keep exact retained track endpoints; pad center snaps remain inside lands.
 for a,b in zip(points,points[1:]):
  pos_a,pos_b=world(a[1],a[2]),world(b[1],b[2])
  if a[0]!=b[0]:
   if pos_a not in vias:vias.append(pos_a)
  elif pos_a!=pos_b:segs.append({'a':pos_a,'b':pos_b,'layer':layers[a[0]]})
 for cand,point in [(s,path[0]),(z,path[-1])]:
  snapped=world(point[1],point[2])
  if snapped!=cand[3]:segs.append({'a':cand[3],'b':snapped,'layer':layers[point[0]]})
 # Verify the complete centerline independently against continuous geometry.
 if net!='GND':
  for seg in segs:
   if seg['layer'] in reference_required and LineString([seg['a'],seg['b']]).distance(reference_required[seg['layer']])<width/2+.265-1e-6:return None
  for v in vias:
   if Point(v).distance(sh.union_all(list(reference_required.values())))<.515-1e-6:return None
 for seg in segs:
  if LineString([seg['a'],seg['b']]).distance(obs[seg['layer']])<width/2+.2-1e-6:return None
 record={'net':net,'width':width,'via_diameter':.5,'segments':segs,'vias':vias}
 for seg in segs:added.append((net,seg['layer'],LineString([seg['a'],seg['b']]).buffer(width/2)))
 for v in vias:
  for l in layers:added.append((net,l,Point(v).buffer(.25)))
 return record
order=sorted(by_net,key=lambda net:(0 if net.startswith('CHG_') else 1 if net in ['BAT_TS','VSYS','VBAT','VBUS_USB'] else 2 if net=='GND' else 3,len(by_net[net])))
for net in order:
 if len(by_net[net])<2:continue
 if net not in ['GND','VBAT','VSYS','VBUS_USB','3V3_SYS','BAT_TS'] and not net.startswith('CHG_'):continue
 gs=by_net[net];width=.3 if net in ['VBAT','VSYS','VBUS_USB'] else .2
 blocked,via,obs=masks(net,width)
 loops=0
 while len(gs)>1:
  pairs=[]
  for i in range(len(gs)):
   a=[v for v in candidates(gs[i]) if not blocked[v[0],v[2],v[1]]]
   if not a:continue
   for j in range(i+1,len(gs)):
    b=[v for v in candidates(gs[j]) if not blocked[v[0],v[2],v[1]]]
    if not b:continue
    aa=np.array([[v[1],v[2]] for v in a]);bb=np.array([[v[1],v[2]] for v in b])
    d,ind=cKDTree(bb).query(aa,k=min(3,len(b)))
    if d.ndim==1:d=d[:,None];ind=ind[:,None]
    choices=[]
    for ai in range(len(a)):
     for k in range(d.shape[1]):
      bi=int(ind[ai,k]);score=float(d[ai,k])+30*(a[ai][0]!=b[bi][0])
      choices.append((score,i,j,a[ai],b[bi]))
    ranked=sorted(choices,key=lambda v:v[0])
    # Preserve the best candidate for every source/destination layer pair.
    # Otherwise many short F.Cu stubs can hide legal existing inner-layer vias.
    best={}
    for v in ranked:best.setdefault((v[3][0],v[4][0]),v)
    pairs+=list(best.values())+ranked[:10]
  success=False
  for _,i,j,s,z in sorted(pairs,key=lambda v:v[0])[:50]:
   path=astar(s,z,blocked,via)
   if path is None:continue
   record=route_path(net,width,path,s,z,obs)
   if record is None:continue
   plan['routes'].append(record);gs[i]+=gs[j];gs.pop(j);success=True
   for pos in record['vias']:via|=sh.contains_xy(Point(pos).buffer(.555),xx,yy)
   output.write_text(json.dumps(plan,indent=2)+'\n')
   print(net,len(gs),'groups remain',len(record['segments']),'segments',len(record['vias']),'vias',flush=True)
   break
  if not success:
   plan['failed'].append({'net':net,'groups_remaining':len(gs),'candidate_group_sizes':[len(candidates(v)) for v in gs]})
   print('FAILED',net,len(gs),flush=True);break
 output.write_text(json.dumps(plan,indent=2)+'\n')
print('PROPOSAL',len(plan['routes']),'connections; unresolved',plan['failed'],flush=True)
