import csv,json
rows=list(csv.DictReader(open('structural-specs-verified.csv')));SPEC=json.load(open('spec_by_cat.json'))
src=open('app/build.py').read();SIZE=eval(src.split('SIZE=')[1].split('\nTHER')[0])
tot=fil=0;per={}
for r in rows:
    fs=list(dict.fromkeys(['manufacturer','n_skus','fda_submission','product_code','catalog_numbers']+SIZE[r['category']]+SPEC[r['category']]))
    n=sum(1 for f in fs if r.get(f));tot+=len(fs);fil+=n;a=per.setdefault(r['category'],[0,0]);a[0]+=n;a[1]+=len(fs);t=per.setdefault('['+r.get('therapy','Coronary')+']',[0,0]);t[0]+=n;t[1]+=len(fs)
print('FILL',fil,tot,round(100*fil/tot,1),{k:round(100*a/b) for k,(a,b) in per.items()})
