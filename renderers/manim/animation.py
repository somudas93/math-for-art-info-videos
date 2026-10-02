"""Manim execution of renderer-neutral animation specs."""
from manim import Create, FadeIn, Animation

def apply_animation(scene, spec, objects):
    target=objects[spec.target]
    action=spec.action
    kwargs={"run_time":spec.duration}
    if action=="create": animation=Create(target)
    elif action=="fade_in": animation=FadeIn(target)
    else: raise ValueError(f"Unsupported animation action: {action}")
    scene.play(animation,**kwargs)
