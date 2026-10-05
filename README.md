# Math for Art Info Videos

A research and engineering lab for turning mathematics, procedural art, and financial models into clear narrated infographic videos.

## Vision

**Mathematical model → visual grammar → animation → narration → educational video**

Inspired by procedural-art systems such as LingDong's fishdraw and Shan-Shui, this project studies how mathematical structure can become a visual language for explaining financial concepts.

## Roadmap

1. Mathematical Art Laboratory
2. Visual Grammar
3. Financial Simulation
4. Animation with Manim and Motion Canvas
5. Audio and narration
6. Scene IR / Concept Compiler

## Design principle

The financial model is the source of truth. Artistic rendering must never silently change a numerical claim.

**model → calculation → visualization → narration → style**

## Iteration 1 — Foundation

This first iteration is intentionally small. It establishes the repository structure and three renderer-independent procedural primitives:

- geometry
- flow fields
- particles

These are the baseline for future financial visualizations.

## Status

Iteration 1 complete. Future iterations can expand the mathematical-art library, financial models, renderers, and narration pipeline without changing this baseline.


## Current pipeline status

The repository now has a source-grounded semantic path in addition to the original mathematical-art and renderer layers:

```
Article URL
  → article evidence
  → numeric facts
  → semantic claims / thesis
  → financial model
  → visual model
  → Storyboard / Scene IR
  → Manim / Motion Canvas
```

The financial model layer currently includes deterministic compound-growth and purchasing-power models. Model inputs retain numeric-fact provenance, and model-backed Scene objects carry calculated points instead of empty visual placeholders when sufficient evidence is available.

See [Agents.md](Agents.md) for the complete architecture, agent conventions, iteration history, current limitations, and next implementation targets.
