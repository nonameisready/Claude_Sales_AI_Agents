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
            - one keyword cluster
            - one full blog post on the first supporting title
            - one FAQ page
        """
        if not topic:
            raise ValueError("SEOContentAgent.run() requires a `topic`.")
        content_types = content_types or ["cluster", "blog_post", "faq"]

        files: list[str] = []

        if "cluster" in content_types:
            cluster = self.write_keyword_cluster(topic)
            files.append(str(self.save(f"cluster-{topic}", cluster)))

        if "blog_post" in content_types:
            post = self.write_blog_post(topic)
            files.append(str(self.save(f"blog-{topic}", post)))

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
