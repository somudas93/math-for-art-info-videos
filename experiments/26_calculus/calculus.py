"""Calculus helpers for visual explanations."""
from typing import List, Tuple

def derivative(f,x,eps=1e-5): return (f(x+eps)-f(x-eps))/(2*eps)

def integral(f,a,b,steps=1000):
    h=(b-a)/steps
    return h*(0.5*f(a)+sum(f(a+i*h) for i in range(1,steps))+0.5*f(b))

def tangent(f,x,eps=1e-5):
    m=derivative(f,x,eps)
    return lambda t: f(x)+m*(t-x)

def cumulative_values(values,dt=1.0)->List[float]:
    total=0.0; out=[0.0]
    for v in values: total+=v*dt; out.append(total)
    return out
