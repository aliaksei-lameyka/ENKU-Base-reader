"""R143 explicit scope, adapted from audit_active_IC_R136.py; original unchanged."""
"""Independent top-view land/pin/interface review of six active ICs.

Constants are transcribed from the primary manufacturer PDFs listed in
manufacturer_reference_manifest_R136.json, not from the generated libraries.
U1 is covered separately by the U1/reserved-pin/EP and USB source guards.
"""
import hashlib,json,math,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
af=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R136.json').read_text())
ap={x['uuid']:x for x in af['pads']};fps={x['ref']:x for x in af['footprints']};groups=partitions(g)
xml=ET.parse(out/'netlist.xml' if server else c/'netlist_R136.xml');comps={x.attrib['ref']:x for x in xml.findall('./components/comp')}
pins={
 'U3': {'1': (-1.4, -0.75, 0.6, 0.24, 'CHG_TS'), '2': (-1.4, -0.25, 0.6, 0.24, 'VBAT'), '3': (-1.4, 0.25, 0.6, 0.24, 'VBAT'), '4': (-1.4, 0.75, 0.6, 0.24, 'CHG_CE_N'), '5': (-0.75, 1.4, 0.24, 0.6, 'CHG_EN2'), '6': (-0.25, 1.4, 0.24, 0.6, 'CHG_EN1'), '7': (0.25, 1.4, 0.24, 0.6, 'CHG_STAT1'), '8': (0.75, 1.4, 0.24, 0.6, 'GND'), '9': (1.4, 0.75, 0.6, 0.24, 'CHG_STAT2'), '10': (1.4, 0.25, 0.6, 0.24, 'VSYS'), '11': (1.4, -0.25, 0.6, 0.24, 'VSYS'), '12': (1.4, -0.75, 0.6, 0.24, 'CHG_ILIM_VSET'), '13': (0.75, -1.4, 0.24, 0.6, 'VBUS_USB'), '14': (0.25, -1.4, 0.24, 0.6, 'CHG_TMR'), '15': (-0.25, -1.4, 0.24, 0.6, 'GND'), '16': (-0.75, -1.4, 0.24, 0.6, 'CHG_ISET'), '17': (0, 0, 1.68, 1.68, 'GND')},
 'U4': {'1':(-.9,-1,.6,.25,'SYS_EN'),'2':(-.9,-.5,.6,.25,'GND'),
        '3':(-.9,0,.6,.25,'GND'),'4':(-.9,.5,.6,.25,'REG_FB'),
        '5':(-.9,1,.6,.25,'REG_PG'),'6':(.75,1,.9,.25,'3V3_SYS'),
        '7':(.75,.5,.9,.25,'REG_L2'),'8':(.55,0,1.3,.25,'GND'),
        '9':(.75,-.5,.9,.25,'REG_L1'),'10':(.75,-1,.9,.25,'SYS_EN')},
 'U5': {'1':(-1.2625,-.75,.675,.25,'GND'),'2':(-1.2625,-.25,.675,.25,None),
        '3':(-1.2625,.25,.675,.25,None),'4':(-1.2625,.75,.675,.25,'IMU_INT1'),
        '5':(-.5,1.0125,.25,.675,'3V3_SYS'),'6':(0,1.0125,.25,.675,'GND'),
        '7':(.5,1.0125,.25,.675,'GND'),'8':(1.2625,.75,.675,.25,'3V3_SYS'),
        '9':(1.2625,.25,.675,.25,None),'10':(1.2625,-.25,.675,.25,None),
        '11':(1.2625,-.75,.675,.25,None),'12':(.5,-1.0125,.25,.675,'3V3_SYS'),
        '13':(0,-1.0125,.25,.675,'I2C_SCL'),'14':(-.5,-1.0125,.25,.675,'I2C_SDA')},
 'U8': {'1':(-1.15,-.95,1.2,.6,'USB_DP_CONN'),'2':(-1.15,0,1.2,.6,'GND'),
        '3':(-1.15,.95,1.2,.6,'USB_DM_CONN'),'4':(1.15,.95,1.2,.6,'USB_DM_CONN'),
        '5':(1.15,0,1.2,.6,'VBUS_USB'),'6':(1.15,-.95,1.2,.6,'USB_DP_CONN')},
 'U9': {'1':(-1.3,-.95,1.1,.6,'BAT_ADC_SW'),'2':(-1.3,0,1.1,.6,'VBAT'),
        '3':(-1.3,.95,1.1,.6,'GND'),'4':(1.3,.95,1.1,.6,'3V3_SYS'),
        '5':(1.3,-.95,1.1,.6,'VBAT')},
 'U11':{'1':(-1.05,-.95,1.3,.6,'GND'),'2':(-1.05,.95,1.3,.6,'ESP_EN'),'3':(1.05,0,1.3,.6,'3V3_SYS')},
 'U10':{'1':(-1.3,-.95,1.1,.6,'USB_VBUS_VALID'),'2':(-1.3,0,1.1,.6,'GND'),
        '3':(-1.3,.95,1.1,.6,'USB_VBUS_DIV'),'4':(1.3,.95,1.1,.6,'USB_VBUS_REF'),
        '5':(1.3,0,1.1,.6,'USB_VBUS_REF'),'6':(1.3,-.95,1.1,.6,'3V3_SYS')},
}
parts={'U3':('BQ24072TRGTR','Texas Instruments'),'U4':('TPS63802DLAR','Texas Instruments'),
       'U11':('TLV803EA30DBZR','Texas Instruments'),
 'U5':('BMI270','Bosch Sensortec'),'U8':('USBLC6-2SC6','STMicroelectronics'),
       'U9':('TMUX1101DBVR','Texas Instruments'),'U10':('TLV3012BIDBVR','Texas Instruments')}
