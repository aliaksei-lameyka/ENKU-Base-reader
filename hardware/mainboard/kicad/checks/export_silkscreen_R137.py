import collections,json,sys
from pathlib import Path
import pcbnew as p
b=p.LoadBoard(sys.argv[1]);rows=[]
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
for ref,items in [('BOARD',b.GetDrawings())]+[(f.GetReference(),list(f.GetFields())+list(f.GraphicalItems())) for f in b.GetFootprints()]:
 for a in items:
  if a.GetLayer() not in (p.F_SilkS,p.B_SilkS):continue
  text=isinstance(a,p.PCB_TEXT)
  if text and (not a.IsVisible() or not a.GetShownText(True)):continue
  row=dict(ref=ref,uuid=a.m_Uuid.AsString(),type=a.GetClass(),layer=b.GetLayerName(a.GetLayer()))
  if text:row.update(text=a.GetShownText(True),size_mm=xy(a.GetTextSize()),position_mm=xy(a.GetPosition()),pen_mm=p.ToMM(a.GetEffectiveTextPenWidth()),nominal_pen_mm=p.ToMM(a.GetTextThickness()),mirrored=a.IsMirrored())
  else:row.update(width_mm=p.ToMM(a.GetWidth()),shape=str(a.GetShape()),start_mm=xy(a.GetStart()),end_mm=xy(a.GetEnd()))
  rows.append(row)
Path(sys.argv[2]).write_text(json.dumps(dict(native_kicad=p.Version(),enabled_layer_ids=list(b.GetEnabledLayers().Seq()),items=rows),indent=2)+'\n')
print('Native visible silk',len(rows),'pen widths',dict(collections.Counter(x.get('pen_mm',x.get('width_mm')) for x in rows)))
print('Too thin',sum(x.get('pen_mm',x.get('width_mm'))<.15 for x in rows),'too small',sum(min(x['size_mm'])<.8 for x in rows if 'size_mm' in x))
print('Text with implicit strokes:',[(x['ref'],x['text'],x['nominal_pen_mm'],x['pen_mm']) for x in rows if 'pen_mm'in x and x['nominal_pen_mm']==0])
