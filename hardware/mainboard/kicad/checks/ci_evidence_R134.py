"""Native CI evidence, isolated engineering branch; no manufacturing activity."""
import base64,gzip,hashlib,io,json,os,re,sys,urllib.request,urllib.error,urllib.parse,zipfile,subprocess
class SafeRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  out=super().redirect_request(req,fp,code,msg,headers,url)
  if urllib.parse.urlsplit(req.full_url).netloc!=urllib.parse.urlsplit(url).netloc:out.remove_header('Authorization')
  return out
opener=urllib.request.build_opener(SafeRedirect)
from pathlib import Path
root=Path.cwd();repo=os.environ['GITHUB_REPOSITORY'];token=os.environ['R134_TASK_GH_TOKEN'];branch='engineering/r134-native-evidence'
def api(path,data=None):
 u='https://api.github.com/repos/'+repo+'/'+path;req=urllib.request.Request(u,data=json.dumps(data).encode()if data is not None else None,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
 return json.loads(urllib.request.urlopen(req,timeout=60).read())
def publish(name,obj,base):
 try:api('git/ref/heads/'+branch)
 except urllib.error.HTTPError as e:
  if e.code!=404:raise
  api('git/refs',{'ref':'refs/heads/'+branch,'sha':base})
 data={'message':'Record actual R134 native CI evidence','content':base64.b64encode((json.dumps(obj,indent=2)+'\n').encode()).decode(),'branch':branch}
 try:data['sha']=api('contents/'+name+'?ref='+branch)['sha']
 except urllib.error.HTTPError as e:
  if e.code!=404:raise
 req=urllib.request.Request('https://api.github.com/repos/'+repo+'/contents/'+name,data=json.dumps(data).encode(),method='PUT',headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json'});urllib.request.urlopen(req,timeout=60).read()
if sys.argv[1]=='announce':
 j=dict(run_id=int(os.environ['GITHUB_RUN_ID']),head_sha=os.environ['GITHUB_SHA'],mode=os.environ['R134_NATIVE_MODE'],status='started',fabrication_ready=False);publish('ci_state_R134.json',j,j['head_sha']);print(json.dumps(j))
elif sys.argv[1]=='collect':
 run=api('actions/runs/'+os.environ['R134_EVIDENCE_INPUT_RUN']);assert run['status']=='completed'and run['conclusion']=='success'and run['head_branch']=='engineering/r134-usb-control-connector'
 jobs=api('actions/runs/'+str(run['id'])+'/jobs');assert len(jobs['jobs'])==1;job=jobs['jobs'][0];assert job['conclusion']=='success'and all(s['conclusion']=='success'for s in job['steps'])
 arts=api('actions/runs/'+str(run['id'])+'/artifacts');a=next(a for a in arts['artifacts']if a['name']=='enku-native-kicad-'+run['head_sha']);assert not a['expired']
 req=urllib.request.Request(a['archive_download_url'],headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json'});raw=opener.open(req,timeout=60).read();h=hashlib.sha256(raw).hexdigest();assert a['digest']=='sha256:'+h and a['size_in_bytes']==len(raw)
 z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip()is None;assert all(not Path(n).is_absolute()and '..'not in Path(n).parts for n in z.namelist());data={n:z.read(n)for n in z.namelist()if not n.endswith('/')};source=data['source_pcb.sha256'].decode().split()[0]
 verify='R134_NATIVE_MODE: VERIFY'in(root/'.github/workflows/kicad-native.yml').read_text()
 proof=dict(revision='R134',run_id=run['id'],run_url=run['html_url'],input_head_sha=run['head_sha'],mode='VERIFY'if verify else'REPAIR',source_pcb_sha256=source,all_actual_job_steps_succeeded=True,actual_job_steps=len(job['steps']),job_id=job['id'],artifact_id=a['id'],artifact_bytes=len(raw),artifact_binary_sha256=h,artifact_API_digest=a['digest'],artifact_CRC_verified=True,fabrication_ready=False)
 if verify:
  c=root/'hardware/mainboard/kicad/checks';cp=json.loads((c/'verification_checkpoint_R134.json').read_text());assert cp['pcb_sha256']==source and cp['independent_guards_passed']==21;hashes=json.loads((c/'local_export_hashes_R134.json').read_text())
  def canonical(j):return hashlib.sha256(json.dumps(j,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  def norm(b):
   v,n=re.subn(rb'(<title>SVG Image created as [^<]* date )\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}( </title>)',rb'\1EXPORT_TIMESTAMP\2',b);assert n==1;return v
  plots={}
  for name,h in hashes['plots'].items():assert hashlib.sha256(norm(data[name+'.svg'])).hexdigest()==h;plots[name]=hashlib.sha256(data[name+'.svg']).hexdigest()
  for name,h in hashes['exports'].items():
   b=data[name];actual=canonical(json.loads(gzip.decompress(b)))if name.endswith('.gz')else canonical(json.loads(b))if name.endswith('.json')else hashlib.sha256(b).hexdigest();assert actual==h,name
  import xml.etree.ElementTree as ET
  for group,h in hashes['netlist_sections'].items():assert hashlib.sha256(ET.tostring(ET.fromstring(data['netlist.xml']).find(group))).hexdigest()==h
  reports=[];exact=[];date_only=[]
  for name,b in data.items():
   if not name.endswith('.json'):continue
   j=json.loads(b)
   if not isinstance(j,dict)or j.get('pcb_sha256',j.get('committed_pcb_sha256'))!=source:continue
   local=json.loads((c/('local_'+name)).read_text());reports.append(name)
   if j==local:exact.append(name)
   else:
    assert name in ['U1_plot_audit.json','IC_stencil_audit.json'];key='plot_sha256'if name=='U1_plot_audit.json'else'actual_plot_sha256';assert j.keys()==local.keys()and all(j[k]==local[k]for k in j if k!=key)
    for p in j[key]:assert j[key][p]==plots[p]and local[key][p]==hashes['raw_plots'][p]
    date_only.append(name)
  assert len(reports)==22 and  len(exact)==20 and  len(date_only)==2,(reports,exact,date_only)
  d=json.loads(data['drc.json']);e=json.loads(data['erc.json']);assert not d['unconnected_items']and not d['schematic_parity']and len(d['violations'])==16 and  all(v['type']=='hole_clearance'for v in d['violations']);assert not any(s['violations']for s in e['sheets'])
  proof.update(immutable_source_and_checkpoint_verified=True,source_commit=run['head_sha'],source_tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}']).decode().strip(),independent_guards=21,report_count=22,exact_report_matches=sorted(exact),only_checked_plot_timestamp_hash_differences=sorted(date_only),native_exports_reference_thermal_process_assembly_and_netlist_exact=True,all5_native_plot_geometry_hashes_match=True,opens=0,ERC=0,parity=0,drc_types={'hole_clearance':16})
  publish('proof_R134.json',proof,run['head_sha'])
 else:publish('repair_result_R134.json',proof,run['head_sha'])
 print(json.dumps(proof,indent=2))
else:raise AssertionError(sys.argv)
