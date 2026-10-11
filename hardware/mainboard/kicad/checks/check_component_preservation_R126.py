"""Strict independent source/copper preservation against accepted R125."""
import gzip,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R125.json.gz').read_bytes()));new=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());plan=json.loads((c/'applied_component_pass_R126.json').read_text())
op={x['uuid']:x for x in old['pads']};np={x['uuid']:x for x in new['pads']};changes={x['uuid']:x for x in plan['declared_pads']};assert op.keys()==np.keys() and len(op)==417 and len(changes)==124
for u,x in op.items():
 y=np[u]
 for k in ['ref','number','net','drill','attribute','layers','drill_shape']:assert x[k]==y[k],(u,k)
 if u in changes:
  q=changes[u]
  for key,label in [('pos','position'),('size','size'),('angle','angle'),('shape','shape')]:
   assert x[key]==q['before_'+label] and y[key]==q['after_'+label],(u,key)
 else:
  for k in ['pos','size','shape','angle','polygons']:assert x[k]==y[k],(u,k)
ot={x['uuid']:x for x in old['tracks']};nt={x['uuid']:x for x in new['tracks']};added={x['uuid']:x for x in plan.get('added_copper_items',[])};assert nt.keys()==ot.keys()|added.keys()
for u,q in added.items():
 for k in ['net','start','end','width','layer','via','drill']:assert nt[u][k]==q[k],(u,k,'Undeclared new copper')
routing={x['uuid']:x for x in plan['routed_copper_changes']}
for u,x in ot.items():
 for k in ['net','width','layer','via','drill']:assert x[k]==nt[u][k],(u,k,'Copper identity changed')
 if u in routing:
  q=routing[u];assert [x['start'],x['end']]==q['before'] and [nt[u]['start'],nt[u]['end']]==q['after'],(u,'Undeclared routing')
 else:assert [x['start'],x['end']]==[nt[u]['start'],nt[u]['end']],(u,'Copper geometry changed')
assert old['footprints'].keys()==new['footprints'].keys()
for ref,x in old['footprints'].items():
 expected=dict(x)
 if ref in plan['recipes']:expected['lib']='ENKU:'+plan['recipes'][ref]['name']
 if ref in plan.get('footprint_placement_changes',{}):expected['pos']=plan['footprint_placement_changes'][ref]['after']
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
 t,n=re.subn(r'(\(property "'+re.escape(key)+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(value),t,count=1)
 if not n:t=t[:-1]+'\n\t\t(property '+json.dumps(key)+' '+json.dumps(value)+' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
 return t
def tokens(t):return re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',t)
for file in ['ENKU.kicad_sym','epd_hv.kicad_sch','power.kicad_sch','mcu_io.kicad_sch','connectors.kicad_sch']:
 expected=gzip.decompress((c/('source_R125_'+file+'.gz')).read_bytes()).decode()
 for ref,q in plan['recipes'].items():
  if file!=q['sheet']:continue
  pos=expected.index('(property "Reference" "'+ref+'"');s=expected.rfind('(symbol (lib_id',0,pos);x,e=block(expected,s)
  for k,v in q['source_fields'].items():x=prop(x,k,v)
  expected=expected[:s]+x+expected[e:]
 assert tokens((r/file).read_text())==tokens(expected),('Undeclared source edit',file)
def nets(path):return {n.attrib['name']:{(x.attrib['ref'],x.attrib['pin']) for x in n.findall('node')} for n in ET.parse(path).findall('./nets/net')}
assert nets(c/'netlist_R125_baseline.xml')==nets(out/'netlist.xml' if server else c/'netlist_R126.xml'),'Schematic net nodes changed'
d=json.loads((out/'drc.json' if server else c/'drc_checkpoint_R126.json').read_text());e=json.loads((out/'erc.json' if server else c/'erc_checkpoint_R126.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
assert d['ignored_checks']==json.loads((c/'drc_checkpoint_R125.json').read_text())['ignored_checks'];assert e['ignored_checks']==json.loads((c/'erc_checkpoint_R125.json').read_text())['ignored_checks']
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
changed=[q for q in changes.values() if any(q['before_'+k]!=q['after_'+k] for k in ['position','size','angle','shape'])]
report=dict(revision='R126',pcb_sha256=sha,original_pad_UUIDs_preserved=417,declared_component_pad_count=124,actual_pad_changes=len(changed),all_other_pad_copper_preserved=True,original_copper_items_preserved=len(ot),all_copper_net_names_preserved=True,declared_copper_items_adjusted=len(routing),declared_copper_items_added=len(added),all_other_copper_geometry_preserved=True,declared_footprint_moves=plan.get('footprint_placement_changes',{}),all_other_footprint_placements_preserved=True,all_previous_pad_groups_preserved=True,all_native_schematic_net_nodes_preserved=True,schematic_and_library_only_declared_metadata_edits=True,project_rules_exclusions_outline_zones_and_RF_keepouts_preserved=True,fabrication_ready=False)
(out/'source_preservation_audit_R126.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
