import random,time,os,sys
from operator import add
from functools import reduce
from array import array
print(os.cpu_count(), getattr(sys,'_is_gil_enabled',lambda:None)())
r=random.Random(7);xs=[r.uniform(0,1) for _ in range(3000)];w=300
def _part(fs,lo,hi,w):
    return array('d',[reduce(add,fs[i:i+w],0.0)/w for i in range(lo,hi)])
def f4(xs,w,k=4):
    n=len(xs)-w+1
    fs=list(map(float,xs))
    cuts=[n*t//k for t in range(k+1)]
    kids=[]
    for t in range(1,k):
        rd,wr=os.pipe()
        pid=os.fork()
        if pid==0:
            os.close(rd)
            data=_part(fs,cuts[t],cuts[t+1],w).tobytes()
            with os.fdopen(wr,'wb') as f: f.write(data)
            os._exit(0)
        os.close(wr);kids.append((pid,rd))
    out=_part(fs,cuts[0],cuts[1],w).tolist()
    for pid,rd in kids:
        with os.fdopen(rd,'rb') as f: b=f.read()
        os.waitpid(pid,0)
        a=array('d');a.frombytes(b);out+=a.tolist()
    return out
def o(xs,w):
    out=[]
    for i in range(len(xs)-w+1):
        t=0.0
        for j in range(i,i+w): t=t+float(xs[j])*1.0
        out.append(t/w)
    return out
ref=o(xs,w)
for f in (o,f4):
    best=9
    for _ in range(5):
        s=time.perf_counter();res=f(xs,w);best=min(best,time.perf_counter()-s)
    print(f.__name__,best,res==ref)
