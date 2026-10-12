"""Peel obsolete Cu leaves while retaining every original physical pad group."""
import json,sys,subprocess,shutil,re,collections
from pathlib import Path
from pad_groups import assert_no_split
root=Path(sys.argv[1]).resolve();c=root/'checks';tag=sys.argv[2] if len(sys.argv)>2 else 'safe_prune_tail';rt=root.parents[1]/'runtime/AppDir/AppRun';py=c/'native_board.py';pcb='enku-mainboard-r0.1.kicad_pcb';tr=root/'trials'/tag;tr.mkdir(parents=True,exist_ok=True)
base=json.loads((c/'geometry_current.json').read_text());current=(root/pcb).read_text();removed=[];protected=[]
for x in root.iterdir():
 if x.suffix in ('.kicad_sch','.kicad_pro','.kicad_dru','.kicad_sym') or x.name.endswith('.pretty') or x.name in ('fp-lib-table','sym-lib-table','standard-footprints','standard-symbols'):
  dest=tr/x.name
  if not dest.exists():dest.symlink_to(x)
def run(a):subprocess.run([str(rt)]+a,check=True,stdout=subprocess.DEVNULL)
def report():
 (tr/pcb).write_text(current)
 run(['kicad-cli','pcb','drc','--all-track-errors','--severity-all','--schematic-parity','--refill-zones','--format','json','-o',str(tr/'drc.json'),str(tr/pcb)])
 return json.loads((tr/'drc.json').read_text())
for step in range(80):
 d=report(); candidates=[]
 for v in d['violations']:
  if v['type'] in ('track_dangling','via_dangling'):
   candidates.extend(i['uuid'] for i in v['items'])
 accepted=False
 for uid in dict.fromkeys(candidates):
  if uid in protected:continue
  found=[]
  def drop(m):
   u=re.search(r'\(uuid "([^"]+)"\)',m.group(0))
   if u and u[1]==uid:found.append(uid);return ''
   return m.group(0)
  proposal=re.sub(r'^\t\((?:segment|via)\n.*?^\t\)\n',drop,current,flags=re.M|re.S)
  if len(found)!=1:continue
  (tr/'candidate.kicad_pcb').write_text(proposal)
  run(['python3.11',str(py),'export',str(tr/'candidate.kicad_pcb'),str(tr/'candidate_geometry.json')])
  g=json.loads((tr/'candidate_geometry.json').read_text())
  try:assert_no_split(base,g)
  except AssertionError:protected.append(uid);continue
  current=proposal;removed.append(uid);accepted=True;print('Guarded leaf removal',len(removed),uid,flush=True);break
 if not accepted:break
else:raise SystemExit('Exceeded pruning limit')
(c/('plan_'+tag+'.json')).write_text(json.dumps({'routes':[],'remove_tracks':removed,'protected_pad_connectivity':protected,'target_opens':0,'require_all_routes':True},indent=2))
print('PROPOSAL',tag,'removed',len(removed),'protected',len(protected),flush=True)
