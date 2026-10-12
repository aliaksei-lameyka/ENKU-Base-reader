"""Compare an actual GitHub R138 artifact to the retained native local result.

Only explicit export timestamps may differ. This does not grant a fab release.
"""
import copy, gzip, hashlib, json, re, sys, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

PCB_SHA = '90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971'
REPO = 'aliaksei-lameyka/ENKU-Base-reader'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def svg(data):
    data, n = re.subn(rb'(<title>SVG Image created as [^<]* date )\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}( </title>)', rb'\1EXPORT_TIMESTAMP\2', data)
    assert n == 1, 'Unrecognized native SVG timestamp'
    return data

def gerber(data):
    for pattern in [rb'%TF.CreationDate,[^*]*\*%', rb'G04 Created by KiCad \(PCBNEW 10\.0\.7\) date [^\r\n]*']:
        data, n = re.subn(pattern, b'EXPORT_TIMESTAMP', data)
        assert n == 1, 'Unrecognized Gerber timestamp'
    return data

def drill(data):
    for pattern in [rb'; DRILL file KiCad 10\.0\.7 date [^\r\n]*', rb'; #@! TF.CreationDate,[^\r\n]*']:
        data, n = re.subn(pattern, b'EXPORT_TIMESTAMP', data)
        assert n == 1, 'Unrecognized Excellon timestamp'
    return data

