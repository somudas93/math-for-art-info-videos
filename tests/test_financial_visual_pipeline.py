import unittest

from engine.data_extraction import extract_numeric_facts
from engine.financial_models import compound_growth, purchasing_power
from engine.financial_visual_compiler import compile_visual_models
from engine.narrative_ir import Claim, ShortFormStory, SourceReference, StoryBeat


class FinancialVisualPipelineTests(unittest.TestCase):
    def test_compound_growth_is_deterministic(self):
        model = compound_growth(0.08, 10)
        self.assertEqual(len(model.points), 11)
        self.assertAlmostEqual(model.points[-1].y, 1.08 ** 10)

    def test_purchasing_power_is_inverse_growth(self):
        model = purchasing_power(0.05, 10)
        self.assertEqual(len(model.points), 11)
        self.assertLess(model.points[-1].y, model.points[0].y)

    def test_visual_compiler_requires_rate_and_horizon(self):
        paragraphs = ["Inflation is 5% over 10 years."]
        facts = extract_numeric_facts(paragraphs, "https://example.com")
        rate = next(f for f in facts if f.kind == "percent")
        duration = next(f for f in facts if f.kind == "duration")
        story = ShortFormStory(
            title="Inflation",
            thesis="Inflation reduces purchasing power.",
            target_duration=10,
            source=SourceReference("https://example.com"),
            claims=[
                Claim(
                    id="C1",
                    text="Inflation reduces purchasing power.",
                    data_refs=[rate.id, duration.id],
                    source_paragraph=0,
                )
            ],
            beats=[
                StoryBeat(
                    id="B1",
                    purpose="idea",
                    narration="Inflation reduces purchasing power.",
                    duration=5,
                    claims=["C1"],
                    visual_concept="purchasing_power_field",
                )
            ],
        )
        bindings = compile_visual_models(story, facts)
        self.assertEqual(len(bindings), 1)
        self.assertEqual(bindings[0].model.model_type, "purchasing_power")
        self.assertEqual(bindings[0].model.inputs[0].data_refs, (rate.id,))
        self.assertEqual(bindings[0].model.inputs[1].data_refs, (duration.id,))


if __name__ == "__main__":
    unittest.main()
