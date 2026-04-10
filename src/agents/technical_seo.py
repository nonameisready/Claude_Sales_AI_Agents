"""
Technical SEO Agent
===================

Handles the engineering side of SEO — the stuff that makes Google *and*
modern AI search engines (AI Overviews, ChatGPT Search, Perplexity) able
to understand and cite a site.

Output formats
--------------
* JSON-LD schema blocks (Product, Article, FAQPage, Organization,
  BreadcrumbList, LocalBusiness, Review)
* Meta tag bundles (title, description, OpenGraph, Twitter Card)
* XML sitemap recommendations
* robots.txt + llms.txt templates for AI crawlers
* Technical audit checklists
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent


ROLE_PROMPT = """
You are a senior technical SEO engineer who specializes in ecommerce and
AI Search Optimization (AEO / GEO). You understand how Googlebot, Bingbot,
GPTBot, ClaudeBot, PerplexityBot, and Google-Extended crawl and interpret
sites. You write schema that validates on schema.org *and* actually drives
rich results.

## Core competencies

1. **Structured data / JSON-LD**
   - Product, Offer, AggregateRating, Review
   - Article, BlogPosting, BreadcrumbList
   - FAQPage, HowTo
   - Organization, LocalBusiness, WebSite (+ SearchAction)
   - You always include the required fields and the recommended fields
     for the specific use case — no placeholder junk.

2. **Meta tags**
   - Title tags (55-60 chars, primary keyword front-loaded, brand at end)
   - Meta descriptions (150-160 chars, benefit-driven, CTA verb)
   - OpenGraph + Twitter Card for link previews
   - Canonical, hreflang, robots directives

3. **Crawlability**
   - XML sitemap structure (index + child sitemaps for products,
     collections, blog)
   - robots.txt — Googlebot-friendly while blocking wasteful crawlers
   - llms.txt — the emerging spec for AI crawler guidance (see llmstxt.org)
   - Handling JS-rendered content, faceted nav, pagination

4. **Core Web Vitals** basics — LCP, INP, CLS targets and common fixes
   for Shopify / WooCommerce / custom stacks.

## Output format

When you return schema, wrap it in a fenced code block:

```json
{
  "@context": "https://schema.org",
  ...
}
```

Always validate mentally: required fields present, correct @type, no
trailing commas, no unescaped quotes. When you return meta tags, use
an HTML code block. When you return a checklist, use Markdown checkboxes.

