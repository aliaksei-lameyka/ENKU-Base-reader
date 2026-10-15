"""Reproducible ENKU R148 nominal enclosure reference; millimetres.

Vendor solids remain separate in a named STEP assembly. No electrical edits.
Source origin KiCad (18,20), CAD X right, Y toward the top, Z above PCB.
"""
from pathlib import Path
import cadquery as cq
import json, hashlib, math, csv

P=Path(__file__).resolve().parent
ROOT=P.parent
V=P/'vendor'; OUT=P/'output'; OUT.mkdir(exist_ok=True)
SRC=P/'reference/enku-mainboard-r0.1.kicad_pcb'
GEOM=P/'reference/geometry.json'
G=json.loads(GEOM.read_text())
SHA=(P/'reference/source_pcb.sha256').read_text().split()[0]
assert hashlib.sha256(SRC.read_bytes()).hexdigest()==SHA

def bbox(s):
 b=s.BoundingBox();return {k:round(getattr(b,k),7) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']}
def box(x0,y0,z0,x1,y1,z1):
 return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def comp(shapes):return cq.Compound.makeCompound(shapes)
def place(s,ref):
 f=G['footprints'][ref];x,y=f['pos']
 return s.rotate((0,0,0),(0,0,1),f['angle']).translate((x-18,20-y,1.6))
def source_model(f):return cq.importers.importStep(str(f)).val()

native=source_model(P/'board_native.step')
face=max((f for f in native.Faces() if f.geomType()=='PLANE' and abs(f.Center().z-1.51)<1e-5),key=lambda f:f.Area())
assert len(face.innerWires())==25
face=face.translate((0,0,-1.51))
board=cq.Solid.extrudeLinear(face.outerWire(),face.innerWires(),cq.Vector(0,0,1.6))
assert board.isValid() and len(board.Solids())==1
assert abs(board.Volume()-native.Volume()*1.6/1.51)<1e-5
assert bbox(board)==dict(xmin=0.0,xmax=59.0,ymin=-101.0,ymax=0.0,zmin=0.0,zmax=1.6)
assembly=cq.Assembly(name='ENKU_R148_NOMINAL_ENCLOSURE_REFERENCE')
objects={};records=[]
def add(ref,name,s,basis,color=(.68,.7,.74),notes=''):
 assert s.isValid(),name
 objects[name]=s
 assembly.add(s,name=name,color=cq.Color(*color))
 records.append(dict(ref=ref,name=name,basis=basis,notes=notes,bbox_mm=bbox(s),solids=len(s.Solids()),valid=True,
                      pcb_placement=G['footprints'].get(ref)))

add('PCB','PCB_59x101x1p6_25_REAL_HOLES',board,'R148 KiCad exact contour and drilled holes; nominal finished thickness1.6',(.05,.29,.21))
# Espressif CAD origin is lower-left of the18x25.5 body; native +Y points toward antenna.
esp=source_model(V/'ESP32-S3-WROOM-1.STEP').translate((-9,-12.75,0))
add('U1','U1_ESP32_S3_WROOM_1_OEM',place(esp,'U1'),'Espressif official STEP',(.63,.65,.66),'Exact module body; RF plastic/metal constraints also supplied as a separate advisory zone.')
# Hirose DM3AT datum comes from contact X1=+2.775 and mouth Y=-8.125; not bbox centring.
sd=source_model(V/'hirose_sd/DM3AT-SF-PEJM5.stp').translate((-165.190260,-153.787419,0))
add('J2','J2_DM3AT_MICROSD_OEM',place(sd,'J2'),'Hirose official STEP + matching 2D mounting drawing',(.69,.71,.73),'Includes actual contact tails;13.85x16.15x1.68, mouth0.875mm inboard of left edge.')
# Body in source fab is v=-2..1.8; CADY=-v gives -1.8..2.0.
fpc=source_model(V/'hirose_fpc/FH34SRJ-24S-0.5SH.stp').translate((0,.1,0))
add('J3','J3_FH34SRJ_24S_FPC_OEM_CLOSED',place(fpc,'J3'),'Hirose official STEP + EDC-159714-50',(.29,.3,.31),'24 terminal X centres/pitch checked. Closed actuator only; actual folded display FPC remains unqualified.')
tact=source_model(V/'TL1016AAFxxxQG.stp').translate((-.532943445710085,-.206496547112306,.4955960063542693))
for ref in ['SW3','SW4','SW5','SW6']:
 add(ref,ref+'_TL1016AA_SIDE_BUTTON_OEM',place(tact,ref),'E-Switch configured official AA/F model; drawing P520001 RevA',(.32,.34,.36),'Actuator extends to CAD-localY=-2.1. No locating bosses. Travel0.20 +0.2/-0.1mm. Tip1.45mm inside board edge.')
boot=source_model(V/'TL3342FxxxQG.stp')
boot=boot.translate((0,0,-boot.BoundingBox().zmin))
add('SW2','SW2_TL3342_BOOT_BUTTON_OEM',place(boot,'SW2'),'E-Switch configured official F model; drawing P010632 RevJ',(.48,.5,.52),'Top actuator diameter2.0mm, nominal height1.5mm; vendor STEP height1.503715mm after seating terminals.')
# USB enclosure reference reconstructed from GCT RevA (2024-04-26), not a substitute vendor CAD.
# Section profile: shell OD8.94x3.16, opening8.34x2.56; mouthv=3.675 at boardY121.
outer=cq.Workplane('XZ').center(0,1.58).rect(8.94,3.16).extrude(6.5).edges('|Y').fillet(1.38).val()
# XZ extrusion runs toward -Y; relocate to span CAD-local[-3.675,2.825].
outer=outer.translate((0,2.825,0))
inner=cq.Workplane('XZ').center(0,1.58).rect(8.34,2.56).extrude(6.7).edges('|Y').fillet(1.15).val().translate((0,2.925,0))
shell=outer.cut(inner)
back=box(-3.85,1.425,.3,3.85,2.825,2.85)
tongue=box(-3.2,-2.5,1.23,3.2,1.5,1.93)
stakes=[box(x-.125,y-.4,-.8,x+.125,y+.4,.3) for x in [-4.32,4.32] for y in [-1.575,2.425]]
usb=comp([shell,back,tongue,*stakes])
add('J5','J5_USB4215_03_A_DRAWING_NOMINAL',place(usb,'J5'),'GCT USB4215 RevA26Apr2024 dimension reconstruction',(.72,.74,.77),'Nominal mating shell and tongue,4stakes; small shell embossings/contact fingers omitted. Port OD and mating face exact nominal; do not use internal reconstruction to design a USB plug.')
# SW1 manufacturer drawing has unresolved body-to-peg Y datum in accepted source.
# Keep the accepted nominal assumption explicit in object name and notes.
swbody=box(-3.3,-1.375,0,3.3,1.375,1.4)
act=box(-1.4,-2.875,.2,1.4,-1.375,1.3)
pegs=[cq.Solid.makeCylinder(.4,.6,cq.Vector(x,0,-.6)) for x in [-1.5,1.5]]
sw1=comp([swbody,act,*pegs])
add('SW1','SW1_MK12C03G015_NOMINAL_DATUM_HOLD',place(sw1,'SW1'),'G-Switch MK-12C03-G015 drawing2022-11-01 + source footprint',(.9,.59,.14),'HOLD: body centred on locator line is a source assumption; latching states/datum need actual sample. Slide travel1.5+/-0.1mm. Envelope is not a fit-qualified model.')
# J1 is bare wire lands with no fitted plastic housing.
add('L2','L2_TYS5040_NOMINAL_5x5x4',place(box(-2.5,-2.5,0,2.5,2.5,4.0),'L2'),'Laird TYS5040 RevA p2:5.0+/-0.2 square, height4.0+0.2/-0.3',(.22,.23,.24),'Use separate5.2x5.2x4.2 tolerance envelope when reserving case space.')
add('L1','L1_DFE201612_NOMINAL_ENVELOPE',place(box(-1,-.8,0,1,.8,1.2),'L1'),'Package size201612 nominal from exact BOM footprint',(.25,.26,.27),'Small inductor included for spatial context; no tolerance qualification.')

for ref in ['C24','C29','C30','C31','C28','C25','C26','C27']:
 add(ref,ref+'_YAGEO_MAX_BODY_ENVELOPE',place(box(-1.1,-.725,0,1.1,.725,1.45),ref),'Yageo exact CC0805 25V sheets:2.0+/-0.2 x1.25+/-0.2 x1.25+/-0.2',(.94,.52,.17),'Maximum body envelope. No solder/placement allowance.')
for ref in ['D1','D2','D3']:
 add(ref,ref+'_SOD123_DRAWING_ENVELOPE',place(box(-1.3,-.8,0,1.3,.8,1.35),ref),'Simplified nominal SOD123 body proxy; not a maximum package envelope',(.35,.36,.39),'Use native footprint courtyard for XY clearance; not exact vendor CAD or a max envelope.')
add('Q1','Q1_MICRO3_CONSERVATIVE_PACKAGE_ENVELOPE',place(box(-1.32,-1.52,0,1.32,1.52,1.12),'Q1'),'Infineon IRLML6346 MICRO3/SOT23 package envelope',(.35,.36,.39),'Rectangular package reserve, not exact mould/lead geometry.')
for ref,size in [('R37',(2.2,1.45,.6)),('R38',(1.7,.95,.6)),('R28',(1.7,.95,.6))]:
 x,y,z=size;add(ref,ref+'_RESISTOR_ENGINEERING_ENVELOPE',place(box(-x/2,-y/2,0,x/2,y/2,z),ref),'Conservative package reserve; source MPN footprint retained',(.35,.36,.39),'Simplified body envelope; no closure qualification.')

assembly.save(str(OUT/'ENKU_R148_Enclosure_Reference.step'),exportType='STEP',mode='default')
cq.exporters.export(board,str(OUT/'ENKU_R148_Bare_Board.step'))

access=cq.Assembly(name='ENKU_R148_ADVISORY_ACCESS_AND_TOLERANCE_ZONES')
zones={};zrec=[]
def zone(name,s,basis,notes):
 assert s.isValid(),name
 zones[name]=s;access.add(s,name=name,color=cq.Color(1,.45,.08,.25));zrec.append(dict(name=name,basis=basis,notes=notes,bbox_mm=bbox(s)))
# All these are intentional design reserves, never fitted components or final cutouts.
zone('USB_PLUG_AND_FINGER_ACCESS_ADVISORY',box(23.5,-114,1.3,34.5,-100.7,5.5),'Design allowance11mm width,4.2mm height,13mm outside board','Actual chosen cable overmould not supplied; measure before finalising wall opening. Port mouth centre(29,-101,3.18).')
# Hirose card leading edge projections from contact back plane:17.55locked,16.75overstroke,21.55ejected.
# Source contact/back datum at localv=-7.825 -> card outer edgev=9.725/8.925/13.725.
# The card width centre is-0.425 relative to connectorX based on (7.35) vs body edge.
for state,edge in [('LOCKED',9.725),('PUSH_OVERSTROKE',8.925),('EJECTED',13.725)]:
 card=box(-5.925,-edge,.12,5.075,-edge+15.0,1.12)
 zone('MICROSD_CARD_'+state+'_DRAWING_REFERENCE',place(card,'J2'),'Hirose EDC-325166-00 p1 card stroke reference; nominal11x15x1 card','Reference card position; validate chosen card and physical connector. Ejection direction is toward left board edge.')
zone('MICROSD_FINGER_ACCESS_ADVISORY',box(-10,-87.2,1.6,1.2,-74.2,5.1),'Case design reserve','Additional fingernail/pusher access is a case choice, not a manufacturer maximum envelope.')
for ref in ['SW3','SW4','SW5','SW6']:
 # reserve unpressed-to-max-pressed0.4mm and route to outer PCB side.
 zone(ref+'_PUSHER_ACCESS_ADVISORY',place(box(-1.15,-4.3,.05,1.15,-1.5,1.6),ref),'Design reserve + manufacturer travel0.1..0.4mm','Axis/outward access only. Avoid preload; actual case pusher geometry/tolerance must be added.')
zone('SW1_SLIDER_TRAVEL_AND_DATUM_HOLD',place(box(-3.0,-3.2,0,3.0,-1.15,1.8),'SW1'),'Conservative design sweep;1.5+/-0.1 stroke, unknown initial detent datum','Do not dimension a final slot from SW1 until physical datum confirmed.')
zone('SW2_BOOT_TOP_ACCESS_ADVISORY',place(cq.Solid.makeCylinder(1.4,8,cq.Vector(0,0,1.2)),'SW2'),'2.8mm service tool reserve','Optional service access. SW2 is BOOT, not a user reset button.')
zone('J3_FPC_COMPONENT_FREE_APPROACH_14x10p7',box(44.27,-26.5,1.65,58.27,-15.8001,6.35),'R148 front courtyard reservation','Local component-free approach only. Not an actual folded FPC or exact latch sweep. Full back-to-back display fold, pin1, reach and closure remain HOLD.')
zone('J1_WIRES_AND_CASE_CLAMP_RESERVE_1p2mm_ASSUMPTION',box(47.2,-77,1.6,58,-72.2,2.8),'Engineering allowance: wire OD<=0.8mm and completed fillet/clamp<=1.2mm above PCB','Not a selected harness or qualified clamp. Clamp insulation above PCB; do not lace against display rear. PCM pack and cell NTC on J8 remain required.')
zone('J7_TAGCONNECT_BOTTOM_SERVICE_ADVISORY',place(box(-4.6,-3.4,-13.6,4.6,3.4,-1.6),'J7'),'Conservative service-tool allowance only; actual contacts are on B.Cu','J7 is bare PCB contact array and3holes, not an installed connector. Tool dimensions/retention need actual TC2030-IDC-NL drawing or sample.')
zone('J8_NTC_WIRE_ACCESS_ADVISORY',place(box(-2.5,-3,0,2.5,3,4),'J8'),'Wire/strain-relief allowance only','J8 consists of solder pads; no installed connector. Cell/NTC route not fixed.')
zone('L2_MAX_TOLERANCE_ENVELOPE',place(box(-2.6,-2.6,0,2.6,2.6,4.2),'L2'),'Laird dimensional upper limits','No placement/solder/case tolerance included.')
# The outline notch and PCB RF rule remain authoritative for board copper; external metal zone is advisory.
zone('ESP_ANTENNA_EXTERNAL_METAL_RESERVE_ADVISORY',box(-10,-35.5,0,10,-14.5,10),'Provisional external metal separation zone; final RF test required','Plastic is permitted subject to RF tuning; avoid batteries/metal and conductive paint. Not a certified all-direction RF spacing specification.')
access.save(str(OUT/'ENKU_R148_Access_Zones_OPTIONAL.step'),exportType='STEP',mode='default')

holes=[]
for ref in ['H1','H2','H3','H4']:
 f=G['footprints'][ref];x,y=f['pos'];p=next(p for p in G['pads'] if p['ref']==ref)
 holes.append(dict(ref=ref,kicad_x_mm=x,kicad_y_mm=y,step_x_mm=x-18,step_y_mm=20-y,diameter_mm=p['drill'][0]))
with (OUT/'Mounting_Holes_mm.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(holes[0]));w.writeheader();w.writerows(holes)
with (OUT/'Bare_Service_Contacts_mm.csv').open('w',newline='')as f:
 fields=['ref','pin','net','side','step_x_mm','step_y_mm','step_z_mm','size_x_mm','size_y_mm'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for p in G['pads']:
  if p['ref']in ['J1','J7','J8']and p['number']:
   bottom=p['layers']==[2];w.writerow(dict(ref=p['ref'],pin=p['number'],net=p['net'],side='BOTTOM'if bottom else'TOP',step_x_mm=p['pos'][0]-18,step_y_mm=20-p['pos'][1],step_z_mm=0 if bottom else 1.6,size_x_mm=3.5 if p['ref']=='J1'else p['size'][0],size_y_mm=1 if p['ref']=='J1'else p['size'][1]))
with (OUT/'Mechanical_Part_Positions_mm.csv').open('w',newline='')as f:
 fields=['ref','name','step_x_mm','step_y_mm','rotation_deg','xmin','xmax','ymin','ymax','zmin','zmax','basis','notes'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in records:
  fp=r['pcb_placement'];w.writerow(dict(ref=r['ref'],name=r['name'],step_x_mm=fp['pos'][0]-18 if fp else 0,step_y_mm=20-fp['pos'][1]if fp else 0,rotation_deg=fp['angle']if fp else 0,**r['bbox_mm'],basis=r['basis'],notes=r['notes']))
report=dict(revision='R148',pcb_sha256=SHA,source_commit='bec2966be64cd6fdce5b1060f05179370ff0da77',units='mm',nominal_board_mm=[59,101,1.6],datum='KiCad(18,20) becomes CAD(0,0); CADY=20-KiCadY; bottomZ0/topZ1.6',native_dielectric_step_height_mm=1.51,physical_board_height_reconstructed_mm=1.6,board_inner_wires=25,mounting_holes=holes,parts=records,advisory_zones=zrec,physical_fit_qualified=False,electrical_topology_changes=False,J1='Bare VBAT/GND wire pads; fitted connector removed',display_architecture='Display back faces PCB back. Actual folded flex and insulating/support gap remain HOLD.')
(OUT/'Mechanical_Provenance_and_Dimensions.json').write_text(json.dumps(report,indent=2)+'\n')
print('Exported',len(records),'assembly objects and',len(zrec),'optional advisory zones',flush=True)

if __name__=='__main__':
 # Roundtrip from final files in a new document; catch malformed STEP before delivery.
 checks={}
 for n in ['ENKU_R148_Enclosure_Reference.step','ENKU_R148_Bare_Board.step','ENKU_R148_Access_Zones_OPTIONAL.step']:
  s=source_model(OUT/n);checks[n]=dict(valid=s.isValid(),solids=len(s.Solids()),bbox_mm=bbox(s),volume_mm3=s.Volume(),sha256=hashlib.sha256((OUT/n).read_bytes()).hexdigest());assert checks[n]['valid']and checks[n]['solids']>0
 # Exact hole centres and diameters: point inside void, adjacent material present.
 for h in holes:
  x,y=h['step_x_mm'],h['step_y_mm'];r=h['diameter_mm']/2
  assert not board.isInside(cq.Vector(x,y,.8),1e-7)
  assert not board.isInside(cq.Vector(x+r-.01,y,.8),1e-7)
  assert board.isInside(cq.Vector(x+r+.01,y,.8),1e-7)
 checks['mounting_holes_exact_radius_probe']='PASS4'
 checks['native_xy_cross_section_and_holes_preserved']='PASS analytic extrusion of exact native face'
 (OUT/'STEP_Roundtrip_QA.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2),flush=True)
