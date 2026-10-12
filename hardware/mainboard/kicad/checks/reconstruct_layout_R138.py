"""Explicit local preparation of the exact R138 layout; never a CI repair.

The coordinates below retain the successful pre-outage native pass. The seed
is immutable R137. Both initial dense-via detection and the final physical
checks must run in real SHA-pinned KiCad10.0.7. No manufacture is authorized.
"""
import collections,copy,gzip,hashlib,json,os,re,subprocess,sys,uuid
from pathlib import Path

SEED_SHA='99f2d9cff7a79cc9347f2430d422493e512e6c3b6d6cf82ffd408e0dd77db798'
MOVES=[
 ('GND',[52.,44.2],[51.375,44.2]),
 ('GND',[52.5,45.],[51.725,45.45]),
 ('GND',[27.245,54.245],[27.12,54.87]),
 ('SPI_SCLK',[36.5,28.3],[36.8,28.375]),
 ('GND',[65.1,94.],[65.,94.3]),
 ('EPD_VCI',[63.3,47.7],[63.05,47.525]),
 ('GND',[31.25,80.9],[31.025,81.125]),
 ('EPD_VGL',[49.85,48.75],[49.7,48.9]),
 ('EPD_DC',[44.5,41.8],[44.325,41.8]),
 ('SPI_MISO',[30.75,109.25],[30.75,109.125]),
 ('3V3_SYS',[62.2,67.75],[62.3,67.75]),
 ('GND',[38.65,80.],[38.65,79.925]),
 ('3V3_SYS',[29.,70.6],[29.025,70.65]),
 ('CHG_CE_CMD',[52.2,76.3],[52.175,76.3]),
 ('CHG_EN2',[56.9,85.7],[56.875,85.7]),
]
STUB_MOVES=[
 ('EPD_DC',[40.5,28.3],[40.775,28.275]),
 ('GND',[59.5,69.],[59.625,68.625]),
 ('GND',[31.,60.],[31.,60.125]),
 ('3V3_SYS',[32.5,61.7],[32.45,61.725]),
]
GEOMETRY_OVERRIDES={
 'c81f7148-d923-4f8b-bc5b-519932063160':(.6,.3),
 'd38f9dbe-e9a9-402e-8fc9-99e6f6c45819':(.6,.3),
 'ff4eba1c-e6fa-478a-9508-9d31da0b459a':(.6,.3),
 '3170d571-6923-486d-97de-ef4f8c3c5fea':(.5,.2),
 '2a26c8d7-d2eb-4047-ad39-9e12c1a5a510':(.5,.2),
 '4bbddcd6-85df-401a-aede-632602bbcbb4':(.5,.2),
}
REMOVE={'0af5e901-919c-47a9-8fae-9b1c57dd256a',
        'aea1280e-d2ec-4ae2-a9cb-7207a1b76182',
        '39ce2de7-a965-4c3b-b43a-ae830d3138fd'}
LAYERS={0:'F.Cu',2:'B.Cu',4:'In1.Cu',6:'In2.Cu'}
TRACK_PATTERN=re.compile(r'^\t\((?:via|segment)\n.*?^\t\)\n',re.M|re.S)

def number(value):return f'{value:.6f}'.rstrip('0').rstrip('.')
def block_uid(block):return re.search(r'\(uuid "([^"]+)"\)',block)[1]
def blocks(source):return {block_uid(m[0]):m[0]for m in TRACK_PATTERN.finditer(source)}
def change_field(block,field,values):
    replacement='('+field+' '+' '.join(number(x)for x in values)+')'
    block,n=re.subn(r'\('+re.escape(field)+r' [^\)]*\)',lambda m:replacement,block,count=1)
    assert n==1,(field,block_uid(block))
    return block
def segment(uid,net,layer,width,start,end):
    return '\t(segment\n\t\t(start '+ ' '.join(map(number,start))+')\n\t\t(end '+ ' '.join(map(number,end))+')\n\t\t(width '+number(width)+')\n\t\t(layer "'+LAYERS[layer]+'")\n\t\t(net '+json.dumps(net)+')\n\t\t(uuid "'+uid+'")\n\t)\n'

