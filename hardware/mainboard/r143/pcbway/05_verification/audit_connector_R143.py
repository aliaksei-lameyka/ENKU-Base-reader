"""Read-only, source-bound J3 audit against transcribed primary drawings.

Usage: audit_connector_R143.py KICAD_DIR VERIFIED_DIR OUTPUT_DIR [PASTE_GERBER]
Original supplier PDFs remain private; their hashes/pages are in the report.
Electrical/nominal land checks do not certify a folded flex or manufacturing.
"""
from pathlib import Path
import copy,csv,hashlib,json,math,re,sys,xml.etree.ElementTree as ET

PCB_SHA='3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266'
PANEL_NAMES=['NC','GDR','RESE','NC','VDHR/VSH2','NC','NC','BS1','BUSY_N','RST_N','DC','CSB','SCL','SDA','VDDIO','VCI','VSS','VDD','VPP (test)','VSH1','VGH','VSL','VGL','VCOM']
NETS={2:'EPD_GDR',3:'EPD_RESE',5:'EPD_VSH2',8:'EPD_BS1',9:'EPD_BUSY',10:'EPD_RST_PANEL',11:'EPD_DC_PANEL',12:'EPD_CS_PANEL',13:'EPD_SCLK_PANEL',14:'EPD_MOSI_PANEL',15:'3V3_SYS',16:'EPD_VCI',17:'GND',18:'EPD_VDD',20:'EPD_VSH1',21:'EPD_VGH',22:'EPD_VSL',23:'EPD_VGL',24:'EPD_VCOM'}
OPEN={1,4,6,7,19}

def sx(text):
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^()\s]+',text)
    stack=[];root=None
    for t in tokens:
        if t=='(':
            item=[]
            if stack:stack[-1].append(item)
            else:
                assert root is None,'Multiple roots';root=item
            stack.append(item)
        elif t==')':
            assert stack,'Unbalanced close';stack.pop()
        else:
            assert stack,'Atom outside root'
            stack[-1].append(json.loads(t) if t.startswith('"') else t)
    assert not stack,'Unclosed expression'
    return root

def children(a,key):return [x for x in a if isinstance(x,list) and x and x[0]==key]
def child(a,key):
    items=children(a,key);assert len(items)==1,(key,len(items));return items[0]
def near(a,b):return abs(a-b)<1e-7

def actual_paste(gbr):
    text=gbr.read_text();assert '%MOMM*%' in text and '%FSLAX46Y46*%' in text,'Unsupported export units/format'
    apertures={int(n):[float(a),float(b)] for n,a,b in re.findall(r'%ADD(\d+)R,([\d.]+)X([\d.]+)\*%',text)}
    component='';aperture=None;flashes=[]
    for line in text.splitlines():
        if line.startswith('%TO.C,'):component=line[6:-2]
        elif line=='%TD*%':component=''
        elif (m:=re.fullmatch(r'D(\d+)\*',line)):aperture=int(m[1])
        elif component=='J3' and (m:=re.fullmatch(r'X(-?\d+)Y(-?\d+)D03\*',line)):
            assert aperture in apertures,'J3 paste must be a rectangular aperture'
            flashes.append({'board_mm':[int(m[1])/1e6,-int(m[2])/1e6],'size_mm':apertures[aperture]})
    assert len(flashes)==26,'J3 must have 24 signal + 2 hold-down paste flashes'
    return flashes

