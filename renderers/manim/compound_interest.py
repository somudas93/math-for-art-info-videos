"""Manim scene driven by Scene IR."""
from manim import Create, FadeIn, MathTex, Scene as ManimScene
from engine.generators.compound_interest_scene import build_scene
from renderers.manim.primitives import render_object, render_timeline

class CompoundInterestScene(ManimScene):
    def construct(self):
        scene=build_scene()
        timeline=next(o for o in scene.objects if o.kind=="timeline")
        axes=render_timeline(timeline)
        self.play(Create(axes))
        equation=MathTex(r"A(t)=P(1+r)^t").to_edge([0,1,0])
        self.play(FadeIn(equation))
        for obj in (render_object(axes,o) for o in scene.objects):
            if obj is not None: self.play(Create(obj),run_time=2)
        self.wait(2)
