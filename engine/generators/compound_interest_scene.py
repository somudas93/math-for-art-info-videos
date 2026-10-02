"""Compose compound interest into a renderer-neutral scene and animation plan."""
from engine.models.compound_interest import CompoundInterest
from engine.scene_ir import Scene

def build_scene(principal=1000.0, annual_rate=0.08, periods=30) -> Scene:
    model=CompoundInterest(principal,annual_rate,periods)
    values=model.values()
    scene=Scene("compound_interest",duration=10.0)
    scene.add("timeline","timeline",start=0,end=periods)
    scene.add("curve","growth_curve",points=[(t,v) for t,v in enumerate(values)])
    scene.add("particles","money_particles",count=len(values),values=values)
    scene.add("label","formula",text=r"A(t)=P(1+r)^t")
    scene.animation.add("create","timeline",duration=1.5,easing="smooth")
    scene.animation.add("fade_in","formula",duration=0.8,delay=0.2)
    scene.animation.add("create","growth_curve",duration=3.0,easing="smooth")
    scene.animation.add("create","money_particles",duration=2.0)
    return scene
