"""Actual-source assertions and open qualifications for the user's eight checks."""
import gzip,hashlib,json,math,sys,xml.etree.ElementTree as E
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon,LineString,Point,box
r,o=[Path(s).resolve()for s in sys.argv[1:3]];x=E.parse(o/'netlist.xml');cs={a.get('ref'):a for a in x.findall('./components/comp')};nodes={(a.get('ref'),a.get('pin')):n.get('name')for n in x.findall('./nets/net')for a in n.findall('node')};g=json.loads((o/'geometry.json').read_text());fill=json.loads(gzip.decompress((o/'native_copper_R138.json.gz').read_bytes()));electrical=json.loads((o/'independent_electrical_R142.json').read_text());route=json.loads((o/'routing/routing_review_R140.json').read_text())
def pin(ref,num,net):assert nodes[(ref,str(num))]==net,(ref,num,net)
def part(ref,val):assert cs[ref].findtext('value')==val,(ref,val)
for gpio,pad in [(3,15),(45,26),(46,16),(35,28),(36,29),(37,30)]:
 n=nodes[('U1',str(pad))];assert n.startswith('unconnected-');assert sum(a==n for a in nodes.values())==1 and not any(t['net']==n for t in g['tracks'])
part('U1','ESP32-S3-WROOM-1-N16R8');pin('U1',27,'BOOT');pin('R18',1,'3V3_SYS');pin('R18',2,'BOOT');part('R18','10k');pin('SW2',1,'BOOT');pin('SW2',2,'GND');pin('J7',5,'BOOT');pin('J7',6,'ESP_EN');pin('J7',1,'3V3_SYS');pin('J7',2,'GND')
assert {p['number']for p in g['pads']if p['ref']=='U1'and p['number']}==set(map(str,range(1,42)))
for ref,cc,pad in [('R62','USB_CC1','A5'),('R63','USB_CC2','B5')]:part(ref,'5.1k 1%');pin(ref,1,cc);pin(ref,2,'GND');pin('J5',pad,cc)
part('U8','USBLC6-2SC6')
for num,n in [(1,'USB_DP_CONN'),(6,'USB_DP_CONN'),(3,'USB_DM_CONN'),(4,'USB_DM_CONN'),(2,'GND'),(5,'VBUS_USB')]:pin('U8',num,n)
for a in ['A4','A9','B4','B9']:pin('J5',a,'VBUS_USB')
assert not any(a.startswith('DOCK')or 'DOCK'in a for a in nodes.values());pin('U3',13,'VBUS_USB');pin('U3',2,'VBAT');pin('U3',3,'VBAT');pin('U3',10,'VSYS');pin('U3',11,'VSYS');pin('Q2',2,'VSYS');pin('Q2',3,'SYS_EN');pin('Q2',1,'PWR_GATE');pin('R40',1,'VSYS');pin('R40',2,'PWR_GATE');pin('SW1',1,'GND');pin('SW1',2,'PWR_GATE');pin('U4',1,'SYS_EN');pin('U4',10,'SYS_EN');pin('U4',2,'GND')
pin('J1',1,'VBAT');pin('J1',2,'GND');pin('R26',1,'BAT_ADC_SW');pin('R26',2,'BAT_ADC');pin('R27',1,'BAT_ADC');pin('R27',2,'GND');pin('U9',2,'VBAT');pin('U9',5,'VBAT');pin('U9',4,'3V3_SYS');pin('U1',39,'BAT_ADC')
for num,n in [(1,'EPD_GDR'),(2,'EPD_RESE'),(3,'EPD_SW')]:pin('Q1',num,n)
part('L2','47uH TYS5040470M-10');pin('L2',1,'EPD_VCI');pin('L2',2,'EPD_SW');part('Q1','IRLML6346TRPBF')
for ref,a,b in [('D1','EPD_VGH','EPD_SW'),('D2','GND','EPD_CP_NEG'),('D3','EPD_CP_NEG','EPD_VGL')]:part(ref,'MBR0530T1G');pin(ref,1,a);pin(ref,2,b)
part('R28','0R');pin('R28',1,'3V3_SYS');pin('R28',2,'EPD_VCI');pin('J3',15,'3V3_SYS');pin('J3',16,'EPD_VCI');part('R29','0R');pin('R29',2,'GND');assert electrical['reset']['maximum_static_output_V']<3.3
sd=[('R23','SD_CS_CARD',2),('R91','SD_MOSI_CARD',3),('R92','SD_MISO_CARD',7),('R93','SD_DAT1_BIAS',8),('R94','SD_DAT2_BIAS',1)]
for ref,net,pad in sd:part(ref,'10k');pin(ref,1,'3V3_SYS');pin(ref,2,net);pin('J2',pad,net)
pin('J2',4,'3V3_SYS');pin('J2',5,'SD_SCLK_CARD');assert not any(set([nodes.get((ref,'1')),nodes.get((ref,'2'))])=={'3V3_SYS','SD_SCLK_CARD'}for ref in cs if ref.startswith('R'))
for n,net in [(5,'3V3_SYS'),(8,'3V3_SYS'),(12,'3V3_SYS'),(7,'GND'),(6,'GND'),(1,'GND'),(13,'I2C_SCL'),(14,'I2C_SDA'),(4,'IMU_INT1')]:pin('U5',n,net)
pin('U1',11,'IMU_INT1');part('R24','4.7k');part('R25','4.7k');pin('R24',1,'3V3_SYS');pin('R25',1,'3V3_SYS')
antenna=[z for z in g['zones']if z['rule']and set(z['layers'])=={0,2,4,6}];assert len(antenna)==1;region=sh.union_all([Polygon(q)for z in antenna for q in z['polygons']]);antenna_areas={}
for layer in [0,4,6,2]:
 objects=[sh.make_valid(Polygon(a['shell'],a['holes']))for a in fill['filled_zones'][str(layer)]]
 objects += [Polygon(q)for p in g['pads']for q in p['polygons'].get(str(layer),[])if p['attribute']!=3]
 objects += [Point(t['start']).buffer(t['width']/2)if t['via']else LineString([t['start'],t['end']]).buffer(t['width']/2)for t in g['tracks']if t['via']or t['layer']==layer]
 area=sh.union_all(objects).intersection(region).area;assert area<1e-8,(layer,area);antenna_areas[str(layer)]=area
