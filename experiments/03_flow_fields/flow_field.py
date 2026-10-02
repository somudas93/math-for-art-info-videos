"""Minimal deterministic flow-field experiment."""
from __future__ import annotations
import math
from typing import List, Tuple

Point = Tuple[float, float]

def direction(x: float, y: float, scale: float = 1.0) -> Point:
    angle = math.sin(x * scale) + math.cos(y * scale)
    return math.cos(angle), math.sin(angle)

def trace(start: Point, steps: int = 200, step_size: float = 0.02, scale: float = 1.5) -> List[Point]:
    x, y = start
    path = [(x, y)]
    for _ in range(steps):
        dx, dy = direction(x, y, scale)
        x += dx * step_size
        y += dy * step_size
        path.append((x, y))
    return path

if __name__ == "__main__":
    path = trace((-1.0, -1.0))
    print(f"Generated {len(path)} points")
    print("Start:", path[0])
    print("End:", path[-1])
