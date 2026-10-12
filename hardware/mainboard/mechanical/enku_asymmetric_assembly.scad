// ENKU R0.1 asymmetric enclosure assembly — preliminary feasibility model
// XY in mm, matching current KiCad origin. Not production CAD.
// Display envelope and PCB are independent; enclosure screws DO NOT traverse display.
// Press F5 to inspect, change 'explode' to 8 for exploded stack.
$fn=48;
explode=0;
pcb=[18,20,59,94]; display=[19.38,18.69,56.24,96.62];
front_z=0; front_t=1.0; display_z=1.0; display_t=0.92;
pcb_z=2.42; pcb_t=1.0; rear_z=8.8; rear_t=1.2;
case_x=17; case_y=16; case_w=61; case_h=102; // asymmetric: 2.69 top, 2.69 bottom in module coordinates; adjust via parameters
// Visible exterior bezel relative to DISPLAY MODULE: top 3 mm, bottom 9 mm.
// These are preliminary exterior dimensions, not clearance-validated:
shell_y=display[1]-3; shell_h=display[3]+3+9;
shell_x=display[0]-2.5; shell_w=display[2]+5;
module slab(x,y,z,w,h,t,c){color(c) translate([x,y,z]) cube([w,h,t]);}
module shell_frame(z,t){
 color([0.20,0.24,0.27,0.4]) translate([shell_x,shell_y,z])
 difference(){
 cube([shell_w,shell_h,t]);
 translate([2.5,3,-0.1]) cube([display[2],display[3],t+0.2]);
 }
}
shell_frame(front_z,front_t);
slab(display[0],display[1],display_z,display[2],display[3],display_t,[0.83,0.82,0.76,0.9]);
slab(pcb[0],pcb[1],pcb_z,pcb[2],pcb[3],pcb_t,[0.08,0.43,0.32,0.65]);
// Rear cover, shown in place; make translucent to see stack
slab(shell_x,shell_y,rear_z+explode,shell_w,shell_h,rear_t,[0.32,0.36,0.40,0.22]);
// Battery envelope, explicitly collision-flagged against U1
slab(27,39,pcb_z+pcb_t+0.3,40,60,3.8,[0.22,0.52,0.8,0.35]);
// U1 module marker: XY collision with candidate battery; NOT solved
slab(24,33,pcb_z+pcb_t,18,25,3,[0.95,0.22,0.18,0.8]);
// Lower two rear screw axes are outside display Y footprint; no PCB-through assumptions
for(x=[shell_x+9,shell_x+shell_w-9]){
 color([0.85,0.65,0.2]) translate([x,shell_y+shell_h-3.8,front_z])
 cylinder(d=4.5,h=rear_z+rear_t);
 color([0.12,0.12,0.12]) translate([x,shell_y+shell_h-3.8,front_z-0.1])
 cylinder(d=2.2,h=rear_z+rear_t+0.2);
}
// Upper hooks: representative blocks, NOT tested flexure/undercut geometry
for(x=[shell_x+9,shell_x+shell_w-13])
 slab(x,shell_y+0.5,front_z+front_t,4,2.5,2.0,[0.9,0.6,0.18]);
echo("Case envelope W/H",shell_w,shell_h);
echo("Top/bottom bezel (display-module exterior)",3,9);
echo("Existing PCB end versus lower screws",pcb[1]+pcb[3],shell_y+shell_h-3.8);
echo("WARNING battery overlaps ESP32 module envelope: placement redesign required");
