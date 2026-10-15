"""R144 explicit scope, adapted from audit_capacitance_R136.py; original unchanged."""
"""Exact native parts and explicit typical-curve scenarios, never a guarantee."""
import hashlib, json, math, sys
import xml.etree.ElementTree as ET
from pathlib import Path

r, out = (Path(s).resolve() for s in sys.argv[1:3])
c = r / 'checks'
parts = {p.attrib['ref']: p for p in ET.parse(out / 'netlist.xml').findall('./components/comp')}
nodes = {(a.attrib['ref'], a.attrib['pin']): n.attrib['name']
         for n in ET.parse(out / 'netlist.xml').findall('./nets/net') for a in n.findall('node')}
features = {p['ref']: p for p in json.loads((out / 'assembly_features.json').read_text())['footprints']}
g = json.loads((out / 'geometry.json').read_text())
sources = json.loads((c / 'capacitor_sources_R136.json').read_text())
assert sources['manufacturer_DC_guarantee_available'] is False
# Rounded downward from the independently viewed downloaded exact-part page2
# DC curves:22uF retention about.44 at4.59V/.49 at4.24V/.59 at3.4V;
# 10uF about.63 at4.59V. These are project scenarios, not guaranteed corners.
scenarios = [
    ('BQ_SYS', ['C7'], 4.59, .40, 4.7),
    ('BQ_BAT', ['C8'], 4.24, .45, 4.7),
    ('TPS_INPUT', ['C9'], 4.59, .40, 4.0),
    ('TPS_OUTPUT_LOCAL', ['C11', 'C12'], 3.60, .50, 7.0),
]
rows = []
for name, refs, voltage, dc, required in scenarios:
    for ref in refs:
        sf = {p.attrib['name']: p.text or '' for p in parts[ref].findall('./fields/field')}
        assert sf['MPN'] == features[ref]['fields']['MPN'] == 'CC0805MKX5R6BB226'
        assert sf['Voltage'] == features[ref]['fields']['Voltage'] == '10V'
        assert parts[ref].findtext('value') == features[ref]['value'] == '22uF 10V'
        assert nodes[(ref, '2')] == 'GND'
        assert nodes[(ref, '1')] == {'C7':'VSYS', 'C8':'VBAT', 'C9':'SYS_EN', 'C11':'3V3_SYS', 'C12':'3V3_SYS'}[ref]
    pre = len(refs) * 22 * .80 * .85 * .90
    effective = pre * dc
    assert effective > required
    rows.append(dict(name=name, refs=refs, DC_voltage_V=voltage, DC_retention_scenario=dc,
                     nominal_uF=len(refs)*22, tolerance_temperature_age_budget_uF=pre,
                     effective_scenario_uF=effective, target_minimum_uF=required,
                     scenario_margin_percent=(effective/required-1)*100,
                     guaranteed_effective_uF=None, qualified=False))
assert g['footprints']['C9']['pos'] == [59.7,87.7] and g['footprints']['C9']['angle'] == 0
assert g['footprints']['C9']['lib'] == 'ENKU:C_CC0805_YAGEO_REFLOW_TRANSFER'
assert sorted((p['number'],p['pos'],p['size']) for p in g['pads'] if p['ref']=='C9') == [
    ('1',[58.775,87.7],[.95,1.4]), ('2',[60.625,87.7],[.95,1.4])]
# Include every board capacitor directly attached to the regulator output.
all_output = sorted(ref for ref in parts if ref.startswith('C')
                    and {nodes[(ref,'1')],nodes[(ref,'2')]} == {'3V3_SYS','GND'})
assert all_output == ['C11','C12','C13','C14','C15','C16','C17','C18','C19','C38']
old_input = 10 * .90 * .85 * .90 * .60
assert math.isclose(old_input,4.131)
ref_max = json.loads((out/'independent_electrical_R144.json').read_text())['reset']['maximum_static_output_V']
assert ref_max < 3.6
report = dict(revision='R144', pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],
              exact_C9_new_MPN_value_and_native_nets_verified=True,
              old_C9_effective_scenario_uF=old_input, old_C9_margin_percent=(old_input/4-1)*100,
              BQ_battery_regulation_max_V=4.24, BQ_OUT_tracking_max_V=4.24+.270,
              allocated_VSYS_SYS_EN_bias_V=4.59, allocated_steady_3V3_bias_V=3.60,
              conditional_PWM_feedback_and_resistor_corner_V=ref_max, scenarios=rows,
              all_direct_TPS_output_capacitors=all_output,
              all_direct_output_nominal_uF=64.6,
              no_direct_USB_capacitor_added=True, direct_VBUS_nominal_uF=6.8,
              C9_max_height_before_mm=.95, C9_max_height_after_mm=1.45,
              other_existing_C7_C8_C11_C12_max_height_mm=1.45,
              height_change_requires_local_enclosure_fit=True, external_case_thickness_increased=False,
              manufacturer_guaranteed_DC_and_AC_corner_available=False,
              temperature_DC_AC_ageing_interaction_and_lot_variation_qualified=False,
              switched_rail_inrush_U4_stability_Q2_USB_startup_and_full_case_fit_qualified=False,
              assembly_and_Ceff_qualified=False, physical_tests='NOT RUN', fabrication_ready=False)
(out/'capacitance_scenarios_R144.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
