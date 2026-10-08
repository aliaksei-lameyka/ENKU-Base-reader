#!/usr/bin/env python3
"""ENKU PCB R15: extend lower edge and validate the resulting KiCad board.
Run: python3 hardware/mainboard/tools/pcb_r15_extend_and_check.py --pcb hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pcb
Requires kicad-cli for DRC. Makes a backup; never modifies copper routing.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys

OLD = '(gr_rect (start 18 20) (end 77 114)'
NEW = '(gr_rect (start 18 20) (end 77 121)'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pcb', type=pathlib.Path, required=True)
    ap.add_argument('--apply', action='store_true', help='Write new outline (default dry run)')
    ap.add_argument('--drc', action='store_true', help='Run kicad-cli pcb drc after patch')
    args = ap.parse_args()
    src = args.pcb.read_text(encoding='utf-8')
    old_count = src.count(OLD)
    new_count = src.count(NEW)
    if old_count + new_count != 1:
        raise SystemExit('ABORT: expected exactly one known R15/R16 Edge.Cuts rectangle')
    for ref in ('H1','H2','H3','H4','J2','J3','J5','SW3','SW4','SW5','SW6'):
        if not re.search(r'\(property "Reference" "'+ref+r'"',src):
            raise SystemExit('ABORT: missing reference '+ref)
    new = src.replace(OLD, NEW) if old_count else src
    assert new.count('(segment ') == src.count('(segment ')
    assert new.count('(via ') == src.count('(via ')
    assert new.count('(footprint ') == src.count('(footprint ')
    print(json.dumps({'old_mm':[59,94],'new_mm':[59,101],
      'segments_unchanged':src.count('(segment '),'vias_unchanged':src.count('(via '),
      'footprints_unchanged':src.count('(footprint '),
      'outline_status':'already_59x101' if new_count else 'still_59x94',
      'applied':bool(args.apply and old_count)},indent=2))
    if not args.apply:
        return
    if old_count:
        backup = args.pcb.with_suffix(args.pcb.suffix+'.pre-r15.bak')
        if backup.exists():
            raise SystemExit('ABORT: backup already exists')
        shutil.copy2(args.pcb,backup)
        args.pcb.write_text(new,encoding='utf-8')
        print('Backup:',backup)
    if args.drc:
        cli=shutil.which('kicad-cli')
        if not cli: raise SystemExit('kicad-cli missing: outline applied, DRC NOT run')
        out=args.pcb.with_name(args.pcb.stem+'-r15-drc.json')
        cmd=[cli,'pcb','drc','--format','json','-o',str(out),str(args.pcb)]
        p=subprocess.run(cmd,text=True,capture_output=True)
        print('DRC exit:',p.returncode,'report:',out)
        print(p.stdout[-2000:]); print(p.stderr[-2000:],file=sys.stderr)
        if p.returncode: raise SystemExit('DRC has violations or failed; board NOT fabrication-ready')

if __name__=='__main__': main()
