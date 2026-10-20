#!/bin/sh
# Rebuilds the whole site in the right order, then stamps every page with a fresh version:  sh _tools/build.sh
# (pages.py first, every build_*.py except the register PDF, the search index, the compressed assets, then the stamp.)
set -e
cd "$(dirname "$0")/.."
python3 _tools/pages.py
for t in _tools/build_*.py; do case $t in *register_pdf*) continue;; esac; python3 "$t" >/dev/null; done
python3 -I _tools/strip_meta.py
python3 _tools/build_misc.py >/dev/null
sh _tools/build_min.sh >/dev/null
sh _tools/stamp.sh
# the first screen of every page is styled inline; the full stylesheet no longer blocks paint (needs the local server on 8765)
if curl -s -o /dev/null http://localhost:8765/; then POSTCSS_DIR=/tmp/claude-0/-home-claude/4ab16262-7f57-5f1b-b1c5-742690289c52/scratchpad/mini/node_modules NODE_PATH=$(npm root -g) node _tools/critical.js | tail -1; else echo "critical: no server on 8765, pages keep the blocking stylesheet"; fi
