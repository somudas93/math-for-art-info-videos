"""Small matrix/vector primitives for visual math."""
from typing import List

Vector=List[float]
Matrix=List[List[float]]

def dot(a:Vector,b:Vector): return sum(x*y for x,y in zip(a,b))

def add(a:Vector,b:Vector): return [x+y for x,y in zip(a,b)]

def scale(v:Vector,s): return [x*s for x in v]

def matmul(A:Matrix,B:Matrix)->Matrix:
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def normalize(v:Vector):
    n=sum(x*x for x in v)**0.5
    return [x/n for x in v] if n else v
