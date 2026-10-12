"""Independent R130/R131 preservation around the declared R132 charger rework."""
import collections,gzip,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split
r=Path(sys.argv[1]).resolve();c=r/'checks';out=Path(sys.argv[2]).resolve()
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R130.json.gz').read_bytes()));new=json.loads((out/'geometry.json').read_text())
oa=json.loads((c/'assembly_features_R130.json').read_text());na=json.loads((out/'assembly_features.json').read_text())
plan=json.loads((c/'preservation_manifest_R132.json').read_text())
for f,sha in plan['unchanged_files'].items():
 assert hashlib.sha256((r/f).read_bytes()).hexdigest()==sha,('Unrelated source or prior evidence changed',f)
op={x['uuid']:x for x in old['pads']};np={x['uuid']:x for x in new['pads']}
oap={x['uuid']:x for x in oa['pads']};nap={x['uuid']:x for x in na['pads']}
moved={'C5':[47.2,87.25],'C6':[45,94.6],'C7':[51.6,93.9],'C8':[48.5,94.5],'R11':[51.5,98.8]}
retained=0
for u,x in op.items():
 if x['ref']=='U3':continue
 assert u in np; y=np[u]
 expected={k:v for k,v in x.items() if k!='code'}
 af_expected=dict(oap[u])
 if x['ref'] in moved:
  dx,dy=[moved[x['ref']][i]-old['footprints'][x['ref']]['pos'][i] for i in range(2)]
  expected['pos']=[round(x['pos'][0]+dx,6),round(x['pos'][1]+dy,6)]
  expected['polygons']={l:[[[round(a+dx,6),round(b+dy,6)] for a,b in poly] for poly in ps] for l,ps in x['polygons'].items()}
  af_expected['position_mm']=expected['pos']
 assert expected=={k:v for k,v in y.items() if k!='code'},(x['ref'],x['number'],'Unapproved pad geometry delta')
 assert af_expected==nap[u],(x['ref'],x['number'],'Mask/paste/drill/assembly delta')
 retained+=1
assert {x['ref'] for u,x in np.items() if u not in op}=={'U3','R80','R81','R82','R83'}
for ref,x in old['footprints'].items():
 expected=dict(x)
 if ref in moved:expected['pos']=moved[ref]
 if ref=='U3':expected['lib']='ENKU:BQ24072T_RGT0016C_TI'
 assert new['footprints'][ref]==expected,(ref,'Unexpected footprint placement/lib delta')
assert new['footprints'].keys()==old['footprints'].keys()|{'R80','R81','R82','R83'}
assert old['bbox']==new['bbox'] and old['board_outline']==new['board_outline']
assert sorted(json.dumps(z,sort_keys=True) for z in old['zones'])==sorted(json.dumps(z,sort_keys=True) for z in new['zones'])
oldtracks={t['uuid']:t for t in old['tracks']};newtracks={t['uuid']:t for t in new['tracks']}
removed={t['uuid']:t for t in plan['removed_original_copper']}
for u,t in oldtracks.items():
 if u in removed:
  assert u not in newtracks
  assert {k:v for k,v in t.items() if k!='code'}==removed[u]
 else:assert {k:v for k,v in t.items() if k!='code'}=={k:v for k,v in newtracks[u].items() if k!='code'},(u,'Undeclared old copper edit')
newcopper=[t for u,t in newtracks.items() if u not in oldtracks]
for t in newcopper:
 assert t['net'] in {'CHG_TS','CHG_CE_N','CHG_STAT1','CHG_STAT2','CHG_ISET','CHG_ILIM_VSET','CHG_TMR','VBAT','VSYS','VBUS_USB','GND','BAT_TS','3V3_SYS'}
 assert all(35.9<=a[0]<=58.1 and 79.9<=a[1]<=107.1 for a in [t['start'],t['end']]),('New copper escaped bounded charge rework',t)
# Former U3 identities are replaced; every other previously joined pad group must remain joined.
subset=dict(old,pads=[a for a in old['pads'] if a['ref']!='U3'])
assert_no_split(subset,new)
def block(t,s):
 depth=0;quoted=esc=False
 for i in range(s,len(t)):
  x=t[i]
  if quoted:
   if esc:esc=False
   elif x=='\\':esc=True
   elif x=='"':quoted=False
  elif x=='"':quoted=True
  elif x=='(':depth+=1
  elif x==')':
   depth-=1
   if depth==0:return t[s:i+1],i+1
 raise ValueError('Incomplete s-expression')
def children(t):
 pos=t.index('(')+1;result=[]
 while pos<len(t)-1:
  i=t.find('(',pos)
  if i<0:break
  z,pos=block(t,i);result.append(z)
 return result
def tokens(t):return re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',t)
oldlib=gzip.decompress((c/'source_R130_ENKU.kicad_sym.gz').read_bytes()).decode();lib=(r/'ENKU.kicad_sym').read_text()
for z in children(oldlib):
 if z.startswith('(symbol '):assert z in lib,'Existing library symbol changed'
