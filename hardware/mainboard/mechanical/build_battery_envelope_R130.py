"""Dimensioned engineering studies from actual R130 native coordinates.

Needs cadquery, matplotlib and shapely. No exact enclosure/panel assembly was
provided by the accepted engineering tree. Every assumed wall/boss/margin is
recorded; these studies cannot establish a manufactured maximum battery fit.
"""
import gzip,hashlib,json,re
from pathlib import Path
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Polygon as PatchPolygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import box,Point,Polygon
from shapely.ops import unary_union

here=Path(__file__).resolve().parent;k=here.parent/'kicad';c=k/'checks'
g=json.loads(gzip.decompress((c/'geometry_checkpoint_R130.json.gz').read_bytes()))
pcb_sha=hashlib.sha256((k/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
pcb_t=float(re.search(r'\(thickness ([^)]+)\)',(k/'enku-mainboard-r0.1.kicad_pcb').read_text())[1]);assert pcb_t==1.6
assert g['bbox']==[18,20,77,121]
rf=next(z for z in g['zones'] if z['rule'] and z['no_pads'] and z['layers']==[0,2,4,6]);rf_shape=unary_union([Polygon(q) for q in rf['polygons']])
holes={a['ref']:a['pos'] for a in g['pads'] if a['ref'] in ['H1','H2','H3','H4']}
boss_radius=2.5;clearance=.5;x0=rf_shape.bounds[2]+clearance;y0=holes['H2'][1]+boss_radius+clearance
conditional_wmax=77-clearance-x0;conditional_lmax=holes['H4'][1]-boss_radius-clearance-y0
packs=[dict(name='Koosay405381',capacity_mAh=2500,T=4.,W=53.,L=81.,envelope_basis='catalogue nominal cell, assembled maximum UNKNOWN'),
 dict(name='PolybatteryLP405079',capacity_mAh=2000,T=4.,W=50.,L=79.,envelope_basis='catalogue nominal cell, assembled maximum UNKNOWN'),
 dict(name='AkygaAKY0156',capacity_mAh=2500,T=5.2,W=51.,L=87.5,envelope_basis='manufacturer assembled maximum, excluding free leads and swelling')]
rows=[]
for q in packs:
 footprint=box(x0,y0,x0+q['W'],y0+q['L'])
 rows.append(dict(**q,trial_xy_mm=[x0,y0],RF_reserved_area_overlap_mm2=footprint.intersection(rf_shape).area,extension_beyond_board_minus_0_5mm_edge_margin_mm=max(0,q['W']-conditional_wmax),boss_clearance_violations=[ref for ref,xy in holes.items() if footprint.distance(Point(xy))<boss_radius+clearance],native_J1_envelope_XY_overlap_mm2=footprint.intersection(box(64.6,90.55,74.2,98.45)).area,real_case_fit_qualified=False))
assert conditional_wmax==49.75 and conditional_lmax==85.5 and all(z['RF_reserved_area_overlap_mm2']==0 for z in rows)
# Actual KiCad STEP contains2 solids: native PCB and conservative nominal PH2.
native_file=here/'native_board_PH2_R130.step';native=cq.importers.importStep(str(native_file)).val().mirror('XZ')
nb=native.BoundingBox();assert abs(nb.xmin-18)<1e-6 and abs(nb.ymin-20)<1e-6 and abs(nb.ymax-121)<1e-6
ph_top=nb.zmax;front_clearance=.5;front_display_t=.92;front_wall=1.;rear_wall=1.2;handling_margin=.5;insulation_gap=.3;sensor_t=.5
front_min=-(front_clearance+front_display_t+front_wall)
safe_pack_z=ph_top+insulation_gap+sensor_t
def brick(x,y,z,w,l,t):return cq.Workplane('XY').box(w,l,t,centered=False).translate((x,y,z)).val()
study=rows[1];pack=brick(x0,y0,safe_pack_z,study['W'],study['L'],study['T'])
# Sensor strip is a conservative51x4.1x0.5 envelope; no claimed exact lead routing.
sensor=brick(49,36,ph_top+insulation_gap,4.1,51,sensor_t)
asm=cq.Assembly(name='R130_conditional_study_not_manufactured_fit');asm.add(native,name='actual_native_PCB_PH2_only',color=cq.Color(.1,.5,.3));asm.add(pack,name='LP405079_nominal_cell_only_UNQUALIFIED',color=cq.Color(.1,.4,.9,.55));asm.add(sensor,name='103JT050_conservative_strip_UNQUALIFIED',color=cq.Color(.9,.6,.1));asm.save(str(here/'BAT_REV3_conditional_stack_R130.step'))
low_pack=brick(x0,y0,pcb_t+insulation_gap,study['W'],study['L'],study['T'])
low=cq.Assembly(name='R130_10mm_counterexample');low.add(native,name='actual_native_PCB_PH2_only');low.add(low_pack,name='battery_in_reserved_PH2_space_INTENTIONAL_OVERLAP');low.save(str(here/'BAT_REV3_10mm_collision_trial_R130.step'))
# Intersections are with the conservative reserved connector envelope, not exact polymer material.
ph=brick(64.6,90.55,ph_top-5.5,9.6,7.9,5.5)
collision=low_pack.intersect(ph).Volume();assert collision>300
case10_rear_inner=front_min+10-rear_wall
stack=[]
for q in packs:stack.append(dict(name=q['name'],pack_T_mm=q['T'],assumed_sensor_max_T_mm=sensor_t,conditional_total_case_T_mm=safe_pack_z+q['T']+handling_margin+rear_wall-front_min,qualified=False))
data=dict(revision='R130',source_pcb_sha256=pcb_sha,native_STEP_sha256=hashlib.sha256(native_file.read_bytes()).hexdigest(),native_KiCad_board_T_mm=pcb_t,native_board_thickness_is_not_manufacturer_approved_stackup=True,native_outline_mm=g['bbox'],source_RF_polygon_mm=rf['polygons'],hole_centers_mm=holes,scenario_assumptions=dict(boss_diameter_mm=5,plan_clearance_mm=.5,front_wall_mm=front_wall,rear_wall_mm=rear_wall,display_T_mm=front_display_t,display_and_FPC_geometry_confirmed=False,front_display_gap_mm=front_clearance,component_pack_insulation_gap_mm=insulation_gap,extra_handling_swelling_scenario_mm=handling_margin,swelling_scenario_is_not_vendor_guarantee=True),
 conditional_board_contained_RF_clear_Wmax_mm=conditional_wmax,conditional_boss_clear_Lmax_mm=conditional_lmax,actual_enclosure_allowable_T_W_L_mm=None,reason='No current registered enclosure/panel/FPC/boss drawing or full97-component3D assembly in accepted source',candidates=rows,conditional_full_overlay_stack_scenarios=stack,nominal_PH2_height_mm=5.5,native_PH2_top_Z_mm=ph_top,ten_mm_trial=dict(rear_inner_Z_mm=case10_rear_inner,low_battery_reserved_PH2_intersection_mm3=collision,pack_clearance_above_PH2_with_sensor_mm=case10_rear_inner-ph_top-insulation_gap-sensor_t,fit_passed=False),connector_choice='A: PH2 avoids extraPH3 breakout and daughterboard; not a manufactured-fit approval',real_NTC_attachment_lead_path_and_replacement_qualified=False,all_remaining_component_height_and_case_collisions_checked=False,mechanical_release_accepted=False,fabrication_ready=False)
(here/'BAT_REV3_mechanical_audit_R130.json').write_text(json.dumps(data,indent=2)+'\n')

fig=plt.figure(figsize=(14,11));ax=fig.add_subplot(121)
ax.add_patch(Rectangle((18,20),59,101,fill=False,color='#1c6448',lw=2,label='Native PCB59x101, T1.6'))
for p in g['pads']:
 for q in p['polygons'].get('0',[]):ax.add_patch(PatchPolygon(q,color='#aaaaaa',alpha=.35,lw=0))
for q in rf['polygons']:ax.add_patch(PatchPolygon(q,color='#e0a300',alpha=.25,hatch='//',label='RF metal keepout'))
colors=['#d65050','#367bd2','#8b50aa']
for row,col in zip(rows,colors):ax.add_patch(Rectangle((x0,y0),row['W'],row['L'],fill=False,color=col,lw=2,label=f"{row['name']}: {row['T']}x{row['W']}x{row['L']}"))
for ref,xy in holes.items():ax.add_patch(Circle(xy,boss_radius,fill=False,color='#333333',ls='--'));ax.text(xy[0],xy[1],ref,ha='center',va='center',fontsize=8)
ax.add_patch(Rectangle((64.6,90.55),9.6,7.9,facecolor='#d7aa57',alpha=.6));ax.text(69.4,94.5,'J1 PH-2',ha='center',fontsize=8)
ax.plot([66.95,64.8],[91.5,89.3],'ko',ms=4);ax.text(63.8,88,'J8 NTC',ha='right',fontsize=8)
ax.annotate('49.75mm conditional RF-clear width',xy=(26.75,120),xytext=(76.5,120),arrowprops=dict(arrowstyle='<->'),ha='right',fontsize=8)
ax.set_xlim(14,84);ax.set_ylim(126,17);ax.set_aspect('equal');ax.grid(alpha=.15);ax.set_xlabel('KiCad X / mm');ax.set_ylabel('KiCad Y / mm');ax.set_title('Native placement + candidate pouch plans\n5mm bosses and0.5mm margins are assumptions',fontsize=11);ax.legend(loc='upper center',bbox_to_anchor=(.52,-.04),fontsize=8)
ax3=fig.add_subplot(122,projection='3d')
def cuboid(x,y,z,w,l,t,color,alpha):
 v=[[x,y,z],[x+w,y,z],[x+w,y+l,z],[x,y+l,z],[x,y,z+t],[x+w,y,z+t],[x+w,y+l,z+t],[x,y+l,z+t]];faces=[[v[i] for i in ids] for ids in [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]];ax3.add_collection3d(Poly3DCollection(faces,facecolors=color,alpha=alpha,edgecolors=color,linewidths=.6))
cuboid(18,20,0,59,101,pcb_t,'#167a54',.35);cuboid(64.6,90.55,ph_top-5.5,9.6,7.9,5.5,'#b58031',.75);cuboid(x0,y0,safe_pack_z,50,79,4,'#2675c8',.3);cuboid(49,36,ph_top+insulation_gap,4.1,51,.5,'#e8a725',.7)
ax3.set_xlim(18,83);ax3.set_ylim(20,121);ax3.set_zlim(-2.5,14);ax3.set_box_aspect((65,101,24));ax3.view_init(elev=24,azim=-125);ax3.set_xlabel('X / mm');ax3.set_ylabel('Y / mm');ax3.set_zlabel('Z / mm');ax3.set_title('Conditional stack above PH-2\nOther component models and actual enclosure absent',fontsize=11)
fig.suptitle('ENKU R130 / BAT-REV3 — dimensional study, NO mechanical release',fontsize=15,y=.97)
fig.text(.56,.12,f"4mm nominal pack full-overlay scenario: {stack[1]['conditional_total_case_T_mm']:.2f}mm case\n5.2mm Akyga scenario: {stack[2]['conditional_total_case_T_mm']:.2f}mm case\n10mm trial overlaps the reserved PH-2 envelope: {collision:.1f}mm³\nReal maximum pack dimensions: UNKNOWN until enclosure + pack drawings.",fontsize=10)
fig.subplots_adjust(bottom=.2,top=.91,wspace=.1);fig.savefig(here/'BAT_REV3_dimensional_study_R130.png',dpi=160);plt.close(fig)
print(json.dumps({k:data[k] for k in ['native_KiCad_board_T_mm','conditional_board_contained_RF_clear_Wmax_mm','conditional_boss_clear_Lmax_mm','conditional_full_overlay_stack_scenarios','ten_mm_trial','mechanical_release_accepted']},indent=2))
