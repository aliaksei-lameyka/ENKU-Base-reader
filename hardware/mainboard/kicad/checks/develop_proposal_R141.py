"""Run isolated development, retain incomplete progress, never manufacture."""
import argparse,collections,gzip,hashlib,json,os,shutil,subprocess,sys,zipfile
from datetime import datetime,timezone
from pathlib import Path
from proposal_routing_R141 import charger,cleanup,repair
from pad_groups import partitions

BASE_SHA="90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    ap=argparse.ArgumentParser();ap.add_argument("canonical",type=Path);ap.add_argument("output",type=Path);ap.add_argument("--phase",choices=["charger","epd","spi"],default="charger");a=ap.parse_args()
    canonical=a.canonical.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    repo=Path(os.environ["GITHUB_WORKSPACE"]).resolve();work=Path(os.environ["RUNNER_TEMP"])/"enku-r141-isolated";root=work/"kicad"
    assert os.environ["GITHUB_REF"]=="refs/heads/engineering/r141-routing-power-fixes"
    assert sha(canonical/"enku-mainboard-r0.1.kicad_pcb")==BASE_SHA
    if root.exists():shutil.rmtree(root)
    shutil.copytree(canonical,root);app=os.environ["ENKU_KICAD_APP"]
    helper=root/"checks/proposal_native_R141.py"
    seed=json.loads(gzip.decompress((canonical/"checks/geometry_checkpoint_R138.json.gz").read_bytes()))
    seed_ids={t["uuid"]for t in seed["tracks"]}
    latest=None;clean=False;exception=None
    def native(mode,*args):
        subprocess.run([app,"python3.11",str(helper),mode,str(root),*map(str,args)],check=True)
    def preview(name):
        nonlocal latest
        latest=out/name;native("preview",latest)
        return json.loads((latest/"preview.json").read_text())
    def apply_plan(plan,name):native("apply",plan,out/(name+"-applied.json"))
    def resolve(prefix):
        nonlocal latest
        for round in range(18):
            s=preview(prefix+"-"+str(round))
            if not s["DRC_types"]and s["opens"]==0 and s["parity"]==0:return True
            d=json.loads((latest/"drc.json").read_text())
            unexpected={v["type"]for v in d["violations"]}-{"track_dangling","via_dangling","hole_to_hole"}
            if unexpected:raise RuntimeError("Native layout needs explicit review: "+str(sorted(unexpected)))
            plan=out/(prefix+"-cleanup-"+str(round)+".json")
            if cleanup(latest,plan,seed_ids):
                apply_plan(plan,prefix+"-cleanup-"+str(round));s=preview(prefix+"-trimmed-"+str(round))
            if s["opens"]:
                plan=out/(prefix+"-repair-"+str(round)+".json")
                try:repair(latest,root/"checks",plan)
                except RuntimeError:
                    # Preserve independently found routes from other pad groups.
                    if plan.exists()and json.loads(plan.read_text())["routes"]:apply_plan(plan,prefix+"-partial-"+str(round))
                    raise
                apply_plan(plan,prefix+"-repair-"+str(round))
        raise RuntimeError("Development iteration bound reached")
    try:
        native("prepare","charger",out/"charger-placement")
        preview("charger-placed")
        plan=out/"charger-route-plan.json";charger(latest,root/"checks",plan);apply_plan(plan,"charger-routes")
        clean=resolve("charger")
        if not clean:raise RuntimeError("Charger proposal is not native-clean")
        if a.phase!="charger":
            raise RuntimeError("EPD/SPI stage is not yet enabled; no false completion")
        subprocess.run([app,"kicad-cli","sch","erc","--severity-all","--format","json","--output",str(latest/"erc.json"),str(root/"enku-mainboard-r0.1.kicad_sch")],check=True)
        erc=json.loads((latest/"erc.json").read_text());assert not any(s["violations"]for s in erc["sheets"])
        g=json.loads((latest/"geometry.json").read_text())
        assert len(g["pads"])==438 and len(g["footprints"])==127
        assert partitions(g)==partitions(seed),"Original pad connectivity changed"
        oldpads={p["uuid"]:p for p in seed["pads"]}
        for p in g["pads"]:
            old=oldpads[p["uuid"]]
            for key in["ref","number","net","size","drill","shape","attribute","layers"]:
                assert old[key]==p[key],("Pad definition changed",p["ref"],p["number"],key)
        for ref,fp in seed["footprints"].items():
            if ref not in{"C5","C7","C8"}:assert fp==g["footprints"][ref],("Unexpected placement change",ref)
        import review_routing_R140 as review
        review.PCB_SHA=sha(root/"enku-mainboard-r0.1.kicad_pcb")
        review.review(root,latest,out/"routing")
        report_path=out/"routing/routing_review_R140.json";report=json.loads(report_path.read_text())
        report.update(audit_revision="R141_DEVELOPMENT",physical_revision="R141_PROPOSED",physical_source_modified=True,accepted_checkpoint_updated=False,fabrication_ready=False)
        report_path.write_text(json.dumps(report,indent=2)+"\n")
        assert all(p["status"]=="MEASURED_TRACK_PATH"for p in report["actual_track_paths"])
        cap_paths={(p["source"][0],p["target"][1]):p for p in report["actual_track_paths"]if p["source"][0]in{"C5","C7","C8"}}
        assert cap_paths[("C5","13")]["track_centerline_length_mm"]<2.
        # Original report measures C7 from U3 and C8 toward U3.
        assert next(p for p in report["actual_track_paths"]if p["source"]==["U3","10"]and p["target"]==["C7","1"])["track_centerline_length_mm"]<3.
        assert cap_paths[("C8","2")]["track_centerline_length_mm"]<3.
        print("PASS native-clean charger proposal, preserved pad connectivity and short decoupling paths",flush=True)
        import importlib.util
        source=(canonical/"checks/render_routing_R140.py").read_text().replace("Physical R138 / R140 routing review -","R141 DEVELOPMENT proposal -")
        render_path=out/"render_proposal.py";render_path.write_text(source)
        spec=importlib.util.spec_from_file_location("render_proposal",render_path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.render(latest,report_path,out/"visuals")
    except Exception as e:
        exception=repr(e);print("R141 DEVELOPMENT INCOMPLETE:",exception,flush=True)
    finally:
        try:preview("final-development-snapshot")
        except Exception as final_error:
            exception=exception or repr(final_error);print("Final snapshot preview failed",repr(final_error),flush=True)
        assert sha(canonical/"enku-mainboard-r0.1.kicad_pcb")==BASE_SHA
        destination=repo/"docs/evidence/R141";destination.mkdir(parents=True,exist_ok=True)
        state=dict(updated_utc=datetime.now(timezone.utc).isoformat(),canonical_physical_revision="R138",canonical_source_unchanged=True,
                   proposal_revision="R141_DEVELOPMENT",proposal_pcb_sha256=sha(root/"enku-mainboard-r0.1.kicad_pcb"),
                   proposal_stage=a.phase,proposal_native_clean=clean and exception is None,exception=exception,
                   actual_workflow_run_id=os.environ["GITHUB_RUN_ID"],actual_workflow_attempt=os.environ["GITHUB_RUN_ATTEMPT"],
                   source_commit=os.environ["GITHUB_SHA"],approved_checkpoint_updated=False,physical_qualification="NOT RUN",
                   manufacturing_files_replaced=False,fabrication_ready=False)
        if latest and (latest/"preview.json").exists():state["last_actual_native_preview"]=json.loads((latest/"preview.json").read_text())
        archive=destination/"R141_development_proposal_NO_FAB.zip"
        included=[]
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=9)as z:
            for p in sorted(root.iterdir()):
                if p.is_file()and(p.suffix==".kicad_sch"or p.name.startswith("enku-mainboard-r0.1.")or p.name in["ENKU.kicad_sym","sym-lib-table","fp-lib-table"]):
                    z.write(p,"editable/"+p.name);included.append("editable/"+p.name)
            for folder in["ENKU.pretty","standard-footprints"]:
                for p in sorted((root/folder).rglob("*")):
                    if p.is_file():name="editable/"+p.relative_to(root).as_posix();z.write(p,name);included.append(name)
            for p in sorted(out.rglob("*")):
                if p.is_file():name="development/"+p.relative_to(out).as_posix();z.write(p,name);included.append(name)
            for p in [repo/"LICENSE",repo/"LICENSE.md",*sorted((repo/"LICENSES").glob("*"))]:
                if p.is_file():name="licenses/"+p.relative_to(repo).as_posix();z.write(p,name);included.append(name)
            note="# R141 DEVELOPMENT PROPOSAL — NO FAB\n\nCanonical source and the reviewed PCBWay R138 package remain unchanged.\nThis archive retains isolated work in progress, not an approved manufacturing checkpoint.\nRead development-state.json and the actual native reports. Physical qualification is NOT RUN.\n"
            z.writestr("README_NO_FAB.md",note);z.writestr("development-state.json",json.dumps(state,indent=2))
        with zipfile.ZipFile(archive)as z:
            assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))
        state["archive"]={"path":archive.relative_to(repo).as_posix(),"bytes":archive.stat().st_size,"sha256":sha(archive)}
        (destination/"development_state_R141.json").write_text(json.dumps(state,indent=2)+"\n")
        if latest:
            for name in["preview.json","drc.json"]:
                if(latest/name).exists():shutil.copyfile(latest/name,destination/name)
        if(out/"routing/routing_review_R140.json").exists():shutil.copyfile(out/"routing/routing_review_R140.json",destination/"routing_review_R141.json")
        if(out/"visuals").exists():shutil.copytree(out/"visuals",destination/"visuals",dirs_exist_ok=True)
        print(json.dumps(state,indent=2),flush=True)
    if exception:raise SystemExit(1)
if __name__=="__main__":run()
