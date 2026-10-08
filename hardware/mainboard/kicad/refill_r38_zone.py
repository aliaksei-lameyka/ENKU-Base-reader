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
if len(zones)!=1:
    raise SystemExit(f"R38 expected exactly one zone, got {len(zones)}")
z=zones[0]
if z.GetNetname()!="GND" or z.GetLayer()!=pcbnew.In2_Cu:
    raise SystemExit(f"R38 zone net/layer mismatch: {z.GetNetname()} {z.GetLayer()}")
filler=pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
if not z.IsFilled():
    raise SystemExit("KiCad zone remained unfilled")
poly=z.GetFilledPolysList(pcbnew.In2_Cu)
if poly.OutlineCount()==0:
    raise SystemExit("KiCad GND zone has zero filled copper outlines")
print("R38 ZONE FILL PASS: native pcbnew filled",poly.OutlineCount(),"In2.Cu GND copper polygon(s)")
pcbnew.SaveBoard(str(src),board)
shutil.copyfile(src,artifact)
# Re-open the exact DRC input and confirm saved fill survived serialization.
check=pcbnew.LoadBoard(str(src))
z2=list(check.Zones())[0]
if not z2.IsFilled() or z2.GetFilledPolysList(pcbnew.In2_Cu).OutlineCount()==0:
    raise SystemExit("Saved R38 zone does not retain valid fill")
print("R38 SAVED ZONE PASS: DRC input is KiCad-filled, artifact:",artifact)
