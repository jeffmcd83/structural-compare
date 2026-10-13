import sys;U=sys.argv[1];T=sys.argv[2]
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome');errs=[]
  for vp,n in [({'width':1300,'height':900},'desk'),({'width':390,'height':844},'mob')]:
    pg=b.new_context(viewport=vp).new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(U+'#c=TAVI%20valve');pg.wait_for_timeout(2000)
    for v in ['cmp','stk','dsk']:
      pg.select_option('#vw',v);pg.wait_for_timeout(500);pg.screenshot(path=f'/workspace/structural-specs/app/live-{T}-{v}-{n}.png')
    pg.click('.pk input[data-i="3"]');pg.wait_for_timeout(300);dis=pg.locator('.pk .list .dis:visible').count()
    if dis: pg.locator('.pk .list .dis:visible').first.dispatch_event('mousedown');pg.wait_for_timeout(400)
    v=[pg.input_value(f'.pk input[data-i="{i}"]') for i in range(4)];f=[x for x in v if x]
    print(n,'disabled',dis,'dupes',len(f)-len(set(f)))
  print('errors',errs)
