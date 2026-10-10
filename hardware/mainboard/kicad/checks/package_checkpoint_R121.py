"""Freeze R121 source and exact native evidence outside the repository checkout."""
import sys,json,gzip,hashlib,shutil,collections,datetime,zipfile
from pathlib import Path
r=Path(sys.argv[1]).resolve();stage=Path(sys.argv[2]).resolve();c=r/'checks';dest=stage/'hardware/mainboard/kicad';dest.mkdir(parents=True,exist_ok=True)
g=json.loads((c/'geometry_current.json').read_text());old=json.loads(Path('restored-geometry-R120.json').read_text());d=json.loads((c/'drc_checkpoint_R121.json').read_text());e=json.loads((c/'erc_checkpoint_R121.json').read_text())
ap={p['uuid']:p for p in old['pads']};bp={p['uuid']:p for p in g['pads']};assert ap.keys()==bp.keys()
for u,p in ap.items():assert all(p[k]==bp[u][k] for k in ['ref','number','net','pos','size','drill','angle','layers','polygons'])
assert old['footprints']==g['footprints'];at={t['uuid']:t for t in old['tracks']};bt={t['uuid']:t for t in g['tracks']};assert all(at[u]['net']==bt[u]['net'] for u in at.keys()&bt.keys())
from pad_groups import assert_no_split
assert_no_split(old,g)
with zipfile.ZipFile('recover-r121.zip') as z:
 for p in r.glob('*.kicad_sch'):assert p.read_bytes()==z.read(p.name)
 for n in ['enku-mainboard-r0.1.kicad_pro','enku-mainboard-r0.1.kicad_dru']:assert (r/n).read_bytes()==z.read(n)
types=dict(collections.Counter(v['type'] for v in d['violations']));assert types=={'lib_footprint_mismatch':111,'hole_clearance':4};assert not d['unconnected_items'] and not d['schematic_parity'];assert sum(len(s['violations']) for s in e['sheets'])==0
sha=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest();physical=json.loads((c/'physical_geometry_audit_R121.json').read_text());usb=json.loads((c/'usb_geometry_audit_R121.json').read_text())
assert physical['pcb_sha256']==usb['pcb_sha256']==sha;assert not physical['new_via_land_violations'] and not physical['Tag_Connect_violations'];assert not usb['all_USB_trace_reference_missing_regions'] and usb['core_reference_missing_area_mm2']<1e-6 and usb['coupled_core_geometry_verified']
prune1=json.loads((c/'accepted_safe_prune_first.json').read_text());close=json.loads((c/'accepted_r121_closure.json').read_text());assert len(prune1['remove_tracks'])==80 and len(close['remove_tracks'])==39 and not set(prune1['remove_tracks'])&set(close['remove_tracks'])
metrics={'revision':'R121 USB routing closure','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_kicad':'10.0.7','all_track_errors':True,'severity_all':True,'opens':0,'drc_types':types,'erc':0,'parity':0,'pads':len(g['pads']),'footprints':len(g['footprints']),'source_R120_opens':6,'obsolete_copper_items_pruned':119,'live_pass_through_tails_trimmed':4,'all_R120_pad_geometry_and_footprint_placement_preserved':True,'all_original_pad_uuids_numbers_nets_drills_layers_preserved':True,'surviving_copper_net_names_preserved':True,'schematics_and_project_rules_byte_identical_to_durable_source':True,'pcb_sha256':sha,'independent_physical_geometry_audit_passed':True,'new_vias_audited':physical['new_vias_checked'],'USB_topology_and_filled_reference_audit_passed':True,'USB_signal_vias_per_net':usb['signal_vias_per_net'],'USB_factory_stackup_confirmed':False,'USB_impedance_qualified':False,'fabrication_ready':False,'server_verified':False,'last_server_verified_revision':'R120 at 22727d5e774f9c7755f558b93db4d91113482764','last_server_run':'https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38074970454'}
(c/'verification_checkpoint_R121.json').write_text(json.dumps(metrics,indent=2)+'\n');(c/'geometry_checkpoint_R121.json.gz').write_bytes(gzip.compress(json.dumps(g,separators=(',',':')).encode(),mtime=0))
(c/'current_checkpoint.json').write_text(json.dumps({'revision':'R121','verification_file':'verification_checkpoint_R121.json','geometry_file':'geometry_checkpoint_R121.json.gz','drc_file':'drc_checkpoint_R121.json'},indent=2)+'\n')
names=['enku-mainboard-r0.1.kicad_pcb']+['checks/'+n for n in ['verification_checkpoint_R121.json','drc_checkpoint_R121.json','erc_checkpoint_R121.json','geometry_checkpoint_R121.json.gz','reference_planes_R121.json.gz','physical_geometry_audit_R121.json','usb_geometry_audit_R121.json','current_checkpoint.json','accepted_safe_prune_first.json','accepted_usb_connector.json','accepted_usb_pair.json','accepted_usb_add.json','accepted_r121_closure.json','drc_usb_add.json','native_board.py','accept.py','prune_copper.py','audit_geometry.py','audit_usb.py','export_reference_planes.py','package_checkpoint_R121.py']]
for n in names:
 p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r/n,p)
