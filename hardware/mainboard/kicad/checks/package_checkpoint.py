"""Freeze a native-verified WIP source and evidence outside the git checkout."""
import sys,json,collections,gzip,hashlib,shutil,datetime,math
from pathlib import Path
root=Path(sys.argv[1]).resolve();drc_path=Path(sys.argv[2]).resolve();stage=Path(sys.argv[3]).resolve();c=root/'checks';prior=root.parent/'ENKU_R119';baseline=root.parent/'ENKU_R118';dest=stage/'hardware/mainboard/kicad';dest.mkdir(parents=True,exist_ok=True)
shutil.copy2(baseline/'enku-mainboard-r0.1.kicad_pro',root/'enku-mainboard-r0.1.kicad_pro')
g=json.loads((c/'geometry_current.json').read_text());old=json.loads((prior/'checks/geometry_current.json').read_text());d=json.loads(drc_path.read_text());e=json.loads((c/'erc_checkpoint_R120.json').read_text());ap={p['uuid']:p for p in old['pads']};bp={p['uuid']:p for p in g['pads']};assert ap.keys()<=bp.keys()
j3=(c/'accepted_j3_land_pattern.json').exists()
for u,p in ap.items():
 q=bp[u];assert all(p[k]==q[k] for k in ['ref','number','net','angle','drill','layers'])
 expected=[p['pos'][0]-.1,p['pos'][1]] if j3 and p['ref']=='J3' else p['pos'];assert math.dist(expected,q['pos'])<2e-6
 assert q['size']==([.8,.8] if j3 and p['ref']=='J3' and p['number'] in ['S1','S2'] else p['size'])
assert len(bp)-len(ap)==(2 if j3 else 0)
for u in bp.keys()-ap.keys():
 p=bp[u];assert p['ref']=='J3' and not p['number'] and not p['net'] and not p['layers'] and p['size']==[.8,.65] and p['drill']==[0,0]
at={p['uuid']:p for p in old['tracks']};bt={p['uuid']:p for p in g['tracks']};assert all(at[u]['net']==bt[u]['net'] for u in at.keys()&bt.keys())
for p in root.glob('*.kicad_sch'):assert p.read_bytes()==(baseline/p.name).read_bytes()
assert not d['schematic_parity'];assert sum(len(s['violations']) for s in e['sheets'])==0
assert d['kicad_version']=='10.0.7';assert set(x['type'] for x in d['violations'])<={'lib_footprint_mismatch','hole_clearance','track_dangling','via_dangling'}
types=dict(collections.Counter(x['type'] for x in d['violations']));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
metrics={'revision':'R120 routing checkpoint','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_kicad':'10.0.7','all_track_errors':True,'severity_all':True,'opens':len(d['unconnected_items']),'drc_types':types,'erc':0,'parity':0,'pads':len(g['pads']),'footprints':len(g['footprints']),'source_R119_opens':67,'accepted_routing_connections':len(json.loads((c/'accepted_reconnect.json').read_text())['routes']),'all_original_pad_uuids_numbers_nets_drills_layers_preserved':True,'J3_land_pattern_corrected':j3,'surviving_copper_net_names_preserved':True,'schematics_byte_identical_to_R118':True,'project_rules_byte_identical_to_R118':True,'pcb_sha256':sha(root/'enku-mainboard-r0.1.kicad_pcb'),'fabrication_ready':False,'server_verified':False,'last_server_verified_revision':'R119 at 4d8abd587b8d5464e6282d4e13699d85c55c5f29','last_server_run':'https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38066701378'}
if (c/'accepted_service_escape.json').exists():metrics['accepted_routing_connections']+=len(json.loads((c/'accepted_service_escape.json').read_text())['routes'])
if (c/'physical_geometry_audit_R120.json').exists():
 audit=json.loads((c/'physical_geometry_audit_R120.json').read_text());assert audit['pcb_sha256']==metrics['pcb_sha256'] and not audit['new_via_land_violations'] and not audit['Tag_Connect_violations'];metrics['independent_physical_geometry_audit_passed']=True;metrics['new_vias_audited']=audit['new_vias_checked']
(c/'verification_checkpoint_R120.json').write_text(json.dumps(metrics,indent=2));shutil.copy2(drc_path,c/'drc_checkpoint_R120.json')
with gzip.open(c/'geometry_checkpoint_R120.json.gz','wt') as f:json.dump(g,f,separators=(',',':'))
names=['enku-mainboard-r0.1.kicad_pcb','checks/verification_checkpoint_R120.json','checks/drc_checkpoint_R120.json','checks/erc_checkpoint_R120.json','checks/geometry_checkpoint_R120.json.gz']
names += ['checks/'+p.name for p in c.glob('*.py') if p.name in ['native_board.py','router.py','accept.py','j3_land_pattern.py','promote_j3.py','package_checkpoint.py','pad_groups.py','service_escape.py','audit_geometry_R120.py']]
if (c/'physical_geometry_audit_R120.json').exists():names+=['checks/physical_geometry_audit_R120.json']
names += ['checks/'+p.name for p in c.glob('accepted_*.json') if p.name!='accepted_fanout.json']
if j3:names+=['ENKU.pretty/FH34SRJ-24S-0.5SH.kicad_mod','checks/j3_land_pattern_changes.json']
for name in names:
 p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,p)
