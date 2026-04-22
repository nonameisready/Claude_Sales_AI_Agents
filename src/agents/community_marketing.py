"""
CommunityMarketingAgent
========================

Reddit, Quora, and niche Facebook groups are some of the most powerful
(and most overlooked) free traffic channels for DTC brands.

Why they work:
- Reddit posts rank in Google for years — a well-written r/femalefashionadvice
  comment can send qualified traffic for 18+ months
- Quora answers appear in AI Overviews and featured snippets
- Facebook group posts surface to highly targeted, warm audiences
- Community participation builds genuine brand credibility — the opposite
  of ad fatigue

The key constraint: communities are allergic to overt promotion. This agent
only produces value-first content where the brand is mentioned naturally,
if at all. Spam gets accounts banned; genuine participation builds trust.

This agent produces:
  • Reddit community strategy — which subreddits, posting cadence, rules
  • Reddit post drafts — value-first posts that earn upvotes (and traffic)
  • Quora answer strategy — which questions to target, how to answer
  • Quora answer drafts — full answers optimized for featured snippets
  • Facebook group engagement plan — groups to join, how to add value
  • Community brand voice guide — how to show up authentically in each platform
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent

ROLE_PROMPT = """
You are a community marketing strategist specializing in authentic, value-first
brand building across Reddit, Quora, and Facebook groups for DTC brands.

## Your philosophy
Community marketing only works when it is genuinely helpful first. The moment
content feels promotional, it gets downvoted, reported, or deleted — and the
account gets banned, destroying months of relationship-building.

Your approach:
1. **Lead with value** — answer the question, solve the problem, share the
   insight. The brand comes second, if at all.
2. **Match community voice** — every subreddit and Facebook group has its own
   culture, rules, and tone. Never paste the same post across communities.
3. **Play the long game** — a trusted 6-month-old account with 200 karma drives
   more sales than a fresh account spamming promo posts.
4. **Track what ranks** — Reddit posts and Quora answers appear in Google. Use
   keyword-conscious language so the content compounds organically.

## Platform-specific rules you enforce
- **Reddit**: Check and follow subreddit rules before every post. Never post
  affiliate links. Mark brand account identity if the subreddit requires it.
  Never ask for upvotes.
- **Quora**: Answers must be substantive (300+ words for featured snippet
  eligibility). Disclose brand affiliation in the bio, not in every answer.
- **Facebook groups**: Many groups have "no promo" rules. Engagement posts,
  questions, and advice get engagement; product links get deleted.

## Output philosophy
Every piece of content must pass the "would a real person upvote/like/save
this?" test. If the primary value is promotional, rewrite it.
"""


class CommunityMarketingAgent(BaseAgent):
    """Reddit, Quora, and Facebook group community marketing agent."""

    name = "community_marketing"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Deliverable methods                                                 #
    # ------------------------------------------------------------------ #

    def build_reddit_strategy(self) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        target_audience = self.brand.get("target_audience", {})
        primary = target_audience.get("primary", "general consumers")
        pain_points = target_audience.get("pain_points", [])
        seed_keywords = self.brand.get("seed_keywords", [])
        reddit_communities = self.brand.get("reddit_communities", [])

        community_hint = ""
        if reddit_communities:
            community_hint = (
                "\n\nThe brand has identified these communities as relevant:\n"
                + "\n".join(f"- r/{c}" for c in reddit_communities)
            )

        return self.generate(
            f"""
Build a complete Reddit community marketing strategy for **{brand_name}**
— a {industry} brand targeting: {primary}.

Customer pain points: {", ".join(pain_points) if pain_points else "not specified"}
Content keywords: {", ".join(seed_keywords)}{community_hint}

## 1. Target Subreddit List (table)
A table: Subreddit | Subscribers | Relevance | Content Type That Works | Key Rules to Know | Promotional Allowed?

Include 10-15 subreddits across:
- High-relevance niche communities (where the exact target audience lives)
- Broader interest communities (lifestyle, sustainability, style, home)
- Question-based communities where expertise can be demonstrated (r/AskReddit style)

## 2. Account Setup and Karma-Building Plan
Step-by-step: how to build a legitimate Reddit presence before posting any
brand-relevant content. What to do in weeks 1-4 to reach a trusted account
status organically.

## 3. Content Pillars for Reddit
5 content pillars — the types of posts that add genuine value to each community
type. For each pillar: description, example post idea, subreddits it fits best.

