import sys;U=sys.argv[1];T=sys.argv[2]
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome');errs=[]
  for vp,n in [({'width':1300,'height':900},'desk'),({'width':390,'height':844},'mob')]:
    pg=b.new_context(viewport=vp).new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(U);pg.wait_for_timeout(2500)
    ths=pg.eval_on_selector_all('#th option','o=>o.map(x=>x.value)')
    for t in ths:
      pg.select_option('#th',t);pg.wait_for_timeout(400)
      cats=pg.eval_on_selector_all('#cat option','o=>o.map(x=>x.value)')
      print(n,t,'->',cats)
      for v in ['cmp','stk','dsk']:
        pg.select_option('#vw',v);pg.wait_for_timeout(300)
        for i in range(min(2,pg.locator('.pk select').count())):
          o=pg.eval_on_selector_all(f'.pk select[data-i="{i}"] option','e=>e.map(x=>x.value).filter(Boolean)')
          if o: pg.select_option(f'.pk select[data-i="{i}"]',o[-1]);pg.wait_for_timeout(300)
        rows=pg.locator('table tr:visible').count()
        print('  ',v,'rows',rows)
        if t!='Coronary': pg.screenshot(path=f'/workspace/structural-specs/app/{T}-{t.replace(" ","_")}-{v}-{n}.png',full_page=(v!='dsk'))
  print('errors',errs)
