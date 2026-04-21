# Overloop Blog

Static HTML blog migrating from Webflow to GitHub Pages + Cloudflare reverse proxy.

## Project Overview

- **Goal**: Migrate the Overloop blog (overloop.com/blog) from Webflow to a self-hosted static HTML setup
- **Stack**: Pure static HTML, no build step. Python 3 for local server + utility scripts
- **Languages**: EN, DE, FR, ES (4 locales, 20 articles each = 80 total currently)
- **Status**: Staging (all pages have `noindex, nofollow` — remove before go-live)
- **Deployment**: GitHub Actions → GitHub Pages → Cloudflare reverse proxy at overloop.com

## Structure

```
blog/
  en/          English articles (20)
  de/          German articles (20)
  fr/          French articles (20)
  es/          Spanish articles (20)
assets/
  css/         overloop.css (design system)
  js/          blog.js (scroll progress, ToC)
  images/      logos/, og/, screenshots/, tools/
  nav.html     Navigation component
  footer.html  Footer component
  template.html Article template with {{VARIABLES}}
tools/         Interactive tools (empty, planned)
playbooks/     Industry playbooks (empty, planned)
templates/     Cold email & LinkedIn templates (empty, planned)
redirects/     redirects.csv (259+ mappings) + cloudflare-worker.js
```

## Local Development

```bash
./serve.sh
# Opens at http://localhost:8000/blog/en/
```

## Content Rules

### Tables on mobile
Tables with 15+ rows MUST have `class="table-keep"` to prevent card layout collapse on mobile.

### Image paths
- **GitHub Pages (preview)**: `/overloop-blog/assets/images/...`
- **Production (Cloudflare)**: `/assets/images/...`

### Internal links
- **GitHub Pages**: `/overloop-blog/blog/en/slug.html`
- **Production**: `/blog/slug`

### Logo filenames
Named by domain, not brand: `overloop.com.png`, `apollo.io.png`, `instantly.ai.svg`

### Author photo
File is `nicolas-finet.png` (not `.jpg`).

## Design System

- **Fonts**: Playfair Display (headings) + Inter (body)
- **Colors**: Violet palette (`#7C3AED` primary, `#2E1065` dark, `#F5F3FF` lightest)
- **CSS**: `assets/css/overloop.css` (25.9 KB)
- **Content width**: 780px max

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `audit.py` | Full HTML structure & SEO audit |
| `seo-audit.py` | Senior SEO compliance checks (crawlability, hreflang, schema, E-E-A-T) |
| `propagate-design.py` | Apply design system to DE/FR/ES articles |
| `fix-logo-paths.py` | Normalize logo filenames to domain-based naming |
| `inject-breadcrumbs.py` | Add breadcrumb bars to articles |
| `inject-design.sh` | Bash wrapper for CSS + nav + footer injection |

## Content Manifest

`content-manifest.json` contains the editorial roadmap (36 articles) with:
- 3 content pillars: Cold Email Mastery, AI Sales Tools, General
- Per-article: slug, keywords per language, search volume, GSC data, brief, internal links
- Priority grouping: W2 (week 2), W3 (week 3)

## Schema Markup

Every article includes JSON-LD for:
- `BlogPosting` (headline, author, dates, publisher)
- `BreadcrumbList` (Overloop / Blog / Article Title)
- `FAQPage` (when article has FAQ section)

## Available Skills (sl-seo plugin)

### Research & Planning
| Skill | Usage | What it does |
|-------|-------|-------------|
| `/seo-planner` | `full \| keyword \| gap \| quick-wins` | Orchestrates all research agents into ranked editorial plan |
| `/kw-researcher` | `[keyword] [--expand] [--trends] [--reddit] [--cluster]` | Deep keyword expansion, trend detection, Reddit pain mining |
| `/gap-analyst` | `[domain1] [domain2] ...` | Multi-competitor content gap analysis (intersection method) |
| `/gsc-miner` | `[--country XX] [--project-id N]` | Mine GSC for quick-win keyword opportunities |
| `/seo-intel` | `scan \| vs-matrix \| alert [domain]` | Competitor monitoring + comparison matrix generation |
| `/aeo-scout` | `[keyword \| full \| monitor]` | AI visibility monitoring (ChatGPT, Perplexity, Gemini, etc.) |

### Content Production
| Skill | Usage | What it does |
|-------|-------|-------------|
| `/content-machine` | `[domain \| keyword \| brief] [--dry-run]` | Full pipeline: research → write → publish |
| `/content-scorer` | `keyword1, keyword2, ...` | Score & rank keywords into publication-ready briefs |
| `/content-visual` | `<article-path> [--type X]` | Generate all visual assets (logos, screenshots, OG, video) |
| `/enrich-article` | `<path> [--deploy]` | Add logos, screenshots, pricing, schema to article HTML |
| `/content-publish` | `<article-path> [--slug X]` | Deploy article to GitHub Pages with template |
| `/ethan-smith-aeo` | `<url-or-path> [--fix]` | Audit article for Answer Engine Optimization |
| `/content-qa` | `<url-or-path> <keyword>` | Final gate: compare vs SERP top results |

### Pipeline Flow
```
seo-planner → content-scorer → content-machine → content-visual → enrich-article → content-publish → content-qa
```

## Go-Live Checklist

- [ ] Remove `noindex, nofollow` from all pages
- [ ] Switch image paths from `/overloop-blog/` to `/`
- [ ] Switch internal links from `/overloop-blog/blog/en/slug.html` to `/blog/slug`
- [ ] Uncomment hreflang tags in template
- [ ] Enable auto-deploy in `.github/workflows/deploy.yml` (change to `on: push`)
- [ ] Import `redirects/redirects.csv` into Cloudflare Workers bulk redirects
- [ ] Configure Cloudflare reverse proxy for overloop.com

## Auto-Learning (Mistakes to Avoid)

> This section tracks errors made during development so they are not repeated.
> Format: `- [DATE] CONTEXT: What went wrong → What to do instead`

- _No entries yet._
