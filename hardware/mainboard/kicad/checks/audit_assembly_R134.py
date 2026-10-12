"""Check actual native CPL and explicit bare-PCB/DNP/BOM classification."""
import csv,hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
af=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R134.json').read_text())
fps={x['ref']:x for x in af['footprints']};expected_bare={'H1','H2','H3','H4','J7','J8','TP1','TP2',*(f'TP{i}' for i in range(4,15))}
bare={ref for ref,x in fps.items() if x['attributes']&12};assert bare==expected_bare and len(bare)==19
for ref in bare:
    assert fps[ref]['attributes']&12==12
    for q in af['pads']:
        if q['ref']==ref:assert not any('Paste' in x for x in q['layers']),(ref,'Service land has paste')
dnp={ref for ref,x in fps.items() if x['dnp']};assert dnp=={'R67'}
fitted=fps.keys()-bare-dnp;assert len(fitted)==107
for ref in fps.keys()-bare:assert fps[ref]['attributes']&3==2,(ref,'Missing SMD mount type')
cp=out/('CPL.csv' if server else 'native_CPL_R134.csv');rows=list(csv.DictReader(cp.open()))
assert len(rows)==len(fitted) and {x['Ref'] for x in rows}==fitted
for x in rows:
    ref=x['Ref'];fp=g['footprints'][ref]
    assert x['Val']==fps[ref]['value'] and x['Package']==fp['lib'].split(':',1)[1]
    assert float(x['PosX'])==fp['pos'][0] and float(x['PosY'])==-fp['pos'][1]
    assert (float(x['Rot'])-fp['angle'])%360==0
    assert x['Side']=='top' # Every assembled component is presently on F.Cu.
old=list(csv.DictReader((c/'native_CPL_R128_baseline.csv').open()));assert len(old)==87
added=fitted-{x['Ref'] for x in old};assert added=={'U1','Q1','J2','U3','U4','U5','J3','J5','L1','L2','R12','R80','R81','R82','R83','R84','R85','R86','R87','R88'}
actual=json.loads((out/'orientation.json' if server else c/'orientation_R134.json').read_text())['features']
marks=[x for x in actual if x['type']=='pin1_line'];assert len(marks)==2
edges={tuple(sorted([tuple(x['start_mm']),tuple(x['end_mm'])])) for x in marks}
assert edges=={tuple(sorted([(33.095,85.73),(33.095,86.365)])),tuple(sorted([(33.095,85.73),(33.73,85.73)]))}
assert all(x['layer']==7 and x['width_mm']==.12 for x in marks) # B.SilkS=7 in KiCad10.
plan=json.loads((c/'applied_active_assembly_R129.json').read_text())
labels=[{k:v for k,v in x.items() if k!='type'} for x in actual if x['type']=='probe_label']
wanted=json.loads(json.dumps(plan['preserved_probe_labels']))
for z in wanted:
    if z['ref']=='TP8':z['position_mm']=[55.5,92.7]
assert sorted(labels,key=lambda x:x['ref'])==sorted(wanted,key=lambda x:x['ref'])
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
            if not depth:return text[start:i+1]
    raise ValueError('Unbalanced symbol')
for ref in {'J7','J8'}|{x for x in bare if x.startswith('TP')}:
    found=[]
    for sheet in r.glob('*.kicad_sch'):
        t=sheet.read_text();m='(property "Reference" "'+ref+'"'
        if m in t:
            symbol=block(t,t.rfind('(symbol (lib_id',0,t.index(m)));assert '(in_bom no)' in symbol
            assert '(on_board yes)' in symbol;found.append(sheet.name)
    assert len(found)==1,(ref,'Missing/duplicate bare-PCB schematic classification')
missing=sorted(ref for ref in fitted if not fps[ref]['fields'].get('MPN'))
assert missing==[]
# Review table retains every DNP and bare-PCB item explicitly. It does not
# invent an MPN from a value string or assert that a manufacturing BOM is frozen.
bom=out/('assembly_review_BOM.csv' if server else 'assembly_review_BOM_R134.csv')
names=['Reference','Value','Manufacturer','MPN','Assembly','Footprint','Side','BoardX_mm','BoardY_mm','NativeCPL_X_mm','NativeCPL_Y_mm','Rotation_deg','MPN_field_status']
with bom.open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=names);writer.writeheader()
    for ref in sorted(fps):
        fp=g['footprints'][ref];fields=fps[ref]['fields'];x,y=fp['pos']
        writer.writerow(dict(Reference=ref,Value=fps[ref]['value'],Manufacturer=fields.get('Manufacturer',''),
                            MPN=fields.get('MPN',''),Assembly='BARE_PCB' if ref in bare else 'DNP' if ref in dnp else 'FIT',
                            Footprint=fp['lib'],Side='back' if ref.startswith('TP') or ref=='J7' else 'front',
                            BoardX_mm=x,BoardY_mm=y,NativeCPL_X_mm=x if ref in fitted else '',
                            NativeCPL_Y_mm=-y if ref in fitted else '',Rotation_deg=fp['angle'],
                            MPN_field_status='NOT_AN_ASSEMBLED_PART' if ref in bare else 'EXPLICIT' if fields.get('MPN') else 'FIELD_FREEZE_PENDING'))
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R134',pcb_sha256=sha,actual_native_CPL_and_assembly_classification_verified=True,
            native_CPL_rows=107,accepted_R128_native_CPL_rows=87,previously_omitted_parts_restored=sorted(added),
            bare_PCB_items_excluded=sorted(bare),DNP_excluded=sorted(dnp),
            native_CPL_coordinates_units_and_rotation_verified=True,
            native_CPL_coordinate_convention='mm; X=KiCad boardX; Y=-KiCad boardY; origin0,0; native top-side angles; no supplier normalization applied',
            actual_J7_pin1_marker_targets_pad1=True,all13_probe_names_preserved=True,TP8_move_verified=True,
            fitted_parts_without_explicit_MPN_fields=missing,
            native_CPL_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),
            review_BOM_sha256=hashlib.sha256(bom.read_bytes()).hexdigest(),
            manufacturer_assembly_BOM_CPL_origin_rotation_and_mechanical_release_accepted=False,
            fabrication_ready=False)
(out/('assembly_audit.json' if server else 'assembly_audit_R134.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
