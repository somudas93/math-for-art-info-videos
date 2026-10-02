"""Simple deterministic particle system."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, List, Tuple

Point = Tuple[float, float]
Field = Callable[[float, float], Point]

@dataclass
class Particle:
    x: float
    y: float
    age: int = 0

def step(particle: Particle, field: Field, dt: float = 0.02) -> None:
    dx, dy = field(particle.x, particle.y)
    particle.x += dx * dt
    particle.y += dy * dt
    particle.age += 1

def simulate(particles: List[Particle], field: Field, frames: int = 100, dt: float = 0.02) -> List[List[Point]]:
    frames_out = []
    for _ in range(frames):
        frames_out.append([(p.x, p.y) for p in particles])
        for particle in particles:
            step(particle, field, dt)
    return frames_out
