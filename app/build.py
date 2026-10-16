import json,csv,os,hashlib,re,datetime,collections
R='/workspace/structural-specs/';OUT=R+'site/preview'
os.makedirs(OUT+'/data',exist_ok=True)
rows=list(csv.DictReader(open(R+'structural-specs-verified.csv')));prov=json.load(open(R+'provenance.json'))
rec=list(csv.DictReader(open(R+'structural-recalls.csv')));SPEC=json.load(open(R+'spec_by_cat.json'))
COMMON=['family','generation','fda_approval_date','manufacturer','n_skus','fda_submission','product_code','catalog_numbers']
SIZE={'DES':['diameters_mm','lengths_mm'],'BMS':['diameters_mm','lengths_mm'],'Covered stent':['diameters_mm','lengths_mm'],'DCB':['diameters_mm','lengths_mm'],
'Balloon':['diameters_mm','lengths_mm'],'Guide catheter':['french_sizes','length_cm','inner_diameter_mm'],'Guidewire':['wire_diameter_in','length_cm'],
'Microcatheter':['french_sizes','length_cm'],'Guide extension':['french_sizes','length_cm'],'Atherectomy & IVL':['diameters_mm','burr_sizes_mm','french_sizes','sheath_compat_fr','guidewire_compat_in','length_cm','nominal_pressure_atm'],
'Imaging & physiology':['wire_diameter_in','french_sizes','sheath_compat_fr','guidewire_compat_in','length_cm'],'Thrombectomy':['french_sizes','length_cm','inner_diameter_mm'],
'TAVI valve':['valve_sizes_mm'],'Valve wire':['wire_diameter_in','length_cm'],'Large-bore sheath':['french_sizes','length_cm'],
'Cerebral embolic protection':['french_sizes','length_cm'],'Valvuloplasty balloon':['diameters_mm','lengths_mm'],'Large-bore closure':['french_sizes'],
'Temporary pacing':['french_sizes','length_cm'],'Mitral TEER':['clip_width_mm','arm_length_mm','grasping_width_mm'],'Tricuspid TEER':['clip_width_mm','arm_length_mm','grasping_width_mm'],
'TMVR valve':['valve_sizes_mm'],'TTVR valve':['valve_sizes_mm'],'LAAO device':['diameters_mm'],'LAAO access sheath':['french_sizes','length_cm','inner_diameter_mm'],'Transseptal access':['french_sizes','length_cm'],'Steerable guide/sheath':['french_sizes','length_cm']}
THER=json.load(open(R+'therapy_by_cat.json'))
SECT={c:[['Identity & regulatory',COMMON],['Sizes (GUDID)',SIZE[c]],['Specifications (OEM IFU / spec sheet)',[f for f in SPEC[c] if f not in SIZE[c]]],['Safety',['recalls']]] for c in SPEC}
LAB=lambda k:{'sheath_id_od':'Sheath ID / OD','sheath_compat':'Sheath / introducer compatibility','delivery_profile':'Delivery system profile','access_routes':'Labeled access routes','approval_indications':'FDA approval / indications','annulus_range_mm':'Annulus range (mm)','implant_sizes':'Implant sizes','independent_grasping':'Independent leaflet grasping','guide_size_fr':'Guide / sheath size (Fr)','grasping_width_mm':'Grasping width, arms open (mm)','clip_width_mm':'Clip / implant width (mm)','arm_length_mm':'Arm length (mm)','valve_position':'Valve position','family':'Product family','generation':'Generation','fda_approval_date':'FDA approval (this model)','implant_design':'Implant design','sizing_range':'Sizing (device → anatomy)','access_sheath':'Access / delivery sheath','anchoring':'Anchoring','inner_diameter_fr':'Inner diameter (Fr)','puncture_mechanism':'Puncture mechanism','needle_curves':'Needle / dilator curves','n_skus':'GUDID device count','fda_submission':'FDA PMA / 510(k) / HDE','catalog_numbers':'Catalog / model numbers','reprocessed':'Reprocessed (3rd-party 510(k))'}.get(k,(lambda m:(m.group(1).replace('_',' ').capitalize()+(' ('+{'mm':'mm','in':'in','cm':'cm','fr':'Fr','um':'µm','atm':'atm','gf':'gf','mhz':'MHz'}[m.group(2)]+')' if m.group(2) else '')))(re.match(r'(.*?)(?:_(mm|in|cm|fr|um|atm|gf|mhz))?$',k)))
PS=[];PI={}
def ps(s):
    u=(re.findall(r'https?://\S+',s) or [''])[0];t=re.sub(r'\s*;?\s*https?://\S+','',s).strip(' ;')
    k=t+'|'+u
    if k not in PI: PI[k]=len(PS);PS.append([t,u])
    return PI[k]
