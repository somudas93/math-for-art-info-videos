"""Manim renderer driven by Scene IR and Animation IR."""
from manim import MathTex, Scene as ManimScene
from engine.generators.compound_interest_scene import build_scene
from renderers.manim.primitives import render_object, render_timeline
from renderers.manim.animation import apply_animation

class CompoundInterestScene(ManimScene):
    def construct(self):
        scene=build_scene()
        timeline=next(o for o in scene.objects if o.id=="timeline")
        axes=render_timeline(timeline)
        formula=next(o for o in scene.objects if o.id=="formula")
        objects={"timeline":axes,"formula":MathTex(formula.data["text"]).to_edge([0,1,0])}
        for obj in scene.objects:
            if obj.id not in objects:
                rendered=render_object(axes,obj)
                if rendered is not None: objects[obj.id]=rendered
        for spec in scene.animation.animations:
            apply_animation(self,spec,objects)
        self.wait(2)
