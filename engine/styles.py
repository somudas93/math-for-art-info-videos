"""Renderer-neutral style defaults for financial scenes."""
from engine.scene_ir import Scene
from engine.style_ir import StyleSpec


def apply_finance_style(scene: Scene) -> Scene:
    scene.animation.style = StyleSpec(
        name="finance",
        font_size=32,
        stroke_width=3,
        opacity=1.0,
        fill_opacity=1.0,
    )
    return scene
