"""Explicit compact EPD proposal in an isolated copy, never a release repair."""
import json, os, subprocess
from pathlib import Path
import numpy as np
from proposal_routing_R141 import ProposalRouter, cap_ground

def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')

def routes(native,checks,output):
    g=json.loads((native/'geometry.json').read_text())
    rebuilt={'EPD_SW','EPD_CP_NEG','EPD_VGH','EPD_VGL','EPD_GDR','EPD_RESE','EPD_VCOM'}
    remove={t['uuid']for t in g['tracks']if t['net']in rebuilt}
    g['tracks']=[t for t in g['tracks']if t['uuid']not in remove]
    r=ProposalRouter(g,checks,[27,22,76,58],step=.05);pads=r.pads
    plan=dict(routes=[],remove_tracks=sorted(remove),fabrication_ready=False)
    tasks=[('EPD_SW',('Q1','3'),('L2','2'),.35),('EPD_SW',('Q1','3'),('D1','2'),.35),
           ('EPD_SW',('Q1','3'),('C25','1'),.3),
           ('EPD_VCI',('C31','1'),('L2','1'),.35),
           ('EPD_CP_NEG',('C25','2'),('D3','1'),.3),('EPD_CP_NEG',('C25','2'),('D2','2'),.3),
           ('EPD_VGH',('D1','1'),('C24','1'),.3),('EPD_VGL',('D3','2'),('C26','1'),.3),
           ('EPD_RESE',('Q1','2'),('R37','1'),.2)]
    for net,a,b,width in tasks:
        r.add(plan,net,[pads[a]],[pads[b]],width=width,front=True,timeout=25)
        write(output,plan)
    for ref in ['C31','C24','C26']:cap_ground(r,plan,ref)
    # The clamp's anode uses its own short ground return.
    clamp_cathode=r.pads[('D2','2')]
    r.pads[('D2','2')]=pads[('D2','1')];cap_ground(r,plan,'D2');r.pads[('D2','2')]=clamp_cathode
    for net in ['EPD_RESE','EPD_GDR','EPD_VGH','EPD_VGL','EPD_VCOM']:
        pp=[p for p in g['pads']if p['net']==net and p['number']]
        if len(pp)<2:continue
        main=[pp[0]]
        # Local connections already added above are available as conductive endpoints.
        main += [t for t in r.g['tracks']if t['net']==net]
        for pad in pp[1:]:
            if any(t['start']==pad['pos']or t['end']==pad['pos']for t in main if 'start'in t):main.append(pad);continue
            _,new=r.add(plan,net,main,[pad],width=.3 if net=='EPD_VCI'else .2,timeout=40)
            main += [pad]+new;write(output,plan)
    write(output,plan)

if __name__=='__main__':
    import sys
    routes(*(Path(a).resolve()for a in sys.argv[1:4]))
