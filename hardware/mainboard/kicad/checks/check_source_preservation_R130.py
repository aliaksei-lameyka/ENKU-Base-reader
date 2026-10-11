"""Accepted R129 geometry, netlist and file preservation; narrow BAT-REV3 delta."""
import collections,gzip,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R129.json.gz').read_bytes()))
new=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
oa=json.loads((c/'assembly_features_R129.json').read_text());na=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R130.json').read_text())
plan=json.loads((c/'applied_parts_BAT_REV3_R130.json').read_text())
# Native net codes are runtime indices and may be renumbered. Net names and every node remain strictly compared.
op={x['uuid']:x for x in old['pads']};np={x['uuid']:x for x in new['pads']}
oap={x['uuid']:x for x in oa['pads']};nap={x['uuid']:x for x in na['pads']}
changed={x['uuid']:x for x in plan['changed_original_pads']}
assert len(op)==427 and len(np)==428 and len(changed)==4
assert np.keys()==op.keys()|{'daaa0800-0000-4000-8000-000000000082'}
for u,x in op.items():
 y=np[u]
 if u not in changed:assert {k:v for k,v in x.items() if k!='code'}=={k:v for k,v in y.items() if k!='code'} and oap[u]==nap[u],(u,'Undeclared pad/assembly geometry edit')
 else:
  z=changed[u]['after'];a=changed[u]['before']
  for k in ['ref','number','net','pos','size','drill','angle','shape','attribute']:
   assert x[k]==a[k] and y[k]==z[k],(u,k,'Recipe does not match actual source')
  assert y['net']==x['net'] and y['drill']==x['drill'] and y['layers']==x['layers'] and y['drill_shape']==x['drill_shape']
  if x['ref']=='L2':assert x['size']==[1.4,2.3] and y['size']==[1.4,4.2] and y['pos']==[56.15 if x['number']=='1' else 59.85,43]
  elif x['ref']=='J1' and x['number']=='3':
   assert y['ref']=='J8' and y['number']=='1' and y['pos']==x['pos']==[66.95,91.5] and y['size']==x['size'] and y['attribute']==2
   assert nap[u]['layers']==['F.Cu','F.Mask'] and oap[u]['layers']==['F.Cu','F.Mask','F.Paste']
  elif x['ref']=='J1' and x['number']=='MP':assert x['pos']==[72.7,89.15] and y['pos']==[72.7,91.15] and x['size']==y['size']
  else:raise AssertionError(('Unexpected pad delta',u))
  for k in ['local_mask_margin_IU','local_paste_margin_IU','local_paste_ratio']:assert oap[u][k]==nap[u][k]
added=np['daaa0800-0000-4000-8000-000000000082'];assert added['ref']=='J8' and added['number']=='2' and added['net']=='GND' and added['pos']==[64.8,89.3] and added['size']==[1.5,1.5] and not max(added['drill'])
assert nap[added['uuid']]['layers']==['F.Cu','F.Mask']
ot={x['uuid']:x for x in old['tracks']};nt={x['uuid']:x for x in new['tracks']};moves={x['uuid']:x for x in plan['moved_existing_copper']}
assert len(ot)==2639 and len(nt)==2641 and len(moves)==3
assert nt.keys()==ot.keys()|{'daaa0800-0000-4000-8000-000000000083','daaa0800-0000-4000-8000-000000000084'}
for u,x in ot.items():
 y=nt[u]
 if u not in moves:assert {k:v for k,v in x.items() if k!='code'}=={k:v for k,v in y.items() if k!='code'},(u,'Undeclared copper edit')
 else:
  assert x['net']==y['net']=='EPD_VCI' and x['start']==[56.6,44.8] and y['start']==[57.4,44.8]
  for k in ['net','width','layer','via','drill']:assert x[k]==y[k]
  assert y['end']==([57.4,44.8] if x['via'] else x['end'])
for ref,x in old['footprints'].items():
 expected=dict(x,lib=plan['footprint_library_changes'].get(ref,x['lib']))
 if ref=='J1':expected['pos']=[69.8,94.5]
 assert new['footprints'][ref]==expected,(ref,'Unrelated footprint placement changed')
