"""Render actual native copper/track geometry for review, not manufacture."""
import argparse
import gzip
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon as PatchPolygon
from matplotlib.path import Path as PlotPath
from matplotlib.patches import PathPatch

LAYERS = {0:"F.Cu",4:"In1.Cu",6:"In2.Cu",2:"B.Cu"}
POWER = {"3V3_SYS","SYS_EN","VSYS","VBAT","VBUS_USB","EPD_VCI","EPD_SW","EPD_VGH","EPD_VGL","REG_L1","REG_L2"}


def drill_ring(pad):
    w, h = pad["drill"]; radius=min(w,h)/2
    dx, dy=max(w-h,0)/2,max(h-w,0)/2
    angle=math.radians(-pad["angle"]); ca,sa=math.cos(angle),math.sin(angle)
    result=[]
    for i in range(256):
        a=2*math.pi*i/256; c,s=math.cos(a),math.sin(a)
        x=radius*c+math.copysign(dx,c); y=radius*s+math.copysign(dy,s)
        result.append([pad["pos"][0]+ca*x-sa*y,pad["pos"][1]+sa*x+ca*y])
    return result


def polygon_with_holes(ax, shell, holes, color):
    def area(ring):
        return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]+ring[:1]))
    coordinates=[]; codes=[]; sign=area(shell)
    for ring, hole in [(shell,False)]+[(p,True) for p in holes]:
        if len(ring)<3:continue
        if hole and sign*area(ring)>0:ring=list(reversed(ring))
        coordinates += ring+[ring[0]]
        codes += [PlotPath.MOVETO]+[PlotPath.LINETO]*(len(ring)-1)+[PlotPath.CLOSEPOLY]
    ax.add_patch(PathPatch(PlotPath(coordinates,codes),facecolor=color,edgecolor="none",zorder=0))


def render(native, review, output):
    output.mkdir(parents=True,exist_ok=True)
    g=json.loads((native/"geometry.json").read_text())
    copper=json.loads(gzip.decompress((native/"native_copper_R138.json.gz").read_bytes()))
    result=json.loads(review.read_text())
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9})
    def draw(layer,bounds,name,refnames=(),route=None,reference_layer=None):
        x0,y0,x1,y1=bounds;w=x1-x0;h=y1-y0
        fig,ax=plt.subplots(figsize=(8.0,8.0*h/w+.8),dpi=130)
        ax.set_position([.06,.05,.91,.9]);ax.set_xlim(x0,x1);ax.set_ylim(y1,y0);ax.set_aspect("equal")
        background_layer=layer if reference_layer is None else reference_layer
        for p in copper["filled_zones"][str(background_layer)]:
            polygon_with_holes(ax,p["shell"],p["holes"],"#e2e7e7")
        points_per_mm=(8.0*.91*72)/w
        for t in g["tracks"]:
            if t["via"]:
                ax.add_patch(Circle(t["start"],t["width"]/2,facecolor="#acb7bc",edgecolor="none",zorder=3))
                ax.add_patch(Circle(t["start"],t["drill"]/2,facecolor="white",edgecolor="none",zorder=4))
            elif t["layer"]==layer:
                color="#9aa5aa" if t["net"]=="GND" else "#d78b31" if t["net"]in POWER else "#2e7398"
                ax.plot([t["start"][0],t["end"][0]],[t["start"][1],t["end"][1]],color=color,
                        linewidth=t["width"]*points_per_mm,solid_capstyle="round",zorder=2)
        for p in g["pads"]:
            for ring in p["polygons"].get(str(layer),[]):
                ax.add_patch(PatchPolygon(ring,facecolor="#5c6970",edgecolor="none",zorder=3))
            if max(p["drill"])>0 and layer in p["layers"]:
                ax.add_patch(PatchPolygon(drill_ring(p),facecolor="white",edgecolor="none",zorder=4))
        for outline in g["board_outline"]:
            closed=outline+[outline[0]];ax.plot(*zip(*closed),color="#26323d",linewidth=1,zorder=5)
        for gap in result["fast_signal_reference_gaps"]:
            if gap["signal_layer"]!=LAYERS[layer]:continue
            for coords in gap["both_inner_gap_pieces_mm"]:
                ax.plot(*zip(*coords),color="#ae1761",linewidth=2.3,zorder=6)
        if route:
            for edge in route["path_centerline_edges"]:
                if edge["layer"]!=LAYERS[layer]:continue
                ax.plot([edge["start"][0],edge["end"][0]],[edge["start"][1],edge["end"][1]],
                        color="#bc2528",linewidth=2.0,zorder=7)
        for ref in refnames:
            pos=g["footprints"][ref]["pos"]
            ax.annotate(ref,pos,xytext=(6,-10),textcoords="offset points",fontweight="bold",color="#20272f",
                        bbox=dict(boxstyle="round,pad=.16",facecolor="white",edgecolor="none",alpha=.92),zorder=8)
        ax.grid(alpha=.18);ax.set_xlabel("Board X (mm)");ax.set_ylabel("Board Y (mm)")
        label=LAYERS[layer] if reference_layer is None else LAYERS[layer]+" over "+LAYERS[reference_layer]+" GND projection"
        ax.set_title("R141 recovered candidate review - "+label+"\nNative geometry; review view, not a fabrication drawing",pad=11)
        fig.savefig(output/name,dpi=130);plt.close(fig)
    for layer in LAYERS:
        draw(layer,[17,19,78,122],"layer_"+LAYERS[layer].replace(".","_")+"_R141.png",
             ["U1","U3","U4","J2","J3","J5","J1"] if layer==0 else ())
    epd=next(p for p in result["actual_track_paths"]if p["net"]=="EPD_SW" and p["target"]==["D1","2"])
    draw(0,[44,36,74,55],"EPD_switching_R141.png",["Q1","L2","D1","C25","C24","R37","R28"],epd)
    cap=next(p for p in result["actual_track_paths"]if p["net"]=="VBUS_USB" and p["source"]==["C5","1"])
    for layer in [0,4,2]:
        draw(layer,[41,82,65,104],"charger_C5_"+LAYERS[layer].replace(".","_")+"_R141.png",
             ["U3","C5","C7","C8","U4","C9","C11","C12"],cap)
    draw(2,[40,84,52,99],"SPI_clock_reference_R141.png",["U3","C5","C7","C8"],reference_layer=6)
    draw(0,[32,34,50,59],"SPI_MCU_reference_R141.png",["U1","R19"],reference_layer=6)
    draw(2,[31,73,52,110],"SD_SPI_reference_R141.png",["R20","R21","J2"],reference_layer=6)
    print("Rendered four complete native copper views and seven focused routing views")


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("native",type=Path);ap.add_argument("review",type=Path);ap.add_argument("output",type=Path)
    args=ap.parse_args();render(args.native,args.review,args.output)
