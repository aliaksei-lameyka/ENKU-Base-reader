"""Create reviewable 45-degree local routes around actual copper polygons."""
import heapq,json,math,sys,uuid
from pathlib import Path
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
from shapely.prepared import prep
r=Path(__file__).resolve().parent;g=json.loads((r/'geometry_current.json').read_text());tracks={x['uuid']:x for x in g['tracks']}
ids=sys.argv[1:] or ['2186658d-bc83-46c7-b517-d72a4a9bda73','4e6f34d5-6b86-4892-b727-aedab2b28bc4','80d5b259-c146-4aa5-a4ee-f1f9ca33602c','e7ee3f6b-f80c-48b0-b942-675f5e968c09','1c466c37-d401-43a7-a402-9e830a4676b0','9ac36e45-9bc5-4684-bb84-13f0514ff658','f8811c90-983a-41ec-b746-068517db2deb','8ea5e584-ab02-4357-9e11-1608a1fdb98c']
output=[];step=.05
# Remove the superseded straight segments before solving. Each solved route is
# inserted into the obstacle geometry immediately, so subsequent foreign nets
# must clear the final copper rather than a temporary, invalid old lead.
g['tracks']=[q for q in g['tracks'] if q['uuid'] not in ids]
for uid in ids:
 t=tracks[uid];assert not t['via'];net,layer,width=t['net'],t['layer'],t['width'];start,end=t['start'],t['end'];shapes=[]
 for q in g['pads']:
  if q['net']!=net and str(layer) in q['polygons']:shapes.extend(Polygon(x) for x in q['polygons'][str(layer)])
 for q in g['tracks']:
  if q['net']==net or not(q['via'] or q['layer']==layer):continue
  shapes.append(Point(q['start']).buffer(q['width']/2,resolution=24) if q['via'] else LineString([q['start'],q['end']]).buffer(q['width']/2,resolution=24))
 obstacle=unary_union(shapes).buffer(width/2+.2-2e-8,resolution=24);prepared=prep(obstacle)
 assert not prepared.contains(Point(start)) and not prepared.contains(Point(end)),(uid,'Endpoint is inside foreign copper clearance',start,end)
 goal=(round((end[0]-start[0])/step),round((end[1]-start[1])/step));assert math.dist([start[0]+goal[0]*step,start[1]+goal[1]*step],end)<1e-7
 def pt(q):return (round(start[0]+q[0]*step,6),round(start[1]+q[1]*step,6))
 def h(q):return math.hypot(q[0]-goal[0],q[1]-goal[1])
 path=None
 for margin in [2,4,7]:
  box=[min(start[0],end[0])-margin,min(start[1],end[1])-margin,max(start[0],end[0])+margin,max(start[1],end[1])+margin]
  queue=[(h((0,0)),0,(0,0))];best={(0,0):0};prev={};cache={};n=0
  while queue:
   _,cost,q=heapq.heappop(queue)
   if cost!=best[q]:continue
   if q==goal:
    path=[q]
    while q!=(0,0):q=prev[q];path.append(q)
    path.reverse();break
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
    z=(q[0]+dx,q[1]+dy);p=pt(z)
    if not(box[0]<=p[0]<=box[2] and box[1]<=p[1]<=box[3]):continue
    edge=tuple(sorted([q,z]))
    if edge not in cache:cache[edge]=not prepared.intersects(LineString([pt(q),p]))
    if not cache[edge]:continue
    turn=.4 if q in prev and (q[0]-prev[q][0],q[1]-prev[q][1])!=(dx,dy) else 0
    nc=cost+math.hypot(dx,dy)+turn
    if nc+1e-9<best.get(z,float('inf')):best[z]=nc;prev[z]=q;heapq.heappush(queue,(nc+h(z),nc,z))
   n+=1
  if path is not None:break
 assert path is not None,(uid,'No legal local route')
 corners=[path[0]]
 for i in range(1,len(path)-1):
  if (path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(path[i+1][0]-path[i][0],path[i+1][1]-path[i][1]):corners.append(path[i])
 corners.append(path[-1]);pts=[list(pt(x)) for x in corners]
 output.append(dict(uuid=uid,net=net,layer=layer,width=width,before=[start,end],points=pts))
 for i,(a,z) in enumerate(zip(pts,pts[1:])):
  g['tracks'].append(dict(uuid=uid+'-planned-'+str(i),net=net,layer=layer,width=width,start=a,end=z,via=False))
 print(uid,net,len(pts)-1,pts,flush=True)
(r/'local_routes_R126.json').write_text(json.dumps(output,indent=2)+'\n')
