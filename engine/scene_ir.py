"""Renderer-independent scene description."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

from engine.animation_ir import AnimationPlan
from engine.vocabulary import ObjectKind


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
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add(
        self,
        kind: str | ObjectKind,
        object_id: str | None = None,
        **data,
    ) -> SceneObject:
        kind = kind.value if isinstance(kind, ObjectKind) else kind
        object_id = object_id or f"{kind}_{len(self.objects)}"
        obj = SceneObject(object_id, kind, data)
        self.objects.append(obj)
        return obj
