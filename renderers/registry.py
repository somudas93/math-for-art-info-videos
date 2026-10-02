"""Renderer registry."""
from __future__ import annotations

from renderers.base import Renderer

_RENDERERS: dict[str, Renderer] = {}


def register(renderer: Renderer) -> Renderer:
    _RENDERERS[renderer.name] = renderer
    return renderer


def get(name: str) -> Renderer:
    try:
        return _RENDERERS[name]
    except KeyError as exc:
        available = ", ".join(sorted(_RENDERERS)) or "none"
        raise ValueError(f"Unknown renderer '{name}'. Available: {available}") from exc


def names() -> list[str]:
    return sorted(_RENDERERS)
