# Iteration 3 — Animation IR

Animation is described independently of a renderer.

```text
Scene IR
   +
Animation IR
   ↓
Renderer adapter
   ↓
Manim / Motion Canvas
```

## Portable vocabulary

Animation specs contain an action, target object, duration, delay, easing, and optional renderer-neutral data.

Current actions:

- `create`
- `draw`
- `grow`
- `move`
- `transform`
- `fade_in`
- `fade_out`
- `highlight`
- `wait`

Easing vocabulary currently includes:

- `linear`
- `smooth`
- `ease_in`
- `ease_out`
- `ease_in_out`

The Manim adapter translates these actions into Manim animations. Future renderers can interpret the same plan differently.

Style remains represented separately by `StyleSpec` so visual appearance does not leak into mathematical models.
