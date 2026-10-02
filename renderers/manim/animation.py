"""Manim execution of renderer-neutral animation specs."""
from __future__ import annotations

from typing import Any

import numpy as np
from manim import (
    ApplyMethod,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    Transform,
)

from engine.vocabulary import AnimationAction, Easing

_RATE_FUNCS = {
    Easing.LINEAR.value: None,
    Easing.SMOOTH.value: "smooth",
    Easing.EASE_IN.value: "ease_in_quad",
    Easing.EASE_OUT.value: "ease_out_quad",
    Easing.EASE_IN_OUT.value: "ease_in_out_quad",
}


def _rate_func(name: str):
    if name == Easing.LINEAR.value:
        return None

    try:
        from manim import rate_functions
        return getattr(rate_functions, _RATE_FUNCS[name])
    except (KeyError, AttributeError) as exc:
        raise ValueError(f"Unsupported easing: {name}") from exc


def _animation(spec, target, objects):
    action = spec.action
    rate_func = _rate_func(spec.easing)
    kwargs = {"run_time": spec.duration}
    if rate_func is not None:
        kwargs["rate_func"] = rate_func

    if action in (AnimationAction.CREATE.value, AnimationAction.DRAW.value):
        return Create(target, **kwargs)
    if action == AnimationAction.GROW.value:
        return GrowFromCenter(target, **kwargs)
    if action == AnimationAction.FADE_IN.value:
        return FadeIn(target, **kwargs)
    if action == AnimationAction.FADE_OUT.value:
        return FadeOut(target, **kwargs)
    if action == AnimationAction.HIGHLIGHT.value:
        return Indicate(target, **kwargs)
    if action == AnimationAction.MOVE.value:
        shift = np.array(spec.data.get("shift", [0.0, 0.0, 0.0]), dtype=float)
        return ApplyMethod(target.shift, shift, **kwargs)
    if action == AnimationAction.TRANSFORM.value:
        destination = spec.data.get("to")
        if destination not in objects:
            raise ValueError(
                f"transform target '{destination}' is not present in rendered objects"
            )
        return Transform(target, objects[destination], **kwargs)

    raise ValueError(f"Unsupported animation action: {action}")


def apply_animation(scene: Any, spec, objects: dict[str, Any]) -> None:
    """Apply one renderer-neutral animation specification."""
    if spec.delay:
        scene.wait(spec.delay)

    if spec.action == AnimationAction.WAIT.value:
        scene.wait(spec.duration)
        return

    target = objects.get(spec.target)
    if target is None:
        raise ValueError(
            f"Animation target '{spec.target}' is not present in rendered objects"
        )

    scene.play(_animation(spec, target, objects))
