import json,urllib.request,urllib.parse,sys
for h in sys.argv[1:]:
    u='https://api.fda.gov/device/udi.json?search='+urllib.parse.quote(h)+'&count=brand_name.exact&limit=15'
    try: d=json.load(urllib.request.urlopen(u,timeout=60))['results'];print(h,'=>',[(x['term'],x['count']) for x in d])
    except Exception as e: print(h,'=> none',e)
