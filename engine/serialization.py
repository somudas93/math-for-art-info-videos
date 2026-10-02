"""JSON serialization for renderer-neutral Scene IR.

The serialized form is the bridge between Python scene generation and
non-Python renderers such as Motion Canvas.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from enum import Enum
from typing import Any

from engine.scene_ir import Scene


def _json_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def scene_to_dict(scene: Scene) -> dict[str, Any]:
    """Convert a Scene into renderer-neutral JSON-compatible data."""
    return _json_value(asdict(scene))


def scene_to_json(scene: Scene, indent: int = 2) -> str:
    """Serialize a Scene for consumption by another renderer."""
    return json.dumps(scene_to_dict(scene), indent=indent)
