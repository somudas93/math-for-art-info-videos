"""Small deterministic value-noise field.

The implementation is intentionally dependency-free so the mathematical
idea stays visible and reproducible.
"""
from __future__ import annotations
import math
from typing import List

def smoothstep(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)

def hash2(ix: int, iy: int, seed: int = 0) -> float:
    n = ix * 374761393 + iy * 668265263 + seed * 1442695041
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)
    return (n & 0xFFFFFFFF) / 4294967295.0

def value_noise(x: float, y: float, scale: float = 1.0, seed: int = 0) -> float:
    x *= scale
    y *= scale
    x0, y0 = math.floor(x), math.floor(y)
    tx, ty = x - x0, y - y0
    sx, sy = smoothstep(tx), smoothstep(ty)

    a = hash2(x0, y0, seed)
    b = hash2(x0 + 1, y0, seed)
    c = hash2(x0, y0 + 1, seed)
    d = hash2(x0 + 1, y0 + 1, seed)

    ab = a + (b - a) * sx
    cd = c + (d - c) * sx
    return ab + (cd - ab) * sy

def fractal_noise(x: float, y: float, octaves: int = 4, seed: int = 0) -> float:
    total = 0.0
    amplitude = 1.0
    frequency = 1.0
    normalization = 0.0

    for octave in range(octaves):
        total += amplitude * value_noise(x, y, frequency, seed + octave)
        normalization += amplitude
        amplitude *= 0.5
        frequency *= 2.0

    return total / normalization
