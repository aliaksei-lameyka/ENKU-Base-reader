"""Publish the actual run identity to an isolated branch, never repair source."""
import base64, json, os, re, urllib.error, urllib.request

repo=os.environ['GITHUB_REPOSITORY']
assert repo=='aliaksei-lameyka/ENKU-Base-reader'
assert os.environ['GITHUB_EVENT_NAME'] in {'push','workflow_dispatch'}
token=os.environ['R136_TASK_GH_TOKEN']
branch='engineering/r136-native-evidence'
sha=os.environ['GITHUB_SHA'];assert re.fullmatch('[0-9a-f]{40}',sha)
def api(path, data=None, method=None):
    request=urllib.request.Request('https://api.github.com/repos/'+repo+'/'+path,
            data=None if data is None else json.dumps(data).encode(), method=method,
            headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
                     'X-GitHub-Api-Version':'2022-11-28'})
    with urllib.request.urlopen(request,timeout=30) as response:
        return json.load(response)
try:
    api('git/ref/heads/'+branch)
except urllib.error.HTTPError as error:
    if error.code!=404:raise
    api('git/refs',dict(ref='refs/heads/'+branch,sha=sha))
name='ci_state_R136.json'
state=dict(run_id=int(os.environ['GITHUB_RUN_ID']),head_sha=sha,ref=os.environ['GITHUB_REF'],
           status='started',native_mode='IMMUTABLE_VERIFY',fabrication_ready=False)
data=dict(message='Record actual R136 native verification run identity',branch=branch,
          content=base64.b64encode((json.dumps(state,indent=2)+'\n').encode()).decode())
try:
    data['sha']=api('contents/'+name+'?ref='+branch)['sha']
except urllib.error.HTTPError as error:
    if error.code!=404:raise
api('contents/'+name,data,'PUT')
print(json.dumps(state))
