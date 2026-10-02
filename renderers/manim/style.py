"""Apply renderer-neutral styles to Manim objects."""
from __future__ import annotations

from typing import Any

from engine.style_ir import StyleSpec


def apply_style(mobject: Any, style: StyleSpec | None) -> Any:
    if style is None:
        return mobject

    if style.stroke is not None and hasattr(mobject, "set_stroke"):
        mobject.set_stroke(color=style.stroke)

    if style.fill is not None and hasattr(mobject, "set_fill"):
        mobject.set_fill(color=style.fill)

    if style.stroke_width is not None and hasattr(mobject, "set_stroke"):
        mobject.set_stroke(width=style.stroke_width)

    if style.opacity is not None and hasattr(mobject, "set_opacity"):
        mobject.set_opacity(style.opacity)

    if style.fill_opacity is not None and hasattr(mobject, "set_fill"):
        mobject.set_fill(opacity=style.fill_opacity)

    if style.scale is not None:
        mobject.scale(style.scale)

    if style.font_size is not None and hasattr(mobject, "scale"):
        # Text/MathTex objects can use renderer-specific font sizing.
        current = getattr(mobject, "font_size", None)
        if current and current > 0:
            mobject.scale(style.font_size / current)

    return mobject