def validate(m):
    assert m['mpn']=='FH34SRJ-24S-0.5SH(50)','J3 exact MPN'
    pads=m['pads'];sig={int(a['number']):a for a in pads if a['number'].isdigit()}
    assert set(sig)==set(range(1,25)),'24 unique numbered contacts'
    assert len([p for p in pads if p['number'].isdigit()])==24,'Duplicate contact'
    for i,p in sig.items():
        assert near(p['local'][0],5.75-(i-1)*.5) and near(p['local'][1],-1.25),f'Pin {i} location/orientation'
        assert all(near(a,b) for a,b in zip(p['size'],[.3,.8])),f'Pin {i} copper land'
        if i in NETS:assert p['net']==NETS[i],f'Pin {i} signal'
        else:
            assert i in OPEN and p['net'].startswith('unconnected-'),f'Pin {i} must remain open'
            # KiCad's PCB token uses {slash}; exported XML uses the literal slash.
            xml_name=p['net'].replace('{slash}','/')
            assert m['net_members'].get(xml_name)==[('J3',str(i))],f'Pin {i} open net is singleton'
            assert not any(t['net']==p['net'] for t in m['tracks']),f'Pin {i} open net has copper'
    for i in range(1,24):assert near(sig[i]['local'][0]-sig[i+1]['local'][0],.5),'Contact pitch'
    assert near(sig[1]['local'][0]-sig[24]['local'][0],11.5),'End-to-end span'
    for name,x in [('S1',6.75),('S2',-6.75)]:
        p=next(p for p in pads if p['number']==name)
        assert near(p['local'][0],x) and near(p['local'][1],1.25),'Hold-down centroid'
        assert p['net']=='GND','Hold-down net'
        assert p['size']==[.4,.8],'Hold-down copper must match Hirose'
    pp=[p for p in pads if not p['number'] and p['layers']==['F.Paste']]
    assert len(pp)==2 and all(p['size']==[.4,.8] for p in pp),'Hold-down paste must match Hirose'
    assert m['values']['R28']=='0R','VCI/VDDIO bridge'
    assert m['byref']['R28']=={'1':'3V3_SYS','2':'EPD_VCI'},'VCI/VDDIO bridge pin map'
    assert m['values']['R29']=='0R' and m['byref']['R29']=={'1':'EPD_BS1','2':'GND'},'4-wire SPI selection'
    assert m['byref']['C28']=={'1':'EPD_VSH2','2':'GND'},'Pin5 bypass wiring'
    assert m['values']['C28']=='4.7uF 25V','Pin5 bypass nominal value'
    return sig

