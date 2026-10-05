"""Renderer-neutral storyboard container for short-form videos."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engine.scene_ir import Scene


@dataclass
class Storyboard:
    """Ordered Scene IR sequence generated from a ShortFormStory."""

    name: str
    duration: float
    scenes: list[Scene] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def total_duration(self) -> float:
        return sum(scene.duration for scene in self.scenes)

    def validate(self) -> None:
        if self.duration < 0:
            raise ValueError("duration must be non-negative")
        if self.total_duration() > self.duration + 1e-9:
            raise ValueError(
                f"scene duration {self.total_duration():.2f}s exceeds "
                f"storyboard duration {self.duration:.2f}s"
            )
