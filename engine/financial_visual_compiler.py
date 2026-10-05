"""Compile grounded claims into deterministic financial visual models."""
from __future__ import annotations
from dataclasses import dataclass
from engine.data_extraction import NumericFact
from engine.financial_models import compound_growth, purchasing_power
from engine.financial_model_ir import FinancialModelResult
from engine.narrative_ir import Claim, ShortFormStory

@dataclass(frozen=True)
class VisualModelBinding:
    beat_id: str
    claim_ids: tuple[str, ...]
    model: FinancialModelResult
    visual_concept: str

def compile_visual_models(story: ShortFormStory, facts: list[NumericFact]) -> list[VisualModelBinding]:
    story.validate()
    facts_by_id = {fact.id: fact for fact in facts}
    claims_by_id = {claim.id: claim for claim in story.claims}
    bindings = []
    for beat in story.beats:
        claims = [claims_by_id[cid] for cid in beat.claims]
        model = _model_for_claims(claims, facts_by_id)
        if model is not None:
            bindings.append(VisualModelBinding(
                beat_id=beat.id,
                claim_ids=tuple(c.id for c in claims),
                model=model,
                visual_concept=beat.visual_concept,
            ))
    return bindings

def _model_for_claims(claims: list[Claim], facts: dict[str, NumericFact]) -> FinancialModelResult | None:
    refs = [ref for claim in claims for ref in claim.data_refs]
    if not refs:
        return None
    source_facts = [facts[ref] for ref in refs if ref in facts]
    percentages = [f for f in source_facts if f.kind == "percent"]
    durations = [f for f in source_facts if f.kind == "duration" and f.unit.startswith("year")]
    if not percentages or not durations:
        return None
    rate = percentages[0].value / 100.0
    periods = max(1, int(durations[0].value))
    text = " ".join(c.text.lower() for c in claims)
    if any(w in text for w in ("inflation", "purchasing power", "price growth", "prices")):
        return purchasing_power(rate, periods, rate_ref=percentages[0].id,
                                period_ref=durations[0].id)
    if any(w in text for w in ("growth", "compound", "compounding", "return")):
        return compound_growth(rate, periods, rate_ref=percentages[0].id,
                               period_ref=durations[0].id)
    return None
