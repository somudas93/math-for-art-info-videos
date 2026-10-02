"""Compose compound interest into a renderer-neutral scene and animation plan."""
from engine.animation_ir import AnimationAction
from engine.models.compound_interest import CompoundInterest
from engine.scene_ir import Scene
from engine.vocabulary import Easing, ObjectKind


def build_scene(principal=1000.0, annual_rate=0.08, periods=30) -> Scene:
    model = CompoundInterest(principal, annual_rate, periods)
    values = model.values()

    y_max = max(values) * 1.10
    y_step = max(principal, y_max / 5.0)

    scene = Scene("compound_interest", duration=10.0)
    scene.add(
        ObjectKind.TIMELINE,
        "timeline",
        start=0,
        end=periods,
        y_min=0,
        y_max=y_max,
        y_step=y_step,
    )
    scene.add(
        ObjectKind.CURVE,
        "growth_curve",
        points=[(t, value) for t, value in enumerate(values)],
    )
    scene.add(
        ObjectKind.PARTICLES,
        "money_particles",
        count=len(values),
        values=values,
    )
    scene.add(
        ObjectKind.LABEL,
        "formula",
        text=r"A(t)=P(1+r)^t",
        position=[0, 3, 0],
    )

    scene.animation.add(
        AnimationAction.CREATE,
        "timeline",
        duration=1.5,
        easing=Easing.SMOOTH,
    )
    scene.animation.add(
        AnimationAction.FADE_IN,
        "formula",
        duration=0.8,
        delay=0.2,
    )
    scene.animation.add(
        AnimationAction.DRAW,
        "growth_curve",
        duration=3.0,
        easing=Easing.SMOOTH,
    )
    scene.animation.add(
        AnimationAction.GROW,
        "money_particles",
        duration=2.0,
    )
    return scene
