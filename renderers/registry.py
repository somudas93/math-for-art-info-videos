"""Renderer registry with lazy built-in adapters."""
from __future__ import annotations

from importlib import import_module

from renderers.base import Renderer

_RENDERERS: dict[str, Renderer] = {}
_BUILTINS = {
    "manim": ("renderers.manim.renderer", "ManimRenderer"),
}


def register(renderer: Renderer) -> Renderer:
    _RENDERERS[renderer.name] = renderer
    return renderer


def get(name: str) -> Renderer:
    if name not in _RENDERERS and name in _BUILTINS:
        module_name, class_name = _BUILTINS[name]
        renderer_class = getattr(import_module(module_name), class_name)
        _RENDERERS[name] = renderer_class()

    try:
        return _RENDERERS[name]
    except KeyError as exc:
        available = ", ".join(sorted(set(_RENDERERS) | set(_BUILTINS))) or "none"
        raise ValueError(f"Unknown renderer '{name}'. Available: {available}") from exc


def names() -> list[str]:
    return sorted(set(_RENDERERS) | set(_BUILTINS))
