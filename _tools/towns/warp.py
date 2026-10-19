import numpy as np, json, sys
from PIL import Image, ImageDraw
def warp(name, keep, out_w=1600, quality=80):
    src=Image.open(f'towns/{name}_raw.png').convert('RGB')
    a=np.load(f'towns/{name}_aff.npy'); clat,clon=a[:3],a[3:]
    mask=Image.new('L',src.size,0); ImageDraw.Draw(mask).polygon(keep,fill=255)
    rgba=src.copy(); rgba.putalpha(mask)
    # bounds of the kept polygon in lat/lon
    P=np.array(keep,float); A=np.c_[P,np.ones(len(P))]
    lats=A@clat; lons=A@clon; N,S,E,W=lats.max(),lats.min(),lons.max(),lons.min()
    mlon=np.cos(np.radians((N+S)/2))
    aspect=((N-S))/((E-W)*mlon)          # height/width in metres
    out_h=int(round(out_w*aspect))
    # output pixel (u,v) -> lon = W + u*(E-W)/out_w ; lat = N - v*(N-S)/out_h
    # source px from lat/lon: solve [lat,lon] = M @ [x,y] + t
    M=np.array([[clat[0],clat[1]],[clon[0],clon[1]]]); t=np.array([clat[2],clon[2]]); Mi=np.linalg.inv(M)
    # (x,y) = Mi @ ([lat,lon]-t); lat = N - v*dlat, lon = W + u*dlon
    dlat=(N-S)/out_h; dlon=(E-W)/out_w
    # x = Mi00*(N - v dlat - t0) + Mi01*(W + u dlon - t1)
    ax=Mi[0,1]*dlon; bx=-Mi[0,0]*dlat; cx=Mi[0,0]*(N-t[0])+Mi[0,1]*(W-t[1])
    ay=Mi[1,1]*dlon; by=-Mi[1,0]*dlat; cy=Mi[1,0]*(N-t[0])+Mi[1,1]*(W-t[1])
    out=rgba.transform((out_w,out_h),Image.AFFINE,(ax,bx,cx,ay,by,cy),resample=Image.BICUBIC)
    out.save(f'towns/{name}.webp',quality=quality,method=6)
    b={'name':name,'N':round(N,6),'S':round(S,6),'E':round(E,6),'W':round(W,6),'w':out_w,'h':out_h}
    json.dump(b,open(f'towns/{name}_bounds.json','w')); print(b)
    out.convert('RGB').resize((out_w//3,out_h//3)).save(f'towns/{name}_warp_small.png')
if __name__=='__main__':
    keep=json.loads(sys.argv[2]); warp(sys.argv[1],[tuple(p) for p in keep])
