"""2D geometric transformations."""
import math
from typing import Iterable, List, Tuple
Point = Tuple[float, float]

def translate(points: Iterable[Point], dx, dy) -> List[Point]:
    return [(x+dx,y+dy) for x,y in points]

def scale(points: Iterable[Point], sx, sy=None) -> List[Point]:
    sy = sx if sy is None else sy
    return [(x*sx,y*sy) for x,y in points]

def rotate(points: Iterable[Point], angle, center=(0.0,0.0)) -> List[Point]:
    c,s=math.cos(angle),math.sin(angle); cx,cy=center
    return [(cx+(x-cx)*c-(y-cy)*s, cy+(x-cx)*s+(y-cy)*c) for x,y in points]

def reflect_x(points: Iterable[Point]) -> List[Point]:
    return [(x,-y) for x,y in points]

def reflect_y(points: Iterable[Point]) -> List[Point]:
    return [(-x,y) for x,y in points]

def repeat_rotated(points: Iterable[Point], count=8) -> List[List[Point]]:
    base=list(points)
    return [rotate(base, 2*math.pi*i/count) for i in range(count)]
