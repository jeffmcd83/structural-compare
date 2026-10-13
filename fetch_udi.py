import json,urllib.request,urllib.parse,time,os
from seed import S
os.makedirs('raw/udi',exist_ok=True)
for c,m,f,h,db in S:
    fn='raw/udi/'+f.replace(' ','_').replace('/','_')+'.json'
    if os.path.exists(fn): continue
    out=[];skip=0
    q='brand_name:"%s"'%h
    while True:
        u='https://api.fda.gov/device/udi.json?search='+urllib.parse.quote(q)+'&limit=100&skip=%d'%skip
        try: d=json.load(urllib.request.urlopen(u,timeout=60))
        except Exception as e: break
        out+=d['results'];skip+=100
        if skip>=d['meta']['results']['total'] or skip>=1000: break
        time.sleep(.3)
    json.dump(out,open(fn,'w'));print(f,len(out),sorted({r.get('brand_name','') for r in out})[:8])
