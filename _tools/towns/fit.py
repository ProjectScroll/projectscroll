import numpy as np, json, sys
def fit(px, M, name, X0, Y0, scale):
    """px: {ns:x} {ew:y} in stitched px; M: {'nsxew':[lat,lon]}"""
    NS,EW=px
    P=[];L=[];K=[]
    for k,(la,lo) in M.items():
        a,b=k.split('x')
        if a in NS and b in EW: P.append((NS[a],EW[b]));L.append((la,lo));K.append(k)
    P=np.array(P,float);L=np.array(L)
    A=np.c_[P,np.ones(len(P))]
    clat,_,_,_=np.linalg.lstsq(A,L[:,0],rcond=None); clon,_,_,_=np.linalg.lstsq(A,L[:,1],rcond=None)
    pred=np.c_[A@clat,A@clon]; mlat=111133; mlon=111320*np.cos(np.radians(L[:,0].mean()))
    r=np.hypot((pred[:,0]-L[:,0])*mlat,(pred[:,1]-L[:,1])*mlon)
    print(name,'points',len(P),'rms %.1f m max %.1f m'%(np.sqrt((r**2).mean()),r.max()), 'worst',K[int(r.argmax())])
    for k,rr in sorted(zip(K,r),key=lambda t:-t[1])[:5]: print('  ',k,round(rr,1))
    return clat,clon
