# Claude Sales AI Agents

A 5-agent organic growth system for DTC brands, powered by Claude Opus 4.6.

Built for anyone running **multiple brands** (like two fashion shops + a
furniture brand) who wants to drive more orders primarily through **free
channels**: SEO, AI Search Optimization, organic social, lifecycle email,
and free analytics tools.

---

## What's in the box

Five specialized agents — each with its own prompt, methodology, and
output formats — coordinated by an orchestrator:

| # | Agent               | Produces                                                      |
|---|---------------------|---------------------------------------------------------------|
| 1 | **SEO Content**     | Blog posts, product descriptions, keyword clusters, FAQ pages |
| 2 | **Social Media**    | 30-day calendars, viral hooks, UGC briefs, hashtag strategies |
| 3 | **Technical SEO**   | JSON-LD schema, meta tags, sitemap plan, AI-crawler guide     |
| 4 | **Email Marketing** | Welcome series, abandoned cart, post-purchase, seasonal flows |
| 5 | **Analytics**       | KPI dashboards, competitor teardowns, free-tools setup guide  |

Every agent writes **brand-specific** content, on-voice and on-strategy,
by reading a single YAML config (`config/brands.yaml`).

See [docs/STRATEGY.md](docs/STRATEGY.md) for the playbook these agents
are designed to execute, and [docs/FREE_TOOLS.md](docs/FREE_TOOLS.md)
for the free analytics stack they rely on.

---

## Why Claude Opus 4.6

- **Adaptive thinking** — spends more compute on a 10-post keyword
  cluster than on a single meta description. You pay for depth only
  when it matters.
- **Prompt caching** — the stable role prompt + brand context are marked
  `cache_control: ephemeral`, so running multiple tasks for the same
  brand in one session drops input-token cost by ~10x.
- **Streaming by default** — long outputs (full blog posts, 30-day
  calendars) don't hit HTTP timeouts.

All three come straight out of the Anthropic Python SDK, no LangChain or
wrappers in the loop.

---

## Setup

Requirements: Python 3.10+, an Anthropic API key.

```bash
# 1. Clone and enter the repo
git clone <your-fork-url>
cd Claude_Sales_AI_Agents

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# then edit .env and paste your key

# 4. Fill in your brand details
# Open config/brands.yaml and replace the three placeholder brands
# with your actual brand voice, audience, USP, competitors, seed keywords.
# The more specific you are here, the sharper every agent's output will be.
```

---

## Usage

### List what's configured

```bash
python -m src.main --list-brands
python -m src.main --list-agents
```

### Run everything for one brand

```bash
python -m src.main --brand fashion_brand_1 \
  --topic "minimalist capsule wardrobe"
```

This runs all 5 agents for `fashion_brand_1` and writes outputs to:

```
outputs/fashion_brand_1/seo_content/2026-04-10_blog-....md
outputs/fashion_brand_1/social_media/2026-04-10_calendar-....md
outputs/fashion_brand_1/technical_seo/2026-04-10_sitemap-....md
outputs/fashion_brand_1/email_marketing/2026-04-10_welcome-series.md
outputs/fashion_brand_1/analytics/2026-04-10_kpi-dashboard.md
... etc.
```

### Run a single agent for a single brand

```bash
python -m src.main --brand furniture_brand \
  --agents seo_content \
  --topic "small apartment living room setup"
```

### Run a few agents for every brand

```bash
python -m src.main \
  --agents seo_content email_marketing \
  --topic "spring refresh"
```

### Programmatic use

```python
from src.orchestrator import Orchestrator

orch = Orchestrator()

result = orch.run_brand(
    brand_id="fashion_brand_2",
    topic="streetwear drops",
    agents=["social_media", "seo_content"],
)
print(result)
```

---

## Project structure

```
Claude_Sales_AI_Agents/
├── README.md
├── requirements.txt
├── .env.example
├── config/
│   └── brands.yaml           # Your brands' voice, audience, USP
├── docs/
│   ├── STRATEGY.md           # The organic growth playbook
│   └── FREE_TOOLS.md         # Free analytics tool stack
├── src/
│   ├── __init__.py
│   ├── main.py               # CLI entry point
│   ├── orchestrator.py       # Coordinates agent runs across brands
│   ├── utils.py              # Config, paths, slugs, brand context
│   └── agents/
│       ├── __init__.py
│       ├── base.py           # Shared Claude API plumbing (streaming,
│       │                     # caching, thinking)
│       ├── seo_content.py
│       ├── social_media.py
│       ├── technical_seo.py
│       ├── email_marketing.py
│       └── analytics.py
└── outputs/                  # Generated content lands here
    └── <brand_id>/<agent>/YYYY-MM-DD_<filename>.md
```

---

## The flywheel

```
  SEO content ──► Organic search traffic ──► Email capture
       ▲                                           │
       │                                           ▼
  Social content ◄── UGC / Reviews ◄── Repeat purchases
```

- **SEO Content + Technical SEO** create the entry points (Google + AI
  Overviews + ChatGPT Search)
- **Social Media** drives net-new attention from TikTok / IG / Pinterest
- **Email Marketing** converts attention into first orders and repeat
  orders
- **Analytics** tells you which 20% of assets are pulling 80% of the
  weight so you can double down next month

See [docs/STRATEGY.md](docs/STRATEGY.md) for the 90-day plan.

---

## Customizing an agent

Every agent subclasses `BaseAgent` and only needs two things:

1. A `role_prompt` string (the stable system prompt — cached)
2. A `run(**kwargs)` method that decides which deliverables to produce

To add a new agent (say, `InfluencerAgent`):

```python
# src/agents/influencer.py
from .base import BaseAgent

ROLE_PROMPT = """You are a senior influencer-marketing strategist..."""

class InfluencerAgent(BaseAgent):
    name = "influencer"
    role_prompt = ROLE_PROMPT

    def find_creators(self, niche: str) -> str:
        return self.generate(f"List 20 micro-creators for {niche}...")

    def run(self, topic=None, **_):
        content = self.find_creators(topic or "general")
        path = self.save(f"creators-{topic}", content)
        return {"agent": self.name, "files": [str(path)]}
```

Then register it in `src/agents/__init__.py` and
`src/orchestrator.py`'s `AGENT_REGISTRY`.

---

## Guardrails

- These agents are **co-pilots, not autopilot**. A human reads every
  output before it ships.
- The Technical SEO Agent outputs JSON-LD that is **valid** but may
  contain placeholder URLs or SKUs — check before pasting into `<head>`.
- Always validate schema with Google's
  [Rich Results Test](https://search.google.com/test/rich-results) first.
- Email content should be reviewed for **deliverability** (spam triggers,
  image ratio, link count) before pushing to your ESP.

---

## License

MIT — do whatever you like with it.
