"""Compile an article directly into a renderer-neutral storyboard JSON."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from engine.article_ingest import fetch_article
from engine.narrative_compiler import compile_story
from engine.serialization import storyboard_to_dict
from engine.story_scene_compiler import build_storyboard


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile an article URL into Narrative IR + Scene IR."
    )
    parser.add_argument("url")
    parser.add_argument("-o", "--output", type=Path, default=Path("storyboard.json"))
    parser.add_argument("--duration", type=float, default=90.0)
    parser.add_argument("--claims", type=int, default=5)
    args = parser.parse_args()

    article = fetch_article(args.url)
    story = compile_story(article, args.duration, args.claims)
    storyboard = build_storyboard(story)

    payload = {
        "story": asdict(story),
        "storyboard": storyboard_to_dict(storyboard),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {args.output}")
    print(f"Title: {story.title}")
    print(f"Thesis: {story.thesis}")
    print(f"Duration: {storyboard.total_duration():.1f}s")
    print(f"Claims: {len(story.claims)}")
    print(f"Beats / scenes: {len(story.beats)}")


if __name__ == "__main__":
    main()
