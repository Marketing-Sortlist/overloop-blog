# BRIEFING: Blog Templates Project — Import into other Claude session

Copy-paste this entire file into your other Claude Code session to transfer all context.

---

## Context

We're building 15 HTML templates for the Overloop blog (overloop.com/blog). The blog was migrated from Webflow to static HTML on GitHub Pages (repo: sortlist/overloop-blog). We have 865 articles planned in the content calendar.

The design system is based on the Webflow landing page (canonical):
- Primary: #6366F1 (indigo) → #A855F7 (purple) gradient
- Fonts: Epilogue (sans) + Playfair Display italic (accent) + JetBrains Mono (code/stats)
- Design system doc: `/Users/tanguy/Downloads/overloop-design-system/design-system-overloop.md`
- Tokens CSS: `/Users/tanguy/Downloads/overloop-design-system/tokens.css`

## Template #1 (DONE): Best Tools Listicle

File: `/Users/tanguy/Downloads/overloop-design-system/templates-v2/best-tools.html`
Example article: best-ai-sales-tools (198 articles planned with this template)

### What's built:
- Hero with gradient background, category pill, H1 with Playfair italic accent
- Author meta: avatar, name, role, publish date, updated date, read time
- "Tested by 3 experts" banner (3 overlapping photos + stats)
- Author intro section: Vincenzo's photo + name + role + bio text (replaces anonymous "I run two B2B companies...")
- Sticky TOC with scroll-spy
- Tool cards: featured (Overloop only, violet border) + normal
- Each tool: logo, rank, G2 rating, "best for" tag, description, pros/cons, pricing
- Case study block: dark card with +47% metric
- Expert callouts: named expert with photo replacing anonymous "Pro tip"
- Methodology section: gradient bg, pill badges, expandable details
- TL;DR comparison table (responsive, featured row)
- Category jump pills (horizontal scroll nav)
- FAQ accordion (native details/summary)
- CTA blocks: inline mid-article + dark end-of-article
- "Compare with Overloop →" links on competitor tool cards
- Expert panel at bottom: 3 full bios with photos + LinkedIn
- Reading progress bar

### Design decisions (apply to ALL templates):
- Featured card = Overloop only (no other tools get violet border)
- Pro tips = named expert with photo, NOT anonymous
- TL;DR summary card = REMOVED (redundant, replaced by author intro)
- Update log = will be automated via cron agent (monthly pricing checks)

## 3 Experts (used across all templates for E-E-A-T)

**Vincenzo Ruggiero** — CEO, Overloop
- Photo: https://cdn.prod.website-files.com/684167ac317862f3216bcd82/686cd1f2480e7dca3a497cbc_vincenzo.avif
- LinkedIn: https://www.linkedin.com/in/vincenzor/
- Bio: "Founded Overloop in 2015 as Prospect.io. 10+ years building sales automation. Personally tests every competitor tool."

**Nicolas Finet** — CEO & Co-founder, Sortlist & Overloop
- Photo: https://sortlist.github.io/overloop-blog/assets/images/nicolas-finet.png
- LinkedIn: https://www.linkedin.com/in/nifinet/
- Bio: "Co-founded Sortlist in 2014. Designed outbound systems for 500+ B2B companies. Deep expertise in cold email, LinkedIn automation, multichannel."

**Nathalie Saikali** — Customer Success Manager, Overloop
- Photo: https://cdn.prod.website-files.com/684167ac317862f3216bcd82/6878e35bb2fbe24081c32dec_nathalie.avif
- LinkedIn: https://www.linkedin.com/in/nathalie-saikali/
- Bio: "Works daily with sales teams deploying Overloop. Sees firsthand what moves the needle. Hundreds of customer conversations."

## 15 Templates to Build

