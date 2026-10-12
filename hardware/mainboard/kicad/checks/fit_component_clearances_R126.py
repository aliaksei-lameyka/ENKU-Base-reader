"""Local fit adjustments required by correctly oriented R126 lands.

Every existing copper UUID and net is retained. Endpoint changes are explicitly
recorded, and the final source guard forbids every other copper edit.
"""
import json
from pathlib import Path
import pcbnew as p
r=Path(__file__).resolve().parents[1];c=r/'checks';path=r/'enku-mainboard-r0.1.kicad_pcb';b=p.LoadBoard(str(path))
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
def vec(x):return p.VECTOR2I(*(int(round(a*1e6)) for a in x))
plan=json.loads((c/'applied_component_pass_R126.json').read_text());changes=[];placements={}
# Use .10 mm courtyard excess beyond maximum body/nominal lands; adjust crowded bodies
# and all required physical routes instead of relaxing global design rules.
moves={'R36':[29.1,70],'R12':[53.3,94.2],'R16':[55.45,95.5],'D1':[49.25,44],'C12':[63.125,94.4],'R13':[69,85.3],'C2':[36.5,91.85],'C6':[45.5,93],'R10':[51.8,89.4],'R15':[53.9,88.3]}
for f in b.GetFootprints():
 ref=f.GetReference()
 if ref in moves:
  placements[ref]=dict(before=xy(f.GetPosition()),after=moves[ref]);f.SetPosition(vec(moves[ref]))
  for a in f.Pads():
   q=next(x for x in plan['declared_pads'] if x['uuid']==a.m_Uuid.AsString());q['after_position']=xy(a.GetPosition())
# Move a route vertex and every attached segment on every copper layer.
vertices=[
 ('BAT_ADC_SW',[28.5,86],[28.6,86.1]),
 ('3V3_SYS',[29.0,70.5],[29.0,70.6]),
 ('I2C_SDA',[25.5,76.4],[25.5,76.45]),
 ('EPD_RST_PANEL',[30.4,69.3],[30.35,69.2]),
 ('EPD_RST',[42.6,28.3],[43.0,29.7]),
 ('EPD_VGH',[51.55,46.35],[51.1,46.35]),
 ('EPD_VGL',[53.05,42.45],[53.0,42.45]),
 ('CHG_STAT1',[50.6,93.9],[51.8,96.0]),
 ('3V3_SYS',[52.45,92.7],[52.6,92.7]),
 ('3V3_SYS',[52.45,93.95],[52.6,93.95]),
 ('EPD_CP_NEG',[56.95,51.1],[56.95,50.95]),
 ('EPD_CP_NEG',[57.85,51.1],[57.85,50.95]),
 ('EPD_SW',[58.2,52.95],[58.2,53.0]),
 ('EPD_SW',[59.8,52.95],[59.8,53.0]),
 ('EPD_CS',[35.55,27.05],[35.5,27.05]),
 ('SYS_EN',[63.45,87.5],[63.4,87.5]),
 ('3V3_SYS',[57.0,95.25],[57.4,95.25]),
 ('3V3_SYS',[57.0,96.0],[57.3,96.15]),
 ('REG_FB',[54.5,87.5],[54.6,87.5]),
 ('REG_FB',[54.5,89.1],[54.6,89.1]),
 ('SYS_EN',[69,87.8],[69,86.15]),
 ('GND',[69,86.2],[69,84.45]),
 ('GND',[69,86.0],[69.7,84.8]),
 ('GND',[68.1,86.2],[68.0,86.2]),
 ('VBUS_USB',[35.5,92.5],[35.575,91.85]),
 ('GND',[37.5,92.5],[37.425,91.85]),
 ('VBUS_USB',[45.3,93],[44.75,93]),
 ('GND',[46.9,93],[46.25,93]),
 ('VBUS_USB',[47.4,91.8],[47.35,91.8])
]
for t in b.GetTracks():
 before=[xy(t.GetStart()),xy(t.GetEnd())];after=[list(x) for x in before]
 for net,a,z in vertices:
  if t.GetNetname()!=net:continue
  after=[z if x==a else x for x in after]
 if before!=after:
  if isinstance(t,p.PCB_VIA):t.SetPosition(vec(after[0]))
  else:t.SetStart(vec(after[0]));t.SetEnd(vec(after[1]))
  changes.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),before=before,after=after))
p.SaveBoard(str(path),b)
plan['routed_copper_changes']=changes;plan['footprint_placement_changes']=placements
(c/'applied_component_pass_R126.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps(dict(copper_items_adjusted=len(changes),footprints_moved=placements),indent=2))
