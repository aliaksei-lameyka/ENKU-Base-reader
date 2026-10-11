"""Apply the declared U1 EP/mask/paste revision to immutable accepted R127.

Do not rerun on a later working board. No routing, holes, placement, rules or
exclusions are changed. Assembly process acceptance remains false.
"""
import hashlib, json, re, sys
from pathlib import Path
import pcbnew as p

r = Path(sys.argv[1]).resolve()
before = Path(sys.argv[2]).resolve()
c = r / 'checks'
filename = 'enku-mainboard-r0.1.kicad_pcb'
source_sha = 'c2316fa909debdd69577cd565b04bab6e40db01acbfc9c2b6f1362ac4b14b1f2'
assert hashlib.sha256((before / filename).read_bytes()).hexdigest() == source_sha
assert hashlib.sha256((r / filename).read_bytes()).hexdigest() == source_sha
b = p.LoadBoard(str(r / filename))
f = next(x for x in b.GetFootprints() if x.GetReference() == 'U1')
assert f.GetValue() == 'ESP32-S3-WROOM-1-N16R8'
assert [p.ToMM(f.GetPosition().x), p.ToMM(f.GetPosition().y)] == [33, 45]
assert f.GetOrientationDegrees() == 90

def xy(v): return [p.ToMM(v.x), p.ToMM(v.y)]
def vec(x, y): return p.VECTOR2I(p.FromMM(x), p.FromMM(y))
def layer_set(ids):
    result = p.LSET()
    for layer in ids: result.AddLayer(layer)
    return result
def state(a):
    return {'uuid': a.m_Uuid.AsString(), 'number': a.GetNumber(), 'net': a.GetNetname(),
            'position_mm': xy(a.GetPosition()), 'size_mm': xy(a.GetSize()),
            'drill_mm': xy(a.GetDrillSize()), 'angle_deg': a.GetOrientationDegrees(),
            'shape': a.GetShape(), 'attribute': a.GetAttribute(),
            'layers': [b.GetLayerName(x) for x in a.GetLayerSet().Seq()],
            'mask_margin_IU': a.GetLocalSolderMaskMargin(),
            'paste_margin_IU': a.GetLocalSolderPasteMargin(),
            'paste_ratio': a.GetLocalSolderPasteMarginRatio()}

old = {a.m_Uuid.AsString(): state(a) for a in f.Pads()}
paste = [a for a in f.Pads() if not a.GetNumber() and a.GetLayerSet().Contains(p.F_Paste)]
thermal = [a for a in f.Pads() if a.GetNumber() == '41' and a.GetAttribute() == p.PAD_ATTRIB_PTH]
solid = [a for a in f.Pads() if a.GetNumber() == '41' and a.GetAttribute() == p.PAD_ATTRIB_SMD]
assert len(paste) == 9 and len(thermal) == 12 and len(solid) == 1
ep = solid[0]
assert xy(ep.GetPosition()) == [35.46, 46.5] and xy(ep.GetSize()) == [3.9, 3.9]
grid = {(x, y) for x in [34.06, 35.46, 36.86] for y in [45.1, 46.5, 47.9]}
assert {tuple(xy(a.GetPosition())) for a in paste} == grid

# Nine separately masked exposed lands match Figure11-1's nominal copper grid.
# The existing central pad keeps its original GND net and UUID.
ep.SetSize(vec(.9, .9))
ep.SetLocalSolderMaskMargin(p.FromMM(-.05))
ep.SetLayerSet(layer_set([p.F_Cu, p.F_Mask]))
added = []
for x, y in sorted(grid - {(35.46, 46.5)}):
    a = p.PAD(f)
    a.SetNumber('41')
    a.SetNet(ep.GetNet())
    a.SetAttribute(p.PAD_ATTRIB_SMD)
    a.SetShape(p.PAD_SHAPE_RECT)
    a.SetPosition(vec(x, y))
    a.SetSize(vec(.9, .9))
    a.SetLayerSet(layer_set([p.F_Cu, p.F_Mask]))
    a.SetLocalSolderMaskMargin(p.FromMM(-.05))
    f.Add(a)
    added.append(a.m_Uuid.AsString())

# Existing paste-only UUIDs/centres survive; nominal aperture .8 x .8 provides
# .15mm paste-edge-to-drill spacing (previously .10mm). These are an engineering
# stencil proposal, not an Espressif-specified or assembler-approved stencil.
for a in paste:
    a.SetSize(vec(.8, .8))
    a.SetLocalSolderPasteMargin(0)
    a.SetLocalSolderPasteMarginRatio(0.0)

