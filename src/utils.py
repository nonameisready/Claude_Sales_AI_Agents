"""Shared utilities: config loading, brand lookup, output paths, slugs."""
from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config" / "brands.yaml"


def load_config(path: Path | str = CONFIG_PATH) -> dict[str, Any]:
    """Load and return the brands.yaml config."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found at {path}. "
            f"Copy config/brands.yaml.example or fill in the template."
        )
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_brand(config: dict[str, Any], brand_id: str) -> dict[str, Any]:
    """Return the brand dict for a given brand id, or raise."""
    for brand in config.get("brands", []):
        if brand.get("id") == brand_id:
            return brand
    available = [b.get("id") for b in config.get("brands", [])]
    raise ValueError(f"Brand '{brand_id}' not found. Available: {available}")


def list_brand_ids(config: dict[str, Any]) -> list[str]:
    return [b["id"] for b in config.get("brands", [])]


def slugify(text: str) -> str:
    """Turn an arbitrary string into a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text[:80] or "untitled"


def output_path(
    config: dict[str, Any],
    brand_id: str,
    agent_name: str,
    filename: str,
) -> Path:
    """
    Compose a timestamped output path:
        outputs/<brand_id>/<agent_name>/YYYY-MM-DD_<filename>
    """
    out_dir = REPO_ROOT / config.get("global", {}).get("output_dir", "outputs")
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    folder = out_dir / brand_id / agent_name
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{date_prefix}_{filename}"


def write_output(path: Path, content: str) -> Path:
    """Write content to a file, returning the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def format_brand_context(brand: dict[str, Any]) -> str:
    """
    Render a brand dict as a readable, stable brief suitable for prompting.

    We use YAML here (not JSON) because it's kinder to Claude's token count
    and the prompt-cache — the layout is deterministic and human-readable.
    """
    return yaml.safe_dump(brand, sort_keys=True, allow_unicode=True).strip()
