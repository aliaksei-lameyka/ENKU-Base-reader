"""Explicit 0.50/0.20mm new bias-route vias; R141 router unchanged."""
"""Geometry-only proposal helpers. Real native results determine progress."""
import copy,json,math,collections
from pathlib import Path
import numpy as np
import shapely as sh
from shapely.geometry import Point,LineString,Polygon,box
from router import Router
from pad_groups import components

FAST={"SPI_SCLK","SPI_MOSI","SPI_MISO","SD_SCLK_CARD","SD_MOSI_CARD","SD_MISO_CARD",
      "SD_CS","SD_CS_CARD","EPD_SCLK_PANEL","EPD_MOSI_PANEL"}
EP=box(47.6,90.1,49.4,91.9)
class ProposalRouter:
    def __init__(self,g,checks,region,step=.05):
        self.g=copy.deepcopy(g);self.r=Router(self.g,step=step,layers=(0,2,4,6),region=region)
        self.pads={(p["ref"],p["number"]):p for p in self.g["pads"]}
        usb=[t for t in self.g["tracks"]if t["net"].startswith("USB_D")]
        voids=sh.union_all([Point(t["start"]).buffer(t["width"]/2+.26)for t in usb if t["via"]])
        center=LineString(json.loads((Path(checks)/"accepted_usb_add.json").read_text())["centerline"])
        self.protected={4:sh.union_all([LineString([t["start"],t["end"]]).buffer(t["width"]/2).difference(voids)for t in usb if not t["via"]and t["layer"]==0]),
                        6:sh.union_all([center.buffer(.5,join_style=2)]+[LineString([t["start"],t["end"]]).buffer(t["width"]/2).difference(voids)for t in usb if not t["via"]and t["layer"]==2])}
        self.usb_protected=dict(self.protected)
        for layer,outer in[(4,0),(6,2)]:
            self.protected[layer]=self.protected[layer].union(sh.union_all([LineString([t["start"],t["end"]]).buffer(t["width"]/2+.15)for t in self.g["tracks"]if not t["via"]and t["layer"]==outer and t["net"]in FAST]))
    def masks(self,net,width,front=False):
        r=self.r;ms,vm=r.masks(net,width,.5)
        # Hole-to-hole clearance applies even between two same-net barrels.
        for t in self.g["tracks"]:
            if t["via"]:r.stamp(vm,Point(t["start"]),t["drill"]/2+.10+.255)
        # Reuse an existing exact-grid through via without creating another hole.
        for t in self.g["tracks"]:
            if not t["via"]or t["net"]!=net:continue
            k=r.idx(t["start"],0)
            if 0<=k[1]<len(r.ys)and 0<=k[2]<len(r.xs)and r.xy(k)==t["start"]:vm[k[1],k[2]]=False
        if net!="GND":
            for layer,shape in self.protected.items():
                r.stamp(ms[r.layers.index(layer)],shape,width/2+.265)
                outer=0 if layer==4 else 2
                foreign=sh.union_all([LineString([t['start'],t['end']]).buffer(t['width']/2+.15)
                    for t in self.g['tracks']if not t['via']and t['layer']==outer and t['net']in FAST and t['net']!=net])
                r.stamp(vm,self.usb_protected[layer].union(foreign),.25+.265)
            r.stamp(ms[r.layers.index(2)],EP,width/2+.205);r.stamp(vm,EP,.25+.205)
        if net=="VBAT":ms[r.layers.index(6)][:]=True
        if front:
            for l in[2,4,6]:ms[r.layers.index(l)][:]=True
            vm[:]=True
        return ms,vm
    def add(self,plan,net,starts,ends,width=.2,front=False,timeout=45):
        result=self.r.route(net,starts,ends,width=width,vd=.5,timeout=timeout,masks=self.masks(net,width,front))
        if result is None:raise RuntimeError("No safe geometric proposal for "+net)
        plan["routes"].append(result);before=len(self.g["tracks"]);self.r.add(result)
        print("Route",net,round(result["length_mm"],3),"mm",len(result["vias"]),"vias",flush=True)
        return result,self.g["tracks"][before:]

def cap_ground(router,plan,ref):
    r=router.r;pad=router.pads[(ref,"2")];ms,vm=router.masks("GND",.3)
    dist=(r.X-pad["pos"][0])**2+(r.Y-pad["pos"][1])**2
    candidates=np.argwhere(~vm&~ms[0]&(dist<4))
    candidates=sorted(candidates,key=lambda yx:dist[tuple(yx)])
    front_masks=router.masks("GND",.3,True)
    for y,x in candidates[:600]:
        pos=r.xy((0,int(y),int(x)))
        target=dict(net="GND",via=True,start=pos,end=pos,layer=0,uuid="ground-"+ref)
        result=r.route("GND",[pad],[target],width=.3,vd=.6,timeout=.25,masks=front_masks)
        if result and result["length_mm"]<2:
            result["vias"]=[pos];plan["routes"].append(result);r.add(result)
            print("Ground",ref,round(result["length_mm"],3),"mm",pos,flush=True);return
    raise RuntimeError("No short GND return for "+ref)

