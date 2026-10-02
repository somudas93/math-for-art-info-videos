"""Generic Manim renderer for Scene IR + Animation IR."""
from __future__ import annotations

from typing import Any

from engine.scene_ir import Scene
from renderers.base import Renderer
from renderers.manim.animation import apply_animation
from renderers.manim.primitives import render_object


class ManimRenderer(Renderer):
    name = "manim"

    def build_objects(self, scene: Scene) -> dict[str, Any]:
        objects: dict[str, Any] = {}

        timeline = next((obj for obj in scene.objects if obj.kind == "timeline"), None)
        axes = render_object(None, timeline) if timeline else None

        if timeline is not None and axes is not None:
            objects[timeline.id] = axes

        for obj in scene.objects:
            if obj.id in objects:
                continue

            rendered = render_object(axes, obj)
            if rendered is not None:
                objects[obj.id] = rendered

        return objects

    def render(self, scene: Scene, target: Any) -> None:
        objects = self.build_objects(scene)

        for spec in scene.animation.animations:
            apply_animation(target, spec, objects)

        elapsed = sum(spec.duration + spec.delay for spec in scene.animation.animations)
        remaining = max(0.0, scene.duration - elapsed)
        if remaining:
            target.wait(remaining)


def renderer() -> ManimRenderer:
    return ManimRenderer()
