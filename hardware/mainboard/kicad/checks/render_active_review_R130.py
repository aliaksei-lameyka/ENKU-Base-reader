"""Render only actual native SVG geometry for the R130 visual review."""
import xml.etree.ElementTree as ET,sys
from pathlib import Path
import cairosvg
c=Path(sys.argv[1])/'checks';ET.register_namespace('','http://www.w3.org/2000/svg')
for source,dest,view in [
 ('native_top_R130.svg','native_top_R130.png',None),
 ('native_bottom_R130.svg','native_bottom_R130.png',None),
 ('native_bottom_R130.svg','native_J7_pin1_R130.png',(13,64.5,8,7)),
 ('native_F_Mask_R130.svg','native_IC_mask_R130.png',(28,69,14,4)),
 ('native_F_Paste_R130.svg','native_IC_paste_R130.png',(28,69,14,4)),
]:
    tree=ET.parse(c/source).getroot()
    if view:
        tree.set('viewBox',' '.join(map(str,view)));tree.set('width',f'{view[2]}mm');tree.set('height',f'{view[3]}mm')
    cairosvg.svg2png(bytestring=ET.tostring(tree),write_to=str(c/dest),output_width=1300,background_color='white')
    print(dest)
