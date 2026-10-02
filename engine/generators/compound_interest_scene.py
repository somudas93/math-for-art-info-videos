"""Compose the compound-interest model into a visual scene."""
from engine.models.compound_interest import CompoundInterest
from engine.scene_ir import Scene

def build_scene(principal=1000.0, annual_rate=0.08, periods=30) -> Scene:
    model = CompoundInterest(principal, annual_rate, periods)
    values = model.values()
    scene = Scene("compound_interest", duration=10.0)
    scene.add("timeline", start=0, end=periods)
    scene.add("curve", points=[(t, value) for t, value in enumerate(values)])
    scene.add("particles", count=periods + 1, values=values)
    scene.add("label", text=f"P = {principal:g}, r = {annual_rate:.1%}")
    return scene

if __name__ == "__main__":
    print(build_scene())
