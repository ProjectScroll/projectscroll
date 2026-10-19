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
