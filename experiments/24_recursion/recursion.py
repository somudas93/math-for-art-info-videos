"""Recursive subdivision primitives."""
from typing import List, Tuple
Point=Tuple[float,float]

def midpoint(a:Point,b:Point)->Point:
    return ((a[0]+b[0])/2,(a[1]+b[1])/2)

def subdivide_segment(a:Point,b:Point,depth:int)->List[Point]:
    if depth<=0:return [a,b]
    m=midpoint(a,b)
    left=subdivide_segment(a,m,depth-1)
    right=subdivide_segment(m,b,depth-1)
    return left[:-1]+right
