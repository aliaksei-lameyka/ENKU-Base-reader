"""Full accepted R128 preservation with a fixed, narrow engineering delta."""
import collections,gzip,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pad_groups import assert_no_split
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R128.json.gz').read_bytes()))
new=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
oa=json.loads((c/'assembly_features_R128.json').read_text());na=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R129.json').read_text())
plan=json.loads((c/'applied_active_assembly_R129.json').read_text())
op={x['uuid']:x for x in old['pads']};np={x['uuid']:x for x in new['pads']}
oap={x['uuid']:x for x in oa['pads']};nap={x['uuid']:x for x in na['pads']}
changed={x['uuid']:x for x in plan['changed_original_pads']};added={x['uuid']:x for x in plan['added_paste_pads']}
assert len(op)==425 and len(np)==427 and len(changed)==25 and len(added)==2
assert np.keys()==op.keys()|added.keys() and not op.keys()&added.keys()
def shape(a,layer):return unary_union([Polygon(q) for q in a['polygons'].get(str(layer),[])])
ep=[];delta_count=collections.Counter()
for u,x in op.items():
    y=np[u]
    for key in ['ref','number','net','pos','size','drill','drill_shape','layers']:
        if key=='size' and x['ref']=='U3' and not x['number']:continue
        assert x[key]==y[key],(u,key,'Pad identity, net, position, drill or copper layers changed')
    if u not in changed:
        assert oap[u]==nap[u],(u,'Undeclared assembly change')
        for key in ['shape','attribute','angle']:assert x[key]==y[key],(u,key)
    else:
        a,z=changed[u]['before'],changed[u]['after'];q=nap[u]
        for key in ['ref','number','net','pos','size','drill','angle','shape','attribute']:
            source=key if key not in ['pos','size','drill'] else {'pos':'position_mm','size':'size_mm','drill':'drill_mm'}[key]
            if key not in ['angle','shape','net']:assert q[source]==z[key],(u,key,'Wrong declared pad change')
            if key in x:assert x[key]==a[key],(u,key,'Wrong accepted baseline')
            assert y[key]==z[key],(u,key,'Wrong native post-state')
        names={0:'F.Cu',1:'F.Mask',2:'B.Cu',3:'B.Mask',13:'F.Paste'}
        assert q['layers']==[names[s] for s in z['layers']]
        assert q['roundrect_radius_mm']==z['roundrect_radius_mm']
        for k,s in [('local_mask_margin_IU','mask'),('local_paste_margin_IU','paste'),('local_paste_ratio','paste_ratio')]:
            assert q[k]==z[s],(u,k,'Undeclared aperture override')
        delta_count[x['ref']]+=1
        if x['ref']=='U3':
            assert x['angle']==0 and y['angle']==180
            if not x['number']:
                assert q['layers']==['F.Paste'] and q['size_mm']==[.85,1.38]
                assert abs(q['roundrect_radius_mm']-.05)<1e-6
            elif x['number']=='11':
                assert y['shape']==4 and q['layers']==['F.Cu','F.Mask']
                assert abs(q['roundrect_radius_mm']-.05)<1e-6;ep.append(u)
            else:assert oap[u]==dict(nap[u]),(u,'Orientation is not an assembly geometry change')
        elif x['ref']=='U8':
            assert (y['angle']-x['angle'])%360==180 and oap[u]==nap[u]
        elif x['ref']=='J7':
            assert x['attribute']==1 and y['attribute']==2
            assert dict(oap[u],attribute=2)==nap[u]
        elif x['ref']=='U4':
            assert x['number']=='8' and q['layers']==['F.Cu','F.Mask']
            expected=dict(oap[u],layers=['F.Cu','F.Mask']);assert expected==nap[u]
        else:raise AssertionError(('Unexpected ref',x['ref']))
    for layer in x['layers']:
        a,z=shape(x,layer),shape(y,layer)
        if x['ref']=='U3' and x['number']=='11':
            assert abs((a.area-z.area)-(4-__import__('math').pi)*.05**2)<1e-4 # Native ERROR_OUTSIDE polygon approximation.
            assert z.bounds==a.bounds and z.difference(a).area<1e-10
        else:assert a.symmetric_difference(z).area<1e-10,(u,layer,'Undeclared copper geometry change')
assert delta_count=={'U3':12,'U8':6,'J7':6,'U4':1} and len(ep)==1
for u,z in added.items():
    x=np[u];q=nap[u]
    assert x['ref']=='U4' and not x['number'] and not x['net'] and not x['layers'] and not max(x['drill'])
    assert x['pos']==z['pos'] and x['size']==[.55,.25] and q['layers']==['F.Paste']
    assert abs(q['roundrect_radius_mm']-.05)<1e-6
ot={x['uuid']:x for x in old['tracks']};nt={x['uuid']:x for x in new['tracks']}
assert len(ot)==2639 and ot.keys()==nt.keys()
for u,x in ot.items():
    for key in ['net','start','end','width','layer','via','drill']:assert x[key]==nt[u][key],(u,key,'Routing changed')
