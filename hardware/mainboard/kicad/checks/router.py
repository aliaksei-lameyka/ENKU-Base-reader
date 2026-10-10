"""Conservative geometric route proposer. Native KiCad DRC is the acceptance gate."""
import json,sys,math,heapq,itertools,time,os
from pathlib import Path
import numpy as np
import shapely as sh
from shapely.geometry import Polygon,LineString,Point
class Router:
 def __init__(self,g,step=.1,layers=(0,4,2),region=None):
  self.g=g;self.step=step;self.layers=list(layers);self.x0,self.y0,self.x1,self.y1=region or g['bbox'];self.xs=np.arange(self.x0,self.x1+step/2,step);self.ys=np.arange(self.y0,self.y1+step/2,step);self.X,self.Y=np.meshgrid(self.xs,self.ys);self.shape=self.X.shape
  self.points=sh.points(self.X,self.Y);self.board=Polygon(g['board_outline'][0]);self.padshapes={p['uuid']:sh.union_all([Polygon(v) for ps in p['polygons'].values() for v in ps]) for p in g['pads'] if p['polygons']};self.trackshapes={t['uuid']:Point(t['start']) if t['via'] else LineString([t['start'],t['end']]) for t in g['tracks']}
 def idx(self,pos,layer):return self.layers.index(layer),round((pos[1]-self.y0)/self.step),round((pos[0]-self.x0)/self.step)
 def xy(self,k):return [round(float(self.xs[k[2]]),5),round(float(self.ys[k[1]]),5)]
 def stamp(self,mask,shape,radius):
  if shape.is_empty:return
  x0,y0,x1,y1=shape.bounds;s=self.step
  a=max(0,math.floor((x0-radius-self.x0)/s));b=min(len(self.xs),math.ceil((x1+radius-self.x0)/s)+1);c=max(0,math.floor((y0-radius-self.y0)/s));d=min(len(self.ys),math.ceil((y1+radius-self.y0)/s)+1)
  if a<b and c<d:mask[c:d,a:b]|=sh.distance(self.points[c:d,a:b],shape)<radius-1e-6
 def masks(self,net,width=.2,vd=.5):
  ms=np.repeat((~sh.contains(self.board.buffer(-(.51+width/2)),self.points))[None,:,:],len(self.layers),axis=0);vm=~sh.contains(self.board.buffer(-(.51+vd/2)),self.points)
  for p in self.g['pads']:
   shape=self.padshapes.get(p['uuid'],Point(p['pos']));same=p['net']==net;clear=.508 if p['ref']=='J7' and not same else .205
   if not same:
    for l in p['layers']:
     if l in self.layers:self.stamp(ms[self.layers.index(l)],shape,width/2+clear)
   self.stamp(vm,shape,vd/2+(.1 if same else clear))
   if max(p['drill'])>0:self.stamp(vm,Point(p['pos']),max(p['drill'])/2+vd/2+.255)
  for t in self.g['tracks']:
   if t['net']==net:continue
   shape=self.trackshapes.get(t['uuid']) or (Point(t['start']) if t['via'] else LineString([t['start'],t['end']]));r=t['width']/2+.205
   for l in self.layers if t['via'] else [t['layer']]:
    if l in self.layers:self.stamp(ms[self.layers.index(l)],shape,r+width/2)
   self.stamp(vm,shape,r+vd/2)
  for z in self.g['zones']:
   if not z['rule']:continue
   for poly in z['polygons']:
    shape=Polygon(poly)
    if z['no_tracks']:
     for l in z['layers']:
      if l in self.layers:self.stamp(ms[self.layers.index(l)],shape,width/2+.01)
    if z['no_vias']:self.stamp(vm,shape,vd/2+.01)
  return ms,vm
 def free_line(self,a,b,mask):
  n=max(1,math.ceil(math.dist(a,b)/self.step*2));v=np.linspace(a,b,n+1);x=np.rint((v[:,0]-self.x0)/self.step).astype(int);y=np.rint((v[:,1]-self.y0)/self.step).astype(int)
  return bool(np.all((x>=0)&(x<len(self.xs))&(y>=0)&(y<len(self.ys)))) and not np.any(mask[y,x])
 def ports(self,item):
  if 'pos' in item:
   pos=item['pos'];layers=[x for x in item['layers'] if x in self.layers]
   if item.get('ref')=='J7' and item['number']:
    pos=[pos[0],pos[1]+(-.265 if pos[1]<87 else .265)]
   return [(self.idx(pos,l),pos) for l in layers]
  ls=self.layers if item['via'] else [item['layer']]
  poss=[item['start'],item['end']]
  if not item['via'] and math.dist(*poss)>2:poss.append([(a+b)/2 for a,b in zip(*poss)])
  return [(self.idx(pos,l),pos) for l in ls if l in self.layers for pos in poss]
 def route(self,net,starts,ends,width=.2,vd=.5,timeout=25,masks=None):
  ms,vm=masks or self.masks(net,width,vd);ny,nx=self.shape
  valid=lambda k:0<=k[1]<ny and 0<=k[2]<nx and not ms[k]
  sp={k:(a,pos) for a in starts for k,pos in self.ports(a) if valid(k)};ep={k:(a,pos) for a in ends for k,pos in self.ports(a) if valid(k)}
  if not sp or not ep:return None
  ekeys=list(ep);endpos=np.array([[k[1],k[2]] for k in ekeys]);lo=endpos.min(axis=0);hi=endpos.max(axis=0)
  def heur(k):
   dy=max(lo[0]-k[1],0,k[1]-hi[0]);dx=max(lo[1]-k[2],0,k[2]-hi[1]);return max(dx,dy)+.41421356*min(dx,dy)
  counter=itertools.count();pq=[];cost={};prev={};end=None;t0=time.monotonic()
  for k in sp:cost[k]=0;heapq.heappush(pq,(heur(k),next(counter),0,k))
  while pq:
   _,_,c,k=heapq.heappop(pq)
   if c!=cost.get(k):continue
   if k in ep:end=k;break
   if len(cost)%2000==0 and time.monotonic()-t0>timeout:break
   l,y,x=k
   for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
    yy,xx=y+dy,x+dx
    if not (0<=yy<ny and 0<=xx<nx) or ms[l,yy,xx]:continue
    if dx and dy and (ms[l,y,xx] or ms[l,yy,x]):continue
    q=(l,yy,xx);cc=c+(1.414213562 if dx and dy else 1)
    if cc<cost.get(q,1e99):cost[q]=cc;prev[q]=k;heapq.heappush(pq,(cc+heur(q),next(counter),cc,q))
   if not vm[y,x]:
    for ll in range(len(self.layers)):
     if ll==l or ms[ll,y,x]:continue
     q=(ll,y,x);cc=c+80
     if cc<cost.get(q,1e99):cost[q]=cc;prev[q]=k;heapq.heappush(pq,(cc+heur(q),next(counter),cc,q))
  if end is None:return None
  path=[end]
  while path[-1] in prev:path.append(prev[path[-1]])
  path.reverse();segments=[];vias=[];i=0
  while i<len(path)-1:
   a,b=path[i:i+2]
   if a[0]!=b[0]:vias.append(self.xy(a));i+=1;continue
   direction=(b[1]-a[1],b[2]-a[2]);j=i+1
   while j+1<len(path) and path[j+1][0]==a[0] and (path[j+1][1]-path[j][1],path[j+1][2]-path[j][2])==direction:j+=1
   segments.append({'a':self.xy(a),'b':self.xy(path[j]),'layer':self.layers[a[0]]});i=j
  for k,(item,pos) in ((path[0],sp[path[0]]),(end,ep[end])):
   if math.dist(pos,self.xy(k))>1e-5:segments.append({'a':pos,'b':self.xy(k),'layer':self.layers[k[0]]})
  r={'net':net,'width':width,'via_diameter':vd,'segments':segments,'vias':vias,'length_mm':sum(math.dist(s['a'],s['b']) for s in segments),'start_uuid':sp[path[0]][0].get('uuid'),'end_uuid':ep[end][0].get('uuid')};return r
 def add(self,r):
  for i,s in enumerate(r['segments']):
   t={'uuid':f'proposal-{len(self.g["tracks"])}','net':r['net'],'start':s['a'],'end':s['b'],'width':r['width'],'layer':s['layer'],'via':False,'drill':0};self.g['tracks'].append(t);self.trackshapes[t['uuid']]=LineString([s['a'],s['b']])
  for v in r['vias']:
   t={'uuid':f'proposal-{len(self.g["tracks"])}','net':r['net'],'start':v,'end':v,'width':r['via_diameter'],'layer':0,'via':True,'drill':.3};self.g['tracks'].append(t);self.trackshapes[t['uuid']]=Point(v)

