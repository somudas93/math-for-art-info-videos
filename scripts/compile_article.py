"""CLI for compiling an article URL into narrative JSON."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from engine.article_ingest import fetch_article
from engine.narrative_compiler import compile_story


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile an article into a short-form story.")
    parser.add_argument("url")
    parser.add_argument("-o", "--output", type=Path, default=Path("story.json"))
    parser.add_argument("--duration", type=float, default=90.0)
    parser.add_argument("--claims", type=int, default=5)
    args = parser.parse_args()

    article = fetch_article(args.url)
    story = compile_story(article, args.duration, args.claims)
    args.output.write_text(
        json.dumps(asdict(story), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {args.output}")
    print(f"Title: {story.title}")
    print(f"Duration: {story.total_duration():.1f}s")
    print(f"Claims: {len(story.claims)}")
    print(f"Beats: {len(story.beats)}")


if __name__ == "__main__":
    main()
