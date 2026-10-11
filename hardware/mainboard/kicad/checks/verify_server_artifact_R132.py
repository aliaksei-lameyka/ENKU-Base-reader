"""Compare actual R132 CI artifact to local native results; only SVG title dates vary.
Usage: script LOCAL_NATIVE_RESULTS SERVER_RESULTS_DIRECTORY
Server directory contains run.json,jobs.json,native_server_R132.zip and artifact/.
"""
import collections,hashlib,json,re,sys
from pathlib import Path
l=Path(sys.argv[1]);p=Path(sys.argv[2]);s=p/'artifact';sha=(s/'source_pcb.sha256').read_text().split()[0]
assert sha=='540faac1779277466bdaca739325d1139cf8cead39f4d9b9df1eaa0529a648f3'
assert (s/'version.txt').read_text().strip()=='10.0.7'
plot_names=['F_Mask','F_Paste','B_Mask'];normalized={};local_hashes={};server_hashes={}
def norm(data):
 z,count=re.subn(rb'(<title>SVG Image created as [^<]* date )\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}( </title>)',rb'\1EXPORT_TIMESTAMP\2',data)
 assert count==1,'Expected exactly the native export title date';return z
for name in plot_names:
 a=(l/(name+'.svg')).read_bytes();b=(s/(name+'.svg')).read_bytes();assert norm(a)==norm(b),('Actual plot geometry differs',name)
 local_hashes[name]=hashlib.sha256(a).hexdigest();server_hashes[name]=hashlib.sha256(b).hexdigest();normalized[name]=hashlib.sha256(norm(b)).hexdigest()
results=[];exact=[];date_only=[]
for file in s.glob('*.json'):
 d=json.loads(file.read_text())
 if d.get('pcb_sha256',d.get('committed_pcb_sha256'))!=sha:continue
 local=json.loads((l/file.name).read_text())
 if local==d:exact.append(file.name)
 else:
  assert file.name in ['U1_plot_audit.json','IC_stencil_audit.json']
  key='plot_sha256'if file.name=='U1_plot_audit.json'else'actual_plot_sha256'
  assert set(local.keys())==set(d.keys())
  assert all(local[k]==d[k]for k in d if k!=key)
  for name in d[key]:assert d[key][name]==server_hashes[name] and local[key][name]==local_hashes[name]
  date_only.append(file.name)
 results.append(file.name)
assert len(results)==18 and len(exact)==16 and len(date_only)==2,(exact,date_only)
for name in ['assembly_features.json','orientation.json','CPL.csv','assembly_review_BOM.csv']:
 assert (s/name).read_bytes()==(l/name).read_bytes(),('Actual native export differs',name)
d=json.loads((s/'drc.json').read_text());e=json.loads((s/'erc.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and len(d['violations'])==20 and all(x['type']=='hole_clearance'for x in d['violations']) and sum(len(x['violations'])for x in e['sheets'])==0
api=json.loads((p/'run.json').read_text());jobs=json.loads((p/'jobs.json').read_text())
assert api['head_sha']=='970c93eac57e411a45d5975d73ed080071d4769b'and api['conclusion']=='success'
assert len(jobs['jobs'])==1 and all(j['conclusion']=='success'and len(j['steps'])==12 and all(v['conclusion']=='success'for v in j['steps'])for j in jobs['jobs'])
binary_sha=hashlib.sha256((p/'native_server_R132.zip').read_bytes()).hexdigest();assert binary_sha=='27674619166d84889e167a7199bbd3ba7729144ddeabd4c922b099ac568db856'
import zipfile
assert zipfile.ZipFile(p/'native_server_R132.zip').testzip() is None
proof=dict(revision='R132',native_kicad='10.0.7',source_pcb_sha256=sha,source_commit=api['head_sha'],source_tree='05e223518200bd546b66153ea9da767e2767d1a5',run_id=api['id'],run_url=api['html_url'],run_event=api['event'],run_created_utc=api['created_at'],run_updated_utc=api['updated_at'],run_conclusion=api['conclusion'],job_id=jobs['jobs'][0]['id'],all12_actual_job_steps_succeeded=True,all18_report_results_match_local_excluding_validated_SVG_title_timestamp_hashes=True,report_names=sorted(results),report_JSON_exact_matches=exact,report_hash_differences_due_only_to_checked_plot_title_timestamp=date_only,actual_native_non_plot_exports_match_by_bytes=True,actual_plot_geometry_matches_after_only_title_date_normalization=True,normalized_native_plot_sha256=normalized,local_raw_plot_sha256=local_hashes,server_raw_plot_sha256=server_hashes,artifact_id=11715901613,artifact_bytes=455203,artifact_API_digest='sha256:'+binary_sha,artifact_binary_sha256=binary_sha,artifact_binary_downloaded_and_CRC_verified=True,opens=0,ERC=0,schematic_parity=0,drc_types={'hole_clearance':20},fabrication_ready=False)
(p/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS actual source,18 report results, SVG geometry/title-date provenance, native exports,12 job steps and artifact binary')