nodes={(x.attrib['ref'],x.attrib['pin']):n.attrib['name'] for n in xml.findall('./nets/net') for x in n.findall('node')}
node_groups={n.attrib['name']:{(x.attrib['ref'],x.attrib['pin']) for x in n.findall('node')} for n in xml.findall('./nets/net')}
checked=0
for ref,expected in pins.items():
    fp=g['footprints'][ref];theta=math.radians(fp['angle']);cx,cy=fp['pos']
    actual={a['number']:a for a in g['pads'] if a['ref']==ref and a['number']}
    assert actual.keys()==expected.keys();assert fps[ref]['attributes']==2 and not fps[ref]['dnp']
    fields=fps[ref]['fields'];assert (fields['MPN'],fields['Manufacturer'])==parts[ref]
    sf={a.attrib['name']:a.text or '' for a in comps[ref].findall('./fields/field')}
    assert (sf['MPN'],sf['Manufacturer'])==parts[ref] and comps[ref].findtext('footprint')==fp['lib']
    for number,(x,y,w,h,net) in expected.items():
        a=actual[number];q=ap[a['uuid']]
        pos=[round(cx+math.cos(theta)*x+math.sin(theta)*y,6),round(cy-math.sin(theta)*x+math.cos(theta)*y,6)]
        assert a['pos']==pos and a['size']==[w,h] and not max(a['drill']),(ref,number,'Wrong primary top-view land')
        assert a['attribute']==1 and a['layers']==[0]
        if net is None:
            assert a['net'].startswith('unconnected-') and nodes[(ref,number)]==a['net']
            assert node_groups[a['net']]=={(ref,number)} and not any(t['net']==a['net'] for t in g['tracks']),(ref,number,'DNC pin used')
        else:
            assert a['net']==nodes[(ref,number)]==net,(ref,number,'Native PCB/schematic pin-map mismatch')
            assert len(groups[net])==1 and a['uuid'] in groups[net][0],(ref,number,'Split native copper group')
        assert {'F.Cu','F.Mask'}<=set(q['layers'])
        checked+=1
assert checked==61
def two(ref,a,b,value):
    pads={p['number']:p['net'] for p in g['pads'] if p['ref']==ref and p['number']}
    assert pads=={'1':a,'2':b} and fps[ref]['value']==value,(ref,'Wrong support network')
for args in [('R8','CHG_ILIM_VSET','GND','3.48k 1%'),('R9','CHG_ISET','GND','2k 1%'),
             ('R10','CHG_CE_N','GND','100k'),('R11','3V3_SYS','CHG_STAT1','10k'),
             ('R14','3V3_SYS','REG_FB','27.4k 0.1% 10ppm'),('R15','REG_FB','GND','4.99k 0.1% 10ppm'),
             ('R16','3V3_SYS','REG_PG','100k'),('R24','3V3_SYS','I2C_SDA','4.7k'),
             ('R25','3V3_SYS','I2C_SCL','4.7k'),('R26','BAT_ADC_SW','BAT_ADC','2M 1%'),
             ('R27','BAT_ADC','GND','680k 1%')]:two(*args)
bypass={}
for ref,net,value in [('C5','VBUS_USB','4.7uF 25V'),('C7','VSYS','22uF 10V'),
                      ('C8','VBAT','22uF 10V'),('C9','SYS_EN','22uF 10V'),
                      ('C10','SYS_EN','100nF'),('C11','3V3_SYS','22uF 10V'),
                      ('C12','3V3_SYS','22uF 10V'),('C15','3V3_SYS','100nF'),('C18','3V3_SYS','100nF'),
                      ('C19','3V3_SYS','100nF'),('C37','VBAT','100nF 10V'),
                      ('C38','3V3_SYS','100nF 10V')]:
    two(ref,net,'GND',value);bypass[ref]=dict(net=net,value=value)
two('L1','REG_L1','REG_L2','0.47uH DFE201612E-R47M=P2')
assert not fps['R12']['dnp'] and not fps['R11']['dnp']
nominal_vout=.5*(1+27.4/4.99);charge_current=890/2000
assert abs(nominal_vout-3.2454909819639277)<1e-12 and charge_current==.445
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R143',pcb_sha256=sha,independent_active_IC_pin_maps_and_nominal_land_dimensions_verified=True,
            ICs_checked=list(pins),numbered_lands_checked=checked,native_PCB_and_schematic_pin_maps_match=True,
            all_assigned_IC_pin_copper_groups_connected=True,bypass_and_support_networks=bypass,
            BQ24072T_nominal_profile=dict(battery_voltage_V=4.2,input_current_limit_A_when_USB500=.5,fast_charge_current_A=.445,
                                        nominal_fast_timer_hours=8.725,source='SLUS937C December2019'),
            TPS63802_nominal_output_V=nominal_vout,TPS_EN_tied_to_switched_VIN=True,MODE_PFM=True,
            BMI270_I2C_address='0x68',BMI270_secondary_and_unused_interrupt_pins_DNC=True,
            U9_VDD_on_VBAT_and_SEL_on_3V3_verified=True,U10_reference_and_comparator_pin_map_verified=True,
            guaranteed_effective_capacitance_layout_inductance_ESD_and_thermal_qualification=False,
            manufacturer_reflow_stencil_process_accepted=False,fabrication_ready=False)
(out/('active_IC_audit.json' if server else 'active_IC_audit_R136.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
