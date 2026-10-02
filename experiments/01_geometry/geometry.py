"""Small procedural geometry toolkit."""
from __future__ import annotations
import math
from typing import List, Tuple

Point = Tuple[float, float]

def circle(radius: float = 1.0, samples: int = 128, phase: float = 0.0) -> List[Point]:
    return [
        (radius * math.cos(phase + 2 * math.pi * i / samples),
         radius * math.sin(phase + 2 * math.pi * i / samples))
        for i in range(samples)
    ]

def radial_pattern(radius: float = 1.0, arms: int = 8, samples_per_arm: int = 32) -> List[List[Point]]:
    result = []
    for arm in range(arms):
        phase = 2 * math.pi * arm / arms
        points = []
        for i in range(samples_per_arm):
            t = i / max(1, samples_per_arm - 1)
            r = radius * t
            points.append((r * math.cos(phase), r * math.sin(phase)))
        result.append(points)
    return result

def polar_curve(radius_fn, turns: float = 2.0, samples: int = 256) -> List[Point]:
    points = []
    for i in range(samples):
        theta = 2 * math.pi * turns * i / (samples - 1)
        r = radius_fn(theta)
        points.append((r * math.cos(theta), r * math.sin(theta)))
    return points

if __name__ == "__main__":
    spiral = polar_curve(lambda theta: 0.05 * theta, turns=4)
    print(f"Generated {len(spiral)} points")
    print("First:", spiral[0])
    print("Last:", spiral[-1])
