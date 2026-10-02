"""Export the compound-interest Scene IR for Motion Canvas."""
from pathlib import Path

from engine.generators.compound_interest_scene import build_scene
from engine.serialization import scene_to_json

OUTPUT = Path(__file__).resolve().parent.parent / "renderers" / "motion_canvas" / "data" / "compound_interest.json"

if __name__ == "__main__":
    OUTPUT.write_text(scene_to_json(build_scene()) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")
