# Iteration 3 — Animation IR

Animation is now described independently of Manim.

```text
Scene IR
   +
Animation IR
   ↓
Renderer adapter
   ↓
Manim / Motion Canvas
```

Animation specs contain an action, target object, duration, delay, easing, and optional renderer-neutral data.

Current actions:
- `create`
- `fade_in`

The Manim adapter translates these actions into Manim animations. Future renderers can interpret the same plan differently.

Style is represented separately by `StyleSpec` so visual appearance does not leak into mathematical models.
