"""Renderer-neutral style vocabulary."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class StyleSpec:
    """Portable visual style; renderer adapters decide how to implement it."""

    name: str = "default"
    font: str | None = None
    font_size: float | None = None
    stroke_width: float | None = None
    opacity: float | None = None
    fill_opacity: float | None = None
    stroke: str | None = None
    fill: str | None = None
    scale: float | None = None
    data: dict[str, Any] = field(default_factory=dict)
