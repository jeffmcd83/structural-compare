# Combined therapy/category dropdown: order, labels, default, deep links, old-URL mapping, valve-position filter
import sys;U=sys.argv[1]
from playwright.sync_api import sync_playwright
G=['TAVI','Mitral TEER','Tricuspid TEER','Mitral TMVR','Tricuspid TTVR','LAAO','Shared accessories']
bad=[];errs=[]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
  for vp,n in [({'width':1440,'height':900},'desk'),({'width':390,'height':844},'mob')]:
    ctx=b.new_context(viewport=vp);pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(U);pg.wait_for_timeout(2500)
    groups=pg.eval_on_selector_all('#cat optgroup','g=>g.map(x=>[x.label,[...x.querySelectorAll("option")].map(o=>[o.value,o.textContent])])')
    if [g[0] for g in groups]!=G: bad.append((n,'group order',[g[0] for g in groups]))
    for t,os in groups:
      for v,l in os:
        SH={'Mitral TEER':'M-TEER','Tricuspid TEER':'T-TEER','Mitral TMVR':'TMVR','Tricuspid TTVR':'TTVR','Shared accessories':'Shared'}
        if not (l.startswith(t+' – ') if n=='desk' else l.startswith(SH.get(t,t)+' – ')): bad.append((n,'label',v,l))
    tav=[l for v,l in groups[0][1]]
    if tav[:4]!=['TAVI – Valves','TAVI – Valve wires','TAVI – Large-bore sheaths','TAVI – Embolic protection']: bad.append((n,'TAVI order',tav))
    if pg.locator('#th').count(): bad.append((n,'old therapy select still present'))
    if pg.input_value('#cat')!='TAVI valve': bad.append((n,'default',pg.input_value('#cat')))
    if not pg.locator('#vp').is_visible(): bad.append((n,'vp hidden on TAVI valves'))
    # new deep link round-trip
    pg.select_option('#cat','LAAO device');pg.wait_for_timeout(500)
    o=pg.eval_on_selector_all('.pk select[data-i="0"] option','e=>e.map(x=>x.value).filter(Boolean)');pg.select_option('.pk select[data-i="0"]',o[-1]);pg.wait_for_timeout(400)
    h=pg.evaluate('location.hash');pg2=ctx.new_page();pg2.goto(U+h);pg2.wait_for_timeout(2000)
    if pg2.input_value('#cat')!='LAAO device' or pg2.input_value('.pk select[data-i="0"]')!=o[-1]: bad.append((n,'deep link',h))
    if pg2.locator('#vp').is_visible(): bad.append((n,'vp visible on LAAO'))
    # old URLs
    for old,exp_c,exp_m in [('#t=LAAO','LAAO device',None),('#t=Mitral%20TEER','Mitral TEER',None),
      ('#t=TAVI&c=TAVI%20valve&m=Navitor~SAPIEN%203~~','TAVI valve',{'Abbott':'Navitor','Edwards':'SAPIEN 3'}),
      ('#t=TAVI&c=Large-bore%20sheath','Large-bore sheath',None)]:
      pg3=ctx.new_page();pg3.goto(U+old);pg3.wait_for_timeout(2000);c=pg3.input_value('#cat')
      if c!=exp_c: bad.append((n,'old url',old,c))
      if exp_m:
        got={pg3.eval_on_selector(f'.pk:nth-child({i+1})','e=>e.dataset.v'):pg3.input_value(f'.pk select[data-i="{i}"]') for i in range(pg3.locator('.pk').count())}
        for k,v in exp_m.items():
          if got.get(k)!=v: bad.append((n,'old url models',old,got))
      pg3.close()
    pg2.close()
    print(n,'groups',len(groups),'options',sum(len(g[1]) for g in groups))
  print('mismatches',bad);print('errors',errs)
