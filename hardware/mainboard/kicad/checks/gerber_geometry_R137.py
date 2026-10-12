"""Independent Gerbonara -> Shapely rendering of positive native aperture objects."""
import collections,re
from gerbonara import graphic_primitives as gp
from gerbonara.utils import MM
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union

def primitive_shape(primitive):
 if isinstance(primitive,gp.Circle):return Point(primitive.x,primitive.y).buffer(primitive.r,quad_segs=128)
 if isinstance(primitive,gp.Line):return LineString([(primitive.x1,primitive.y1),(primitive.x2,primitive.y2)]).buffer(primitive.width/2,quad_segs=128)
 polygon=primitive if isinstance(primitive,gp.ArcPoly)else primitive.to_arc_poly()
 shape=Polygon(polygon.approximate_arcs(max_error=.0001).outline)
 assert shape.is_valid,'Invalid independently parsed Gerber primitive'
 return shape

def object_shape(obj):
 assert obj.polarity_dark,'Unexpected clear object in mask/paste/legend aperture image'
 shapes=[]
 for primitive in obj.to_primitives(MM):
  assert primitive.polarity_dark,'Unexpected clear macro primitive'
  shapes.append(primitive_shape(primitive))
 return unary_union(shapes)

def layer_shape(file):return unary_union([object_shape(obj)for obj in file.objects])

def normalize_copper(data):
 text=data.decode()
 text,n=re.subn(r'(?m)^(%TF\.CreationDate,)[^*]+(\*%)$',r'\1EXPORT_TIMESTAMP\2',text);assert n==1
 text,n=re.subn(r'(?m)^(G04 Created by KiCad \(PCBNEW 10\.0\.7\) date )[^*]+(\*)$',r'\1EXPORT_TIMESTAMP\2',text);assert n==1
 text,n=re.subn(r'(?m)^(%TF\.ProjectId,enku-mainboard-r0\.1,656e6b75-2d6d-4616-996e-626f6172642d,)(?:R122|R137) - ENGINEERING / NO FAB(\*%)$',r'\1ACCEPTED_REVISION - ENGINEERING / NO FAB\2',text);assert n==1
 return text.encode()
