"""Distance-field helpers."""
import math
from typing import Callable

def distance(a,b):
    return math.hypot(a[0]-b[0],a[1]-b[1])

def radial_field(x,y,center=(0.0,0.0)):
    return distance((x,y),center)

def inverse_field(x,y,center=(0.0,0.0),epsilon=1e-6):
    return 1.0/max(radial_field(x,y,center),epsilon)

def attraction(x,y,target=(0.0,0.0),strength=1.0,epsilon=1e-6):
    dx=target[0]-x; dy=target[1]-y
    d=math.hypot(dx,dy)
    return strength*dx/max(d,epsilon), strength*dy/max(d,epsilon)
