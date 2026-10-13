# Passes 03+: values from sources/passNN/values.csv (model,field,value,source). IFU > brochure: rank by 'IFU' in source.
import glob as _g,csv as _c,json as _j
_conf=[];_app=[]
rk=lambda s:2 if 'IFU' in s else 1
for f in sorted(set(_g.glob('sources/passSH*/values.csv'))):
    pn=f.split('/')[1]
    for v in _c.DictReader(open(f)):
        r=byname.get(v['model'])
        if not r: print('NO ROW',v['model']);continue
        cur=r.get(v['field'],'');cs=prov[v['model']].get(v['field'],'')
        if cur and cur!=v['value']:
            _conf.append({'pass':pn,**v,'existing':cur,'existing_source':cs})
            if not (rk(v['source'])>rk(cs)): continue
        r[v['field']]=v['value'];prov[v['model']][v['field']]=v['source'];_app.append({'pass':pn,**v})
_j.dump(_conf,open('sources/conflicts_passes.json','w'),indent=1);_j.dump(prov,open('provenance.json','w'))
print('passes applied',len(_app),'conflicts',len(_conf))
