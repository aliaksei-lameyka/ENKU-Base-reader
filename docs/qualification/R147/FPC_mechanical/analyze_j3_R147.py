"""R147 read-only FPC entry corridor study; no qualified folded-flex claim."""
from pathlib import Path
import cadquery as cq
import json,math,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon as PlotPolygon
import numpy as np

P=Path(__file__).resolve().parent;ROOT=P.parent;O=P/'output';O.mkdir(exist_ok=True)
G=json.loads((ROOT/'r147-work/verified/geometry.json').read_text())
PCB=ROOT/'r146-work/repo/hardware/mainboard/r147/kicad/enku-mainboard-r0.1.kicad_pcb'
SHA='856e6d84905f978994316e2efcbb398184cf06dc4f95580c203ee244dd918bb2'
assert hashlib.sha256(PCB.read_bytes()).hexdigest()==SHA
def box(x0,y0,z0,x1,y1,z1):return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def place(s,ref):
 f=G['footprints'][ref];x,y=f['pos'];return s.rotate((0,0,0),(0,0,1),f['angle']).translate((x-18,20-y,1.6))
def bounds(s):
 b=s.BoundingBox();return {k:round(getattr(b,k),6)for k in ['xmin','xmax','ymin','ymax','zmin','zmax']}
official=cq.importers.importStep(str(ROOT/'mech-r146/vendor/hirose_fpc/FH34SRJ-24S-0.5SH.stp')).val()
assert all(not official.isInside(cq.Vector(0,y,.5),1e-7)for y in [-1.89,-1.5,-1.,-.7])
assert official.isInside(cq.Vector(0,-.5,.5),1e-7)
j3=place(official.translate((0,.1,0)),'J3');mouth_y=35.8;cx=G['footprints']['J3']['pos'][0];left,right=cx-6.25,cx+6.25
# Counterexample only: unconstrained0.1mm flex lies flat at0.5mm above top copper.
# It is deliberately NOT presented as the actual bent panel cable.
flat=box(left-18,20-48,2.05,right-18,20-mouth_y,2.15)
caps={};max_caps={};rows=[];assy=cq.Assembly(name='ENKU_R147_J3_FPC_CRITICAL_CAPACITORS_ADDON')
for ref in ['C24','C29','C30','C28']:
 body=place(box(-1,-.625,0,1,.625,1.25),ref);upper=place(box(-1.1,-.725,0,1.1,.725,1.45),ref)
 assert body.isValid()and upper.isValid();caps[ref]=body;max_caps[ref]=upper
 assy.add(upper,name=ref+'_YAGEO_MAX_DIMENSION_ENVELOPE_NO_SOLDER_ALLOWANCE',color=cq.Color(.95,.55,.13))
 b=upper.BoundingBox();world_y_near=20-b.ymax
 rows.append(dict(ref=ref,placement_KiCad_mm=G['footprints'][ref]['pos'],dimension_basis='Yageo exact MPN2.0+/-0.2x1.25+/-0.2x1.25+/-0.2mm',nominal_body_bounds_STEP_mm=bounds(body),upper_dimension_envelope_bounds_STEP_mm=bounds(upper),nearest_body_distance_from_port_mouth_mm=round(world_y_near-mouth_y,6),flat_counterexample_intersection_mm3=round(body.intersect(flat).Volume(),6)))
