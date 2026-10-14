"""Rebuild the R144 schematic proposal from the immutable R143 source.

This generates a proposal, not an accepted manufacturing release.  Run once
against a clean copy; the exact reference PCB hash prevents accidental reuse.
"""
from pathlib import Path
import hashlib,json,re,shutil,sys,uuid
repo=Path(__file__).resolve().parents[4]
base=repo/'hardware/mainboard/r143/kicad'; k=repo/'hardware/mainboard/r144/kicad'
assert not k.exists(), 'Refuse to overwrite an existing R144 source'
assert hashlib.sha256((base/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()=='3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266'
shutil.copytree(base,k)
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'enku-r144:'+s))
def blocks(t):
    """Top-level child spans, respecting quotes and escapes."""
    depth=0; quote=False; esc=False; start=None
    for i,c in enumerate(t):
        if quote:
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':quote=False
        elif c=='"':quote=True
        elif c=='(':
            if depth==1:start=i
            depth+=1
        elif c==')':
            depth-=1
            if depth==1 and start is not None:yield start,i+1,t[start:i+1]
def inst(t,ref):return next((a,b,x)for a,b,x in blocks(t)if x.startswith('(symbol (lib_id ')and '(property "Reference" "'+ref+'"'in x)
def prop(x,key,val):
    pat=r'(\(property "'+re.escape(key)+r'" )"(?:\\.|[^"\\])*"'
    if re.search(pat,x):return re.sub(pat,lambda m:m[1]+json.dumps(val),x,count=1)
    return x[:-1]+'\n(property '+json.dumps(key)+' '+json.dumps(val)+' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n)'
def label(net,x,y,tag):return f'(global_label "{net}" (shape input) (at {x:.6f} {y:.6f} 0) (effects (font (size .88 .88)) (justify right bottom)) (uuid "{uid(tag)}"))\n'
def insert_lib(t,s):
    a,b,x=next(z for z in blocks(t)if z[2].startswith('(lib_symbols'))
    return t[:b-1]+'\n'+s+'\n'+t[b-1:]
def change_label(t,id,net):
    a,b,x=next(z for z in blocks(t)if '(uuid "'+id+'")'in z[2]);return t[:a]+re.sub(r'^\(global_label "[^"]+"','(global_label "'+net+'"',x)+t[b:]
def update(t,ref,values):
    a,b,x=inst(t,ref)
    for key,v in values.items():x=prop(x,key,v)
    return t[:a]+x+t[b:]
fields={'U11':dict(Value='TPS389001DSER',Footprint='ENKU:TPS3890_TI_DSE0006A_SMD_LEFT',Datasheet='https://www.ti.com/lit/ds/symlink/tps3890.pdf',Description='R144 adjustable precision reset supervisor; R95/R96 sense; C40 delay; R17 pullup',MPN='TPS389001DSER',Manufacturer='Texas Instruments',Assembly='FIT'),
'R14':dict(Description='R144 upper feedback 27.4k plus R98 402R; PWM nominal 3.22035V'),
'R15':dict(Value='5.11k 0.1% 10ppm',MPN='RT0603BRB075K11L',Description='R144 feedback bottom 5.11k; PWM nominal 3.22035V'),
'C15':dict(Description='R144 local TPS389001 100nF supply bypass')}
pininfo=[('1','SENSE',-10.16,5.08,0,'input'),('2','GND',-10.16,0,0,'power_in'),('3','MR_N',-10.16,-5.08,0,'input'),('4','VDD',10.16,-5.08,180,'power_in'),('5','CT',10.16,0,180,'passive'),('6','RESET_N',10.16,5.08,180,'open_collector')]
lib='(symbol "ENKU:TPS3890" (pin_names (offset .7)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
for key,val in [('Reference','U'),('Value','TPS389001DSER'),('Footprint',fields['U11']['Footprint']),('Datasheet',fields['U11']['Datasheet'])]:lib+=f'(property "{key}" "{val}" (at 0 10 0) (effects (font (size .88 .88))))\n'
lib+='(symbol "TPS3890_0_1" (rectangle (start -7.62 7.62) (end 7.62 -7.62) (stroke (width .254) (type default)) (fill (type background))))\n(symbol "TPS3890_1_1"\n'
for num,name,x,y,ang,typ in pininfo:lib+=f'(pin {typ} line (at {x} {y} {ang}) (length 2.54) (name "{name}" (effects (font (size .88 .88)))) (number "{num}" (effects (font (size .88 .88)))))\n'
lib+='))'
sch=k/'mcu_io.kicad_sch';t=sch.read_text();a,b,old=inst(t,'U11');new=old.replace('ENKU:TLV803E','ENKU:TPS3890')
new=re.sub(r'\(pin "\d+" \(uuid "[^"]+"\)\)\s*','',new)
new=new.replace('(instances ',''.join(f'(pin "{q[0]}" (uuid "{uid("U11-pin"+q[0])}"))\n'for q in pininfo)+'(instances ')
for key,v in fields['U11'].items():new=prop(new,key,v)
t=t[:a]+new+t[b:]
remove={'d23aba9e-9501-59d4-9a09-e0b123105370','ee0781d1-5835-5868-9b8e-e8e6cae765c6','fbb7a594-411a-5b6f-9266-343a357f2716'}
for a,b,x in reversed(list(blocks(t))):
    if any('(uuid "'+u+'")'in x for u in remove):t=t[:a]+t[b:]
