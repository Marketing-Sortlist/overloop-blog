# Overloop Blog

Static HTML blog, tools & playbooks served via GitHub Pages + Cloudflare reverse proxy.

## Plan

Full migration plan: [Notion — Overloop SEO Migration](https://www.notion.so/33e48f1b12ff812c9ceaf6e1bf650398)

## Structure

```
blog/
  en/          Articles (English)
  de/          Articles (German)
  fr/          Articles (French)
  es/          Articles (Spanish)
tools/         Interactive tools (spam checker, ROI calculator, etc.)
playbooks/     Industry-specific outbound playbooks
templates/     Cold email & LinkedIn templates
redirects/     301 redirect mapping for Cloudflare Workers
assets/        CSS, fonts, images shared across all pages
```

## How to publish

1. Create or edit an HTML file in the right folder
2. Commit and push to `main`
3. GitHub Actions deploys automatically
4. Cloudflare serves it at `overloop.com/blog/*`, `/tools/*`, `/playbooks/*`

## Content production

Use Claude Code with the `/content-machine` skill:

```bash
# Produce an article in all 4 languages
/content-machine "ai bdr tools" --langs en,de,fr,es

# Produce a template page
/content-machine "cold email template for SaaS" --type template
```

Each article follows the E-E-A-T template in `assets/template.html`.

## Redirect map

`redirects/redirects.csv` contains all 259+ URL mappings.
Import into Cloudflare Workers bulk redirects.

---

## Content Rules (MUST FOLLOW)

### Tables on mobile

**Every table with 15+ rows MUST have `class="table-keep"`.**

Without it, tables become stacked card layout on mobile (good for 5-10 row comparison tables, catastrophic for 300-row word lists).

```html
<!-- GOOD: Dense word list stays as compact scrollable table -->
<table class="table-keep">

<!-- GOOD: Small comparison table becomes cards on mobile (default) -->
<table>
```

Articles that ALWAYS need `table-keep` on all tables:
- `500-trigger-words.html` (1000+ words in tables)
- `455-email-spam-trigger-words-avoid-2018.html` (600+ words in tables)
- `cold-email-stats-2018.html` (stats tables)

### Image paths

**Preview (GitHub Pages):** All paths use `/overloop-blog/` prefix.
```html
<img src="/overloop-blog/assets/images/logos/overloop.com.png">
```

**Production (Cloudflare):** Paths use `/` directly.
```html
<img src="/assets/images/logos/overloop.com.png">
```

When switching to prod, run: `sed -i 's|/overloop-blog/|/|g' blog/**/*.html`

### Internal links

**Preview (GitHub Pages):**
```html
<a href="/overloop-blog/blog/en/slug.html">
```

**Production (Cloudflare):**
```html
<a href="/blog/slug">
```

### Logo filenames

Logos are named by domain, not by brand:
- `overloop.com.png` (not `overloop-logo.png`)
- `apollo.io.png` (not `apollo-logo.png`)
- `instantly.ai.svg` (not `instantly-logo.svg`)

### noindex for preview

All pages currently have `<meta name="robots" content="noindex, nofollow">`.
**MUST be removed before going live on overloop.com.**

### Author photo

The file is `nicolas-finet.png` (not `.jpg`). All articles reference `.png`.

### Design system

- Font: Playfair Display (headings) + Inter (body)
- Colors: violet palette (#7C3AED primary)
- CSS: `/assets/css/overloop.css`
- Nav: `/assets/nav.html`
- Footer: `/assets/footer.html`
- JS: `/assets/js/blog.js` (scroll progress, ToC active state)
