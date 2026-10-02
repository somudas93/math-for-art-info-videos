"""Renderer-neutral animation and style specifications."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

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

    def add(self, action: str, target: str, duration=1.0, delay=0.0, easing="linear", **data):
        self.animations.append(AnimationSpec(action, target, duration, delay, easing, data))
