# Iteration 3 — Mathematical Composition

Iteration 3 changes the focus from individual primitives to composable visual systems.

## First composition

The first complete system is compound interest:

    financial model → values → Scene IR → curve + particles → renderer

The `CompoundInterest` model remains the numerical source of truth.

## Scene IR

`engine/scene_ir.py` defines a renderer-independent scene description. It describes what should exist rather than calling a specific renderer.

## Composition rules

1. Start from a mathematical model.
2. Derive numerical values without changing them.
3. Map values to one or more visual primitives.
4. Keep visual mappings deterministic where possible.
5. Leave rendering and style to a later layer.

## Initial vocabulary

- Curve + particles
- Curve + noise
- Flow field + particles
- Graph + forces
- Distribution + particles
- Fractal + transformation
- Fourier + waves
- Optimization + contours
- Financial model + any primitive

Next: build renderer adapters around the Scene IR, beginning with Manim.
