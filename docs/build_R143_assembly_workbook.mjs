import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const data=JSON.parse(await fs.readFile(process.argv[2],'utf8'));
const wb=Workbook.create();const bom=wb.worksheets.add('BOM');const cpl=wb.worksheets.add('CPL');
function fill(sheet,rows,last,widths,title){
 sheet.showGridLines=false;sheet.getRange(`A1:${last}${rows.length+9}`).format.font={name:'Arial',size:10,color:'#182A3A'};
 sheet.getRange('A2').values=[[title]];sheet.getRange('A2').format.font={name:'Arial',size:14,bold:true};
 sheet.getRange('A4').values=[['Fitted top components']];sheet.getRange('A5').values=[['NO FAB. Absolute origin 0,0; native top angles require supplier import approval.']];
 sheet.getRange(`A7:${last}${rows.length+6}`).values=rows;
 sheet.getRange(`A7:${last}7`).format={fill:'#182A3A',font:{name:'Arial',size:10,color:'#FFFFFF',bold:true},wrapText:true,rowHeight:34,horizontalAlignment:'center',verticalAlignment:'center'};
 sheet.getRange(`A8:${last}${rows.length+6}`).format.rowHeight=25;
 widths.forEach((w,i)=>sheet.getRangeByIndexes(0,i,rows.length+9,1).format.columnWidth=w);
 sheet.freezePanes.freezeRows(7);sheet.freezePanes.freezeColumns(1);
 sheet.getRange(`A8:${last}${rows.length+6}`).format.verticalAlignment='center';
}
fill(bom,data.bom,'G',[43,10,32,27,29,57,9],'ENKU Base R143 - PCBWay BOM');
bom.getRange(`B8:B${data.bom.length+6}`).format.numberFormat='0';bom.getRange(`A8:G${data.bom.length+6}`).format.wrapText=true;bom.getRange(`A8:G${data.bom.length+6}`).format.autofitRows();
bom.getRange('B4').formulas=[[`=SUM(B8:B${data.bom.length+6})`]];bom.getRange('B4').format.font={bold:true};
fill(cpl,data.cpl,'E',[22,17,17,24,12],'ENKU Base R143 - native top placements');
cpl.getRange(`B8:D${data.cpl.length+6}`).format.numberFormat='0.0000';cpl.getRange('B4').formulas=[[`=COUNTA(A8:A${data.cpl.length+6})`]];cpl.getRange('B4').format.font={bold:true};
cpl.getRange('A5').values=[['X=board X, Y=-board Y (mm). No supplier rotation normalization is approved.']];
wb.recalculate();
if(bom.getRange('B4').values[0][0]!==114||cpl.getRange('B4').values[0][0]!==114)throw Error('Fitted count mismatch');
console.log((await wb.inspect({kind:'table',range:'BOM!A2:G10',include:'values,formulas',tableMaxRows:10,tableMaxCols:7,maxChars:2000})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
for(const name of ['BOM','CPL']){
 const im=await wb.render({sheetName:name,range:name==='BOM'?'A1:G15':'A1:E18',scale:1,format:'png'});await fs.writeFile(`/tmp/enku-r143-sheet/${name}.png`,new Uint8Array(await im.arrayBuffer()));
}
const dest=process.argv[3];
const x=await SpreadsheetFile.exportXlsx(wb);await x.save(dest);console.log('Exported',dest);
