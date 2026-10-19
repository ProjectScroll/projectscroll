#!/bin/sh
# Stamps the version on every page from the content of the compressed assets, so a bump can never be forgotten:
# site.min.css?v=HASH, site.min.js?v=HASH and the service-worker cache name ps-HASH all change together.
set -e
cd "$(dirname "$0")/.."
H=$(cat site.min.css site.min.js | sha1sum | cut -c1-8)
FILES=$(grep -rlE 'site\.min\.(css|js)\?v=' --include=*.html --include=*.py --include=sw.js . | grep -v node_modules)
for f in $FILES; do sed -i -E "s/(site\.min\.(css|js)\?v=)[0-9A-Za-z]+/\1$H/g" "$f"; done
sed -i -E "s/^const CACHE = 'ps-[0-9A-Za-z]+';/const CACHE = 'ps-$H';/" sw.js
echo "stamped v=$H on $(echo "$FILES" | wc -l) files"
