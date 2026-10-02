"""Number-theoretic sequences useful for procedural art."""
from math import isqrt
from typing import List, Tuple

def primes(n=100)->List[int]:
    out=[]
    for x in range(2,n+1):
        if all(x%p for p in out if p*p<=x): out.append(x)
    return out

def fibonacci(n=20)->List[int]:
    a,b=0,1; out=[]
    for _ in range(n): out.append(a); a,b=b,a+b
    return out

def pascal(rows=10)->List[List[int]]:
    out=[]
    for n in range(rows):
        row=[1]
        for k in range(1,n+1):
            row.append(row[-1]*(n-k+1)//k)
        out.append(row)
    return out

def ulam_spiral(n=25)->List[Tuple[int,int,int]]:
    size=2*n+1; x=y=0; dx,dy=1,0; step=1; value=1; out=[(x,y,value)]
    while value<size*size:
        for _ in range(2):
            for _ in range(step):
                x+=dx; y+=dy; value+=1
                if value>size*size: return out
                out.append((x,y,value))
            dx,dy=-dy,dx
        step+=1
    return out