t=insert_lib(t,lib)
for pin,net in [('1','RESET_SENSE'),('2','GND'),('3','3V3_SYS'),('4','3V3_SYS'),('5','RESET_CT'),('6','ESP_EN')]:
    q=next(q for q in pininfo if q[0]==pin);t=t.rstrip()[:-1]+label(net,82.55+q[2],204.47-q[3],'U11-label'+pin)+')\n'
t=update(t,'C15',fields['C15']);sch.write_text(t)
sym=k/'ENKU.kicad_sym';v=sym.read_text();sym.write_text(v.rstrip()[:-1]+'\n'+lib.replace('"ENKU:TPS3890"','"TPS3890"',1)+'\n)\n')
power=k/'power.kicad_sch';t=power.read_text();t=change_label(t,'70000000-0000-4000-8000-000000000067','REG_MODE');t=change_label(t,'70000000-0000-4000-8000-000000009304','REG_FB_TOP')
for ref in ['R14','R15']:t=update(t,ref,fields[ref])
power.write_text(t)
spec={
'R95':('mcu_io','R90',[152.4,203.2],['3V3_SYS','RESET_SENSE'],'16.5k 0.1% 10ppm','RT0603BRB0716K5L','R14',[44.5,65.4]),
'R96':('mcu_io','R90',[152.4,226.06],['RESET_SENSE','GND'],'10k 0.1% 10ppm','RT0603BRB0710KL','R14',[41.5,66.5]),
'C40':('mcu_io','C15',[210.82,203.2],['RESET_CT','GND'],'100nF','CC0603KRX7R9BB104','C15',[46,71.2]),
'C41':('mcu_io','C15',[210.82,226.06],['RESET_SENSE','GND'],'1nF 50V','CC0603JRNPO9BN102','C39',[44.5,63.9]),
'R97':('power','R15',[345.44,223.52],['3V3_SYS','REG_MODE'],'0R','RC0603JR-070RL','R90',[56.5,97.2]),
'R98':('power','R15',[345.44,246.38],['3V3_SYS','REG_FB_TOP'],'402R 0.1% 10ppm','RT0603BRB07402RL','R14',[55.3,85.3]),
'R99':('power','R15',[345.44,269.24],['REG_MODE','GND'],'0R','RC0603JR-070RL','R67',[56.5,99.6])}
out={}
for ref,(sheet,template,xy,nets,value,mpn,fp_template,pos)in spec.items():
    s=k/(sheet+'.kicad_sch');t=s.read_text();_,_,old=inst(t,template);old_uuid=re.search(r'\(uuid "([^"]+)"\)',old)[1];new_uuid=uid(ref);m=re.search(r'\(at ([\d.]+) ([\d.]+) 0\)',old);dx,dy=xy[0]-float(m[1]),xy[1]-float(m[2])
    x=re.sub(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)',lambda m:f'(at {float(m[1])+dx:.6f} {float(m[2])+dy:.6f} {m[3]})',old)
    x=x.replace(old_uuid,new_uuid);x=re.sub(r'\(uuid "([^"]+)"\)',lambda m:'(uuid "'+(new_uuid if m[1]==new_uuid else uid(ref+m[1]))+'")',x);x=x.replace('(reference "'+template+'")','(reference "'+ref+'")')
    footprint='ENKU:'+('R_RT0603_YAGEO_REFLOW'if ref in ['R95','R96','R98']else 'R_RC0603_YAGEO_REFLOW'if ref=='R97'else 'R_RC0603_YAGEO_REFLOW_DNP'if ref=='R99'else 'C_CC0603_YAGEO_REFLOW_TRANSFER')
    # DNP footprint ID comes from the actual reviewed R67 library below.
    if ref=='R99':
        pcb=(base/'enku-mainboard-r0.1.kicad_pcb').read_text();footprint=re.search(r'\(footprint "([^"]+)"(?:(?!\n\t\(footprint ).)*?\(property "Reference" "R67"',pcb,re.S)[1]
    vals=dict(Reference=ref,Value=value,Footprint=footprint,MPN=mpn,Manufacturer='Yageo',Assembly='DNP'if ref=='R99'else'FIT',Description='R144 '+ref+' startup supply/reset circuit',Datasheet=('https://yageogroup.com/content/datasheet/asset/file/PYU-RT_1-TO-0-01_ROHS_L'if ref in ['R95','R96','R98']else'https://yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L'if ref in ['R97','R99']else'https://yageogroup.com/download/specsheet/'+mpn))
    if ref in ['R95','R96','R98']:vals['Tolerance']='0.1%';vals['TCR']='10ppm/K'
    if ref in ['R97','R99']:vals['Tolerance']='5%'
    for key,val in vals.items():x=prop(x,key,val)
    if ref=='R99':x=x.replace('(dnp no)','(dnp yes)')
    # Both passive symbol libraries have horizontal pins at +/-7.62 mm.
    t=t.rstrip()[:-1]+'\n'+x+'\n'+''.join(label(net,xy[0]+offset,xy[1],ref+'label'+str(n))for n,(net,offset)in enumerate(zip(nets,[-7.62,7.62])))+')\n';s.write_text(t)
    out[ref]=dict(symbol_uuid=new_uuid,values=vals,nets=dict(zip(['1','2'],nets)),template=fp_template,position_mm=pos,angle_deg=0,sheet=sheet)
