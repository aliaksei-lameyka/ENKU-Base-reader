"""Prove CLI custom rules execute, including rejection of a real legacy fault."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
k,o=map(lambda s:Path(s).resolve(),sys.argv[1:3]);app=os.environ['ENKU_KICAD_APP'];name='enku-mainboard-r0.1';source=(k/(name+'.kicad_dru')).read_text();marker='R144_RULE_ENGINE_SENTINEL'
probe=f'''\n(rule "{marker}" (condition "A.Type == 'Pad' && B.Type == 'Pad' && A.memberOfFootprint('U11') && B.memberOfFootprint('U11')") (constraint clearance (min 0.40mm)))\n'''
rows=[]
with tempfile.TemporaryDirectory(prefix='enku-r144-rules-')as td:
 d=Path(td)
 for suffix in ['kicad_pcb','kicad_pro']:shutil.copy2(k/(name+'.'+suffix),d)
 for label,text,expected in [('valid_actual_rules',source,True),('injected_unsupported_operator',source+'\n(rule "INJECTED_BAD_OPERATOR" (condition "A.NetName =~ \'EPD_TEST\'") (constraint track_width (min 0.15mm)))\n',False)]:
  (d/(name+'.kicad_dru')).write_text(text+probe);report=d/(label+'.json')
  subprocess.run([app,'kicad-cli','pcb','drc','--severity-all','--format','json','--output',str(report),str(d/(name+'.kicad_pcb'))],check=True,stdout=subprocess.DEVNULL)
  j=json.loads(report.read_text());hits=[v for v in j['violations']if v['type']=='clearance'and marker in v['description']and'U11'in str(v)]
  assert bool(hits)==expected,(label,'Custom rules did not execute as expected')
  rows.append(dict(case=label,sentinel_rule_hits=len(hits),custom_rules_effective=bool(hits),expected=expected,result='PASS'))
  (o/(label+'_rule_probe.json')).write_bytes(report.read_bytes())
(o/'rule_engine_R144.json').write_text(json.dumps(dict(revision='R144',scope='Exact current custom rules in KiCad10.0.7; isolated PCB copies',probes=rows,legacy_unsupported_regex_operator_removed=True,original_revisions_untouched=True),indent=2)+'\n')
print('PASS custom rule execution sentinel and actual unsupported-operator fault')
