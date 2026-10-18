(function(){ "use strict";
/* ---------- faded-ink enhancer ---------- */
const file=document.getElementById('inkfile'), cv=document.getElementById('inkc'), ui=document.getElementById('inkui');
let src=null, rot=0;
const ids=['kB','kC','kL','kS','kG','kI'], el={}; ids.forEach(function(i){ el[i]=document.getElementById(i); });
function render(){
  if (!src) return; const MAX=2000; let w=src.width, h=src.height; const k=Math.min(1, MAX/Math.max(w,h)); w=Math.round(w*k); h=Math.round(h*k);
  const sw=(rot%180)?h:w, sh=(rot%180)?w:h; cv.width=sw; cv.height=sh; const x=cv.getContext('2d');
  x.save(); x.translate(sw/2,sh/2); x.rotate(rot*Math.PI/180); x.drawImage(src,-w/2,-h/2,w,h); x.restore();
  const B=+el.kB.value, C=+el.kC.value, L=+el.kL.value/100, S=+el.kS.value/100, G=el.kG.checked, I=el.kI.checked;
  const im=x.getImageData(0,0,sw,sh), d=im.data, f=(259*(C*2.55+255))/(255*(259-C*2.55));
  for (let i=0;i<d.length;i+=4){ let r=d[i],g=d[i+1],b=d[i+2];
    if (G){ const y=.299*r+.587*g+.114*b; r=g=b=y; }
    r=f*(r-128)+128+B; g=f*(g-128)+128+B; b=f*(b-128)+128+B;
    if (L>0){ const lift=function(v){ v=Math.max(0,Math.min(255,v))/255; return 255*Math.pow(v, 1+L*2.2); }; r=lift(r); g=lift(g); b=lift(b); }
    if (I){ r=255-r; g=255-g; b=255-b; }
    d[i]=r; d[i+1]=g; d[i+2]=b; }
  if (S>0){ const o=new Uint8ClampedArray(d), W=sw*4;
    for (let yy=1; yy<sh-1; yy++) for (let xx=1; xx<sw-1; xx++){ const p=yy*W+xx*4;
      for (let c=0;c<3;c++){ const v=o[p+c]*(1+4*S) - S*(o[p-4+c]+o[p+4+c]+o[p-W+c]+o[p+W+c]); d[p+c]=v; } } }
  x.putImageData(im,0,0);
}
let t=null; const later=function(){ clearTimeout(t); t=setTimeout(render,40); };
ids.forEach(function(i){ el[i].addEventListener('input', later); });
if (file) file.addEventListener('change', function(){ const f=file.files[0]; if (!f) return; document.getElementById('inkname').textContent=f.name;
  const img=new Image(); img.onload=function(){ src=img; rot=0; ui.hidden=false; render(); URL.revokeObjectURL(img.src); }; img.src=URL.createObjectURL(f); });
document.getElementById('kRot').addEventListener('click', function(){ rot=(rot+90)%360; render(); });
document.getElementById('kReset').addEventListener('click', function(){ el.kB.value=0; el.kC.value=0; el.kL.value=0; el.kS.value=0; el.kG.checked=false; el.kI.checked=false; rot=0; render(); });
document.getElementById('kSave').addEventListener('click', function(){ cv.toBlob(function(b){ const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download='enhanced-'+(document.getElementById('inkname').textContent.replace(/\.[^.]+$/,'')||'record')+'.png'; a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); },2000); }, 'image/png'); });

/* ---------- age at death → birth date ---------- */
const M=['January','February','March','April','May','June','July','August','September','October','November','December'];
function age(){
  const v=document.getElementById('aD').value, out=document.getElementById('aOut'); if (!v){ out.textContent=''; return; }
  const p=v.split('-').map(Number); let y=p[0], m=p[1], d=p[2];
  const Y=+document.getElementById('aY').value||0, Mo=+document.getElementById('aM').value||0, D=+document.getElementById('aDd').value||0;
  // the genealogists' method: subtract days, borrowing a month of the previous month's length; then months; then years
  d-=D; while (d<1){ m-=1; if (m<1){ m=12; y-=1; } d+=new Date(y,m,0).getDate(); }
  m-=Mo; while (m<1){ m+=12; y-=1; }
  y-=Y; const dim=new Date(y,m,0).getDate(); if (d>dim) d=dim;
  out.innerHTML='Born about <b>'+d+' '+M[m-1]+' '+y+'</b>.';
}
['aD','aY','aM','aDd'].forEach(function(i){ document.getElementById(i).addEventListener('input', age); }); age();

