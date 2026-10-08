#!/usr/bin/env python3
"""Reproducibly fill the legacy R38 or dual R41 GND reference zones using native pcbnew.

Only run on a disposable KiCad board working copy. This is engineering
diagnostic data, not PCBWay Gerbers or final reference-plane qualification.
A failed import, fill, or zero-area zone MUST fail the CI.
"""
import pathlib
import json
import shutil
import sys
if len(sys.argv)!=3:
    raise SystemExit("usage: refill_r38_zone.py path/to/temporary-board.kicad_pcb /tmp/diagnostic.kicad_pcb")
src=pathlib.Path(sys.argv[1])
artifact=pathlib.Path(sys.argv[2])
try:
    import pcbnew
except ImportError as exc:
    raise SystemExit("Native KiCad Python pcbnew not available; R38 zone fill BLOCKED") from exc
board=pcbnew.LoadBoard(str(src))
zones=list(board.Zones())
if len(zones) not in (1,2):
    raise SystemExit(f"Expected one legacy ground island or two R41 reference zones, got {len(zones)}")
expected={pcbnew.In2_Cu} if len(zones)==1 else {pcbnew.In1_Cu,pcbnew.In2_Cu}
if {z.GetLayer() for z in zones}!=expected or any(z.GetNetname()!="GND" for z in zones):
    raise SystemExit("Ground zone net/layer mismatch")
filler=pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
for z in zones:
    if not z.IsFilled() or z.GetFilledPolysList(z.GetLayer()).OutlineCount()==0:
        raise SystemExit("Native KiCad ground zone fill failed")
    print("GROUND FILL PASS:",board.GetLayerName(z.GetLayer()),z.GetFilledPolysList(z.GetLayer()).OutlineCount(),"polygons")
pcbnew.SaveBoard(str(src),board)
shutil.copyfile(src,artifact)
# Re-open the exact DRC input and confirm saved fill survived serialization.
check=pcbnew.LoadBoard(str(src))
if {z.GetLayer() for z in check.Zones()}!=expected or any(z.GetNetname()!="GND" for z in check.Zones()):
    raise SystemExit("Saved ground zone net/layer mismatch")
report=[]
for z2 in check.Zones():
    if not z2.IsFilled() or z2.GetFilledPolysList(z2.GetLayer()).OutlineCount()==0:
        raise SystemExit("Saved ground zone does not retain valid fill")
    report.append({"layer":check.GetLayerName(z2.GetLayer()),"layer_id":int(z2.GetLayer()),"net":z2.GetNetname(),"filled":bool(z2.IsFilled()),"outline_count":z2.GetFilledPolysList(z2.GetLayer()).OutlineCount()})
pathlib.Path("/tmp/r41-ground-fill.json").write_text(json.dumps(report,indent=2)+"\n")
print("SAVED GROUND FILL PASS: exact DRC input retains native fill; artifact:",artifact)
