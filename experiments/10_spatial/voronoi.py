"""Simple dependency-free spatial primitives."""
import math
from typing import List, Tuple
Point=Tuple[float,float]

def nearest_site(point: Point, sites: List[Point]) -> int:
    return min(range(len(sites)), key=lambda i: (point[0]-sites[i][0])**2+(point[1]-sites[i][1])**2)

def grid_labels(sites: List[Point], width=40, height=20, xmin=-1, xmax=1, ymin=-1, ymax=1):
    rows=[]
    for j in range(height):
        y=ymax-(ymax-ymin)*j/(height-1)
        rows.append([nearest_site((xmin+(xmax-xmin)*i/(width-1),y),sites) for i in range(width)])
    return rows

def delaunay_note():
    return "Delaunay triangulation is the geometric dual of a Voronoi diagram; use a dedicated implementation when exact triangulation is required."
