import json,urllib.request,urllib.parse
def q(ep,s):
    try: return json.load(urllib.request.urlopen(f'https://api.fda.gov/device/{ep}.json?search='+urllib.parse.quote(s)+'&limit=100',timeout=60))['results']
    except Exception: return []
P={'XIENCE Skypoint':'trade_name:"XIENCE"','Orsiro Mission':'trade_name:Orsiro','MULTI-LINK 8':'trade_name:"MULTI-LINK 8"','PK Papyrus':'trade_name:Papyrus','GRAFTMASTER RX':'trade_name:GRAFTMASTER',
 'Diamondback 360 Coronary OAS':'trade_name:Diamondback','BioFreedom':'trade_name:BioFreedom','Ringer':'trade_name:Ringer','CAT RX':'trade_name:"CAT RX"','AGENT DCB others':'generic_name:"drug coated" AND advisory_committee:CV'}
for k,s in P.items():
    R=q('pma',s);seen={}
    for r in R: seen.setdefault(r['pma_number'],(r.get('trade_name','')[:50],r['applicant'][:25],r.get('decision_date')))
    print(k,list(seen.items())[:6])
K={'GuideLiner':'device_name:GuideLiner','Heartrail':'device_name:Heartrail','Telescope':'device_name:Telescope AND applicant:Medtronic','Hyperion':'device_name:Hyperion AND applicant:Asahi',
 'Mach 1':'device_name:"Mach 1"','CAT RX':'device_name:"CAT RX"','SION':'device_name:SION','Gaia':'device_name:Gaia','Confianza':'device_name:Confianza','Fielder':'device_name:Fielder',
 'BALANCE':'device_name:"BALANCE MIDDLEWEIGHT"','PILOT':'device_name:"HI-TORQUE" AND device_name:PILOT','Runthrough':'device_name:Runthrough','Guidezilla':'device_name:Guidezilla','Mamba':'device_name:Mamba',
 'Finecross':'device_name:Finecross','Caravel':'device_name:Caravel','Corsair':'device_name:Corsair','OptiCross':'device_name:OptiCross','Dragonfly':'device_name:Dragonfly','COMET':'device_name:Comet AND applicant:Boston','PressureWire':'device_name:PressureWire','AngioJet AVX':'device_name:AVX',
 'AltaView':'device_name:AltaView','Vista Brite':'device_name:"Vista Brite"','ROTAPRO':'device_name:ROTAPRO'}
for k,s in K.items():
    R=sorted(q('510k',s),key=lambda r:r['decision_date'],reverse=True)
    print(k,[(r['k_number'],r['device_name'][:40],r['decision_date']) for r in R[:5]])
