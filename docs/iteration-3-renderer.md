# Iteration 3 — Renderer Layer

The renderer layer is separated from mathematical models, Scene IR, Animation IR, and Style IR.

```text
financial model → Scene IR → Animation IR + Style IR → renderer → video
```

## Renderer library

The reusable renderer library contains:

- `renderers/base.py` — common renderer interface
- `renderers/registry.py` — named, lazy-loaded renderer registry
- `renderers/manim/primitives.py` — reusable Manim object mappings
- `renderers/manim/animation.py` — reusable Manim animation mappings
- `renderers/manim/style.py` — Manim implementation of Style IR
- `renderers/manim/renderer.py` — complete Scene renderer
- `renderers/manim/compound_interest.py` — thin executable entry point
- `engine/serialization.py` — JSON bridge for non-Python renderers
- `renderers/motion_canvas/` — Motion Canvas TypeScript adapter

## Motion Canvas adapter

Motion Canvas consumes the same serialized Scene IR rather than a second financial model.

The adapter currently covers:

- object kinds: timeline, curve, particles, label, line, circle, rectangle, group
- animation actions: create, draw, grow, fade in/out, highlight, move, transform, wait
- portable style properties such as opacity, scale, fill, stroke, and stroke width

This makes the renderer boundary explicit:

```text
Python financial model
        ↓
Python Scene IR
        ↓
      JSON
        ↓
Motion Canvas TypeScript
        ↓
       video
```

## Result

A financial scene generator stays unaware of the concrete animation framework. Manim and Motion Canvas can consume the same mathematical scene description without changing financial calculations.

## Next

Build a small shared style library and add a first end-to-end compound-interest render in Motion Canvas.
