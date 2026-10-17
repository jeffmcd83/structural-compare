# Verify every study link: PMC pages must load (200) and show the article title; PubMed-only items
# (PubMed blocks automated fetches from this network with 403/203) are verified via NCBI E-utilities record + doi.org redirect.
import csv,json,urllib.request,re,html,time
rows=list(csv.DictReader(open('/workspace/structural-specs/sources/passSH11/study.csv')));bad=[];n=0
S=json.load(urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id='+','.join(sorted({r['pmid'] for r in rows}))))['result']
norm=lambda s:re.sub(r'[^a-z0-9]','',html.unescape(re.sub('<[^>]+>','',s)).lower())
seen=set()
for r in rows:
  if r['url'] in seen: continue
  seen.add(r['url']);n+=1;t=norm(S[r['pmid']]['title'])[:40]
  if not t: bad.append((r['url'],'no pubmed record'));continue
  if 'pmc.ncbi' in r['url']:
    ok=False
    for k in range(4):
      try:
        x=urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=40);b=x.read().decode('utf8','replace')
        m=re.search(r'citation_title" content="([^"]+)',b)
        if x.status==200 and m: ok=norm(m.group(1))[:30]==t[:30];break
      except Exception as e: pass
      time.sleep(3)
    if not ok: bad.append((r['url'],'not verified'))
  else:
    try:
      req=urllib.request.Request('https://doi.org/api/handles/'+r['doi']);j=json.load(urllib.request.urlopen(req,timeout=30))
      if j.get('responseCode')!=1: bad.append((r['url'],'doi unresolved'))
    except Exception as e: bad.append((r['url'],'doi '+str(e)))
  time.sleep(0.4)
print('links',n,'bad',bad)
