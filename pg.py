import sys,re,subprocess
f=sys.argv[1];pat=sys.argv[2];n=int(sys.argv[3]) if len(sys.argv)>3 else 40
t=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,text=True).stdout.split('\f');c=0
for i,p in enumerate(t):
    for l in p.splitlines():
        if re.search(pat,l,re.I) and c<n: print(i+1,'|',re.sub(r'\s+',' ',l).strip()[:200]);c+=1
