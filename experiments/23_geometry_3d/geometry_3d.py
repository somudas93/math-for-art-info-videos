"""Lightweight 3D mathematical primitives."""
import math
from typing import List, Tuple
Point3=Tuple[float,float,float]

def sphere(radius=1.0, u_samples=32, v_samples=16)->List[Point3]:
    points=[]
    for j in range(v_samples+1):
        v=math.pi*j/v_samples
        for i in range(u_samples):
            u=2*math.pi*i/u_samples
            points.append((radius*math.sin(v)*math.cos(u),
                           radius*math.sin(v)*math.sin(u),
                           radius*math.cos(v)))
    return points

def helix(radius=1.0,height=2.0,turns=3.0,samples=256)->List[Point3]:
    return [(radius*math.cos(2*math.pi*turns*t),
             radius*math.sin(2*math.pi*turns*t),height*t)
            for t in [i/(samples-1) for i in range(samples)]]
