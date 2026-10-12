"""Minimal quoted s-expression edits with UUID-bounded source preservation."""
import json,math,re,uuid

def uid(name):return str(uuid.uuid5(uuid.NAMESPACE_URL,'ENKU/R134/'+name))
def q(value):return json.dumps(str(value))
def block(text,start):
    depth=0;quoted=escaped=False
    for i in range(start,len(text)):
        ch=text[i]
        if quoted:
            if escaped:escaped=False
            elif ch=='\\':escaped=True
            elif ch=='"':quoted=False
        elif ch=='"':quoted=True
        elif ch=='(':depth+=1
        elif ch==')':
            depth-=1
            if not depth:return text[start:i+1],i+1
    raise ValueError('Unbalanced s-expression')
def children(text):
    i=text.index('(')+1
    while i<len(text):
        start=text.find('(',i)
        if start<0:break
        value,end=block(text,start);yield start,end,value;i=end

def symbol(text,name,cache=False):
    offset=0;target=text
    if cache:
        offset=text.index('(lib_symbols');target,_=block(text,offset)
    for a,z,value in children(target):
        if re.match(r'\(symbol\s+'+re.escape(q(name))+r'[\s)]',value):return offset+a,offset+z,value
    raise AssertionError(name)
def instance(text,ref):
    for a,z,value in children(text):
        if value.startswith('(symbol (lib_id ')and f'(property "Reference" "{ref}"'in value:return a,z,value
    raise AssertionError(ref)
def prop(text,name,value):
    m=re.search(r'\(property '+re.escape(q(name))+r' ',text)
    if not m:return text[:-1]+f'\n(property {q(name)} {q(value)} (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n)'
    part,end=block(text,m.start());part=re.sub(r'^(\(property "[^"]+" )"(?:\\.|[^"\\])*"',lambda x:x[1]+q(value),part,count=1)
    return text[:m.start()]+part+text[end:]
def pins(sym):
    out={}
    for _,_,part in children(sym):
        if not part.startswith('(symbol '):continue
        for _,_,pin in children(part):
            if not pin.startswith('(pin '):continue
            n=re.search(r'\(number "([^"]+)"',pin)[1];v=re.search(r'\(at ([\d.-]+) ([\d.-]+) ([\d.-]+)\)',pin)
            out[n]=(float(v[1]),float(v[2]),pin)
    return out

def label(net,x,y,angle=0,name=''):
    return f'(global_label {q(net)} (shape input) (at {x:.6f} {y:.6f} {angle}) (effects (font (size .88 .88)) (justify {"right"if angle==0 else "left"} bottom)) (uuid {q(uid(name or net+str((x,y))))}))'
def change_pin_label(text,point,net):
    connected={tuple(point)};wires=[]
    for _,_,part in children(text):
        if part.startswith('(wire '):
            rows=re.findall(r'\(xy ([\d.-]+) ([\d.-]+)\)',part);assert len(rows)==2
            wires.append(tuple((round(float(x),6),round(float(y),6))for x,y in rows))
    while True:
        old=len(connected)
        for a,b in wires:
            if a in connected or b in connected:connected.update([a,b])
        if len(connected)==old:break
    found=0
    for a,z,part in reversed(list(children(text))):
        if not part.startswith('(global_label '):continue
        at=re.search(r'\(at ([\d.-]+) ([\d.-]+) ',part)
        if at and any(math.dist([float(at[1]),float(at[2])],p)<1e-6 for p in connected):
            new=re.sub(r'^\(global_label "[^"]+"',f'(global_label {q(net)}',part,count=1);text=text[:a]+new+text[z:];found+=1
    assert found==1,(point,net,found)
    return text
