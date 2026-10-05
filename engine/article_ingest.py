"""Dependency-light article ingestion for the narrative compiler."""
from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import re


@dataclass
class ArticleDocument:
    url: str
    title: str = ""
    publisher: str = ""
    paragraphs: list[str] = field(default_factory=list)
    headings: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n\n".join(self.paragraphs)


class _ArticleParser(HTMLParser):
    BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "li"}
    SKIP_TAGS = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self.current: list[str] = []
        self.in_skip = 0
        self.blocks: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self.SKIP_TAGS:
            self.in_skip += 1
        if tag in self.BLOCK_TAGS and not self.in_skip:
            self.current = []

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self.in_skip:
            self.in_skip -= 1
        if tag in self.BLOCK_TAGS and not self.in_skip:
            text = re.sub(r"\s+", " ", " ".join(self.current)).strip()
            if text:
                self.blocks.append((tag, text))
            self.current = []

    def handle_data(self, data: str) -> None:
        if not self.in_skip and self.current is not None:
            self.current.append(data)


def fetch_article(url: str, timeout: int = 20) -> ArticleDocument:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("article URL must use http or https")

    request = Request(url, headers={"User-Agent": "math-for-art-info-videos/1.0"})
    with urlopen(request, timeout=timeout) as response:
        html = response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")
        final_url = response.geturl()

    parser = _ArticleParser()
    parser.feed(html)

    title = next((text for tag, text in parser.blocks if tag == "h1"), "")
    headings = [text for tag, text in parser.blocks if tag in {"h1", "h2", "h3"}]
    paragraphs = [
        text for tag, text in parser.blocks
        if tag == "p" and 8 <= len(text.split()) <= 120
    ]

    return ArticleDocument(
        url=final_url,
        title=title,
        publisher=parsed.netloc,
        paragraphs=_dedupe(paragraphs),
        headings=_dedupe(headings),
    )


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
