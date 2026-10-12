"""Finite, SHA-pinned C9 metadata replacement; no geometry or wiring edits."""
import hashlib, json, sys
from pathlib import Path
from cad_text_R134 import children, instance, prop

root = Path(sys.argv[1]).resolve()
pcb = root / 'enku-mainboard-r0.1.kicad_pcb'
assert hashlib.sha256(pcb.read_bytes()).hexdigest() == '9c5101ce9b748e19be893f5cc75de55afe5ff6eb01c257cc48fc48c850bcf7df'
fields = {
    'Value': '22uF 10V',
    'MPN': 'CC0805MKX5R6BB226',
    'Datasheet': 'https://yageogroup.com/download/specsheet/CC0805MKX5R6BB226',
    'Description': 'R136 TPS63802 input 22uF; modeled DC-bias margin; max height1.45mm; Ceff/fit qualification pending',
}
text = pcb.read_text()
found = []
for start, end, part in children(text):
    if part.startswith('(footprint ') and '(property "Reference" "C9"' in part:
        assert '(property "MPN" "CC0805KKX5R6BB106"' in part
        for key, value in fields.items():
            part = prop(part, key, value)
        found.append((start, end, part))
assert len(found) == 1
start, end, part = found[0]
pcb.write_text(text[:start] + part + text[end:])
sheet = root / 'power.kicad_sch'
text = sheet.read_text()
start, end, part = instance(text, 'C9')
assert '(property "MPN" "CC0805KKX5R6BB106"' in part
for key, value in fields.items():
    part = prop(part, key, value)
sheet.write_text(text[:start] + part + text[end:])
print('Applied C9 10uF -> 22uF, same copper/lands/net/XY; component height0.95 ->1.45mm max; case fit HOLD')
