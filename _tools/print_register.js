// Prints tools/register.html to sample/project-scroll-sample-family-register.pdf
const { chromium } = require('playwright'); const path=require('path');
const R=path.resolve(__dirname,'..');
(async()=>{const b=await chromium.launch(); const p=await b.newPage();
await p.goto('file://'+path.join(R,'tools/register.html')); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
await p.pdf({path:path.join(R,'sample/project-scroll-sample-family-register.pdf'),format:'Letter',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font-size:7.5px;color:#8a8f96;font-family:Georgia,serif">Project Scroll · SPECIMEN: an invented family, made to show how a family register reads · projectscroll.com · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>'});
await b.close(); console.log('register pdf printed');})();
