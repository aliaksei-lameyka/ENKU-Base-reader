"""Export actual native mask/paste layers, not just the copper geometry."""
import json,sys
from pathlib import Path
import pcbnew as p
b=p.LoadBoard(sys.argv[1]);rows=[]
for f in b.GetFootprints():
 if f.GetReference() not in ['U1','Q1','Q2','U9','J7']:continue
 for a in f.Pads():
  rows.append(dict(ref=f.GetReference(),uuid=a.m_Uuid.AsString(),number=a.GetNumber(),position_mm=[p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)],size_mm=[p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)],drill_mm=[p.ToMM(a.GetDrillSize().x),p.ToMM(a.GetDrillSize().y)],layers=[b.GetLayerName(x) for x in a.GetLayerSet().Seq()],roundrect_radius_mm=p.ToMM(a.GetRoundRectCornerRadius()),attribute=a.GetAttribute(),local_mask_margin_IU=a.GetLocalSolderMaskMargin(),local_paste_margin_IU=a.GetLocalSolderPasteMargin(),local_paste_ratio=a.GetLocalSolderPasteMarginRatio()))
Path(sys.argv[2]).write_text(json.dumps({'native_kicad':p.Version(),'pads':rows},indent=2)+'\n');print('Exported actual assembly pad features:',len(rows))