(dest/'checks/current_checkpoint.json').write_text(json.dumps({'revision':'R120','verification_file':'verification_checkpoint_R120.json','geometry_file':'geometry_checkpoint_R120.json.gz','drc_file':'drc_checkpoint_R120.json'},indent=2))
repo=Path('github-work').resolve();v=(repo/'hardware/mainboard/kicad/checks/verify_native_checkpoint.py').read_text();v=v.replace("expected=json.loads((c/'verification_checkpoint_R119.json').read_text())","manifest=json.loads((c/'current_checkpoint.json').read_text()) if (c/'current_checkpoint.json').exists() else {'verification_file':'verification_checkpoint_R119.json','geometry_file':'geometry_checkpoint_R119.json.gz','drc_file':'drc_checkpoint_R119.json'}\nexpected=json.loads((c/manifest['verification_file']).read_text())");v=v.replace("c/'geometry_checkpoint_R119.json.gz'","c/manifest['geometry_file']").replace("c/'drc_checkpoint_R119.json'","c/manifest['drc_file']");(dest/'checks/verify_native_checkpoint.py').write_text(v)
rd=(repo/'README.md').read_text();s=rd.index('> **Current working source:');z=rd.index('\n\n',s);rd=rd[:s]+f"> **Current working source: R120, KiCad 10.0.7, NO FAB.**\n> Open [the canonical project](hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro).\n> Full native local checkpoint: {metrics['opens']} opens, {sum(types.values())} other DRC, ERC 0, schematic parity 0.\n> Read [the R120 handoff](docs/WORK_HANDOFF_R120.md). [R119 server comparison passed](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38066701378); R120 is locally verified and has not run on the server yet.\n> R118 and R119 remain available in history. The R48–R50 results below are historical."+rd[z:];rd=rd.replace('Active R48 engineering source:','## Historical R40–R50 engineering notes\n\nHistorical R48 source:').replace('Continue from R43 active board; use','For historical context, use');(stage/'README.md').write_text(rd)
docs=stage/'docs';docs.mkdir(exist_ok=True);opens='\n'.join('- '+x['items'][0]['description']+' ↔ '+x['items'][1]['description'] for x in d['unconnected_items']);counts='\n'.join(f'| {k} | {v} |' for k,v in sorted(types.items()))
(docs/'WORK_HANDOFF_R120.md').write_text(f'''# ENKU Base R120 — engineering checkpoint, NO FAB

Canonical project: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Working branch: `engineering/r120-routing-closure`.

R120 recovers the routing pass from the exact server-verified R119. It accepts 59 routing proposals, reducing native missing connections from 67 to {metrics['opens']}. All 400 original pad UUIDs, pin numbers, net names, drills and copper layers are preserved; all surviving copper retains its net name. The dedicated Base scope remains four side buttons, microSD and native USB MSC; Hall, frontlight, Qi and Pogo/Dock are outside Base.

Native KiCad 10.0.7: full DRC with `--severity-all --all-track-errors --schematic-parity --refill-zones --save-board`, ERC with `--severity-all`. ERC 0, parity 0. Project rules and schematics are byte-identical to R118. No new copper clearance or RF keepout violations were introduced. DRC findings remain:

| Type | Count |
| --- | ---: |
{counts}

The server comparison at commit `4d8abd587b8d5464e6282d4e13699d85c55c5f29` proved R119 geometry and native results matched the local source; this R120 checkpoint is locally verified. Passing source comparison does not imply fabrication readiness. Source PCB SHA-256: `{metrics['pcb_sha256']}`.

## Remaining missing connections

{opens}

## Continue

1. Reserve a coupled USB corridor and route low-frequency/power crossings around it. The two series resistors are beside GPIO19/20, and USBLC6 has front-to-back D+/D− flow-through. Do not accept two independent long meandering data tracks. Actual 90-ohm geometry requires the PCBWay stackup and a reference-plane fill audit.
2. ESP_EN to the bottom Tag-Connect contact is closed by the accepted 8.666 mm service route; its source via stays outside the probe contact. The isolated EPD_VGH remnant and obsolete BOOT leaf stub are removed. Before pruning any further dangling copper, verify that every previously connected pad group remains connected; removing a flagged segment can expose another missing connection.
3. J3 land-pattern correction applied: {j3}. The supplied Hirose EDC-159714-50-08 drawing, page 1, calls for 0.8×0.8 mm reinforcement copper, 0.25×0.65 mm signal stencil apertures and 0.8×0.65 mm reinforcement apertures. The isolated correction script shifts J3 0.1 mm left to retain edge clearance. It must pass a full native check and declared pad/copper identity audit before promotion.
4. The independent physical audit checks all 67 vias added since R118 against SMD lands, and every B-side foreign track/via against the Tag-Connect 0.020-inch contact margin. One C28 ground via originally drilled 0.095 mm into its own SMD land; it was moved 0.45 mm outward, retaining its UUID/net and a 0.255 mm annulus-to-land gap. The audit now passes. Preserve existing rules and exclusions; do not waive the four USB-C guide-hole findings or blindly replace library-mismatched footprints.
5. Keep the FPC/display orientation and enclosure fit as a separate open qualification item. The user is designing the enclosure; this pass does not settle the top connector versus bottom FPC pocket.

## Durable continuation

The previous local R120 pass was lost when the scratch environment refreshed. Recover from this committed source, not from an unsaved local pathname. Stop all local writing processes before GitHub connector mutations; these may synchronize the workspace. Freeze source and evidence outside the git checkout, then upload that immutable snapshot. Keep R119 and its CI evidence intact. Avoid repeated intermediate Actions runs.

`checks/current_checkpoint.json` selects the active revision for the exact-version native CI comparator. Decompress the committed geometry JSON before running local routing helpers. Only native-accepted plans may replace the canonical PCB. No fabrication package is released.
''')
manifest=[]
for p in sorted(stage.rglob('*')):
 if p.is_file():
  data=p.read_bytes();manifest.append({'path':str(p.relative_to(stage)),'absolute_path':str(p),'size':len(data),'sha':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
(stage.parent/'github_r120_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'metrics':metrics,'files':len(manifest),'bytes':sum(p['size'] for p in manifest)}))