def main():
    k,v,out=map(Path,sys.argv[1:4]);out.mkdir(parents=True,exist_ok=True)
    pcb=k/'enku-mainboard-r0.1.kicad_pcb'
    assert hashlib.sha256(pcb.read_bytes()).hexdigest()==PCB_SHA,'Source changed since native verification'
    board=sx(pcb.read_text());footprints=children(board,'footprint')
    f=next(f for f in footprints if any(p[1:3]==['Reference','J3'] for p in children(f,'property')))
    origin=[float(x) for x in child(f,'at')[1:3]]
    assert len(child(f,'at'))==3 or near(float(child(f,'at')[3]),0),'Unmirrored J3 rotation'
    props={p[1]:p[2] for p in children(f,'property')}
    pads=[]
    for p in children(f,'pad'):
        net=children(p,'net')
        pads.append({'number':p[1],'local':[float(x) for x in child(p,'at')[1:3]],'size':[float(x) for x in child(p,'size')[1:3]],'net':net[0][-1] if net else '', 'layers':child(p,'layers')[1:], 'paste_margin':float(children(p,'solder_paste_margin')[0][1]) if children(p,'solder_paste_margin') else 0,'paste_ratio':float(children(p,'solder_paste_margin_ratio')[0][1]) if children(p,'solder_paste_margin_ratio') else 0})
    g=json.loads((v/'geometry.json').read_text())
    native=[p for p in g['pads'] if p['ref']=='J3'];assert len(native)==len(pads)
    for p in pads:
        pos=[a+b for a,b in zip(origin,p['local'])]
        assert any(n['number']==p['number'] and n['net']==p['net'] and all(near(a,b) for a,b in zip(n['pos'],pos)) and n['size']==p['size'] for n in native),'Raw PCB/native export consistency'
    root=ET.parse(v/'netlist.xml').getroot();net_members={};byref={}
    for n in root.findall('./nets/net'):
        name=n.get('name');members=[(a.get('ref'),a.get('pin')) for a in n.findall('node')];net_members[name]=members
        for ref,pin in members:byref.setdefault(ref,{})[pin]=name
    values={a.get('ref'):a.findtext('value') for a in root.findall('./components/comp')}
    m={'mpn':props['MPN'],'pads':pads,'tracks':g['tracks'],'net_members':net_members,'byref':byref,'values':values}
    sig=validate(m)
    gbr=Path(sys.argv[4]) if len(sys.argv)==5 else k.parent/'pcbway/01_fabrication/gerber/enku-mainboard-r0.1-F_Paste.gbr'
    flashes=actual_paste(gbr)
    expected_paste=[]
    for p in pads:
        if 'F.Paste' not in p['layers']:continue
        size=[x*(1+2*p['paste_ratio'])+2*p['paste_margin'] for x in p['size']]
        expected_paste.append({'board_mm':[a+b for a,b in zip(origin,p['local'])],'size_mm':size})
        assert any(all(near(a,b) for a,b in zip(f['board_mm'],expected_paste[-1]['board_mm'])) and all(near(a,b) for a,b in zip(f['size_mm'],size)) for f in flashes),'Source/paste Gerber mismatch'
        if p['number'].isdigit():assert all(near(a,b) for a,b in zip(size,[.25,.65])),'Numbered paste must match OEM'
    assert len(expected_paste)==len(flashes)
    fixtures={}
    mutations={
       'all_24_nets_reversed':lambda q:[p.update(net=next(s['net'] for s in pads if s['number']==str(25-int(p['number'])))) for p in q['pads'] if p['number'].isdigit()],
       'pin5_to_ground':lambda q:next(p for p in q['pads'] if p['number']=='5').update(net='GND'),
       'NC6_to_signal':lambda q:next(p for p in q['pads'] if p['number']=='6').update(net='EPD_BUSY'),
       'pad1_mirrored':lambda q:next(p for p in q['pads'] if p['number']=='1').update(local=[-5.75,-1.25]),
       'contact_pitch_slip':lambda q:next(p for p in q['pads'] if p['number']=='12').update(local=[.35,-1.25]),
       'hold_down_centroid_shift':lambda q:next(p for p in q['pads'] if p['number']=='S1').update(local=[6.85,1.25]),
       'oversized_hold_down_copper':lambda q:next(p for p in q['pads'] if p['number']=='S1').update(size=[.8,.8]),
       'oversized_hold_down_paste':lambda q:next(p for p in q['pads'] if not p['number'] and p['layers']==['F.Paste']).update(size=[.8,.65]),
       'VCI_bridge_absent':lambda q:q['values'].update(R28='DNP'),
       'BS1_not_low':lambda q:q['byref']['R29'].update({'2':'3V3_SYS'}),
    }
    for name,mutate in mutations.items():
        q=copy.deepcopy(m);mutate(q)
        assert q!=m,'Ineffective fault fixture'
        try:validate(q)
        except AssertionError as e:fixtures[name]={'detected':True,'reason':str(e)}
        else:raise AssertionError('Fault escaped: '+name)
    rows=[]
    for i,p in sorted(sig.items()):rows.append([i,PANEL_NAMES[i-1],p['net'],origin[0]+p['local'][0],origin[1]+p['local'][1],'PASS / open' if i in OPEN else 'PASS'])
    with (out/'J3_pin_map_R143.csv').open('w',newline='') as fcsv:
        w=csv.writer(fcsv);w.writerow(['Pin','Panel designation pp5-6','Actual PCB net','Board X mm','Board Y mm','Electrical result']);w.writerows(rows)
    hold=[p for p in pads if p['number'] in ['S1','S2']]
    paste=[p for p in pads if not p['number'] and p['layers']==['F.Paste']]
    # OEM E/F dimensions are the inner/outer hold-down edges, not centroids.
    assert near((13.9-13.1)/2,.4) and near((13.9+13.1)/4,6.75)
    thickness={'panel_mm':[.25,.35],'Hirose_spec_mm':[.27,.33],'nominal_match':True,'full_panel_tolerance_contained':False,'excess_each_end_mm':.02}
    width={'panel_mm':[12.4,12.6],'Hirose_recommended_FPC_mm':[12.45,12.55],'nominal_match':True,'full_panel_tolerance_contained':False,'recommendation_not_a_guaranteed_cavity_limit':True}
    record={'revision':'R143','source_parent_commit':'5be2afb9341840aecfc660ee920f26d113b0de18','pcb_sha256':PCB_SHA,'source_unchanged':True,'electrical_24_contacts_passed':True,'NC_1_4_6_7_and_test_19_open':True,'VCI_VDDIO_link':'R28 0R','four_wire_SPI_selection':'R29 0R to GND','pin5':'VDHR and VSH2 equivalent per Felix 2026-10-10; J3.5 -> C28 4.7uF/25V -> GND','contacts':'Top and bottom; actual folded pin1 alignment not certified','J3_board_origin_mm':origin,'pad1_board_mm':[origin[0]+5.75,origin[1]-1.25],'pad24_board_mm':[origin[0]-5.75,origin[1]-1.25],'numbered_copper_lands_mm':[.3,.8],'numbered_paste_apertures_mm':[.25,.65],'manufacturer_numbered_lands_match':True,'hold_down_centroids_match':True,'hold_down_copper_OEM_mm':[.4,.8],'hold_down_copper_actual_mm':[p['size'] for p in hold],'hold_down_paste_OEM_mm':[.4,.8],'hold_down_paste_actual_mm':[p['size'] for p in paste],'hold_down_copper_and_paste_match_OEM':True,'thickness':thickness,'tongue_width':width,'pin_pitch_nominal_mm':.5,'pin1_to_pin24_span_nominal_mm':11.5,'panel_unsupported_width_or_thickness_is_not_proven_failure':True,'supplier_bend_radius_mm':[1,1.5],'design_bend_radius_min_mm':1.5,'supplier_glass_to_bend_clearance_min_mm':2,'DIANWEI_is_not_Hirose_drop_in':True,'DIANWEI_recommended_FPC_thickness_mm':[.28,.32],'remaining_HOLD':['Guaranteed production FPC thickness/width or written Hirose acceptance','Actual folded pin1-to-pin1 pose, insertion/coverlay/stiffener and actuator access','GDEM CAD vs GDEY panel variant identity and case registration','Common stencil/reflow/connector assembly process acceptance','Real panel startup/refresh/HV and combined-load tests'],'physical_tests':'NOT RUN','fabrication_release':'NO FAB','fault_fixtures':fixtures,'primary_sources':{'panel':{'SHA256':'e28ea298457108bb3431b8c4de065834f62390b6caf2dc58e216d134fe559dbc','pages':[5,6,19]},'GoodDisplay_connector':{'SHA256':'c2d1760728c3b14170a0500a0b63d12b7317848b2ed8e7026d266a98cd9a07ed','page':1,'part':'DIANWEI 8.21A0.024200'},'Hirose_drawing':{'drawing':'EDC-159714-50-08','pages':[1,2,4]},'Hirose_spec':{'spec':'ELC4-159714-04','pages':[1,2]},'supplier_email':{'date':'2026-10-10','url':'https://mail.google.com/mail/u/?authuser=aliaksei.lameyka%40gmail.com#all/1a1244f1a3c71a96'}}}
    record['actual_paste_Gerber_checked']=True
    record['paste_Gerber_sha256']=hashlib.sha256(gbr.read_bytes()).hexdigest()
    record['J3_paste_flash_count']=len(flashes)
    record['primary_sources']['Hirose_drawing']['SHA256']='7f66a5ac31dad33a8be59bcd17cb3defd6a977ed2ba90b8d26b12f4031024990'
    record['primary_sources']['Hirose_spec']['SHA256']='606666ad7c738122fb0656b18423191499fc7fede416fc713e4c395fbb04ecb5'
    (out/'FPC_connector_audit_R143.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    print('J3: 24 pin mappings, nominal numbered copper lands and centroids PASS; 10 effective design-fault fixtures detected; physical/DFM qualification HOLD.')

if __name__=='__main__':main()
