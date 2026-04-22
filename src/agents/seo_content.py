"""
SEO Content Agent
=================

Writes long-form SEO content designed to rank in Google *and* get cited by
AI Overviews / ChatGPT / Perplexity. Output formats:

* Blog posts (1500-2500 words, featured-snippet optimized)
* Product descriptions (E-E-A-T signals, buyer-intent keywords)
* FAQ pages (PAA-style questions, schema-ready answers)
* Keyword clusters (topic -> pillar + supporting posts)
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent


ROLE_PROMPT = """
You are a senior SEO content strategist and copywriter with 10+ years of
experience ranking ecommerce brands on Google. You specialize in:

1. **Traditional SEO** — long-tail keyword targeting, search-intent matching,
   E-E-A-T signals, featured-snippet structure, and internal linking.
2. **AI Search Optimization (AEO/GEO)** — writing in a way that Google AI
   Overviews, ChatGPT Search, Perplexity, and Claude actually cite. This
   means: clear definitions up top, structured comparisons, numbered lists,
   specific facts with sources, and semantic completeness.
3. **Conversion copywriting** — content that ranks *and* drives clicks to
   product pages. You always include a soft CTA.

## Methodology

Whenever you write, follow this order:
1. Identify the primary search intent (informational, commercial,
   transactional, or navigational).
2. Surface 3-5 related long-tail keywords you'll naturally integrate.
3. Structure content with H2/H3 headings that match People-Also-Ask.
4. Open with a direct answer to the query in the first 40-60 words
   (snippet bait).
5. Include one comparison table or bulleted list whenever reasonable
   (AI engines cite these disproportionately).
6. Close with an internal-link suggestion and a soft CTA.

## Output format

Always return clean Markdown. Begin with a short metadata block like:

---
title: "..."
primary_keyword: "..."
secondary_keywords: ["...", "..."]
search_intent: "informational | commercial | transactional"
target_word_count: 1800
meta_description: "..."  # 150-160 chars, has the primary keyword
---

Then the content itself.

