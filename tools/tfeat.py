# Tests: header search (aliases, grouping, pick -> category + supplier column) and compatibility view (sourced only).
import sys,json,urllib.request
from playwright.sync_api import sync_playwright
U=sys.argv[1];bad=[];errs=[]
D=json.loads(urllib.request.urlopen(U+'data/core.json').read())
CASES=[('S3UR','TAVI valve','SAPIEN 3 Ultra RESILIA','Edwards'),('FX+','TAVI valve','Evolut FX+','Medtronic'),('flx pro','LAAO device','WATCHMAN FLX Pro','Boston Scientific'),('Amulet','LAAO device','Amplatzer Amulet','Abbott'),('proglide','Large-bore closure','Perclose ProGlide','Abbott'),('TriClip G4','Tricuspid TEER','TriClip G4','Abbott')]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
  for n,vp in [('desk',{'width':1440,'height':900}),('mob',{'width':390,'height':844})]:
    pg=b.new_page(viewport=vp);pg.on('pageerror',lambda e:errs.append(str(e)))
    for q,c,m,s in CASES:
      pg.goto('about:blank');pg.goto(U+'#');pg.wait_for_timeout(1500);pg.fill('#q',q);pg.wait_for_timeout(200)
      first=pg.eval_on_selector('#qr','e=>{const b=e.querySelector("button");return b&&[b.dataset.m,e.hidden,e.querySelector(".g").textContent]}')
      if not first or first[0]!=m or first[1]: bad.append((n,q,'first hit',first));continue
      pg.click('#qr button >> nth=0');pg.wait_for_timeout(300)
      got=pg.evaluate('s=>[document.querySelector("#cat").value,(document.querySelector(`.pk[data-v="${s}"] select`)||{}).value,location.hash]',s)
      if got[0]!=c or got[1]!=m: bad.append((n,q,'pick',got))
    pg.goto('about:blank');pg.goto(U+'#');pg.wait_for_timeout(1500);pg.fill('#q','Edwards');pg.wait_for_timeout(200)
    gs=pg.eval_on_selector_all('#qr .g','a=>a.map(x=>x.textContent)')
    if len(gs)<3: bad.append((n,'grouping',gs))
    pg.fill('#q','zzzz');pg.wait_for_timeout(100)
    if 'No matching' not in pg.inner_text('#qr'): bad.append((n,'no-match'))
    # compat
    pg.goto('about:blank');pg.goto(U+'#cp=Evolut%20FX%2B');pg.wait_for_timeout(1800)
    if not pg.evaluate('document.body.classList.contains("cpm")&&!document.querySelector("#cp").hidden'): bad.append((n,'cp deep link'))
    cards=pg.eval_on_selector_all('#cpp .cpc','a=>a.map(c=>[c.dataset.k,c.querySelectorAll(".cpi").length,!!c.querySelector(".ns"),[...c.querySelectorAll(".cpi .d")].map(d=>/Doc:/.test(d.textContent)&&/Page:/.test(d.textContent)&&/URL: https?:/.test(d.textContent))])')
    ks=[c[0] for c in cards]
    if ks!=['delivery_system','sheaths','access_routes','wires','embolic','closure','balloons']: bad.append((n,'cp fields',ks))
    for k,ni,ns,ok in cards:
      exp=len(D['compat']['Evolut FX+'][k])
      if ni!=exp or (ni==0)!=ns or not all(ok): bad.append((n,'cp card',k,ni,exp,ns,ok))
    # every device: panel items == data, each with doc/page/url; empty -> Not stated
    for m in D['compat']:
      pg.select_option('#cpsel',m);pg.wait_for_timeout(30)
      cs=pg.eval_on_selector_all('#cpp .cpc','a=>a.map(c=>[c.dataset.k,c.querySelectorAll(".cpi").length,!!c.querySelector(".ns")])')
      for k,ni,ns in cs:
        if ni!=len(D['compat'][m][k]) or (ni==0)!=ns: bad.append((n,'cp',m,k))
    # search while in compat mode switches panel
    pg.fill('#q','S3UR');pg.wait_for_timeout(150);pg.click('#qr button >> nth=0');pg.wait_for_timeout(200)
    if pg.eval_on_selector('#cpsel','e=>e.value')!='SAPIEN 3 Ultra RESILIA': bad.append((n,'search in cp'))
    pg.click('#cpb');pg.wait_for_timeout(300)
    if pg.evaluate('document.body.classList.contains("cpm")') or not pg.is_visible('#m'): bad.append((n,'cp off'))
    if pg.evaluate('document.documentElement.scrollWidth')>vp['width']+1: bad.append((n,'h-overflow'))
    print(n,'search cases',len(CASES),'compat devices',len(D['compat']))
  b.close()
# data rule: every compat item has a source with URL
for m,c in D['compat'].items():
  for k,L in c.items():
    for v,pi in L:
      if not D['ps'][pi][1]: bad.append(('data','no url',m,k))
print('mismatches',bad);print('errors',errs)
