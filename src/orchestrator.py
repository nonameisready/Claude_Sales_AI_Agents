"""
Orchestrator
============

Coordinates running one or more specialized agents across one or more
brands. Reuses a single `anthropic.Anthropic` client so every agent in
the same run shares the session's prompt cache (role prompt + brand
context is cached per-brand and per-agent).

Usage
-----
    from src.orchestrator import Orchestrator

    orch = Orchestrator()
    orch.run_brand(
        brand_id="fashion_brand_1",
        topic="minimalist capsule wardrobe",
        agents=["seo_content", "social_media"],
    )
"""
from __future__ import annotations

import os
from typing import Any

import anthropic

from .agents import (
    AnalyticsAgent,
    EmailMarketingAgent,
    SEOContentAgent,
    SocialMediaAgent,
    TechnicalSEOAgent,
)
from .agents.base import BaseAgent
from .utils import get_brand, list_brand_ids, load_config


# Registry: string key -> agent class. Order here is the natural
# "run all" order (content → distribution → infra → retention → measurement).
AGENT_REGISTRY: dict[str, type[BaseAgent]] = {
    "seo_content": SEOContentAgent,
    "social_media": SocialMediaAgent,
    "technical_seo": TechnicalSEOAgent,
    "email_marketing": EmailMarketingAgent,
    "analytics": AnalyticsAgent,
}


class Orchestrator:
    def __init__(
        self,
        config: dict[str, Any] | None = None,
        client: anthropic.Anthropic | None = None,
    ):
        self.config = config or load_config()
        self.client = client or anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

    # ------------------------------------------------------------------ #
    # Single-brand run                                                   #
    # ------------------------------------------------------------------ #
    def run_brand(
        self,
        brand_id: str,
        topic: str | None = None,
        agents: list[str] | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """
        Run the chosen agents for a single brand. Returns a dict keyed by
        agent name with each agent's run() result.
        """
        brand = get_brand(self.config, brand_id)
        agent_keys = agents or list(AGENT_REGISTRY.keys())
        results: dict[str, Any] = {}

        for key in agent_keys:
            cls = AGENT_REGISTRY.get(key)
            if cls is None:
                print(f"[orchestrator] Unknown agent '{key}', skipping.")
                continue

            print(f"[orchestrator] {brand_id} → {key} ...")
            agent = cls(brand=brand, config=self.config, client=self.client)
            try:
                results[key] = agent.run(topic=topic, **extra)
            except Exception as exc:  # noqa: BLE001 — surface, don't crash
                print(f"[orchestrator] {key} failed: {exc}")
                results[key] = {"error": str(exc)}

        return {"brand": brand_id, "topic": topic, "results": results}

    # ------------------------------------------------------------------ #
    # Multi-brand run                                                    #
    # ------------------------------------------------------------------ #
    def run_all_brands(
        self,
        topic: str | None = None,
        agents: list[str] | None = None,
        **extra: Any,
    ) -> list[dict[str, Any]]:
        """Run the chosen agents for every brand in the config."""
        all_results = []
        for brand_id in list_brand_ids(self.config):
            all_results.append(
                self.run_brand(brand_id, topic=topic, agents=agents, **extra)
            )
        return all_results
