"""Discrete dynamical systems and attractors."""
import math
from typing import List, Tuple
Point=Tuple[float,float]

def logistic_map(x=0.2, r=3.8, steps=200) -> List[float]:
    out=[x]
    for _ in range(steps):
        x=r*x*(1-x); out.append(x)
    return out

def lorenz(x=0.1,y=0.0,z=0.0,sigma=10.0,rho=28.0,beta=8/3,dt=0.01,steps=5000) -> List[Point]:
    out=[]
    for _ in range(steps):
        dx=sigma*(y-x); dy=x*(rho-z)-y
        dz=x*y-beta*z
        x+=dx*dt; y+=dy*dt; z+=dz*dt
        out.append((x,z))
    return out

def harmonic_oscillator(x=1.0,v=0.0,k=1.0,dt=0.02,steps=500):
    out=[(x,v)]
    for _ in range(steps):
        v += -k*x*dt; x += v*dt; out.append((x,v))
    return out
