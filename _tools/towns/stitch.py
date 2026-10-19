import sys,glob,json
from PIL import Image
D='/root/.claude/projects/-home-claude/4ab16262-7f57-5f1b-b1c5-742690289c52/tool-results/'
def stitch(name,tiles,x0,y0,w,h,scale=2):
    out=Image.new('RGB',(w//scale,h//scale),(230,215,185))
    for x,y,k in tiles:
        im=Image.open(glob.glob(D+'*'+k+'.jpg')[0]).convert('RGB'); assert im.size==(800,450)
        out.paste(im,((x-x0)//scale,(y-y0)//scale))
    out.save(f'towns/{name}_raw.png'); print(name,out.size)
if __name__=='__main__':
    stitch('niles',[(1820,3280,'qsr9ws'),(3550,3280,'78g5sg'),(1820,4180,'ro488v'),(3550,4180,'8vcrfi'),(1820,5080,'q7crfj'),(3550,5080,'koig81'),(1820,5600,'djehqe'),(3550,5600,'2oo9vv')],1820,3280,3330,3220)