def run(root,output):
    if os.environ.get('GITHUB_ACTIONS')=='true':raise SystemExit('CI may not reconstruct or repair its verification source')
    root,output=Path(root).resolve(),Path(output).resolve();output.mkdir(parents=True,exist_ok=True);checks=root/'checks'
    app=Path(os.environ['ENKU_KICAD_APP']);pcb=root/'enku-mainboard-r0.1.kicad_pcb';pro=root/'enku-mainboard-r0.1.kicad_pro'
    assert hashlib.sha256(pcb.read_bytes()).hexdigest()==SEED_SHA,'Only the immutable accepted R137 seed may be prepared'
    version=subprocess.check_output([str(app),'kicad-cli','version']).decode().strip();assert version=='10.0.7'
    os.environ['KIPRJMOD']=str(root)
    source=pcb.read_text();old=json.loads(gzip.decompress((checks/'geometry_checkpoint_R137.json.gz').read_bytes()))
    geometry={x['uuid']:copy.deepcopy(x)for x in old['tracks']};via={u:t for u,t in geometry.items()if t['via']}
    assert len(via)==330 and len(geometry)==3707
    data=blocks(source);assert data.keys()==geometry.keys()
    under_EP=json.loads((checks/'thermal_via_manifest_R136.json').read_text())['added_vias'];thermal_ids={x['uuid']for x in under_EP}
    grown={u for u,t in via.items()if t['width']==.5 and t['drill']==.3};assert len(grown)==165
    for u in grown:data[u]=change_field(data[u],'size',[.6])
    for u in thermal_ids:
        x,y=via[u]['start']
        if [x,y]!=[48.5,91.]:data[u]=change_field(data[u],'at',[48.5+(.53 if x>48.5 else-.53),91.+(.53 if y>91. else-.53)])
    source=TRACK_PATTERN.sub(lambda m:data[block_uid(m[0])],source).replace('R137 - ENGINEERING / NO FAB','R138 - ENGINEERING / NO FAB')
    pcb.write_text(source)
    settings=json.loads(pro.read_text());settings['board']['design_settings']['rules']['min_via_annular_width']=.15
    pro.write_text(json.dumps(settings,indent=2)+'\n')
    def drc(name):
        project=pro.read_bytes()
        try:
            subprocess.run([str(app),'kicad-cli','pcb','drc','--severity-all','--all-track-errors','--schematic-parity','--refill-zones','--save-board','--format','json','--output',str(output/name),str(pcb)],check=True)
        finally:pro.write_bytes(project)
        return json.loads((output/name).read_text())
    first=drc('drc_initial_growth_R138.json')
    dense={i['uuid']for finding in first['violations']for i in finding['items']if i['uuid']in grown}
    assert len(dense)==82 and collections.Counter(x['type']for x in first['violations'])=={'clearance':461},'The pinned native dense-via detection differs from the retained pass'
    assert not first['unconnected_items']and not first['schematic_parity']
    source=pcb.read_text();data=blocks(source)
    for u in dense:data[u]=change_field(change_field(data[u],'size',[.5]),'drill',[.2])
    for u,(width,drill)in GEOMETRY_OVERRIDES.items():data[u]=change_field(change_field(data[u],'size',[width]),'drill',[drill])
    for u,t in via.items():
        t['width']=float(re.search(r'\(size ([^\)]+)\)',data[u])[1]);t['drill']=float(re.search(r'\(drill ([^\)]+)\)',data[u])[1])
    def get_via(net,position):
        matches=[t for t in via.values()if t['net']==net and t['start']==position];assert len(matches)==1,(net,position)
        return matches[0]
    move_records=[];new_segments={}
    for net,before,after in MOVES:
        v=get_via(net,before);u=v['uuid'];data[u]=change_field(data[u],'at',after);changed=[]
        for t in geometry.values():
            if t['via']or t['net']!=net:continue
            for field in ['start','end']:
                if t[field]==before:data[t['uuid']]=change_field(data[t['uuid']],field,after);t[field]=list(after);changed.append(t['uuid'])
        v['start']=list(after);v['end']=list(after);move_records.append(dict(uuid=u,net=net,before=before,after=after,changed_segments=sorted(set(changed))))
    for net,before,after in STUB_MOVES:
        v=get_via(net,before);u=v['uuid'];data[u]=change_field(data[u],'at',after)
        attached=[t for t in geometry.values()if not t['via']and t['net']==net and(t['start']==before or t['end']==before)]
        widths={t['layer']:max(x['width']for x in attached if x['layer']==t['layer'])for t in attached}
        for layer,width in widths.items():
            su=str(uuid.uuid5(uuid.NAMESPACE_URL,'ENKU/R138/wick-stub/'+u+'/'+str(layer)));new_segments[su]=segment(su,net,layer,width,before,after)
        v['start']=list(after);v['end']=list(after);move_records.append(dict(uuid=u,net=net,before=before,after=after,retained_old_junctions=True,stub_layers=sorted(widths)))
    data['d3e13750-f122-4e4d-81aa-11c5973f0236']=change_field(data['d3e13750-f122-4e4d-81aa-11c5973f0236'],'end',[28.,80.112])
    u='3170d571-6923-486d-97de-ef4f8c3c5fea';data[u]=change_field(data[u],'at',[62.325,48.125]);assert '(tenting'not in data[u]
    data[u]=data[u].replace('\t\t(net ','\t\t(tenting\n\t\t\t(front no)\n\t\t\t(back yes)\n\t\t)\n\t\t(capping yes)\n\t\t(filling yes)\n\t\t(net ',1)
    su=str(uuid.uuid5(uuid.NAMESPACE_URL,'ENKU/R138/R28-filled-cap-B-short-connection'));new_segments[su]=segment(su,'3V3_SYS',2,.2,[62.7,48.2],[62.325,48.125])
    su=str(uuid.uuid5(uuid.NAMESPACE_URL,'ENKU/R138/J1-ground-explicit-F-return'));new_segments[su]=segment(su,'GND',0,.4,[65.6,93.8],[65.,94.3]);assert len(new_segments)==8
    for u in REMOVE:assert u in data
    source=TRACK_PATTERN.sub(lambda m:''if block_uid(m[0])in REMOVE else data[block_uid(m[0])],source).rstrip()
    assert source.endswith(')');pcb.write_text(source[:-1]+''.join(new_segments.values())+')\n')
    settings['board']['design_settings']['rules']['min_through_hole_diameter']=.2;pro.write_text(json.dumps(settings,indent=2)+'\n')
    rules=root/'enku-mainboard-r0.1.kicad_dru';text=rules.read_text();a=text.index('# USB4105 manufacturer-defined geometry:');b=text.index('# Three compact right-edge');text=text[:a]+text[b:]
    text=text.replace('(constraint hole_size (min 0.30mm))','(constraint hole_size (min 0.20mm))').replace('# R0.1 production preference: use comfortable geometry by default.','# R138 uses0.60/0.30mm or0.50/0.20mm vias with0.15mm nominal rings.\n# Exact reviewed0.20mm bore UUIDs and nominal aspect8 are guarded independently;\n# fabrication must accept finished thickness/drill/registration/plating tolerances.\n# R0.1 production preference: use comfortable geometry by default.');rules.write_text(text)
    final=drc('drc_final_layout_R138.json');assert not final['violations']and not final['unconnected_items']and not final['schematic_parity']
    subprocess.run([str(app),'kicad-cli','sch','erc','--severity-all','--format','json','--output',str(output/'erc_R138.json'),str(root/'enku-mainboard-r0.1.kicad_sch')],check=True)
    erc=json.loads((output/'erc_R138.json').read_text());assert not any(x['violations']for x in erc['sheets'])
    subprocess.run([str(app),'python3.11',str(checks/'native_board.py'),'export',str(pcb),str(output/'geometry_R138.json')],check=True)
    subprocess.run([str(app),'python3.11',str(checks/'export_via_process_R133.py'),str(pcb),str(output/'via_process_R138.json')],check=True)
    g=json.loads((output/'geometry_R138.json').read_text());process={v['uuid']:v for v in json.loads((output/'via_process_R138.json').read_text())['vias']}
    from pad_groups import partitions
    assert partitions(g)==partitions(old),'Any formerly connected pad group split'
    assert g['pads']==old['pads']and g['footprints']==old['footprints']and g['zones']==old['zones']and g['board_outline']==old['board_outline']and g['bbox']==old['bbox']
    assert len(g['tracks'])==3712 and sum(t['via']for t in g['tracks'])==329 and len(g['pads'])==438 and len(g['footprints'])==127
    from shapely.geometry import Point,Polygon
    from shapely import union_all
    smd=[p for p in g['pads']if p['attribute']==1 and p['number']];lands=union_all([Polygon(q)for p in smd for ps in p['polygons'].values()for q in ps]);new_vias={v['uuid']:v for v in g['tracks']if v['via']}
    caps=thermal_ids|{'3170d571-6923-486d-97de-ef4f8c3c5fea'}
    assert {u for u,p in process.items()if p['fill_requested']or p['cap_requested']}==caps
    for u in caps:
        p=process[u];v=new_vias[u];ref,pin=('U3','17')if u in thermal_ids else('R28','1');pad=next(p for p in smd if p['ref']==ref and p['number']==pin);shape=union_all([Polygon(q)for q in pad['polygons']['0']])
        assert shape.covers(Point(v['start']).buffer(v['width']/2,quad_segs=128)) and p['fill_requested']and p['cap_requested']and not p['front_tented']and p['back_tented']
    gaps=[lands.distance(Point(v['start']))-v['width']/2 for u,v in new_vias.items()if u not in caps];assert len(gaps)==323 and min(gaps)>=.1-1e-6
    rings=collections.Counter(round((v['width']-v['drill'])/2,6)for v in new_vias.values());assert rings=={.15:241,.2:88}
    variants=collections.Counter((v['width'],v['drill'])for v in new_vias.values());assert variants=={(.7,.3):88,(.6,.3):156,(.5,.2):85}
    summary=dict(revision='R138',pcb_sha256=hashlib.sha256(pcb.read_bytes()).hexdigest(),seed_R137_sha256=SEED_SHA,native_kicad=version,DRC=0,ERC=0,opens=0,parity=0,native_vias=329,copper_items=3712,pads=438,placements=127,old_pad_partitions_and_all_placements_fields_outline_and_zone_parameters_preserved=True,ordinary_vias=323,ordinary_minimum_SMD_gap_mm=min(gaps),all_nominal_rings_at_least_mm=.15,filled_capped_requests=6,bores_0_20mm_count=85,initial_native_clearance_findings=461,dense_bore_UUIDs=sorted(dense),exact_19_ordinary_via_moves=move_records,nominal_board_thickness_mm=1.6,full_independent_audit_and_immutable_checkpoint_preparation='PENDING',factory_approval=False,physical_qualification='NOT RUN',fabrication_ready=False)
    (output/'layout_preparation_R138.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
    return summary

if __name__=='__main__':run(*sys.argv[1:])
