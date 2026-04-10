"""
Email Marketing Agent
=====================

Builds the lifecycle email flows that generate the highest ROI of any
channel for DTC brands — welcome series, abandoned cart, post-purchase,
winback, and seasonal campaigns.

Output formats
--------------
* Multi-email flows with timing, subject lines, preheaders, bodies, CTAs
* Single campaign emails (holiday, launch, restock)
* Subject line libraries with A/B test variants
* Segmentation + list-growth tactics
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent


ROLE_PROMPT = """
You are a senior email / lifecycle marketer who has built 8-figure
revenue programs for DTC brands on Klaviyo, Omnisend, and Mailchimp.
You treat email as a 1:1 conversation — not a newsletter blast.

## Core principles

1. **Segment before you write.** Every flow assumes a segment with a
   specific intent (first-time visitor, cart abandoner, 60-day lapsed
   customer, VIP, etc.). You name the segment explicitly.
2. **The subject line + preheader are 80% of the work.** You always
   write them as a unit — the preheader completes or subverts the
   subject, it doesn't repeat it.
3. **One CTA per email.** Multiple CTAs dilute clicks. If there must
   be two, one is primary and one is tertiary/footer.
4. **Plain-text-first.** You write emails that would still convert if
   the images failed to load, because for ~20% of recipients they do.
5. **Deliverability hygiene.** You avoid spam trigger words, balance
   image-to-text, keep links sane, and never use all-caps in subjects.

## Flow design

For multi-email flows, you specify:
* **Trigger** — what event enrolls someone
* **Exit conditions** — what removes them (purchase, unsubscribe, etc.)
* **Timing** — delay between each email, with reasoning
* **Goal metric** — CTR, revenue per recipient, reactivation rate

For each email in a flow, you deliver:
* Subject line (under 50 chars)
* Preheader (under 90 chars, complements subject)
* Email body in Markdown (headings, short paragraphs, clear CTA)
* Primary CTA button copy + where it links
* Fallback plain-text version notes

## Output format

Return Markdown. Use `###` for each email in a flow. Use a metadata
block at the top:

```
Flow: Welcome Series
Segment: New email subscribers who haven't purchased
Goal: First purchase within 14 days
Emails: 4
```

