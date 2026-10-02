"""Combinatorial structures for visual generation."""
from typing import List

def combinations(n:int,k:int)->List[List[int]]:
    result=[]
    def backtrack(start,path):
        if len(path)==k: result.append(path[:]); return
        for i in range(start,n+1):
            path.append(i); backtrack(i+1,path); path.pop()
    backtrack(1,[])
    return result

def permutations(items):
    items=list(items); result=[]
    def rec(prefix,rest):
        if not rest: result.append(prefix[:]); return
        for i,x in enumerate(rest): rec(prefix+[x],rest[:i]+rest[i+1:])
    rec([],items); return result
