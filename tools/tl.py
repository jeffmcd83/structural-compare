# Supplier-column test: fixed supplier pickers per category, each with that supplier's products only
import sys,json;U=sys.argv[1];T=sys.argv[2]
from playwright.sync_api import sync_playwright
ORDER=['Edwards','Medtronic','Abbott','Boston Scientific']
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome');errs=[];bad=[]
  for vp,n in [({'width':1300,'height':900},'desk'),({'width':390,'height':844},'mob')]:
    pg=b.new_context(viewport=vp).new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(U);pg.wait_for_timeout(2500);D=pg.evaluate("fetch('data/core.json').then(r=>r.json())")
    cats=sorted({r['category'] for r in D['rows']});nc=0
    for c in cats:
      pg.goto(U+'#c='+c.replace(' ','%20').replace('&','%26'));pg.reload();pg.wait_for_timeout(900)
      exp={};[exp.setdefault(r.get('supplier'),[]).append(r['model']) for r in D['rows'] if r['category']==c]
      vs=pg.eval_on_selector_all('.pk','e=>e.map(x=>x.dataset.v)')
      known=[v for v in vs if v in ORDER]
      if sorted(vs)!=sorted(exp) or known!=[o for o in ORDER if o in exp] or vs[:len(known)]!=known: bad.append((n,c,'suppliers',vs,list(exp)))
      for i,v in enumerate(vs):
        o=pg.eval_on_selector_all(f'.pk select[data-i="{i}"] option','e=>e.map(x=>x.value).filter(Boolean)')
        if sorted(o)!=sorted(exp[v]): bad.append((n,c,v,o))
      ths=pg.locator('thead th').count()
      if ths!=len(vs)+1: bad.append((n,c,'cols',ths))
      nc+=1
    # choose a non-default product and clear one supplier
    pg.goto(U+'#c=TAVI%20valve');pg.reload();pg.wait_for_timeout(1200)
    o=pg.eval_on_selector_all('.pk select[data-i="0"] option','e=>e.map(x=>x.value).filter(Boolean)')
    pg.select_option('.pk select[data-i="0"]',o[-1]);pg.wait_for_timeout(400)
    ok=pg.locator('thead th').nth(1).inner_text().find(o[-1])>=0
    pg.click('.pk .x[data-i="1"]');pg.wait_for_timeout(400);slot=pg.locator('thead th.slot').count()
    pg.screenshot(path=f'/workspace/structural-specs/app/{T}-suppliers-{n}.png')
    print(n,'categories',nc,'pick ok',ok,'cleared->slot',slot)
  print('mismatches',bad);print('errors',errs)
