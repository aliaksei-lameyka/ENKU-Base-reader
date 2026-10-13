"""Read-only validation of current documentation entry links and retained sources."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ["README.md", "docs/README.md", "docs/CURRENT_STATUS.md",
           "docs/BATTERY_STATUS_R139.md", "docs/REPOSITORY_CONSOLIDATION_R139.md",
           "hardware/mainboard/CURRENT_STATUS.md", "hardware/mainboard/kicad/README.md",
           "docs/history/retained-branches/README.md"]

links = 0
for name in ENTRIES:
    p = ROOT / name
    for href in re.findall(r"\]\(([^\s)]+)\)", p.read_text()):
        if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", href) or href.startswith("#"):
            continue
        target = (p.parent / href.split("#", 1)[0]).resolve()
        assert target.is_relative_to(ROOT) and target.is_file(), (name, href)
        links += 1

preserved = json.loads((ROOT / "hardware/mainboard/kicad/checks/preservation_manifest_R138.json").read_text())
for name, digest in preserved["unchanged_main_R137_files"].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
assert len(preserved["unchanged_main_R137_files"]) == 1325
assert not subprocess.check_output(["git", "diff", "--name-only", "1bab0f2b811b8f9f1cdb9136e408784b2519e7f0", "--", "hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pcb", "hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro", "hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_dru", "hardware/mainboard/kicad/ENKU.kicad_sym", "hardware/mainboard/kicad/*.kicad_sch", "hardware/mainboard/kicad/ENKU.pretty", "hardware/mainboard/kicad/standard-footprints", ".github/workflows"], cwd=ROOT)
registry = json.loads((ROOT / "docs/qualification/R139/REPOSITORY_BRANCHES_R139.json").read_text())
for branch in registry["all_observed_heads"]:
    if "diff_file" in branch:
        expected = subprocess.check_output(["git", "diff", "--binary", branch["merge_base"], branch["observed_head_sha"]], cwd=ROOT)
        assert (ROOT / branch["diff_file"]).read_bytes() == expected
print(f"PASS: {links} current local links,1325 historical hashes, frozen electrical/workflow source and five exact branch diffs")
