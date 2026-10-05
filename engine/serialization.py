"""JSON serialization for renderer-neutral Scene and Storyboard IR."""
from __future__ import annotations
import json
from dataclasses import asdict
from enum import Enum
from typing import Any
from engine.scene_ir import Scene
from engine.storyboard_ir import Storyboard

def _json_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(v) for v in value]
    return value

def scene_to_dict(scene: Scene) -> dict[str, Any]:
    return _json_value(asdict(scene))

def scene_to_json(scene: Scene, indent: int = 2) -> str:
    return json.dumps(scene_to_dict(scene), indent=indent)

def storyboard_to_dict(storyboard: Storyboard) -> dict[str, Any]:
    return {
        "name": storyboard.name,
        "duration": storyboard.duration,
        "metadata": _json_value(storyboard.metadata),
        "scenes": [scene_to_dict(scene) for scene in storyboard.scenes],
    }

def storyboard_to_json(storyboard: Storyboard, indent: int = 2) -> str:
    return json.dumps(storyboard_to_dict(storyboard), indent=indent)
