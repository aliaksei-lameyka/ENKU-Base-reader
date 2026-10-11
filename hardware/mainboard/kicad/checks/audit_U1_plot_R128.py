"""Independently inspect actual native mask/paste SVGs, including via tents.

Uses the native board bounding box for KiCad's board-area plot origin.
These are drawing requests; an absent opening does not prove a sealed via.
"""
import gzip, hashlib, json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union
from shapely import affinity

root = Path(sys.argv[1]).resolve(); c = root / 'checks'
server = len(sys.argv) > 2; out = Path(sys.argv[2]).resolve() if server else c
g = (json.loads((out / 'geometry.json').read_text()) if server else
     json.loads(gzip.decompress((c / 'geometry_checkpoint_R128.json.gz').read_bytes())))
ox, oy = g['bbox'][:2]
roi = box(33.5-ox, 44.5-oy, 37.4-ox, 48.5-oy)
centres = [(x-ox,y-oy) for x in (34.06,35.46,36.86) for y in (45.1,46.5,47.9)]
expected = unary_union([box(x-.4,y-.4,x+.4,y+.4) for x,y in centres])
thermal = [(x-ox,y-oy) for x in (34.76,36.16) for y in (45.1,46.5,47.9)]
thermal += [(x-ox,y-oy) for x in (34.06,35.46,36.86) for y in (45.8,47.2)]
number = r'[-+]?(?:\d*\.\d+|\d+)'

def actual_shapes(path):
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

plots = {}; results = {}
for layer in ('F_Mask','F_Paste','B_Mask'):
    path = out / (f'{layer}.svg' if server else f'native_{layer}_R128.svg')
    shapes = actual_shapes(path); actual = unary_union(shapes)
    target = expected if layer != 'B_Mask' else Polygon()
    assert actual.symmetric_difference(target).area < 1e-7,(layer,'Unexpected EP openings',actual.area)
    assert len(shapes) == (9 if layer != 'B_Mask' else 0),(layer,len(shapes))
    assert actual.is_empty or all(actual.distance(Point(x,y)) >= .29999 for x,y in thermal),(layer,'Thermal drill opening')
    plots[layer] = hashlib.sha256(path.read_bytes()).hexdigest()
    results[layer] = {'EP_opening_count':len(shapes),'EP_opening_area_mm2':round(actual.area,8)}
report = {'revision':'R128','pcb_sha256':hashlib.sha256((root/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),
          'actual_native_U1_mask_paste_plots_match':True,'native_plot_origin_mm':[ox,oy],
          'layers':results,'plot_sha256':plots,
          'actual_native_both_mask_layers_have_no_thermal_drill_openings':True,
          'filled_plugged_capped_or_sealed_tents_proven':False,'assembly_process_qualified':False,'fabrication_ready':False}
dest = out / ('U1_plot_audit.json' if server else 'U1_plot_audit_R128.json')
dest.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
