"""Reusable renderer-neutral visual and animation vocabulary.

These enums keep Scene IR readable while avoiding renderer-specific strings.
""" 
from __future__ import annotations

from enum import Enum


class ObjectKind(str, Enum):
    TIMELINE = "timeline"
    CURVE = "curve"
    PARTICLES = "particles"
    LABEL = "label"
    GROUP = "group"
    LINE = "line"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"


class AnimationAction(str, Enum):
    CREATE = "create"
    DRAW = "draw"
    GROW = "grow"
    MOVE = "move"
    TRANSFORM = "transform"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    HIGHLIGHT = "highlight"
    WAIT = "wait"


class Easing(str, Enum):
    LINEAR = "linear"
    SMOOTH = "smooth"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
