"""Map narrative beats to renderer-neutral visual plans."""
from __future__ import annotations

from dataclasses import dataclass, field

from engine.narrative_ir import ShortFormStory


@dataclass(frozen=True)
class VisualPlan:
    beat_id: str
    visual_concept: str
    object_kinds: tuple[str, ...] = ()
    animation_actions: tuple[str, ...] = ()
    duration: float = 0.0
    emphasis: str = ""


_VISUAL_OBJECTS = {
    "kinetic_title": ("label", "group"),
    "overview_network": ("circle", "line", "particles", "label"),
    "exponential_curve": ("timeline", "curve", "particles", "label"),
    "particles_and_flow": ("particles", "line", "circle"),
    "purchasing_power_field": ("curve", "particles", "label"),
    "stochastic_paths": ("timeline", "curve", "particles"),
    "distribution": ("curve", "particles"),
    "coupled_trajectories": ("curve", "line", "particles"),
    "correlated_paths": ("curve", "particles"),
    "simplex": ("line", "particles", "label"),
    "network": ("circle", "line", "particles"),
    "flow_field": ("curve", "particles"),
    "graph": ("circle", "line", "label"),
    "wave": ("curve", "label"),
    "curve_and_slope": ("timeline", "curve", "line"),
    "loss_surface": ("rectangle", "curve", "particles"),
    "highlighted_network": ("circle", "line", "label"),
    "portfolio_network": ("circle", "line", "particles", "label"),
    "converging_paths": ("curve", "particles", "label"),
    "source_card": ("rectangle", "label"),
}


def plan_story(story: ShortFormStory) -> list[VisualPlan]:
    story.validate()
    plans = []
    for beat in story.beats:
        concept = beat.visual_concept or "flow_field"
        plans.append(
            VisualPlan(
                beat_id=beat.id,
                visual_concept=concept,
                object_kinds=_VISUAL_OBJECTS.get(concept, ("curve", "particles", "label")),
                animation_actions=("create", "highlight"),
                duration=beat.duration,
                emphasis=beat.emphasis,
            )
        )
    return plans
