"""Baseline article-to-story compiler.

This deterministic compiler is deliberately conservative. It selects source
sentences rather than inventing financial facts. A future semantic/LLM compiler
can implement the same interface and produce richer narration.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

from engine.article_ingest import ArticleDocument
from engine.narrative_ir import Claim, ShortFormStory, SourceReference, StoryBeat


_VISUAL_RULES = {
    "growth": "exponential_curve",
    "grow": "exponential_curve",
    "investment": "particles_and_flow",
    "capital": "particles_and_flow",
    "inflation": "purchasing_power_field",
    "risk": "stochastic_paths",
    "uncertainty": "stochastic_paths",
    "volatile": "stochastic_paths",
    "dispersion": "distribution",
    "correlation": "coupled_trajectories",
    "diversif": "correlated_paths",
    "allocation": "simplex",
    "portfolio": "network",
    "supply": "flow_field",
    "demand": "flow_field",
    "network": "graph",
    "cycle": "wave",
    "rate": "curve_and_slope",
    "optimization": "loss_surface",
    "opportun": "highlighted_network",
}


def compile_story(
    article: ArticleDocument,
    target_duration: float = 90.0,
    max_claims: int = 5,
) -> ShortFormStory:
    if not article.paragraphs:
        raise ValueError("article contains no usable paragraphs")

    source = SourceReference(
        url=article.url,
        title=article.title,
        publisher=article.publisher,
        accessed_at=datetime.now(timezone.utc).isoformat(),
    )

    scored = sorted(
        enumerate(article.paragraphs),
        key=lambda item: _score(item[1], article.title),
        reverse=True,
    )
    selected = [text for _, text in scored[:max_claims]]
    claims = [
        Claim(
            id=f"C{i + 1}",
            text=_sentence(text),
            importance=max(0.1, 1.0 - i * 0.12),
            source=source,
        )
        for i, text in enumerate(selected)
    ]

    thesis = _thesis(article.title, claims)
    beats = _build_beats(article.title, thesis, claims, target_duration)

    story = ShortFormStory(
        title=article.title or "Untitled financial insight",
        thesis=thesis,
        target_duration=target_duration,
        source=source,
        claims=claims,
        beats=beats,
        disclaimer="Source-grounded summary. Not investment advice.",
    )
    story.validate()
    return story


def _score(text: str, title: str) -> float:
    words = re.findall(r"[A-Za-z][A-Za-z'-]+", text.lower())
    if not words:
        return 0.0
    keywords = set(re.findall(r"[A-Za-z][A-Za-z'-]+", title.lower()))
    finance = {
        "market", "investment", "investor", "portfolio", "growth", "risk",
        "inflation", "capital", "economy", "rates", "returns", "opportunity",
        "demand", "supply", "ai", "technology",
    }
    score = sum(1.0 for word in words if word in finance)
    score += 0.5 * sum(1.0 for word in words if word in keywords)
    return score + min(len(words), 80) / 160.0


def _sentence(text: str, limit: int = 34) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentence = max(sentences, key=lambda item: min(len(item.split()), limit))
    words = sentence.split()
    if len(words) <= limit:
        return sentence
    return " ".join(words[:limit]).rstrip(",;:") + "…"


def _thesis(title: str, claims: list[Claim]) -> str:
    if title:
        return title.rstrip(".")
    return claims[0].text if claims else "The market is changing"


def _visual_for(text: str) -> str:
    lower = text.lower()
    for keyword, visual in _VISUAL_RULES.items():
        if keyword in lower:
            return visual
    return "flow_field"


def _build_beats(
    title: str,
    thesis: str,
    claims: list[Claim],
    target: float,
) -> list[StoryBeat]:
    if target <= 30:
        durations = [3, 7, max(1, target - 10)]
    else:
        durations = [4, 8, 15, 15, 15, 15, 10, 3]

    beats: list[StoryBeat] = []
    beats.append(StoryBeat(
        "hook", "hook",
        _hook(title, thesis),
        durations[0], [], "kinetic_title", "thesis",
    ))
    beats.append(StoryBeat(
        "context", "context",
        thesis + ".",
        durations[1], ["C1"] if claims else [], "overview_network", "context",
    ))

    body_claims = claims[:3]
    for i, claim in enumerate(body_claims, start=1):
        beats.append(StoryBeat(
            f"idea_{i}",
            f"idea_{i}",
            claim.text,
            durations[min(i + 1, len(durations) - 1)],
            [claim.id],
            _visual_for(claim.text),
            "key_fact",
        ))

    if claims:
        beats.append(StoryBeat(
            "implication",
            "implication",
            "The important question is what this change means for the broader investment picture.",
            10,
            [claims[0].id],
            "portfolio_network",
            "implication",
        ))

    beats.append(StoryBeat(
        "payoff",
        "payoff",
        "The goal is to understand the forces changing the landscape—not just the headlines.",
        8,
        [claims[0].id] if claims else [],
        "converging_paths",
        "payoff",
    ))
    beats.append(StoryBeat(
        "source",
        "source",
        "Source and context shown on screen.",
        3,
        [],
        "source_card",
        "disclaimer",
    ))

    scale = min(1.0, target / sum(beat.duration for beat in beats))
    if scale < 1.0:
        for beat in beats:
            beat.duration = round(beat.duration * scale, 3)
    return beats


def _hook(title: str, thesis: str) -> str:
    if title:
        return title.rstrip(".") + "—here's what matters."
    return thesis + "—here's what matters."
