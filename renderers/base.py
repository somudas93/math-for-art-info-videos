"""Base interface for renderer adapters."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from engine.scene_ir import Scene


class Renderer(ABC):
    """Convert a renderer-neutral Scene into a concrete animation."""

    name: str

    @abstractmethod
    def build_objects(self, scene: Scene) -> dict[str, Any]:
        """Build concrete objects keyed by SceneObject id."""

    @abstractmethod
    def render(self, scene: Scene, target: Any) -> None:
        """Execute a Scene against a renderer-specific target."""
