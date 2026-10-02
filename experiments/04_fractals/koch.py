"""Koch curve generator using recursive geometry."""
from __future__ import annotations
import math
from typing import List, Tuple

Point = Tuple[float, float]

def koch(a: Point, b: Point, depth: int) -> List[Point]:
    if depth == 0:
        return [a, b]

    ax, ay = a
    bx, by = b
    dx = (bx - ax) / 3.0
    dy = (by - ay) / 3.0

    p1 = (ax + dx, ay + dy)
    p3 = (ax + 2 * dx, ay + 2 * dy)

    angle = math.atan2(dy, dx) - math.pi / 3.0
    length = math.hypot(dx, dy)
    p2 = (
        p1[0] + length * math.cos(angle),
        p1[1] + length * math.sin(angle),
    )

    parts = [(a, p1), (p1, p2), (p2, p3), (p3, b)]
    points = []
    for start, end in parts:
        segment = koch(start, end, depth - 1)
        points.extend(segment[:-1])
    points.append(parts[-1][1])
    return points

if __name__ == "__main__":
    points = koch((0.0, 0.0), (1.0, 0.0), 4)
    print(f"Generated {len(points)} points")
