#!/bin/bash
# usage: release.sh TAG  — copy current site/preview build to site/ root (live)
set -e; cd /workspace/structural-specs; T=$1
SITE_URL=${SITE_URL:-https://jeffmcd83.github.io/structural-compare/}  # root release target; run only with Jeff's approval
rm -rf site/data site/index.html site/sw.js site/favicon.svg
cp -r site/preview/data site/preview/index.html site/preview/sw.js site/preview/favicon.svg site/preview/manifest.webmanifest site/
sed -i "s/const P='sh-preview-',C=P+'\([0-9a-f]*\)'/const P='sh-live-',C=P+'\1-$T'/" site/sw.js
sed -i "s/'Preview · pass '/'$T · pass '/" site/index.html
# Guides menu: this guide becomes "live" only on a root release
python3 - <<'PY'
import json
for f in ['guides.self.json','site/data/guides.json']:
    d=json.load(open(f))
    for g in (d['guides'] if 'guides' in d else [d]):
        if g.get('id')=='structural-heart': g['status']='live';g['url']='https://jeffmcd83.github.io/structural-compare/'
    json.dump(d,open(f,'w'),ensure_ascii=False)
PY
# Deploy gate: release stops (non-zero) if the promoted root build fails smoke tests; do not push on failure
python3 tools/site_gate.py site "" preview/ || { echo "ABORT: deploy gate failed on root build — do not push; restore with: git checkout -- site"; exit 1; }
