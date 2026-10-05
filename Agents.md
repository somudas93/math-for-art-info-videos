# Agents.md

## Project

**Repository:** `somudas93/math-for-art-info-videos`

**Purpose:** Build a reusable system that turns mathematical models, financial data, and source-grounded articles into clear narrated short-form infographic videos.

The long-term pipeline is:

```
Article URL
  ↓
Article ingestion
  ↓
Evidence / numeric data extraction
  ↓
LLM semantic compiler
  ↓
Narrative IR
  ↓
Financial / mathematical model compiler
  ↓
Visual model
  ↓
Storyboard / Scene IR
  ↓
Manim / Motion Canvas renderer
  ↓
TTS + subtitles
  ↓
9:16 MP4
```

The governing principle is:

```
source → data → model → calculation → visualization → narration → style
```

The financial model is the source of numerical truth. Artistic rendering must never silently change a factual number or derived calculation.

---

## Agent working rules

1. Read this file before changing architecture.
2. Prefer small, composable modules over renderer-specific logic.
3. Keep financial calculations independent from Manim and Motion Canvas.
4. Preserve provenance whenever a value moves between layers.
5. Never invent financial facts, dates, percentages, monetary values, or causal claims.
6. If a visual uses a normalized baseline, mark it as normalized and do not narrate it as a source monetary amount.
7. Extend the existing mathematical vocabulary before inventing one-off visual primitives.
8. Keep Scene IR renderer-neutral.
9. Treat Manim and Motion Canvas as adapters, not sources of business logic.
10. Add tests for deterministic numerical behavior and provenance rules when adding models.
11. Update the relevant iteration document when a major architectural layer is added.
12. Keep this `Agents.md` current when architecture, commands, contracts, or limitations change.

---

## Mathematical-art foundation

The project was initially created as a mathematical/procedural-art laboratory inspired by procedural systems such as LingDong's:

- `fishdraw`
- `shan-shui-inf`

The mathematical vocabulary currently covers 30 primitive families:

1. Geometry
2. Noise
3. Flow fields
4. Fractals
5. L-systems
6. Particles
7. Parametric curves
8. Transformations and symmetry
9. Probability / random processes
10. Spatial geometry / Voronoi
11. Graphs / networks
12. Dynamical systems
13. Waves / signal composition
14. Signed distance fields
15. Optimization
16. Number-theoretic patterns
17. Cellular automata
18. Distance / potential fields
19. Trigonometric patterns
20. Combinatorics
21. Chaos
22. Interpolation
23. 3D geometry
24. Recursive subdivision
25. Financial mappings
26. Calculus
27. Linear algebra
28. Fourier analysis
29. Grids / tilings
30. Simplex / barycentric geometry

The mathematical primitives are intended to become a reusable visual vocabulary rather than isolated demonstrations.

---

## Financial visual mappings

The intended semantic-to-mathematical vocabulary includes:

| Financial idea | Mathematical / visual primitive |
|---|---|
| Compound growth | Exponential curves + recursive particles |
| Inflation | Inverse scaling / purchasing-power field |
| SIP | Repeated particle injection + compounding |
| Amortization | Recursive balance update + area proportions |
| Risk | Distributions + random walks + dispersion |
| Diversification | Correlated trajectories + graphs |
| Liquidity | Flow fields + density |
| Market uncertainty | Stochastic trajectories + confidence bands |
| Optimization | Loss surfaces + gradient paths |
| Correlation | Wave superposition + trajectories |
| Portfolio allocation | Simplex / combinatorial geometry |
| Time value of money | Discounting curves |

Existing experiments are under `experiments/`.

---

## Repository structure

Current important areas:

