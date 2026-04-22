"""
ConversionOptimizationAgent (CRO)
==================================

Traffic without conversion is just a vanity metric. This agent closes
the gap between visitors and orders by generating:

  • Product page copy — headline, bullet benefits, full description, FAQ
  • Trust signals — badges, guarantee copy, review request templates
  • Size & dimension guides — the #1 reason customers don't buy online
  • Checkout & cart reassurance copy — reduces abandonment before the
    email flow even fires
  • Google Shopping feed optimization guide — free product listings in
    Google Search, Google Images, and the Shopping tab

The agent is brand-aware: every output matches the brand's voice, USPs,
and target audience's specific purchase hesitations (pulled from the
pain_points in the brand config).
"""
from __future__ import annotations

from typing import Any

from .base import BaseAgent

ROLE_PROMPT = """
You are a conversion rate optimization (CRO) specialist for DTC e-commerce
brands. Your job is to make every touchpoint — from product page to checkout
— work harder so more visitors become buyers.

## Your expertise
- Product page copywriting: benefit-first headlines, scannable bullet
  benefits, objection-handling descriptions, compelling FAQs
- Trust architecture: what signals (badges, guarantees, review counts,
  certifications) actually move hesitant buyers and where to place them
- Size, fit, and dimension guides: the #1 reason online shoppers abandon —
  you write guides that eliminate guesswork and cut return rates
- Checkout and cart UX copy: micro-copy on buttons, progress bars,
  reassurance messages, and order-confirmation pages that prevent
  buyer's remorse and start the post-purchase relationship right
- Google Free Listings (Google Shopping organic): how to structure the
  product feed so products appear in Google Search, Images, and the free
  Shopping tab without spending a cent on ads
- Urgency and scarcity — only when real: you never fake low stock or
  false countdown timers; if scarcity is genuine, you surface it clearly

## Output philosophy
- Lead with the customer's desire, not the product's features
- Address the top 3 purchase hesitations specific to the brand's
  target audience in every product description
- Every CTA is specific: "Shop the Drop", "Find Your Size", "Build
  Your Room" — never just "Buy Now" or "Shop Now"
- Copy is scannable: short paragraphs, bullet lists, clear headers —
  most shoppers don't read, they scan
- Never fabricate reviews, testimonials, or certifications

## Formatting
Return clean, copy-paste-ready Markdown. Include a "Where to place this"
note for each copy block so a developer or Shopify editor knows exactly
where each element goes.
"""


