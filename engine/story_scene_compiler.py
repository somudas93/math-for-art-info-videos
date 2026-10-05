"""Compile Narrative IR and financial visual models into Scene IR."""
from __future__ import annotations

from engine.animation_ir import AnimationAction
from engine.data_extraction import NumericFact
from engine.financial_visual_compiler import VisualModelBinding, compile_visual_models
from engine.narrative_ir import ShortFormStory, StoryBeat
from engine.scene_ir import Scene
from engine.storyboard_ir import Storyboard
from engine.visual_model import VisualModel
from engine.visual_planner import VisualPlan, plan_story
from engine.vocabulary import Easing, ObjectKind

def build_storyboard(story: ShortFormStory, facts: list[NumericFact] | None = None) -> Storyboard:
    story.validate()
    visual_plans = {p.beat_id: p for p in plan_story(story)}
    bindings = compile_visual_models(story, facts or []) if facts else []
    binding_by_beat = {b.beat_id: b for b in bindings}
    scenes = [
        build_scene(
            beat, visual_plans[beat.id], story.title,
            story.source.url if story.source else "",
            binding_by_beat.get(beat.id),
        )
        for beat in story.beats
    ]
    storyboard = Storyboard(
        name=_slug(story.title),
        duration=story.total_duration(),
        scenes=scenes,
        metadata={
            "story_title": story.title,
            "thesis": story.thesis,
            "target_duration": story.target_duration,
            "source": {
                "url": story.source.url, "title": story.source.title,
                "publisher": story.source.publisher,
            } if story.source else None,
            "disclaimer": story.disclaimer,
            "financial_models": [b.model.to_dict() for b in bindings],
        },
    )
    storyboard.validate()
    return storyboard

def build_scene(
    beat: StoryBeat, visual: VisualPlan, story_title: str,
    source_url: str, binding: VisualModelBinding | None = None,
) -> Scene:
    scene = Scene(
        name=f"beat_{beat.id}", duration=beat.duration,
        metadata={
            "beat_id": beat.id, "purpose": beat.purpose,
            "narration": beat.narration, "claim_ids": list(beat.claims),
            "visual_concept": visual.visual_concept, "emphasis": beat.emphasis,
            "source_url": source_url, "story_title": story_title,
        },
    )
    if binding:
        vm = VisualModel.from_financial_model(binding.model)
        scene.metadata["financial_model_id"] = binding.model.id
        scene.metadata["model_provenance"] = vm.provenance
    if beat.purpose == "source":
        _add_source_card(scene, source_url)
        return scene

    scene.add(ObjectKind.LABEL, "headline", text=_headline(beat.narration),
              position=[0, 2.6, 0], role="headline")

    if binding:
        vm = VisualModel.from_financial_model(binding.model)
        scene.add(ObjectKind.CURVE, "visual", **vm.data,
                  visual_concept=visual.visual_concept, status="model_backed")
    elif visual.visual_concept == "exponential_curve":
        scene.add(ObjectKind.CURVE, "visual", points=[],
                  visual_concept=visual.visual_concept, status="awaiting_model_data")
    elif "timeline" in visual.object_kinds:
        scene.add(ObjectKind.TIMELINE, "visual", start=0,
                  end=max(1, int(beat.duration)), y_min=0, y_max=1, y_step=0.2,
                  visual_concept=visual.visual_concept, status="awaiting_model_data")
    else:
        scene.add(ObjectKind.GROUP, "visual", children=[],
                  visual_concept=visual.visual_concept,
                  object_kinds=list(visual.object_kinds),
                  status="semantic_visual_placeholder")

    scene.animation.add(AnimationAction.FADE_IN, "headline",
                          duration=min(0.5, beat.duration / 4),
                          easing=Easing.EASE_OUT)
    scene.animation.add(
        AnimationAction.DRAW if visual.visual_concept in {"exponential_curve", "curve_and_slope"} else AnimationAction.CREATE,
        "visual", duration=min(1.0, max(0.2, beat.duration / 3)),
        delay=min(0.1, beat.duration / 20), easing=Easing.SMOOTH,
    )
    return scene

def _add_source_card(scene: Scene, source_url: str) -> None:
    scene.add(ObjectKind.RECTANGLE, "source_card", width=10, height=4, role="source_card")
    scene.add(ObjectKind.LABEL, "source_label", text=source_url or "Source",
              position=[0, 0, 0], role="source")
    scene.animation.add(AnimationAction.FADE_IN, "source_card", duration=0.4)
    scene.animation.add(AnimationAction.FADE_IN, "source_label", duration=0.4)

def _headline(text: str, max_words: int = 9) -> str:
    words = text.replace("—", " ").split()
    headline = " ".join(words[:max_words])
    return headline + "…" if len(words) > max_words else headline

def _slug(title: str) -> str:
    value = "-".join(title.lower().split())
    return "".join(c for c in value if c.isalnum() or c == "-")[:80] or "short-form-story"
