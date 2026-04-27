# Blog Templates System — Overloop (2026)

> **For Notion:** copy-paste this file into https://www.notion.so/sortlist/generate-templates-for-blog-34c48f1b12ff805d8d89d22e03f6e711
> Notion MCP is currently disconnected, so this doc was generated locally.

---

## The idea in one paragraph

We've built **15 reusable HTML templates** for the Overloop blog, covering **100% of the 937 articles** planned for 2026 (862 new + 75 already published). Each template is a standalone HTML file with the Overloop design system baked in (indigo → purple gradient, Epilogue + Playfair typography, JSON-LD schemas, AEO-ready structure). The promise: every article — whether writer-crafted or AI-generated — gets dropped into the right template and produces a consistent, on-brand page with zero design decisions left to authors.

## Why this matters

1. **Consistency:** no more 15 different ways to present a "best X tools" article. One template, one opinion, one UX.
2. **Speed:** writers stop designing and start writing. AI agents can auto-route articles to templates via column O in the content calendar.
3. **SEO + AEO compound:** every template includes Article, FAQPage, HowTo, Review, or DefinedTerm JSON-LD — optimized for LLM citation (ChatGPT, Perplexity, Claude, Gemini).
4. **Migration path for 75 legacy articles:** existing Webflow-era articles can be re-routed into V2 templates without rewriting content.

---

## The 15 templates — coverage summary

| # | Template | New articles | Legacy articles | **Total** |
|---|---|---:|---:|---:|
| 1 | Best Tools Listicle | 198 | 15 | **213** |
| 2 | Alternatives to X | 10 | 5 | **15** |
| 3 | Pillar / Ultimate Guide | 288 | 22 | **310** |
| 4 | How-To Tutorial | 40 | 7 | **47** |
| 5 | X vs Y | 28 | 2 | **30** |
| 6 | Templates & Swipe Files | 101 | 2 | **103** |
| 7 | Data List / Directory | 53 | 2 | **55** |
| 8 | Statistics & Benchmarks | 13 | 2 | **15** |
| 9 | Best Agency Roundup | 34 | 0 | **34** |
| 10 | Strategy / Playbook | 21 | 1 | **22** |
| 11 | Lead Gen for X Business | 16 | 0 | **16** |
| 12 | What is X? (Definition) | 11 | 0 | **11** |
| 13 | Role-Based Guide | 11 | 0 | **11** |
| 14 | Tactical Articles | 38 | 17 | **55** |
| 15 | Tool Review (Single) | 3 | 0 | **3** |
| | **Total** | **865** | **75** | **940** |

> Note: "New" = planned in content calendar 2026; "Legacy" = already published on overloop.com (sitemap crawl 2026-04-24). Total slightly exceeds 937 due to overlap counting on the Templates/Swipe Files sub-variants.

## Top 3 templates cover 66% of the pipeline

- **Pillar / Ultimate Guide** (33%) — broad head-term authority content
- **Best Tools Listicle** (22%) — buyer's guide format, editor's pick = Overloop
- **Templates & Swipe Files** (11%) — copy-paste assets (cold email, LinkedIn, subject lines)

Build these 3 right and you've covered the biggest volume immediately.

---

## Template-to-column mapping

In the [Content calendar 2026 sheet](https://docs.google.com/spreadsheets/d/1bnWo-B0r9CCOEZn0FzqYYAL4vPtDiQmaNkf2kt_7aYk/edit?gid=1672227751), column O (`TEMPLATE`) assigns each row to a template. Legacy articles appended at rows 864-938 have `Status = Already Published` and `FROM = Sitemap crawl 2026-04-24`.

Swipe-file sub-variants use em-dash format: `Templates & swipe file — Email templates`, `Templates & swipe file — Subject lines`, etc. (5 sub-types). Tactical sub-variants: `Tactical article — Tips`, `— Best practices`, `— Mistakes to avoid`, etc. (13 sub-types).

## Design system foundations

- **Colors:** Primary `#6366F1` (indigo-500), Secondary `#A855F7` (purple-500), gradient `linear-gradient(135deg, #6366F1 → #A855F7)`. Canonical source: Webflow landing page (overloop.com).
- **Typography:** Epilogue (sans, 400-800) + Playfair Display italic (accent) + JetBrains Mono (code/stats).
- **Shared components:** reading progress bar, author intro card, expert callouts (Vincenzo / Nicolas / Nathalie), FAQ accordion with `<details>/<summary>`, sticky TOC with scroll-spy, JSON-LD schemas, mid-article CTAs, dark end-of-article CTA, newsletter capture, related articles, footer.
- **Tested-by banner:** kept on 5 product-comparison templates (Best Tools, Alternatives, X vs Y, Best Agency, Tool Review), removed from the other 10 (informational/strategic content).

## Template library location

Local repo: `/Users/tanguy/Documents/overloop-design-system/templates-v2/`

```
templates-v2/
├── best-tools.html
├── alternatives.html
├── pillar-guide.html
├── how-to.html
├── versus.html
├── swipe-files.html
├── data-list.html
├── statistics.html
├── best-agency.html
├── strategy.html
├── lead-gen-industry.html
├── what-is.html
├── role-guide.html
├── tactical.html
└── tool-review.html
```

Each template ships with:
- Full working HTML (open directly in browser, no build step)
- Embedded CSS (25-30KB per file)
- Lucide icons via CDN
- Vanilla JS (reading progress, TOC scroll-spy, copy-to-clipboard where relevant)
- JSON-LD schemas (Article / FAQPage / HowTo / Review / DefinedTerm)

Full design system tokens: `/Users/tanguy/Documents/overloop-design-system/tokens.css`
Full design system doc: `/Users/tanguy/Documents/overloop-design-system/design-system-overloop.md`

---

## Roadmap

**Phase 1 — Templates ✅ (DONE, Apr 2026)**
- 15 V2 templates built and visually validated
- Design system extracted from Webflow landing
- 100% of content calendar covered

**Phase 2 — Legacy migration (IN PROGRESS)**
- POC: 5 legacy articles migrated to V2 in `blog/_v2/` folder
- Validation: compare V2 rendering vs Webflow originals
- Full batch: 75 legacy articles migrated in one pass if POC validates

**Phase 3 — New content production (UPCOMING)**
- AI-assisted content generation per template type
- Auto-route articles from content calendar → correct V2 template
- Scale to 865 new articles across Q3-Q4 2026

---

## Key people

- **Content strategy:** Damien (agency Onze context), Tanguy (SEO lead)
- **Product + brand:** Vincenzo (CEO, Overloop), Nicolas (CEO Sortlist & Overloop)
- **Customer insights:** Nathalie (Customer Success Manager, Overloop)

The 3 experts rotate through author-intro cards and expert callouts for E-E-A-T signals (Google + LLM citation optimization).

---

## Links

- [Content calendar 2026 (Google Sheets)](https://docs.google.com/spreadsheets/d/1bnWo-B0r9CCOEZn0FzqYYAL4vPtDiQmaNkf2kt_7aYk/edit?gid=1672227751)
- [GSC opportunities tab](https://docs.google.com/spreadsheets/d/1bnWo-B0r9CCOEZn0FzqYYAL4vPtDiQmaNkf2kt_7aYk/edit?gid=607926645)
- Blog repo: `sortlist/overloop-blog`
- Design system repo: `/Users/tanguy/Documents/overloop-design-system/`
- Templates V2: `/Users/tanguy/Documents/overloop-design-system/templates-v2/` (15 files)
