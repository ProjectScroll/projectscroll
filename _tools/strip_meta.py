#!/usr/bin/env python3
"""Strips metadata from every image the site serves: EXIF, IPTC/Photoshop, XMP, comments and
colour profiles from JPEGs (segment removal, no re-encoding); text, EXIF and ICC chunks from
PNGs; EXIF, XMP and ICC chunks from WebPs. Run by _tools/build.sh. Pixels are never touched."""
import os, struct, sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP=('node_modules', os.sep+'.git', '_tools')
def jpeg(b):
    out=bytearray(b[:2]); i=2; changed=False
    while i<len(b) and b[i]==0xFF:
        m=b[i+1]
        if m in (0xDA, 0xD9): break
        L=struct.unpack('>H',b[i+2:i+4])[0]; seg=b[i:i+2+L]
        drop = m in (0xE1,0xE2,0xED,0xFE) or (0xE3<=m<=0xEF)
        if m==0xE0 and seg[4:8]!=b'JFIF': drop=True
        if drop: changed=True
        else: out+=seg
        i+=2+L
    out+=b[i:]
    return bytes(out), changed
def png(b):
    out=bytearray(b[:8]); i=8; changed=False
    while i<len(b):
        L=struct.unpack('>I',b[i:i+4])[0]; t=b[i+4:i+8]; chunk=b[i:i+12+L]
        if t in (b'tEXt',b'iTXt',b'zTXt',b'eXIf',b'iCCP',b'tIME'): changed=True
        else: out+=chunk
        i+=12+L
        if t==b'IEND': break
    return bytes(out), changed
def webp(b):
    out=bytearray(); i=12; changed=False
    while i+8<=len(b):
        t=b[i:i+4]; L=struct.unpack('<I',b[i+4:i+8])[0]; n=8+L+(L&1); chunk=b[i:i+n]
        if t in (b'EXIF',b'XMP ',b'ICCP'): changed=True
        else: out+=chunk
        i+=n
    if not changed: return b, False
    body=bytes(out)
    if body[:4]==b'VP8X':  # clear the EXIF/XMP/ICC flags
        fl=bytearray(body[:12]); fl[8]&= ~(0x20|0x08|0x04); body=bytes(fl)+body[12:]
    return b'RIFF'+struct.pack('<I',4+len(body))+b'WEBP'+body, True
n=0
for root,_,fs in os.walk(R):
    if any(s in root for s in SKIP): continue
    for f in fs:
        p=os.path.join(root,f); ext=f.lower().rsplit('.',1)[-1]
        if ext not in ('jpg','jpeg','png','webp'): continue
        b=open(p,'rb').read()
        if ext in('jpg','jpeg') and b[:2]==b'\xff\xd8': nb,ch=jpeg(b)
        elif ext=='png' and b[:8]==b'\x89PNG\r\n\x1a\n': nb,ch=png(b)
        elif ext=='webp' and b[:4]==b'RIFF': nb,ch=webp(b)
        else: continue
        if ch: open(p,'wb').write(nb); n+=1
print(f'metadata stripped from {n} image(s)')
# PDFs: keep only the title (what a reader's window shows); drop the making program, dates and any XMP
try:
    from pypdf import PdfReader, PdfWriter
    m=0
    for root,_,fs in os.walk(R):
        if any(s in root for s in SKIP): continue
        for f in fs:
            if not f.lower().endswith('.pdf'): continue
            p=os.path.join(root,f); r=PdfReader(p); md=dict(r.metadata or {})
            if set(md)-{'/Title'} or r.xmp_metadata is not None:
                w=PdfWriter(clone_from=r); w._info=None if False else w._info
                w.metadata={'/Title': md.get('/Title','Project Scroll')}
                try:
                    if '/Metadata' in w._root_object: del w._root_object['/Metadata']
                except Exception: pass
                with open(p,'wb') as o: w.write(o)
                m+=1
    print(f'pdf metadata cleared from {m} file(s)')
except ImportError:
    print('pypdf not installed: PDFs not checked')
