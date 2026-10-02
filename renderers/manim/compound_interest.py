"""Manim renderer for the first Scene IR composition."""
from manim import Axes, Create, Dot, FadeIn, MathTex, Scene as ManimScene, ValueTracker, VGroup
from engine.generators.compound_interest_scene import build_scene

class CompoundInterestScene(ManimScene):
    def construct(self):
        scene = build_scene()
        curve = next(o for o in scene.objects if o.kind == "curve")
        timeline = next(o for o in scene.objects if o.kind == "timeline")

        points = curve.data["points"]
        values = [y for _, y in points]
        max_value = max(values)

        axes = Axes(
            x_range=[timeline.data["start"], timeline.data["end"], 5],
            y_range=[0, max_value * 1.1, max_value / 4],
            x_length=10,
            y_length=5,
        )

        graph = axes.plot(lambda t: values[min(int(round(t)), len(values)-1)],
                          x_range=[0, timeline.data["end"]])
        title = MathTex(r"A(t)=P(1+r)^t").to_edge([0, 1, 0])
        dots = VGroup(*[Dot(axes.c2p(t, value), radius=0.045) for t, value in points])

        self.play(Create(axes), FadeIn(title))
        self.play(Create(graph), FadeIn(dots), run_time=3)
        self.wait(2)