assert new['footprints'].keys()==old['footprints'].keys()|{'J8'}
assert old['bbox']==new['bbox'] and old['board_outline']==new['board_outline']
assert sorted(json.dumps(z,sort_keys=True) for z in old['zones'])==sorted(json.dumps(z,sort_keys=True) for z in new['zones'])
assert_no_split(old,new)
# Reference labels changed only to clear the new PH2 bracket and sensor ground.
oo=json.loads((c/'orientation_reference_R129.json').read_text())['features']
nn=json.loads((out/'orientation.json' if server else c/'orientation_R130.json').read_text())['features']
orfs={x['ref']:x for x in oo if x['type']=='reference_field'};nrfs={x['ref']:x for x in nn if x['type']=='reference_field'}
for ref,x in orfs.items():
 y=nrfs[ref];expected=dict(x)
 if ref=='SW6':expected['position_mm']=[73.5,88.9]
 if ref=='C12':expected['position_mm']=[63.525,90.8]
 assert y==expected,(ref,'Undeclared reference label edit',x,y)

ofs={x['ref']:x for x in oa['footprints']};nfs={x['ref']:x for x in na['footprints']}
for ref,x in ofs.items():
 y=nfs[ref];assert y['attributes']==x['attributes'] and y['dnp']==x['dnp']
 assert y['value']==('1S LiPo PCM / PH-2' if ref=='J1' else x['value'])
 expected=dict(x['fields']);expected['Value']=y['value'];expected.update({k:v for k,v in plan['native_board_fields'].get(ref,{}).items() if k!='Footprint'})
 # The new library has its own standard Description field; it is declared explicitly.
 assert y['fields']==expected,(ref,'Undeclared board field edit',y['fields'],expected)
for file,sha in plan['unchanged_files'].items():assert hashlib.sha256((r/file).read_bytes()).hexdigest()==sha,('Unrelated source/library edit',file)
def blocks(t,keyword):
 result=[]
 for m in re.finditer(r'\('+keyword+r' "',t):
  s=m.start();d=0;q=e=False
  for i in range(s,len(t)):
   ch=t[i]
   if q:
    if e:e=False
    elif ch=='\\':e=True
    elif ch=='"':q=False
   elif ch=='"':q=True
   elif ch=='(':d+=1
   elif ch==')':
    d-=1
    if not d:result.append(t[s:i+1]);break
 return result
oldlib=gzip.decompress((c/'source_R129_ENKU.kicad_sym.gz').read_bytes()).decode();lib=(r/'ENKU.kicad_sym').read_text()
for symbol in blocks(oldlib,'symbol'):assert symbol in lib,'Existing symbol definition changed'
def block(t,s):
 d=0;q=e=False
 for i in range(s,len(t)):
  ch=t[i]
  if q:
   if e:e=False
   elif ch=='\\':e=True
   elif ch=='"':q=False
  elif ch=='"':q=True
  elif ch=='(':d+=1
  elif ch==')':
   d-=1
   if not d:return t[s:i+1],i+1
 raise AssertionError('Unbalanced schematic')
def children(t):
 # Direct children of a balanced s-expression; preserve order and all source tokens.
 s=1;items=[]
 while s<len(t)-1:
  if t[s]=='(':
   a,s=block(t,s);items.append(a)
  else:s+=1
 return items
def tokens(t):return re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',t)
def prop(t,k,v):
 t,n=re.subn(r'(\(property "'+re.escape(k)+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(v),t,count=1)
 if not n:t=t[:-1]+'\n\t\t(property '+json.dumps(k)+' '+json.dumps(v)+' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
 return t
