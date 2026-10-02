"""Probability primitives for visual simulation."""
import math, random
from typing import List

def gaussian(mu=0.0, sigma=1.0, samples=1000, seed=0) -> List[float]:
    rng=random.Random(seed)
    return [rng.gauss(mu,sigma) for _ in range(samples)]

def random_walk(steps=500, step_sigma=1.0, seed=0) -> List[float]:
    rng=random.Random(seed); x=0.0; path=[x]
    for _ in range(steps):
        x += rng.gauss(0.0, step_sigma)
        path.append(x)
    return path

def poisson(lam=4.0, samples=1000, seed=0) -> List[int]:
    rng=random.Random(seed); out=[]
    for _ in range(samples):
        l=math.exp(-lam); k=0; p=1.0
        while p>l:
            k+=1; p*=rng.random()
        out.append(k-1)
    return out

def monte_carlo_pi(samples=10000, seed=0) -> float:
    rng=random.Random(seed); inside=0
    for _ in range(samples):
        x,y=rng.uniform(-1,1),rng.uniform(-1,1)
        inside += x*x+y*y <= 1
    return 4*inside/samples
