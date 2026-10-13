#!/bin/bash
# usage: publish.sh NN
set -e; cd /workspace/structural-specs; P=$1
SITE_URL=${SITE_URL:-https://jeffmcd83.github.io/structural-compare/}; REMOTE=https://github.com/jeffmcd83/structural-compare.git; git remote get-url origin >/dev/null 2>&1 || git remote add origin $REMOTE
python3 build_master.py >/dev/null; sed -i "s/'pass':'[0-9a-z]*'/'pass':'$P'/" app/build.py; python3 app/build.py
git add -A; git commit -qm "Pass $P"; git tag preview-pass$P; git push -q origin master preview-pass$P
git subtree split --prefix site -b g2 -q; git push -q -f origin g2:gh-pages; git branch -D g2 -q
for i in $(seq 1 50); do curl -s "${SITE_URL:?set SITE_URL to the new GitHub Pages base URL}preview/data/core.json?x=$RANDOM" | grep -q "\"pass\":\"$P\"" && echo live && break; sleep 10; done
python3 tools/tl.py ${SITE_URL:?set SITE_URL to the new GitHub Pages base URL}preview/ pass$P
python3 fill.py
