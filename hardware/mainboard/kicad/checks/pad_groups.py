"""Connected pad partitions, derived independently from native connectivity export."""
import collections
def components(g):
 items={p['uuid']:p for p in g['pads']+g['tracks']};parents={u:u for u in items}
 def f(u):
  while parents[u]!=u:parents[u]=parents[parents[u]];u=parents[u]
  return u
 for group in g['components']:
  us=[u for u in group if u in parents]
  for u in us[1:]:parents[f(u)]=f(us[0])
 groups=collections.defaultdict(list)
 for u,p in items.items():groups[f(u)].append(p)
 return list(groups.values())
def partitions(g):
 out=collections.defaultdict(list)
 for group in components(g):
  pads=[p for p in group if 'pos' in p and p['layers'] and p['net'] and not p['net'].startswith('unconnected-')]
  if pads:out[pads[0]['net']].append(frozenset(p['uuid'] for p in pads))
 return dict(out)
def assert_no_split(before,after):
 a,b=partitions(before),partitions(after)
 for net,groups in a.items():
  for group in groups:assert any(group<=v for v in b.get(net,[])),('Previously connected pads were split',net,sorted(group))
