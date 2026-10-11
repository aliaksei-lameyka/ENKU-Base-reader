"""One-time R129 edits from the immutable accepted R128 source.

Canonical pad angles, mounting classifications, real IC stencil corrections,
and J7 pin-1 graphics. No tracks, vias, drills, placements or rules are edited.
Project bare-PCB definitions do not assert any manufactured assembly fit.
"""
import hashlib, json, re, sys, gzip
from pathlib import Path
import pcbnew as p

r = Path(sys.argv[1]).resolve(); before = Path(sys.argv[2]).resolve(); c = r / 'checks'
filename = 'enku-mainboard-r0.1.kicad_pcb'
source_sha = 'f53da6653e1f98241a4da7e337aa001a2b8614fa1b3e0685d893d299a18d5fa6'
assert hashlib.sha256((before / filename).read_bytes()).hexdigest() == source_sha
assert hashlib.sha256((r / filename).read_bytes()).hexdigest() == source_sha
b = p.LoadBoard(str(r / filename)); fps = {f.GetReference(): f for f in b.GetFootprints()}
def xy(v): return [p.ToMM(v.x), p.ToMM(v.y)]
def vec(x, y): return p.VECTOR2I(p.FromMM(x), p.FromMM(y))
def state(a):
    return dict(uuid=a.m_Uuid.AsString(), ref=a.GetParentFootprint().GetReference(), number=a.GetNumber(),
                net=a.GetNetname(), pos=xy(a.GetPosition()), size=xy(a.GetSize()),
                drill=xy(a.GetDrillSize()), angle=a.GetOrientationDegrees(), shape=a.GetShape(),
                attribute=a.GetAttribute(), layers=list(a.GetLayerSet().Seq()),
                roundrect_radius_mm=p.ToMM(a.GetRoundRectCornerRadius()),
                mask=a.GetLocalSolderMaskMargin(), paste=a.GetLocalSolderPasteMargin(),
                paste_ratio=a.GetLocalSolderPasteMarginRatio())
old = {a.m_Uuid.AsString(): state(a) for f in fps.values() for a in f.Pads()}
old_attrs = {ref: f.GetAttributes() for ref, f in fps.items()}
fields = {}; lib_changes = {}; attr_changes = {}; labels = []
def set_fields(ref, values):
    f = fps[ref]; fields.setdefault(ref, {}).update(values)
    for key, value in values.items():
        if key == 'Footprint': continue
        exists = f.HasField(key); f.SetField(key, value); a = f.GetField(key)
        if not exists:
            a.SetLayer(p.B_Fab if f.IsFlipped() else p.F_Fab)
            a.SetPosition(f.GetPosition()); a.SetTextSize(vec(.8, .8)); a.SetVisible(False)
def save_variant(ref, name, description):
    f = fps[ref]; f.SetFPID(p.LIB_ID('ENKU', name)); f.SetLibDescription(description)
    lib_changes[ref] = 'ENKU:' + name
    fields.setdefault(ref, {})['Footprint'] = 'ENKU:' + name
    clone = p.FOOTPRINT(f)
    clone.SetOrientationDegrees(0)
    if clone.IsFlipped(): clone.Flip(clone.GetPosition(), False)
    clone.SetPosition(vec(0, 0)); clone.SetReference('REF**'); clone.SetPath(p.KIID_PATH())
    for a in clone.Pads(): a.SetNetCode(0)
    if clone.HasField('Probe Label'): clone.SetField('Probe Label', 'NET')
    p.FootprintSave(str(r / 'ENKU.pretty'), clone)

# Unspecified mount type previously omitted these six parts and J5 from an SMD-only CPL.
for ref in ['U1', 'Q1', 'J2', 'U3', 'U4', 'U5', 'J3', 'J5', 'L1', 'L2']:
    assert fps[ref].GetAttributes() == 0
    fps[ref].SetAttributes(p.FP_SMD)

