"""Strict R124 to R125 preservation, including all copper and schematic nets."""
import gzip,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R124.json.gz').read_bytes()));new=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());plan=json.loads((c/'applied_component_lands_R125.json').read_text())
op={x['uuid']:x for x in old['pads']};np={x['uuid']:x for x in new['pads']};changes={x['uuid']:x for x in plan['declared_pad_changes']};assert op.keys()==np.keys() and len(op)==417 and len(changes)==11
for u,x in op.items():
 y=np[u]
 for k in ['ref','number','net','drill','attribute','layers','drill_shape','angle']:assert x[k]==y[k],(u,k)
 if u in changes:
  q=changes[u];assert x['pos']==q['before_position'] and x['size']==q['before_size'];assert y['pos']==q['after_position'] and y['size']==q['after_size'] and y['shape']==q['shape']
 else:
  for k in ['pos','size','shape','polygons']:assert x[k]==y[k],(u,k)
ot={x['uuid']:x for x in old['tracks']};nt={x['uuid']:x for x in new['tracks']};assert ot.keys()==nt.keys()
for u,x in ot.items():
 for k in ['net','start','end','width','layer','via','drill']:assert x[k]==nt[u][k],(u,k,'Copper changed')
assert old['footprints'].keys()==new['footprints'].keys()
for ref,x in old['footprints'].items():
 expected=dict(x)
 if ref in plan['recipes']:expected['lib']='ENKU:'+plan['recipes'][ref]['name']
 assert new['footprints'][ref]==expected,(ref,'Placement changed')
assert old['bbox']==new['bbox'] and old['board_outline']==new['board_outline']
assert sorted(json.dumps(x,sort_keys=True) for x in old['zones'])==sorted(json.dumps(x,sort_keys=True) for x in new['zones'])
assert_no_split(old,new)
for file,sha in plan['unchanged_files'].items():assert hashlib.sha256((r/file).read_bytes()).hexdigest()==sha,('Unrelated source change',file)
def block(t,s):
 depth=0;quoted=False;escaped=False
 for i in range(s,len(t)):
  ch=t[i]
  if quoted:
   if escaped:escaped=False
   elif ch=='\\':escaped=True
   elif ch=='"':quoted=False
  elif ch=='"':quoted=True
  elif ch=='(':depth+=1
  elif ch==')':
   depth-=1
   if depth==0:return t[s:i+1],i+1
 raise ValueError('Unbalanced source')
def prop(t,key,value):
 t,n=re.subn(r'(\(property "'+key+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(value),t,count=1);assert n==1;return t
def tokens(t):return re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',t)
for file in ['ENKU.kicad_sym','epd_hv.kicad_sch','power.kicad_sch','mcu_io.kicad_sch']:
 expected=gzip.decompress((c/('source_R124_'+file+'.gz')).read_bytes()).decode()
 for ref,q in plan['recipes'].items():
  if file!='ENKU.kicad_sym' and file!=q['sheet']:continue
  if file!='ENKU.kicad_sym':
   pos=expected.index('(property "Reference" "'+ref+'"');s=expected.rfind('(symbol (lib_id',0,pos);x,e=block(expected,s);y=prop(prop(x,'Footprint','ENKU:'+q['name']),'Datasheet',q['datasheet']);expected=expected[:s]+y+expected[e:]
  s=expected.index('(symbol "'+('ENKU:' if file!='ENKU.kicad_sym' else '')+q['symbol']+'"');x,e=block(expected,s);y=prop(prop(x,'Footprint','ENKU:'+q['name']),'Datasheet',q['datasheet']);expected=expected[:s]+y+expected[e:]
 assert tokens((r/file).read_text())==tokens(expected),('Undeclared source edit',file)
def nets(path):return {n.attrib['name']:{(x.attrib['ref'],x.attrib['pin']) for x in n.findall('node')} for n in ET.parse(path).findall('./nets/net')}
assert nets(c/'netlist_R124_baseline.xml')==nets(out/'netlist.xml' if server else c/'netlist_R125.xml'),'Schematic net nodes changed'
d=json.loads((out/'drc.json' if server else c/'drc_checkpoint_R125.json').read_text());e=json.loads((out/'erc.json' if server else c/'erc_checkpoint_R125.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
assert d['ignored_checks']==json.loads((c/'drc_checkpoint_R124.json').read_text())['ignored_checks'];assert e['ignored_checks']==json.loads((c/'erc_checkpoint_R124.json').read_text())['ignored_checks']
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R125',pcb_sha256=sha,original_pad_UUIDs_preserved=417,declared_manufacturer_pad_changes=11,all_other_pad_copper_preserved=True,original_copper_items_preserved=len(ot),all_copper_net_names_and_geometry_preserved=True,all_footprint_placements_preserved=True,all_previous_pad_groups_preserved=True,all_native_schematic_net_nodes_preserved=True,schematic_and_library_only_declared_metadata_edits=True,project_rules_exclusions_outline_zones_and_RF_keepouts_preserved=True,fabrication_ready=False)
(out/'source_preservation_audit_R125.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
