import json,urllib.request,urllib.parse,time,os,sys
Q={ # file -> openFDA UDI query
'SAPIEN':'brand_name:SAPIEN AND company_name:Edwards','Evolut':'brand_name:Evolut','Navitor':'brand_name:Navitor','Trilogy':'company_name:JenaValve',
'MitraClip':'brand_name:MitraClip','TriClip':'brand_name:TriClip','PASCAL_Edwards':'brand_name:PASCAL AND company_name:Edwards',
'SAFARI':'brand_name:SAFARI','Confida':'brand_name:Confida','Lunderquist':'brand_name:Lunderquist AND company_name:Cook','Amplatz_ES':'brand_name:Amplatz AND device_description:"Extra Stiff"',
'eSheath':'brand_name:eSheath','Sentrant':'brand_name:Sentrant','DrySeal':'brand_name:DrySeal','Sentinel_BSC':'brand_name:Sentinel AND company_name:Boston',
'TRUE_Dilatation':'brand_name:"TRUE DILATATION"','Z-MED':'brand_name:"Z-MED"','Perclose':'brand_name:Perclose','MANTA':'brand_name:MANTA AND company_name:Essential',
'Tempo':'brand_name:Tempo AND device_description:pacing','BRK':'brand_name:BRK','VersaCross':'brand_name:VersaCross','Agilis':'brand_name:Agilis'}
for f,q in Q.items():
    fn=f'raw/udi/SH_{f}.json'
    if os.path.exists(fn): continue
    out=[];skip=0
    while True:
        u='https://api.fda.gov/device/udi.json?search='+urllib.parse.quote(q)+'&limit=100&skip=%d'%skip
        try: d=json.load(urllib.request.urlopen(u,timeout=60))
        except Exception as e: print(f,'ERR',e);break
        out+=d['results'];skip+=100
        if skip>=d['meta']['results']['total'] or skip>=1000: break
        time.sleep(.3)
    json.dump(out,open(fn,'w'));print(f,len(out),sorted({(r.get('brand_name',''),r.get('company_name','')[:20]) for r in out})[:6])