assy.save(str(O/'ENKU_R147_J3_Critical_Caps_AddOn.step'),exportType='STEP',mode='default')
check=cq.importers.importStep(str(O/'ENKU_R147_J3_Critical_Caps_AddOn.step')).val();assert check.isValid()and len(check.Solids())==4
l2=place(box(-2.5,-2.5,0,2.5,2.5,4),'L2');rows.append(dict(ref='L2',placement_KiCad_mm=G['footprints']['L2']['pos'],nominal_height_mm=4.0,upper_height_mm=4.2,flat_counterexample_intersection_mm3=round(l2.intersect(flat).Volume(),6)))
assert all(r['flat_counterexample_intersection_mm3']>0 for r in rows if r['ref']in ['C24','C29','C30','L2'])
# Exact R147 native placements; plot source XY rather than a false mirrored 3D assembly.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig=plt.figure(figsize=(14,9),dpi=170,facecolor='#f5f7fa');gs=fig.add_gridspec(2,2,width_ratios=[1.0,1.12],height_ratios=[1,.56],hspace=.42,wspace=.24)
ax=fig.add_subplot(gs[:,0]);ax.set_facecolor('white')
for t in G['tracks']:
 if t['layer']!=0 or t['via']:continue
 if max(t['start'][0],t['end'][0])<56 or min(t['start'][1],t['end'][1])>49:continue
 ax.plot([t['start'][0],t['end'][0]],[t['start'][1],t['end'][1]],color='#d9dde2',lw=.65,zorder=0)
ax.add_patch(Rectangle((left,mouth_y),12.5,12.2,facecolor='#e8793425',edgecolor='#d25a18',ls='--',lw=1.5,zorder=1))
ax.text(75.3,48,'12.5 mm straight cable corridor\nCOUNTEREXAMPLE ONLY',ha='right',va='bottom',fontsize=9,color='#a34418',bbox=dict(facecolor='white',alpha=.9,edgecolor='none'))
ax.add_patch(Rectangle((62.27,32.0),14,3.8,facecolor='#35485e',edgecolor='#24354c',lw=1.5,zorder=4));ax.text(69.27,33.8,'J3 | CLOSED',ha='center',va='center',color='white',fontsize=11,zorder=5)
ax.plot([63.02,75.52],[mouth_y,mouth_y],color='#ffbe35',lw=3,zorder=6)
ax.annotate('Insertion into J3\nfrom lower board side',xy=(74.8,35.7),xytext=(74.0,43.0),ha='left',fontsize=10,color='#24354c',arrowprops=dict(arrowstyle='->',lw=1.4),bbox=dict(facecolor='white',edgecolor='none',alpha=.9),zorder=8)
for ref in ['C24','C29','C30','C28']:
 x,y=G['footprints'][ref]['pos'];ax.add_patch(Rectangle((x-.725,y-1.1),1.45,2.2,facecolor='#e88932',edgecolor='#9b440b',zorder=3));ax.text(x,y,ref,ha='center',va='center',rotation=90,fontsize=8,zorder=4)
ax.add_patch(Rectangle((59,41.7),5,5,facecolor='#d05761',edgecolor='#983140',zorder=3));ax.text(61.5,44.2,'L2\n4.0 mm',ha='center',va='center',color='white',zorder=4)
for ref in ['R38','D1']:
 x,y=G['footprints'][ref]['pos'];ax.plot(x,y,'o',color='#536d8a',ms=5,zorder=4);ax.text(x+.3,y,ref,fontsize=9,va='center',color='#3c536c')
