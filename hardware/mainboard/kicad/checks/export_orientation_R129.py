"""Native service-label and J7 orientation features for independent CI checks."""
import json, sys
from pathlib import Path
import pcbnew as p
b=p.LoadBoard(sys.argv[1]); rows=[]
def xy(v): return [p.ToMM(v.x),p.ToMM(v.y)]
for f in b.GetFootprints():
    if f.GetReference()=='J7':
        for a in f.GraphicalItems():
            if a.GetLayer()==p.B_SilkS:
                rows.append(dict(ref='J7',type='pin1_line',uuid=a.m_Uuid.AsString(),layer=a.GetLayer(),
                                 start_mm=xy(a.GetStart()),end_mm=xy(a.GetEnd()),width_mm=p.ToMM(a.GetWidth())))
    if f.GetReference().startswith('TP'):
        a=f.GetField('Probe Label'); assert a and a.IsVisible()
        rows.append(dict(ref=f.GetReference(),type='probe_label',text=a.GetText(),layer=a.GetLayer(),
                         position_mm=xy(a.GetPosition()),size_mm=xy(a.GetTextSize()),mirrored=a.IsMirrored()))
Path(sys.argv[2]).write_text(json.dumps(dict(native_kicad=p.Version(),features=rows),indent=2)+'\n')
print('Exported native pin1/probe features:',len(rows))
