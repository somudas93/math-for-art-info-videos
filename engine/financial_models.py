"""Deterministic financial models used by visual compilation."""
from __future__ import annotations
from engine.financial_model_ir import ModelInput, ModelPoint, FinancialModelResult

def compound_growth(rate: float, periods: int, initial: float = 1.0,
                    *, rate_ref: str | None = None,
                    period_ref: str | None = None) -> FinancialModelResult:
    if periods < 1:
        raise ValueError("periods must be positive")
    if initial <= 0:
        raise ValueError("initial must be positive")
    points = tuple(ModelPoint(float(t), initial * (1.0 + rate) ** t)
                    for t in range(periods + 1))
    inputs = (
        ModelInput("annual_rate", rate, "fraction",
                   (rate_ref,) if rate_ref else ()),
        ModelInput("periods", float(periods), "years",
                   (period_ref,) if period_ref else ()),
    )
    return FinancialModelResult(
        id="compound_growth", model_type="compound_growth", inputs=inputs,
        points=points, x_label="Time", y_label="Relative value",
        y_unit="normalized", normalized=initial == 1.0,
        metadata={"initial": initial, "baseline_note": "1.0 = normalized baseline"},
    )

def purchasing_power(inflation_rate: float, periods: int, initial: float = 1.0,
                     *, rate_ref: str | None = None,
                     period_ref: str | None = None) -> FinancialModelResult:
    if periods < 1:
        raise ValueError("periods must be positive")
    if initial <= 0:
        raise ValueError("initial must be positive")
    if inflation_rate <= -1:
        raise ValueError("inflation_rate must be greater than -100%")
    points = tuple(ModelPoint(float(t), initial / (1.0 + inflation_rate) ** t)
                    for t in range(periods + 1))
    inputs = (
        ModelInput("inflation_rate", inflation_rate, "fraction",
                   (rate_ref,) if rate_ref else ()),
        ModelInput("periods", float(periods), "years",
                   (period_ref,) if period_ref else ()),
    )
    return FinancialModelResult(
        id="purchasing_power", model_type="purchasing_power", inputs=inputs,
        points=points, x_label="Time", y_label="Purchasing power",
        y_unit="normalized", normalized=initial == 1.0,
        metadata={"initial": initial, "baseline_note": "1.0 = normalized baseline"},
    )
