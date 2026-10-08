// ENKU Reader R0.1 — preliminary fastener envelope, NOT a validated assembly
// Coordinates use KiCad XY in mm. Z exaggerated for readability.
$fn=48;
pcb_x0=18; pcb_x1=77;
pcb_y0=12; pcb_y1=122; // CANDIDATE 59 x 110 mm, NOT applied to PCB
display_w=56.24; display_h=96.62;
cx=47.5; cy=67;
disp_x0=cx-display_w/2; disp_y0=cy-display_h/2;
boss_d=5.0; drill_d=2.2;
holes=[[30,15],[71,15],[30,119],[71,119]]; // candidate, NOT KiCad positions
module slab(x,y,z,w,h,t,c) {color(c) translate([x,y,z]) cube([w,h,t]);}
slab(pcb_x0,pcb_y0,0,pcb_x1-pcb_x0,pcb_y1-pcb_y0,1,[0.1,0.43,0.35,0.75]);
slab(disp_x0,disp_y0,3,display_w,display_h,0.92,[0.82,0.83,0.78,0.8]);
for(p=holes) {
  color([0.8,0.56,0.2,0.9])
  translate([p[0],p[1],0]) difference() {
    cylinder(d=boss_d,h=3);
    translate([0,0,-0.1]) cylinder(d=drill_d,h=3.2);
  }
}
echo("DISPLAY_Y",disp_y0,disp_y0+display_h);
echo("TOP_BOSS_TO_DISPLAY_GAP",disp_y0-(15+boss_d/2));
echo("BOTTOM_BOSS_TO_DISPLAY_GAP",(119-boss_d/2)-(disp_y0+display_h));
