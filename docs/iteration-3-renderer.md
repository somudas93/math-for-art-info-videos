# Iteration 3 — Renderer Layer

The renderer layer is separated from mathematical models, Scene IR, and Animation IR.

```text
financial model → Scene IR → Animation IR → renderer → video
```

## Renderer library

The reusable renderer library now contains:

- `renderers/base.py` — common renderer interface
- `renderers/registry.py` — named, lazy-loaded renderer registry
- `renderers/manim/primitives.py` — reusable Manim object mappings
- `renderers/manim/animation.py` — reusable Manim animation mappings
- `renderers/manim/renderer.py` — complete Scene renderer
- `renderers/manim/compound_interest.py` — thin executable entry point

## Boundary

The renderer may control:

- timing
- animation
- camera
- typography
- visual style

It must not change or recalculate the numerical model.

## Result

A financial scene generator can now stay completely unaware of Manim. A future Motion Canvas renderer can consume the same IR and implement the same vocabulary independently.

## Next

Build reusable style specifications and then add the Motion Canvas adapter against the same Scene IR + Animation IR.