Then the emails. Never use filler ("Dear valued customer"). Write like
a smart friend recommending a brand they actually love.
""".strip()


class EmailMarketingAgent(BaseAgent):
    name = "email_marketing"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Individual deliverables                                            #
    # ------------------------------------------------------------------ #
    def build_welcome_series(self, incentive: str | None = None) -> str:
        incentive_line = (
            f"**Signup incentive offered:** {incentive}\n"
            if incentive
            else "**Signup incentive:** 10% off first order (assume this unless the brand says otherwise)\n"
        )
        task = (
            f"Build a 4-email welcome series for new subscribers.\n\n"
            f"{incentive_line}\n"
            f"Structure:\n"
            f"- **Email 1** (immediate): deliver the incentive + brand story hook\n"
            f"- **Email 2** (+2 days): the USP / why this brand is different\n"
            f"- **Email 3** (+4 days): social proof (reviews, UGC, press)\n"
            f"- **Email 4** (+6 days): last-chance nudge on the incentive + "
            f"introduce the hero collection\n\n"
            f"Deliver full subject lines, preheaders, bodies, and CTAs for "
            f"each. Include the flow metadata block at the top."
        )
        return self.generate(task)

    def build_abandoned_cart_flow(self) -> str:
        task = (
            f"Build a 3-email abandoned cart recovery flow.\n\n"
            f"Structure:\n"
            f"- **Email 1** (+1 hour): 'You left something' — helpful tone, "
            f"show items, no discount yet\n"
            f"- **Email 2** (+23 hours): overcome objections — reviews, "
            f"shipping/return reassurance, stock scarcity if honest\n"
            f"- **Email 3** (+48 hours): final nudge — small incentive "
            f"(free shipping or 10% off, not both) + clear CTA\n\n"
            f"Deliver full subjects, preheaders, bodies, CTAs, and the "
            f"metadata block at the top. Include one A/B variant subject "
            f"for each email."
        )
        return self.generate(task)

    def build_post_purchase_flow(self) -> str:
        task = (
            f"Build a 4-email post-purchase flow designed to maximize "
            f"repeat purchases and reviews.\n\n"
            f"Structure:\n"
            f"- **Email 1** (immediate): order confirmation + what to "
            f"expect (shipping, unboxing)\n"
            f"- **Email 2** (on delivery day): 'how to get the most from "
            f"your purchase' — education, styling/usage, care\n"
            f"- **Email 3** (+7 days): review request with a clear link "
            f"and small incentive (entry into a giveaway, loyalty points)\n"
            f"- **Email 4** (+21 days): curated 'complete the look / "
            f"complete the room' recommendations\n\n"
            f"Deliver full subjects, preheaders, bodies, and CTAs."
        )
        return self.generate(task)

    def build_seasonal_campaign(self, occasion: str) -> str:
        task = (
            f"Build a 3-email seasonal campaign for: **{occasion}**\n\n"
            f"Structure:\n"
            f"- **Email 1** — teaser / announcement (build anticipation)\n"
            f"- **Email 2** — main launch / offer\n"
            f"- **Email 3** — last call (urgency, final hours)\n\n"
            f"Respect the brand voice — don't use generic holiday clichés. "
            f"Tie the offer to the brand's seasonal_focus. Deliver full "
            f"subjects, preheaders, bodies, and CTAs, plus the metadata "
            f"block at the top."
        )
        return self.generate(task)

    def build_subject_line_library(self, topic: str, count: int = 25) -> str:
        task = (
            f"Generate {count} high-performing subject lines for emails "
            f"about: **{topic}**\n\n"
            f"Rules:\n"
            f"- Each subject line ≤ 50 characters\n"
            f"- Label each with archetype "
            f"(curiosity / benefit / urgency / personal / numbered / "
            f"question / controversial)\n"
            f"- For each, also give a matching preheader (≤ 90 chars) "
            f"that complements — not repeats — the subject\n"
            f"- At the bottom, recommend the top 5 to A/B test first"
        )
        return self.generate(task)

    def build_winback_flow(self) -> str:
        task = (
            f"Build a 3-email winback flow for customers who haven't "
            f"purchased in 90+ days.\n\n"
            f"Structure:\n"
            f"- **Email 1**: 'we miss you' — soft, reintroduce what's new\n"
            f"- **Email 2**: best-seller showcase + a real incentive\n"
            f"- **Email 3**: last call + confirm unsubscribe path (list "
            f"hygiene matters — let uninterested contacts leave cleanly)\n\n"
            f"Deliver full subjects, preheaders, bodies, and CTAs."
        )
        return self.generate(task)

    # ------------------------------------------------------------------ #
    # Orchestrator entry point                                           #
    # ------------------------------------------------------------------ #
    def run(
        self,
        topic: str | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        """
        Produce the core lifecycle stack any DTC brand should have:
            - welcome series
            - abandoned cart
            - post-purchase
            - (optional) seasonal campaign if `topic` is set
        """
        files: list[str] = []

        welcome = self.build_welcome_series()
        files.append(str(self.save("welcome-series", welcome)))

        cart = self.build_abandoned_cart_flow()
        files.append(str(self.save("abandoned-cart-flow", cart)))

        post = self.build_post_purchase_flow()
        files.append(str(self.save("post-purchase-flow", post)))

        if topic:
            seasonal = self.build_seasonal_campaign(topic)
            files.append(str(self.save(f"seasonal-{topic}", seasonal)))

        return {
            "agent": self.name,
            "brand": self.brand["id"],
            "topic": topic,
            "files": files,
            "summary": (
                f"Produced {len(files)} lifecycle email flow(s): "
                f"welcome, abandoned cart, post-purchase"
                + (f", seasonal ({topic})" if topic else "")
                + "."
            ),
        }
