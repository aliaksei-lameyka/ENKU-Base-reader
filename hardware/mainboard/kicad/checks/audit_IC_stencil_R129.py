"""Inspect real native BQ/TPS paste and mask, including union/coverage/gaps."""
import hashlib,json,math,sys
from pathlib import Path
from shapely.geometry import Point,box
from shapely.ops import unary_union
from native_svg_shapes_R129 import actual_shapes
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());ox,oy=g['bbox'][:2]
def rounded(x,y,w,h,rad):return box(x-w/2+rad,y-h/2+rad,x+w/2-rad,y+h/2-rad).buffer(rad,resolution=128)
rois={'U3':box(48-ox,90.2-oy,49-ox,91.8-oy),'U4':box(57.85-ox,90.85-oy,59.25-ox,91.15-oy)}
targets={
 ('U3','F_Mask'):[rounded(48.5-ox,91-oy,.9,1.5,.05)],
 ('U3','F_Paste'):[rounded(48.5-ox,91-oy,.85,1.38,.05)],
 ('U4','F_Mask'):[box(57.9-ox,90.875-oy,59.2-ox,91.125-oy)],
 ('U4','F_Paste'):[rounded(x-ox,91-oy,.55,.25,.05) for x in [58.175,58.925]],
}
results={};hashes={}
for (ref,layer),targets_here in targets.items():
    file=out/(f'{layer}.svg' if server else f'native_{layer}_R129.svg')
    shapes=actual_shapes(file,rois[ref]);actual=unary_union(shapes);target=unary_union(targets_here)
    assert len(shapes)==len(targets_here),(ref,layer,'Overlapping/extra/unseparated aperture',len(shapes))
    # Native SVG roundrects use chord approximations; exact radius is also
    # checked independently through pcbnew assembly features.
    assert actual.symmetric_difference(target).area<.0005,(ref,layer,'Wrong native aperture',actual.area)
    assert actual.hausdorff_distance(target)<.0011,(ref,layer,'Wrong rounded boundary')
    assert all(abs(a-z)<1e-5 for a,z in zip(actual.bounds,target.bounds))
    results[ref+'_'+layer]=dict(opening_count=len(shapes),opening_area_mm2=actual.area,
                              bounds_mm=[round(a+([ox,oy,ox,oy][i]),6) for i,a in enumerate(actual.bounds)])
    if ref=='U4' and layer=='F_Paste':
        assert abs(shapes[0].distance(shapes[1])-.2)<1e-5
        assert not actual.contains(Point(58.55-ox,91-oy)),'Full GND paste rectangle still present'
    hashes[layer]=hashlib.sha256(file.read_bytes()).hexdigest()
coverage={ref:100*results[ref+'_F_Paste']['opening_area_mm2']/results[ref+'_F_Mask']['opening_area_mm2'] for ref in rois}
assert 86.7<coverage['U3']<87.0 and 83.1<coverage['U4']<83.4
baseline=c/'native_F_Paste_R128.svg'
old_U4=unary_union(actual_shapes(baseline,rois['U4']))
assert old_U4.symmetric_difference(targets[('U4','F_Mask')][0]).area<1e-8
assert old_U4.contains(Point(58.55-ox,91-oy)),'Accepted baseline did not have the stated full-paste defect'
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R129',pcb_sha256=sha,actual_native_IC_mask_and_stencil_apertures_verified=True,
            U4_full_GND_paste_rectangle_absent=True,U4_two_R005_apertures_gap_mm=.2,
            actual_accepted_R128_U4_full_paste_defect_confirmed=True,
            accepted_R128_paste_plot_sha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),
            U3_TI_nominal_EP_and_stencil_R005_verified=True,apertures=results,
            geometric_paste_coverage_percent=coverage,actual_plot_sha256=hashes,
            native_plot_origin_mm=[ox,oy],printed_solder_volume_transfer_voiding_and_reflow_qualified=False,
            stencil_thickness_assumption_mm={'U3_TI_example':.125,'U4_TI_example':.1},
            common_board_stencil_process_accepted=False,fabrication_ready=False)
(out/('IC_stencil_audit.json' if server else 'IC_stencil_audit_R129.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
