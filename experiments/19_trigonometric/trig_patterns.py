"""Trigonometric pattern primitives."""
import math
from typing import List, Tuple
Point=Tuple[float,float]

def rose(k=5, radius=1.0, samples=512)->List[Point]:
    return [(radius*math.cos(k*t)*math.cos(t), radius*math.cos(k*t)*math.sin(t))
            for t in [2*math.pi*i/(samples-1) for i in range(samples)]]

def hypotrochoid(R=5.0,r=3.0,d=5.0,samples=1000)->List[Point]:
    return [((R-r)*math.cos(t)+d*math.cos((R-r)*t/r),
             (R-r)*math.sin(t)-d*math.sin((R-r)*t/r))
            for t in [2*math.pi*i/(samples-1) for i in range(samples)]]