for sheet,edits in plan['schematic_edits'].items():
 original=gzip.decompress((c/('source_R129_'+sheet+'.gz')).read_bytes()).decode();current=(r/sheet).read_text()
 och=children(original);nch=children(current);expected=[]
 for item in och:
  if item.startswith('(symbol (lib_id'):
   ref=re.search(r'\(property "Reference" "([^"]+)"',item)[1]
   if ref=='J1':
    item=item.replace('ENKU:BAT3','ENKU:BAT2');item=prop(item,'Value','1S LiPo PCM / PH-2');item=prop(item,'Description','Protected standard TWO-wire LiPo; separate J8 cell-temperature sensor')
    item=re.sub(r'\n\s*\(pin "3" \(uuid "[^"]+"\)\)','',item,count=1)
   for key,value in edits.get(ref,{}).items():item=prop(item,key,value)
  if sheet=='power.kicad_sch' and item.startswith('(global_label "BAT_TS"') and '70000000-0000-4000-8000-000000000078' in item:continue
  if item.startswith('(lib_symbols'):
   actual=next(z for z in nch if z.startswith('(lib_symbols'))
   additions=[z for z in children(actual) if z.startswith('(symbol "ENKU:BAT2"') or z.startswith('(symbol "ENKU:NTC_WIRE2"')]
   assert len(additions)==(2 if sheet=='power.kicad_sch' else 0)
   filtered='(lib_symbols '+' '.join(z for z in children(actual) if z not in additions)+')'
   assert tokens(filtered)==tokens(item),'An existing embedded symbol definition changed'
   expected.append(tokens(actual));continue
  expected.append(tokens(item))
 additions=[]
 for item in nch:
  if re.search(r'\(uuid "daaa0800-0000-4000-8000-0000000000(?:08|93|94|95)"\)',item) and not item.startswith('(lib_symbols'):additions.append(item)
 assert len(additions)==(4 if sheet=='power.kicad_sch' else 0)
 assert [tokens(z) for z in nch if z not in additions]==expected,(sheet,'Undeclared schematic position, wire, annotation, field, instance or library edit')
def nets(path):return {n.attrib['name']:{(x.attrib['ref'],x.attrib['pin']) for x in n.findall('node')} for n in ET.parse(path).findall('./nets/net')}
a=nets(c/'netlist_R129.xml');z=nets(out/'netlist.xml' if server else c/'netlist_R130.xml')
assert ('J1','3') in a['BAT_TS'];a['BAT_TS'].remove(('J1','3'));a['BAT_TS'].add(('J8','1'));a['GND'].add(('J8','2'));assert a==z,'Unrelated schematic net node edit'
d=json.loads((out/'drc.json' if server else c/'drc_checkpoint_R130.json').read_text());e=json.loads((out/'erc.json' if server else c/'erc_checkpoint_R130.json').read_text())
baseline=json.loads((c/'drc_checkpoint_R129.json').read_text());baseline_erc=json.loads((c/'erc_checkpoint_R129.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
assert d['ignored_checks']==baseline['ignored_checks'] and e['ignored_checks']==baseline_erc['ignored_checks']
def findings(data):return sorted((x['type'],x['severity'],x['description'],tuple(sorted(i['uuid'] for i in x['items']))) for x in data['violations'])
assert findings(d)==findings(baseline),'Native DRC delta differs from unchanged20 hole findings'
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R130',pcb_sha256=sha,original_pad_UUIDs_preserved=427,only_four_declared_original_pad_changes=True,added_bare_sensor_ground_land=1,original_copper_items_preserved=2639,unchanged_original_copper_geometry_items=2636,only_three_declared_L2_via_track_geometry_changes=True,added_sensor_ground_copper_items=2,only_J1_existing_footprint_origin_changed=True,all_other_footprint_placements_preserved=True,all_existing_schematic_net_nodes_preserved_except_J1_3_to_J8_1=True,only_J8_2_GND_node_added=True,all_existing_libraries_and_symbol_definitions_preserved=True,project_rules_exclusions_outline_zones_and_RF_keepouts_preserved=True,native_DRC_same20_findings_by_item_UUID=True,all_previous_connected_pad_groups_preserved=True,fabrication_ready=False)
(out/('source_preservation_audit.json' if server else 'source_preservation_audit_R130.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
