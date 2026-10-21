"""Reports any served file that still carries hidden metadata: EXIF, XMP, IPTC, comments or
colour profiles in JPEG/PNG/WebP/GIF/ICO, metadata blocks in SVG, and author/creator fields in PDF.
python3 _tools/check/meta.py   (prints OK or one line per file; exit 1 if anything is found)"""
import os, re, struct, sys
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad=[]
def jpg(b):
    i=2; f=[]
    while i+4<len(b) and b[i]==0xFF:
        m=b[i+1]
        if m in (0xDA,0xD9): break
        L=struct.unpack('>H',b[i+2:i+4])[0]
        if m in (0xE1,0xED,0xFE) or (0xE2<=m<=0xEF): f.append(hex(m))
        i+=2+L
    return f
def png(b):
    i=8; f=[]
    while i+8<=len(b):
        L=struct.unpack('>I',b[i:i+4])[0]; t=b[i+4:i+8]
        if t in (b'tEXt',b'iTXt',b'zTXt',b'eXIf',b'iCCP',b'tIME'): f.append(t.decode())
        i+=12+L
        if t==b'IEND': break
    return f
def webp(b):
    i=12; f=[]
    while i+8<=len(b):
        t=b[i:i+4]; L=struct.unpack('<I',b[i+4:i+8])[0]
        if t in (b'EXIF',b'XMP ',b'ICCP'): f.append(t.decode().strip())
        i+=8+L+(L&1)
    return f
for root,dirs,fs in os.walk(R):
    dirs[:]=[d for d in dirs if d not in ('.git','node_modules','_tools')]
    for n in fs:
        p=os.path.join(root,n); e=n.lower().rsplit('.',1)[-1]; rel=os.path.relpath(p,R)
        if e not in ('jpg','jpeg','png','webp','gif','ico','svg','pdf','avif'): continue
        b=open(p,'rb').read(); f=[]
        if b[:2]==b'\xff\xd8': f=jpg(b)
        elif b[:8]==b'\x89PNG\r\n\x1a\n': f=png(b)
        elif b[:4]==b'RIFF' and b[8:12]==b'WEBP': f=webp(b)
        elif b[:3]==b'GIF': f=['comment/app ext'] if (b'\x21\xfe' in b or b'XMP DataXMP' in b) else []
        elif e=='ico':
            f=[x for x in (b'Exif',b'<x:xmpmeta',b'iTXt',b'tEXt') if x in b]
        elif e=='svg':
            s=b.decode('utf-8','ignore'); f=[k for k in ('<metadata','sodipodi:','inkscape:','<!--','rdf:RDF','xmlns:dc') if k in s]
        elif e=='pdf':
            f=[k.decode() for k in (b'/Author',b'/Creator',b'/Producer',b'/Subject',b'/Keywords',b'/CreationDate',b'<x:xmpmeta') if k in b]
        elif e=='avif': f=['avif (check)'] if b'Exif' in b or b'mime' in b else []
        if f: bad.append(f'{rel}: {", ".join(map(str,f))}')
print('\n'.join(bad) if bad else 'OK: no hidden metadata in any served image or PDF')
sys.exit(1 if bad else 0)
