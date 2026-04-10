"""
CLI entry point.

Examples
--------
    # Run every agent for every brand with a shared topic
    python -m src.main --topic "minimalist capsule wardrobe"

    # Run a single agent for a single brand
    python -m src.main --brand fashion_brand_1 --agents seo_content \
        --topic "organic cotton basics"

    # Run two agents for the furniture brand
    python -m src.main --brand furniture_brand \
        --agents seo_content email_marketing \
        --topic "small apartment living room setup"

    # List configured brands
    python -m src.main --list-brands
"""
from __future__ import annotations

import argparse
import json
import sys

from dotenv import load_dotenv

from .orchestrator import AGENT_REGISTRY, Orchestrator
from .utils import list_brand_ids, load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="claude-sales-ai-agents",
        description=(
            "Run specialized AI sales agents (SEO / social / technical SEO / "
            "email / analytics) across your brands using Claude Opus 4.6."
        ),
    )
    parser.add_argument(
        "--brand",
        help="Brand id to run (see --list-brands). Omit to run all brands.",
    )
    parser.add_argument(
        "--agents",
        nargs="+",
        choices=list(AGENT_REGISTRY.keys()),
        help="Which agents to run. Defaults to all five.",
    )
    parser.add_argument(
        "--topic",
        help=(
            "The topic / theme passed to each agent. Most agents require "
            "this — e.g. 'minimalist capsule wardrobe' or "
            "'small apartment living room'."
        ),
    )
    parser.add_argument(
        "--list-brands",
        action="store_true",
        help="Print the configured brand ids and exit.",
    )
    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="Print the available agents and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_agents:
        for name in AGENT_REGISTRY:
            print(name)
        return 0

    config = load_config()

    if args.list_brands:
        for brand_id in list_brand_ids(config):
            print(brand_id)
        return 0

    orch = Orchestrator(config=config)

    if args.brand:
        result = orch.run_brand(
            brand_id=args.brand,
            topic=args.topic,
            agents=args.agents,
        )
        print(json.dumps(result, indent=2, default=str))
    else:
        results = orch.run_all_brands(
            topic=args.topic,
            agents=args.agents,
        )
        print(json.dumps(results, indent=2, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