for s in k.glob('*.kicad_sch'):s.write_text(s.read_text().replace('R143 - ENGINEERING / NO FAB','R144 - ENGINEERING / NO FAB'))
name='TPS3890_TI_DSE0006A_SMD_LEFT';f=f'(footprint "{name}" (version 20260101) (generator pcbnew) (layer "F.Cu") (attr smd)\n(property "Reference" "REF**" (at 0 -2 0) (layer "F.SilkS") (hide yes) (effects (font (size .8 .8))))\n(property "Value" "TPS389001DSER" (at 0 2 0) (layer "F.Fab") (hide yes) (effects (font (size .8 .8))))\n'
for layer,xa,ya,xb,yb,width in [('F.Fab',-.75,-.75,.75,.75,.1),('F.CrtYd',-1.25,-1.05,1.25,1.05,.05)]:f+=f'(fp_rect (start {xa} {ya}) (end {xb} {yb}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))\n'
f+='(fp_circle (center -1.35 -1.2) (end -1.25 -1.2) (stroke (width .1) (type default)) (fill none) (layer "F.SilkS"))\n'
for n,x,y,w in [('1',-.55,-.5,.9),('2',-.6,0,.8),('3',-.6,.5,.8),('4',.6,.5,.7),('5',.6,0,.7),('6',.6,-.5,.7)]:
    left=int(n)<=3;h=.35 if left else.25;layers='"F.Cu" "F.Mask"'if left else'"F.Cu" "F.Paste" "F.Mask"';ratio=.1/min(w,h)if left else.05/min(w,h)
    f+=f'(pad "{n}" smd roundrect (at {x} {y}) (size {w} {h}) (layers {layers}) (roundrect_rratio {ratio}) (solder_mask_margin {-.05 if left else .025}))\n'
    if left:f+=f'(pad "" smd roundrect (at {x} {y}) (size {w-.1:.6f} .25) (layers "F.Paste") (roundrect_rratio .2))\n'
f+=')\n';(k/'ENKU.pretty'/f'{name}.kicad_mod').write_text(f)
dru=k/'enku-mainboard-r0.1.kicad_dru';legacy="A.NetName =~ 'EPD_(GDR|RESE|VSH2|BS1|BUSY|RST_PANEL|DC_PANEL|CS_PANEL|SCLK_PANEL|MOSI_PANEL|VCI|VDD|VSH1|VGH|VSL|VGL|VCOM)'";exact='('+' || '.join("A.NetName == 'EPD_"+n+"'"for n in ['GDR','RESE','VSH2','BS1','BUSY','RST_PANEL','DC_PANEL','CS_PANEL','SCLK_PANEL','MOSI_PANEL','VCI','VDD','VSH1','VGH','VSL','VGL','VCOM'])+')';dru.write_text(dru.read_text().replace(legacy,exact)+'''\n# R144 TI DSE0006A OEM SMD lands: the two left-pad copper gaps are 0.15mm.\n# Restrict the exception to pad pairs inside U11, not any external copper.\n(rule "R144 U11 OEM SMD-defined left lands"\n (condition "A.Type == 'Pad' && B.Type == 'Pad' && A.memberOfFootprint('U11') && B.memberOfFootprint('U11')")\n (constraint clearance (min 0.15mm)))\n''')
(k.parent/'new_parts_R144.json').write_text(json.dumps(dict(new_parts=out,original_fields=fields),indent=2)+'\n')
print('R144 schematic proposal generated; native export/ERC and routing still required')
