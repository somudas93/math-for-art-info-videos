"""Renderer-neutral narrative representation for short-form explainers.

The narrative layer compresses source material into a timed story without
becoming the source of financial truth. Claims should retain source references;
numerical facts should later be resolved by a financial/data model.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class SourceReference:
    url: str
    title: str = ""
    publisher: str = ""
    accessed_at: str = ""


@dataclass(frozen=True)
class Claim:
    id: str
    text: str
    importance: float = 1.0
    source: SourceReference | None = None
    factual: bool = True


@dataclass
class StoryBeat:
    """One viewer-facing beat in a short-form narrative."""

    id: str
    purpose: str
    narration: str
    duration: float
    claims: List[str] = field(default_factory=list)
    visual_concept: str = ""
    emphasis: str = ""

    def __post_init__(self) -> None:
        if self.duration < 0:
            raise ValueError("duration must be non-negative")


@dataclass
class ShortFormStory:
    """A compressed, source-grounded story ready for visual compilation."""

    title: str
    thesis: str
    target_duration: float = 90.0
    source: SourceReference | None = None
    claims: List[Claim] = field(default_factory=list)
    beats: List[StoryBeat] = field(default_factory=list)
    disclaimer: str = ""

    def total_duration(self) -> float:
        return sum(beat.duration for beat in self.beats)

    def validate(self) -> None:
        if not 1.0 <= self.target_duration <= 90.0:
            raise ValueError("target_duration must be between 1 and 90 seconds")

        claim_ids = {claim.id for claim in self.claims}
        missing = {
            claim_id
            for beat in self.beats
            for claim_id in beat.claims
            if claim_id not in claim_ids
        }
        if missing:
            raise ValueError(f"Story references unknown claims: {sorted(missing)}")

        if self.total_duration() > self.target_duration + 1e-9:
            raise ValueError(
                f"Beat duration {self.total_duration():.2f}s exceeds "
                f"target {self.target_duration:.2f}s"
            )

    def narration_text(self) -> str:
        return " ".join(beat.narration.strip() for beat in self.beats if beat.narration)