# The first three references also lacked SMD in the local library itself, so
# DRC equality had hidden their omission from the real SMD-only position file.
library_mount_type_edits = {}
for ref in ['U1', 'Q1', 'J2']:
    name = str(fps[ref].GetFPID().GetLibItemName())
    rel = 'ENKU.pretty/' + name + '.kicad_mod'; file = r / rel
    text = file.read_text(); original = text
    assert not re.search(r'\(attr\s', text), ref
    text = text.replace('(layer "F.Cu")', '(layer "F.Cu")\n\t(attr smd)', 1)
    assert text != original
    file.write_text(text)
    (c / ('source_R128_' + name + '.kicad_mod.gz')).write_bytes(gzip.compress(original.encode(), mtime=0))
    library_mount_type_edits[rel] = dict(before_sha256=hashlib.sha256(original.encode()).hexdigest(),
                                       after_sha256=hashlib.sha256(text.encode()).hexdigest())

# Equivalent symmetric pad poses are canonicalized to the library orientation.
# Actual copper equality is checked independently after native polygon export.
for ref in ['U3', 'U8']:
    for a in fps[ref].Pads(): a.SetOrientation(fps[ref].GetOrientation())

# TI DLH0010A: EP 0.9x1.5 R0.05; stencil 0.85x1.38 R0.05 (drawing4226298/A).
u3 = fps['U3']; ep = next(a for a in u3.Pads() if a.GetNumber() == '11')
ep.SetShape(p.PAD_SHAPE_ROUNDRECT); ep.SetRoundRectRadiusRatio(.05 / .9)
paste = next(a for a in u3.Pads() if not a.GetNumber())
assert list(paste.GetLayerSet().Seq()) == [p.F_Paste]
paste.SetSize(vec(.85, 1.38)); paste.SetRoundRectRadiusRatio(.05 / .85)
save_variant('U3', 'BQ25185_DLH0010A_TI_STENCIL',
             'R129 TI4226298/A nominal copper and stencil; assembly thickness, transfer and reflow unqualified')

# TI DLA0010A split GND stencil was defeated by pad8's additional full paste layer.
u4 = fps['U4']; ground = next(a for a in u4.Pads() if a.GetNumber() == '8')
layers = ground.GetLayerSet(); assert layers.Contains(p.F_Paste); layers.RemoveLayer(p.F_Paste)
ground.SetLayerSet(layers)
graphics = [a for a in u4.GraphicalItems() if a.GetLayer() == p.F_Paste]
assert len(graphics) == 2
removed_paste_graphics = [a.m_Uuid.AsString() for a in graphics]
for a in graphics: u4.Remove(a)
added = []
for x in [58.175, 58.925]:
    a = p.PAD(u4); a.SetNumber(''); a.SetAttribute(p.PAD_ATTRIB_SMD)
    a.SetShape(p.PAD_SHAPE_ROUNDRECT); a.SetSize(vec(.55, .25))
    a.SetRoundRectRadiusRatio(.05 / .25); a.SetPosition(vec(x, 91))
    layer = p.LSET(); layer.AddLayer(p.F_Paste); a.SetLayerSet(layer); u4.Add(a)
    added.append(a.m_Uuid.AsString())
save_variant('U4', 'TPS63802_DLA0010A_SPLIT_PASTE',
             'R129 TI4223750/D: no full pad8 paste; two0.55x0.25 R0.05 apertures,0.2 gap; assembly unqualified')

# Bare-PCB service pads have no purchased body and must never enter the assembly list.
for ref in sorted(fps):
    if not ref.startswith('TP'): continue
    f = fps[ref]; assert f.GetAttributes() == 0
    f.SetAttributes(p.FP_EXCLUDE_FROM_BOM | p.FP_EXCLUDE_FROM_POS_FILES)
    texts = [a for a in f.GraphicalItems() if isinstance(a, p.PCB_TEXT)]
    assert len(texts) == 1; t = texts[0]
    set_fields(ref, {'Assembly': 'BARE_PCB', 'Probe Label': t.GetText()})
    a = f.GetField('Probe Label'); a.SetLayer(t.GetLayer()); a.SetPosition(t.GetPosition())
    a.SetTextSize(t.GetTextSize()); a.SetTextThickness(t.GetTextThickness())
    a.SetTextAngle(t.GetTextAngle()); a.SetMirrored(t.IsMirrored()); a.SetVisible(True)
    labels.append(dict(ref=ref, text=t.GetText(), position_mm=xy(t.GetPosition()),
                       layer=t.GetLayer(), size_mm=xy(t.GetTextSize()), mirrored=t.IsMirrored()))
    f.Remove(t)