```
docs/
  architecture.md
  mathematical-art.md
  iteration-2.md
  iteration-3.md
  iteration-3-renderer.md
  iteration-4-article-to-video.md

experiments/
  01_geometry/
  02_noise/
  03_flow_fields/
  04_fractals/
  05_l_systems/
  06_particles/

engine/
  models/
  narrative_ir.py
  article_ingest.py
  narrative_compiler.py
  semantic_compiler.py
  openai_responses.py
  data_extraction.py
  financial_model_ir.py
  financial_models.py
  financial_visual_compiler.py
  visual_model.py
  visual_planner.py
  scene_ir.py
  storyboard_ir.py
  story_scene_compiler.py
  animation_ir.py
  style_ir.py
  styles.py
  vocabulary.py
  serialization.py

renderers/
  base.py
  registry.py
  manim/
  motion_canvas/

scripts/
  compile_article.py
  compile_video_plan.py
  compile_semantic_video.py

tests/
  test_financial_visual_pipeline.py
```

---

# Layer contracts

## 1. Article ingestion

`engine/article_ingest.py`

Provides an `ArticleDocument` from a URL.

Current parser:

- uses a dependency-light standard-library HTML parser
- extracts title
- extracts headings
- extracts paragraphs and useful list items
- skips script/style/noscript/svg content
- deduplicates paragraphs
- filters implausibly short/long text
- keeps the original URL

Known limitation: article extraction is intentionally conservative and is not yet a production-grade browser reader. Tables, chart captions, JavaScript-rendered content, publication dates, canonical links, and complex article layouts need further work.

---

## 2. Numeric evidence extraction

`engine/data_extraction.py`

Defines:

```python
NumericFact(
    id,
    value,
    raw_value,
    unit,
    context,
    paragraph_index,
    source_url,
    kind,
)
```

The extractor recognizes:

- currencies: USD, EUR, GBP, INR, JPY
- currency values with million/billion/trillion and mn/bn/tn
- percentages
- basis points
- durations such as years/months/quarters
- four-digit years
- generic numbers

Every fact retains the paragraph index and source URL.

Important distinction:

**NumericFact is evidence, not financial interpretation.**

A raw `5%` does not become an inflation rate until a model compiler has enough semantic context to establish what the percentage represents.

Known limitations:

- generic non-currency scaled values such as `3.5 million` need richer scale handling
- negative numbers are not currently modeled
- dates are deliberately conservative
- semantic unit interpretation remains a later layer

---

## 3. Semantic compiler

`engine/semantic_compiler.py`

The semantic compiler turns source evidence into a structured story.

Core types:

- `SemanticClaim`
- `SemanticBeat`
- `SemanticStory`
- `LLMClient`
- `SemanticCompiler`

The compiler requires:

- source paragraph for every factual claim
- exact numeric fact IDs for numeric claims
- numeric facts used by a claim must come from the same paragraph as the claim
- beat claim IDs must resolve
- total duration must fit the target
- one central thesis and a small number of supporting ideas
- spoken narration rather than article prose
- no investment advice

The semantic JSON schema is strict and rejects additional properties.

The OpenAI adapter is in:

```
engine/openai_responses.py
```

It uses the Responses API and structured JSON output through a small standard-library HTTP client, so the repository does not require the OpenAI Python SDK.

Environment variables:

```
OPENAI_API_KEY=...
OPENAI_MODEL=...
```

Default model configuration is defined in the adapter and should be reviewed before production deployment.

---

## 4. Narrative IR

`engine/narrative_ir.py`

The renderer-neutral story contract contains:

### SourceReference

- URL
- title
- publisher
- accessed time

### Claim

- ID
- text
- importance
- source
- factual flag
- numeric data references
- source paragraph

### StoryBeat

- ID
- purpose
- narration
- duration
- claim IDs
- visual concept
- emphasis

### ShortFormStory

- title
- thesis
- target duration
- source
- claims
- beats
- disclaimer

The narrative layer decides **what the video explains**.

It must not become the financial source of truth.

---

# 5. Financial model layer

This is the latest architectural addition.

Files:

```
engine/financial_model_ir.py
engine/financial_models.py
engine/financial_visual_compiler.py
engine/visual_model.py
```

## FinancialModel IR

`FinancialModelResult` represents a deterministic model output.

It contains:

- model ID
- model type
- typed model inputs
- calculated points
- x/y labels
- units
- normalized flag
- metadata

Each `ModelInput` retains the raw numeric fact IDs and source paragraph provenance when available.

This establishes the explicit chain:

