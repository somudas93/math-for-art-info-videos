"""Grid and tiling primitives."""
from typing import List, Tuple

def checkerboard(width=10,height=10)->List[List[int]]:
    return [[(x+y)%2 for x in range(width)] for y in range(height)]

def triangular_grid(rows=8,cols=8)->List[Tuple[Tuple[float,float],Tuple[float,float]]]:
    edges=[]
    for y in range(rows):
        for x in range(cols):
            a=(x+y%2*0.5,y*0.866)
            if x+1<cols: edges.append((a,(x+1+y%2*0.5,y*0.866)))
            if y+1<rows: edges.append((a,(x+0.5+(y+1)%2*0.5,(y+1)*0.866)))
    return edges