| # | Template | Articles | Status | Priority |
|---|----------|----------|--------|----------|
| 1 | Best Tools Listicle | 198 | ✅ V2 DONE | P0 |
| 2 | Alternatives | 10 | Onze V1 → needs V2 | P2 |
| 3 | Pillar / Ultimate Guide | 288 | TO BUILD | P0 |
| 4 | How-To Tutorial | 40 | TO BUILD | P1 |
| 5 | X vs Y | 28 | V1 done → needs V2 | P2 |
| 6 | Templates & Swipe Files | 101 | TO BUILD | P1 |
| 7 | Data List / Directory | 53 | TO BUILD | P1 |
| 8 | Statistics & Benchmarks | 13 | TO BUILD | P3 |
| 9 | Best Agency Roundup | 34 | TO BUILD | P1 |
| 10 | Strategy / Playbook | 21 | TO BUILD | P2 |
| 11 | Lead Gen for X Business | 16 | TO BUILD | P3 |
| 12 | What is X? (Definition) | 11 | TO BUILD | P3 |
| 13 | Role-Based Guide | 11 | TO BUILD | P3 |
| 14 | Tactical Articles | 38 | TO BUILD | P2 |
| 15 | Tool Review (Single) | 3 | Onze V1 → needs V2 | P3 |

## Content calendar mapping (column O → template #)

| Calendar type | Template |
|---|---|
| Best tool for X | #1 |
| Alternatives to X | #2 |
| Pillar / ultimate guide | #3 |
| How-to tutorial | #4 |
| X vs Y | #5 |
| Templates & swipe file — * (all variants) | #6 |
| Data list / directory | #7 |
| Statistics & benchmarks | #8 |
| Best service / agency roundup | #9 |
| Strategy / playbook | #10 |
| Lead gen for X business | #11 |
| What is X? (definition pillar) | #12 |
| Role-based guide | #13 |
| Tactical article — * (all variants) | #14 |
| (single tool reviews) | #15 |

## Template-specific features (summary)

### #3 Pillar / Ultimate Guide (288 articles — TOP PRIORITY)
- Chapter navigation with progress tracking
- Sub-TOC per chapter, key takeaways per section
- Downloadable checklist/PDF CTA
- Expert quotes scattered throughout
- Internal links to related articles per section

### #6 Templates & Swipe Files (101 articles)
- Copyable template cards (one-click copy)
- Category tabs (email, LinkedIn, follow-up)
- Variables highlighted in templates
- Performance stats per template
- Download all as PDF CTA

### #7 Data List / Directory (53 articles)
- Searchable/filterable table
- Categories/tags for filtering
- "table-keep" for mobile
- Export/download CTA

### #9 Best Agency Roundup (34 articles)
- Like Best Tools but for agencies
- Agency cards: logo, specialties, pricing, location
- Overloop as self-serve alternative

### #4 How-To Tutorial (40 articles)
- Numbered steps with gradient circles
- Prerequisites, time-to-complete
- Screenshot placeholders per step

## Files & repos

- Blog repo: `sortlist/overloop-blog` (GitHub Pages)
- Worker repo: `sortlist/overloop-ai-cloudflare-worker` (auto-deploy)
- Tools repo: `sortlist/overloop-tools` (separate, proxied via Worker)
- Design system: `/Users/tanguy/Downloads/overloop-design-system/`
- Template V2 (done): `/Users/tanguy/Downloads/overloop-design-system/templates-v2/best-tools.html`
- Content calendar: https://docs.google.com/spreadsheets/d/1bnWo-B0r9CCOEZn0FzqYYAL4vPtDiQmaNkf2kt_7aYk/edit?gid=1672227751
- Notion initiative: https://www.notion.so/sortlist/generate-templates-for-blog-34c48f1b12ff805d8d89d22e03f6e711

## Feedback applied on Template #1

1. Customer outcome block: metric 54px + glow, text 16px, border-left violet — more readable
2. Pro tips → expert callouts with photo + name + role (rotate 3 experts)
3. Featured card = Overloop ONLY (removed from Lavender)
4. "Tested by 3 experts" banner with overlapping photos
5. "Compare with Overloop →" links on competitor cards
6. Methodology section more prominent (gradient, pills, expandable)
7. Expert panel at bottom (3 cards with full bios + LinkedIn)
8. TL;DR summary card DELETED (replaced by author intro)
9. Author intro section with Vincenzo photo + bio before the "I run two B2B companies" text
10. Nicolas photo: use CDN URL https://sortlist.github.io/overloop-blog/assets/images/nicolas-finet.png
11. "Tested by" banner recolored from green → brand violet/indigo
