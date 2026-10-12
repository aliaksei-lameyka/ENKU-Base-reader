"""Compare R123 to server-verified R122; allow only the declared edits."""
import json,gzip,sys,hashlib,collections,copy
from pathlib import Path
from pad_groups import assert_no_split
r=Path(sys.argv[1]).resolve();c=r/'checks';old=json.loads(gzip.decompress((c/'geometry_checkpoint_R122.json.gz').read_bytes()));new=json.loads((c/'geometry_current.json').read_text()) if (c/'geometry_current.json').exists() else json.loads(gzip.decompress((c/'geometry_checkpoint_R123.json.gz').read_bytes()));plan=json.loads((c/'applied_manufacturer_R123.json').read_text())
op={p['uuid']:p for p in old['pads']};np={p['uuid']:p for p in new['pads']};added=set(plan['new_mechanical_pad_uuids']);assert np.keys()-op.keys()==added and not op.keys()-np.keys()
position={m['uuid']:m['after'] for m in plan['contact_pad_changes']+plan['locator_changes']+plan['C18_pad_moves']};size={m['uuid']:m['after_size'] for m in plan['contact_pad_changes']};renames={(m['ref'],m['number']):m for m in plan['declared_unused_contact_net_label_changes']}
for u,a in op.items():
 b=np[u]
 for k in ('ref','number','drill','angle','layers'):assert a[k]==b[k],(u,k)
 m=renames.get((a['ref'],a['number']));assert b['net']==(m['after_net'] if m else a['net']),(u,'net')
 if m:assert a['net']==m['before_net']
 assert b['pos']==position.get(u,a['pos']),(u,'position');assert b['size']==size.get(u,a['size']),(u,'size')
 if u not in position:assert a['polygons']==b['polygons'],(u,'effective copper')
for u in added:assert np[u]['number']=='' and np[u]['net']=='' and np[u]['drill']==[0,0]
allowed={m['ref']:m for m in plan['footprint_moves']}
for ref,f in old['footprints'].items():
 b=new['footprints'][ref];expected=dict(f)
 if ref in allowed:assert f['pos']==allowed[ref]['before'];expected['pos']=allowed[ref]['after']
 assert b==expected,(ref,'placement')
assert old['bbox']==new['bbox'] and old['board_outline']==new['board_outline']
ot={t['uuid']:t for t in old['tracks']};nt={t['uuid']:t for t in new['tracks']};removed=set(plan['removed_BTN_R2_track_uuids']);new_ids=set(plan['new_track_uuids']+plan['new_refinement_track_uuids']+plan['new_BTN_R2_via_uuids'])
assert ot.keys()-nt.keys()==removed and nt.keys()-ot.keys()==new_ids
moves={m['uuid']:m for m in plan['original_BTN_L2_clearance_moves']}
for u in ot.keys()&nt.keys():
 a,b=ot[u],nt[u]
 for k in ('net','width','layer','via','drill'):assert a[k]==b[k],('Surviving copper changed identity',u,k,a,b)
 expected=moves[u]['after'] if u in moves else [a['start'],a['end']];assert [b['start'],b['end']]==expected,('Undeclared copper move',u)
 if u in moves:assert [a['start'],a['end']]==moves[u]['before']
assert_no_split(old,new)
d=json.loads((c/'drc_checkpoint_R123.json').read_text());e=json.loads((c/'erc_checkpoint_R123.json').read_text());assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
assert d['ignored_checks']==json.loads((c/'drc_checkpoint_R122.json').read_text())['ignored_checks'];assert e['ignored_checks']==json.loads((c/'erc_checkpoint_R122.json').read_text())['ignored_checks']
baseline=json.loads((c/'source_R122_unchanged_files_R123.json').read_text())
assert baseline['source_commit']=='1698fbfa4ce06684c97c8e70e58b18c25e0a8d63'
for file,sha in baseline['sha256'].items():
 assert hashlib.sha256((r/file).read_bytes()).hexdigest()==sha,('Unexpected unrelated source edit',file)
report={'revision':'R123','source_R122_sha256':plan['source_R122_sha256'],'pcb_sha256':hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),'original_pad_uuids_preserved':len(op),'added_unnumbered_mechanical_lands':len(added),'declared_pad_position_changes':len(position),'declared_contact_size_changes':len(size),'declared_unused_common_net_label_changes':len(renames),'all_other_effective_pad_copper_preserved':True,'footprint_placements_preserved_except_declared_C18_move':True,'original_copper_items_removed':len(removed),'new_copper_items':len(new_ids),'declared_existing_copper_geometry_moves':len(moves),'all_surviving_copper_net_names_preserved':True,'original_GND_stitch_preserved':plan['original_ground_stitch_retained'],'previously_connected_pad_groups_preserved':True,'project_rules_and_unrelated_schematic_sources_preserved':True,'native_exclusions_unchanged':True,'fabrication_ready':False}
(c/'source_preservation_audit_R123.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
