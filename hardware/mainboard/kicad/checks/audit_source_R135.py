"""Exact R134 preservation with finite, declared R135 switch/TS changes."""
import gzip,hashlib,json,sys,collections,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split
r,o=map(lambda s:Path(s).resolve(),sys.argv[1:3]);c=r/'checks';repo=r.parents[2]
m=json.loads((c/'preservation_manifest_R135.json').read_text());g=json.loads((o/'geometry.json').read_text());old=json.loads(gzip.decompress((c/'geometry_checkpoint_R134.json.gz').read_bytes()));sha=(o/'source_pcb.sha256').read_text().split()[0]
for path,h in m['unchanged_parent_files'].items():assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==h,path
for path,h in m['checked_source_sha256'].items():assert (sha if path.endswith('.kicad_pcb')else hashlib.sha256((repo/path).read_bytes()).hexdigest())==h,path
assert g['bbox']==old['bbox']and g['board_outline']==old['board_outline']
assert collections.Counter(json.dumps(z,sort_keys=True)for z in g['zones'])==collections.Counter(json.dumps(z,sort_keys=True)for z in old['zones']if z['name']!='TL3340 P021301B circuit trace keepout')
switches={'SW3','SW4','SW5','SW6'}
for ref,f in old['footprints'].items():
 want=dict(f)
 if ref in switches:want['lib']='ENKU:TL1016AAF160QG_ESWITCH_P520001';want['pos']=[21.55 if ref in ['SW3','SW4']else 73.45,f['pos'][1]]
 assert g['footprints'][ref]==want,ref
assert old['footprints'].keys()==g['footprints'].keys()
def ix(rows):return {x['uuid']:{k:v for k,v in x.items()if k!='code'}for x in rows}
a,b=ix(old['tracks']),ix(g['tracks']);removed=set(m['removed_old_copper']);assert a.keys()-b.keys()==removed and len(removed)==20
approved=set(json.loads((c/'applied_switch_ntc_R135.json').read_text())['exact_removed_GND_terminal_spur_UUIDs'])|set(json.loads((c/'applied_switch_repair_R135.json').read_text())['remove_tracks']);assert removed==approved
changed=[]
for u in a.keys()&b.keys():
 if a[u]!=b[u]:changed.append(u);assert u=='1ffd319f-3120-440a-9a11-d4babb0b9d2e';want=dict(a[u]);want['start']=[23.2,83.075];assert b[u]==want
assert changed==['1ffd319f-3120-440a-9a11-d4babb0b9d2e']
assert b.keys()-a.keys()==set(m['added_copper'])
for u in b.keys()-a.keys():assert b[u]==m['added_copper'][u]and b[u]['width']>=.2
a,b=ix(old['pads']),ix(g['pads'])
for u,p in a.items():
 if p['ref']in switches:continue
 assert b[u]==p,u
for ref in switches:
 ps=[p for p in old['pads']if p['ref']==ref];ns=[p for p in g['pads']if p['ref']==ref]
 assert len(ps)==7 and len(ns)==4 and not any(max(p['drill'])for p in ns)
 assert {p['uuid']for p in ps if p['number']}<={p['uuid']for p in ns}
adjusted=json.loads(json.dumps(old))
for p in adjusted['pads']:
 if p['ref']in switches:p['net']=''
assert_no_split(adjusted,g)
def nodes(path):return {(a.attrib['ref'],a.attrib['pin']):n.attrib['name']for n in ET.parse(path).findall('./nets/net')for a in n.findall('node')}
before,after=nodes(c/'netlist_R134.xml'),nodes(o/'netlist.xml')
for k,n in before.items():
 if k[0]in switches and k[1]=='2':continue
 assert after[k]==n,k
for ref,net in [('SW3','BTN_L1'),('SW4','BTN_L2'),('SW5','BTN_R1'),('SW6','BTN_R2')]:assert {p:after[(ref,p)]for p in ['1','2','3','4']}=={'1':net,'2':net,'3':'GND','4':'GND'}
d=json.loads((o/'drc.json').read_text());base=json.loads((c/'drc_checkpoint_R134.json').read_text());assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']and d['ignored_checks']==base['ignored_checks']
report=dict(revision='R135',pcb_sha256=sha,unchanged_R134_parent_files=len(m['unchanged_parent_files']),exact20_old_copper_removals_and_single_3V3_jog_verified=True,all_old_non_switch_physical_pads_and_core_positions_preserved=True,original_outline_stack_RF_and_non_switch_zones_preserved=True,explicit_four_terminal_switch_pairs_verified=True,native_DRC_ERC_parity_and_opens_zero=True,fabrication_ready=False)
(o/'source_preservation_R135.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