# Request mask tenting on both sides of the existing .3mm PTHs. No holes,
# annuli or coordinates change, and no filled/plugged/capped process is implied.
for a in thermal:
    assert xy(a.GetDrillSize()) == [.3, .3] and xy(a.GetSize()) == [.6, .6]
    a.SetLayerSet(p.LSET.AllCuMask())

name = 'ESP32_S3_WROOM_1_N16R8_EP_GRID_03_TENT_REQUEST'
lib = 'ENKU:' + name
fields = {
    'Footprint': lib,
    'Manufacturer': 'Espressif',
    'MPN': 'ESP32-S3-WROOM-1-N16R8',
    'EP Process': '9x0.9mm GND lands;9x0.8mm mask/paste;12x0.3mm PTH both-side tent request;assembly acceptance pending',
    'Module Ambient': '-40..65C by default;85C requires qualified PSRAM ECC firmware and1/16 capacity reduction',
}
f.SetFPID(p.LIB_ID('ENKU', name))
f.SetLibDescription('R128 Espressif v1.8 p45 Fig11-1 nominal EP grid;0.3mm original vias and0.8mm stencil are unqualified process adaptations')
for key, value in fields.items():
    if key == 'Footprint': continue
    existed = f.HasField(key)
    f.SetField(key, value)
    field = f.GetField(key)
    if not existed:
        field.SetLayer(p.F_Fab)
        field.SetPosition(f.GetPosition())
        field.SetTextSize(vec(.8, .8))
        field.SetVisible(False)

p.SaveBoard(str(r / filename), b)
clone = p.FOOTPRINT(f)
clone.SetOrientationDegrees(0)
clone.SetPosition(vec(0, 0))
clone.SetReference('REF**')
clone.SetPath(p.KIID_PATH())
for a in clone.Pads(): a.SetNetCode(0)
p.FootprintSave(str(r / 'ENKU.pretty'), clone)

def block(text, start):
    depth, quote, escaped = 0, False, False
    for i in range(start, len(text)):
        char = text[i]
        if quote:
            if escaped: escaped = False
            elif char == '\\': escaped = True
            elif char == '"': quote = False
        elif char == '"': quote = True
        elif char == '(': depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0: return text[start:i + 1], i + 1
    raise ValueError('Unbalanced symbol')

def prop(text, key, value):
    text, n = re.subn(r'(\(property "' + re.escape(key) + r'" )"(?:\\.|[^"\\])*"',
                      lambda m: m[1] + json.dumps(value), text, count=1)
    if not n:
        text = text[:-1] + '\n\t\t(property ' + json.dumps(key) + ' ' + json.dumps(value) + ' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
    return text

sheet = r / 'mcu_io.kicad_sch'
text = sheet.read_text()
pos = text.index('(property "Reference" "U1"')
start = text.rfind('(symbol (lib_id', 0, pos)
assert start >= 0
symbol, end = block(text, start)
for key, value in fields.items(): symbol = prop(symbol, key, value)
sheet.write_text(text[:start] + symbol + text[end:])

new = {a.m_Uuid.AsString(): state(a) for a in f.Pads()}
changed = [dict(uuid=u, before=x, after=new[u]) for u, x in old.items() if x != new[u]]
assert len(changed) == 22
assert len(added) == 8
unchanged = [
    'enku-mainboard-r0.1.kicad_pro', 'enku-mainboard-r0.1.kicad_dru',
    'ENKU.kicad_sym', 'fp-lib-table', 'sym-lib-table',
    'epd_hv.kicad_sch', 'power.kicad_sch', 'connectors.kicad_sch',
] + [str(x.relative_to(before)) for x in (before / 'ENKU.pretty').glob('*.kicad_mod')] + [str(x.relative_to(before)) for x in (before / 'standard-footprints').rglob('*.kicad_mod')]
recipe = {
    'revision': 'R128', 'predecessor_R127_pcb_sha256': source_sha,
    'U1_footprint_library': lib, 'changed_original_pads': changed,
    'added_EP_pads': [new[u] for u in added], 'schematic_U1_fields': fields,
    'unchanged_files': {rel: hashlib.sha256((before / rel).read_bytes()).hexdigest() for rel in unchanged},
    'no_footprint_placement_changes': True, 'no_track_or_via_changes': True,
    'no_USB_or_button_hole_or_land_changes': True, 'fabrication_ready': False,
}
(c / 'applied_U1_EP_grid_R128.json').write_text(json.dumps(recipe, indent=2) + '\n')
print(json.dumps({'changed_original_pads': len(changed), 'added_EP_pads': len(added), 'original_pad_UUIDs_preserved': 417, 'total_pads': 425, 'routing_changed': False, 'fabrication_ready': False}))