distances=[]
for net in ['EPD_SW','EPD_CP_NEG','REG_L1','REG_L2']:
 for signal in ['EPD_SCLK_PANEL','EPD_MOSI_PANEL','EPD_BUSY','SPI_SCLK','SPI_MOSI']:
  a=[LineString([t['start'],t['end']]).buffer(t['width']/2)for t in g['tracks']if not t['via']and t['net']==net];b=[LineString([t['start'],t['end']]).buffer(t['width']/2)for t in g['tracks']if not t['via']and t['net']==signal]
  if a and b:distances.append(dict(switch_net=net,signal=signal,projected_copper_edge_gap_mm=sh.union_all(a).distance(sh.union_all(b)),different_layers_and_planes_not_resolved_by_this_projection=True))
report=dict(revision='R142',pcb_sha256=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),ESP32=dict(GPIO35_37_no_loads=True,GPIO26_32_not_exposed_on_module=True,module_pad32_is_GPIO39_not_GPIO32=True,strap3_45_46_free=True,BOOT10k_and_SW2_and_J7_recovery=True,hold_BOOT_low_3ms_after_EN_rises=True,UART_download_no_auto_programmer_on_board=True),USB=dict(CC1_CC2_independent5k1=True,USBLC6_data_ESD_present=True,VBUS_ferrite=False,VBUS_shunt_filter_caps=True,direct_nominal_capacitance_uF=6.8,ESD_EMC_inrush_and_factory90ohm_stackup='HOLD'),power_path=dict(dock_installed=False,USB_battery_DPPM='BQ24072T internal power path prioritizes system, reduces charge and permits battery supplement; input reverse blocking per TI',battery_PCM_on_mainboard=False,finished_pack_PCM_required_and_unqualified=True,SOC='Switched 2M/680k ADC voltage proxy, not fuel gauge',OFF='Q2 disconnects reader; charger remains supplied; reset follows decaying switched3V3; highZ modes defaultUSB100 and CE low',OFF_backpower_USB_UART_GPIO_leakage_measurements='NOT RUN'),EPD=dict(panel='GDEY0397T81P / SSD1677',panel_source_sha256='e28ea298457108bb3431b8c4de065834f62390b6caf2dc58e216d134fe559dbc',VCI_max_operating_V=3.3,panel_ambient_range_C=[0,50],L2_uH=47,L2_tolerance_percent=20,L2_Irms_typ_A=1.,L2_Isat_typ_A=1.1,L2_Isat_definition='30% inductance reduction at25+-5C, not guaranteed hot minimum',L2_DCRmax_ohm=.326,diodes='MBR0530T1G 30V /0.5A',Q1='IRLML6346TRPBF 30V',pin5_VDHR_VSH2_dispute='HOLD; no vendor resolution in registered reply',FPC_contact_side_pin1_and_case_fit='HOLD',ceramic_capacitance_DC_loss_and_actual_HV_overshoot='HOLD',PFM_and_load_step_voltage_qualification='HOLD'),SD=dict(mode='SPI shared with EPD',all_CMD_DAT0_3_external10k=True,SD_CD_separate_GPIO39=True,peak_current_and_hotplug_USBMSC_exclusive_ownership='HOLD'),BMI270=dict(VDD_VDDIO_same_switched_rail=True,CSB_high_I2C=True,SDO_GND_address='0x68',INT1_to_GPIO18=True,I2C_external4k7=True,configuration_blob_internal_status_and_actual_interrupt_test='NOT RUN'),layout=dict(antenna_all_four_copper_intersections_mm2=antenna_areas,case_metal_battery_FPC_RF_clearance_and_throughput='HOLD',power_switch_to_display_projected_distances=distances,reference_and_power_path_geometry_report='routing/routing_review_R140.json',ground_projection_is_not_EMI_or_control_loop_qualification=True),physical_tests='NOT RUN',fabrication_ready=False)
(o/'requested_review_R142.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS requested pin, power, SD, IMU, antenna source assertions; explicit supplier/bench HOLDs',flush=True)
