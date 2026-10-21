"""The cover plates also as AVIF, about 40% smaller than WebP; browsers that cannot show AVIF keep the WebP.
Made only when missing or older than the WebP. No metadata is written (AVIF from pixels only)."""
import glob, os
from PIL import Image
n = 0
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), '..', 'img', 'strip', '*.webp'))):
    a = f[:-5] + '.avif'
    if os.path.exists(a) and os.path.getmtime(a) >= os.path.getmtime(f): continue
    im = Image.open(f); im.load()
    Image.frombytes('RGB', im.size, im.convert('RGB').tobytes()).save(a, 'AVIF', quality=52, speed=6); n += 1
print('avif plates made', n)
