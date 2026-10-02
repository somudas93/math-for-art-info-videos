"""Renderer-independent scene description."""
from dataclasses import dataclass, field
from typing import Any, Dict, List
from engine.animation_ir import AnimationPlan

@dataclass
class SceneObject:
    id: str
    kind: str
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Scene:
    name: str
    duration: float = 8.0
    objects: List[SceneObject] = field(default_factory=list)
    animation: AnimationPlan = field(default_factory=AnimationPlan)

    def add(self, kind: str, object_id: str | None = None, **data) -> SceneObject:
        object_id = object_id or f"{kind}_{len(self.objects)}"
        obj = SceneObject(object_id, kind, data)
        self.objects.append(obj)
        return obj
