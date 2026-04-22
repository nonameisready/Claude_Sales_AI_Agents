"""
BaseAgent — shared OpenAI API plumbing for every specialized agent.

Design notes
------------
* Uses the official OpenAI Python SDK (openai>=1.0.0) directly — no
  LangChain or wrappers.
* The role prompt + brand context are combined into a single system message
  so the model has full brand awareness on every call.
* Streaming is on by default to avoid HTTP timeouts on long outputs
  (full blog posts, 30-day social calendars).
* Default model is gpt-4o — swap to gpt-4o-mini in config/brands.yaml
  for ~85% lower cost at somewhat lower output quality.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import openai

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
        client: openai.OpenAI | None = None,
    ):
        self.brand = brand
        self.config = config
        self.client = client or openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.model = config.get("global", {}).get("model", "gpt-4o")
        self.max_tokens = config.get("global", {}).get("max_tokens", 16000)

    # ------------------------------------------------------------------ #
    # Core generation                                                    #
    # ------------------------------------------------------------------ #
    def generate(self, task: str) -> str:
        """
        Run one request against the OpenAI Chat Completions API and return
        the full text response.

        The system message combines:
          1. The agent's role prompt (methodology and output format)
          2. The brand context (YAML-dumped brand config)

        Streaming is used to handle long outputs without hitting timeouts.
        """
        brand_ctx = format_brand_context(self.brand)

        system_content = (
            self.role_prompt.strip()
            + "\n\n"
            + "## Brand Context\n"
            + "You are working on behalf of the following brand. "
            + "Every recommendation must be on-voice and on-strategy "
            + "for this brand specifically.\n\n"
            + f"```yaml\n{brand_ctx}\n```"
        )

        stream = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": task},
            ],
            stream=True,
        )

        parts: list[str] = []
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                parts.append(delta.content)

        return "".join(parts).strip()

    # ------------------------------------------------------------------ #
    # Output helpers                                                     #
    # ------------------------------------------------------------------ #
    def save(self, filename: str, content: str) -> Path:
        """Persist content to <output_dir>/<brand>/<agent>/<date>_<filename>."""
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