## 4. Posting Cadence
Recommended frequency per subreddit type. When NOT to post (busy periods,
rule-restricted days). How to stagger posts to avoid looking like a bot.

## 5. Engagement Playbook
How to respond to comments, how to handle criticism, what to do when someone
mentions a competitor, how to handle someone asking where to buy something
similar to the brand's product (the golden opportunity).

## 6. Google SEO Bonus
Explain which post formats (listicles, how-tos, comparison questions) are most
likely to rank in Google from Reddit — and why this makes Reddit posts
"compound content" that keeps driving traffic for years.

## 7. Red Lines
5 specific things NEVER to do on Reddit for this brand — with brief
explanation of why each gets accounts banned or brands roasted.
"""
        )

    def write_reddit_posts(self, count: int = 8) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        seed_keywords = self.brand.get("seed_keywords", [])
        pain_points = (
            self.brand.get("target_audience", {}).get("pain_points", [])
        )

        return self.generate(
            f"""
Write {count} ready-to-post Reddit posts for **{brand_name}** — a {industry} brand.

Topic areas: {", ".join(seed_keywords)}
Customer pain points to address: {", ".join(pain_points) if pain_points else "not specified"}

Rules:
- Each post must stand alone as genuinely useful, even without any brand mention
- Brand mentions (if any) must feel natural, not promotional
- Posts must be value-first: tips, stories, questions, comparisons, or
  guides that the community would upvote regardless of brand affiliation
- Vary post types across the set

For each post:

### Post [N]: [Title]
**Subreddit:** r/[subreddit]
**Post Type:** [text / link / question / image description]
**Upvote Likelihood:** [High / Medium — with 1-line reason]
**Google Ranking Potential:** [High / Medium / Low — with 1-line reason]

**Title:**
[The exact post title — this is the SEO headline too]

**Body:**
[Full post text, formatted with Reddit markdown]

**Expected Engagement:** [what comments/discussion this will likely generate]

**Brand Connection:** [how this naturally relates to the brand without being promotional]

---

Vary the post types across: personal story/experience, how-to guide,
asking for opinions, sharing a resource, comparison question, "what I
learned after X" format, and community discussion starter.
"""
        )

    def write_quora_answers(self, count: int = 6) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        usp = self.brand.get("usp", [])
        seed_keywords = self.brand.get("seed_keywords", [])
        target_audience = self.brand.get("target_audience", {})
        primary = target_audience.get("primary", "general consumers")

        return self.generate(
            f"""
Write {count} Quora answers for **{brand_name}** — a {industry} brand.

Target audience: {primary}
Brand USPs: {", ".join(usp) if usp else "not specified"}
Keyword focus: {", ".join(seed_keywords)}

Each answer should:
- Be 300-600 words (long enough to earn featured snippet consideration)
- Answer the question completely without requiring the reader to click anywhere
- Mention the brand naturally in context (1-2 times max), not as the focus
- Be optimized for Google ranking: lead with a direct 1-2 sentence answer,
  then expand with supporting details, examples, and specifics
- Include a credentials/context line showing why the answerer knows this topic

For each answer:

### Answer [N]
**Question:** [The exact Quora question to answer]
**Search Intent:** [What someone Googling this question actually wants]
**Google Featured Snippet Potential:** [High/Medium + 1-line reason]
**Brand Mention Strategy:** [how/whether the brand is mentioned — or not]

**Full Answer:**

[Credentials line — 1 sentence establishing why this person knows the topic]

[Direct answer — 1-2 sentences that directly answer the question]

[Expanded answer — detailed, specific, genuinely helpful body]

[Practical tip or actionable takeaway]

[Closing — optional: related resource or invitation to ask follow-up]

---

Questions to cover: target real high-volume questions around the brand's
topic area (capsule wardrobes, ethical fashion, small space furniture,
streetwear sizing, etc.). Mix commercial-intent questions (best X for Y)
and informational questions (how to X, what is X).
"""
        )

    def build_facebook_group_strategy(self) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        target_audience = self.brand.get("target_audience", {})
        primary = target_audience.get("primary", "general consumers")
        pain_points = target_audience.get("pain_points", [])

        return self.generate(
            f"""
Build a Facebook group community marketing strategy for **{brand_name}**
— a {industry} brand targeting: {primary}.

Customer pain points: {", ".join(pain_points) if pain_points else "not specified"}

