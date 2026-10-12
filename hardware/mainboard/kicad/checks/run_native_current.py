"""Select the reviewed immutable checkpoint; CI cannot regenerate its baseline."""
import hashlib, json, os, subprocess, sys
from pathlib import Path

def reviewed_driver(root):
    c = root / 'checks'
    selector = json.loads((c / 'current_checkpoint.json').read_text())
    revisions = {'R136': 'run_native_R136.py', 'R137': 'run_native_R137.py'}
    revision = selector['revision']
    if revision not in revisions:
        raise ValueError('No reviewed native driver for checkpoint ' + str(revision))
    expected_selector = dict(revision=revision, verification_file='verification_checkpoint_'+revision+'.json',
                             geometry_file='geometry_checkpoint_'+revision+'.json.gz', drc_file='drc_checkpoint_'+revision+'.json')
    if selector != expected_selector:
        raise ValueError('Unexpected checkpoint paths')
    expected = json.loads((c / selector['verification_file']).read_text())
    actual = hashlib.sha256((root / 'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
    if actual != expected['pcb_sha256']:
        raise ValueError('Committed PCB differs from the reviewed checkpoint')
    required_guards = {'R136': 23, 'R137': 25}
    if expected['native_kicad'] != '10.0.7' or expected['independent_guards_passed'] != required_guards[revision]:
        raise ValueError('Incomplete or unsupported reviewed baseline')
    if expected['fabrication_ready'] is not False:
        raise ValueError('This driver verifies engineering NO FAB; release requires a separate reviewed gate')
    return c / revisions[revision]

def main():
    if len(sys.argv) != 3:
        raise SystemExit('usage: run_native_current.py KICAD_DIR OUTPUT_DIR (no freeze option)')
    root = Path(sys.argv[1]).resolve()
    driver = reviewed_driver(root)
    print('Verify', driver.name, 'without repairs or baseline regeneration', flush=True)
    subprocess.run([sys.executable, str(driver), str(root), str(Path(sys.argv[2]).resolve())], check=True)

if __name__ == '__main__':
    main()
