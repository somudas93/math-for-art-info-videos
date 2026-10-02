"""Simple chaotic maps."""
def tent_map(x=0.2, mu=2.0, steps=200):
    out=[x]
    for _ in range(steps):
        x=mu*x if x<0.5 else mu*(1-x)
        out.append(x)
    return out

def henon(x=0.1,y=0.0,a=1.4,b=0.3,steps=5000):
    out=[]
    for _ in range(steps):
        x,y=1-a*x*x+y,b*x
        out.append((x,y))
    return out
