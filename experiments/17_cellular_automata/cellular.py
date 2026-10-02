"""Elementary cellular automata."""
from typing import List

def next_row(row:List[int], rule=30)->List[int]:
    n=len(row); out=[0]*n
    for i in range(n):
        left=row[(i-1)%n]; center=row[i]; right=row[(i+1)%n]
        code=left*4+center*2+right
        out[i]=(rule>>code)&1
    return out

def evolve(seed:List[int], rule=30, steps=100)->List[List[int]]:
    rows=[seed[:]]
    for _ in range(steps-1): rows.append(next_row(rows[-1],rule))
    return rows