save_variant('TP1', 'SERVICE_PAD_D1_5_NO_PASTE',
             'ENKU bare-PCB1.5mm probe land with2mm silk ring; no paste/BOM/CPL; Probe Label is instance-specific')
for ref in fps:
    if ref.startswith('TP') and ref != 'TP1':
        fps[ref].SetFPID(p.LIB_ID('ENKU', 'SERVICE_PAD_D1_5_NO_PASTE'))
        lib_changes[ref] = 'ENKU:SERVICE_PAD_D1_5_NO_PASTE'
        fields[ref]['Footprint'] = lib_changes[ref]

# The four mounting holes are board-only, unlike the schematic-backed library default.
save_variant('H1', 'MOUNT_HOLE_D2_2_BOARD_ONLY',
             'ENKU2.2mm NPTH at existing mechanical datum;4mm courtyard; board-only, no BOM/CPL; enclosure unqualified')
for ref in ['H2', 'H3', 'H4']:
    fps[ref].SetFPID(p.LIB_ID('ENKU', 'MOUNT_HOLE_D2_2_BOARD_ONLY'))
    lib_changes[ref] = 'ENKU:MOUNT_HOLE_D2_2_BOARD_ONLY'

# J5's symbol intentionally uses S, rather than the stock footprint's SH, for all shields.
save_variant('J5', 'USB4105_EXISTING_LANDS_SHIELD_S',
             'ENKU USB4105 existing16 contacts and four shieldS lands; nominal drawing review retained; hole/process/3D not qualified')

# J7 pin1 marker was beside actual pad2. Mirror only the two marker lines about y=87.
j7 = fps['J7']; marks = [a for a in j7.GraphicalItems() if a.GetLayer() == p.B_SilkS]
assert len(marks) == 2
for a in marks:
    for getter, setter in [(a.GetStart, a.SetStart), (a.GetEnd, a.SetEnd)]:
        x, y = xy(getter()); setter(vec(x, 174 - y))
for a in j7.Pads():
    if a.GetNumber(): a.SetAttribute(p.PAD_ATTRIB_CONN)
set_fields('J7', {'Assembly': 'BARE_PCB', 'Datasheet':
    'https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/2019/12/TC2030-IDC-NL-Datasheet-Rev-B.pdf'})
save_variant('J7', 'TC2030_NL_CONTACTS_PIN1',
             'TC2030-IDC-NL RevB bare PCB contacts: pin1 silk corrected; no paste/BOM/CPL; existing keepout and holes retained')

parts = {
 'U3': ('Texas Instruments', 'BQ25185DLHR', 'https://www.ti.com/lit/ds/symlink/bq25185.pdf'),
 'U4': ('Texas Instruments', 'TPS63802DLAR', 'https://www.ti.com/lit/ds/symlink/tps63802.pdf'),
 'U5': ('Bosch Sensortec', 'BMI270', 'https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf'),
 'U8': ('STMicroelectronics', 'USBLC6-2SC6', 'https://www.st.com/resource/en/datasheet/usblc6-2.pdf'),
 'U9': ('Texas Instruments', 'TMUX1101DBVR', 'https://www.ti.com/lit/ds/symlink/tmux1101.pdf'),
 'U10': ('Texas Instruments', 'TLV3012BIDBVR', 'https://www.ti.com/lit/ds/symlink/tlv3012b.pdf'),
 'J3': ('Hirose', 'FH34SRJ-24S-0.5SH(50)', 'https://www.hirose.com/product/en/products/FH34/FH34SRJ-24S-0.5SH%2850%29/'),
}
for ref, (maker, mpn, url) in parts.items():
    set_fields(ref, {'Manufacturer': maker, 'MPN': mpn, 'Datasheet': url, 'Assembly': 'FIT'})
