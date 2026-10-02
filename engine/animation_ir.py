"""Renderer-neutral animation and style specifications."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

from engine.vocabulary import AnimationAction, Easing


@dataclass(frozen=True)
class AnimationSpec:
    action: str
    target: str
    duration: float = 1.0
    delay: float = 0.0
    easing: str = "linear"
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StyleSpec:
    name: str = "default"
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnimationPlan:
    animations: List[AnimationSpec] = field(default_factory=list)
    style: StyleSpec = field(default_factory=StyleSpec)

    def add(
        self,
        action: str | AnimationAction,
        target: str,
        duration: float = 1.0,
        delay: float = 0.0,
        easing: str | Easing = Easing.LINEAR,
        **data,
    ) -> AnimationSpec:
        action = action.value if isinstance(action, AnimationAction) else action
        easing = easing.value if isinstance(easing, Easing) else easing

        if duration < 0:
            raise ValueError("duration must be non-negative")
        if delay < 0:
            raise ValueError("delay must be non-negative")

        spec = AnimationSpec(action, target, duration, delay, easing, data)
        self.animations.append(spec)
        return spec
