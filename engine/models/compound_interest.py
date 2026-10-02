"""Numerical source of truth for compound-interest visuals."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class CompoundInterest:
    principal: float
    annual_rate: float
    periods: int

    def values(self) -> List[float]:
        return [
            self.principal * (1.0 + self.annual_rate) ** t
            for t in range(self.periods + 1)
        ]

    def value_at(self, t: int) -> float:
        return self.principal * (1.0 + self.annual_rate) ** t

if __name__ == "__main__":
    model = CompoundInterest(1000.0, 0.08, 30)
    print(model.values()[-1])
