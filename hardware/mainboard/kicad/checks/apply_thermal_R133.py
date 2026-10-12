"""One-time R132 -> R133 thermal geometry proposal; NO FAB until process approval.

TI RGT0016C 4222419/E places a central via and four vias at +/-0.58 mm.
The project keeps its existing 0.30 mm drill / 0.50 mm land constraints.
These five vias are under the unchanged EP paste; filled and copper capped
construction is an explicit fabrication requirement, never inferred from mask.
"""
import hashlib, json, sys, uuid
from pathlib import Path
import pcbnew as p

root = Path(sys.argv[1]).resolve()
pcb = root / 'enku-mainboard-r0.1.kicad_pcb'
assert hashlib.sha256(pcb.read_bytes()).hexdigest() == '540faac1779277466bdaca739325d1139cf8cead39f4d9b9df1eaa0529a648f3', 'Requires the exact accepted R132 PCB'
board = p.LoadBoard(str(pcb))
ground = board.FindNet('GND')
positions = [(48.5, 91.0)] + [(48.5+x, 91.0+y) for x in [-.58, .58] for y in [-.58, .58]]
added = []
for x, y in positions:
    via = p.PCB_VIA(board)
    via.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL, f'enku:R133:U3:thermal:{x:.2f}:{y:.2f}'))))
    via.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))
    via.SetWidth(p.FromMM(.5))
    via.SetDrill(p.FromMM(.3))
    via.SetViaType(p.VIATYPE_THROUGH)
    via.SetLayerPair(p.F_Cu, p.B_Cu)
    via.SetNet(ground)
    via.SetFillingMode(p.FILLING_MODE_FILLED)
    via.SetCappingMode(p.CAPPING_MODE_CAPPED)
    via.SetFrontTentingMode(p.TENTING_MODE_NOT_TENTED)
    via.SetBackTentingMode(p.TENTING_MODE_TENTED)
    board.Add(via)
    added.append(dict(uuid=via.m_Uuid.AsString(), position_mm=[x, y], net='GND', drill_mm=.3, land_mm=.5, construction_required='resin filled and copper capped; supplier approval pending'))
p.SaveBoard(str(pcb), board)
(root/'checks/thermal_via_manifest_R133.json').write_text(json.dumps(dict(revision='R133',base_R132_pcb_sha256='540faac1779277466bdaca739325d1139cf8cead39f4d9b9df1eaa0529a648f3', added_vias=added, expected_filled_capped_process_approved=False, fabrication_ready=False), indent=2)+'\n')
print('Added five explicitly process-gated U3 thermal vias; native DRC and plane checks required')
