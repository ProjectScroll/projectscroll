# Site checks

Run against the live site (or a local copy with BASE=http://localhost:8765):

    npm i -g playwright axe-core     # once
    cd tools/check
    NODE_PATH=$(npm root -g) node diag.js     # 140 checks: every button, link, file, light/dark, phone/computer
    NODE_PATH=$(npm root -g) node diag24.js   # 42 checks: scroll reveal, magnifier, seals, checker, scale, filters, offline
    NODE_PATH=$(npm root -g) node diag25.js   # 45 checks: glossary, listen, case pages, guide, map room, keepsake
    NODE_PATH=$(npm root -g) node diag26.js   # 48 checks: search, toolkit, handwriting, book, notebook
    NODE_PATH=$(npm root -g) node axe.js      # accessibility audit, every page, light and dark

Rule: nothing is published to the main branch until Michael has seen the draft.
