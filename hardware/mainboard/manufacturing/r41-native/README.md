# Exact R41 Native KiCad diagnostic evidence

Reports extracted losslessly from gzip/base64 records in GitHub Actions job **113444113178**, run **37815837327**, commit **cf04f72110456540a6bb1c9ef0a49f7621f87319**. No issue filtering or report rewriting was applied. Original `r29-*` names are legacy workflow output names, not report revision labels.

See `verification.json` for input PCB and report SHA-256 hashes, exact counts, priority gate types and artifact identity. The workflow copies the active R41 PCB to the root schematic basename in a temporary runner, refills both GND zones, saves/reopens them, and executes schematic parity DRC on that filled input. Source PCB remains the editable unfilled-zone design; filled diagnostic PCB is in the linked Actions artifact.

**ERC 0 / parity 0 / priority DRC 0; full DRC NOT PASS: 241 violations plus 210 unconnected items. PCBWay Ready 30%, manufacturing blocked.**

`structural-ci.log` preserves the complete successful active hardware-check job 113447000213, run 37816685057, commit 621e9df64eae1afd63eae35c61bdd8bdacd9aea6. Historical baseline diagnostics in this log must not be mistaken for the explicit active R41 audits.
