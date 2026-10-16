# Sticky label test: Desktop view, 1440px. Every first-column label cell (tbody th.a, section header th) must keep the same
# viewport x after horizontal scroll, and be opaque, in every therapy/category, with all supplier columns + extra width.
import sys;U=sys.argv[1];T=sys.argv[2] if len(sys.argv)>2 else 'x'
from playwright.sync_api import sync_playwright
JS="""()=>{const m=document.querySelector('main');const L=[...document.querySelectorAll('tbody th.a, tbody tr.sh th')].filter(e=>e.offsetParent);
const x0=L.map(e=>e.getBoundingClientRect().left);const mx=m.scrollWidth-m.clientWidth;m.scrollLeft=mx;
return new Promise(r=>requestAnimationFrame(()=>{const bad=[];L.forEach((e,i)=>{const b=e.getBoundingClientRect(),cs=getComputedStyle(e);
 const vis=b.top<innerHeight&&b.bottom>0; const bg=cs.backgroundColor;const op=!(bg==='transparent'||/rgba\\(.*, 0\\)$/.test(bg));
 if(Math.abs(b.left-x0[i])>1||!op) bad.push([e.textContent.trim().slice(0,30),Math.round(x0[i]),Math.round(b.left),bg,cs.position])});
 // vertical: scroll down, labels still pinned left
 m.scrollTop=m.scrollHeight;requestAnimationFrame(()=>{L.forEach((e,i)=>{const b=e.getBoundingClientRect();if(b.bottom>0&&b.top<innerHeight&&Math.abs(b.left-x0[i])>1)bad.push(['V:'+e.textContent.trim().slice(0,26),Math.round(x0[i]),Math.round(b.left)])});
 m.scrollLeft=0;m.scrollTop=0;r({n:L.length,mx,bad})})}))}"""
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':1440,'height':900}).new_page();errs=[]
  pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto(U);pg.wait_for_timeout(2500);pg.select_option('#vw','dsk');pg.add_style_tag(content='body.dsk table{min-width:2400px!important}')  # force horizontal overflow
  tot=0;fails=[]
  for t in ['all']:
    for c in pg.eval_on_selector_all('#cat option','o=>o.map(x=>x.value)'):
      pg.select_option('#cat',c);pg.wait_for_timeout(400)
      for diff in [False,True]:
        pg.set_checked('#diff',diff);pg.wait_for_timeout(200)
        r=pg.evaluate(JS);tot+=r['n']
        if r['bad']: fails.append((t,c,'diff' if diff else 'all',r['bad'][:4],len(r['bad'])))
      pg.set_checked('#diff',False)
  pg.select_option('#cat','TAVI valve');pg.wait_for_timeout(500)
  pg.evaluate("document.querySelector('main').scrollLeft=600");pg.wait_for_timeout(300);pg.screenshot(path=f'/workspace/structural-specs/app/{T}-sticky-scrolled.png')
  print('label cells checked',tot,'failing groups',len(fails))
  for f in fails[:12]: print(' ',f)
  print('errors',errs)
