"""Correct J3 from the supplied Hirose EDC-159714-50-08 PCB/stencil drawing."""
import json,sys,re
from pathlib import Path
import pcbnew as p
from native_board import xy,iu
def layers(ids):
 s=p.LSET()
 for l in ids:s.AddLayer(l)
 return s
root=Path(sys.argv[1]).resolve();c=root/'checks';trial=root/'trials/j3_land_pattern';trial.mkdir(parents=True,exist_ok=True)
for x in root.iterdir():
 if x.suffix in ('.kicad_sch','.kicad_pro','.kicad_dru','.kicad_sym') or x.name.endswith('.pretty') or x.name in ('fp-lib-table','sym-lib-table','standard-footprints','standard-symbols'):
  dest=trial/x.name
  if not dest.exists():dest.symlink_to(x)
b=p.LoadBoard(str(root/'enku-mainboard-r0.1.kicad_pcb'));f=next(f for f in b.GetFootprints() if f.GetReference()=='J3');before={a.GetNumber():xy(a.GetPosition()) for a in f.Pads() if a.GetNumber()};assert xy(f.GetPosition())==[69.37,34.0]
f.SetPosition(p.VECTOR2I(iu(69.27),iu(34)));mapping={tuple(old):xy(next(a for a in f.Pads() if a.GetNumber()==n).GetPosition()) for n,old in before.items()};paste=[]
for a in list(f.Pads()):
 if a.GetNumber().isdigit():
  a.SetLocalSolderPasteMargin(iu(.005));a.SetLocalSolderPasteMarginRatio(-.1);margin=xy(a.GetSolderPasteMargin(p.F_Cu));dims=[x+2*y for x,y in zip(xy(a.GetSize()),margin)];assert all(abs(x-y)<1e-6 for x,y in zip(dims,[.25,.65]));paste.append({'pin':a.GetNumber(),'size':dims,'pos':xy(a.GetPosition())})
 elif a.GetNumber() in ('S1','S2'):
  a.SetSize(p.VECTOR2I(iu(.8),iu(.8)));a.SetLayerSet(layers([p.F_Cu,p.F_Mask]));ap=p.PAD(f);ap.SetNumber('');ap.SetAttribute(p.PAD_ATTRIB_SMD);ap.SetShape(p.PAD_SHAPE_RECT);ap.SetSize(p.VECTOR2I(iu(.8),iu(.65)));ap.SetLayerSet(layers([p.F_Paste]));ap.SetPosition(a.GetPosition());f.Add(ap);paste.append({'pin':a.GetNumber(),'size':[.8,.65],'pos':xy(ap.GetPosition()),'paste_only_pad_uuid':ap.m_Uuid.AsString()})
mapping[(62,35.25)]=[61.7,35.25];changes=[]
for t in b.GetTracks():
 old_a,old_d=xy(t.GetStart()),xy(t.GetEnd());pos=[]
 for point in (old_a,old_d):
  new=mapping.get(tuple(point),point)
  if new==point and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and 63.3<=point[0]<=75.3 and 32.15<=point[1]<=33.4 and (t.GetNetname().startswith('EPD_') or t.GetNetname() in ('GND','3V3_SYS')):new=[point[0]-.1,point[1]]
  pos.append(new)
 if pos!=[old_a,old_d]:
  if isinstance(t,p.PCB_VIA):t.SetPosition(p.VECTOR2I(*(iu(x) for x in pos[0])))
  else:t.SetStart(p.VECTOR2I(*(iu(x) for x in pos[0])));t.SetEnd(p.VECTOR2I(*(iu(x) for x in pos[1])))
  changes.append({'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'before':[old_a,old_d],'after':pos})
b.GetTitleBlock().SetRevision('R120 - ENGINEERING / NO FAB');p.SaveBoard(str(trial/'enku-mainboard-r0.1.kicad_pcb'),b)
(c/'j3_land_pattern_changes.json').write_text(json.dumps({'source':'Hirose EDC-159714-50-08, page 1 recommended PCB/stencil; supplied exact 24S drawing','J3_origin_before':[69.37,34],'J3_origin_after':[69.27,34],'reason_for_shift':'Keep nominal 0.8x0.8 reinforcement lands at least 0.5 mm from PCB edge.','reinforcement_lands_before':[.4,.8],'reinforcement_lands_after':[.8,.8],'paste_apertures':paste,'copper_endpoint_changes':changes},indent=2))
lib=root/'ENKU.pretty/FH34SRJ-24S-0.5SH.kicad_mod';s=lib.read_text();assert '(size 0.4 0.8)' in s
ls=[]
for line in s.splitlines():
 if '(pad "S' in line:line=line.replace('(size 0.4 0.8)','(size 0.8 0.8)').replace('(layers "F.Cu" "F.Paste" "F.Mask")','(layers "F.Cu" "F.Mask")')
 elif re.search(r'\(pad "\d+"',line):line=line[:-1]+' (solder_paste_margin 0.005) (solder_paste_margin_ratio -0.1))'
 ls.append(line)
ls[-1:-1]=['  (pad "" smd rect (at 6.75 1.25) (size 0.8 0.65) (layers "F.Paste"))','  (pad "" smd rect (at -6.75 1.25) (size 0.8 0.65) (layers "F.Paste"))'];lib.write_text('\n'.join(ls)+'\n')
print('Corrected J3 PCB lands and 26 stencil apertures;',len(changes),'declared copper endpoint changes; trial requires full native verification')
