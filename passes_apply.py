# Passes 03+ (optional 'approved' column: non-empty = Jeff-approved source, applied and earlier conflicts on that cell marked resolved; optional 'hold' column: hold=1 rows are logged to conflicts, never applied): values from sources/passNN/values.csv (model,field,value,source). IFU > brochure: rank by 'IFU' in source.
import glob as _g,csv as _c,json as _j
_conf=[];_app=[]
rk=lambda s:2 if 'IFU' in s else 1
for f in sorted(set(_g.glob('sources/passSH*/values.csv'))):
    pn=f.split('/')[1]
    for v in _c.DictReader(open(f)):
        r=byname.get(v['model'])
        if not r: print('NO ROW',v['model']);continue
        cur=r.get(v['field'],'');cs=prov[v['model']].get(v['field'],'')
        if (v.get('hold') or '').strip()=='1':  # SH14: held = log as conflict, never apply
            _conf.append({'pass':pn,**v,'existing':cur,'existing_source':cs});continue
        _ok=(v.get('approved') or '').strip()  # SH15: Jeff-approved source -> apply, resolve earlier conflicts on this cell
        if _ok:
            for c in _conf:
                if c['model']==v['model'] and c['field']==v['field'] and 'resolved' not in c: c['resolved']=f"{_ok}; applied in {pn}: {v['value']}"
            r[v['field']]=v['value'];prov[v['model']][v['field']]=v['source'];_app.append({'pass':pn,**v});continue
        if cur and cur!=v['value']:
            _conf.append({'pass':pn,**v,'existing':cur,'existing_source':cs})
            if not (rk(v['source'])>rk(cs)): continue
        r[v['field']]=v['value'];prov[v['model']][v['field']]=v['source'];_app.append({'pass':pn,**v})
_j.dump(_conf,open('sources/conflicts_passes.json','w'),indent=1);_j.dump(prov,open('provenance.json','w'))
print('passes applied',len(_app),'conflicts',len(_conf))
