"""Exercise rejection of stale sources, unreviewed baselines and physical regressions."""
import copy, json, os, subprocess, sys, tempfile
from pathlib import Path
from run_native_current import reviewed_driver

root, output = (Path(s).resolve() for s in sys.argv[1:3])
checks = root/'checks'
passed = []
with tempfile.TemporaryDirectory(prefix='enku-r136-rejection-') as directory:
    fixture = Path(directory)/'kicad'
    (fixture/'checks').mkdir(parents=True)
    original_selector = json.loads((checks/'current_checkpoint.json').read_text())
    original_checkpoint = json.loads((checks/original_selector['verification_file']).read_text())
    board = (root/'enku-mainboard-r0.1.kicad_pcb').read_bytes()
    def prepare(selector=None, checkpoint=None, pcb=None):
        (fixture/'checks/current_checkpoint.json').write_text(json.dumps(selector or original_selector))
        (fixture/'checks'/original_selector['verification_file']).write_text(json.dumps(checkpoint or original_checkpoint))
        (fixture/'enku-mainboard-r0.1.kicad_pcb').write_bytes(board if pcb is None else pcb)
    def rejected(name, **kwargs):
        prepare(**kwargs)
        try:
            reviewed_driver(fixture)
        except ValueError:
            passed.append(name)
        else:
            raise AssertionError('Accepted unsafe fixture: '+name)
    prepare();assert reviewed_driver(fixture).name=='run_native_R136.py'
    selector=copy.deepcopy(original_selector);selector['revision']='R999'
    rejected('unknown revision rejected',selector=selector)
    selector=copy.deepcopy(original_selector);selector['geometry_file']='../other.json'
    rejected('unreviewed checkpoint path rejected',selector=selector)
    rejected('changed source PCB rejected',pcb=board+b'\n')
    checkpoint=copy.deepcopy(original_checkpoint);checkpoint['independent_guards_passed']=0
    rejected('incomplete baseline rejected',checkpoint=checkpoint)
    checkpoint=copy.deepcopy(original_checkpoint);checkpoint['fabrication_ready']=True
    rejected('fabrication declaration cannot be inferred from native pass',checkpoint=checkpoint)
    q=subprocess.run([sys.executable,str(checks/'run_native_R136.py'),str(fixture),str(Path(directory)/'out'),'--freeze'],
                     env={**os.environ,'GITHUB_ACTIONS':'true'},capture_output=True,text=True)
    assert q.returncode!=0 and 'freeze is forbidden' in q.stderr
    passed.append('CI baseline regeneration rejected')
    altered=Path(directory)/'native';altered.mkdir()
    for path in output.iterdir():
        if path.is_file():
            (altered/path.name).write_bytes(path.read_bytes())
    geometry=json.loads((altered/'geometry.json').read_text())
    geometry['pads'][0]['pos'][0]+=.01
    (altered/'geometry.json').write_text(json.dumps(geometry))
    q=subprocess.run([sys.executable,str(checks/'audit_source_R136.py'),str(root),str(altered)],capture_output=True,text=True)
    assert q.returncode!=0 and 'outside R136' in q.stderr,q.stderr
    passed.append('unauthorised physical pad movement rejected')
    (altered/'geometry.json').write_bytes((output/'geometry.json').read_bytes())
    assembly=json.loads((altered/'assembly_features.json').read_text())
    next(f for f in assembly['footprints']if f['ref']=='C9')['fields']['MPN']='CC0805KKX5R6BB106'
    (altered/'assembly_features.json').write_text(json.dumps(assembly))
    q=subprocess.run([sys.executable,str(checks/'audit_capacitance_R136.py'),str(root),str(altered)],capture_output=True,text=True)
    assert q.returncode!=0
    passed.append('wrong assembled C9 MPN rejected')
report=dict(revision='R136',positive_baseline_accepted=True,negative_cases_passed=passed,
            altered_project_or_physical_board=False,fabrication_ready=False)
(output/'rejection_tests_R136.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
