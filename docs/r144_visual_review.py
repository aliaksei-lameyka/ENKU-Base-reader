"""Read-only visual review maps and same-net geometry candidates. No auto cleanup."""
from pathlib import Path
import collections,csv,gzip,hashlib,json,math,sys,xml.etree.ElementTree as ET
import shapely as sh
from shapely.geometry import LineString,Polygon,Point
from shapely.ops import polygonize
import fitz
repo=Path(__file__).resolve().parents[1];v=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True);source=repo/'hardware/mainboard/r144/kicad/enku-mainboard-r0.1.kicad_pcb';g=json.loads((v/'geometry.json').read_text());sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha==json.loads((v/'verification_R144.json').read_text())['pcb_sha256'];before=source.read_bytes()
layers={0:'F_Cu',4:'In1_Cu',6:'In2_Cu',2:'B_Cu'};titles={0:'TOP COPPER',4:'INNER 1 COPPER',6:'INNER 2 COPPER',2:'BOTTOM COPPER - UNMIRRORED'}
def draw(layer,name):
 root=ET.fromstring((v/(name+'.svg')).read_text());groups_svg=[e for e in root if e.tag.endswith('g')];assert len(groups_svg)>1;inner=''.join(ET.tostring(e,encoding='unicode')for e in root if not e.tag.endswith(('title','desc')));w,h=75,119;x0,y0=8,10;svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">',f'<rect width="{w}" height="{h}" fill="white"/>',f'<text x="8" y="3" font-family="DejaVu Sans" font-size="1.6" fill="#172f45">ENKU R144 - {titles[layer]}</text>',f'<text x="8" y="5.4" font-family="DejaVu Sans" font-size="1.05" fill="#46586b">Board X/Y in mm. Copper source {sha[:12]}. NO FAB.</text>',f'<g transform="translate({x0} {y0})">',inner]
 for poly in g['board_outline']:
  points=' '.join(f'{x-18},{y-20}'for x,y in poly+[poly[0]]);svg.append(f'<polyline points="{points}" fill="none" stroke="#51606d" stroke-width="0.07"/>')
 svg.append('</g>')
 for x in range(18,78):
  px=x0+x-18;major=x%5==0 or x in [18,77];tick=.8 if major else .4
  svg.append(f'<path d="M{px},{y0-1.5}v{-tick} M{px},{y0+102.5}v{tick}" stroke="#607080" stroke-width=".06"/>')
  if major:
   for py in [y0-3.1,y0+105.2]:svg.append(f'<text x="{px}" y="{py}" text-anchor="middle" font-family="DejaVu Sans" font-size="1.2">{x}</text>')
 for y in range(20,122):
  py=y0+y-20;major=y%5==0 or y==121;tick=.8 if major else .4
  svg.append(f'<path d="M{x0-1.5},{py}h{-tick} M{x0+60.5},{py}h{tick}" stroke="#607080" stroke-width=".06"/>')
  if major:
   svg.append(f'<text x="{x0-3}" y="{py+.45}" text-anchor="end" font-family="DejaVu Sans" font-size="1.2">{y}</text>');svg.append(f'<text x="{x0+63}" y="{py+.45}" font-family="DejaVu Sans" font-size="1.2">{y}</text>')
 svg.append(f'<text x="8" y="117" font-family="DejaVu Sans" font-size="1.05">Mark suspected areas with numbered circles. Image scale is not a PCB fabrication scale.</text></svg>');text=''.join(svg);s=out/f'ENKU_R144_{name}_Review_Map.svg';s.write_text(text);d=fitz.open(stream=text.encode(),filetype='svg');pdf=fitz.open(stream=d.convert_to_pdf(),filetype='pdf');png=pdf[0].get_pixmap(matrix=fitz.Matrix(50*25.4/72,50*25.4/72),alpha=False).tobytes('png');assert png.startswith(b'\x89PNG\r\n\x1a\n');(out/f'ENKU_R144_{name}_Review_Map.png').write_bytes(png);pdf.close();d.close()
