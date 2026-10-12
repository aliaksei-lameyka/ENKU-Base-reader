"""Reconstruct the interrupted R119 layout from immutable R118 and its handoff."""
import json,sys
from pathlib import Path
import pcbnew as p
from native_board import apply,xy
root=Path(sys.argv[1]).resolve(); c=root/'checks'; source=root.parent/'ENKU_R118'
g=json.loads((source/'checks/geometry_final.json').read_text())
moves={'SW3':([21.5,73],270),'SW4':([21.5,85],270),'SW5':([73.5,73],90),'SW6':([73.5,85],90),'H1':([29,22.5],0),'U9':([35.5,70],0),'C37':([38.5,67],0),'R39':([35.5,73],0),'R25':([26,73],90),'R24':([26,76.5],90),'C28':([73.12,28.5],90),'TP10':([66,46],0),'R64':([44.25,56.5],90),'R65':([42.98,56.5],90),'U8':([47,108.5],270)}
whole={'BTN_L1','BTN_L2','BTN_R1','BTN_R2','EPD_BUSY','EPD_RST_PANEL','EPD_DC_PANEL','EPD_CS_PANEL','EPD_SCLK_PANEL','EPD_MOSI_PANEL','EPD_BS1','BAT_ADC_SW'}
removed=[]; extra=set(json.loads((c/'restore_extra_remove.json').read_text())) if (c/'restore_extra_remove.json').exists() else set()
for t in g['tracks']:
    a,b=t['start'],t['end']; reason=None
    if t['net'] in whole:reason='Rebuild moved button/ADC and complete J3 fanout'
    if t['uuid'] in extra:reason='Native conflict or obsolete dangling stub after relocation'
    if any(x<=26.55 and 20.5<=y<=69.3 for x,y in (a,b)):reason='RF keepout clearance'
    for pad in g['pads']:
        if pad['ref'] not in moves and pad['ref']!='J7':continue
        # Remove only the lead touching the old pad, preserving remote power branches.
        if any(abs(q[0]-pad['pos'][0])<.03 and abs(q[1]-pad['pos'][1])<.03 for q in (a,b)):reason='Old moved pad lead'
    if t['net'].startswith('EPD_') or t['net']=='3V3_SYS':
        if any(61.8<=x<=76 and 29.5<=y<=38.75 for x,y in (a,b)):reason='J3 through-via escape redraw'
    if t['uuid'] in {'90d4a06e-fbd3-4b15-94d5-ffbab28bceb8','589dd05e-dummy'}:reason='USB source resistor corridor'
    if reason:removed.append({'uuid':t['uuid'],'net':t['net'],'reason':reason})
plan={'remove_tracks':[x['uuid'] for x in removed],'routes':[]}
(c/'restoration_remove.json').write_text(json.dumps(plan,indent=2))
pcb='enku-mainboard-r0.1.kicad_pcb'; apply(source/pcb,c/'restoration_remove.json',root/pcb)
b=p.LoadBoard(str(root/pcb)); fs={f.GetReference():f for f in b.GetFootprints()}
for ref,(pos,angle) in moves.items():
    f=fs[ref];f.SetOrientationDegrees(angle);f.SetPosition(p.VECTOR2I(*(p.FromMM(x) for x in pos)))
for ref in ('SW3','SW4','SW5','SW6'):
    f=fs[ref];f.SetAttributes(p.FP_SMD)
    textpos=[moves[ref][0][0],moves[ref][0][1]+(-4.5 if ref in ('SW3','SW5') else (5.5 if ref=='SW6' else 4.5))]
    f.Reference().SetPosition(p.VECTOR2I(*(p.FromMM(x) for x in textpos))); f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
for ref,pos in {'H1':[31,22.5],'U9':[35.5,66],'C37':[38.5,65.2],'R39':[38.3,73],'R25':[28,73],'R24':[28,76.5],'C28':[73.12,25.8],'TP10':[66,44],'R64':[46.4,56.5],'R65':[41,56.5],'U8':[50,108.5],'J5':[53.8,116.5],'U1':[47,35]}.items():
    f=fs[ref];f.Reference().SetPosition(p.VECTOR2I(*(p.FromMM(x) for x in pos)));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T)); f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));f.Reference().SetTextThickness(p.FromMM(.12))
# Correct the contact rows for a bottom-side physical TC2030, preserving pad identity.
f=fs['J7'];jf={}
for pad in f.Pads():
    if pad.GetNumber():
        before=xy(pad.GetPosition());after=[before[0],174-before[1]];pad.SetPosition(p.VECTOR2I(*(p.FromMM(x) for x in after)));jf[pad.GetNumber()]={'before':before,'after':after}
z=p.ZONE(f);z.SetLayer(p.B_Cu);z.SetIsRuleArea(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(True);z.SetDoNotAllowZoneFills(True)
outline=z.Outline();outline.NewOutline()
for x,y in ((33.73,86.365),(36.27,86.365),(36.27,87.635),(33.73,87.635)):outline.Append(p.FromMM(x),p.FromMM(y))
f.Add(z)
for d in list(b.GetDrawings()):
    if d.GetLayer()==p.Edge_Cuts:b.Remove(d)
edge=[[18,20],[77,20],[77,121],[18,121],[18,55.5],[25.4,55.5],[26.4,54.5],[26.4,35.5],[25.4,34.5],[18,34.5]]
for a,d in zip(edge,edge[1:]+edge[:1]):
    s=p.PCB_SHAPE(b);s.SetShape(p.SHAPE_T_SEGMENT);s.SetLayer(p.Edge_Cuts);s.SetWidth(p.FromMM(.05));s.SetStart(p.VECTOR2I(*(p.FromMM(x) for x in a)));s.SetEnd(p.VECTOR2I(*(p.FromMM(x) for x in d)));b.Add(s)
b.GetTitleBlock().SetRevision('R119 - ENGINEERING / NO FAB');p.SaveBoard(str(root/pcb),b)
(c/'layout_changes_R119.json').write_text(json.dumps({'moves':moves,'removed':removed,'tag_contact_rows':jf,'board_outline':edge,'note':'Reconstructed from R118 and interrupted R119 journal; native validation required.'},indent=2))
print('Layout restored:',len(removed),'copper objects removed; ',len(moves),'footprints relocated')
