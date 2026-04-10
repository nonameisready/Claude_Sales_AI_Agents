"""
Social Media Agent
==================

Creates organic social content across the platforms that actually move
product for DTC brands: Instagram, TikTok, Pinterest, X/Twitter, Facebook,
and YouTube (Shorts + long-form).

Output formats
--------------
* 30-day content calendars (platform-aware, season-aware)
* Viral hook libraries (IG Reels, TikTok, YouTube Shorts)
* UGC / creator briefs
* Hashtag strategies (niche + broad + branded)
* Platform-specific post copy (captions, scripts, pin descriptions)
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent


ROLE_PROMPT = """
You are a senior organic-social strategist who has grown multiple DTC brands
from zero to 100k+ followers without paid ads. You think in hooks, pattern
interrupts, and retention curves — not vanity metrics.

## Platform expertise

* **Instagram** — Reels first, carousels for saves, Stories for retention.
  You know IG's algorithm rewards saves + shares > likes.
* **TikTok** — 1.5-second hook window, native-feeling scripts, trending
  sounds, text overlay pacing, CapCut-friendly structure.
* **Pinterest** — the most underrated free-traffic source for fashion &
  home. Keyword-stuffed descriptions, idea pins, seasonal boards, rich pins.
* **X / Twitter** — short-form threads, behind-the-scenes, founder voice.
* **Facebook** — community groups + shoppable catalog posts for 35+ demo.
* **YouTube** — Shorts for discovery, long-form for authority (lookbooks,
  styling tutorials, home tours, "how I made X" content).

## Methodology

For every asset you produce, you:
1. Start with the **hook** (first 1.5 seconds or first 8 words).
2. Name the **retention mechanism** (loop, open question, countdown, etc.).
3. Match the format to the platform's native behavior — never cross-post
   verbatim.
4. Write captions that stand alone (the video may be muted).
5. Suggest 1 **CTA** per post (save, share, comment keyword, link in bio).

## Hashtag philosophy

You never dump 30 generic tags. You use a tiered mix:
* 3-5 **niche** tags (under 100k posts — real discovery)
* 5-8 **mid-tier** tags (100k - 2M posts — the sweet spot)
* 2-3 **broad** tags (context only)
* 1 **branded** tag (for UGC tracking)

## Output format

Return clean Markdown. When producing a calendar, use a table with columns:
`Day | Platform | Format | Hook | Caption/Script | CTA | Hashtags/Notes`.
For single posts, use headed sections. Always specify the platform.