```
source paragraph
  ↓
NumericFact
  ↓
Claim
  ↓
ModelInput
  ↓
FinancialModelResult
```

## Current deterministic models

### Compound growth

```
V(t) = V₀(1+r)^t
```

The implementation can use `V₀ = 1` as a **normalized visual baseline** when the source does not provide a principal.

That baseline is visual, not a financial fact.

### Purchasing power under inflation

```
P(t) = P₀ / (1+i)^t
```

Again, `P₀ = 1` means normalized purchasing power unless an explicit source principal is introduced by a future model.

---

# 6. Financial visual compiler

`engine/financial_visual_compiler.py`

This is the boundary between semantic claims and mathematical visuals.

It currently uses a conservative rule:

A model is generated only when the claim evidence contains:

- a percentage
- a duration in years
- enough semantic wording to identify the model family

Current mappings:

- inflation / purchasing power / price growth → purchasing-power model
- growth / compound / compounding / return → compound-growth model

If evidence is insufficient, the compiler returns no financial model instead of guessing.

This behavior is intentional.

Future model resolution should become more expressive while preserving the same conservative principle.

---

# 7. Visual Model IR

`engine/visual_model.py`

`VisualModel` converts a financial model into portable geometry.

A curve model exposes:

```
points: [[x, y, z], ...]
x_label
y_label
y_unit
normalized
model_type
```

It also carries model provenance:

```
model_inputs
metadata
```

The visual renderer therefore receives calculated data rather than recalculating finance.

---

# 8. Visual planner

`engine/visual_planner.py`

Maps semantic visual concepts to portable Scene IR object kinds.

Examples:

```
exponential_curve
  → timeline, curve, particles, label

purchasing_power_field
  → curve, particles, label

stochastic_paths
  → timeline, curve, particles

network
  → circle, line, particles

simplex
  → line, particles, label
```

If the LLM emits an unknown visual concept, the planner currently falls back to a generic curve/particle/label plan.

Future work should move toward explicit concept validation and a formal visual vocabulary registry.

---

# 9. Storyboard and Scene IR

`engine/storyboard_ir.py`

A storyboard is an ordered collection of renderer-neutral scenes.

`engine/scene_ir.py` contains:

```SceneObject(
    id,
    kind,
    data,
)
```

and:

```Scene(
    name,
    duration,
    objects,
    animation,
    metadata,
)
```

Scene metadata carries:

- beat ID
- purpose
- narration
- claim IDs
- visual concept
- emphasis
- source URL
- story title
- financial model ID where available
- model provenance where available

This makes the Scene IR auditable without forcing narration into renderer geometry.

---

# 10. Story → Scene compiler

`engine/story_scene_compiler.py`

Current flow:

```
ShortFormStory
  ↓
VisualPlanner
  ↓
FinancialVisualCompiler
  ↓
VisualModel
  ↓
Storyboard
  ↓
Scene IR
```

A model-backed curve now creates a Scene object containing actual calculated points instead of an empty placeholder.

When no model can safely be resolved, the scene retains the semantic placeholder status.

This distinction is important:

- `model_backed` = numerical geometry came from a financial model
- `awaiting_model_data` = known visual family but no numerical model
- `semantic_visual_placeholder` = semantic visual concept exists but concrete geometry is not implemented

---

# 11. Serialization

`engine/serialization.py`

Serializes:

- Scene IR
- Storyboard IR

The output is JSON-compatible and is the bridge to non-Python renderers.

A storyboard contains:

```
name
duration
metadata
scenes[]
```

Financial model results are also exposed through storyboard metadata so downstream tools can audit the calculations.

---

# 12. Animation IR

`engine/animation_ir.py`

Portable animation actions include:

- create
- draw
- grow
- move
- transform
- fade in
- fade out
- highlight
- wait

Animation specifications retain:

- target
- duration
- delay
- easing
- renderer-neutral data

Easing vocabulary includes:

- linear
- smooth
- ease_in
- ease_out
- ease_in_out

---

# 13. Renderer layer

Renderer abstraction:

```
renderers/base.py
renderers/registry.py
```

Current adapters:

### Manim

```
renderers/manim/
```

Contains:

