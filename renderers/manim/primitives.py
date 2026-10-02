"""Reusable Manim primitives for Scene IR objects."""
from __future__ import annotations

import math
from typing import Any, Iterable

from manim import Axes, Circle, Dot, Line, MathTex, Rectangle, Text, VGroup, VMobject


def render_timeline(obj):
    data = obj.data
    start = data["start"]
    end = data["end"]
    step = max(1, (end - start) // 5 or 1)

    y_min = data.get("y_min", 0.0)
    y_max = data.get("y_max", max(1.0, y_min + 1.0))
    y_step = data.get("y_step", max(1.0, (y_max - y_min) / 5.0))

    return Axes(
        x_range=[start, end, step],
        y_range=[y_min, y_max, y_step],
        x_length=10,
        y_length=5,
    )


def render_curve(axes, obj):
    if axes is None:
        raise ValueError("curve objects require a timeline/axes object")

    points = obj.data["points"]
    if not points:
        return VMobject()

    graph = VMobject()
    graph.set_points_as_corners([axes.c2p(x, y) for x, y in points])
    return graph


def render_particles(axes, obj):
    if axes is None:
        raise ValueError("particles objects require a timeline/axes object")

    values = obj.data["values"]
    radius = obj.data.get("radius", 0.045)
    return VGroup(
        *[Dot(axes.c2p(i, value), radius=radius) for i, value in enumerate(values)]
    )


def render_label(obj):
    text = obj.data["text"]
    position = obj.data.get("position")
    rendered = MathTex(text) if any(c in text for c in "^_{}\\") else Text(text)
    if position is not None:
        rendered.move_to(position)
    return rendered


def render_line(obj):
    start = obj.data["start"]
    end = obj.data["end"]
    return Line(start, end)


def render_circle(obj):
    return Circle(radius=obj.data.get("radius", 1.0))


def render_rectangle(obj):
    return Rectangle(
        width=obj.data.get("width", 2.0),
        height=obj.data.get("height", 1.0),
    )


def render_group(axes, obj):
    children = obj.data.get("objects", [])
    if not isinstance(children, Iterable):
        raise ValueError("group.objects must be iterable")
    return VGroup(*children)


def render_object(axes: Any, obj):
    if obj is None:
        return None

    renderers = {
        "timeline": render_timeline,
        "curve": lambda item: render_curve(axes, item),
        "particles": lambda item: render_particles(axes, item),
        "label": render_label,
        "line": render_line,
        "circle": render_circle,
        "rectangle": render_rectangle,
        "group": lambda item: render_group(axes, item),
    }

    renderer = renderers.get(obj.kind)
    if renderer is None:
        return None
    return renderer(obj)
