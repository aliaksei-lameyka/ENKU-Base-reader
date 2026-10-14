"""R143 explicit scope, adapted from proposal_native_R141.py; original unchanged."""
"""Isolated R143 development proposals; canonical CI source is never repaired."""
import collections, hashlib, json, os, re, subprocess, sys
from pathlib import Path
import pcbnew as p
from native_board import apply, export

SEED_SHA="90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971"
CHARGER={"C5":([47.75,94.9],-90),"C7":([44.5,91.0],180),"C8":([52.5,91.0],0)}
EPD={"L2":([62.5,44.2],0),"C31":([57.7,44.2],180),
     "D1":([66.8,43.2],-90),"C24":([68.9,39.0],90),
     "C25":([67.8,52.0],-90),"D2":([64.3,53.5],0),
     "D3":([71.3,52.9],0),"C26":([74.0,49.7],90)}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
def isolated(root):
    if os.environ.get("GITHUB_ACTIONS")=="true":
        assert os.environ["GITHUB_REF"]=="refs/heads/engineering/r143-j3-startup-review"
        assert root.is_relative_to(Path(os.environ["RUNNER_TEMP"]).resolve()),"Proposal must be outside checkout"
        canonical=Path(os.environ["GITHUB_WORKSPACE"])/"hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pcb"
        assert sha(canonical)==SEED_SHA,"Canonical CI source changed"
        assert not root.is_relative_to(Path(os.environ["GITHUB_WORKSPACE"]).resolve())
    assert p.Version()=="10.0.7"
def prepare(root,stage,output):
    root,output=Path(root).resolve(),Path(output).resolve();output.mkdir(parents=True,exist_ok=True);isolated(root)
    pcb=root/"enku-mainboard-r0.1.kicad_pcb";pro=root/"enku-mainboard-r0.1.kicad_pro";project=pro.read_bytes()
    if stage=="charger":assert sha(pcb)==SEED_SHA
    moves=CHARGER if stage=="charger"else EPD
    b=p.LoadBoard(str(pcb));fps={f.GetReference():f for f in b.GetFootprints()};removed=set();records=[]
    for ref,(pos,angle)in moves.items():
        f=fps[ref];pads=list(f.Pads())
        for t in b.GetTracks():
            if isinstance(t,p.PCB_VIA):continue
            if any(t.GetLayer()in list(a.GetLayerSet().Seq())and t.GetNetCode()==a.GetNetCode()and(a.HitTest(t.GetStart())or a.HitTest(t.GetEnd()))for a in pads):
                removed.add(t.m_Uuid.AsString())
        records.append(dict(ref=ref,before_position_mm=xy(f.GetPosition()),before_angle=f.GetOrientationDegrees(),after_position_mm=pos,after_angle=angle))
    found=set()
    def drop(m):
        u=re.search(r'\(uuid "([^"]+)"\)',m[0])[1]
        if u in removed:found.add(u);return""
        return m[0]
    source=re.sub(r'^\t\((?:segment|via)\n.*?^\t\)\n',drop,pcb.read_text(),flags=re.M|re.S)
    assert found==removed
    source=source.replace("R138 - ENGINEERING / NO FAB","R143 - DEVELOPMENT / NO FAB")
    staging=output/"placement-input.kicad_pcb";staging.write_text(source);b=p.LoadBoard(str(staging))
    for f in b.GetFootprints():
        if f.GetReference()not in moves:continue
        pos,angle=moves[f.GetReference()];f.SetOrientationDegrees(angle);f.SetPosition(p.VECTOR2I(*(p.FromMM(v)for v in pos)));f.Reference().SetVisible(False)
    try:p.SaveBoard(str(pcb),b)
    finally:pro.write_bytes(project)
    (output/"placement.json").write_text(json.dumps(dict(stage=stage,moves=records,removed_tracks=sorted(removed),pcb_sha256=sha(pcb),fabrication_ready=False),indent=2)+"\n")
def apply_plan(root,plan,output):
    root,plan,output=Path(root).resolve(),Path(plan).resolve(),Path(output).resolve();isolated(root)
    pcb=root/"enku-mainboard-r0.1.kicad_pcb";pro=root/"enku-mainboard-r0.1.kicad_pro";project=pro.read_bytes();before=sha(pcb)
    try:apply(pcb,plan,pcb)
    finally:pro.write_bytes(project)
    output.write_text(json.dumps(dict(input_pcb_sha256=before,pcb_sha256=sha(pcb),plan_sha256=sha(plan),project_bytes_preserved=True,fabrication_ready=False),indent=2)+"\n")
def preview(root,output):
    root,output=Path(root).resolve(),Path(output).resolve();output.mkdir(parents=True,exist_ok=True);isolated(root)
    pcb=root/"enku-mainboard-r0.1.kicad_pcb";pro=root/"enku-mainboard-r0.1.kicad_pro";project=pro.read_bytes();app=os.environ["ENKU_KICAD_APP"];before=sha(pcb)
    os.environ["KIPRJMOD"]=str(root)
    try:subprocess.run([app,"kicad-cli","pcb","drc","--severity-all","--all-track-errors","--schematic-parity","--refill-zones","--save-board","--format","json","--output",str(output/"drc.json"),str(pcb)],check=True)
    finally:pro.write_bytes(project)
    export(pcb,output/"geometry.json")
    subprocess.run([app,"python3.11",str(root/"checks/export_native_copper_R138.py"),str(pcb),str(output/"native_copper_R138.json.gz")],check=True)
    d=json.loads((output/"drc.json").read_text());summary=dict(native_kicad="10.0.7",input_pcb_sha256=before,pcb_sha256=sha(pcb),DRC_types=dict(collections.Counter(v["type"]for v in d["violations"])),opens=len(d["unconnected_items"]),parity=len(d["schematic_parity"]),project_bytes_preserved=pro.read_bytes()==project,fabrication_ready=False)
    (output/"preview.json").write_text(json.dumps(summary,indent=2)+"\n");(output/"source_pcb.sha256").write_text(sha(pcb)+"  enku-mainboard-r0.1.kicad_pcb\n")
    print(json.dumps(summary,indent=2),flush=True)
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="prepare":prepare(*sys.argv[2:])
    elif mode=="apply":apply_plan(*sys.argv[2:])
    elif mode=="preview":preview(*sys.argv[2:])
    else:raise ValueError(mode)