/* ---------- Soundex ---------- */
function soundex(s){
  s=(s||'').toUpperCase().replace(/[^A-Z]/g,''); if (!s) return '';
  const code={B:1,F:1,P:1,V:1,C:2,G:2,J:2,K:2,Q:2,S:2,X:2,Z:2,D:3,T:3,L:4,M:5,N:5,R:6};
  let out=s[0], last=code[s[0]]||0;
  for (let i=1;i<s.length && out.length<4;i++){ const ch=s[i], c=code[ch]||0;
    if (ch==='H'||ch==='W') continue;
    if (c && c!==last) out+=c; last=c; }
  return (out+'000').slice(0,4);
}
function variants(n){
  n=n.trim(); if (!n) return []; const L=n.toLowerCase(), v=new Set();
  const swaps=[['sky','ski'],['ski','sky'],['y','i'],['i','y'],['ck','k'],['k','ck'],['ph','f'],['f','ph'],['z','s'],['s','z'],['c','k'],['k','c'],['ow','ou'],['ei','ie'],['ie','ei'],['mann','man'],['man','mann'],['son','sen'],['sen','son'],['er','ar']];
  swaps.forEach(function(sw){ if (L.includes(sw[0])) v.add(L.replace(sw[0],sw[1])); });
  v.add(L.replace(/(.)\1/g,'$1'));
  if (/^[aeiou]/.test(L)) ['a','e','i','o','u'].forEach(function(x){ v.add(x+L.slice(1)); });
  v.delete(L);
  return [...v].filter(function(x){ return x.length>1; }).slice(0,10).map(function(x){ return x.charAt(0).toUpperCase()+x.slice(1); });
}
function sx(){ const n=document.getElementById('sx').value, out=document.getElementById('sxOut'), c=soundex(n);
  if (!c){ out.textContent=''; return; }
  const vs=variants(n).filter(function(x){ return soundex(x)===c; }), other=variants(n).filter(function(x){ return soundex(x)!==c; });
  out.innerHTML='Soundex code <b>'+c+'</b>.'+(vs.length?' Same code, also try: <i>'+vs.join(', ')+'</i>.':'')+(other.length?' Different code but worth a search: <i>'+other.slice(0,5).join(', ')+'</i>.':'');
}
document.getElementById('sx').addEventListener('input', sx); sx();

/* ---------- cousin calculator ---------- */
const ord=function(n){ return n+(['th','st','nd','rd'][(n%100-20)%10]||['th','st','nd','rd'][n%100]||'th'); };
const greats=function(n,base){ return n<=0?base: n===1?'great-'+base : (n)+'× great-'+base; };
function cousin(){
  const a=+document.getElementById('cA').value, b=+document.getElementById('cB').value, out=document.getElementById('cOut');
  let r;
  if (a===0 && b===0) r='That is the same person.';
  else if (a===0 || b===0){ const g=a||b, who=a===0?'Person A':'Person B', other=a===0?'Person B':'Person A';
    r=who+' is '+other+'’s '+(g===1?'parent':g===2?'grandparent':greats(g-2,'grandparent'))+'.'; }
  else if (a===1 && b===1) r='They are brothers or sisters.';
  else if (a===1 || b===1){ const g=Math.max(a,b), older=a===1?'Person A':'Person B', younger=a===1?'Person B':'Person A';
    r=older+' is '+younger+'’s '+(g===2?'aunt or uncle':g===3?'great-aunt or great-uncle':greats(g-2,'aunt or uncle').replace('great-aunt or uncle','great-aunt or great-uncle'))+'.'; }
  else { const deg=Math.min(a,b)-1, rem=Math.abs(a-b);
    r='They are <b>'+ord(deg)+' cousins'+(rem? ' '+(rem===1?'once':rem===2?'twice':rem+' times')+' removed':'')+'</b>.'; }
  out.innerHTML=r;
}
['cA','cB'].forEach(function(i){ document.getElementById(i).addEventListener('change', cousin); });
document.getElementById('cA').value=3; document.getElementById('cB').value=4; cousin();

/* ---------- cipher wheel ---------- */
(function(){
  const inp=document.getElementById('cyIn'), k=document.getElementById('cyK'), out=document.getElementById('cyOut'); if (!inp) return;
  const shift=function(str,n){ return str.replace(/[a-z]/gi,function(ch){ const b=ch<='Z'?65:97; return String.fromCharCode((ch.charCodeAt(0)-b+n)%26+b); }); };
  const draw=function(){ const n=+k.value; out.innerHTML=''; const b=document.createElement('b'); b.textContent=shift(inp.value, (26-n)%26); out.append('Turned '+n+': ', b); };
  inp.addEventListener('input',draw); k.addEventListener('input',draw); draw();
})();
})();
