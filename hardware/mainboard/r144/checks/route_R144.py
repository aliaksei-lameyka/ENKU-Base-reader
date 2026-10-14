"""Conservative geometric R144 proposal. Native DRC is the acceptance gate."""
from pathlib import Path
import json,sys,math
import numpy as np
from scipy.ndimage import binary_dilation
from scipy.spatial import cKDTree
repo=Path(__file__).resolve().parents[4];common=repo/'hardware/mainboard/kicad/checks';sys.path[:0]=[str(repo/'hardware/mainboard/r143/checks'),str(common)]
from proposal_routing_R143 import ProposalRouter
from pad_groups import components
class R144Router(ProposalRouter):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);original=self.r.ports
  def ports(item):
   if item.get('ref')=='U11' and item['number']:
    sign=-1 if int(item['number'])<=3 else 1;pos=[item['pos'][0]+sign*.25,item['pos'][1]]
    return [(self.r.idx(pos,0),pos)]+original(item)
   return original(item)
  self.r.ports=ports
 def masks(self,net,width,front=False):
  ms,vm=super().masks(net,width,front)
  # Expand the 0.50mm proposal mask for actual 0.60/0.30mm vias.
  vm=binary_dilation(vm,iterations=max(1,math.ceil(.05/self.r.step)))
  return ms,vm
 def add(self,plan,net,starts,ends,width=.2,front=False,timeout=45):
  result=self.r.route(net,starts,ends,width=width,vd=.6,timeout=timeout,masks=self.masks(net,width,front))
  if result is None:raise RuntimeError('No safe proposal for '+net)
  plan['routes'].append(result);before=len(self.g['tracks']);self.r.add(result)
  print('Route',net,round(result['length_mm'],3),'mm',len(result['vias']),'vias',flush=True)
  return result,self.g['tracks'][before:]
def points(group):return np.array([q for a in group for q in([a['pos']]if'pos'in a else[a['start'],a['end']])])
def run(native,out,nets):
 g=json.loads((native/'geometry.json').read_text());by={}
 for group in components(g):
  if group and group[0]['net']and not group[0]['net'].startswith('unconnected-'):by.setdefault(group[0]['net'],[]).append(group)
 plan=dict(routes=[],remove_tracks=[],fabrication_ready=False)
 router=R144Router(g,common,[32,53,66,103],step=.05)
 for net in nets:
  groups=by.get(net,[])
  if len(groups)<2:continue
  main=next((q for q in groups if any(a.get('ref')=='U11'for a in q)),max(groups,key=len))if net in ['RESET_SENSE','RESET_CT']else max(groups,key=len)
  rest=[q for q in groups if q is not main]
  while rest:
   distances=[float(cKDTree(points(main)).query(points(q))[0].min())for q in rest];target=rest.pop(int(np.argmin(distances)))
   # Limit starts to physically nearby objects without hiding routing obstacles.
   tree=cKDTree(points(target));near=sorted(main,key=lambda a:float(tree.query(points([a]))[0].min()))[:100]
   _,new=router.add(plan,net,near,target,front=net in ['RESET_SENSE','RESET_CT'],timeout=55)
   main=main+target+new;out.write_text(json.dumps(plan,indent=2)+'\n')
 out.write_text(json.dumps(plan,indent=2)+'\n')
if __name__=='__main__':run(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3:]or['RESET_SENSE','RESET_CT','GND','3V3_SYS','ESP_EN','REG_FB_TOP','REG_MODE'])
