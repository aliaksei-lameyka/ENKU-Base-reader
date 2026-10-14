"""Strict downloaded server artifact and 24-file manufacturing comparison.
Only declared creation timestamps are normalized, never geometry or net data.
"""
import hashlib,json,re,sys,zipfile
from pathlib import Path
archive,local,output=map(Path,sys.argv[1:4]);expected=sys.argv[4];digest=hashlib.sha256(archive.read_bytes()).hexdigest();assert digest==expected
z=zipfile.ZipFile(archive);assert z.testzip()is None;names=z.namelist();report=json.loads(z.read('candidate/verification_R143.json'));assert report['pcb_sha256']=='3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266'and report['DRC']==report['ERC']==report['opens']==report['parity']==0 and not report['fabrication_ready']
manifest=json.loads((local/'manifest_R143.json').read_text());assert len(manifest['files'])==24
def normalize(name,data):
 text=data.decode();counts=[]
 def sub(pattern,repl,required):
  nonlocal text
  text,n=re.subn(pattern,repl,text,flags=re.M);assert n==required,(name,pattern,n);counts.append(n)
 if name.endswith('.gbr'):
  sub(r'^(%TF\.CreationDate,)[^*]+(\*%)$',r'\1CREATION_TIMESTAMP\2',1);sub(r'^(G04 Created by KiCad \(PCBNEW 10\.0\.7\) date )[^*]+(\*)$',r'\1CREATION_TIMESTAMP\2',1)
 elif name.endswith('.drl'):
  sub(r'^(; DRILL file KiCad 10\.0\.7 date ).*$',r'\1CREATION_TIMESTAMP',1);sub(r'^(; #@! TF\.CreationDate,).*$',r'\1CREATION_TIMESTAMP',1)
 elif name.endswith('.svg'):
  sub(r'^(<title>SVG Image created as [^<]+ date )[^<]+(</title>)$',r'\1CREATION_TIMESTAMP \2',1)
 elif name.endswith('drill-report.txt'):sub(r'^(Created on ).*$',r'\1CREATION_TIMESTAMP',1)
 elif name.endswith('.gbrjob'):sub(r'^(\s*"CreationDate": ")[^"]+("[,]?)$',r'\1CREATION_TIMESTAMP\2',1)
 return text.encode(),counts
results=[]
for name,meta in manifest['files'].items():
 a=(local/name).read_bytes();b=z.read('candidate/manufacturing_review_R143/'+name);assert hashlib.sha256(a).hexdigest()==meta['sha256'];na,ca=normalize(name,a);nb,cb=normalize(name,b);assert ca==cb and na==nb,('Server manufacturing mismatch',name)
 results.append(dict(path=name,normalized_creation_fields=ca,normalized_sha256=hashlib.sha256(na).hexdigest(),local_sha256=hashlib.sha256(a).hexdigest(),server_sha256=hashlib.sha256(b).hexdigest()))
baseline=json.loads(z.read('baseline/rejection_tests_R138.json'));assert len(baseline['negative_cases_passed'])==20
output.write_text(json.dumps(dict(revision='R143',pcb_sha256=report['pcb_sha256'],archive_sha256=digest,ZIP_members=len(names),ZIP_CRC_verified=True,manufacturing_files=results,all24_manufacturing_payloads_match_after_declared_timestamp_normalization=True,source_report=report,baseline_negative_case_record=baseline,physical_tests='NOT RUN',fabrication_ready=False),indent=2)+'\n');print('Verified API digest, ZIP CRC, current-source report and all24 manufacturing files')
