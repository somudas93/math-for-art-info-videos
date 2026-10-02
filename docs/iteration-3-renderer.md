# Iteration 3 — Renderer Layer

The renderer layer is now separated from mathematical models and Scene IR.

```text
financial model → Scene IR → renderer → video
```

The first adapter targets Manim and renders the compound-interest composition as axes, an equation, an exponential-value curve, and particles.

## Boundary

The renderer may control:

- camera
- timing
- animation
- typography
- visual style

It must not change the numerical model.

## Next

Add reusable renderer primitives so Scene IR objects such as `curve`, `particles`, `timeline`, and `label` map to renderer objects without embedding financial logic inside the renderer.
