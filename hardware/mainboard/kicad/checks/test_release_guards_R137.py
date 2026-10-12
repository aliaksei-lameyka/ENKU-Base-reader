"""Exercise rejection of stale sources, unreviewed baselines and physical regressions."""
import copy, json, os, subprocess, sys, tempfile
from pathlib import Path
from run_native_current import reviewed_driver

root, output = (Path(s).resolve() for s in sys.argv[1:3])
checks = root/'checks'
passed = []
with tempfile.TemporaryDirectory(prefix='enku-r137-rejection-') as directory:
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
    prepare();assert reviewed_driver(fixture).name=='run_native_R137.py'
    selector=copy.deepcopy(original_selector);selector['revision']='R999'
    rejected('unknown revision rejected',selector=selector)
    selector=copy.deepcopy(original_selector);selector['geometry_file']='../other.json'
    rejected('unreviewed checkpoint path rejected',selector=selector)
    rejected('changed source PCB rejected',pcb=board+b'\n')
    checkpoint=copy.deepcopy(original_checkpoint);checkpoint['independent_guards_passed']=0
    rejected('incomplete baseline rejected',checkpoint=checkpoint)
    checkpoint=copy.deepcopy(original_checkpoint);checkpoint['fabrication_ready']=True
    rejected('fabrication declaration cannot be inferred from native pass',checkpoint=checkpoint)
    q=subprocess.run([sys.executable,str(checks/'run_native_R137.py'),str(fixture),str(Path(directory)/'out'),'--freeze'],
                     env={**os.environ,'GITHUB_ACTIONS':'true'},capture_output=True,text=True)
    assert q.returncode!=0 and 'freeze is forbidden' in q.stderr
    passed.append('CI baseline regeneration rejected')
    altered=Path(directory)/'native';altered.mkdir()
    import shutil
    shutil.copytree(output/'manufacturing_review_R137',altered/'manufacturing_review_R137')
    for path in output.iterdir():
        if path.is_file():
            (altered/path.name).write_bytes(path.read_bytes())
    geometry=json.loads((altered/'geometry.json').read_text())
    geometry['pads'][0]['pos'][0]+=.01
    (altered/'geometry.json').write_text(json.dumps(geometry))
    q=subprocess.run([sys.executable,str(checks/'audit_source_R137.py'),str(root),str(altered)],capture_output=True,text=True)
    assert q.returncode!=0 and 'outside R137' in q.stderr,q.stderr
    passed.append('unauthorised physical pad movement rejected')
    (altered/'geometry.json').write_bytes((output/'geometry.json').read_bytes())
    assembly=json.loads((altered/'assembly_features.json').read_text())
    next(f for f in assembly['footprints']if f['ref']=='C9')['fields']['MPN']='CC0805KKX5R6BB106'
    (altered/'assembly_features.json').write_text(json.dumps(assembly))
    q=subprocess.run([sys.executable,str(checks/'audit_capacitance_R137.py'),str(root),str(altered)],capture_output=True,text=True)
    assert q.returncode!=0
    passed.append('wrong assembled C9 MPN rejected')
    (altered/'assembly_features.json').write_bytes((output/'assembly_features.json').read_bytes())
    assembly=json.loads((altered/'assembly_features.json').read_text())
    for pad in assembly['pads']:
        if pad['ref']=='R67':pad['layers'].append('F.Paste')
    (altered/'assembly_features.json').write_text(json.dumps(assembly))
    q=subprocess.run([sys.executable,str(checks/'audit_component_pass_R137.py'),str(root),str(altered)],capture_output=True,text=True)
    assert q.returncode!=0
    passed.append('DNP R67 native paste restoration rejected')
    (altered/'assembly_features.json').write_bytes((output/'assembly_features.json').read_bytes())
    import hashlib
    package=altered/'manufacturing_review_R137'
    def rejected_export(name,relative,mutation):
        file=package/relative;original=file.read_bytes();manifest_file=package/'manifest_R137.json';old_manifest=manifest_file.read_bytes()
        try:
            file.write_bytes(mutation(original))
            manifest=json.loads(old_manifest);manifest['files'][relative]['sha256']=hashlib.sha256(file.read_bytes()).hexdigest();manifest['files'][relative]['bytes']=file.stat().st_size
            manifest_file.write_text(json.dumps(manifest))
            q=subprocess.run([sys.executable,str(checks/'audit_exports_R137.py'),str(root),str(altered)],capture_output=True,text=True)
            assert q.returncode!=0,('Unsafe manufacturing fixture accepted',name)
            passed.append(name)
        finally:file.write_bytes(original);manifest_file.write_bytes(old_manifest)
    missing=package/'gerber/enku-mainboard-r0.1-B_Paste.gbr';saved=missing.read_bytes();missing.unlink()
    try:
        q=subprocess.run([sys.executable,str(checks/'audit_exports_R137.py'),str(root),str(altered)],capture_output=True,text=True)
        assert q.returncode!=0;passed.append('successful CLI package with a missing requested layer rejected')
    finally:missing.write_bytes(saved)
    rejected_export('changed full copper Gerber with updated package checksum rejected','gerber/enku-mainboard-r0.1-F_Cu.gbr',lambda b:__import__('re').sub(rb'X(-?\d+)(Y-?\d+D03\*)',lambda m:b'X'+str(int(m[1])+10000).encode()+m[2],b,count=1))
    rejected_export('wrong PTH plating metadata with updated checksum rejected','drill/enku-mainboard-r0.1-PTH.drl',lambda b:b.replace(b'TF.FileFunction,Plated,',b'TF.FileFunction,NonPlated,',1))
    rejected_export('DNP paste flashes independently detected despite updated checksum','gerber/enku-mainboard-r0.1-F_Paste.gbr',lambda b:b.replace(b'M02*',b'%TO.C,R67*%\nD10*\nX62150000Y-108500000D03*\nX63850000Y-108500000D03*\n%TD*%\nM02*'))
report=dict(revision='R137',positive_baseline_accepted=True,negative_cases_passed=passed,
            altered_project_or_physical_board=False,fabrication_ready=False)
(output/'rejection_tests_R137.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