ax.annotate('Only 2.1 mm to the\nmaximum capacitor body',xy=(68.9,37.9),xytext=(69.9,45.8),fontsize=10,ha='left',color='#9b440b',arrowprops=dict(arrowstyle='->',color='#9b440b',lw=1.1),bbox=dict(facecolor='white',edgecolor='none',alpha=.9),zorder=7)
ax.set_xlim(57,77.2);ax.set_ylim(49,25.5);ax.set_aspect('equal');ax.set_xlabel('KiCad X, mm');ax.set_ylabel('KiCad Y, mm (down the board)');ax.grid(alpha=.15);ax.set_title('CURRENT R147: real entry direction and nearby parts',loc='left',weight='bold',pad=14)
ax2=fig.add_subplot(gs[0,1]);ax2.set_facecolor('white');ax2.add_patch(Rectangle((31.5,-.25),11.5,.25,facecolor='#317260',edgecolor='none'));ax2.add_patch(Rectangle((32,0),3.8,1.0,facecolor='#35485e',edgecolor='none'));ax2.text(33.8,.75,'J3',ha='center',color='white')
ax2.add_patch(Rectangle((35.8,.45),6.8,.1,facecolor='#bd3844',edgecolor='none',zorder=5));ax2.plot([35.8,35.8],[0,2.2],ls=':',color='#536d8a',lw=.8);ax2.add_patch(Rectangle((37.9,0),2.2,1.45,facecolor='#f2bf90',edgecolor='#a85b1c',ls='--'));ax2.add_patch(Rectangle((38,0),2,1.25,facecolor='#e88932',edgecolor='#9b440b'));ax2.text(39,1.55,'C24 nominal 1.25 mm\n(maximum body 1.45 mm)',ha='center',fontsize=10,color='#9b440b')
ax2.text(40.3,.58,'Flat flex intersects\nthe capacitor volume',ha='left',fontsize=10,color='#ad2635');ax2.text(36.8,.06,'PCB top Z = 0',fontsize=9,color='#143f32',va='bottom');ax2.set(xlim=(31.5,44),ylim=(-.3,2.25),xlabel='KiCad Y, mm',ylabel='Height above PCB top, mm');ax2.set_title('SECTION THROUGH C24 - flat path is not viable',loc='left',weight='bold',pad=14);ax2.grid(alpha=.12)
ax3=fig.add_subplot(gs[1,1]);ax3.axis('off');ax3.text(0,1,'WHAT IS VERIFIED',weight='bold',color='#24354c',fontsize=12,va='top');notes='J3 opens toward +KiCad Y; OEM CAD channel checked.\nC24 / C29 / C30 stand in the straight entry corridor.\nSupplier: bend radius 1-1.5 mm; >=2 mm from glass.\n33.66 mm is a flat projection, not certified usable slack.\n\nStill required: registered display pose, developed flex path,\nlatch/tool access and no-force closure of the case.';ax3.text(0,.79,notes,color='#384d64',linespacing=1.55,va='top',fontsize=10)
fig.suptitle('ENKU R147 | Display FPC: mechanical risk review',x=.08,y=.98,ha='left',fontsize=19,weight='bold',color='#18354c');fig.text(.08,.93,'No PCB edits. No actual folded-flex fit or physical prototype test claimed.',fontsize=11,color='#53677b');fig.subplots_adjust(top=.86,bottom=.08,left=.08,right=.96);fig.savefig(O/'ENKU_R147_J3_FPC_Risk_Map.png',facecolor=fig.get_facecolor());plt.close(fig)
case_file=ROOT/'fpc-fit-r147/case-source/ENKU_R142_Compact_R04_USB_SD_Fusion.zip'
report=dict(revision='R147',pcb_sha256=SHA,source_changed=False,J3_source_origin_mm=G['footprints']['J3']['pos'],J3_world_body_KiCad_mm=[62.27,32,76.27,35.8],J3_mouth_y_KiCad_mm=mouth_y,J3_entry_from='+KiCadY, into port in -Y direction',OEM_mouth_void_probe='PASS; native negativeY channel atZ0.5',entry_contact_plane_above_PCB_mm=.5,free_flex_counterexample_thickness_mm=.1,straight_corridor_KiCad_bbox_mm=[left,35.8,right,48],counterexample_is_not_actual_flex_pose=True,parts=rows,supplier_bend_radius_mm=[1,1.5],engineering_radius_floor_mm=1.5,supplier_glass_to_bend_min_mm=2,panel_flat_projection_mm=33.66,panel_flat_projection_tolerance_mm=.3,panel_projection_is_not_usable_length_certificate=True,exact_folded_reach='NOT QUALIFIED',case_R04=dict(file=case_file.name,sha256=hashlib.sha256(case_file.read_bytes()).hexdigest(),includes_display=False,includes_flex=False,includes_fitted_components=False,trial_mounts_do_not_match_R147=True),critical_caps_addon_nominal='maximum component dimension envelope only; no solder/case margin',addon_roundtrip_valid=True,physical_tests='NOT RUN')
(O/'J3_FPC_Analysis_R147.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(source_sha=SHA,part_counterexamples=[(r['ref'],r['flat_counterexample_intersection_mm3'])for r in rows],addon_valid=True),indent=2))