shutil.copyfile('restored-native-checker.py',dest/'checks/verify_native_checkpoint.py')
w=stage/'.github/workflows/kicad-native.yml';w.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile('final-workflow.yml',w)
readme=Path('restored-README.md').read_text();a=readme.index('> **Current working source:');b=readme.index('\n\n',a)
readme=readme[:a]+'''> **Current working source: R121, KiCad 10.0.7, NO FAB.**
> Open [the canonical project](hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro).
> Full native local checkpoint: **0 opens, 115 other DRC, ERC 0, schematic parity 0**.
> USB routing and actual filled reference planes pass the independent local audit. [R121 handoff](docs/WORK_HANDOFF_R121.md). Server verification of this exact source is pending; [R120 server evidence](docs/GITHUB_NATIVE_R120.md) remains historical proof.
> R118–R120 sources and evidence remain in history. The R40–R50 engineering notes below are historical.'''+readme[b:]
readme=readme.replace('USB D+/D− remain unrouted pending the actual 90-ohm stackup;','R121 closes D+/D− through the ESD device and both USB-C contact orientations; the actual 90-ohm stackup is still unqualified;')
(stage/'README.md').write_text(readme)
docs=stage/'docs';docs.mkdir(exist_ok=True)
(docs/'WORK_HANDOFF_R121.md').write_text(f'''# ENKU Base R121 — USB routing closure, NO FAB

Canonical project: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Working branch: `engineering/r120-routing-closure`.

All six R120 missing connections are closed. Native KiCad 10.0.7, full severity, all track errors, actual zone refill and schematic parity: **0 opens, ERC 0, parity 0**. No dangling tracks or vias remain. The remaining 115 DRC findings are 111 library footprint mismatches and four inherited USB-C guide-hole clearance findings. These are retained, with unchanged rules and exclusions. Server verification of this exact checkpoint is pending.

PCB SHA-256: `{sha}`. All 402 R120 pad geometries, all 117 footprints and placements are identical; every surviving copper UUID retains its net. The original 400 electrical pad identities remain preserved. Schematics, project settings and rules are unchanged from the durable source. Base remains 59 × 101 mm, four side buttons, microSD and native USB MSC. Hall, frontlight, Qi and Pogo/Dock remain outside Base.

## Physical changes and evidence

The USB-C A6/B6 and A7/B7 duplicates have a local F.Cu breakout with no data vias. The long pair uses B.Cu with 0.20 mm track width and 0.20 mm gap, two signal vias per net, and nearby GND return vias at layer transitions. Six crossing low-frequency or power nets were rerouted around the pair; the accepted SD clock route is about 52.7 mm with its original series resistor retained. Local VBUS/ESD feed routing was rebuilt.

The cleanup removes 119 obsolete Cu elements in two guarded batches (80 + 39) and trims four live pass-through tails to actual junctions. Each removed element was checked against all previously connected pad groups; final native DRC confirms zero opens. A flagged dangling segment can still carry a needed pass-through connection, so blindly deleting every flag is unsafe.

The filled-plane audit found cuts below F.Cu USB caused by BTN_R1 and CC1, plus an isolated MCU ground island. The short BTN_R1 escape and CC1 were moved to In2 outside the B.Cu USB corridor, the MCU island received a GND stitch, and the DM fan-in shifted 0.02 mm clear of a foreign antipad edge. The full USB trace projection now stays over filled GND outside declared own signal-via antipads; the whole coupled core has a clear 1 mm reference strip. Native polygons are unfractured before testing real holes, rather than treating fill fracture seams as physical ground gaps.

The independent land/contact audit checks all {physical['new_vias_checked']} surviving vias added since R118 against SMD lands, including their own-net lands, and all foreign B-side Cu against Tag-Connect contacts. Both checks pass. The retained C28 correction provides 0.255 mm annulus-to-land clearance. The USB audit verifies MCU polarity, resistor nets, USBLC6 flow-through pin mapping and both connector contact orientations.

## USB limitations retained explicitly

Resistor-to-ESD centreline lengths: D− {usb['centreline_lengths_from_series_resistors_to_ESD_mm']['USB_DM_CONN']:.3f} mm; D+ {usb['centreline_lengths_from_series_resistors_to_ESD_mm']['USB_DP_CONN']:.3f} mm. Difference approximately 0.236 mm. This does not establish equal complete connector paths: the A-contact branch skew is {usb['orientation_A_skew_mm']:.3f} mm and B-contact skew {usb['orientation_B_skew_mm']:.3f} mm. The measurement excludes pad spreading, package/via delay and an electromagnetic stackup model. Width/gap are engineering geometry; factory 90-ohm impedance remains unqualified.

## Next release gates

1. Reconcile the 111 library mismatches against actual land patterns and manufacturer MPNs, keeping intentional/custom copper only with evidence. Never replace all footprints blindly or waive mismatches merely to reduce the count.
2. Resolve the four manufacturer USB-C guide-hole findings with the selected vendor footprint and board-fabricator rules.
3. Confirm the actual stackup and USB impedance, review both contact branches, then verify USB MSC, hotplug, OFF/backfeed and SD ownership on hardware.
4. Complete display/FPC pin and orientation qualification, button/connector mechanics, enclosure fit and assembly checks. The user designs the enclosure; top connector versus bottom panel FPC remains open.

The source is an engineering checkpoint, not a fabrication release. No Gerber/BOM/assembly release is issued.

## Reproduce and continue

`checks/current_checkpoint.json` selects the active revision for CI. The workflow installs the SHA-pinned official KiCad 10.0.7 image, runs full DRC/ERC/netlist, exports actual refilled ground polygons and runs `audit_usb.py` on the server geometry. It then compares every committed pad, footprint and track/via geometry plus native counts and exclusions. Passing the source comparison does not waive fabrication findings.

For local routing helpers, decompress `checks/geometry_checkpoint_R121.json.gz` into `checks/geometry_current.json`. The physical audit uses the committed R120 geometry and its preserved via audit as the baseline. The R121 source was recovered from the GitHub zero-open ZIP after a workspace reset; all last changes are now in the declared, native-accepted `accepted_r121_closure.json`. Prefer this canonical source over the older intermediate ZIP. Stop local writers before connector synchronization, and freeze uploads outside the checkout.
''')
manifest=[]
for p in sorted(stage.rglob('*')):
 if p.is_file():
  data=p.read_bytes();manifest.append({'path':str(p.relative_to(stage)),'absolute_path':str(p),'size':len(data),'sha':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
Path('github_r121_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'metrics':metrics,'files':len(manifest),'bytes':sum(x['size'] for x in manifest)}))
