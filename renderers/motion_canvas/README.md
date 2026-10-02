# Motion Canvas renderer

The Motion Canvas adapter consumes the same renderer-neutral Scene IR,
Animation IR, and Style IR used by the Manim adapter.

## Data flow

financial model → Scene IR → JSON → Motion Canvas

Python remains the source of truth for financial calculations. Motion Canvas
only turns serialized scene semantics into visual objects and animation.

## Bridge

Use `engine.serialization.scene_to_json()` to export a generated scene:

```python
from engine.generators.compound_interest_scene import build_scene
from engine.serialization import scene_to_json

print(scene_to_json(build_scene()))
```

Save that JSON into the Motion Canvas project as scene data. The TypeScript
adapter accepts the resulting object.

## Current coverage

Objects:
- timeline
- curve
- particles
- label
- line
- circle
- rectangle
- group

Animation actions:
- create
- draw
- grow
- fade_in
- fade_out
- highlight
- move
- transform
- wait

The adapter intentionally does not implement financial calculations.