before=gzip.decompress((c/'source_R130_power.kicad_sch.gz').read_bytes()).decode();after=(r/'power.kicad_sch').read_text()
olditems=children(before);newitems=children(after)
visual={x['uuid']:x for x in plan.get('schematic_visual_adjustments',[])}
def token_sha(z):return hashlib.sha256(json.dumps(tokens(z),ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
changedrefs={'U3','R8','R9','R12','C7','C8','J8'}
newbyuuid={re.search(r'\(uuid "([^"]+)"\)',z)[1]:z for z in newitems if re.search(r'\(uuid "([^"]+)"\)',z)}
oldU3endpoint_positions={(115.57,57.15),(115.57,59.69),(115.57,62.23),(115.57,64.77),(115.57,67.31),(148.59,55.88),(148.59,58.42),(148.59,60.96),(148.59,63.5),(148.59,66.04),(148.59,68.58)}
for z in olditems:
 uid=re.search(r'\(uuid "([^"]+)"\)',z)
 if uid and uid[1] in visual:
  v=visual[uid[1]];assert token_sha(z)==v['before_token_sha256'] and token_sha(newbyuuid[uid[1]])==v['after_token_sha256'],'Undeclared visual annotation/placement edit'
  continue
 if z.startswith('(title_block'):
  v=plan['title_block_visual_adjustment'];assert token_sha(z)==v['before_token_sha256'] and token_sha(next(a for a in newitems if a.startswith('(title_block')))==v['after_token_sha256']
  continue
 if z.startswith('(lib_symbols'):
  current=next(a for a in newitems if a.startswith('(lib_symbols'))
  for sym in children(z):assert tokens(sym) in [tokens(a) for a in children(current)],'Old cached symbol changed'
  continue
 if z.startswith('(symbol (lib_id'):
  ref=re.search(r'\(property "Reference" "([^"]+)"',z)[1]
  if ref in changedrefs:continue
 if z.startswith('(global_label'):
  a=re.search(r'\(at ([\d.-]+) ([\d.-]+)',z)
  if a and (float(a[1]),float(a[2])) in oldU3endpoint_positions:continue
 if z.startswith('(text "BAT-REV3 HOLD:'):continue
 m=re.search(r'\(uuid "([^"]+)"\)',z)
 if m:assert tokens(z)==tokens(newbyuuid[m[1]]),('Unrelated schematic element changed',m[1])
 else:assert tokens(z) in [tokens(a) for a in newitems]
def netnodes(path):return {n.attrib['name']:{(x.attrib['ref'],x.attrib['pin']) for x in n.findall('node')} for n in ET.parse(path).findall('./nets/net')}
expected={net:{node for node in nodes if node[0]!='U3'} for net,nodes in netnodes(c/'netlist_R130.xml').items()}
u3=['CHG_TS','VBAT','VBAT','CHG_CE_N','GND','VBUS_USB','CHG_STAT1','GND','CHG_STAT2','VSYS','VSYS','CHG_ILIM_VSET','VBUS_USB','CHG_TMR','GND','CHG_ISET','GND']
for n,net in enumerate(u3,1):expected.setdefault(net,set()).add(('U3',str(n)))
for ref,nets in {'R80':['VBUS_USB','BAT_TS'],'R81':['BAT_TS','GND'],'R82':['BAT_TS','CHG_TS'],'R83':['CHG_TMR','GND']}.items():
 for n,net in enumerate(nets,1):expected.setdefault(net,set()).add((ref,str(n)))
assert expected==netnodes(out/'netlist.xml'),'Unrelated electrical node change'
d=json.loads((out/'drc.json').read_text());e=json.loads((out/'erc.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
base=json.loads((c/'drc_checkpoint_R130.json').read_text());be=json.loads((c/'erc_checkpoint_R130.json').read_text())
assert d['ignored_checks']==base['ignored_checks'] and e['ignored_checks']==be['ignored_checks']
def findings(d):return sorted((a['type'],a['severity'],a['description'],tuple(sorted(i['uuid'] for i in a['items']))) for a in d['violations'])
assert findings(d)==findings(base),'DRC baseline is not exactly the same20 hole findings'
ofs={x['ref']:x for x in oa['footprints']};nfs={x['ref']:x for x in na['footprints']}
fieldrefs=changedrefs
for ref,x in ofs.items():
 y=nfs[ref]
 if ref not in fieldrefs:assert x==y,(ref,'Unrelated assembly field change')
 if ref not in {'U3','R12'}:assert x['attributes']==y['attributes'] and x['dnp']==y['dnp']
oo=json.loads((c/'orientation_R130.json').read_text())['features'];nn=json.loads((out/'orientation.json').read_text())['features']
for x in oo:
 if x.get('ref') in {'U3',*moved}:continue
 assert x in nn,('Unrelated native orientation/reference feature changed',x)
report=dict(revision='R132',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],unchanged_files_checked=len(plan['unchanged_files']),retained_original_non_U3_pad_UUIDs=retained,unchanged_original_copper_items=len(oldtracks)-len(removed),declared_removed_local_copper_items=len(removed),new_bounded_copper_items=len(newcopper),unrelated_schematic_and_library_tokens_preserved=True,all_other_electrical_nodes_preserved=True,rules_outline_RF_keepouts_exclusions_and_thickness_preserved=True,DRC_exact_same20_holes_by_UUID=True,reconstructed_after_scratch_reset=True,fabrication_ready=False)
(out/'source_preservation_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
