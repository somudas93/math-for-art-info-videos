"""Compile an article into a semantic, source-grounded video plan."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from engine.article_ingest import fetch_article
from engine.data_extraction import extract_numeric_facts
from engine.narrative_ir import SourceReference
from engine.openai_responses import OpenAIResponsesClient
from engine.semantic_compiler import SemanticCompiler
from engine.serialization import storyboard_to_dict
from engine.story_scene_compiler import build_storyboard


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile an article URL with an LLM into a validated storyboard."
    )
    parser.add_argument("url")
    parser.add_argument("-o", "--output", type=Path, default=Path("semantic_storyboard.json"))
    parser.add_argument("--duration", type=float, default=90.0)
    args = parser.parse_args()

    article = fetch_article(args.url)
    facts = extract_numeric_facts(article.paragraphs, article.url)
    source = SourceReference(
        url=article.url,
        title=article.title,
        publisher=article.publisher,
    )

    compiler = SemanticCompiler(OpenAIResponsesClient())
    story = compiler.compile(
        title=article.title,
        paragraphs=article.paragraphs,
        facts=facts,
        source=source,
        target_duration=args.duration,
    )
    storyboard = build_storyboard(story)

    payload = {
        "story": asdict(story),
        "numeric_facts": [asdict(fact) for fact in facts],
        "storyboard": storyboard_to_dict(storyboard),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {args.output}")
    print(f"Title: {story.title}")
    print(f"Thesis: {story.thesis}")
    print(f"Duration: {story.total_duration():.1f}s")
    print(f"Numeric facts: {len(facts)}")
    print(f"Claims: {len(story.claims)}")
    print(f"Beats / scenes: {len(story.beats)}")


if __name__ == "__main__":
    main()
