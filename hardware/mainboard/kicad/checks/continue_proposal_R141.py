"""Explicit isolated charger recovery; native results determine acceptance."""
import argparse, gzip, hashlib, json, os, shutil, subprocess
from pathlib import Path
from proposal_routing_R141 import cleanup, ProposalRouter
from pad_groups import partitions, components

def write(path, value): path.write_text(json.dumps(value, indent=2)+"\n")

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('root',type=Path); parser.add_argument('output',type=Path)
    a=parser.parse_args(); root=a.root.resolve(); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    canonical=Path(__file__).resolve().parents[1]
    assert root!=canonical and not root.is_relative_to(canonical)
    assert hashlib.sha256((canonical/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()=='90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971'
    app=os.environ['ENKU_KICAD_APP']; helper=root/'checks/proposal_native_R141.py'
    for name in ['proposal_board_R141.py','proposal_native_R141.py']:
        shutil.copyfile(canonical/'checks'/name,root/'checks'/name)
    seed=json.loads(gzip.decompress((canonical/'checks/geometry_checkpoint_R138.json.gz').read_bytes()))
    ids={t['uuid']for t in seed['tracks']}
    def native(mode,*args): subprocess.run([app,'python3.11',str(helper),mode,str(root),*map(str,args)],check=True,stdout=subprocess.DEVNULL)
    def preview(name):
        path=out/name; native('preview',path); print(name,(path/'preview.json').read_text(),flush=True); return path
    def apply(plan,name): native('apply',plan,out/(name+'-applied.json'))
    current=preview('recovered')
    for n in range(45):
        plan=out/f'trim-{n}.json'
        if not cleanup(current,plan,ids): break
        before=json.loads((current/'geometry.json').read_text())
        apply(plan,f'trim-{n}'); current=preview(f'trimmed-{n}')
        assert partitions(before)==partitions(json.loads((current/'geometry.json').read_text()))
    state=json.loads((current/'preview.json').read_text()); assert not state['DRC_types']
    # The standard grid cannot represent this narrow, explicitly reviewed escape.
    # A 0.50/0.20 via has the same 0.15 ring as existing qualified geometry.
    # Preserve the USB/SPI reference projections and U3 exposed-pad return area.
    g=json.loads((current/'geometry.json').read_text())
    r=ProposalRouter(g,canonical/'checks',[49,89,52,92],step=.01)
    src=r.pads[('R10','1')]; pos=[50.64,90.54]
    ms,_=r.r.masks('CHG_CE_N',.2,.5)
    assert r.r.free_line(src['pos'],pos,ms[0])
    route=dict(net='CHG_CE_N',width=.2,via_diameter=.5,via_drill=.2,
               segments=[dict(a=src['pos'],b=pos,layer=0)],vias=[pos])
    plan=out/'CE-escape.json';write(plan,dict(routes=[route],remove_tracks=[],fabrication_ready=False));apply(plan,'CE-escape');current=preview('CE-escape-native')
    d=json.loads((current/'drc.json').read_text())
    assert all(v['type']=='via_dangling' for v in d['violations']) and not d['schematic_parity']
    (out/'latest.txt').write_text(str(current))

if __name__=='__main__':main()