for ref,x in old['footprints'].items():
    assert new['footprints'][ref]==dict(x,lib=plan['footprint_library_changes'].get(ref,x['lib'])),ref
assert old['bbox']==new['bbox'] and old['board_outline']==new['board_outline']
assert sorted(json.dumps(z,sort_keys=True) for z in old['zones'])==sorted(json.dumps(z,sort_keys=True) for z in new['zones'])
assert_no_split(old,new)
ofs={x['ref']:x for x in oa['footprints']};nfs={x['ref']:x for x in na['footprints']}
for ref,x in ofs.items():
    y=nfs[ref];a=plan['footprint_attribute_changes'].get(ref)
    if a:assert x['attributes']==a['before']
    assert y['attributes']==(a['after'] if a else x['attributes']) and y['dnp']==x['dnp'] and y['value']==x['value']
    expected=dict(x['fields']);expected.update({k:v for k,v in plan['native_board_fields'].get(ref,{}).items() if k!='Footprint'})
    assert y['fields']==expected,(ref,'Undeclared native field change')
for file,sha in plan['unchanged_files'].items():assert hashlib.sha256((r/file).read_bytes()).hexdigest()==sha,('Unrelated source edit',file)
tokens=lambda t:re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',t)
for rel,edit in plan['library_mount_type_edits'].items():
    base=gzip.decompress((c/('source_R128_'+Path(rel).name+'.gz')).read_bytes()).decode()
    expected=base.replace('(layer "F.Cu")','(layer "F.Cu")\n\t(attr smd)',1)
    assert hashlib.sha256(base.encode()).hexdigest()==edit['before_sha256']
    assert tokens((r/rel).read_text())==tokens(expected),'Undeclared library geometry change'
def block(text,start):
    depth=0;quote=escaped=False
    for i in range(start,len(text)):
        ch=text[i]
        if quote:
            if escaped:escaped=False
            elif ch=='\\':escaped=True
            elif ch=='"':quote=False
        elif ch=='"':quote=True
        elif ch=='(':depth+=1
        elif ch==')':
            depth-=1
            if not depth:return text[start:i+1],i+1
    raise ValueError('Unbalanced source')
def prop(text,key,value):
    text,n=re.subn(r'(\(property "'+re.escape(key)+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(value),text,count=1)
    if not n:text=text[:-1]+'\n\t\t(property '+json.dumps(key)+' '+json.dumps(value)+' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
    return text
for sheet,edits in plan['schematic_edits'].items():
    text=gzip.decompress((c/('source_R128_'+sheet+'.gz')).read_bytes()).decode()
    for ref,edit in edits.items():
        pos=text.index('(property "Reference" "'+ref+'"');start=text.rfind('(symbol (lib_id',0,pos)
        symbol,end=block(text,start)
        for key,value in edit['fields'].items():symbol=prop(symbol,key,value)
        if edit['in_bom'] is False:symbol=symbol.replace('(in_bom yes)','(in_bom no)',1)
        text=text[:start]+symbol+text[end:]
    assert tokens((r/sheet).read_text())==tokens(text),('Undeclared schematic edit',sheet)
def nets(path):return {n.attrib['name']:{(x.attrib['ref'],x.attrib['pin']) for x in n.findall('node')} for n in ET.parse(path).findall('./nets/net')}
assert nets(c/'netlist_R128_baseline.xml')==nets(out/'netlist.xml' if server else c/'netlist_R129.xml')
d=json.loads((out/'drc.json' if server else c/'drc_checkpoint_R129.json').read_text())
e=json.loads((out/'erc.json' if server else c/'erc_checkpoint_R129.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
assert d['ignored_checks']==json.loads((c/'drc_checkpoint_R128.json').read_text())['ignored_checks']
assert e['ignored_checks']==json.loads((c/'erc_checkpoint_R128.json').read_text())['ignored_checks']
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R129',pcb_sha256=sha,original_pad_UUIDs_preserved=425,original_copper_items_preserved=2639,
            all_original_pad_numbers_nets_positions_and_drills_preserved=True,
            only_declared_25_pad_assembly_changes=True,added_paste_only_pads=2,
            only_U3_EP_corner_copper_rounding_changed=True,all_other_pad_copper_geometry_preserved=True,
            all_track_via_geometry_and_net_names_preserved=True,all_footprint_placements_preserved=True,
            all_native_schematic_net_nodes_preserved=True,all_previous_pad_groups_preserved=True,
            only_declared_metadata_and_library_mount_types_changed=True,
            project_rules_exclusions_outline_zones_and_RF_keepouts_preserved=True,
            all_USB_button_and_thermal_holes_preserved=True,fabrication_ready=False)
(out/('source_preservation_audit.json' if server else 'source_preservation_audit_R129.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
