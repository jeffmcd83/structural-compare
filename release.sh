#!/bin/bash
# usage: release.sh TAG  — copy current site/preview build to site/ root (live)
set -e; cd /workspace/structural-specs; T=$1
SITE_URL=${SITE_URL:-https://jeffmcd83.github.io/structural-compare/}  # root release target; run only with Jeff's approval
rm -rf site/data site/index.html site/sw.js site/favicon.svg
cp -r site/preview/data site/preview/index.html site/preview/sw.js site/preview/favicon.svg site/
sed -i "s/const P='sh-preview-',C=P+'\([0-9a-f]*\)'/const P='sh-live-',C=P+'\1-$T'/" site/sw.js
sed -i "s/'Preview · pass '/'$T · pass '/" site/index.html