def propose(root,out,include=None,exclude=()):
 c=root/'checks';g=json.loads((c/'geometry_current.json').read_text());r=Router(g,layers=tuple(int(x) for x in os.getenv('LAYERS','0,4,2').split(',')),step=float(os.getenv('GRID','.1'))); items={x['uuid']:x for x in g['pads']+g['tracks']};groups={}
 for ids in g['components']:
  members=[items[u] for u in ids if u in items];net=members[0]['net'] if members else ''
  if members and any('pos' in a and a.get('number') for a in members) and net and not net.startswith('unconnected-'):groups.setdefault(net,[]).append(members)
 routes=[];failed=[]
 for net,gg in sorted(groups.items(),key=lambda kv: (not kv[0].startswith('EPD_'),-len(kv[1]))):
  if len(gg)<2 or net in exclude or (include is not None and net not in include):continue
  gg.sort(key=len,reverse=True);main=gg.pop(0)
  while gg:
   target=gg.pop(0);s=sorted(main,key=lambda x: 0 if 'pos' in x else 1)[:65];e=sorted(target,key=lambda x: 0 if 'pos' in x else 1)[:65]
   result=r.route(net,s,e,timeout=30)
   if result is None:failed.append(net);print('FAIL',net,len(s),len(e),flush=True);continue
   r.add(result);routes.append(result);main+=target;main+=g['tracks'][-(len(result['segments'])+len(result['vias'])):];print('PLAN',net,round(result['length_mm'],2),len(result['vias']),flush=True)
   (c/out).write_text(json.dumps({'routes':routes,'failed':failed,'in_progress':True},indent=2))
 (c/out).write_text(json.dumps({'routes':routes,'failed':failed},indent=2));print('TOTAL',len(routes),'failed',failed)
if __name__=='__main__':propose(Path(sys.argv[1]).resolve(),sys.argv[2],exclude={'USB_DM','USB_DP','USB_DM_CONN','USB_DP_CONN'})
