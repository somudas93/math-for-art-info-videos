"""Minimal L-system engine.

Symbol rewriting is kept separate from turtle interpretation so the same
grammar can later produce trees, networks, or financial process diagrams.
"""
from __future__ import annotations
from typing import Dict

def expand(axiom: str, rules: Dict[str, str], iterations: int) -> str:
    current = axiom
    for _ in range(iterations):
        current = "".join(rules.get(symbol, symbol) for symbol in current)
    return current

def plant_example(iterations: int = 4) -> str:
    return expand("X", {
        "X": "F+[[X]-X]-F[-FX]+X",
        "F": "FF",
    }, iterations)

if __name__ == "__main__":
    result = plant_example()
    print(f"Generated {len(result)} symbols")
    print(result[:120])
