import json,re,csv,collections,urllib.parse
from fam import F,CAT,THER
def num(v):
    try: return float(v)
    except: return None
def rng(vals,unit):
    v=sorted({x for x in vals if x is not None})
    if not v: return ''
    f=lambda x:('%g'%x)
    return (f(v[0]) if len(v)==1 else f'{f(v[0])}–{f(v[-1])}')+f' {unit}'+('' if len(v)<2 else f' ({len(v)} sizes)')
def lst(vals,unit):
    v=sorted({x for x in vals if x is not None}); return ', '.join('%g'%x for x in v)+(' '+unit if v else '')
rows=[];prov={};devs={}
MMX=re.compile(r'(\d+(?:\.\d+)?)\s*(?:mm)?\s*[xX×]\s*(\d+(?:\.\d+)?)\s*(?:mm)?')
for fam,(fn,brx,inc,exc) in F.items():
    R=[r for r in json.load(open(f'raw/udi/{fn}.json')) if re.search(brx,r.get('brand_name',''))]
    CO={'Safari':'LAKE REGION','Amplatz Extra Stiff':'COOK','BRK / BRK-1':'ST. JUDE','Agilis NxT':'ST. JUDE','Cougar':'MEDTRONIC','Wolverine Cutting Balloon':'BOSTON','Mamba':'BOSTON','GRAFTMASTER RX':'ABBOTT VASCULAR'}
    if fam in CO: R=[r for r in R if CO[fam] in r.get('company_name','').upper()]
    if inc: R=[r for r in R if re.search(inc,(r.get('device_description') or '')+' '+r.get('brand_name','')+' '+json.dumps(r.get('device_sizes')))]
    if exc: R=[r for r in R if not re.search(exc,(r.get('device_description') or '')+' '+r.get('brand_name',''))]
    cat=CAT[fam]; reproc=fam.startswith(('NES ','Vein360'))
    S=collections.defaultdict(list); cats=set(); dis=[]; subs=set(); pc=set(); comp=collections.Counter()
    for r in R:
        cats.add(r.get('catalog_number') or r.get('version_or_model_number') or '')
        di=[i['id'] for i in r.get('identifiers',[]) if i.get('type')=='Primary']; dis+=di
        comp[r.get('company_name','')]+=1
        for p in r.get('premarket_submissions') or []: subs.add(p['submission_number'])
        for p in r.get('product_codes') or []: pc.add(p['code'])
        for s in r.get('device_sizes') or []:
            t=s['type'];u=s.get('unit') or '';v=num(s.get('value'))
            if t=='Device Size Text, specify':
                m=MMX.search(s.get('text') or s.get('value') or '')
                if m and cat in('DES','BMS','Covered stent','DCB','Balloon'): S['dia'].append(float(m.group(1)));S['len'].append(float(m.group(2)))
                continue
            if v is None: continue
            if cat in('Mitral TEER','Tricuspid TEER') and u=='Millimeter' and t in('Width','Length','Depth'):
                S[{'Depth':'cw','Length':'al','Width':'gw_'}[t]].append(v);continue
            if cat=='TAVI valve' and t=='Outer Diameter' and u=='Millimeter' and v>=18: S['vs'].append(v);continue
            if cat=='Valve wire' and t=='Outer Diameter' and u=='Inch': S['wire'].append(v);continue
            if t in('Stent Diameter','Balloon Diameter') or (t=='Outer Diameter' and u=='Millimeter' and cat in('DES','BMS','Balloon')): S['dia'].append(v)
            elif t in('Stent Length','Balloon Length') or (t=='Length' and u=='Millimeter' and cat in('DES','BMS','Balloon','Covered stent')): S['len'].append(v)
            elif t=='Catheter Gauge': S['fr'].append(v)
            elif t in('Length','Catheter Length','Catheter Working Length','Shaft Length','Guidewire Length') and u=='Centimeter': S['lcm'].append(v)
            elif t in('Outer Diameter','Guidewire Diameter') and u=='Inch' and cat in('Guidewire','Imaging & physiology') and t=='Outer Diameter' or (t=='Guidewire Diameter' and cat=='Guidewire'): S['wire'].append(v)
            elif t=='Guidewire Diameter': S['gw'].append(v if u=='Inch' else round(v/25.4,3))
            elif t=='Introducer Sheath Compatibility': S['sheath'].append(v)
            elif t=='Atherectomy Rotating Component Diameter': S['burr'].append(v)
            elif t=='Lumen/Inner Diameter' and u=='Millimeter': S['id'].append(v)
            elif t=='Balloon Nominal (Inflation) Pressure': S['nom'].append(v)
        dd=(r.get('device_description') or '')+' '+(r.get('catalog_number') or '')
        if cat=='TAVI valve':
            m=re.search(r'(?:\(|\b|THV |Size |, )(\d{2})\s*MM|(?:-|FX|PLUS-?|TF|RSL|NV[RT][OR]-)(\d{2})(?:A|US)?\b',dd,re.I)
            if m and 'DELIV' not in dd.upper() and 'LOADING' not in dd.upper() and 'Delivery' not in dd: S['vs'].append(float(m.group(1) or m.group(2)))
        if cat=='Valvuloplasty balloon':
            m=re.search(r'(\d+(?:\.\d+)?)\s*mm\s*x\s*(\d+(?:\.\d+)?)\s*cm',dd)
            if m: S['dia'].append(float(m.group(1)));S['len'].append(float(m.group(2))*10)
        if cat in('Large-bore sheath','Transseptal access','Steerable guide/sheath','Large-bore closure','Cerebral embolic protection'):
            for m in re.finditer(r'(?<![\d.])(\d{1,2}(?:\.\d)?)\s?F(?:r|R)?\b',(r.get('device_description') or '')): S['fr'].append(float(m.group(1)))
        if cat in('DES','BMS','Balloon','DCB','Covered stent') and not S['dia']:
            m=MMX.search(r.get('device_description') or '')
            if m and float(m.group(1))<6: S['_ddia'].append(float(m.group(1)));S['_dlen'].append(float(m.group(2)))
    if not R: subs=set()
    man=comp.most_common(1)[0][0] if comp else ''
    q='https://api.fda.gov/device/udi.json?search='+urllib.parse.quote(f'brand_name:"{R[0]["brand_name"]}"') if R else ''
    gsrc=f'GUDID (FDA AccessGUDID via openFDA UDI) — {len(R)} device identifiers, brand "{R[0]["brand_name"] if R else ""}"; record-level device_sizes; {q}'
    def ap(s):
        return f'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id={s}' if s.startswith(('P','H')) else f'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={s}'
    o={'category':cat,'manufacturer':man,'model':fam,'reprocessed':'Yes (third-party 510(k))' if reproc else 'No',
       'n_skus':str(len(R)) if R else '','catalog_numbers':'; '.join(sorted(c for c in cats if c))[:4000],
       'fda_submission':', '.join(sorted(subs)),'product_code':', '.join(sorted(pc)),
       'diameters_mm':lst(S['dia'] or S['_ddia'],'mm'),'lengths_mm':lst(S['len'] or S['_dlen'],'mm'),
       'french_sizes':lst(S['fr'],'Fr'),'length_cm':lst(S['lcm'],'cm'),'wire_diameter_in':lst(S['wire'],'in'),
       'guidewire_compat_in':lst(S['gw'],'in'),'sheath_compat_fr':lst(S['sheath'],'Fr'),'burr_sizes_mm':lst(S['burr'],'mm'),
       'inner_diameter_mm':lst(S['id'],'mm'),'nominal_pressure_atm':lst(S['nom'],'atm'),'valve_sizes_mm':lst(S['vs'],'mm'),'clip_width_mm':lst(S['cw'],'mm'),'arm_length_mm':lst(S['al'],'mm'),'grasping_width_mm':lst(S['gw_'],'mm'),'therapy':THER[cat]}
    p={}
    for k in o:
        if k in('category','model','reprocessed','therapy') or not o[k]: continue
        if k=='fda_submission': p[k]='FDA premarket database via GUDID premarket_submissions; '+' ; '.join(ap(s) for s in sorted(subs)[:3])
        elif k in('diameters_mm','lengths_mm') and not (S['dia'] or S['len']): p[k]=gsrc.replace('record-level device_sizes','parsed from GUDID device_description "D x L" text')
        else: p[k]=gsrc
    rows.append(o);prov[fam]=p;devs[fam]=R
