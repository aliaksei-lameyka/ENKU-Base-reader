# ENKU R45 production-visible text and test-point service labels

Derived from the Native-qualified R44 copper: 132 footprints, 471 track segments, 124 plated vias, two editable inner GND zones. **No netlist, copper, cell charger, PMOS or Good Display FPC change**.

R44 inherited 239 non-unrouted DRC violations and in particular **16 `text_height` violations** from 14 rear B.SilkS probe labels (TP1–TP14: 0.55mm high), the ESP32 antenna label (0.6mm) and small ENKU license warning text (0.55mm). KiCad fabrication rule requires **>=0.8mm**. R45 sets *each* to 0.8mm with readable stroke 0.12mm. The antenna message is shortened to `RF ANTENNA` to preserve edge clearance; board warning shortened to `ENKU BASE / OPEN HARDWARE` with correctly mirrored B.SilkS, keeping production verification instruction here and in manufacturing docs instead of tiny silk print.

**Not enough to remove DRC warnings by suppressing them.** Native KiCad R45 must refill both zones and assert **zero `text_height` violations**. Enlarge labels only if their new mask/silk overlap impact is identified and resolved; stop and fix any critical clearance. Other silk overlaps/clipped labels and library mismatches remain real release debt.
