import sys,gzip,json,pcbnew as p
from pathlib import Path
old=json.loads(gzip.decompress(Path(sys.argv[2]).read_bytes()));ids={x['uuid']for x in old['tracks']};b=p.LoadBoard(sys.argv[1])
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA)and t.m_Uuid.AsString()not in ids:t.SetFrontTentingMode(p.TENTING_MODE_TENTED);t.SetBackTentingMode(p.TENTING_MODE_TENTED)
p.SaveBoard(sys.argv[1],b)
