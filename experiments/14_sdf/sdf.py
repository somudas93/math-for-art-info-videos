"""Signed-distance primitives and composition."""
import math
from typing import Callable

SDF=Callable[[float,float],float]

def circle(radius=1.0) -> SDF:
    return lambda x,y: math.hypot(x,y)-radius

def box(width=1.0,height=1.0) -> SDF:
    def f(x,y):
        qx=abs(x)-width/2; qy=abs(y)-height/2
        ox=max(qx,0); oy=max(qy,0)
        return math.hypot(ox,oy)+min(max(qx,qy),0)
    return f

def union(a:SDF,b:SDF)->SDF:
    return lambda x,y:min(a(x,y),b(x,y))

def intersection(a:SDF,b:SDF)->SDF:
    return lambda x,y:max(a(x,y),b(x,y))

def difference(a:SDF,b:SDF)->SDF:
    return lambda x,y:max(a(x,y),-b(x,y))
