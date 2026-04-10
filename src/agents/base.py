"""
BaseAgent — shared Claude API plumbing for every specialized agent.

Design notes
------------
* We use Anthropic's Python SDK directly (no wrappers, no LangChain).
* Prompt caching is enabled: the agent's role system prompt + brand context
  are cached for 5 minutes, so running multiple tasks for the same brand in
  the same session reads the cached prefix (~0.1x cost) instead of paying
  full input-token price every time.
* Opus 4.6 with adaptive thinking is the default — it spends more compute
  on complex jobs (keyword clusters) and less on simple ones (a meta tag).
* Streaming is on by default to stay under SDK HTTP timeouts on long
  outputs like full blog posts.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import anthropic

from ..utils import format_brand_context, output_path, slugify, write_output


class BaseAgent(ABC):
    """
    Subclasses must set:
        name          — short agent identifier, used for output folders
        role_prompt   — the long, stable system prompt describing the
                        agent's job, methodology, and output format
    """

    name: str = "base"
    role_prompt: str = ""

    def __init__(
        self,
        brand: dict[str, Any],
        config: dict[str, Any],
        client: anthropic.Anthropic | None = None,
    ):
        self.brand = brand
        self.config = config
        self.client = client or anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )
        self.model = config.get("global", {}).get("model", "claude-opus-4-6")
        self.max_tokens = config.get("global", {}).get("max_tokens", 16000)

    # ------------------------------------------------------------------ #
    # Core generation                                                    #
    # ------------------------------------------------------------------ #
    def generate(self, task: str) -> str:
        """
        Run one request against Claude and return the text response.

        The `system` parameter is a list of text blocks so we can mark the
        stable prefix (role + brand) as cacheable. See shared/prompt-caching.md.
        """
        brand_ctx = format_brand_context(self.brand)

        system_blocks = [
            {
                "type": "text",
                "text": self.role_prompt.strip(),
            },
            {
                "type": "text",
                "text": (
                    "## Brand Context\n"
                    "You are working on behalf of the following brand. "
                    "Every recommendation must be on-voice and on-strategy "
                    "for this brand specifically.\n\n"
                    f"```yaml\n{brand_ctx}\n```"
                ),
                # Everything up to here is stable for the whole session →
                # cache it. Task varies per call and comes last.
                "cache_control": {"type": "ephemeral"},
            },
        ]

        # Stream to avoid SDK HTTP timeouts on long outputs (full blog posts,
        # 30-day social calendars).
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            thinking={"type": "adaptive"},
            system=system_blocks,
            messages=[{"role": "user", "content": task}],
        ) as stream:
            # Drain the stream — we don't need per-token output here.
            for _ in stream.text_stream:
                pass
            final = stream.get_final_message()

        # Extract the first text block (thinking blocks precede it).
        text_parts = [b.text for b in final.content if b.type == "text"]
        return "\n".join(text_parts).strip()

    # ------------------------------------------------------------------ #
    # Output helpers                                                     #
    # ------------------------------------------------------------------ #
    def save(self, filename: str, content: str) -> Path:
        """Persist content to outputs/<brand>/<agent>/<date>_<filename>."""
        path = output_path(
            self.config,
            self.brand["id"],
            self.name,
            slugify(filename) + ".md",
        )
        return write_output(path, content)

    # ------------------------------------------------------------------ #
    # Subclass contract                                                  #
    # ------------------------------------------------------------------ #
    @abstractmethod
    def run(self, **kwargs: Any) -> dict[str, Any]:
        """
        Execute the agent's primary task(s).

        Returns a dict summarizing what was produced, typically:
            {"files": [path, ...], "summary": "short description"}
        """
        raise NotImplementedError
