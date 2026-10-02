# Motion Canvas renderer

The Motion Canvas adapter consumes the same renderer-neutral Scene IR,
Animation IR, and Style IR used by the Manim adapter.

## First scene: compound interest

The first end-to-end scene is:

```text
CompoundInterest model
        ↓
compound_interest_scene.py
        ↓
Scene IR
        ↓
compound_interest.json
        ↓
Motion Canvas
```

Entry point:

```text
src/compound_interest.ts
```

The scene uses the existing `CompoundInterest(1000, 0.08, 30)` model and
renders the timeline, growth curve, money particles, and formula.

## Regenerate scene data

From the repository root:

```bash
python renderers/motion_canvas/export_compound_interest.py
```

This regenerates:

```text
renderers/motion_canvas/data/compound_interest.json
```

Python remains the source of truth for financial calculations. Motion Canvas
only turns serialized scene semantics into visual objects and animation.

## Motion Canvas project

Copy the `renderers/motion_canvas` directory into a Motion Canvas 3.x
project, or use its source files as the renderer package.

The scene can then be registered as the project's entry scene using the normal
Motion Canvas project configuration.

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