Never use filler like "In today's fast-paced world". Be specific, be useful,
be unmistakably on-brand.
""".strip()


class SEOContentAgent(BaseAgent):
    name = "seo_content"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Individual content types                                           #
    # ------------------------------------------------------------------ #
    def write_blog_post(self, topic: str, word_count: int = 1800) -> str:
        task = (
            f"Write a complete SEO blog post on this topic:\n\n"
            f"**Topic:** {topic}\n"
            f"**Target word count:** ~{word_count} words\n\n"
            f"Requirements:\n"
            f"- Optimize for the primary long-tail keyword you choose\n"
            f"- Include at least one comparison table OR numbered list for "
            f"AI-snippet targeting\n"
            f"- Answer the main question in the first paragraph (40-60 words)\n"
            f"- Include an FAQ section (4-6 questions) at the bottom\n"
            f"- End with a soft CTA pointing to a relevant collection "
            f"or product on the brand's site"
        )
        return self.generate(task)

    def write_product_description(
        self, product_name: str, key_features: list[str] | None = None
    ) -> str:
        features = key_features or []
        feature_block = (
            "\n".join(f"- {f}" for f in features) if features else "(not provided — use your judgement)"
        )
        task = (
            f"Write an SEO-optimized product description for:\n\n"
            f"**Product:** {product_name}\n"
            f"**Known features / details:**\n{feature_block}\n\n"
            f"Deliverables:\n"
            f"1. SEO title (55-60 chars, primary keyword up front)\n"
            f"2. Meta description (150-160 chars)\n"
            f"3. A 120-180 word sales description emphasizing benefits "
            f"(not just features)\n"
            f"4. A bulleted spec list\n"
            f"5. 3 possible product FAQs with answers"
        )
        return self.generate(task)

    def write_keyword_cluster(self, topic: str) -> str:
        task = (
            f"Build a topic cluster for the pillar theme: **{topic}**\n\n"
            f"Deliverables:\n"
            f"1. One **pillar page** concept (broad, high-volume, "
            f"1 recommended title + target keyword)\n"
            f"2. 8-12 **supporting posts** that internally link back to the "
            f"pillar, each with:\n"
            f"   - Working title\n"
            f"   - Primary long-tail keyword\n"
            f"   - Search intent\n"
            f"   - Estimated difficulty (low / medium / high)\n"
            f"   - Why it matters for this brand specifically\n"
            f"3. A recommended publishing order and internal-linking map\n"
            f"4. 3-5 'AI search' queries (e.g. 'what's the best X for Y') "
            f"this cluster should aim to be cited by"
        )
        return self.generate(task)

    def write_faq_page(self, topic: str) -> str:
        task = (
            f"Create an FAQ page on the topic: **{topic}**\n\n"
            f"Deliverables:\n"
            f"- 10-12 questions pulled from likely 'People Also Ask' results\n"
            f"- Each answer is 40-80 words, structured for featured-snippet "
            f"targeting\n"
            f"- Use a mix of what / why / how / is / can questions\n"
            f"- Include a JSON-LD FAQPage schema block at the bottom "
            f"ready to paste into the page's <head>"
        )
        return self.generate(task)

    def write_pillar_page(self, topic: str) -> str:
        """
        Write a comprehensive 3 000+ word pillar/hub page designed to rank for
        a broad head keyword and internally link to all supporting cluster posts.
        """
        task = (
            f"Write a comprehensive pillar page on: **{topic}**\n\n"
            f"Target word count: 3 000-3 500 words.\n\n"
            f"A pillar page is the definitive guide on a broad topic. It ranks "
            f"for the head keyword and links out to every supporting cluster "
            f"post for depth.\n\n"
            f"Structure:\n"
            f"1. **Metadata block** (same YAML front-matter format as always)\n"
            f"2. **Hero section** (60-word direct answer for AI snippets + "
            f"what the reader will learn — no fluff)\n"
            f"3. **Table of contents** (linked H2s)\n"
            f"4. **H2 sections** (6-8 sections covering every major sub-topic; "
            f"each H2 is a long-tail keyword phrase)\n"
            f"   - Each H2 section: 300-400 words + at minimum one comparison "
            f"table, bullet list, or numbered steps (AI engines cite these)\n"
            f"   - Include a '[Deep dive: link to supporting post]' callout "
            f"at the end of each H2 so internal links are mapped\n"
            f"5. **Comparison / summary table** (consolidates key takeaways)\n"
            f"6. **FAQ section** (6-8 PAA-style questions + schema-ready answers)\n"
            f"7. **CTA** (product collection or category page — one CTA, specific)\n\n"
            f"The page must be specific, fact-dense, and genuinely useful as a "
            f"standalone resource — not a surface-level overview."
        )
        return self.generate(task)

    def write_comparison_post(self, topic: str) -> str:
        """
        Write an 'X vs Y' or 'Best X for Y' comparison post.

        These posts target high commercial intent ('which should I buy?')
        and consistently rank #1 in both Google and AI Overviews because
        they contain the structured comparison tables AI engines love to cite.
        """
        competitors = self.brand.get("competitors", [])
        comp_hint = (
            f"\n\nThe brand's main competitors are: {', '.join(competitors)}. "
            f"Include at least one of them in a fair, factual comparison."
            if competitors
            else ""
        )
        task = (
            f"Write a high-converting comparison blog post on: **{topic}**\n\n"
            f"Target word count: 1 800-2 200 words.\n\n"
            f"Comparison posts have the highest commercial intent of any content "
            f"format — readers are actively deciding what to buy.{comp_hint}\n\n"
            f"Structure:\n"
            f"1. **Metadata block** (YAML front-matter)\n"
            f"2. **Quick answer** (first 50 words — name a winner or give a "
            f"clear 'it depends' with 2-3 crisp criteria; this is the AI snippet)\n"
            f"3. **Comparison overview table** immediately after intro:\n"
            f"   Columns: Brand/Option | Price | Key strength | Best for | "
            f"Rating (out of 5)\n"
            f"4. **Deep-dive sections** (one H2 per option being compared, "
            f"300-400 words each)\n"
            f"   - Who it's for, standout features, real limitations (no "
            f"puff), price-to-value assessment\n"
            f"5. **Side-by-side spec table** (the most-cited element in AI "
            f"Overviews — be specific with numbers, materials, dimensions)\n"
            f"6. **Our pick / verdict** section (clear recommendation, no "
            f"fence-sitting — state who should buy which option and why)\n"
            f"7. **FAQ section** (5-6 questions buyers actually ask)\n"
            f"8. **CTA** to the brand's most relevant collection or product\n\n"
            f"Be objective and honest. If a competitor beats the brand on a "
            f"specific dimension, say so — this is what earns trust and "
            f"AI citations. The brand wins on its genuine USPs."
        )
        return self.generate(task)

    # ------------------------------------------------------------------ #
    # Orchestrator entry point                                           #
    # ------------------------------------------------------------------ #
    def run(
        self,
        topic: str | None = None,
        content_types: list[str] | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        """
        Run a full content sprint on `topic`. By default produces:
            - one keyword cluster (content map for the topic)
            - one full blog post
            - one comparison post (high commercial intent)
            - one FAQ page
        """
        if not topic:
            raise ValueError("SEOContentAgent.run() requires a `topic`.")
        content_types = content_types or ["cluster", "blog_post", "comparison", "faq"]

        files: list[str] = []

        if "cluster" in content_types:
            cluster = self.write_keyword_cluster(topic)
            files.append(str(self.save(f"cluster-{topic}", cluster)))

        if "blog_post" in content_types:
            post = self.write_blog_post(topic)
            files.append(str(self.save(f"blog-{topic}", post)))

        if "pillar" in content_types:
            pillar = self.write_pillar_page(topic)
            files.append(str(self.save(f"pillar-{topic}", pillar)))

        if "comparison" in content_types:
            comparison = self.write_comparison_post(topic)
            files.append(str(self.save(f"comparison-{topic}", comparison)))

        if "faq" in content_types:
            faq = self.write_faq_page(topic)
            files.append(str(self.save(f"faq-{topic}", faq)))

        return {
            "agent": self.name,
            "brand": self.brand["id"],
            "topic": topic,
            "files": files,
            "summary": (
                f"Produced {len(files)} content asset(s) for '{topic}': "
                f"{', '.join(content_types)}"
            ),
        }
