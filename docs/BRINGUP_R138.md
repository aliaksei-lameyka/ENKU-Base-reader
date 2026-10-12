# R138 first-board checks — physical qualification NOT RUN

Continue the complete R134 staged plan and R135/R136 power, NTC and capacitance additions. These are instructions for future user-approved EVT samples; no test result is implied.

Before power, record exact source commit/PCB SHA, board serial, manufacturing and component lots, instruments and ambient/cell temperature. Verify all329 via positions and the actual agreed0.20mm bore process; obtain the agreed barrel-copper/thickness/registration evidence. Do not treat a visual nominal0.15mm ring or a simple DC continuity result as proof of plating thickness, void-free barrels or current rating.

Verify the five U3 and one R28 resin-filled/copper-capped sites against the process CSVs, including flatness and finish under paste. Inspect R28 pin1 solder joint and U3 EP/thermal joints for the agreed voiding/assembly criteria. Ordinary tenting does not satisfy these requests. Confirm the12 U1 EP holes and grid/stencil assembly process, plus four USB plated slots and0.8mm stakes on the actual1.6mm board.

With battery disconnected, use the existing staged current-limited supply sequence. Capture3V3,VSYS/SYS_EN,VBUS,VBAT, input/battery currents and reset causes during startup, power cycling, hard OFF, brownouts and USB hot-plug. Check the R28 supply transition and local MCU/SD/EPD loads; isolate measurement contributions before assigning barrel heating or voltage-drop limits. The conditional18µm single-barrel resistance model is not a thermal acceptance specification.

Check both USB-C orientations, negotiated power policy, reset/ROM behavior and actual90-ohm stack assumptions. Firmware must provide exclusive host/reader ownership before exposing microSD as USB Mass Storage, preserve writes safely across removal and return the card to the reader. USB MSC remains unimplemented/unqualified in this hardware tree.

Repeat full charging-cycle and high-load thermal tests with the final case, qualified thin pack and attached NTC. Exercise sensor-open/short/detachment, R81 and R82 faults under controlled fixtures and retain raw traces. Actual U3 B spreading55.3333mm² and native0 findings do not prove safe cell temperature, detached-sensor detection or fault behavior. Retain the4.90–35.01°C nominal window and all R136 unqualified corners.

Finally verify battery insertion/replacement, PH-2 polarity, external NTC attachment/strain relief, C9 maximum1.45mm clearance, button travel, USB/card access, RF battery-metal keepout, display/FPC bend and case closure at unchanged thickness. Qualify at least two interchangeable finished PCM pack models with China/Poland supply before treating substitution as supported. Empty evidence records are HOLD, never a passed physical test.
