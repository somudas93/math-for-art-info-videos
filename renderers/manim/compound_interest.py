"""Concrete Manim entry point for the compound-interest scene."""
from manim import Scene as ManimScene

from engine.generators.compound_interest_scene import build_scene
from renderers.registry import get


class CompoundInterestScene(ManimScene):
    def construct(self):
        scene = build_scene()
        get("manim").render(scene, self)
