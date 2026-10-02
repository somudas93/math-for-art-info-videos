"""Simplex and barycentric-coordinate primitives."""
from typing import Tuple

Point=Tuple[float,float]

def barycentric(p:Point,a:Point,b:Point,c:Point):
    det=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    u=((b[1]-c[1])*(p[0]-c[0])+(c[0]-b[0])*(p[1]-c[1]))/det
    v=((c[1]-a[1])*(p[0]-c[0])+(a[0]-c[0])*(p[1]-c[1]))/det
    return u,v,1-u-v

def interpolate(a,b,c,weights):
    u,v,w=weights
    return (u*a[0]+v*b[0]+w*c[0],u*a[1]+v*b[1]+w*c[1])