- primitives
- animation adapter
- style adapter
- renderer
- compound-interest scene

### Motion Canvas

```
renderers/motion_canvas/
```

Contains:

- TypeScript types
- primitives
- style adapter
- animation adapter
- renderer
- compound-interest example
- JSON data bridge
- export helper

Renderer adapters should consume Scene IR and should not contain financial-model logic.

---

# 14. Style layer

`engine/style_ir.py`

Portable style parameters include:

- font
- font size
- stroke width
- opacity
- fill opacity
- stroke
- fill
- scale
- arbitrary style data

`engine/styles.py` contains reusable finance styling.

The intended separation is:

```
model → geometry → animation → style
```

not:

```
financial calculation buried inside renderer styling
```

---

# 15. Existing compound-interest path

`engine/models/compound_interest.py`

Current numerical source of truth:

```
V(t) = P(1+r)^t
```

The model exposes:

- `values()`
- `value_at(t)`

The project also has a compound-interest Scene/renderer example.

A previously verified MP4 exists in the project workflow. It is a polished 10-second, 1280×720 H.264 example showing a compound-growth chart, exponential curve, dots, formula, and final value.

Important historical note: the MP4 was verified as an existing artifact; it was not freshly rendered from the latest source in the restricted environment. Do not claim otherwise.

---

# 16. CLI entry points

## Deterministic article compiler

```
python scripts/compile_article.py \
  "https://example.com/article" \
  --duration 90 \
  --claims 5 \
  --output story.json
```

## Storyboard compiler

```
python scripts/compile_video_plan.py \
  "https://example.com/article" \
  --duration 90 \
  --claims 5 \
  --output storyboard.json
```

## Semantic LLM compiler

```
python scripts/compile_semantic_video.py \
  "https://example.com/article" \
  --duration 90 \
  --output semantic_storyboard.json
```

The semantic CLI now passes extracted numeric facts into the financial visual compiler.

Its output includes:

- Story IR
- numeric facts
- Storyboard / Scene IR
- financial model metadata

---

# 17. Testing

Current test:

```
tests/test_financial_visual_pipeline.py
```

It verifies:

- deterministic compound growth
- decreasing purchasing power under positive inflation
- evidence requirements for financial visual compilation
- numeric fact IDs remain attached to model inputs

Whenever a new financial model is introduced, add tests for:

1. formula correctness
2. boundary conditions
3. source-data provenance
4. normalized-vs-factual semantics
5. visual conversion

---

# 18. Iteration history

## Iteration 1 — Foundation

Established:

- repository structure
- mathematical-art experiments
- initial geometry / flow-field / particle primitives
- financial project direction

## Iteration 2 — Mathematical vocabulary

Expanded the reusable mathematical vocabulary to 30 primitive families and mapped financial concepts onto them.

## Iteration 3 — Renderer architecture

Built:

- Scene IR
- vocabulary
- Animation IR
- Style IR
- Manim adapter
- Motion Canvas adapter
- renderer registry
- JSON bridge
- compound-interest example

## Iteration 4 — Article to video

Built:

- article ingestion
- deterministic narrative compiler
- Narrative IR
- Visual Planner
- Storyboard IR
- Story → Scene compiler
- numeric data extraction
- semantic LLM compiler
- structured validation
- OpenAI Responses adapter
- semantic video CLI
- numeric provenance validation

## Current extension — Financial data → visual model

Added:

- typed Financial Model IR
- deterministic compound-growth model
- deterministic purchasing-power model
- Financial Visual Compiler
- renderer-neutral Visual Model
- model-backed Scene geometry
- model provenance in storyboard metadata
- financial visual pipeline tests
- this Agents.md

---

# 19. Provenance invariant

The most important invariant in the repository is:

```
source paragraph
    ↓
numeric fact
    ↓
claim
    ↓
model input
    ↓
calculation
    ↓
visual model
    ↓
scene object
    ↓
renderer
```

At every stage, the system should be able to answer:

> Where did this number come from?

And:

> Which calculation produced this visual?

If the answer cannot be reconstructed, the layer is not production-ready.

---

# 20. What is intentionally NOT finished

