# Architecture

## Core pipeline

Financial concept
→ concept model
→ numerical simulation
→ Scene IR
→ visual generators
→ Manim / Motion Canvas
→ narration + subtitles
→ video

## Separation of concerns

- **Mathematical model:** verified numerical state.
- **Visual generator:** geometry, particles, curves, fields, and other primitives.
- **Animation layer:** time, transitions, camera, emphasis, synchronization.
- **Narrative layer:** explains the same model in natural language.
- **Style layer:** visual aesthetics only.

## Scene IR

The long-term goal is a renderer-independent representation describing what the viewer should understand rather than implementation-specific drawing calls.
