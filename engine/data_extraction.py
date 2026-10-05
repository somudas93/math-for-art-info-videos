"""Structured factual data extracted from article text."""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class NumericFact:
    id: str
    value: float
    raw_value: str
    unit: str
    context: str
    paragraph_index: int
    source_url: str = ""
    kind: str = "number"


_CURRENCY = {"$": "USD", "€": "EUR", "£": "GBP", "₹": "INR", "¥": "JPY"}


def extract_numeric_facts(
    paragraphs: list[str],
    source_url: str = "",
) -> list[NumericFact]:
    """Extract explicit numeric facts without interpreting their meaning."""
    facts: list[NumericFact] = []
    counter = 1

    patterns = [
        (r"(?P<currency>[$€£₹¥])\s*(?P<num>\d[\d,]*(?:\.\d+)?)\s*(?P<scale>billion|million|trillion|bn|mn|tn)?", "currency"),
        (r"(?P<num>\d+(?:\.\d+)?)\s*%", "percent"),
        (r"(?P<num>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>basis points?|bps)", "basis_points"),
        (r"(?P<num>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>years?|months?|quarters?)", "duration"),
        (r"\b(?P<num>20\d{2})\b", "year"),
        (r"\b(?P<num>\d[\d,]*(?:\.\d+)?)\b", "number"),
    ]

    for paragraph_index, paragraph in enumerate(paragraphs):
        seen_spans: set[tuple[int, int]] = set()
        for pattern, kind in patterns:
            for match in re.finditer(pattern, paragraph, flags=re.IGNORECASE):
                if any(
                    start < match.end() and match.start() < end
                    for start, end in seen_spans
                ):
                    continue
                seen_spans.add(match.span())

                raw = match.group(0)
                value = _parse_value(match, kind)
                if value is None:
                    continue

                facts.append(
                    NumericFact(
                        id=f"D{counter}",
                        value=value,
                        raw_value=raw,
                        unit=_unit(match, kind),
                        context=_context(paragraph, match.start(), match.end()),
                        paragraph_index=paragraph_index,
                        source_url=source_url,
                        kind=kind,
                    )
                )
                counter += 1

    return facts


def _parse_value(match: re.Match[str], kind: str) -> float | None:
    raw = match.group("num").replace(",", "")
    try:
        value = float(raw)
    except ValueError:
        return None

    scale = (match.groupdict().get("scale") or "").lower()
    multiplier = {
        "million": 1_000_000,
        "mn": 1_000_000,
        "billion": 1_000_000_000,
        "bn": 1_000_000_000,
        "trillion": 1_000_000_000_000,
        "tn": 1_000_000_000_000,
    }.get(scale, 1.0)
    return value * multiplier


def _unit(match: re.Match[str], kind: str) -> str:
    if kind == "currency":
        return _CURRENCY[match.group("currency")] + (
            f"_{match.group('scale').lower()}" if match.group("scale") else ""
        )
    if kind == "percent":
        return "%"
    return (match.groupdict().get("unit") or kind).lower()


def _context(text: str, start: int, end: int, window: int = 90) -> str:
    left = max(0, start - window)
    right = min(len(text), end + window)
    return " ".join(text[left:right].split())
