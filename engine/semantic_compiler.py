"""Semantic compiler contracts and validation."""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Protocol

from engine.data_extraction import NumericFact
from engine.narrative_ir import Claim, ShortFormStory, SourceReference, StoryBeat


@dataclass(frozen=True)
class SemanticClaim:
    id: str
    text: str
    source_paragraph: int
    data_ids: tuple[str, ...] = ()
    importance: float = 1.0


@dataclass(frozen=True)
class SemanticBeat:
    id: str
    purpose: str
    narration: str
    duration: float
    claim_ids: tuple[str, ...]
    visual_concept: str
    emphasis: str = ""


@dataclass(frozen=True)
class SemanticStory:
    title: str
    thesis: str
    beats: tuple[SemanticBeat, ...]
    disclaimer: str = "Source-grounded summary. Not investment advice."


class LLMClient(Protocol):
    def complete_json(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        ...


class SemanticCompiler:
    """Compile article evidence into a validated SemanticStory."""

    def __init__(self, client: LLMClient):
        self.client = client

    def compile(
        self,
        title: str,
        paragraphs: list[str],
        facts: list[NumericFact],
        source: SourceReference,
        target_duration: float = 90.0,
    ) -> ShortFormStory:
        payload = {
            "title": title,
            "paragraphs": [
                {"index": i, "text": paragraph}
                for i, paragraph in enumerate(paragraphs)
            ],
            "numeric_facts": [
                {
                    "id": fact.id,
                    "value": fact.value,
                    "raw_value": fact.raw_value,
                    "unit": fact.unit,
                    "context": fact.context,
                    "paragraph_index": fact.paragraph_index,
                }
                for fact in facts
            ],
            "target_duration": target_duration,
        }

        result = self.client.complete_json(
            _SYSTEM_PROMPT,
            json.dumps(payload, ensure_ascii=False),
            semantic_story_schema(),
        )
        semantic = parse_semantic_story(result)
        validate_semantic_story(semantic, paragraphs, facts, target_duration)

        claims = [
            Claim(
                id=claim.id,
                text=claim.text,
                importance=claim.importance,
                source=source,
                factual=True,
                data_refs=list(claim.data_ids),
                source_paragraph=claim.source_paragraph,
            )
            for claim in semantic.claims
        ]

        beats = [
            StoryBeat(
                id=beat.id,
                purpose=beat.purpose,
                narration=beat.narration,
                duration=beat.duration,
                claims=list(beat.claim_ids),
                visual_concept=beat.visual_concept,
                emphasis=beat.emphasis,
            )
            for beat in semantic.beats
        ]

        story = ShortFormStory(
            title=semantic.title,
            thesis=semantic.thesis,
            target_duration=target_duration,
            source=source,
            claims=claims,
            beats=beats,
            disclaimer=semantic.disclaimer,
        )
        story.validate()
        return story


def semantic_story_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["title", "thesis", "claims", "beats", "disclaimer"],
        "properties": {
            "title": {"type": "string"},
            "thesis": {"type": "string"},
            "disclaimer": {"type": "string"},
            "claims": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "text", "source_paragraph", "data_ids", "importance"],
                    "properties": {
                        "id": {"type": "string"},
                        "text": {"type": "string"},
                        "source_paragraph": {"type": "integer", "minimum": 0},
                        "data_ids": {"type": "array", "items": {"type": "string"}},
                        "importance": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                },
            },
            "beats": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "purpose", "narration", "duration", "claim_ids", "visual_concept", "emphasis"],
                    "properties": {
                        "id": {"type": "string"},
                        "purpose": {"type": "string"},
                        "narration": {"type": "string"},
                        "duration": {"type": "number", "minimum": 0},
                        "claim_ids": {"type": "array", "items": {"type": "string"}},
                        "visual_concept": {"type": "string"},
                        "emphasis": {"type": "string"},
                    },
                },
            },
        },
    }


def parse_semantic_story(data: dict[str, Any]) -> SemanticStory:
    claims = tuple(
        SemanticClaim(
            id=item["id"],
            text=item["text"],
            source_paragraph=item["source_paragraph"],
            data_ids=tuple(item.get("data_ids", [])),
            importance=float(item.get("importance", 1.0)),
        )
        for item in data["claims"]
    )
    beats = tuple(
        SemanticBeat(
            id=item["id"],
            purpose=item["purpose"],
            narration=item["narration"],
            duration=float(item["duration"]),
            claim_ids=tuple(item.get("claim_ids", [])),
            visual_concept=item["visual_concept"],
            emphasis=item.get("emphasis", ""),
        )
        for item in data["beats"]
    )
    return SemanticStory(
        title=data["title"],
        thesis=data["thesis"],
        claims=claims,
        beats=beats,
        disclaimer=data.get("disclaimer", ""),
    )


def validate_semantic_story(
    story: SemanticStory,
    paragraphs: list[str],
    facts: list[NumericFact],
    target_duration: float,
) -> None:
    claim_ids = {claim.id for claim in story.claims}
    data_ids = {fact.id for fact in facts}
    facts_by_id = {fact.id: fact for fact in facts}

    if not story.claims:
        raise ValueError("semantic compiler returned no claims")
    if not story.beats:
        raise ValueError("semantic compiler returned no story beats")

    for claim in story.claims:
        if claim.source_paragraph < 0 or claim.source_paragraph >= len(paragraphs):
            raise ValueError(f"claim {claim.id} references invalid paragraph")
        missing = set(claim.data_ids) - data_ids
        if missing:
            raise ValueError(f"claim {claim.id} references unknown data: {sorted(missing)}")
        wrong_paragraph = [
            data_id
            for data_id in claim.data_ids
            if facts_by_id[data_id].paragraph_index != claim.source_paragraph
        ]
        if wrong_paragraph:
            raise ValueError(
                f"claim {claim.id} references data from another paragraph: "
                f"{sorted(wrong_paragraph)}"
            )

    for beat in story.beats:
        missing = set(beat.claim_ids) - claim_ids
        if missing:
            raise ValueError(f"beat {beat.id} references unknown claims: {sorted(missing)}")

    total = sum(beat.duration for beat in story.beats)
    if total > target_duration + 1e-9:
        raise ValueError(f"semantic story is {total:.2f}s, over {target_duration:.2f}s")
    if total < 1:
        raise ValueError("semantic story has no meaningful duration")


_SYSTEM_PROMPT = """You are the semantic compiler for a financial short-form video system.

Your job is to turn source evidence into a compelling 60–90 second explainer.

Rules:
1. Use ONLY the supplied paragraphs and numeric_facts.
2. Never invent a number, date, percentage, company fact, causal relationship, or quote.
3. Every factual claim must point to its source_paragraph.
4. If a claim uses a numeric fact, include its exact data_id.
5. Narration may paraphrase, but must preserve the source meaning.
6. Prefer one central thesis and 2–4 supporting ideas.
7. Write spoken narration, not article prose.
8. Use visual_concept names from the existing mathematical vocabulary when possible.
9. Do not give investment advice or recommendations.
10. Fit all beat durations inside target_duration.
11. The hook should create curiosity without adding unsupported facts.
12. Keep the source/disclaimer beat short.

The output MUST match the supplied JSON schema."""