The following are known next-stage tasks:

### Data extraction

- robust table extraction
- chart-caption extraction
- better scaled-number parsing
- negative values
- richer financial units
- date normalization
- company/entity extraction
- semantic interpretation of raw numbers

### Financial models

Add typed models for:

- SIP
- amortization
- discounting / present value
- bond duration
- portfolio allocation
- volatility
- normal / lognormal distributions
- random walks
- correlated paths
- correlation matrices
- optimization
- loss surfaces
- liquidity / flow models

Each model must be deterministic and independently testable.

### Model selection

Replace keyword-only model selection with an explicit model registry and typed parameter requirements.

Example future contract:

```
ModelSpec(
    name="purchasing_power",
    required_inputs=["inflation_rate", "periods"],
    optional_inputs=["initial_value"],
    visual_families=["purchasing_power_field"],
)
```

The semantic compiler can then select a model, but the financial layer validates whether the required evidence actually exists.

### Visual grammar

Build reusable visual templates such as:

- number counter
- curve growth
- erosion curve
- particle injection
- network formation
- stochastic fan
- distribution reveal
- simplex allocation
- loss surface descent
- correlated trajectory reveal

### Renderer

Complete:

- proper data-range scaling
- 9:16 composition
- real transform semantics
- font-size propagation
- robust Motion Canvas JSON import
- real particle animation
- scene continuity between beats

### Audio

Add:

- TTS generation
- narration timing
- word/phrase timestamps
- subtitle IR
- subtitle renderer
- audio/video synchronization

### Production pipeline

Final target:

```
article URL
→ evidence
→ semantic story
→ financial model
→ visual model
→ storyboard
→ renderer
→ TTS
→ subtitles
→ 9:16 MP4
```

---

# 21. 9:16 target

The final short-form format should be designed for:

```
1080 × 1920
```

or an equivalent vertical render size.

Composition should reserve regions for:

- headline
- primary mathematical visual
- key number
- optional explanatory label
- subtitles
- source/disclaimer

Do not simply crop a 16:9 scene after rendering. The scene layout should understand vertical composition.

---

# 22. Important renderer limitation history

Motion Canvas currently has known unfinished behavior:

- timeline axes use fixed pixel/range assumptions
- particles use fixed coordinate scaling
- create/draw are partially represented through opacity
- transform is not yet a true geometric transform
- font-size style is not fully propagated
- JSON imports may require `resolveJsonModule`
- TypeScript API compatibility should be verified before claiming a render

These are adapter limitations, not reasons to weaken the Scene IR.

---

# 23. Source-grounded narration rules

Narration can be:

- concise
- explanatory
- visually synchronized
- paraphrased

Narration cannot:

- introduce unsupported numbers
- convert a normalized visual baseline into a factual monetary claim
- imply causality absent from the source
- provide investment recommendations
- alter the meaning of source facts

A strong video may be artistic in presentation while remaining conservative in factual semantics.

---

# 24. Preferred development sequence

When extending the project, use this order:

1. Define the mathematical/financial model.
2. Add deterministic calculations.
3. Add tests.
4. Define portable visual data.
5. Connect semantic claims to model inputs.
6. Preserve provenance.
7. Compile to Scene IR.
8. Add renderer behavior.
9. Add animation.
10. Add narration/subtitles.
11. Render and inspect.
12. Document the iteration.

Avoid starting with renderer effects before the model and data contracts are stable.

---

# 25. Architectural north star

The final system should make it possible to take a sentence such as:

> “Inflation remains elevated while real purchasing power declines.”

and turn it into an auditable chain like:

```
Claim
  ↓
inflation_rate = 4.2%
  ↓
periods = 10 years
  ↓
PurchasingPowerModel
  ↓
P(t) = P₀ / (1 + 0.042)^t
  ↓
normalized purchasing-power curve
  ↓
particle representing the baseline
  ↓
curve erosion animation
  ↓
narration + subtitles
  ↓
vertical video
```

The critical property is not merely that the result looks good.

It is that the result is:

**mathematically explainable, source-grounded, renderer-independent, auditable, reusable, and visually compelling.**
