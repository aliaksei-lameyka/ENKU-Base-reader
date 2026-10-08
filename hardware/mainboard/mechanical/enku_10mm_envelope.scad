// ENKU Reader mechanical envelope study — NOT a manufacturing model
// All coordinates in mm, based on KiCad R0.1 placements (2026-10-08).
// Open in OpenSCAD; F5 preview, F6 render. Change parameters to explore.
$fn=24;
pcb_x0=18; pcb_y0=20; pcb_w=59; pcb_h=94; pcb_t=1.0;
case_target=10; front_t=1.0; rear_t=1.0;
display_w=56.24; display_h=96.62; display_t=0.92;
support_gap=0.5; battery_t=3.8; battery_w=40; battery_h=60;
battery_x=27; battery_y=39; // PROVISIONAL envelope; collisions must be resolved
// WARNING: the battery envelope intersects the U1 ESP32 placement region in XY.
// The 10 mm target cannot be approved until a component-height map and battery
// pocket prove actual physical separation. Do not treat this as a solved layout.
// KiCad coordinate y increases down the board; this mockup uses same xy.
module slab(x,y,z,w,h,t,c){color(c) translate([x,y,z]) cube([w,h,t]);}
slab(pcb_x0,pcb_y0,front_t+display_t+support_gap,pcb_w,pcb_h,pcb_t,[0.08,0.42,0.35]);
slab((pcb_x0+pcb_w/2)-display_w/2,(pcb_y0+pcb_h/2)-display_h/2,front_t,display_w,display_h,display_t,[0.75,0.75,0.70]);
slab(battery_x,battery_y,front_t+display_t+support_gap+pcb_t+0.3,battery_w,battery_h,battery_t,[0.28,0.50,0.70,0.65]);
// Board outline / major connectors and placeholder switches
module marker(x,y,w,h,label_color){slab(x-w/2,y-h/2,front_t+display_t+support_gap+pcb_t,w,h,0.8,label_color);}
marker(58,28,13,4,[0.85,0.55,0.2]); // J3 FPC
marker(47,110.325,9,5,[0.75,0.75,0.8]); // J5 USB-C
marker(28.9,100.7,12,11,[0.85,0.5,0.2]); // J2 microSD, rotated
marker(66,93.5,8,6,[0.85,0.5,0.2]); // J1 battery
marker(30.5,29,7,4,[0.85,0.2,0.2]); // SW1 placeholder
for (y=[63,75]) {
  marker(25,y,3.8,5,[0.9,0.7,0.2]);
  marker(71.2,y,3.8,5,[0.9,0.7,0.2]);
}
// Reference only: do NOT infer collision-free design from this envelope.
// Battery overlaps some markers in XY; actual component bodies and routing
// must be imported from KiCad before locking its position.
echo("Nominal stack (no high components) =",front_t+display_t+support_gap+pcb_t+0.3+battery_t+rear_t);
echo("Remaining from 10 mm target =",case_target-(front_t+display_t+support_gap+pcb_t+0.3+battery_t+rear_t));
