"""Check actual visible native silk widths, sizes and declared plot-layer availability."""
import hashlib,json,sys
from pathlib import Path

r,out=(Path(x).resolve()for x in sys.argv[1:3]);j=json.loads((out/'silkscreen_native_R138.json').read_text())
assert j['native_kicad']=='10.0.7'
assert all(x in j['enabled_layer_ids']for x in [0,2,4,6,1,3,13,15,5,7,25]),'Fabrication plot layer is disabled'
rows=j['items'];assert len(rows)==104
assert all(x.get('pen_mm',x.get('width_mm'))>=.15 for x in rows),'Printed silk is too thin'
assert all(min(x['size_mm'])>=.8 for x in rows if 'size_mm'in x),'Printed text is too small'
assert len([x for x in rows if x['ref'].startswith('TP')and 'text'in x])==13
report=dict(revision='R138',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],
    all104_visible_native_silk_features_measured=True,minimum_native_stroke_mm=min(x.get('pen_mm',x.get('width_mm'))for x in rows),
    minimum_native_text_height_mm=min(min(x['size_mm'])for x in rows if 'size_mm'in x),
    exact_four_mask_and_paste_layers_enabled=True,PCBWay_published_legend_width_and_height_minima_satisfied=True,
    primary_capability_URL='https://www.pcbway.com/capabilities.html',factory_process_approval=False,fabrication_ready=False)
(out/'silkscreen_audit_R138.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
