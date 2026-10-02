# Renderers

Renderer adapters convert Scene IR + Animation IR into concrete animation systems.

## Public API

The renderer registry keeps renderer selection out of scene generators:

```python
from renderers import get

renderer = get("manim")
renderer.render(scene, manim_scene)
```

Built-in renderers are loaded lazily, so adding a renderer does not force its runtime dependencies onto the engine.

## Architecture

```text
financial model
      ↓
    Scene IR
      ↓
 Animation IR + Style IR
      ↓
   renderer bridge
      ↓
 Manim / Motion Canvas / ...
```

## Renderer bridge

Python is the source of truth for scene generation. For TypeScript renderers, `engine/serialization.py`
exports the same Scene IR as JSON.

```python
from engine.generators.compound_interest_scene import build_scene
from engine.serialization import scene_to_json

print(scene_to_json(build_scene()))
```

Motion Canvas consumes that JSON through `renderers/motion_canvas/src/renderer.ts`.

### Rules

- The engine owns financial truth and scene semantics.
- The animation vocabulary stays renderer-neutral.
- Renderers map vocabulary to framework-specific APIs.
- Renderers never recalculate financial values.
- New renderer implementations should consume the same Scene IR before introducing renderer-specific scene logic.
