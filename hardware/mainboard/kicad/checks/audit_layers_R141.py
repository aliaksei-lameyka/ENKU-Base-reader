"""Read-only native layer, hidden-field and netless-copper inventory."""
import hashlib,json,sys
from pathlib import Path
from collections import Counter
import pcbnew as p

source=Path(sys.argv[1]);out=Path(sys.argv[2]);b=p.LoadBoard(str(source))
enabled=set(b.GetEnabledLayers().Seq())
layers=[{'id':l,'name':b.GetLayerName(l),'copper':p.IsCopperLayer(l)} for l in sorted(enabled)]
assert all(x['name'].strip() for x in layers)
assert len({x['name'] for x in layers})==len(layers)
assert {x['name'] for x in layers if x['copper']}=={'F.Cu','In1.Cu','In2.Cu','B.Cu'}
used=Counter();disabled=[];hidden=[];copper_graphics=[];netless=[]
def item(x,kind,ref=''):
    ls=list(x.GetLayerSet().Seq()) if hasattr(x,'GetLayerSet') else [x.GetLayer()]
    for l in ls:used[l]+=1
    # NPTH pads may retain the KiCad all-copper wildcard despite no copper fabrication image.
    bad=[l for l in ls if l not in enabled]
    if bad:disabled.append({'kind':kind,'ref':ref,'uuid':x.m_Uuid.AsString(),'layers':bad,'layer_names':[b.GetLayerName(l) for l in bad],'text':x.GetText() if hasattr(x,'GetText') else '', 'attribute':int(x.GetAttribute()) if hasattr(x,'GetAttribute') else None})
    if hasattr(x,'IsVisible') and not x.IsVisible():hidden.append({'kind':kind,'ref':ref,'text':x.GetText() if hasattr(x,'GetText') else '', 'layer':b.GetLayerName(x.GetLayer()),'uuid':x.m_Uuid.AsString()})
    if kind in ['drawing','footprint_graphic'] and any(p.IsCopperLayer(l) for l in ls):copper_graphics.append({'kind':kind,'ref':ref,'uuid':x.m_Uuid.AsString(),'layers':[b.GetLayerName(l) for l in ls]})
    if hasattr(x,'GetNetCode') and x.GetNetCode()==0 and any(p.IsCopperLayer(l) for l in ls):
        netless.append({'kind':kind,'ref':ref,'pad':x.GetNumber() if hasattr(x,'GetNumber') else '', 'uuid':x.m_Uuid.AsString(),'layers':[b.GetLayerName(l) for l in ls],'attribute':int(x.GetAttribute()) if hasattr(x,'GetAttribute') else None})
for t in b.GetTracks():item(t,'via' if isinstance(t,p.PCB_VIA) else 'track')
for z in b.Zones():item(z,'rule_area' if z.GetIsRuleArea() else 'zone')
for d in b.GetDrawings():item(d,'drawing')
for f in b.GetFootprints():
    for pad in f.Pads():item(pad,'pad',f.GetReference())
    for d in f.GraphicalItems():item(d,'footprint_graphic',f.GetReference())
    for z in f.Zones():item(z,'rule_area' if z.GetIsRuleArea() else 'zone',f.GetReference())
    for field in f.GetFields():item(field,'field',f.GetReference())
prl=source.with_suffix('.kicad_prl');ui=json.loads(prl.read_text()).get('board',{}) if prl.exists() else None
assert not copper_graphics
assert not [x for x in netless if x['kind'] in ['track','via','zone']]
assert not [x for x in disabled if x['kind'] in ['track','via','zone','rule_area']]
data={'revision':'R141','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'native_kicad':p.Version(),'enabled_layers':layers,'unnamed_layers':[],'duplicate_layer_names':[],'four_copper_layers_exact':True,'objects_per_layer':{b.GetLayerName(l):n for l,n in sorted(used.items())},'objects_touching_disabled_layers':disabled,'hidden_fields_or_graphics':hidden,'copper_graphics_without_net_semantics':copper_graphics,'netless_copper_items':netless,'local_UI_settings':ui,'visibility_does_not_remove_objects_from_DRC_or_explicit_layer_exports':True,'fabrication_ready':False}
data['hidden_reference_count']=sum(not f.Reference().IsVisible() for f in b.GetFootprints())
data['hidden_value_count']=sum(not f.Value().IsVisible() for f in b.GetFootprints())
disabled_non_copper=Counter(l for x in disabled for l in x['layers'] if not p.IsCopperLayer(l))
data['disabled_documentation_layers']=[{'id':l,'name':b.GetLayerName(l),'objects':n} for l,n in sorted(disabled_non_copper.items())]
data['inactive_copper_pad_wildcards_are_not_additional_board_layers']=True
data['unassigned_tracks_vias_and_copper_zones']=0
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'enabled_layers':len(layers),'unnamed':0,'disabled_items':len(disabled),'hidden':len(hidden),'copper_graphics':len(copper_graphics),'netless':len(netless),'netless_types':dict(Counter(x['kind'] for x in netless)),'hidden_types':dict(Counter(x['kind'] for x in hidden)),'output':str(out)}))
