import json,csv,re,urllib.request,urllib.parse,time
from fam import F,CAT
rows=list(csv.DictReader(open('structural-specs-verified.csv')));cats=json.load(open('raw/catalogs.json'))
def get(q):
    try: return json.load(urllib.request.urlopen('https://api.fda.gov/device/recall.json?search='+urllib.parse.quote(q)+'&limit=100',timeout=60))['results']
    except Exception: return []
out=[];per={}
for r in rows:
    m=r['model'];ids={x for p in cats.get(m,[]) for x in p if x and len(x)>=5}
    if not ids: per[m]=0;continue
    base=re.sub(r'^(NES|Vein360) Reprocessed ','',m).split(' RX')[0]
    qs=['product_description:"%s"'%base]+['pma_numbers:%s'%s if s.startswith('P') else 'k_numbers:%s'%s for s in r['fda_submission'].split(', ') if s]
    seen={}
    for q in qs:
        for x in get(q): seen[x['res_event_number']+x.get('product_res_number','')]=x
        time.sleep(.25)
    hits=[]
    for x in seen.values():
        txt=(x.get('code_info','')+' '+x.get('product_description',''))
        mt=sorted(i for i in ids if (i in txt) and re.search(r'(?<![A-Za-z0-9])'+re.escape(i)+r'(?![A-Za-z0-9])',txt))
        if mt: hits.append((x,mt))
    for x,mt in hits:
        out.append({'manufacturer':r['manufacturer'],'model':m,'category':r['category'],'recall_number':x.get('product_res_number',''),'event':x.get('res_event_number',''),
          'recalling_firm':x.get('recalling_firm',''),'status':x.get('recall_status',''),'date':x.get('event_date_initiated',''),'reason':(x.get('reason_for_recall','') or '')[:300],
          'matched_catalogs':'; '.join(mt[:20])+(' …' if len(mt)>20 else ''),'n_matched':len(mt),'source':'openFDA device recall API https://api.fda.gov/device/recall.json?search=product_res_number:"%s"'%x.get('product_res_number','')})
    per[m]=len(hits);print(m,len(seen),len(hits))
import os
if os.path.exists('raw/recall_manual.csv'):  # FDA Early Alerts / safety comms not yet in openFDA (exact model, source URL in 'source')
    for x in csv.DictReader(open('raw/recall_manual.csv')):
        if not any(o['model']==x['model'] and o['recall_number']==x['recall_number'] for o in out): out.append(x); per[x['model']]=per.get(x['model'],0)+1
F2=list(out[0].keys()) if out else ['model']
with open('structural-recalls.csv','w',newline='') as f:
    w=csv.DictWriter(f,F2);w.writeheader();w.writerows(out)
json.dump(per,open('raw/recall_counts.json','w'))