json.dump(prov,open('provenance.json','w'),indent=0)
json.dump({k:[(r.get('catalog_number'),r.get('version_or_model_number'))+tuple(i['id'] for i in r.get('identifiers',[])) for r in v] for k,v in devs.items()},open('raw/catalogs.json','w'))
SPEC={'DES':['drug','drug_dose','polymer','strut_thickness_um','platform_alloy','crossing_profile_in','max_expansion_mm','nominal_pressure_atm','rbp_atm','delivery_length_cm','guide_compat'],
'BMS':['platform_alloy','strut_thickness_um','crossing_profile_in','nominal_pressure_atm','rbp_atm','delivery_length_cm'],'Covered stent':['covering_material','platform_alloy','crossing_profile_in','delivery_length_cm','guide_compat'],
'DCB':['drug','coating_excipient','drug_dose'],'Balloon':['balloon_type','compliance','nominal_pressure_atm','rbp_atm','crossing_profile_in','tip_profile_in','shaft_length_cm'],
'Guide catheter':['curves','inner_diameter_in','side_holes'],'Guidewire':['tip_load_gf','core_material','coating','wire_use'],
'Microcatheter':['tip_od_fr','shaft_od_fr','inner_diameter_in','marker_bands'],'Guide extension':['inner_diameter_in','outer_diameter_in','guide_compat_fr'],
'Atherectomy & IVL':['mechanism','pulses_or_runs','rbp_atm','crossing_profile_in','tip_profile_in','guide_compat'],'Imaging & physiology':['modality','frequency_mhz','pullback_speed','physiology_indices'],
'Thrombectomy':['mechanism','aspiration_lumen_in'],
'TAVI valve':['expansion_type','annulus_range_mm','frame_material','leaflet_tissue','skirt','delivery_system','delivery_profile','sheath_compat','access_routes','approval_indications'],
'Valve wire':['tip_config','stiffness','core_material','coating','wire_use'],
'Large-bore sheath':['sheath_type','sheath_id_od','compatible_devices','coating'],
'Cerebral embolic protection':['filter_config','delivery_sheath','access_routes','vessel_range','approval_indications'],
'Valvuloplasty balloon':['nominal_pressure_atm','rbp_atm','shaft_length_cm','sheath_compat','guidewire_compat_in','approval_indications'],
'Large-bore closure':['mechanism','closure_range','sheath_compat','approval_indications'],
'Temporary pacing':['electrode_config','fixation','sheath_compat','approval_indications'],
'Mitral TEER':['implant_sizes','independent_grasping','delivery_system','guide_size_fr','access_routes','approval_indications'],
'Tricuspid TEER':['implant_sizes','independent_grasping','delivery_system','guide_size_fr','access_routes','approval_indications'],
'Transseptal access':['puncture_mechanism','needle_curves','sheath_compat','compatible_devices'],
'Steerable guide/sheath':['curves','deflection','inner_diameter_fr','compatible_devices']}
allspec=[];[allspec.append(x) for v in SPEC.values() for x in v if x not in allspec]
# conservative name-derived values
for o in rows:
    m=o['model'];p=prov[o['model']]
    def setv(k,v,why): o[k]=v;p[k]=why
    if o['category']=='Balloon':
        if 'Wolverine' in m: setv('balloon_type','Cutting','Brand name / GUDID product code')
        elif 'AngioSculpt' in m: setv('balloon_type','Scoring','Brand name / GUDID brand "AngioSculpt PTCA RX Scoring Balloon Catheter"')
        else: setv('balloon_type','PTCA dilatation','GUDID product code LOX (PTCA catheter)' if 'LOX' in o['product_code'] else 'Brand name')
        if m.startswith('NC '): setv('compliance','Non-compliant','Brand name prefix "NC" (manufacturer designation)')
    if o['category']=='Atherectomy & IVL':
        mech={'ROTAPRO':'Rotational','Diamondback':'Orbital','ELCA':'Excimer laser','Shockwave':'Intravascular lithotripsy'}
        for k,v in mech.items():
            if k in m: setv('mechanism',v,'FDA product code / device classification name for '+o['product_code'])
    if o['category']=='Imaging & physiology':
        mod='IVUS (solid-state)' if 'Eagle' in m else 'IVUS (rotational)' if m in('Refinity ST','OptiCross HD') else 'OCT' if 'Dragonfly' in m else 'Pressure wire' if m in('OmniWire','PressureWire X','COMET II') else 'Pressure microcatheter' if 'Navvus' in m else ''
        if mod: setv('modality',mod,'GUDID brand name / FDA product code '+o['product_code'])
