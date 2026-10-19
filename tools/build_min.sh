#!/bin/sh
# Builds the compressed copies the pages load (site.min.css, site.min.js) from the readable sources (site.css, site.js).
# Run after any change to site.css or site.js:  sh tools/build_min.sh
set -e
cd "$(dirname "$0")/.."
M=${MINI:-/tmp/claude-0/-home-claude/4ab16262-7f57-5f1b-b1c5-742690289c52/scratchpad/mini/node_modules/.bin}
"$M/lightningcss" --minify site.css -o site.min.css
"$M/terser" site.js --compress --mangle --comments false -o site.min.js
ls -l site.css site.min.css site.js site.min.js | awk '{print $5, $9}'