for layer,name in layers.items():draw(layer,name)
# The native SVG is translated by exactly18,20mm: independently anchor R72.1.
assert next(p for p in g['pads']if p['ref']=='R72'and p['number']=='1')['pos']==[65.15,70.0]
tracks=[t for t in g['tracks']if not t['via']];groups=collections.defaultdict(list)
assert {t['layer']for t in tracks} <= layers.keys()
for t in tracks:groups[(t['net'],t['layer'])].append(t)
faces=[];overlaps=[];duplicates=[]
for (net,layer),ts in groups.items():
 lines=[LineString([t['start'],t['end']])for t in ts];pad_shapes=[Polygon(q)for p in g['pads']if p['net']==net for q in p['polygons'].get(str(layer),[])];pads=sh.union_all(pad_shapes).buffer(.000001)
 for face in polygonize(sh.union_all(lines)):
  area=face.difference(pads.buffer(.02)).area
  if area<.005:continue
  minx,miny,maxx,maxy=face.bounds;near=sorted(g['footprints'],key=lambda ref:face.distance(Point(g['footprints'][ref]['pos'])))[:4];faces.append(dict(net=net,layer=layers[layer],bounds_mm=[minx,miny,maxx,maxy],area_mm2=face.area,area_outside_pads_mm2=area,nearby_refs=near,disposition='REVIEW CANDIDATE; same-net meshes can be intentional'))
 tree=sh.STRtree(lines)
 for i,line in enumerate(lines):
  for jj in tree.query(line):
   j=int(jj)
   if j<=i:continue
   overlap=line.intersection(lines[j]);length=overlap.difference(pads).length
   if length<.05:continue
   equal=line.equals(lines[j])and ts[i]['width']==ts[j]['width'];row=dict(net=net,layer=layers[layer],UUIDs=[ts[i]['uuid'],ts[j]['uuid']],overlap_outside_pads_mm=length,bounds_mm=list(overlap.bounds),disposition='REVIEW CANDIDATE; no automatic removal')
   (duplicates if equal else overlaps).append(row)
def count_faces(coords):return len(list(polygonize(sh.union_all([LineString(x)for x in coords]))))
square=[[(0,0),(1,0)],[(1,0),(1,1)],[(1,1),(0,1)],[(0,1),(0,0)]];assert count_faces(square)==1 and count_faces(square[:-1])==0
assert LineString([(0,0),(2,0)]).intersection(LineString([(1,0),(3,0)])).length==1
report=dict(revision='R144',pcb_sha256=sha,scope='All routed tracks on four copper layers; same-net centerline faces and collinear overlap outside pads',tracks_reviewed=len(tracks),closed_face_candidates=faces,partial_collinear_overlap_candidates=overlaps,exact_duplicate_candidates=duplicates,synthetic_closed_open_overlap_cases='PASS',limitations=['Candidate detector, not a functional defect verdict','Filled-plane mesh, pad spreading, width transitions and intentional parallel current paths require manual review','No copper, via, pad, clearance or source change made','No physical or dynamic qualification performed'],fabrication_ready=False)
report['input_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [v/'geometry.json',v/'verification_R144.json',*[v/(name+'.svg')for name in layers.values()]]}
for prefix,items in [('C',faces),('O',overlaps),('D',duplicates)]:
 for n,a in enumerate(items,1):a['id']=f'{prefix}{n:03}'
(out/'VISUAL_REVIEW_CANDIDATES_R144.json').write_text(json.dumps(report,indent=2)+'\n')
rows=[]
for kind,items in [('closed_face',faces),('partial_overlap',overlaps),('exact_duplicate',duplicates)]:
 for a in items:rows.append([a['id'],kind,a['net'],a['layer'],*a['bounds_mm'],a.get('area_mm2',''),a.get('overlap_outside_pads_mm',''),','.join(a.get('nearby_refs',[])),','.join(a.get('UUIDs',[])),a['disposition']])
with(out/'VISUAL_REVIEW_CANDIDATES_R144.csv').open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['ID','Candidate','Net','Layer','Min X mm','Min Y mm','Max X mm','Max Y mm','Area mm2','Overlap mm','Nearby refs','Track UUIDs','Disposition']);w.writerows(rows)
assert source.read_bytes()==before
print(json.dumps(dict(tracks_reviewed=len(tracks),closed_face_candidates=len(faces),partial_overlap_candidates=len(overlaps),exact_duplicate_candidates=len(duplicates),closed_faces_by_net=dict(collections.Counter(a['net']for a in faces)),source_unchanged=True)))
