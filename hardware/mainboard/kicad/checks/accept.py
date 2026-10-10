"""Apply proposal on isolated copy, require native DRC and independent net identity."""
import json,sys,subprocess,shutil,collections
from pathlib import Path
from pad_groups import assert_no_split
root=Path(sys.argv[1]).resolve();tag=sys.argv[2];c=root/'checks'; runtime=root.parents[1]/'runtime/AppDir/AppRun';py=c/'native_board.py';pcb='enku-mainboard-r0.1.kicad_pcb';proposal=json.loads((c/('plan_'+tag+'.json')).read_text());base=json.loads((c/'geometry_current.json').read_text());tr=root/'trials'/tag;tr.mkdir(parents=True,exist_ok=True)
for x in root.iterdir():
 if x.suffix in ('.kicad_sch','.kicad_pro','.kicad_dru','.kicad_sym') or x.name.endswith('.pretty') or x.name in ('fp-lib-table','sym-lib-table','standard-footprints','standard-symbols'):
  dest=tr/x.name
  if not dest.exists():dest.symlink_to(x)
def run(args):subprocess.run([str(runtime)]+args,check=True,stdout=subprocess.DEVNULL)
def sig(x):return x['type'],x['description'],tuple(sorted(i['uuid'] for i in x['items']))
inherited=json.loads((c/'drc_usb_add.json').read_text());allowed=collections.Counter(sig(x) for x in inherited['violations'] if x['type']!='items_not_allowed')
for attempt in range(8):
 (tr/'plan.json').write_text(json.dumps(proposal));run(['python3.11',str(py),'apply',str(root/pcb),str(tr/'plan.json'),str(tr/pcb)])
 run(['kicad-cli','pcb','drc','--all-track-errors','--severity-all','--schematic-parity','--refill-zones','--save-board','--format','json','-o',str(tr/'drc.json'),str(tr/pcb)])
 d=json.loads((tr/'drc.json').read_text());run(['python3.11',str(py),'export',str(tr/pcb),str(tr/'geometry.json')]);g=json.loads((tr/'geometry.json').read_text());items={x['uuid']:x for x in g['tracks']};bad=collections.Counter(sig(x) for x in d['violations'] if x['type'] not in ('track_dangling','via_dangling'))-allowed
 bp={x['uuid']:x for x in base['pads']};gp={x['uuid']:x for x in g['pads']};assert bp.keys()==gp.keys()
 for u,p in bp.items():
  assert all(p[k]==gp[u][k] for k in ('ref','number','net','pos','size','angle','drill','layers')),('Pad identity changed',p,gp[u])
 bt={x['uuid']:x for x in base['tracks']}
 for u in bt.keys()&items.keys():assert bt[u]['net']==items[u]['net'],('Copper net changed',bt[u],items[u])
 assert_no_split(base,g)
 if proposal.get('target_opens') is not None:assert len(d['unconnected_items'])==proposal['target_opens'],('Open target not met',len(d['unconnected_items']))
 if bad and proposal.get('require_all_routes'):
  print('CRITICAL BATCH REJECTED; retaining isolated DRC and geometry',flush=True);raise SystemExit(2)
 if not bad and not d['schematic_parity']:
  shutil.copy2(tr/pcb,root/pcb);shutil.copy2(tr/'geometry.json',c/'geometry_current.json');shutil.copy2(tr/'drc.json',c/('drc_'+tag+'.json'));(c/('accepted_'+tag+'.json')).write_text(json.dumps(proposal,indent=2));print('ACCEPT',tag,'routes',len(proposal['routes']),'opens',len(d['unconnected_items']),'DRC',collections.Counter(x['type'] for x in d['violations']),flush=True);break
 violating=[x for x in d['violations'] if sig(x) in bad];badnets={items[i['uuid']]['net'] for x in violating for i in x['items'] if i['uuid'] in items and i['uuid'] not in bt};print('REJECT',tag,'bad types',collections.Counter(x['type'] for x in violating),'nets',badnets,flush=True)
 if not badnets:
  print(json.dumps(violating,indent=2));raise SystemExit(2)
 proposal['routes']=[r for r in proposal['routes'] if r['net'] not in badnets]
 if not proposal['routes'] and not proposal.get('remove_tracks'):raise SystemExit(3)
else:raise SystemExit('No valid batch')
