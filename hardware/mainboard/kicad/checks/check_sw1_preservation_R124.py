"""Compare R124 against the server-verified R123 physical checkpoint."""
import json, gzip, hashlib, sys, re, xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split

r=Path(sys.argv[1]).resolve(); c=r/'checks'
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R123.json.gz').read_bytes()))
new=json.loads((c/'geometry_current.json').read_text()); plan=json.loads((c/'applied_SW1_R124.json').read_text())
op={a['uuid']:a for a in old['pads']}; np={a['uuid']:a for a in new['pads']}
added=set(plan['new_pad_uuids']); changes={a['uuid']:a for a in plan['declared_original_pad_changes']}
assert not op.keys()-np.keys() and np.keys()-op.keys()==added and len(added)==7
assert len(op)==410 and len(np)==417 and len(changes)==2
for u,a in op.items():
 b=np[u]
 for k in ['ref','net','drill','layers','shape','attribute','drill_shape']: assert a[k]==b[k],(u,k)
 if u in changes:
  m=changes[u]; assert a['ref']=='SW1' and b['number']==m['number'] and b['pos']==m['pos'] and b['size']==m['size'] and b['angle']==180
 else:
  for k in ['number','pos','size','angle','polygons']: assert a[k]==b[k],(u,k)
assert new['footprints'].keys()==old['footprints'].keys()
for ref,f in old['footprints'].items():
 expected=dict(f)
 if ref=='SW1': expected.update(pos=plan['SW1_after']['pos'],angle=plan['SW1_after']['angle'],lib=plan['SW1_after']['library'])
 assert new['footprints'][ref]==expected,(ref,'footprint')
assert old['bbox']==new['bbox'] and old['board_outline']==new['board_outline']
assert sorted(json.dumps(z,sort_keys=True) for z in old['zones'])==sorted(json.dumps(z,sort_keys=True) for z in new['zones'])
ot={t['uuid']:t for t in old['tracks']}; nt={t['uuid']:t for t in new['tracks']}
removed=set(plan['removed_track_uuids']); added_copper=set(plan['added_copper_uuids'])
assert ot.keys()-nt.keys()==removed and nt.keys()-ot.keys()==added_copper
assert len(removed)==3 and sum(ot[u]['via'] for u in removed)==1
for u in ot.keys()&nt.keys():
 for k in ['net','start','end','width','layer','via','drill']: assert ot[u][k]==nt[u][k],(u,k,'surviving copper changed')
assert_no_split(old,new)
d=json.loads((c/'drc_checkpoint_R124.json').read_text()); e=json.loads((c/'erc_checkpoint_R124.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
assert d['ignored_checks']==json.loads((c/'drc_checkpoint_R123.json').read_text())['ignored_checks']
assert e['ignored_checks']==json.loads((c/'erc_checkpoint_R123.json').read_text())['ignored_checks']
baseline=json.loads((c/'source_R123_unchanged_files_R124.json').read_text())
for file,sha in baseline['sha256'].items(): assert hashlib.sha256((r/file).read_bytes()).hexdigest()==sha,('Unexpected unrelated edit',file)
def block(text,start):
 depth=0; quoted=False; escaped=False
 for i in range(start,len(text)):
  ch=text[i]
  if quoted:
   if escaped: escaped=False
   elif ch=='\\': escaped=True
   elif ch=='"': quoted=False
  elif ch=='"': quoted=True
  elif ch=='(': depth+=1
  elif ch==')':
   depth-=1
   if depth==0: return text[start:i+1],i+1
 raise ValueError('Unbalanced schematic/library')
def tokens(text): return re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text)
library=(r/'ENKU.kicad_sym').read_text(); start=library.index('(symbol "MK12C03_G015"'); _,end=block(library,start)
assert tokens(library[:start]+library[end:])==tokens(gzip.decompress((c/'source_R123_ENKU.kicad_sym.gz').read_bytes()).decode()),'Unrelated symbol-library edit'
power=(r/'power.kicad_sch').read_text(); prior=gzip.decompress((c/'source_R123_power.kicad_sch.gz').read_bytes()).decode()
start=power.index('(symbol "ENKU:MK12C03_G015"'); _,end=block(power,start); power=power[:start]+power[end:]
start=power.index('(symbol (lib_id "ENKU:MK12C03_G015")'); instance,end=block(power,start)
ostart=prior.index('(symbol (lib_id "ENKU:SW_SPST") (at 205.105 127 0)'); original,_=block(prior,ostart)
restored=instance.replace('ENKU:MK12C03_G015','ENKU:SW_SPST').replace('ENKU:GSWITCH_MK12C03_G015_DRAWING_REVIEW','ENKU:HARD_POWER_SWITCH_PLACEMENT').replace('"MK-12C03-G015"','"HARD POWER"')
restored=restored.replace('(property "Datasheet" "'+plan['source_documents']['A0_exact']['url']+'"','(property "Datasheet" "~"')
restored=re.sub(r'\(pin "3" \(uuid "[^"]+"\)\)', '', restored)
restored=re.sub(r'\(pin "([12])"', lambda m:'(pin "'+('2' if m[1]=='1' else '1')+'"', restored)
assert tokens(restored)==tokens(original),'Undeclared SW1 schematic instance edit'
power=power[:start]+original+power[end:]
start=power.index('(no_connect (at 205.74 134.62)'); marker,end=block(power,start)
assert plan['external_unused_pin_marker']['uuid'] in marker
assert tokens(power[:start]+power[end:])==tokens(prior),'Unrelated power schematic edit'
# Compare every native schematic net node, allowing only the real SW1 pin map.
def nets(path):
 t=ET.parse(path)
 return {n.attrib['name']:{(a.attrib['ref'],a.attrib['pin']) for a in n.findall('node')} for n in t.findall('./nets/net')}
before=nets(c/'netlist_R123_baseline.xml'); after=nets(c/'netlist_R124.xml')
for net, nodes in before.items():
 expected={(ref,('2' if pin=='1' else '1') if ref=='SW1' else pin) for ref,pin in nodes}
 assert after[net]==expected,(net,'undeclared schematic net edit')
assert after.keys()-before.keys()=={'unconnected-(SW1-OFF_UNUSED-Pad3)'}
assert after['unconnected-(SW1-OFF_UNUSED-Pad3)']=={('SW1','3')}
report={'revision':'R124','source_R123_sha256':plan['source_R123_sha256'],'pcb_sha256':hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),'original_pad_uuids_preserved':410,'added_SW1_pad_uuids':7,'declared_original_SW1_pad_changes':2,'all_other_effective_pad_copper_preserved':True,'footprint_placements_and_library_ids_preserved_except_SW1':True,'original_copper_items_removed':len(removed),'obsolete_SW1_via_removed':1,'new_copper_items':len(added_copper),'all_surviving_copper_net_names_and_geometry_preserved':True,'previously_connected_pad_groups_preserved':True,'all_schematic_net_nodes_preserved_except_declared_SW1_pin_map':True,'power_schematic_and_symbol_library_only_declared_SW1_edits':True,'project_rules_and_unrelated_schematic_and_library_sources_preserved':True,'board_outline_zone_outlines_and_RF_keepouts_preserved':True,'native_exclusions_unchanged':True,'fabrication_ready':False}
(c/'source_preservation_audit_R124.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