set_fields('U3', {'Charge Profile': '4.2V/500mA input/300mA fast charge;RevB timer360min;battery NTC and capacity qualification pending'})

def block(text, start):
    depth = 0; quote = escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if quote:
            if escaped: escaped = False
            elif ch == '\\': escaped = True
            elif ch == '"': quote = False
        elif ch == '"': quote = True
        elif ch == '(': depth += 1
        elif ch == ')':
            depth -= 1
            if not depth: return text[start:i+1], i+1
    raise ValueError('Unbalanced symbol')
def prop(text, key, value):
    text, n = re.subn(r'(\(property "' + re.escape(key) + r'" )"(?:\\.|[^"\\])*"',
                     lambda m: m[1] + json.dumps(value), text, count=1)
    if not n:
        text = text[:-1] + '\n\t\t(property ' + json.dumps(key) + ' ' + json.dumps(value) + ' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
    return text
sheet_edits = {}; excluded = {ref for ref in fps if ref.startswith('TP')} | {'J7'}
for sheet in r.glob('*.kicad_sch'):
    text = sheet.read_text(); original = text; edits = {}
    for ref, values in fields.items():
        marker = '(property "Reference" "' + ref + '"'
        if marker not in text: continue
        pos = text.index(marker); start = text.rfind('(symbol (lib_id', 0, pos)
        assert start >= 0, ref
        symbol, end = block(text, start)
        for key, value in values.items(): symbol = prop(symbol, key, value)
        if ref in excluded:
            symbol, n = re.subn(r'\(in_bom yes\)', '(in_bom no)', symbol, count=1)
            assert n == 1 or '(in_bom no)' in symbol, ref
        text = text[:start] + symbol + text[end:]; edits[ref] = dict(fields=values, in_bom=False if ref in excluded else None)
    if text != original:
        (c / ('source_R128_' + sheet.name + '.gz')).write_bytes(gzip.compress(original.encode(), mtime=0))
        sheet.write_text(text); sheet_edits[sheet.name] = edits

p.SaveBoard(str(r / filename), b)
new = {a.m_Uuid.AsString(): state(a) for f in fps.values() for a in f.Pads()}
changed = [dict(uuid=u, before=x, after=new[u]) for u, x in old.items() if x != new[u]]
attr_changes = {ref: dict(before=old_attrs[ref], after=f.GetAttributes()) for ref,f in fps.items() if old_attrs[ref] != f.GetAttributes()}
unchanged = ['enku-mainboard-r0.1.kicad_pro', 'enku-mainboard-r0.1.kicad_dru',
             'ENKU.kicad_sym', 'fp-lib-table', 'sym-lib-table']
unchanged += [str(x.relative_to(before)) for x in before.glob('*.kicad_sch') if x.name not in sheet_edits]
unchanged += [str(x.relative_to(before)) for d in ['ENKU.pretty','standard-footprints'] for x in (before/d).rglob('*.kicad_mod') if str(x.relative_to(before)) not in library_mount_type_edits]
plan = dict(revision='R129', predecessor_R128_pcb_sha256=source_sha,
            changed_original_pads=changed, added_paste_pads=[new[u] for u in added],
            removed_U4_paste_graphics=removed_paste_graphics,
            footprint_attribute_changes=attr_changes, footprint_library_changes=lib_changes,
            library_mount_type_edits=library_mount_type_edits,
            schematic_edits=sheet_edits, native_board_fields=fields, preserved_probe_labels=labels,
            unchanged_files={rel:hashlib.sha256((before/rel).read_bytes()).hexdigest() for rel in unchanged},
            only_original_U3_EP_corner_copper_changed=True, no_track_via_hole_or_placement_changes=True,
            fabrication_ready=False)
(c/'applied_active_assembly_R129.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps(dict(changed_original_pads=len(changed), added_paste_pads=len(added),
                      footprint_attribute_changes=len(attr_changes), excluded_service_points=len(excluded),
                      original_pad_UUIDs_preserved=len(old), fabrication_ready=False),indent=2))
