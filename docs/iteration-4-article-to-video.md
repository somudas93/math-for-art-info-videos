# Iteration 4 — Article → 90-Second Story Compiler

The system now expands upward from mathematical scene generation into a
source-grounded short-form video pipeline.

## Target

Input:

    article URL

Output:

    source-grounded 60–90 second storyline
    → visual plan
    → Scene IR
    → Manim / Motion Canvas
    → narration + subtitles
    → vertical MP4

The hard boundary remains:

    source/article claims
        ↓
    narrative compression
        ↓
    financial/data model
        ↓
    Scene IR
        ↓
    renderer

The narrative layer may decide **what to explain**, but it must not invent,
alter, or silently reinterpret financial numbers.

## 1. Article ingestion

The article reader should extract:

- title
- publisher
- publication date
- canonical URL
- headings/sections
- paragraphs
- tables and chart captions when available
- explicit numerical claims
- source notes/disclaimers

The raw article is retained as the evidence layer.

For web articles such as J.P. Morgan Private Bank research, this is especially
useful because the source material commonly already contains themes, key
takeaways, opportunities, risks and portfolio implications.

## 2. Claim extraction

Convert the article into atomic claims.

Example:

    Claim C1:
    "AI-driven demand is increasing investment in semiconductors,
    hardware, power infrastructure and automation."

A claim keeps its source reference and importance score.

Claims are not yet visuals.

## 3. Thesis extraction

The compiler asks:

    What is this article really trying to make the reader understand?

A good 90-second thesis is normally one sentence.

Example structure:

    "The market story is not simply X; the more important shift is Y."

The thesis becomes the spine of the video.

## 4. Narrative compression

The compiler selects only the claims needed to support the thesis.

Default 90-second structure:

    0–04s   HOOK
    04–12s  CONTEXT
    12–28s  IDEA 1
    28–45s  IDEA 2
    45–62s  IDEA 3
    62–78s  IMPLICATION
    78–87s  PAYOFF
    87–90s  SOURCE / DISCLAIMER

This is a default, not a rigid template.

The compiler should optimize for:

    comprehension > completeness > article structure

It should not try to summarize every section.

## 5. Story Beat

Each beat contains:

- purpose
- narration
- duration
- supporting claims
- visual concept
- emphasis

This becomes the bridge between language and graphics.

Example:

    HOOK
    "Three forces are reshaping the investment landscape."

    VISUAL
    Three mathematical fields converge into one portfolio.

Then:

    IDEA 1
    "AI is changing where capital is being deployed."

    VISUAL
    Capital particles flow toward a growing infrastructure network.

## 6. Narrative → mathematical visual mapping

The compiler should select an existing mathematical primitive before inventing
a new one.

Examples:

    growth        → exponential curve
    acceleration  → derivative / slope
    uncertainty   → stochastic trajectories
    dispersion    → distribution / particles
    correlation   → coupled trajectories
    competition   → graph/network
    flows         → flow field
    allocation    → simplex
    cycles        → waves
    compounding   → recursive particles
    optimization  → loss surface + gradient
    concentration → density field
    diversification → correlated paths

This keeps the 30-family mathematical vocabulary reusable.

## 7. Financial truth boundary

There are three types of statements:

### Source facts

Taken directly from the article.

### Derived calculations

Computed from source data using an explicit financial model.

### Interpretive narration

A concise explanation intended to help the viewer understand the source.

The renderer must never modify source facts or derived calculations.

Every numerical visual should be traceable to either:

    source claim → data
    or
    source claim → explicit calculation

## 8. TikTok-style visual grammar

The video should behave like a short-form explainer, not a narrated PDF.

Preferred rhythm:

- immediate visual hook
- one idea per shot
- large kinetic headline
- animated numbers
- mathematical transformations
- visual continuity between beats
- frequent but meaningful scene changes
- minimal paragraphs on screen
- subtitles generated from narration
- source/disclaimer kept visually secondary

A beat should generally introduce only one new conceptual object.

## 9. Source grounding

The final story object should retain:

    source URL
    source title
    claim IDs
    derived-data provenance

This allows a later audit view:

    "Why did this sentence appear in the video?"

Answer:

    sentence → beat → claim → source paragraph

## 10. Example

For a J.P. Morgan Private Bank outlook discussing AI, fragmentation and
inflation, the compiler might reduce the article to:

    Hook:
    "Three forces are changing the investment landscape."

    Setup:
    "AI is accelerating capital investment, while geopolitics is reshaping
    supply chains and inflation is becoming less predictable."

    Body:
    1. AI → capital-flow network
    2. Fragmentation → network splitting into regional clusters
    3. Inflation → purchasing-power / price-growth field

    Implication:
    "The portfolio problem therefore shifts from predicting one future to
    building resilience across several futures."

    Payoff:
    "The important question is not just what happens next—but how prepared
    the portfolio is for different outcomes."

This is a transformation of the article's ideas, not a reproduction of its
prose.

## 11. New pipeline

    URL
      ↓
    Article Extractor
      ↓
    Claim Extractor
      ↓
    Thesis Compiler
      ↓
    60–90s Narrative IR
      ↓
    Financial/Data Model
      ↓
    Visual Planner
      ↓
    Scene IR
      ↓
    Manim / Motion Canvas
      ↓
    TTS + subtitles
      ↓
    vertical MP4

## 12. Next implementation steps

1. Implement article ingestion from a URL.
2. Implement claim/thesis extraction.
3. Add a 90-second narrative compiler.
4. Add narrative-to-visual mapping.
5. Add vertical 9:16 composition to the renderer layer.
6. Add narration timing and subtitle tracks.
7. Test the whole pipeline on one real J.P. Morgan Private Bank article.


## 13. Implemented baseline

The first runnable implementation is now in the repository:

- `engine/article_ingest.py` — fetches an HTML article and extracts title, headings and usable paragraphs.
- `engine/narrative_ir.py` — source, claim, beat and story contracts.
- `engine/narrative_compiler.py` — deterministic source-grounded 90-second compiler.
- `engine/visual_planner.py` — maps story beats to existing mathematical visual primitives.
- `scripts/compile_article.py` — command-line entry point.

Example:

    python scripts/compile_article.py \
      "https://example.com/article" \
      --duration 90 \
      --claims 5 \
      --output story.json

The baseline intentionally prefers conservative extraction and paraphrase over
inventing facts. A semantic/LLM compiler can later replace the heuristic
selection while producing the same Narrative IR.

The next production step is to add an LLM-backed semantic compiler with
structured output validation, followed by vertical Scene IR generation,
subtitle timing and TTS.


## 14. Narrative → Scene IR bridge

The Narrative IR is now connected to the renderer-neutral Scene IR through a
Storyboard layer:

    ShortFormStory
        ↓
    VisualPlanner
        ↓
    Storyboard
        ↓
    Scene IR (one scene per beat)
        ↓
    Manim / Motion Canvas

Added:

- `engine/storyboard_ir.py`
- `engine/story_scene_compiler.py`
- `engine/serialization.py` storyboard serialization
- `scripts/compile_video_plan.py`

Each generated Scene carries provenance metadata:

- beat ID
- beat purpose
- narration
- claim IDs
- visual concept
- source URL
- story title

Narration remains metadata rather than being baked into the visual layer. This
creates a clean future connection to TTS and subtitle timing.

Example command:

    python scripts/compile_video_plan.py \
      "https://example.com/article" \
      --duration 90 \
      --claims 5 \
      --output storyboard.json

The resulting JSON contains both the source-grounded Story IR and the ordered
Scene IR sequence.
