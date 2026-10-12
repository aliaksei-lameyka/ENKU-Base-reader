"""Compare actual R134 CI bytes/geometry; normalize only one SVG title date.
Usage: script GENERATED_NATIVE_BASELINE SERVER_DIRECTORY
The generated baseline is retained from the separate native repair run;
this check verifies the later immutable-source run without baseline regeneration.
The server directory contains actual run.json, jobs.json, artifacts.json,
native_server_R134.zip and safely extracted artifact/. No R132 proof is reused.
"""
import gzip,hashlib,json,re,sys,zipfile
from pathlib import Path
l=Path(sys.argv[1]);p=Path(sys.argv[2]);s=p/'artifact'
expected_sha='07813982c1b4c4f191178a905edb90ecf9f583862de3b648eb4e9da416daa70a'
expected_commit='c33ef737064422e5a860bce3401c4fea8167daca'
expected_tree='c7272c0f3dd58180dfed30edf198e9f5ff97422d'
sha=(s/'source_pcb.sha256').read_text().split()[0]
assert sha==expected_sha and (l/'source_pcb.sha256').read_text().split()[0]==sha
assert (s/'version.txt').read_text().strip()=='10.0.7'
plot_names=['F_Mask','F_Paste','B_Mask','F_Cu','B_Cu'];normalized={};local_hashes={};server_hashes={}
def norm(data):
    z,count=re.subn(rb'(<title>SVG Image created as [^<]* date )\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}( </title>)',rb'\1EXPORT_TIMESTAMP\2',data)
    assert count==1,'Expected exactly one native SVG title date'
    return z
for name in plot_names:
    a=(l/(name+'.svg')).read_bytes();b=(s/(name+'.svg')).read_bytes()
    assert norm(a)==norm(b),('Actual native plot geometry differs',name)
    local_hashes[name]=hashlib.sha256(a).hexdigest();server_hashes[name]=hashlib.sha256(b).hexdigest()
    normalized[name]=hashlib.sha256(norm(b)).hexdigest()
results=[];exact=[];date_only=[]
for file in sorted(s.glob('*.json')):
    d=json.loads(file.read_text())
    if not isinstance(d,dict)or d.get('pcb_sha256',d.get('committed_pcb_sha256'))!=sha:continue
    local=json.loads((l/file.name).read_text())
    if local==d:exact.append(file.name)
    else:
        assert file.name in ['U1_plot_audit.json','IC_stencil_audit.json'],file.name
        key='plot_sha256'if file.name=='U1_plot_audit.json'else'actual_plot_sha256'
        assert set(local)==set(d) and all(local[k]==d[k]for k in d if k!=key)
        for name in d[key]:
            assert d[key][name]==server_hashes[name] and local[key][name]==local_hashes[name]
        date_only.append(file.name)
    results.append(file.name)
assert len(results)==22 and len(exact)==20 and len(date_only)==2,(results,exact,date_only)
for name in ['geometry.json','assembly_features.json','orientation.json','via_process_R134.json']:
    assert json.loads((s/name).read_text())==json.loads((l/name).read_text()),name
for name in ['reference_planes_active.json.gz','thermal_planes_R134.json.gz']:
    assert json.loads(gzip.decompress((s/name).read_bytes()))==json.loads(gzip.decompress((l/name).read_bytes())),name
for name in ['CPL.csv','assembly_review_BOM.csv','source.kicad_pro']:
    assert (s/name).read_bytes()==(l/name).read_bytes(),name
# Netlist export date/tool paths vary; all electrical sections must be exact.
import xml.etree.ElementTree as ET
for group in ['components','libparts','nets']:
    assert ET.tostring(ET.parse(s/'netlist.xml').find(group))==ET.tostring(ET.parse(l/'netlist.xml').find(group)),group
d=json.loads((s/'drc.json').read_text());e=json.loads((s/'erc.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity']
assert len(d['violations'])==16 and all(x['type']=='hole_clearance'for x in d['violations'])
assert sum(len(x['violations'])for x in e['sheets'])==0
api=json.loads((p/'run.json').read_text());jobs=json.loads((p/'jobs.json').read_text())
assert api['head_sha']==expected_commit and api['head_branch']=='engineering/r134-usb-control-connector'
assert api['status']=='completed'and api['conclusion']=='success'
assert json.loads((p/'source_commit.json').read_text())['tree']['sha']==expected_tree
assert len(jobs['jobs'])==1 and all(j['conclusion']=='success'and len(j['steps'])==12 and all(v['conclusion']=='success'for v in j['steps'])for j in jobs['jobs'])
assert jobs['jobs'][0]['run_id']==api['id']
a=json.loads((p/'artifacts.json').read_text());a=next(x for x in a['artifacts']if x['name']=='enku-native-kicad-'+expected_commit)
assert not a['expired'] and a['workflow_run']['head_sha']==expected_commit
assert a['workflow_run']['id']==api['id']
raw=(p/'native_server_R134.zip').read_bytes();binary_sha=hashlib.sha256(raw).hexdigest()
assert a['digest']=='sha256:'+binary_sha and a['size_in_bytes']==len(raw)
with zipfile.ZipFile(p/'native_server_R134.zip')as z:
    assert z.testzip()is None;member_count=len(z.infolist())
proof=dict(revision='R134',native_kicad='10.0.7',source_pcb_sha256=sha,source_commit=expected_commit,source_tree=expected_tree,
    run_id=api['id'],run_url=api['html_url'],run_event=api['event'],run_created_utc=api['created_at'],run_updated_utc=api['updated_at'],run_conclusion=api['conclusion'],job_id=jobs['jobs'][0]['id'],
    all12_actual_job_steps_succeeded=True,independent_guards=21,all22_report_results_match_local_excluding_validated_SVG_title_timestamp_hashes=True,
    report_names=results,report_JSON_exact_matches=exact,report_hash_differences_due_only_to_checked_plot_title_timestamp=date_only,
    native_geometry_reference_and_thermal_fills_via_process_and_assembly_exports_match=True,
    actual_plot_geometry_matches_after_only_title_date_normalization=True,normalized_native_plot_sha256=normalized,
    local_raw_plot_sha256=local_hashes,server_raw_plot_sha256=server_hashes,
    artifact_id=a['id'],artifact_bytes=len(raw),artifact_members=member_count,artifact_API_digest=a['digest'],artifact_binary_sha256=binary_sha,
    artifact_binary_downloaded_and_CRC_verified=True,opens=0,ERC=0,schematic_parity=0,drc_types={'hole_clearance':16},fabrication_ready=False,
    U3_filled_capped_fabrication_approved=False,thermal_and_cell_temperature_qualified=False,real_enclosure_and_replaceable_CN_PL_pack_qualified=False)
(p/'proof.json').write_text(json.dumps(proof,indent=2)+'\n')
print('PASS actual R134 source,22 report results,5 native plots,filled planes/via requests,exports,12 job steps and SHA/CRC')
