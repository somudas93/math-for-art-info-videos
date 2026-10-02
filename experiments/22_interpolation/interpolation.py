"""Interpolation primitives."""
def lerp(a,b,t): return a+(b-a)*t

def smoothstep(a,b,t):
    t=max(0.0,min(1.0,t)); t=t*t*(3-2*t)
    return lerp(a,b,t)

def smootherstep(a,b,t):
    t=max(0.0,min(1.0,t)); t=t*t*t*(t*(t*6-15)+10)
    return lerp(a,b,t)

def inverse_lerp(a,b,value):
    return (value-a)/(b-a) if a!=b else 0.0
