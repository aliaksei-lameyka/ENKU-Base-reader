# Rebuild the enclosure reference

Run `python3 build_mechanical.py`, then `python3 render_mechanical.py` from this directory with CadQuery,NumPy,Matplotlib andPillow installed. The scripts use the included exact R148 PCB/geometry snapshot, native bare-board face and OEM models. Outputs are created in `output/`; the render creates `qa/` itself. Geometry units:mm.

No PCB routing or source is changed by these scripts. The1.6mmfinished board is analytically extruded from the exact native1.51mmdielectric face; the25holes are preserved. STEP is nominal enclosure reference, not qualified full display/flex/battery/case assembly. Small diode bodies are nominal visual proxies, not max package envelopes; native courtyards govern the cleared local FPC approach.

To rebuild visual maps/PDF, use the sibling `04_visual_review/rebuild` scripts in this order:render_maps.py,render_changes.py,rebuild_pdf_templates.py. They resolve the package's source, manufacturing and verification folders automatically; dependencies also includePyMuPDF,Shapely2.2 andGerbonara1.6.3. No private supplier STEP is required for the paper template because its derived flat outline is included. The fold is not solved or approved.
