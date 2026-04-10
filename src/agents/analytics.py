"""
Analytics Agent
===============

Closes the loop on the other four agents: tells the brand what to measure,
how to measure it with FREE tools, who they're losing to, and what to do
next month based on what worked this month.

Output formats
--------------
* KPI dashboards and baseline tracking plans
* Competitor teardowns (organic + social + SEO)
* Free-tool setup guides (GSC, GA4, Bing Webmaster, Keyword Planner,
  Ahrefs Webmaster Tools, Microsoft Clarity, etc.)
* Monthly performance reviews with next-month recommendations
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent


ROLE_PROMPT = """
You are a senior growth analyst embedded with a lean DTC team. You don't
have a paid analytics stack. You squeeze every ounce of insight from FREE
tools: Google Search Console, Google Analytics 4, Bing Webmaster Tools,
Microsoft Clarity (free session recordings), Ahrefs Webmaster Tools (free
tier), Google Keyword Planner, Google Trends, SimilarWeb (free tier),
SpyFu (free tier), and native platform analytics (IG Insights, TikTok
Analytics, Pinterest Analytics).

## Core competencies

1. **KPI frameworks** — You define North-Star, leading, and lagging
   metrics for organic growth programs. You translate vanity metrics
   (impressions, followers) into revenue-relevant ones (qualified
   sessions, add-to-cart rate, email signup rate, revenue per visitor).

2. **Competitor intelligence** — You teach the team to read a competitor's
   site + socials + backlinks and extract 3-5 things worth copying and
   3-5 things worth *not* copying.

3. **Free-tool mastery** — You can walk a non-technical founder through
   setting up GSC and GA4 from scratch in under an hour, and you know the
   one-line answer to questions like 'which GA4 report tells me which
   landing pages convert best?'.

4. **Monthly review cadence** — You close the loop: what ran, what
   happened, what to do next. You never present a number without a
   recommendation attached.

## Output format

Return Markdown. Prefer tables for KPIs and competitor comparisons. When
writing setup guides, use numbered steps with screenshots-would-go-here
notes. When flagging an issue, always pair it with a concrete next action.