RC=collections.defaultdict(list)
for x in rec: RC[x['model']].append([x['recall_number'],x['date'],x['status'],x['reason'],x['matched_catalogs'],x['source'].split(' ',3)[-1] if 'http' in x['source'] else ''])
# Supplier = company that markets the device in the US (GUDID labeler shown separately as manufacturer)
SUPMAP=[('EDWARDS','Edwards'),('MEDTRONIC','Medtronic'),('ST. JUDE','Abbott'),('ABBOTT','Abbott'),('BOSTON SCIENTIFIC','Boston Scientific'),('BAYLIS','Boston Scientific'),
('COOK','Cook Medical'),('GORE','Gore'),('JENAVALVE','JenaValve'),('ESSENTIAL MEDICAL','Teleflex'),('BARD','BD'),('B BRAUN','B. Braun'),('BIO TRACE','BioTrace Medical')]
SUPMODEL={'Safari':'Boston Scientific'}  # SAFARI is a Boston Scientific product; GUDID labeler is OEM Lake Region Medical
def SUP(r):
    if r['model'] in SUPMODEL: return SUPMODEL[r['model']]
    m=r['manufacturer'].upper()
    return next((v for k,v in SUPMAP if k in m),r['manufacturer'])
SUPORDER=['Edwards','Medtronic','Abbott','Boston Scientific']
out=[]
for r in rows:
    o={k:v for k,v in r.items() if v}
    o['supplier']=SUP(r)
    o['recalls']=str(len(RC[r['model']])) if RC[r['model']] else '0 matched'
    o['_p']={k:ps(v) for k,v in prov.get(r['model'],{}).items() if r.get(k)}
    o['_p']['recalls']=ps('openFDA device recall API, exact catalog-number match in code_info; https://open.fda.gov/apis/device/recall/')
    out.append(o)
F=sorted({f for c in SECT.values() for s in c for f in s[1]})

# Compatibility panel: ONLY labeling-stated items (existing sourced cells + sources/passSH10/compat.csv). Never inferred.
ANCH={'TAVI valve','Mitral TEER','Tricuspid TEER','TMVR valve','TTVR valve','LAAO device'}
CF={'delivery_system':['delivery_system','delivery_profile'],'sheaths':['sheath_compat','access_sheath','delivery_sheath'],'access_routes':['access_routes']}
_cc=collections.defaultdict(lambda:collections.defaultdict(list))
for x in csv.DictReader(open(R+'sources/passSH10/compat.csv')):_cc[x['model']][x['field']].append([x['value'],ps(x['source'])])
COMPAT={}
for o in out:
    if o['category'] not in ANCH: continue
    c={k:[[o[f],o['_p'][f]] for f in fs if o.get(f) and f in o['_p']] for k,fs in CF.items()}
    for k in ['sheaths','wires','embolic','closure','balloons']: c.setdefault(k,[]); c[k]+=_cc[o['model']].get(k,[])
    COMPAT[o['model']]=c
core={'compat':COMPAT,'rows':out,'sect':SECT,'ther':{c:THER.get(c,'Coronary') for c in SECT},'labels':{f:LAB(f) for f in F},'ps':PS,'suporder':SUPORDER,'built':datetime.date.today().isoformat(),'pass':'sh10b'}
def dump(n,o):
    s=json.dumps(o,ensure_ascii=False,separators=(',',':'));open(f'{OUT}/data/{n}','w').write(s);return s
a=dump('core.json',core);b=dump('recalls.json',RC)
tpl=open(R+'app/template.html').read()
ver=hashlib.md5((a+b+tpl).encode()).hexdigest()[:8]
open(OUT+'/index.html','w').write(tpl.replace('__VER__',ver).replace('__BUILT__',core['built']))
open(OUT+'/favicon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#111827"/><path d="M8 34h12l5-12 8 24 6-16 4 4h13" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
open(OUT+'/manifest.webmanifest','w').write('{"name":"Structural Heart Comparison Guide","short_name":"Structural","start_url":"./","scope":"./","display":"standalone","background_color":"#111827","theme_color":"#111827","icons":[{"src":"favicon.svg","sizes":"any","type":"image/svg+xml"}]}\n')  # PWA manifest (offline/installable)
open(OUT+'/sw.js','w').write(f"const P='sh-preview-',C=P+'{ver}';self.addEventListener('install',e=>{{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(['./','./favicon.svg','./data/core.json?v={ver}'])))}});self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith(P)&&x!==C).map(x=>caches.delete(x))))));self.addEventListener('fetch',e=>{{if(e.request.method!=='GET')return;const u=new URL(e.request.url);if(u.origin!==location.origin)return;e.respondWith(caches.open(C).then(c=>fetch(e.request,{{cache:'no-cache'}}).then(r=>{{if(r.ok)c.put(e.request,r.clone());return r}}).catch(()=>c.match(e.request,{{ignoreSearch:true}}))))}});")
print('ver',ver,len(out),'rows',len(PS),'sources')

# Guides menu: merge shared /workspace/guides.json (if present) with this guide's own entry (live only after a root release)
import pathlib
_me=json.load(open(R+'guides.self.json'));_g=[]
_p=pathlib.Path('/workspace/guides.json')
if _p.exists():
    try:
        _d=json.load(open(_p));_g=_d.get('guides',_d) if isinstance(_d,dict) else _d
    except Exception as e: print('guides.json unreadable',e)
_ids=[x.get('id') for x in _g]
if _me['id'] in _ids: _g=[({**x,**{k:v for k,v in _me.items() if k not in('url','status') or x.get('status')!='live'}} if x.get('id')==_me['id'] else x) for x in _g]
else: _g=_g+[_me]
open(OUT+'/data/guides.json','w').write(json.dumps({'guides':_g,'self':_me['id'],'shared':_p.exists()},ensure_ascii=False))
print('guides menu entries',len(_g),'shared file' if _p.exists() else '(guides.json not found; own entry only)')
