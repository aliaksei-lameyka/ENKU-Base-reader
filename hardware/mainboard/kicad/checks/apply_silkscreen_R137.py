"""One-time UUID-bounded silk stroke repair from SHA-pinned accepted R136."""
import hashlib,json,re,sys
from pathlib import Path
from cad_text_R134 import children,instance,prop

r=Path(sys.argv[1]).resolve();inventory=Path(sys.argv[2]);c=r/'checks'
pcb=r/'enku-mainboard-r0.1.kicad_pcb';before=pcb.read_text()
assert hashlib.sha256(before.encode()).hexdigest()=='396a7ee137778778539848e9e1a3a7b95518ce329b63425822e191f1ef9c6849'
native=json.loads(inventory.read_text())
wanted={x['uuid']:x for x in native if x.get('pen_mm',x.get('width_mm'))<.15}
assert len(wanted)==72
rows=[];edits=[]
for a,z,part in children(before):
    candidates=[(a,z,part)]
    if part.startswith('(footprint '):
        candidates=[(a+x,a+y,v)for x,y,v in children(part)]
    for x,y,item in candidates:
        match=re.search(r'\(uuid "([^"]+)"\)',item)
        if not match or match[1] not in wanted:continue
        identity=match[1];row=wanted[identity]
        source_layer={'f.silkscreen':'F.SilkS','b.silkscreen':'B.SilkS'}.get(row['layer'],row['layer'])
        assert '(layer "'+source_layer+'"'in item
        name='thickness' if 'pen_mm'in row else 'width'
        old=row.get('nominal_pen_mm',row.get('width_mm'))
        new,n=re.subn(r'\('+name+r' ([\d.]+)\)',lambda m:'('+name+' 0.15)'if float(m[1])==old else m[0],item)
        assert n==1 and new!=item,(row,n)
        edits.append((x,y,new));rows.append(dict(uuid=identity,ref=row['ref'],layer=row['layer'],type=row['type'],
            text=row.get('text'),old_width_mm=old,new_width_mm=.15,before=item,after=new))
assert {x['uuid']for x in rows}==wanted.keys()and len(rows)==72
after=before
for a,z,item in sorted(edits,reverse=True):after=after[:a]+item+after[z:]
root_edits=[]
for a,z,item in reversed(list(children(after))):
    if item.startswith('(layers\n'):
        anchor='\t\t(2 "B.Cu" signal)'
        assert item.count(anchor)==1 and not any('"'+v+'"'in item for v in ['F.Mask','B.Mask','F.Paste','B.Paste'])
        new=item.replace(anchor,anchor+'\n\t\t(13 "F.Paste" user)\n\t\t(15 "B.Paste" user)')
        anchor='\t\t(7 "B.SilkS" user "b.silkscreen")'
        new=new.replace(anchor,anchor+'\n\t\t(1 "F.Mask" user)\n\t\t(3 "B.Mask" user)')
        root_edits.append(dict(kind='layers',before=item,after=new));after=after[:a]+new+after[z:]
    elif item.startswith('(title_block\n'):
        new=item.replace('(date "2026-10-10")','(date "2026-10-12")').replace('(rev "R122 - ENGINEERING / NO FAB")','(rev "R137 - ENGINEERING / NO FAB")')
        assert new!=item;root_edits.append(dict(kind='title_block',before=item,after=new));after=after[:a]+new+after[z:]
assert len(root_edits)==2
pad_edits=[]
for a,z,fp in children(after):
    if not fp.startswith('(footprint ')or '(property "Reference" "R67"'not in fp:continue
    assert '(attr smd dnp)'in fp
    for x,y,pad in reversed(list(children(fp))):
        if not pad.startswith('(pad '):continue
        assert pad.count('"F.Paste"')==1
        new=pad.replace(' "F.Paste"','')
        assert new!=pad
        pad_edits.append(dict(uuid=re.search(r'\(uuid "([^"]+)"\)',pad)[1],ref='R67',before=pad,after=new,
            change='Only F.Paste removed from default-DNP R67; F.Cu/F.Mask, hole, size, position, net and all other pad fields retained'))
        after=after[:a+x]+new+after[a+y:]
assert len(pad_edits)==2
old_library='R_RC0603_YAGEO_REFLOW';new_library=old_library+'_DNP_NO_PASTE'
for a,z,fp in children(after):
    if not fp.startswith('(footprint ')or '(property "Reference" "R67"'not in fp:continue
    old_id='(footprint "ENKU:'+old_library+'"';new_id='(footprint "ENKU:'+new_library+'"'
    assert fp.startswith(old_id);after=after[:a]+fp.replace(old_id,new_id,1)+after[z:]
    root_edits.append(dict(kind='R67_footprint_id',before=old_id,after=new_id));break
else:raise AssertionError('R67 not found')
sheet=r/'connectors.kicad_sch';sheet_before=sheet.read_text();a,z,symbol=instance(sheet_before,'R67')
sheet_after=sheet_before[:a]+prop(symbol,'Footprint','ENKU:'+new_library)+sheet_before[z:]
sheet.write_text(sheet_after)
library=r/'ENKU.pretty'/(old_library+'.kicad_mod');original_library=library.read_text()
new_text=original_library.replace('"'+old_library+'"','"'+new_library+'"').replace(' "F.Paste"','').replace('(thickness 0.12)','(thickness 0.15)')
new_file=r/'ENKU.pretty'/(new_library+'.kicad_mod');new_file.write_text(new_text)
pcb.write_text(after)
manifest=dict(revision='R137',source_revision='R136',source_pcb_before_sha256=hashlib.sha256(before.encode()).hexdigest(),
    source_pcb_after_sha256=hashlib.sha256(after.encode()).hexdigest(),minimum_visible_stroke_mm=.15,
    minimum_visible_text_height_mm=.8,only_silkscreen_strokes_four_missing_enabled_plot_layers_NO_FAB_title_and_two_DNP_paste_exclusions=True,
    enabled_mask_paste_layer_ids=[1,3,13,15],position_text_visibility_and_every_electrical_feature_unchanged=True,
    edits=rows,root_edits=root_edits,DNP_paste_edits=pad_edits,
    schematic_edits=[dict(path='hardware/mainboard/kicad/connectors.kicad_sch',before=symbol,after=prop(symbol,'Footprint','ENKU:'+new_library),before_sha256=hashlib.sha256(sheet_before.encode()).hexdigest(),after_sha256=hashlib.sha256(sheet_after.encode()).hexdigest())],
    new_DNP_library=dict(path='hardware/mainboard/kicad/ENKU.pretty/'+new_file.name,sha256=hashlib.sha256(new_text.encode()).hexdigest(),derived_from='hardware/mainboard/kicad/ENKU.pretty/'+library.name,original_sha256=hashlib.sha256(original_library.encode()).hexdigest(),only_name_paste_and_reference_stroke_changed=True),
    fabrication_ready=False)
(c/'silkscreen_change_manifest_R137.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Applied72 finite visible silk strokes; no source geometry changed; SHA',manifest['source_pcb_after_sha256'])
