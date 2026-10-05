"""Renderer-neutral visual data derived from financial models."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from engine.financial_model_ir import FinancialModelResult

@dataclass(frozen=True)
class VisualModel:
    id: str
    kind: str
    data: dict[str, Any]
    source_model_id: str
    provenance: dict[str, Any]

    @classmethod
    def from_financial_model(cls, model: FinancialModelResult, *, kind: str = "curve") -> "VisualModel":
        return cls(
            id=model.id,
            kind=kind,
            data={
                "points": [[p.x, p.y, 0.0] for p in model.points],
                "x_label": model.x_label,
                "y_label": model.y_label,
                "y_unit": model.y_unit,
                "normalized": model.normalized,
                "model_type": model.model_type,
            },
            source_model_id=model.id,
            provenance={
                "model_inputs": [i.__dict__ for i in model.inputs],
                "metadata": model.metadata,
            },
        )
