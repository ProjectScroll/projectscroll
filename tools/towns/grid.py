import sys
from PIL import Image, ImageDraw
def grid(src,box,out,step=50):
    im=Image.open(src).convert('RGB').crop(box); d=ImageDraw.Draw(im)
    x0,y0=box[0],box[1]
    for x in range((x0//step+1)*step, box[2], step):
        d.line([(x-x0,0),(x-x0,im.height)],fill=(0,160,255),width=1); d.text((x-x0+2,2),str(x),fill=(0,0,255))
    for y in range((y0//step+1)*step, box[3], step):
        d.line([(0,y-y0),(im.width,y-y0)],fill=(0,160,255),width=1); d.text((2,y-y0+2),str(y),fill=(0,0,255))
    im.save(out)
if __name__=='__main__':
    a=sys.argv; grid(a[1],tuple(map(int,a[2:6])),a[6],int(a[7]) if len(a)>7 else 50)
