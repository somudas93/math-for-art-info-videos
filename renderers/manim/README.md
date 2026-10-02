# Manim renderer

The Manim adapter is a concrete implementation of the renderer library.

Run with Manim installed:

`manim -pqh renderers/manim/compound_interest.py CompoundInterestScene`

## Structure

- `primitives.py` maps Scene IR object kinds to Manim objects.
- `animation.py` maps the reusable animation vocabulary to Manim animations.
- `renderer.py` builds and renders a complete Scene.
- `compound_interest.py` is only a thin executable entry point.

The scene generator does not import Manim. The renderer is downstream of the numerical source of truth.

## Animation vocabulary

Current portable actions:

- `create`
- `draw`
- `grow`
- `move`
- `transform`
- `fade_in`
- `fade_out`
- `highlight`
- `wait`

Supported easing names start with `linear`, `smooth`, `ease_in`, `ease_out`, and `ease_in_out`.
