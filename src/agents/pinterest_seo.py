"""
PinterestSEOAgent
=================

Pinterest is a visual search engine, not a social network — and it is the
single highest-leverage free channel for fashion and furniture brands.
Pins have a 3-6 month half-life; a well-optimized pin published today can
still drive clicks (and orders) six months from now.

This agent produces:
  • Board strategy — names, descriptions, cover concepts, board order
  • Keyword-rich pin descriptions (title + description + CTA + hashtags)
  • Idea Pin scripts (step-by-step story pins that drive saves)
  • Rich Pins + Shopping Pins setup guide (free product feed in Pinterest)
  • Seasonal pin calendar aligned to the brand's seasonal_focus
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent

ROLE_PROMPT = """
You are a Pinterest SEO strategist and visual content expert specializing in
DTC fashion and home brands. You treat Pinterest as a **visual search engine**,
not a social network, and every recommendation reflects that distinction.

## Your expertise
- Pinterest keyword research and long-tail pin title optimization
- Board architecture that signals topical authority to the Pinterest algorithm
- Idea Pin (story pin) scripting that maximizes saves and follows
- Rich Pins and Shopping Pins setup — the free product catalog feed that
  surfaces your products in Pinterest Shopping, related searches, and the
  shopping spotlight tab
- Seasonal content calendars timed to Pinterest's 45-day lead time (users
  plan ahead — you must publish Christmas content in October)
- Repurposing existing blog posts, product pages, and lookbooks into pins
  without duplicating effort

## Output philosophy
- Every pin title must lead with a keyword (not the brand name)
- Every pin description follows: keyword-rich sentence → benefit sentence →
  soft CTA → 3-5 hashtags (NOT 30 — Pinterest penalizes keyword stuffing)
- Board names must be search-friendly (e.g. "Small Apartment Furniture Ideas"
  not "My Home Inspo")
- Never recommend buying Pinterest ads — this agent is organic-only

## Formatting
Return clean, copy-paste-ready Markdown. Use tables where they add clarity
(e.g., board overview, pin calendar). Separate each pin with a clear
header so the user can find and edit individual pins quickly.
"""


class PinterestSEOAgent(BaseAgent):
    """Pinterest SEO and visual content strategy agent."""

    name = "pinterest_seo"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Deliverable methods                                                 #
    # ------------------------------------------------------------------ #

    def build_board_strategy(self) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        seed_keywords = self.brand.get("seed_keywords", [])
        pinterest_boards = self.brand.get("pinterest_boards", [])

        board_hint = ""
        if pinterest_boards:
            board_hint = (
                f"\n\nThe brand already has or is considering these boards:\n"
                + "\n".join(f"- {b}" for b in pinterest_boards)
            )

        return self.generate(
            f"""
Create a complete Pinterest board strategy for **{brand_name}** — a {industry} brand.

Seed keywords to build around: {", ".join(seed_keywords)}{board_hint}

Deliver:

## 1. Board Architecture Overview (table)
A table with columns: Board Name | Primary Keyword | Secondary Keywords |
Pin Volume Goal (first 90 days) | Cover Image Concept

Include 8-12 boards, ordered from most-to-least important. The first board
should be the brand's most commercially valuable keyword cluster.

## 2. Board Descriptions
For each board: write a 2-3 sentence SEO-optimized board description (160
chars ideal). Embed keywords naturally — do not stuff.

## 3. Secret / Staging Board
One private board strategy for drafting and scheduling pins before they go live.

## 4. Profile Bio
A 160-char Pinterest bio for the brand account that leads with the primary
keyword and ends with a soft CTA.

## 5. Quick Wins
Three boards the brand should create and fill (20 pins each) in the first 7
days to signal topical authority to the algorithm fast.
"""
        )

    def write_pin_descriptions(self, count: int = 15) -> str:
        brand_name = self.brand["name"]
        seed_keywords = self.brand.get("seed_keywords", [])
        website = self.brand.get("website", "")
        usp = self.brand.get("usp", [])

        return self.generate(
            f"""
Write {count} fully optimized Pinterest pin descriptions for **{brand_name}**.

Seed keywords: {", ".join(seed_keywords)}
Website: {website}
Brand USPs: {", ".join(usp) if usp else "not specified"}

For each pin, provide:

### Pin [N]: [Descriptive Pin Title]
**Board:** [which board this belongs to]
**Pin Title (100 chars max):** [keyword-first title]
**Pin Description (500 chars max):**
[keyword-rich opening sentence] [benefit/story sentence] [soft CTA with link or "link in bio"] [3-5 relevant hashtags]
**Image Concept:** [1-2 sentences describing the ideal image or graphic]
**Repurpose Opportunity:** [one sentence: could this image come from a blog post, product page, lookbook, or UGC?]

---

Vary the pin types across: product closeups, lifestyle/styled shots, quote
cards, infographics/tips, before-and-after, step-by-step, and seasonal.

Make sure pin titles lead with the keyword, not the brand name.
"""
        )

    def write_idea_pins_scripts(self, count: int = 5) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        voice = self.brand.get("voice", {})
        tone = voice.get("tone", "friendly and helpful")

        return self.generate(
            f"""
Write {count} complete Idea Pin (multi-slide story pin) scripts for **{brand_name}**
— a {industry} brand with a {tone} voice.

Idea Pins are 2-10 slides and live permanently on Pinterest. They drive
**saves and follows** (the strongest engagement signals). They cannot be
linked out, so the goal is brand recall and audience building, not
direct click-through.

For each Idea Pin, provide:

