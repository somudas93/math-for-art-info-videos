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

## Style boundary

Style is renderer-neutral:

- font
- font size
- stroke width
- stroke
- fill
- opacity
- fill opacity
- scale
- named style preset

The Manim adapter decides how those properties map to Manim APIs.

Financial models never depend on style or rendering.

## Result

A financial scene generator can stay completely unaware of Manim. A future Motion Canvas renderer can consume the same Scene IR + Animation IR + Style IR and implement the same visual vocabulary independently.

## Next

Add the Motion Canvas adapter against the same IR, then build a small style library for financial visual language.
