"""Render actual native SVGs without modifying or inventing CAD geometry."""
import copy, xml.etree.ElementTree as ET, sys
from pathlib import Path
import cairosvg

c = Path(sys.argv[1]) / 'checks'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
for source, dest, view in [
    ('native_top_R128.svg','native_U1_copper_R128.png',(14.7,23.7,5.6,5.6)),
    ('native_F_Mask_R128.svg','native_U1_F_Mask_R128.png',(14.7,23.7,5.6,5.6)),
    ('native_F_Paste_R128.svg','native_U1_F_Paste_R128.png',(14.7,23.7,5.6,5.6)),
    ('native_B_Mask_R128.svg','native_U1_B_Mask_R128.png',(14.7,23.7,5.6,5.6)),
    ('native_top_R128.svg','native_top_R128.png',None),
]:
    r = ET.parse(c/source).getroot()
    if view:
        r.set('viewBox',' '.join(map(str,view)));r.set('width',f'{view[2]}mm');r.set('height',f'{view[3]}mm')
    cairosvg.svg2png(bytestring=ET.tostring(r),write_to=str(c/dest),output_width=1100,background_color='white')
    print(dest)
