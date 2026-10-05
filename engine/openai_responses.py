"""OpenAI Responses API adapter for the semantic compiler.

The adapter is optional: the core engine remains dependency-free. Set
OPENAI_API_KEY and OPENAI_MODEL to enable it.
"""
from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen

from typing import Any


class OpenAIResponsesClient:
    """Minimal stdlib client for structured JSON Responses."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: int = 120,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-6-luna")
        self.timeout = timeout
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")

    def complete_json(
        self,
        system: str,
        user: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "semantic_story",
                    "strict": True,
                    "schema": schema,
                }
            },
        }

        request = Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request, timeout=self.timeout) as response:
            result = json.loads(response.read().decode("utf-8"))

        return _extract_json(result)


def _extract_json(response: dict[str, Any]) -> dict[str, Any]:
    if response.get("error"):
        raise RuntimeError(response["error"])

    output_text = response.get("output_text")
    if output_text:
        return json.loads(output_text)

    for item in response.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return json.loads(content["text"])

    raise RuntimeError("Responses API returned no JSON output")