def verify(local, proof, commit, tree, branch):
    local, proof = Path(local), Path(proof)
    read = lambda name: json.loads((proof / (name + '.json')).read_text())
    run, jobs, artifacts, source = (read(n) for n in ['run', 'jobs', 'artifacts', 'source_commit'])
    assert run['head_sha'] == source['sha'] == commit and source['tree']['sha'] == tree
    assert run['head_commit']['tree_id'] == tree and run['head_branch'] == branch
    assert run['status'] == 'completed' and run['conclusion'] == 'success' and run['event'] == 'push'
    assert run['repository']['full_name'] == REPO and jobs['total_count'] == 1
    job = jobs['jobs'][0]
    assert job['head_sha'] == commit and job['status'] == 'completed' and job['conclusion'] == 'success'
    assert all(s['status'] == 'completed' and s['conclusion'] == 'success' for s in job['steps'])
    names = {s['name'] for s in job['steps']}
    assert {'Install SHA-pinned KiCad10.0.7 and exact audit runtime',
            'Record actual run identity in this run artifact',
            'Verify immutable current source with full native checks and27 R138 scopes',
            'Check rejection of stale source baselines and component/geometry regressions',
            'Run actions/upload-artifact@v4'} <= names
    assert artifacts['total_count'] == 1
    art = artifacts['artifacts'][0]
    assert art['name'] == 'enku-native-kicad-' + commit and art['expired'] is False
    assert art['workflow_run']['id'] == run['id'] and art['workflow_run']['head_sha'] == commit
    data = (proof / 'native_server_R138.zip').read_bytes()
    assert len(data) == art['size_in_bytes'] and 'sha256:' + digest(data) == art['digest']
    z = zipfile.ZipFile(proof / 'native_server_R138.zip')
    assert z.testzip() is None
    assert len(z.namelist()) == len(set(z.namelist())) == 79
    for n in z.namelist():
        assert not n.startswith('/') and '..' not in Path(n).parts
    server = proof / 'native'
    z.extractall(server)
    identity = json.loads((server / 'run_identity_R138.json').read_text())
    assert identity == dict(run_id=run['id'], head_sha=commit, ref='refs/heads/' + branch,
                           repository=REPO, native_mode='IMMUTABLE_VERIFY', status='started',
                           fabrication_ready=False, shared_branch_mutation=False)
    local_files = {p.relative_to(local).as_posix() for p in local.rglob('*') if p.is_file()}
    server_files = {p.relative_to(server).as_posix() for p in server.rglob('*') if p.is_file()}
    assert server_files == local_files | {'run_identity_R138.json'}
    for root in [local, server]:
        assert (root / 'source_pcb.sha256').read_text().split()[0] == PCB_SHA
        assert (root / 'version.txt').read_text().strip() == '10.0.7'
    reports, exact_reports, plots = 0, 0, 0
    for rel in sorted(local_files):
        a, b = (local / rel).read_bytes(), (server / rel).read_bytes()
        if rel.startswith('manufacturing_review_R138/'):
            continue
        if rel.endswith('.svg'):
            assert svg(a) == svg(b), rel
            plots += 1
        elif rel.endswith('.json.gz'):
            assert gzip.decompress(a) == gzip.decompress(b), rel
        elif rel == 'netlist.xml':
            ea, eb = ET.fromstring(a), ET.fromstring(b)
            for group in ['components', 'libparts', 'libraries', 'nets']:
                assert ET.tostring(ea.find(group)) == ET.tostring(eb.find(group)), group
        elif rel.endswith('.json'):
            ja, jb = json.loads(a), json.loads(b)
            if ja.get('pcb_sha256', ja.get('committed_pcb_sha256')) == PCB_SHA:
                reports += 1
                assert jb.get('pcb_sha256', jb.get('committed_pcb_sha256')) == PCB_SHA
                if ja == jb:
                    exact_reports += 1
            if rel in ['drc.json', 'erc.json']:
                ja.pop('date'); jb.pop('date')
            if rel in ['U1_plot_audit.json', 'IC_stencil_audit.json']:
                field = 'plot_sha256' if rel.startswith('U1') else 'actual_plot_sha256'
                for root, j in [(local, ja), (server, jb)]:
                    for layer, sha in j[field].items():
                        assert digest((root / (layer + '.svg')).read_bytes()) == sha
                ja.pop(field); jb.pop(field)
            assert ja == jb, rel
        else:
            assert a == b, rel
    assert reports == 28 and exact_reports == 26 and plots == 8
    mr = 'manufacturing_review_R138'
    ma, mb = (json.loads((root / mr / 'manifest_R138.json').read_text()) for root in [local, server])
    assert ma['files'].keys() == mb['files'].keys() and len(ma['files']) == 24
    assert {k:v for k,v in ma.items() if k != 'files'} == {k:v for k,v in mb.items() if k != 'files'}
    for rel in ma['files']:
        a, b = ((root / mr / rel).read_bytes() for root in [local, server])
        for raw, m in [(a, ma), (b, mb)]:
            assert dict(sha256=digest(raw), bytes=len(raw)) == m['files'][rel], rel
        if rel.endswith('.gbr'):
            assert gerber(a) == gerber(b), rel
        elif rel.endswith('.drl'):
            assert drill(a) == drill(b), rel
        elif rel.endswith('.svg'):
            assert svg(a) == svg(b), rel
        elif rel.endswith('.gbrjob'):
            ja, jb = json.loads(a), json.loads(b)
            ja['Header'].pop('CreationDate'); jb['Header'].pop('CreationDate')
            assert ja == jb, rel
        elif rel.endswith('drill-report.txt'):
            norm = lambda raw: re.sub(rb'^Created on [^\r\n]*', b'Created on EXPORT_TIMESTAMP', raw, flags=re.M)
            assert norm(a) == norm(b), rel
        else:
            assert a == b, rel
    drc, erc = (json.loads((server / n).read_text()) for n in ['drc.json', 'erc.json'])
    assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
    assert not any(s['violations'] for s in erc['sheets'])
    rejection = json.loads((server / 'rejection_tests_R138.json').read_text())
    assert rejection['positive_baseline_accepted'] is True and len(rejection['negative_cases_passed']) == 20
    export = json.loads((server / 'manufacturing_export_audit_R138.json').read_text())
    assert export['total_vias_below_published_standard_ring'] == 0 and not export['fabrication_ready']
    result = dict(revision='R138', verified_source_commit=commit, verified_source_tree=tree,
                  verified_branch=branch, pcb_sha256=PCB_SHA, run_id=run['id'], job_id=job['id'],
                  actual_successful_job_steps=len(job['steps']), artifact_id=art['id'],
                  artifact_sha256=digest(data), artifact_bytes=len(data), artifact_members=79,
                  ZIP_CRC_and_actual_API_digest_verified=True, native_kicad='10.0.7',
                  DRC=0, ERC=0, opens=0, schematic_parity=0, independent_scopes=27,
                  compared_reports=28, byte_equivalent_report_values=26,
                  actual_negative_cases_passed=20,
                  two_plot_reports_differ_only_in_verified_timestamp_dependent_hashes=True,
                  exact_normalized_native_SVGs=8, all_24_manufacturing_files_verified=True,
                  only_explicit_export_timestamps_normalized=True,
                  all_native_geometry_nets_assembly_process_and_rejection_reports_identical=True,
                  below_standard_annular_ring_vias=0, physical_qualification='NOT RUN',
                  fabrication_ready=False)
    (proof / 'comparison_R138.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    verify(*sys.argv[1:])
