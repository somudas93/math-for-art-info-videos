"""Optimization primitives."""
from typing import Callable, List, Tuple

Point=Tuple[float,float]

def gradient(f, x:float, y:float, eps=1e-5)->Point:
    return ((f(x+eps,y)-f(x-eps,y))/(2*eps),
            (f(x,y+eps)-f(x,y-eps))/(2*eps))

def gradient_descent(f, start:Point, learning_rate=0.05, steps=100)->List[Point]:
    x,y=start; path=[(x,y)]
    for _ in range(steps):
        gx,gy=gradient(f,x,y)
        x-=learning_rate*gx; y-=learning_rate*gy
        path.append((x,y))
    return path

def quadratic(x,y):
    return x*x+2*y*y
