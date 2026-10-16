import sys
from playwright.sync_api import sync_playwright
U=sys.argv[1];T=sys.argv[2];A='/workspace/structural-specs/app/'
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome');errs=[]
  for vp,n in [({'width':1300,'height':900},'desk'),({'width':390,'height':844},'mob')]:
    pg=b.new_context(viewport=vp).new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    lab=lambda: pg.locator('th.a',has_text='Reprocessed').count()
    # SH: reprocessing attribute removed (no TAVI reprocessing) -> assert label absent in every category
    pg.goto(U);pg.wait_for_timeout(2000);cats=pg.evaluate("fetch('data/core.json').then(r=>r.json()).then(d=>[...new Set((d.rows||d.devices||[]).map(x=>x.category))])")
    bad=[]
    for c in cats:
      pg.goto(U+'#c='+c.replace(' ','%20').replace('&','%26'));pg.reload();pg.wait_for_timeout(1200)
      if lab(): bad.append(c)
    print(n,'categories',len(cats),'reprocessed label present in',bad)
    pg.goto(U+'#c=TAVI%20valve');pg.reload();pg.wait_for_timeout(2000)
    for v in ['cmp','stk','dsk']:
      pg.select_option('#vw',v);pg.wait_for_timeout(300)
      pg.click('.pk .x[data-i="1"]');pg.wait_for_timeout(400)
      cols=pg.locator('thead th').count();slots=pg.locator('thead th.slot').count();pg.screenshot(path=A+f'{T}-slot-removed-{v}-{n}.png')
      for i in range(pg.locator('.pk .x').count()): pg.click(f'.pk .x[data-i="{i}"]')
      pg.wait_for_timeout(400);ca=pg.locator('thead th').count();rows=pg.locator('tbody tr').count();pg.screenshot(path=A+f'{T}-all-empty-{v}-{n}.png')
      print(n,v,'cols',cols,'slots',slots,'| all-empty cols',ca,'rows',rows)
      pg.goto(U+'#c=TAVI%20valve&m=');pg.evaluate('location.hash="c=TAVI%20valve"');pg.reload();pg.wait_for_timeout(1500)
  print('errors',errs)
# Desktop sticky-label check (1440px, every therapy/category, all + diff mode): see tools/tsticky.py
import subprocess as _sp;_sp.run([sys.executable,'/workspace/structural-specs/tools/tsticky.py',U,T])
_sp.run([sys.executable,'/workspace/structural-specs/tools/tnav.py',U])
_sp.run([sys.executable,'/workspace/structural-specs/tools/tfeat.py',U])
