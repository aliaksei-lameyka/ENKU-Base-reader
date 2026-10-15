"""Independent nominal Hirose rev4 p1 mounting-side no-pattern transcription.
Anchor pin1 x2.775, row land bottom y-7.125. Cross-band dimensions8.2/.5,
vertical offsets4.4/6.0; adjacent strip x8.9..8.2 relative to pin1.
Primary supplied PDF SHA43ac6f1af4a1fd92836f71e34614bbbc36903d2f403ff63c5aa4910da6a1e6ca.
These are engineering nominal constraints; part/case/process fit is not qualified.
"""
import math
POLYGONS=[
 [(-7.2,-7.125),(-6.45,-7.125),(-6.45,-4.025),(-7.2,-4.025)],
 [(-7.2,-2.825),(-6.45,-2.825),(-6.45,.775),(-7.2,.775)],
 [(-5.425,-2.725),(3.275,-2.725),(3.275,-1.125),(-5.425,-1.125)],
 [(-6.125,-1.425),(-5.425,-1.425),(-5.425,6.225),(-6.125,6.225)],
 [(2.925,6.975),(5.475,6.975),(5.475,7.975),(6.025,7.975),(6.025,8.325),(2.925,8.325)]]
def transform(q,fp):
 a=math.radians(fp['angle']);x,y=q;cx,cy=fp['pos'];return [round(cx+math.cos(a)*x+math.sin(a)*y,6),round(cy-math.sin(a)*x+math.cos(a)*y,6)]