byname={r['model']:r for r in rows}  # coronary pass02 not applicable
exec(open('passes_apply.py').read())
# STANDING_DECISIONS 2026-10-13: exclude devices not labeled for coronary use
EXCLUDE={"AngioJet AVX"}  # AV-access grafts/fistulae only (BSC US AngioJet page)
rows=[r for r in rows if r.get("model") not in EXCLUDE]
for r in rows: r['therapy']=THER.get(r['category'],'Coronary')
FIELDS=['therapy','category','manufacturer','model','n_skus','catalog_numbers','fda_submission','product_code','diameters_mm','lengths_mm','french_sizes','length_cm','wire_diameter_in','guidewire_compat_in','sheath_compat_fr','burr_sizes_mm','inner_diameter_mm','valve_sizes_mm','clip_width_mm','arm_length_mm','grasping_width_mm']+[x for x in allspec if x!='inner_diameter_mm']
FIELDS=list(dict.fromkeys(FIELDS))
with open('structural-specs-verified.csv','w',newline='') as f:
    w=csv.DictWriter(f,FIELDS);w.writeheader();[w.writerow({k:r.get(k,'') for k in FIELDS}) for r in rows]
SPEC={c:SPEC[c] for c in set(CAT.values())};json.dump(SPEC,open('spec_by_cat.json','w'));json.dump(THER,open('therapy_by_cat.json','w'))
for r in rows: r={k:r.get(k,'') for k in FIELDS};print(r['category'][:12],'|',r['model'][:30],'|',r['manufacturer'][:25],r['n_skus'],r['fda_submission'][:30],r['diameters_mm'][:40],r['french_sizes'][:30],r['length_cm'][:30],r['wire_diameter_in'][:20])