class ConversionOptimizationAgent(BaseAgent):
    """Conversion rate optimization and product page copy agent."""

    name = "cro"
    role_prompt = ROLE_PROMPT

    # ------------------------------------------------------------------ #
    # Deliverable methods                                                 #
    # ------------------------------------------------------------------ #

    def optimize_product_page(self, product_name: str | None = None) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        usp = self.brand.get("usp", [])
        pain_points = (
            self.brand.get("target_audience", {}).get("pain_points", [])
        )
        voice = self.brand.get("voice", {})
        tone = voice.get("tone", "friendly and confident")
        product = product_name or f"flagship {industry} product"

        return self.generate(
            f"""
Write a complete, conversion-optimized product page for **{brand_name}**'s
**{product}** — a {industry} brand with a {tone} voice.

Brand USPs: {", ".join(usp) if usp else "not specified"}
Customer pain points to address: {", ".join(pain_points) if pain_points else "not specified"}

Deliver every element of the product page:

## 1. Page Title (SEO + conversion)
Format: [Keyword-rich name] | [Brand] — max 60 chars

## 2. Hero Headline
One line. Leads with the customer desire, not the product name.

## 3. Subheadline
One sentence. Handles the primary purchase hesitation.

## 4. Bullet Benefits (5-7 bullets)
Format: **[Bold benefit]** — [1-sentence elaboration]
Each bullet addresses a specific customer pain point or fear.

## 5. Full Product Description (200-300 words)
Story-driven, benefit-led, voice-on-brand. Weave in 1-2 keywords naturally.
End with a single specific CTA sentence.

## 6. Product FAQ (6-8 questions)
The real questions customers ask before they buy (sizing, materials,
care, shipping, returns, sustainability). Answers: 2-4 sentences each.

## 7. Trust Signal Block
List 4-6 trust elements with copy for each:
- Badge text (e.g. "Free returns within 30 days")
- Placement recommendation

## 8. Cross-sell / Upsell Hook
One line for a "Complete the Look" or "You Might Also Like" section.

## 9. SEO Meta Description (155 chars max)
Keyword-first, benefit-focused, includes a soft CTA.
"""
        )

    def write_trust_signals(self) -> str:
        brand_name = self.brand["name"]
        usp = self.brand.get("usp", [])
        industry = self.brand.get("industry", "retail")
        pain_points = (
            self.brand.get("target_audience", {}).get("pain_points", [])
        )

        return self.generate(
            f"""
Create a complete trust signal system for **{brand_name}** — a {industry} brand.

Brand USPs: {", ".join(usp) if usp else "not specified"}
Customer hesitations: {", ".join(pain_points) if pain_points else "not specified"}

## 1. Trust Badge Copy (8-10 badges)
For each badge:
- **Icon suggestion** (e.g., shield, lock, leaf, star)
- **Badge headline** (3-5 words)
- **Subtext** (1 line, optional)
- **Where to place** (product page hero / checkout / footer / cart)

## 2. Guarantee Statement
A 3-4 sentence paragraph for the returns/guarantee policy section that
turns the policy into a confidence builder, not a legal disclaimer.

## 3. Review Request Email (post-purchase)
A short, authentic email sent 14-21 days post-delivery asking for a review.
Subject line + preheader + body (4-6 sentences) + one CTA button.
Avoid begging or offering incentives (stay platform-compliant).

## 4. Social Proof Placement Map
Table: Page/Section | Social Proof Element | Ideal Format | Why It Works Here
Cover: homepage, product page, collection page, cart, checkout, confirmation page.

## 5. Urgency & Scarcity Templates
3-5 copy templates for REAL scarcity/urgency situations only:
- Low stock (< 5 units remaining)
- Limited edition / drop closing
- Seasonal sale ending
- Restock waitlist

## 6. "Why Us?" Section Copy
A 3-column comparison section (brand vs. fast fashion / mass market /
luxury) using only factual differentiators from the brand USPs.
"""
        )

    def write_size_and_fit_guide(self) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        target_audience = self.brand.get("target_audience", {})
        primary = target_audience.get("primary", "general audience")

        return self.generate(
            f"""
Write a complete size and fit guide (or dimension guide for furniture) for
**{brand_name}** — a {industry} brand whose primary customer is: {primary}.

This guide will live as:
1. A dedicated /size-guide page
2. A pop-up or drawer on every product page
3. A FAQ section on product pages

## For fashion brands — include:
### 1. How to Measure (with diagram copy)
Step-by-step text instructions for bust/chest, waist, hips, inseam, torso
(with note: "tip: measure over your underwear, not over clothing").

### 2. Size Chart
A Markdown table: Size | US | UK | EU | Bust | Waist | Hip | Height
Include XS-4XL if size-inclusive is a USP. Add a "Between sizes? Size up
for [brand's fit philosophy]" note.

### 3. Fit Descriptions by Style
For each major product category (tops, bottoms, dresses, outerwear):
Describe the fit (relaxed / true-to-size / slim) and give a "model wears"
example: "Model is 5'8", wears a size M."

### 4. Fabric Behavior Note
2-3 sentences per fabric: does it stretch? shrink after wash? feel stiff
at first? This pre-handles a top return reason.

### 5. "Still unsure?" CTA
One line pointing to live chat, email, or the customer care link.

## For furniture brands — include:
### 1. How to Measure Your Space
Room layout tips: traffic flow clearances, sofa-to-coffee-table distance,
rug sizing formula, doorway clearance check.

### 2. Product Dimensions Template
A fill-in table structure for each product: Overall W × D × H | Seat H |
Arm H | Leg H | Clearance needed for delivery.

### 3. Small Space Tips
5-7 tips specific to the brand's target (small apartments, first homes).

### 4. Delivery Access Checklist
A printable checklist customers fill in before ordering to confirm the
piece fits through their building. Reduces delivery refusals.
"""
        )

    def write_checkout_reassurance(self) -> str:
        brand_name = self.brand["name"]
        usp = self.brand.get("usp", [])
        voice = self.brand.get("voice", {})
        tone = voice.get("tone", "friendly and confident")

        return self.generate(
            f"""
Write the complete checkout and cart micro-copy for **{brand_name}**
— {tone} voice — to reduce abandonment at every step.

Brand USPs (to echo in reassurance copy): {", ".join(usp) if usp else "not specified"}

## 1. Cart Page Elements
- **Cart headline** (instead of generic "Your Cart")
- **Empty cart message** — friendly, not sad; includes a CTA
- **Order summary label** — what to call the sidebar total block
- **Shipping threshold progress bar text** — e.g., "Add $X more for free shipping"
- **Trust strip under cart** — 3-4 mini trust icons with text
- **"Checkout" button micro-copy** — the text on and below the CTA button

## 2. Checkout Step Micro-copy
### Step 1: Contact Info
- Page headline
- Email field label + helper text (why we ask for it)
- Newsletter opt-in checkbox label

### Step 2: Shipping
- Page headline
- Address field labels (any helpful hints)
- Shipping method labels + delivery estimate copy

### Step 3: Payment
- Page headline
- Security reassurance line (appears near card fields)
- "Complete Order" button text + the line beneath it

## 3. Order Confirmation Page
- Headline (not "Thank you for your order" — something on-voice)
- 3-4 sentences: what happens next, what they'll receive, how to reach support
- "What's next" timeline: Order confirmed → Processing → Shipped → Delivered
- One soft invite (share on social, join the community, or refer a friend)

## 4. Abandoned Cart Email — Subject Lines (10 options)
Just subject lines + preheaders. The email body is handled by the Email
Marketing Agent. Vary tone: curious, reminder, FOMO, helpful, witty.

## 5. Exit-Intent Pop-up Copy (for cart/checkout pages)
Headline + 1-2 sentences + CTA button text. Offer: email capture for
"save your cart" — NOT a discount (protect margin). Two variations: one
for new visitors, one for returning visitors.
"""
        )

    def write_google_shopping_guide(self) -> str:
        brand_name = self.brand["name"]
        industry = self.brand.get("industry", "retail")
        website = self.brand.get("website", "yourwebsite.com")

        return self.generate(
            f"""
Write a complete setup guide for **Google Free Listings** (Google Shopping
organic) for **{brand_name}** — a {industry} e-commerce brand at {website}.

This is 100% free. Google surfaces products in:
- The "Shopping" tab in Google Search
- Google Images (with price + store overlay)
- Google Search results (as product carousels)
- Google Lens results

## Guide sections:

### 1. What Free Listings Are (and Aren't)
2-3 sentences clarifying the difference between free listings and paid
Shopping Ads — so the team knows they're setting up the free version.

### 2. Step-by-Step Setup
1. Google Merchant Center account creation
2. Website claim (meta tag OR DNS record)
3. Business information: shipping, returns, tax (US) settings
4. Product feed creation — required attributes:
   - id, title, description, link, image_link, price, availability,
     condition, brand, gtin/mpn, google_product_category
5. Feed submission and review timeline
6. Enabling "Surfaces across Google" (the free listings toggle)
7. Linking to Google Search Console (recommended)

### 3. Feed Optimization for {industry.title()}
Title formula: [Brand] + [Key Attribute] + [Product Type] + [Size/Color]
Example for each product category the brand sells.

Description best practices: keyword-first sentence, key specs, material/
construction, size range, and one differentiating claim.

### 4. Product Category Taxonomy
The correct google_product_category ID numbers for this brand's main
product types. (Use the official Google taxonomy.)

### 5. Common Rejection Reasons and Fixes
Top 6 disapproval reasons and the exact fix for each.

### 6. Performance Monitoring (Free Tools Only)
How to track impressions, clicks, and attributed revenue using:
- Merchant Center Performance dashboard
- Google Search Console (linked)
- GA4 (UTM-tagged feed URLs)

### 7. Ongoing Feed Health
What to update and when: price changes, new products, out-of-stock
handling, seasonal title updates.
"""
        )

    # ------------------------------------------------------------------ #
    # Default run                                                         #
    # ------------------------------------------------------------------ #
    def run(self, topic: str | None = None, **_: Any) -> dict[str, Any]:
        files = []

        print(f"  [{self.name}] Optimizing product page copy ...")
        product_page = self.optimize_product_page(product_name=topic)
        files.append(str(self.save("product-page-copy", product_page)))

        print(f"  [{self.name}] Building trust signal system ...")
        trust = self.write_trust_signals()
        files.append(str(self.save("trust-signals", trust)))

        print(f"  [{self.name}] Writing size and fit guide ...")
        size_guide = self.write_size_and_fit_guide()
        files.append(str(self.save("size-fit-guide", size_guide)))

        print(f"  [{self.name}] Writing checkout reassurance copy ...")
        checkout = self.write_checkout_reassurance()
        files.append(str(self.save("checkout-reassurance", checkout)))

        print(f"  [{self.name}] Writing Google Shopping setup guide ...")
        shopping = self.write_google_shopping_guide()
        files.append(str(self.save("google-shopping-guide", shopping)))

        return {
            "agent": self.name,
            "files": files,
            "summary": (
                "CRO outputs: product page copy, trust signals, size/fit guide, "
                "checkout micro-copy, Google Free Listings setup guide"
            ),
        }
