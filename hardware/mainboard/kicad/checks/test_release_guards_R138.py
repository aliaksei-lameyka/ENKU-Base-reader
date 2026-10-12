"""Positive baselines then20 meaningful rejection cases; runtime failures never pass."""
import copy,gzip,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
from run_native_current import reviewed_driver
root,output=(Path(s).resolve()for s in sys.argv[1:3]);checks=root/'checks';passed=[]
def call(guard,r,o):
 p=checks/guard;assert p.is_file(),('Missing actual guard',guard)
 return subprocess.run([sys.executable,str(p),str(r),str(o)],capture_output=True,text=True)
def positive(guard,r,o):
 q=call(guard,r,o);assert q.returncode==0,(guard,q.stderr)
def failure(name,q,message):
 assert q.returncode==1 and 'AssertionError'in q.stderr and message in q.stderr,(name,q.returncode,q.stderr)
 assert 'No such file or directory'not in q.stderr and 'ModuleNotFoundError'not in q.stderr
 passed.append(name)
with tempfile.TemporaryDirectory(prefix='enku-r138-rejection-')as directory:
 fixture=Path(directory)/'kicad';(fixture/'checks').mkdir(parents=True)
 selector=json.loads((checks/'current_checkpoint.json').read_text());checkpoint=json.loads((checks/selector['verification_file']).read_text());board=(root/'enku-mainboard-r0.1.kicad_pcb').read_bytes()
 def prepare(s=None,c=None,b=None):
  (fixture/'checks/current_checkpoint.json').write_text(json.dumps(selector if s is None else s));(fixture/'checks'/selector['verification_file']).write_text(json.dumps(checkpoint if c is None else c));(fixture/'enku-mainboard-r0.1.kicad_pcb').write_bytes(board if b is None else b)
 def dispatch_rejected(name,**kwargs):
  prepare();assert reviewed_driver(fixture).name=='run_native_R138.py'
  prepare(**kwargs)
  try:reviewed_driver(fixture)
  except ValueError:passed.append(name)
  else:raise AssertionError('Accepted unsafe dispatcher fixture: '+name)
 s=copy.deepcopy(selector);s['revision']='R999';dispatch_rejected('unknown revision rejected',s=s)
 s=copy.deepcopy(selector);s['geometry_file']='../other.json';dispatch_rejected('unreviewed checkpoint path rejected',s=s)
 dispatch_rejected('changed source PCB rejected',b=board+b'\n')
 c=copy.deepcopy(checkpoint);c['independent_guards_passed']=0;dispatch_rejected('incomplete baseline rejected',c=c)
 c=copy.deepcopy(checkpoint);c['fabrication_ready']=True;dispatch_rejected('fabrication declaration cannot be inferred from native pass',c=c)
 prepare();q=subprocess.run([sys.executable,str(checks/'run_native_R138.py'),str(fixture),str(Path(directory)/'out'),'--freeze'],env={**os.environ,'GITHUB_ACTIONS':'true'},capture_output=True,text=True)
 assert q.returncode==1 and 'freeze is forbidden'in q.stderr;passed.append('CI baseline regeneration rejected')
 altered=Path(directory)/'native';shutil.copytree(output,altered);package=altered/'manufacturing_review_R138'
 def mutated_json(name,guard,filename,mutation,message,r=root):
  positive(guard,r,altered);p=altered/filename;original=p.read_bytes()
  try:
   obj=json.loads(original);mutation(obj);p.write_text(json.dumps(obj));failure(name,call(guard,r,altered),message)
  finally:p.write_bytes(original)
 mutated_json('unauthorised physical pad movement rejected','audit_source_R138.py','geometry.json',lambda g:g['pads'][0]['pos'].__setitem__(0,g['pads'][0]['pos'][0]+.01),'Pads changed outside R138')
 mutated_json('wrong assembled C9 MPN rejected','audit_capacitance_R136.py','assembly_features.json',lambda af:next(f for f in af['footprints']if f['ref']=='C9')['fields'].__setitem__('MPN','CC0805KKX5R6BB106'),"sf['MPN'] == features[ref]['fields']['MPN']")
 def paste(af):
  for p in af['pads']:
   if p['ref']=='R67':p['layers'].append('F.Paste')
 mutated_json('DNP R67 native paste restoration rejected','audit_component_pass_R137.py','assembly_features.json',paste,'AssertionError')
 def export_mutation(name,relative,mutation,message):
  positive('audit_exports_R138.py',root,altered);p=package/relative;original=p.read_bytes();mp=package/'manifest_R138.json';old=mp.read_bytes()
  try:
   modified=mutation(original);assert modified!=original;p.write_bytes(modified);m=json.loads(old);m['files'][relative]=dict(sha256=hashlib.sha256(modified).hexdigest(),bytes=len(modified));mp.write_text(json.dumps(m));failure(name,call('audit_exports_R138.py',root,altered),message)
  finally:p.write_bytes(original);mp.write_bytes(old)
 positive('audit_exports_R138.py',root,altered);p=package/'gerber/enku-mainboard-r0.1-B_Paste.gbr';original=p.read_bytes();p.unlink()
 try:failure('successful CLI package with missing requested layer rejected',call('audit_exports_R138.py',root,altered),'Missing/extra fabrication layer')
 finally:p.write_bytes(original)
 shift=lambda b:re.sub(rb'X(-?\d+)(Y-?\d+D03\*)',lambda m:b'X'+str(int(m[1])+10000).encode()+m[2],b,count=1)
 export_mutation('changed full copper with updated package checksum rejected','gerber/enku-mainboard-r0.1-F_Cu.gbr',shift,'Complete copper Gerber differs')
 export_mutation('wrong PTH plating metadata with updated checksum rejected','drill/enku-mainboard-r0.1-PTH.drl',lambda b:b.replace(b'TF.FileFunction,Plated,',b'TF.FileFunction,NonPlated,',1),'Wrong drill plating metadata')
 export_mutation('DNP paste flashes detected despite updated checksum','gerber/enku-mainboard-r0.1-F_Paste.gbr',lambda b:b.replace(b'M02*',b'%TO.C,R67*%\nD10*\nX62150000Y-108500000D03*\nX63850000Y-108500000D03*\n%TD*%\nM02*'),'Gerber added/moved opening')
 def small(g):next(t for t in g['tracks']if t['via']and t['drill']==.3 and t['width']==.6)['width']=.5
 mutated_json('nominal annular ring regression rejected','audit_annular_R138.py','geometry.json',small,'Via dimensions or coordinates differ')
 def tiny(g):next(t for t in g['tracks']if t['via']and t['drill']==.2)['drill']=.15
 mutated_json('unreviewed smaller bore rejected','audit_annular_R138.py','geometry.json',tiny,'Via dimensions or coordinates differ')
 capids={v['uuid']for v in json.loads((checks/'thermal_via_manifest_R138.json').read_text())['added_vias']}|{'3170d571-6923-486d-97de-ef4f8c3c5fea'}
 def overlap(g):
  v=next(v for v in g['tracks']if v['via']and v['uuid']not in capids);p=next(p for p in g['pads']if p['ref']=='R64'and p['number']=='1');v['start']=p['pos'];v['end']=p['pos']
 mutated_json('ordinary via in SMD land rejected','audit_geometry_R138.py','geometry.json',overlap,'Ordinary via too close to SMD land')
 def no_cap(p):next(v for v in p['vias']if v['uuid']=='3170d571-6923-486d-97de-ef4f8c3c5fea')['cap_requested']=False
 mutated_json('R28 copper cap request removal rejected','audit_geometry_R138.py','via_process_R138.json',no_cap,'Exact filled capped construction request missing')
 def extra_cap(p):next(v for v in p['vias']if v['uuid']not in capids)['fill_requested']=True
 mutated_json('unreviewed fill exception rejected','audit_geometry_R138.py','via_process_R138.json',extra_cap,'Unexpected via process exception')
 export_mutation('wrong R28 process request coordinate rejected','R28_via_process_request.csv',lambda b:b.replace(b'62.325',b'62.425',1),'AssertionError')
 # Update both package checksum and the temporary stream baseline, then
 # demand the independent whole-image/native comparison detect the defect.
 positive('audit_copper_R138.py',root,altered)
 from full_copper_R138 import normalize_copper
 fake_root=Path(directory)/'copper-fixture';(fake_root/'checks').mkdir(parents=True);bp=fake_root/'checks/copper_Gerber_baseline_R138.json';baseline=json.loads((checks/'copper_Gerber_baseline_R138.json').read_text())
 p=package/'gerber/enku-mainboard-r0.1-F_Cu.gbr';original=p.read_bytes()
 try:
  changed=shift(original);assert changed!=original;p.write_bytes(changed);baseline['normalized_copper_sha256']['F_Cu']=hashlib.sha256(normalize_copper(changed)).hexdigest();bp.write_text(json.dumps(baseline));failure('independent copper image rejects defect despite updated stream baseline',call('audit_copper_R138.py',fake_root,altered),'Native/Gerber copper mismatch')
 finally:p.write_bytes(original)
assert len(passed)==20 and len(set(passed))==20,passed
report=dict(revision='R138',positive_baseline_accepted=True,all_negative_guards_first_passed_positive_fixture=True,runtime_or_missing_file_errors_are_not_accepted=True,negative_cases_passed=passed,altered_project_or_physical_board=False,fabrication_ready=False)
(output/'rejection_tests_R138.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