Never use recycled creator-economy clichés ("get ready with me" without a
twist, "POV:" hooks that don't pay off, "tell me X without telling me X").
Be specific to this brand.
""".strip()


class SocialMediaAgent(BaseAgent):
    name = "social_media"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Individual deliverables                                            #
    # ------------------------------------------------------------------ #
    def build_content_calendar(
        self,
        days: int = 30,
        platforms: list[str] | None = None,
        theme: str | None = None,
    ) -> str:
        platforms = platforms or ["Instagram", "TikTok", "Pinterest"]
        theme_line = f"**Theme / focus:** {theme}\n" if theme else ""
        task = (
            f"Build a {days}-day organic social content calendar.\n\n"
            f"**Platforms:** {', '.join(platforms)}\n"
            f"{theme_line}"
            f"\nRequirements:\n"
            f"- Aim for 1 post per platform per day (adjust down for YouTube "
            f"long-form to 1-2/week).\n"
            f"- Mix content pillars: 40% educational/inspirational, "
            f"30% product-led, 20% UGC/community, 10% behind-the-scenes.\n"
            f"- Seasonal awareness — reflect the brand's `seasonal_focus` "
            f"from the brief.\n"
            f"- For each row, give a concrete hook, not a topic.\n"
            f"- At the end, list 3 'hero' posts to boost with even a tiny "
            f"($5-10) paid amplification if budget allows.\n"
            f"- Include a weekly recurring cadence summary."
        )
        return self.generate(task)

    def write_viral_hooks(self, product_or_topic: str, count: int = 20) -> str:
        task = (
            f"Generate {count} scroll-stopping social hooks for:\n\n"
            f"**Subject:** {product_or_topic}\n\n"
            f"Rules:\n"
            f"- Each hook is ≤ 12 words, designed for the first 1.5 seconds.\n"
            f"- Label each hook with its archetype "
            f"(contrarian / curiosity gap / before-after / listicle / "
            f"founder confession / stat drop / demo / POV-with-payoff).\n"
            f"- Note which platform it fits best (IG Reels / TikTok / "
            f"YouTube Shorts).\n"
            f"- After the list, pick the 3 strongest and write a full "
            f"30-second script for each (hook → value → CTA)."
        )
        return self.generate(task)

    def write_ugc_brief(self, campaign_goal: str) -> str:
        task = (
            f"Draft a UGC / micro-creator brief for this campaign goal:\n\n"
            f"**Goal:** {campaign_goal}\n\n"
            f"Deliverables:\n"
            f"1. Campaign name + one-line pitch\n"
            f"2. Ideal creator profile (follower range, niche, vibe)\n"
            f"3. 3 content concepts with hook + beats + CTA\n"
            f"4. Do's and don'ts (aligned to the brand voice)\n"
            f"5. Usage rights + posting requirements\n"
            f"6. Suggested non-cash compensation ideas "
            f"(free product tiers, affiliate code, reposts)\n"
            f"7. Branded hashtag + tracking plan"
        )
        return self.generate(task)

    def write_hashtag_strategy(self, topic: str) -> str:
        task = (
            f"Build a hashtag strategy for content about: **{topic}**\n\n"
            f"Deliverables:\n"
            f"- 3 reusable hashtag sets (Discovery / Community / Shopping), "
            f"each a tiered mix of niche + mid + broad tags.\n"
            f"- Estimated post count for each tag (rough order of "
            f"magnitude is fine) so we understand saturation.\n"
            f"- 1 branded hashtag recommendation + rollout idea.\n"
            f"- Note which sets fit which platform (IG vs TikTok vs "
            f"Pinterest keywords — Pinterest is keyword-SEO, not hashtag-SEO, "
            f"so treat it differently)."
        )
        return self.generate(task)

    def write_platform_post(self, platform: str, concept: str) -> str:
        task = (
            f"Write a complete post for **{platform}** around this concept:\n\n"
            f"**Concept:** {concept}\n\n"
            f"Return:\n"
            f"- The hook (first 1.5 seconds or first line)\n"
            f"- The full script or caption\n"
            f"- On-screen text cues (if video)\n"
            f"- CTA\n"
            f"- Hashtags / keywords sized for that platform\n"
            f"- 1 sentence explaining *why* this will retain viewers"
        )
        return self.generate(task)

    # ------------------------------------------------------------------ #
    # Orchestrator entry point                                           #
    # ------------------------------------------------------------------ #
    def run(
        self,
        topic: str | None = None,
        platforms: list[str] | None = None,
        days: int = 30,
        **_: Any,
    ) -> dict[str, Any]:
        """
        Produce a default social sprint:
            - one 30-day calendar
            - one viral hook library around `topic`
            - one hashtag strategy around `topic`
        """
        if not topic:
            raise ValueError("SocialMediaAgent.run() requires a `topic`.")
        platforms = platforms or ["Instagram", "TikTok", "Pinterest"]
        files: list[str] = []

        calendar = self.build_content_calendar(
            days=days, platforms=platforms, theme=topic
        )
        files.append(str(self.save(f"calendar-{topic}-{days}d", calendar)))

        hooks = self.write_viral_hooks(topic, count=20)
        files.append(str(self.save(f"hooks-{topic}", hooks)))

        hashtags = self.write_hashtag_strategy(topic)
        files.append(str(self.save(f"hashtags-{topic}", hashtags)))

        return {
            "agent": self.name,
            "brand": self.brand["id"],
            "topic": topic,
            "files": files,
            "summary": (
                f"Produced a {days}-day calendar, 20 viral hooks, and a "
                f"hashtag strategy for '{topic}' across "
                f"{', '.join(platforms)}."
            ),
        }
