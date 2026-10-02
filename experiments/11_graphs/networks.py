"""Small graph primitives and force-directed layout."""
import math, random
from typing import Dict, List, Tuple
Point=Tuple[float,float]
Graph=Dict[int,List[int]]

def ring_graph(n=12) -> Graph:
    return {i:[(i-1)%n,(i+1)%n] for i in range(n)}

def force_layout(graph: Graph, iterations=100, seed=0) -> List[Point]:
    rng=random.Random(seed); n=len(graph)
    pos=[(rng.uniform(-1,1),rng.uniform(-1,1)) for _ in range(n)]
    for _ in range(iterations):
        force=[ [0.0,0.0] for _ in range(n) ]
        for i in range(n):
            for j in range(i+1,n):
                dx=pos[i][0]-pos[j][0]; dy=pos[i][1]-pos[j][1]
                d2=max(dx*dx+dy*dy,1e-4); f=0.01/d2
                force[i][0]+=dx*f; force[i][1]+=dy*f
                force[j][0]-=dx*f; force[j][1]-=dy*f
        for i,neighbors in graph.items():
            for j in neighbors:
                dx=pos[j][0]-pos[i][0]; dy=pos[j][1]-pos[i][1]
                force[i][0]+=dx*0.01; force[i][1]+=dy*0.01
        pos=[(x+fx,y+fy) for (x,y),(fx,fy) in zip(pos,force)]
    return pos
