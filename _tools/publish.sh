#!/bin/sh
# Build, run every check, and publish only if all pass:  sh _tools/publish.sh draft-N "message"

B=$1; M=$2; cd "$(dirname "$0")/.."
sh _tools/build.sh >/tmp/ps-build.log 2>&1 || { tail -5 /tmp/ps-build.log; echo "BUILD FAILED"; exit 1; }
if grep -q "share tags fall outside" /tmp/ps-build.log; then echo "HEADS FAILED"; exit 1; fi
python3 _tools/check/links.py >/dev/null || { python3 _tools/check/links.py | head; echo "LINKS FAILED"; exit 1; }
F=0; for c in diag diag24 diag25 diag26; do r=$(BASE=http://localhost:8765 NODE_PATH=$(npm root -g) timeout 300 node _tools/check/$c.js 2>&1 | grep -E "TOTAL|FAIL"); if ! echo "$r" | grep -q TOTAL; then echo "$c produced no result"; F=1; fi; echo "$r" | grep TOTAL; if echo "$r" | grep -q "^FAIL"; then echo "$r" | grep FAIL | head -5; F=1; fi; done
A=$(BASE=http://localhost:8765 NODE_PATH=$(npm root -g) timeout 400 node _tools/check/axe.js 2>&1 | grep -v "violations: 0" | grep -v "^$"); if [ -n "$A" ]; then echo "$A" | head -8; F=1; fi
if [ $F = 1 ]; then echo "CHECKS FAILED, not published"; exit 1; fi
rm -f D2[0-9]_*.png; git checkout -- _tools/check/*.png 2>/dev/null || true
git checkout -q -B "$B" || exit 1; git add -A; git commit -qm "$M

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HMuVy4MP32mW96WdEuAjrt"
git push -qu origin "$B" 2>/dev/null; git config --add remote.origin.fetch "+refs/heads/$B:refs/remotes/origin/$B"
git checkout -q main || { echo "could not switch to main (uncommitted changes?); not published"; exit 1; }; git merge -q --ff-only "$B" || { echo "main cannot fast-forward to $B; not published"; git checkout -q "$B"; exit 1; }; git push -q origin main:main 2>/dev/null; sleep 8
gh run list -L1 --json databaseId -q '.[0].databaseId' | xargs -I{} gh run watch {} --exit-status >/dev/null && echo DEPLOYED
git checkout -q "$B"; git push -q origin "$B" 2>/dev/null; true
