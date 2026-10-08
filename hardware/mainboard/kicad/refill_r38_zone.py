#!/usr/bin/env python3
"""Reproducibly fill the single R38 GND return island using native pcbnew.

Only run on a disposable KiCad board working copy. This is engineering
diagnostic data, not PCBWay Gerbers or final reference-plane qualification.
A failed import, fill, or zero-area zone MUST fail the CI.
"""
import pathlib
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
    print("GROUND FILL PASS:",z.GetLayerName(),z.GetFilledPolysList(z.GetLayer()).OutlineCount(),"polygons")
pcbnew.SaveBoard(str(src),board)
shutil.copyfile(src,artifact)
# Re-open the exact DRC input and confirm saved fill survived serialization.
check=pcbnew.LoadBoard(str(src))
for z2 in check.Zones():
    if not z2.IsFilled() or z2.GetFilledPolysList(z2.GetLayer()).OutlineCount()==0:
        raise SystemExit("Saved ground zone does not retain valid fill")
print("SAVED GROUND FILL PASS: exact DRC input retains native fill; artifact:",artifact)
