"""Renderer-independent scene description."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class SceneObject:
    kind: str
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Scene:
    name: str
    duration: float = 8.0
    objects: List[SceneObject] = field(default_factory=list)

    def add(self, kind: str, **data) -> SceneObject:
        obj = SceneObject(kind, data)
        self.objects.append(obj)
        return obj