Be precise. A wrong schema block is worse than no schema block.
""".strip()


class TechnicalSEOAgent(BaseAgent):
    name = "technical_seo"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Individual deliverables                                            #
    # ------------------------------------------------------------------ #
    def generate_product_schema(
        self, product_name: str, details: dict[str, Any] | None = None
    ) -> str:
        details = details or {}
        detail_lines = "\n".join(f"- **{k}:** {v}" for k, v in details.items())
        task = (
            f"Produce a complete Product JSON-LD schema block for:\n\n"
            f"**Product:** {product_name}\n"
            f"{detail_lines or '(details not provided — use reasonable placeholders marked clearly)'}\n\n"
            f"Requirements:\n"
            f"- Include Product, Offer, and AggregateRating (if reviews exist)\n"
            f"- Use priceCurrency + availability that can be templated\n"
            f"- Include brand, sku, image, description\n"
            f"- Also return a one-line explanation of any placeholders "
            f"the developer needs to fill in"
        )
        return self.generate(task)

    def generate_meta_bundle(self, page_type: str, page_topic: str) -> str:
        task = (
            f"Produce a complete meta tag bundle for a **{page_type}** page "
            f"about: {page_topic}\n\n"
            f"Deliver:\n"
            f"1. `<title>` (55-60 chars)\n"
            f"2. `<meta name=\"description\">` (150-160 chars)\n"
            f"3. OpenGraph tags (og:title, og:description, og:type, og:image, og:url)\n"
            f"4. Twitter Card tags\n"
            f"5. Canonical link element\n"
            f"6. Recommended robots directive\n\n"
            f"Return as a single pasteable HTML block in the `<head>`."
        )
        return self.generate(task)

    def generate_faq_schema(self, questions_and_answers: list[dict[str, str]]) -> str:
        qa_block = "\n".join(
            f"- Q: {qa.get('q', '')}\n  A: {qa.get('a', '')}"
            for qa in questions_and_answers
        )
        task = (
            f"Produce a valid FAQPage JSON-LD schema block for these Q&As:\n\n"
            f"{qa_block}\n\n"
            f"Return just the JSON-LD in a fenced code block, ready to paste "
            f"into the page `<head>`."
        )
        return self.generate(task)

    def generate_sitemap_plan(self) -> str:
        task = (
            f"Design an XML sitemap strategy for this brand's ecommerce site.\n\n"
            f"Deliverables:\n"
            f"1. Proposed sitemap index structure (parent + child sitemaps)\n"
            f"2. Recommended `<changefreq>` and `<priority>` per content type\n"
            f"3. A small XML example of the sitemap index\n"
            f"4. Submission checklist (Google Search Console, Bing Webmaster, "
            f"IndexNow)\n"
            f"5. A robots.txt template that references the sitemap and "
            f"allows major search + AI crawlers while blocking junk"
        )
        return self.generate(task)

    def generate_ai_crawler_guide(self) -> str:
        task = (
            f"Write an AI Search Optimization (AEO / GEO) implementation "
            f"guide for this brand. Cover:\n\n"
            f"1. Which crawlers matter today (GPTBot, ClaudeBot, "
            f"PerplexityBot, Google-Extended, Amazonbot, etc.) and what "
            f"each one does.\n"
            f"2. A recommended robots.txt block to allow (or block) each.\n"
            f"3. A suggested `llms.txt` file (per llmstxt.org spec) "
            f"pointing AI systems at the brand's most citeable pages.\n"
            f"4. On-page tactics that make a page more citeable by "
            f"LLM-powered search (clear definitions, entity naming, "
            f"consistent facts, structured comparisons, author markup).\n"
            f"5. A 'citation-readiness' checklist developers can hand to "
            f"content teams."
        )
        return self.generate(task)

    def generate_technical_audit(self) -> str:
        task = (
            f"Produce a technical SEO audit checklist tailored to this "
            f"brand's industry and stack (Shopify / WooCommerce / custom — "
            f"make reasonable assumptions and state them).\n\n"
            f"Sections:\n"
            f"- Crawlability & indexation\n"
            f"- On-page (titles, H1s, meta, canonical, internal linking)\n"
            f"- Structured data coverage\n"
            f"- Core Web Vitals (LCP, INP, CLS — common offenders)\n"
            f"- Mobile UX\n"
            f"- AI crawler accessibility\n"
            f"- Duplicate content & faceted nav\n\n"
            f"Use Markdown checkboxes and, for each item, say *why* it "
            f"matters in 1 short sentence."
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
        Run a full technical SEO onboarding pack:
            - sitemap + robots plan
            - AI crawler / llms.txt guide
            - technical audit checklist
            - one example product schema (generic)
        """
        files: list[str] = []

        sitemap = self.generate_sitemap_plan()
        files.append(str(self.save("sitemap-and-robots-plan", sitemap)))

        ai_guide = self.generate_ai_crawler_guide()
        files.append(str(self.save("ai-crawler-optimization-guide", ai_guide)))

        audit = self.generate_technical_audit()
        files.append(str(self.save("technical-seo-audit", audit)))

        example_product = topic or "Hero product (replace with real SKU)"
        schema = self.generate_product_schema(example_product)
        files.append(str(self.save(f"product-schema-example-{example_product}", schema)))

        return {
            "agent": self.name,
            "brand": self.brand["id"],
            "topic": topic,
            "files": files,
            "summary": (
                f"Produced a technical SEO pack (sitemap plan, AI crawler "
                f"guide, audit checklist, example product schema)."
            ),
        }
