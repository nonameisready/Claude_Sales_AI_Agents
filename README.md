# Claude Sales AI Agents

An 8-agent organic growth system for DTC brands, powered by OpenAI GPT-4o.

Built for anyone running **multiple brands** (like two fashion shops + a
furniture brand) who wants to drive more orders primarily through **free
channels**: SEO, AI Search Optimization, organic social, Pinterest, lifecycle
email, community marketing, conversion optimization, and free analytics tools.

---

## What's in the box

Eight specialized agents — each with its own prompt, methodology, and
output formats — coordinated by an orchestrator:

| # | Agent                    | Key (`--agents`)      | Produces                                                          |
|---|--------------------------|-----------------------|-------------------------------------------------------------------|
| 1 | **SEO Content**          | `seo_content`         | Blog posts, product descriptions, keyword clusters, FAQ pages     |
| 2 | **Social Media**         | `social_media`        | 30-day calendars, viral hooks, UGC briefs, hashtag strategies     |
| 3 | **Pinterest SEO**        | `pinterest_seo`       | Board strategy, pin descriptions, Idea Pins, Rich Pins setup      |
| 4 | **Technical SEO**        | `technical_seo`       | JSON-LD schema, meta tags, sitemap plan, AI-crawler guide         |
| 5 | **Conversion (CRO)**     | `cro`                 | Product page copy, trust signals, size guides, checkout copy      |
| 6 | **Community Marketing**  | `community_marketing` | Reddit strategy + posts, Quora answers, Facebook group plan       |
| 7 | **Email Marketing**      | `email_marketing`     | Welcome series, abandoned cart, post-purchase, seasonal flows     |
| 8 | **Analytics**            | `analytics`           | KPI dashboards, competitor teardowns, free-tools setup guide      |

Every agent writes **brand-specific** content, on-voice and on-strategy,
by reading a single YAML config (`config/brands.yaml`).

See [docs/STRATEGY.md](docs/STRATEGY.md) for the playbook these agents
are designed to execute, and [docs/FREE_TOOLS.md](docs/FREE_TOOLS.md)
for the free analytics stack they rely on.

---

## Why GPT-4o

- **128k context window** — the full brand config, role prompt, and task
  all fit comfortably in a single call; no chunking needed.
- **Streaming by default** — long outputs (full blog posts, 30-day
  calendars) don't hit HTTP timeouts.
- **Cost-flexible** — swap `model: gpt-4o` to `model: gpt-4o-mini` in
  `config/brands.yaml` for ~85% lower cost when running high-volume
  scheduled workflows.

Uses the official OpenAI Python SDK directly — no LangChain or wrappers.

---

## Setup

Requirements: Python 3.10+, an OpenAI API key.

```bash
# 1. Clone and enter the repo
git clone <your-fork-url>
cd Claude_Sales_AI_Agents

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# then edit .env and paste your OpenAI API key

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

This runs all 8 agents for `fashion_brand_1` and writes outputs to:

```
outputs/fashion_brand_1/seo_content/2026-04-10_blog-....md
outputs/fashion_brand_1/social_media/2026-04-10_calendar-....md
outputs/fashion_brand_1/pinterest_seo/2026-04-10_board-strategy.md
outputs/fashion_brand_1/technical_seo/2026-04-10_sitemap-....md
outputs/fashion_brand_1/cro/2026-04-10_product-page-copy.md
outputs/fashion_brand_1/community_marketing/2026-04-10_reddit-strategy.md
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
│   └── brands.yaml           # Your brands' voice, audience, USP,
│                             # Pinterest boards, Reddit communities
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
│       ├── pinterest_seo.py  # NEW: Pinterest board strategy, pins,
│       │                     # Idea Pins, Rich Pins / Shopping setup
│       ├── technical_seo.py
│       ├── cro.py            # NEW: Product page copy, trust signals,
│       │                     # size guides, checkout copy, Google Shopping
│       ├── community_marketing.py  # NEW: Reddit, Quora, Facebook groups
│       ├── email_marketing.py
│       └── analytics.py
└── outputs/                  # Generated content lands here
    └── <brand_id>/<agent>/YYYY-MM-DD_<filename>.md
```

---

## The flywheel

```
  SEO content ──► Organic search traffic ──► Email capture
       ▲                 ▲                        │
       │                 │                        ▼
  Social content    Community posts  ◄── Repeat purchases
       ▲                 ▲                        │
       │                 │                        ▼
  Pinterest pins ◄── Product pages ◄── CRO → First order
```

- **SEO Content + Technical SEO** create the entry points (Google + AI Overviews + ChatGPT Search)
- **Social Media** drives net-new attention from TikTok / IG / Pinterest / YouTube
- **Pinterest SEO** compounds visual search traffic — pins have a 3-6 month half-life vs. 24 hrs for IG
- **CRO** ensures visitors who arrive actually buy — product page copy, trust signals, checkout reassurance
- **Community Marketing** builds brand credibility on Reddit, Quora, and Facebook groups; Reddit posts rank in Google for years
- **Email Marketing** converts attention into first orders and repeat orders
- **Analytics** tells you which 20% of assets are pulling 80% of the weight so you can double down next month

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
