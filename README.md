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