## 1. Target Group List
15 types of Facebook groups to join, ranked by relevance. For each:
- Group type description (with example group names to search for)
- Estimated audience overlap with the brand's target customer
- What type of content performs in this group
- Whether the group allows product mentions / links

## 2. Engagement Content Templates (10 templates)
10 Facebook group post templates that generate discussion and naturally
create opportunities to mention the brand. For each:
- Template category (question / tip / poll / story / resource share)
- Post text (ready to adapt and post)
- Where to use it (group types)
- How the brand connection emerges naturally in comments/discussion

## 3. Brand Group Launch Plan (Optional Own Group)
If the brand wants to create its own Facebook group (recommended for
fashion brands especially):
- Group name formula
- Group purpose / rules
- First 30-day content plan to get initial members engaged
- How to use the group for product research, UGC, and early access drops

## 4. Community Listening Setup
How to use Facebook groups (and Reddit) as FREE market research:
- What to search for to find brand mentions
- How to track competitor complaints (= your opportunity)
- How to identify the exact language customers use (= copy gold)

## 5. Cross-Platform Compounding
How Reddit + Quora + Facebook group activity compounds:
Reddit post → Google ranking → Quora answer links to blog → Blog links
to Pinterest pin → Pinterest drives product page traffic → email capture.
Show the full chain for this specific brand.
"""
        )

    def write_brand_voice_guide(self) -> str:
        brand_name = self.brand["name"]
        voice = self.brand.get("voice", {})
        tone = voice.get("tone", "friendly and helpful")
        avoid = voice.get("avoid", "")
        favorite_words = voice.get("favorite_words", [])

        return self.generate(
            f"""
Write a **Community Voice Guide** for the team members who will post on
behalf of **{brand_name}** in online communities.

Brand voice: {tone}
Words/phrases to avoid: {avoid}
Preferred language: {", ".join(favorite_words) if favorite_words else "not specified"}

## 1. Community vs. Brand Voice
How the brand voice adapts in community settings. The difference between
the voice on product pages vs. in Reddit comments vs. in Facebook groups.
(Community voice is always a little more casual and human than brand copy.)

## 2. The Authenticity Test
A 5-question checklist the team asks before posting anything. If any
question gets a "no", the post needs rewriting.

## 3. Platform-Specific Tone Adjustments
How the voice shifts slightly across:
- Reddit (most casual, most skeptical audience)
- Quora (more authoritative, informational)
- Facebook groups (warm, community-oriented)
- YouTube comments (brief, direct)

## 4. Dos and Don'ts by Scenario
Table format: Scenario | Do This | Don't Do This

Scenarios:
- Someone asks for product recommendations in our category
- Someone mentions a competitor positively
- Someone complains about a problem our product solves
- Someone shares negative press/news about the brand
- Someone asks if we're affiliated with the brand

## 5. How to Handle Criticism
A step-by-step response guide for when a community post or comment gets
negative pushback. What to say, what NOT to say, when to disengage.
"""
        )

    # ------------------------------------------------------------------ #
    # Default run                                                         #
    # ------------------------------------------------------------------ #
    def run(self, topic: str | None = None, **_: Any) -> dict[str, Any]:
        files = []

        print(f"  [{self.name}] Building Reddit strategy ...")
        reddit_strategy = self.build_reddit_strategy()
        files.append(str(self.save("reddit-strategy", reddit_strategy)))

        print(f"  [{self.name}] Writing Reddit posts ...")
        reddit_posts = self.write_reddit_posts(count=8)
        files.append(str(self.save("reddit-posts", reddit_posts)))

        print(f"  [{self.name}] Writing Quora answers ...")
        quora = self.write_quora_answers(count=6)
        files.append(str(self.save("quora-answers", quora)))

        print(f"  [{self.name}] Building Facebook group strategy ...")
        fb_strategy = self.build_facebook_group_strategy()
        files.append(str(self.save("facebook-group-strategy", fb_strategy)))

        print(f"  [{self.name}] Writing community brand voice guide ...")
        voice_guide = self.write_brand_voice_guide()
        files.append(str(self.save("community-voice-guide", voice_guide)))

        return {
            "agent": self.name,
            "files": files,
            "summary": (
                "Community marketing: Reddit strategy + 8 posts, 6 Quora answers, "
                "Facebook group strategy, community voice guide"
            ),
        }
