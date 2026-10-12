"""Independent Gerbonara image composition, including clear macros and regions."""
import re
import numpy as np
import shapely as sh
from shapely.geometry import Point,Polygon,LineString
from gerbonara import graphic_primitives as gp
from gerbonara.utils import MM
def normalize_copper(data):
 s=data.decode();s,n=re.subn(r'(?m)^(%TF\.CreationDate,)[^*]+(\*%)$',r'\1EXPORT_TIMESTAMP\2',s);assert n==1
 s,n=re.subn(r'(?m)^(G04 Created by KiCad \(PCBNEW 10\.0\.7\) date )[^*]+(\*)$',r'\1EXPORT_TIMESTAMP\2',s);assert n==1
 return s.encode()
def primitive_shape(p):
 if isinstance(p,gp.Circle):return Point(p.x,p.y).buffer(p.r,quad_segs=128)
 if isinstance(p,gp.Line):return LineString([(p.x1,p.y1),(p.x2,p.y2)]).buffer(p.width/2,quad_segs=128)
 q=p if isinstance(p,gp.ArcPoly)else p.to_arc_poly();return sh.make_valid(Polygon(q.approximate_arcs(max_error=.0001).outline))
def object_shape(obj):
 # Gerbonara primitives carry the object's outer polarity, inverted for
 # clear macro primitives. Recover relative macro polarity before applying
 # the sequential layer polarity to the complete object shape.
 shape=Polygon()
 for p in obj.to_primitives(MM):
  q=primitive_shape(p)
  shape=shape.union(q)if p.polarity_dark==obj.polarity_dark else shape.difference(q)
 return shape
def layer_shape(file):
 shape=Polygon();group=[];polarity=None
 def apply(base,objects,dark):
  u=sh.union_all(objects);return base.union(u)if dark else base.difference(u)
 for obj in file.objects:
  if polarity is not None and obj.polarity_dark!=polarity:shape=apply(shape,group,polarity);group=[]
  polarity=obj.polarity_dark;group.append(object_shape(obj))
 return apply(shape,group,polarity)if group else shape

def discrete_hausdorff(a,b):
 """Exact vertex-to-segment metric, spatially indexed instead of quadratic.

 GEOS's undensified discrete Hausdorff examines all boundary vertices in
 both directions. STRtree preserves that metric while avoiding exhaustive
 comparisons between the many thousands of copper boundary segments.
 """
 def boundary(g):
  rings=list(sh.get_parts(sh.boundary(g)));coordinates=[sh.get_coordinates(p)for p in rings]
  assert coordinates and all(len(c)>=2 for c in coordinates)
  segments=np.concatenate([np.stack([c[:-1],c[1:]],axis=1)for c in coordinates])
  return sh.points(np.concatenate(coordinates)),sh.STRtree(sh.linestrings(segments))
 pa,ta=boundary(a);pb,tb=boundary(b)
 return max(float(tb.query_nearest(pa,all_matches=False,return_distance=True)[1].max()),float(ta.query_nearest(pb,all_matches=False,return_distance=True)[1].max()))
