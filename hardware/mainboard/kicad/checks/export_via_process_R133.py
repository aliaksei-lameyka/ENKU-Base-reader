"""Export native construction REQUESTS, not evidence of manufactured via fill."""
import json, sys
from pathlib import Path
import pcbnew as p

b = p.LoadBoard(sys.argv[1])
rows = []
for t in b.GetTracks():
    if not isinstance(t, p.PCB_VIA):
        continue
    rows.append(dict(uuid=t.m_Uuid.AsString(), net=t.GetNetname(),
                     position_mm=[p.ToMM(t.GetPosition().x), p.ToMM(t.GetPosition().y)],
                     fill_requested=t.GetFillingMode() == p.FILLING_MODE_FILLED,
                     cap_requested=t.GetCappingMode() == p.CAPPING_MODE_CAPPED,
                     front_tented=t.IsTented(p.F_Mask),
                     back_tented=t.IsTented(p.B_Mask)))
Path(sys.argv[2]).write_text(json.dumps(dict(native_kicad=p.Version(),
    manufacturing_requests_only=True, fabricated_construction_verified=False,
    vias=sorted(rows, key=lambda x: x['uuid'])), indent=2)+'\n')
print('Exported native via fill/cap requests; actual construction remains unapproved')
