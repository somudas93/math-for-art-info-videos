"""Typed financial-model outputs with explicit provenance."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ModelInput:
    name: str
    value: float
    unit: str
    data_refs: tuple[str, ...] = ()
    source_paragraphs: tuple[int, ...] = ()

@dataclass(frozen=True)
class ModelPoint:
    x: float
    y: float

@dataclass(frozen=True)
class FinancialModelResult:
    id: str
    model_type: str
    inputs: tuple[ModelInput, ...]
    points: tuple[ModelPoint, ...]
    x_label: str
    y_label: str
    y_unit: str
    normalized: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "model_type": self.model_type,
            "inputs": [
                {"name": i.name, "value": i.value, "unit": i.unit,
                 "data_refs": list(i.data_refs),
                 "source_paragraphs": list(i.source_paragraphs)}
                for i in self.inputs
            ],
            "points": [{"x": p.x, "y": p.y} for p in self.points],
            "x_label": self.x_label,
            "y_label": self.y_label,
            "y_unit": self.y_unit,
            "normalized": self.normalized,
            "metadata": self.metadata,
        }
