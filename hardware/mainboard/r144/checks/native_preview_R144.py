"""Native proposal preview, preserving project settings across KiCad CLI."""
from pathlib import Path
import json,subprocess,sys,os,hashlib
k=Path(sys.argv[1]).resolve();o=Path(sys.argv[2]).resolve();o.mkdir(parents=True,exist_ok=True);app=os.environ['ENKU_KICAD_APP'];repo=Path(__file__).resolve().parents[4];common=repo/'hardware/mainboard/kicad/checks';pro=k/'enku-mainboard-r0.1.kicad_pro';raw=pro.read_bytes();os.environ['KIPRJMOD']=str(k)
try:
 subprocess.run([app,'kicad-cli','pcb','drc','--severity-all','--all-track-errors','--schematic-parity','--refill-zones','--save-board','--format','json','--output',str(o/'drc.json'),str(k/'enku-mainboard-r0.1.kicad_pcb')],check=True)
finally:pro.write_bytes(raw)
for script,name in [('native_board.py','geometry.json'),('export_assembly_features.py','assembly_features.json')]:subprocess.run([app,'python3.11',str(common/script),'export',str(k/'enku-mainboard-r0.1.kicad_pcb'),str(o/name)]if script=='native_board.py'else[app,'python3.11',str(common/script),str(k/'enku-mainboard-r0.1.kicad_pcb'),str(o/name)],check=True)
subprocess.run([app,'kicad-cli','sch','export','netlist','--format','kicadxml','--output',str(o/'netlist.xml'),str(k/'enku-mainboard-r0.1.kicad_sch')],check=True,stdout=subprocess.DEVNULL)
(o/'source_pcb.sha256').write_text(hashlib.sha256((k/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()+'  enku-mainboard-r0.1.kicad_pcb\n')
