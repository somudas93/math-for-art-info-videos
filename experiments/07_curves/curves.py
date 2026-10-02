"""Parametric curve primitives."""
import math
from typing import Callable, List, Tuple
Point = Tuple[float, float]

def parametric(fn: Callable[[float], Point], start=0.0, end=1.0, samples=256) -> List[Point]:
    return [fn(start + (end-start)*i/(samples-1)) for i in range(samples)]

def spiral(a=0.05, b=0.12, turns=4.0, samples=256) -> List[Point]:
    return parametric(lambda t: ((a+b*t)*math.cos(2*math.pi*turns*t),
                                (a+b*t)*math.sin(2*math.pi*turns*t)), 0, 1, samples)

def lissajous(a=3, b=2, delta=math.pi/2, samples=512) -> List[Point]:
    return parametric(lambda t: (math.sin(a*t+delta), math.sin(b*t)), 0, 2*math.pi, samples)

def bezier(p0: Point, p1: Point, p2: Point, p3: Point, samples=256) -> List[Point]:
    def f(t):
        u=1-t
        return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
    return parametric(f, 0, 1, samples)
