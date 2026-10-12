"""Record actual identity inside this run artifact; no shared branch writes."""
import json, os, re
from pathlib import Path

repo=os.environ['GITHUB_REPOSITORY']
assert repo=='aliaksei-lameyka/ENKU-Base-reader'
assert os.environ['GITHUB_EVENT_NAME'] in {'push','workflow_dispatch'}
sha=os.environ['GITHUB_SHA'];assert re.fullmatch('[0-9a-f]{40}',sha)
run_id=int(os.environ['GITHUB_RUN_ID']);assert run_id>0
state=dict(run_id=run_id,head_sha=sha,ref=os.environ['GITHUB_REF'],repository=repo,
           native_mode='IMMUTABLE_VERIFY',status='started',fabrication_ready=False,
           shared_branch_mutation=False)
output=Path('native-results');output.mkdir(exist_ok=True)
(output/'run_identity_R136.json').write_text(json.dumps(state,indent=2)+'\n')
print(json.dumps(state))