def charger(native,checks,output):
    g=json.loads((native/"geometry.json").read_text());d=json.loads((native/"drc.json").read_text())
    remove={t["uuid"]for t in g["tracks"]if t["net"]in{"CHG_STAT2","CHG_TMR"}or(t["net"]=="VBAT"and not t["via"]and t["layer"]==6)or(t["net"]=="VBUS_USB"and not t["via"]and t["layer"]==4 and LineString([t["start"],t["end"]]).intersects(box(41,88,56,100)))}
    lands=sh.union_all([Polygon(q)for p in g["pads"]if p["ref"]in{"C5","C7","C8"}for q in p["polygons"].get("0",[])])
    for t in g["tracks"]:
        if t["via"]and lands.distance(Point(t["start"]))-t["width"]/2<.100001:remove.add(t["uuid"])
    for v in d["violations"]:
        if v["type"]in{"track_dangling","via_dangling"}:remove.update(i["uuid"]for i in v["items"])
        if v["type"]in{"clearance","shorting_items","hole_clearance"}and any("of "+ref+" "in i["description"]for ref in["C5","C7","C8"]for i in v["items"]):
            ids={t["uuid"]for t in g["tracks"]};remove.update(i["uuid"]for i in v["items"]if i["uuid"]in ids)
    positions={tuple(t["start"])for t in g["tracks"]if t["via"]and t["uuid"]in remove}
    remove.update(t["uuid"]for t in g["tracks"]if not t["via"]and(tuple(t["start"])in positions or tuple(t["end"])in positions))
    g["tracks"]=[t for t in g["tracks"]if t["uuid"]not in remove]
    plan=dict(remove_tracks=sorted(remove),routes=[],fabrication_ready=False)
    router=ProposalRouter(g,checks,[40.5,75,56,105]);pads=router.pads
    for net,cap,pin in[("VBUS_USB","C5","13"),("VSYS","C7","10"),("VBAT","C8","2")]:
        router.add(plan,net,[pads[(cap,"1")]],[pads[("U3",pin)]],front=True)
    for ref in["C5","C7","C8"]:cap_ground(router,plan,ref)
    router.add(plan,"CHG_CE_N",[pads[("U3","4")]],[pads[("R10","1")]])
    for net,a,b in[("CHG_TMR",("U3","14"),("R83","1")),("CHG_STAT2",("U3","9"),("R12","2"))]:
        router.add(plan,net,[pads[a]],[pads[b]])
    output.write_text(json.dumps(plan,indent=2)+"\n")

def cleanup(native,output,seed):
    g=json.loads((native/"geometry.json").read_text());d=json.loads((native/"drc.json").read_text())
    items={t["uuid"]:t for t in g["tracks"]};remove=set();moves=[]
    for group in components(g):
        if not any("pos"in a and a["number"]and a["net"]for a in group):
            remove.update(a["uuid"]for a in group if "via"in a)
    for v in d["violations"]:
        if v["type"]in{"track_dangling","via_dangling"}:remove.update(i["uuid"]for i in v["items"])
        if v["type"]=="hole_to_hole":
            vs=[items[i["uuid"]]for i in v["items"]if i["uuid"]in items and items[i["uuid"]]["via"]]
            added=[a for a in vs if a["uuid"]not in seed]
            if not added:raise RuntimeError("Unreviewed existing-hole violation")
            new=added[0];other=next(a for a in vs if a["uuid"]!=new["uuid"])
            remove.add(new["uuid"])
            for t in g["tracks"]:
                if t["via"]or t["net"]!=new["net"]:continue
                if new["start"]not in[t["start"],t["end"]]:continue
                if new["net"]==other["net"]:
                    after=[other["start"]if q==new["start"]else q for q in[t["start"],t["end"]]]
                    if after[0]==after[1]:remove.add(t["uuid"])
                    else:moves.append(dict(uuid=t["uuid"],net=t["net"],before=[t["start"],t["end"]],after=after))
                else:remove.add(t["uuid"])
    plan=dict(remove_tracks=sorted(remove),move_tracks=[m for m in moves if m["uuid"]not in remove],routes=[],fabrication_ready=False)
    output.write_text(json.dumps(plan,indent=2)+"\n")
    return bool(remove or moves)

def repair(native,checks,output):
    g=json.loads((native/"geometry.json").read_text());by=collections.defaultdict(list)
    for group in components(g):
        if group and group[0]["net"]and not group[0]["net"].startswith("unconnected-"):by[group[0]["net"]].append(group)
    plan=dict(routes=[],remove_tracks=[],fabrication_ready=False)
    router=ProposalRouter(g,checks,[29,64,75,118],step=.1);r=router.r
    def pts(group):return np.array([q for a in group for q in([a["pos"]]if"pos"in a else[a["start"],a["end"]])])
    from scipy.spatial import cKDTree
    for net in["CHG_CE_N","GND","VBAT","VBUS_USB"]:
        groups=by[net]
        if len(groups)<2:continue
        if net=="GND":
            ep=router.pads[("U3","17")];main=next(q for q in groups if any(a["uuid"]==ep["uuid"]for a in q))
        else:main=max(groups,key=len)
        rest=[q for q in groups if q is not main];width=.2 if net in{"GND","CHG_CE_N"}else .3
        while rest:
            dist=[float(cKDTree(pts(main)).query(pts(q))[0].min())for q in rest];target=rest.pop(int(np.argmin(dist)))
            result,new=router.add(plan,net,[ep]if net=="GND"else main,target,width=width,timeout=50)
            main=main+target+new;output.write_text(json.dumps(plan,indent=2)+"\n")
    output.write_text(json.dumps(plan,indent=2)+"\n")