Never recommend a paid tool unless you first exhaust the free equivalent
and explain why free isn't enough.
""".strip()


class AnalyticsAgent(BaseAgent):
    name = "analytics"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Individual deliverables                                            #
    # ------------------------------------------------------------------ #
    def build_kpi_dashboard(self) -> str:
        task = (
            f"Design an organic-growth KPI dashboard for this brand.\n\n"
            f"Deliver:\n"
            f"1. **North-Star metric** with justification\n"
            f"2. **Leading indicators** (things that move BEFORE revenue)\n"
            f"3. **Lagging indicators** (revenue, repeat rate, LTV)\n"
            f"4. For each metric: target / warning / critical thresholds "
            f"appropriate to a small DTC brand\n"
            f"5. Which FREE tool measures it (GSC / GA4 / IG Insights / etc.)\n"
            f"6. Recommended review cadence (daily / weekly / monthly)\n\n"
            f"Return as a Markdown table, then a short 'how to read this "
            f"dashboard' paragraph for a non-technical founder."
        )
        return self.generate(task)

    def build_competitor_teardown(self, competitor_name_or_url: str) -> str:
        task = (
            f"Do a free-tools-only teardown of this competitor:\n\n"
            f"**Competitor:** {competitor_name_or_url}\n\n"
            f"Deliver:\n"
            f"1. **Organic content signals** — What kinds of blog posts / "
            f"landing pages do they seem to rank for? Which keywords "
            f"should we go after *next to* them (where we can realistically "
            f"win) and which to avoid?\n"
            f"2. **Social presence** — Which platforms are they strong on, "
            f"what content pillars, what works for them.\n"
            f"3. **3 things worth copying** (specific tactics, not vibes).\n"
            f"4. **3 things worth NOT copying** (traps).\n"
            f"5. **One asymmetric opportunity** they're missing that we "
            f"can own.\n"
            f"6. A short 'how I'd research this further for free' section "
            f"listing the exact free tools and queries."
        )
        return self.generate(task)

    def build_free_tools_setup_guide(self) -> str:
        task = (
            f"Write a step-by-step setup guide for the core free analytics "
            f"stack every DTC brand should have.\n\n"
            f"Cover each of these tools with: what it's for, how to set it "
            f"up (numbered steps), 2-3 reports worth bookmarking, and "
            f"'one gotcha' a beginner hits:\n\n"
            f"1. Google Search Console\n"
            f"2. Google Analytics 4 (with ecommerce events enabled)\n"
            f"3. Bing Webmaster Tools\n"
            f"4. Ahrefs Webmaster Tools (free tier)\n"
            f"5. Microsoft Clarity (free session recordings + heatmaps)\n"
            f"6. Google Keyword Planner\n"
            f"7. Google Trends\n"
            f"8. Native platform analytics (IG / TikTok / Pinterest)\n\n"
            f"End with a 'day one / week one / month one' implementation "
            f"checklist so a founder knows exactly what to do first."
        )
        return self.generate(task)

    def build_monthly_review_template(self) -> str:
        task = (
            f"Create a reusable monthly organic-growth review template "
            f"for this brand. It should be a fill-in Markdown document "
            f"the team can copy at the start of each month.\n\n"
            f"Sections:\n"
            f"- **Headline numbers** (organic sessions, revenue, email "
            f"list growth, social followers by platform)\n"
            f"- **What we shipped** (blog posts, social posts, emails, "
            f"technical changes)\n"
            f"- **What worked** (top 3 wins with data)\n"
            f"- **What didn't** (top 3 misses with hypotheses)\n"
            f"- **Funnel health** (GSC impressions → clicks → sessions → "
            f"add-to-cart → purchase)\n"
            f"- **Competitive note** (anything notable a competitor did)\n"
            f"- **Next month's top 3 experiments** (with success criteria)\n\n"
            f"Include inline placeholders like `[insert number]` and "
            f"short prompts to help a non-analyst fill it in."
        )
        return self.generate(task)

    def build_attribution_playbook(self) -> str:
        task = (
            f"Write a short playbook on attribution for an organic-only "
            f"DTC brand.\n\n"
            f"Cover:\n"
            f"- Why last-click attribution lies to you (esp. for "
            f"content + social-led brands)\n"
            f"- How to use GA4's 'default channel grouping' and "
            f"'data-driven attribution' correctly\n"
            f"- How to add UTM tags to every organic social link without "
            f"breaking them\n"
            f"- A simple 'post-purchase survey' (one-question: 'how did "
            f"you hear about us?') as the single most useful free "
            f"attribution signal\n"
            f"- When to trust which signal for which decision."
        )
        return self.generate(task)

    # ------------------------------------------------------------------ #
    # Orchestrator entry point                                           #
    # ------------------------------------------------------------------ #
    def run(
        self,
        topic: str | None = None,
        competitors: list[str] | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        """
        Produce the default analytics onboarding pack:
            - KPI dashboard
            - free-tools setup guide
            - monthly review template
            - one competitor teardown per competitor provided
        """
        files: list[str] = []

        dashboard = self.build_kpi_dashboard()
        files.append(str(self.save("kpi-dashboard", dashboard)))

        guide = self.build_free_tools_setup_guide()
        files.append(str(self.save("free-tools-setup-guide", guide)))

        review = self.build_monthly_review_template()
        files.append(str(self.save("monthly-review-template", review)))

        # Pull competitors from the brand config if the caller didn't pass any
        competitors = competitors or self.brand.get("competitors") or []
        for competitor in competitors:
            teardown = self.build_competitor_teardown(competitor)
            files.append(str(self.save(f"competitor-teardown-{competitor}", teardown)))

        return {
            "agent": self.name,
            "brand": self.brand["id"],
            "topic": topic,
            "files": files,
            "summary": (
                f"Produced a KPI dashboard, free-tools setup guide, "
                f"monthly review template, and "
                f"{len(competitors)} competitor teardown(s)."
            ),
        }
