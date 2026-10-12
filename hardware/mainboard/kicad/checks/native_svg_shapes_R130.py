"""Read actual native SVG paths into physical aperture geometry."""
import re, xml.etree.ElementTree as ET
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
from shapely import affinity

number = r'[-+]?(?:\d*\.\d+|\d+)'

def actual_shapes(path, roi):
    result = []
    def walk(e, inherited, transforms):
        style = dict(inherited)
        style.update(dict(s.strip().split(':',1) for s in e.get('style','').split(';') if ':' in s))
        transforms = transforms + ([e.get('transform')] if e.get('transform') else [])
        tag = e.tag.split('}')[-1]; shape = None
        if tag == 'circle':
            shape = Point(float(e.get('cx')),float(e.get('cy'))).buffer(float(e.get('r')), resolution=96)
            if style.get('fill','black') == 'none':
                shape = shape.boundary.buffer(float(style.get('stroke-width',1))/2)
        elif tag == 'path':
            d = e.get('d',''); commands = set(re.findall('[A-Za-z]', d))
            assert commands <= {'M','L','Z'}, ('Unexpected native path commands',path,commands)
            nums = list(map(float,re.findall(number,d)))
            assert len(nums)%2 == 0
            if 'Z' in commands:
                assert d.count('M') == 1 and style.get('fill') != 'none'
                shape = Polygon(list(zip(nums[::2],nums[1::2])))
            elif style.get('stroke','none') != 'none':
                lines = []
                for part in d.split('M')[1:]:
                    n = list(map(float,re.findall(number,part)))
                    if len(n)>=4: lines.append(LineString(list(zip(n[::2],n[1::2]))))
                shape = unary_union(lines).buffer(float(style.get('stroke-width',1))/2)
        if shape is not None:
            for transform in reversed(transforms):
                for op, args in reversed(re.findall(r'(\w+)\(([^)]*)\)',transform)):
                    a = list(map(float,re.findall(number,args)))
                    if op == 'translate': shape = affinity.translate(shape,a[0],a[1] if len(a)>1 else 0)
                    elif op == 'scale': shape = affinity.scale(shape,a[0],a[1] if len(a)>1 else a[0],origin=(0,0))
                    elif op == 'rotate': shape = affinity.rotate(shape,a[0],origin=tuple(a[1:]) if len(a)==3 else (0,0))
                    else: raise AssertionError(('Unexpected native SVG transform',op))
            if shape.intersects(roi): result.append(shape.intersection(roi))
        for child in e: walk(child,style,transforms)
    walk(ET.parse(path).getroot(),{},[])
    return result