### Idea Pin [N]: [Topic]
**Keyword / Search Trigger:** [what someone searches to find this]
**Format:** [tutorial / listicle / before-after / outfit formula / room reveal / etc.]
**Slide Count:** [2-10]

**Slides:**
- **Slide 1 (Hook):** [text overlay + image concept — must stop the scroll in 1 second]
- **Slide 2:** [text + image]
- ... (all slides)
- **Final Slide:** [text + image + save prompt or "follow for more X" CTA]

**Save-Worthy Hook:** [one sentence on why someone would save this to come back to]
**Hashtags (on the pin):** [3-5]

---

Ideas should be genuinely useful — tutorials, how-tos, style formulas,
buying guides, room makeovers — not promotional. The brand appears naturally
in the content, not as the subject of the pin.
"""
        )

    def generate_rich_pins_guide(self) -> str:
        website = self.brand.get("website", "yourwebsite.com")
        industry = self.brand.get("industry", "retail")

        return self.generate(
            f"""
Write a complete step-by-step guide for setting up **Rich Pins** and
**Pinterest Shopping** (formerly Catalog / Shopping Pins) for a {industry}
brand with website: {website}

This is a free product feed that puts products directly in:
- Pinterest Shopping tab
- Related product sections under pins
- Shopping Spotlights

## Guide sections:

### 1. Rich Pins vs Shopping Pins — what's the difference
Brief explanation (3-4 sentences), which one to do first.

### 2. Rich Pins Setup (Product Rich Pins)
Step-by-step: Open Graph meta tags OR schema.org Product markup required,
how to validate, how to apply for approval at Pinterest.

### 3. Pinterest Catalog / Shopping Pins Setup
Step-by-step:
- Creating a business account (if not done)
- Claiming the website
- Creating a product data source (feed URL)
- Required feed fields (id, title, description, link, image_link, price,
  availability, condition, google_product_category)
- Feed format options (RSS/XML, CSV, Google Merchant Center import)
- Validation and approval timeline

### 4. Product Group Strategy
How to organize the catalog into product groups for Shopping Ads (if the
brand decides to run ads later) — do this right from day one.

### 5. Common Errors and Fixes
Top 5 feed errors and how to resolve them.

### 6. Ongoing Maintenance
How often to update the feed, how to handle out-of-stock items, seasonal
collections.

Be specific and technical — this is a setup guide, not a marketing pitch.
Include exact field names, character limits, and example values where helpful.
"""
        )

    def build_seasonal_pin_calendar(self, season: str | None = None) -> str:
        brand_name = self.brand["name"]
        seasonal_focus = self.brand.get("seasonal_focus", {})

        if season and season in seasonal_focus:
            focus = seasonal_focus[season]
            season_label = season.title()
        else:
            # Build a full annual calendar hint
            focus = "; ".join(
                f"{s.title()}: {v}" for s, v in seasonal_focus.items()
            )
            season_label = "Annual"

        return self.generate(
            f"""
Create a **{season_label} Pinterest Content Calendar** for **{brand_name}**.

Seasonal product/content focus: {focus}

Pinterest users plan 45-60 days ahead of holidays and seasonal moments.
Content must be published 45 days BEFORE the season begins — not during it.

Deliver:

## 1. Key Publishing Dates (table)
A table: Date | Content Theme | Pin Type | Board | Notes
Cover 8 weeks of publishing cadence (3-5 pins per week = 24-40 rows).

## 2. Content Themes by Week
Brief description of the narrative arc across the season — how content
builds from awareness → consideration → purchase intent → post-purchase.

## 3. Trending Search Terms for This Season
10-15 season-specific keyword phrases the brand should target in pin titles
and descriptions during this window (pulled from Pinterest Trends logic).

## 4. Cross-Channel Repurposing Map
Table showing: Blog post / social post / email → which pins it spawns →
which board those pins go to. Show how one piece of content creates 5+ pins.

## 5. Seasonal Board Covers
Image concepts for updating board covers to match the season (keeps the
profile looking fresh without creating new boards).
"""
        )

    # ------------------------------------------------------------------ #
    # Default run                                                         #
    # ------------------------------------------------------------------ #
    def run(self, topic: str | None = None, **_: Any) -> dict[str, Any]:
        files = []

        print(f"  [{self.name}] Building board strategy ...")
        board_strategy = self.build_board_strategy()
        files.append(str(self.save("board-strategy", board_strategy)))

        print(f"  [{self.name}] Writing pin descriptions ...")
        pins = self.write_pin_descriptions(count=15)
        files.append(str(self.save("pin-descriptions", pins)))

        print(f"  [{self.name}] Writing Idea Pin scripts ...")
        idea_pins = self.write_idea_pins_scripts(count=5)
        files.append(str(self.save("idea-pin-scripts", idea_pins)))

        print(f"  [{self.name}] Generating Rich Pins setup guide ...")
        rich_pins = self.generate_rich_pins_guide()
        files.append(str(self.save("rich-pins-shopping-setup", rich_pins)))

        print(f"  [{self.name}] Building seasonal pin calendar ...")
        season = topic if topic in {"spring", "summer", "fall", "winter"} else None
        calendar = self.build_seasonal_pin_calendar(season=season)
        files.append(str(self.save("seasonal-pin-calendar", calendar)))

        return {
            "agent": self.name,
            "files": files,
            "summary": (
                f"Pinterest strategy: board architecture, {15} pin descriptions, "
                f"5 Idea Pin scripts, Rich Pins setup guide, seasonal calendar"
            ),
        }
