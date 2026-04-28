#!/usr/bin/env python3
"""
migrate-locales-v2.py — Migrate locale blog articles (FR/DE/ES/IT) from V1 to V2 design.

Extracts metadata + body content from each V1 locale article,
wraps in the V2 shell (inline CSS, Epilogue font, V2 nav/footer).

Usage:
    python3 migrate-locales-v2.py                    # migrate all locales
    python3 migrate-locales-v2.py --dry-run           # preview without writing
    python3 migrate-locales-v2.py --locale fr         # only French
    python3 migrate-locales-v2.py --file blog/fr/X.html  # single file
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from html import unescape

BLOG_DIR = Path(__file__).parent / "blog"
LOCALES = ["fr", "de", "es", "it"]
# Reference EN article to extract V2 CSS shell (must have ALL component CSS: tested-banner, tool-card, etc.)
REFERENCE_EN = BLOG_DIR / "best-ai-sales-tools.html"


# ─── V2 Shell extraction ─────────────────────────────────────────────────────

def extract_v2_shell():
    """Extract the V2 CSS, nav, footer, and scripts from a reference EN article."""
    html = REFERENCE_EN.read_text(encoding="utf-8")
    shell = {}

    # Style block (line 20 to ~397)
    m = re.search(r'(<style>.*?</style>)', html, re.DOTALL)
    shell["style"] = m.group(1) if m else ""

    # Nav
    m = re.search(r'(  <nav class="nav">.*?</nav>)', html, re.DOTALL)
    shell["nav"] = m.group(1) if m else ""

    # Footer
    m = re.search(r'(    <footer class="footer">.*?</footer>)', html, re.DOTALL)
    shell["footer"] = m.group(1) if m else ""

    # Scripts (after footer, before </body>)
    footer_end = html.find("</footer>")
    body_end = html.find("</body>")
    if footer_end > 0 and body_end > 0:
        shell["scripts"] = html[footer_end + len("</footer>"):body_end].strip()
    else:
        shell["scripts"] = ""

    return shell


# ─── Metadata extraction ─────────────────────────────────────────────────────

def extract_meta(html):
    """Extract metadata from a V1 locale article."""
    meta = {}

    # Lang
    m = re.search(r'<html\s+lang="([^"]*)"', html)
    meta["lang"] = m.group(1) if m else "en"

    # Title
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    meta["title_tag"] = unescape(m.group(1).strip()) if m else ""

    # Meta description
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.DOTALL)
    meta["description"] = m.group(1).strip() if m else ""

    # Canonical
    m = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', html)
    meta["canonical"] = m.group(1) if m else ""

    # Hreflang tags
    hreflang_tags = re.findall(
        r'(<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>)', html
    )
    meta["hreflang_tags"] = "\n    ".join(hreflang_tags)

    # OG tags
    og_tags = re.findall(r'(<meta\s+property="og:[^"]*"\s+content="[^"]*"\s*/?>)', html)
    meta["og_tags"] = "\n    ".join(og_tags)

    # Twitter tags
    twitter_tags = re.findall(r'(<meta\s+name="twitter:[^"]*"\s+content="[^"]*"\s*/?>)', html)
    meta["twitter_tags"] = "\n    ".join(twitter_tags)

    # JSON-LD
    jsonld_blocks = re.findall(
        r'(<script type="application/ld\+json">.*?</script>)', html, re.DOTALL
    )
    meta["jsonld"] = "\n    ".join(jsonld_blocks)

    # Extract author + dates from JSON-LD
    meta["author_name"] = ""
    meta["date_published"] = ""
    meta["date_modified"] = ""
    for block in jsonld_blocks:
        try:
            json_str = re.search(r"<script[^>]*>(.*?)</script>", block, re.DOTALL).group(1)
            data = json.loads(json_str)
            if data.get("@type") in ("BlogPosting", "Article"):
                meta["author_name"] = data.get("author", {}).get("name", "")
                meta["date_published"] = data.get("datePublished", "")
                meta["date_modified"] = data.get("dateModified", "")
        except (json.JSONDecodeError, AttributeError):
            continue

    # Fallbacks
    if not meta["author_name"]:
        m = re.search(r'Par\s+<a[^>]*>([^<]+)</a>', html)
        if m:
            meta["author_name"] = m.group(1).strip()
        else:
            meta["author_name"] = "Nicolas Finet"

    # Headline (clean title)
    meta["headline"] = meta["title_tag"].replace(" | Overloop", "")

    return meta


def extract_body(html):
    """Extract the article body content from a V1 locale article."""
    # Pattern 1: <article class="article-content">...</article>
    m = re.search(
        r'<article\s+class="article-content"[^>]*>\s*(.*?)\s*</article>',
        html, re.DOTALL
    )
    if m:
        return m.group(1).strip()

    # Pattern 2: any <article>...</article>
    m = re.search(r'<article[^>]*>\s*(.*?)\s*</article>', html, re.DOTALL)
    if m:
        return m.group(1).strip()

    # Pattern 3: <main class="article-body">...<div class="container">...content...</div>...</main>
    m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if m:
        content = m.group(1).strip()
        # Strip container div and article-meta/author-bio/cta-box wrappers
        content = re.sub(r'<div class="container">\s*', '', content)
        content = re.sub(r'\s*</div>\s*$', '', content)
        content = re.sub(r'<div class="article-meta">.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="cta-box">.*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="author-bio">.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        return content.strip()

    return ""


def generate_toc(body):
    """Generate TOC from H2 headings in the body content."""
    headings = re.findall(r'<h2[^>]*(?:id="([^"]*)")?[^>]*>(.*?)</h2>', body, re.DOTALL)
    items = []
    ch = 1
    for h_id, h_text in headings:
        text = re.sub(r'<[^>]+>', '', h_text).strip()
        if not text or len(text) > 80:
            continue
        # Generate ID if missing
        if not h_id:
            h_id = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
        short = text if len(text) <= 40 else text[:37] + '…'
        items.append(f'          <li><a href="#{h_id}"><span class="ch-num">{ch:02d}</span> {short}</a></li>')
        ch += 1

    if not items:
        return ""

    return "\n".join(items)


def ensure_h2_ids(body):
    """Add IDs to H2 headings that don't have them."""
    def add_id(match):
        tag_open = match.group(1)
        text = match.group(2)
        if 'id="' in tag_open:
            return match.group(0)
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        h_id = re.sub(r'[^a-z0-9]+', '-', clean_text.lower()).strip('-')
        return f'<h2{tag_open} id="{h_id}">{text}</h2>'

    return re.sub(r'<h2([^>]*)>(.*?)</h2>', add_id, body, flags=re.DOTALL)


def format_date(date_str):
    """Convert 2024-09-12 to Sep 12, 2024."""
    if not date_str:
        return ""
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except ValueError:
        return date_str


def author_initials(name):
    parts = name.split()
    return "".join(p[0].upper() for p in parts if p)[:2]


def get_author_bio(name):
    """Get author bio for the author card."""
    bios = {
        "Nicolas Finet": ("CEO & Co-founder, Sortlist & Overloop",
                          "Co-founded Sortlist in 2014. Designed outbound systems for 500+ B2B companies across Europe."),
        "Vincenzo Ruggiero": ("CEO, Overloop",
                              "Founded Overloop in 2015. Tests every competitor tool hands-on."),
        "Nathalie Saikali": ("Customer Success Manager, Overloop",
                             "Works daily with sales teams deploying Overloop across industries."),
        "Jazmin Villarino": ("Contributing Writer at Overloop",
                             "Covering outbound sales and cold email best practices."),
    }
    role, bio = bios.get(name, ("Contributing Writer at Overloop",
                                "Covering outbound sales and cold email best practices."))
    return role, bio


# ─── Article builder ─────────────────────────────────────────────────────────

def build_v2_article(filepath, shell):
    """Build a V2 article from a V1 locale article."""
    html = filepath.read_text(encoding="utf-8")
    meta = extract_meta(html)
    body = extract_body(html)

    if not body:
        return None, "empty body"

    # Add IDs to H2 headings
    body = ensure_h2_ids(body)

    # Generate TOC
    toc_items = generate_toc(body)

    # Date display
    pub_date = format_date(meta["date_published"])
    mod_date = format_date(meta["date_modified"])
    dates_display = pub_date
    if mod_date and mod_date != pub_date:
        dates_display += f" &middot; Updated {mod_date}"

    # Author
    initials = author_initials(meta["author_name"])
    author_role, author_bio = get_author_bio(meta["author_name"])

    # TOC section
    if toc_items:
        toc_html = f"""      <aside class="toc" role="navigation" aria-label="Table of contents">
        <div class="toc__label">On this page</div>
        <ul id="toc-list">
{toc_items}
        </ul>
      </aside>"""
    else:
        toc_html = ""

    # Lead paragraph (first <p> from body, shortened)
    lead_match = re.search(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)
    lead_text = ""
    if lead_match:
        lead_text = re.sub(r'<[^>]+>', '', lead_match.group(1)).strip()
        if len(lead_text) > 200:
            lead_text = lead_text[:197] + "…"

    # Pill label
    pill_label = "Article"
    headline_lower = meta["headline"].lower()
    if any(w in headline_lower for w in ["best", "meilleur", "mejor", "miglio", "besten"]):
        pill_label = "Buyer's Guide"
    elif any(w in headline_lower for w in ["guide", "guía", "guida", "leitfaden"]):
        pill_label = "Complete Guide"
    elif any(w in headline_lower for w in ["how to", "comment", "cómo", "come", "wie"]):
        pill_label = "How-To Guide"
    elif any(w in headline_lower for w in ["vs", "versus", "compar"]):
        pill_label = "Comparison"
    elif any(w in headline_lower for w in ["template", "modèle", "plantilla", "vorlage"]):
        pill_label = "Templates"
    elif any(w in headline_lower for w in ["alternative"]):
        pill_label = "Alternatives"

    # Build the HTML
    article_html = f'''<!DOCTYPE html>
<html lang="{meta['lang']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta['title_tag']}</title>
  <meta name="description" content="{meta['description']}">
  <link rel="canonical" href="{meta['canonical']}">

    {meta['hreflang_tags']}

  <!-- Fonts: Epilogue (sans) + JetBrains Mono + Playfair Display italic (accent) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">

  {shell['style']}

    {meta['og_tags']}
    {meta['twitter_tags']}
    {meta['jsonld']}

  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
</head>

<body>
<div class="reading-progress" id="reading-progress"></div>

{shell['nav']}

    <header class="article-hero">
      <div class="article-hero-inner">
        <span class="pill pill--glass">
          <i data-lucide="book-open" style="width:12px;height:12px"></i>
          {pill_label}
        </span>
        <h1>{meta['headline']}</h1>
        <p class="lead">{lead_text if lead_text else meta['description']}</p>
        <div class="article-meta">
          <div class="article-meta__avatar">{initials}</div>
          <div class="article-meta__text">
            <div class="article-meta__author">{meta['author_name']}</div>
            <div class="article-meta__dates">{dates_display}</div>
          </div>
        </div>
      </div>
    </header>

    <!-- Content -->
    <div class="article-layout">
{toc_html}

      <main class="prose">

{body}

      </main>
    </div>

    <section class="author-card">
      <div class="author-card__avatar">{initials}</div>
      <div>
        <div class="author-card__name">{meta['author_name']}</div>
        <div class="author-card__role">{author_role}</div>
        <div class="author-card__bio">{author_bio}</div>
      </div>
    </section>

{shell['footer']}

    {shell['scripts']}
</body>
</html>'''

    return article_html, None


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--locale", help="Only process this locale (fr/de/es/it)")
    parser.add_argument("--file", help="Process a single file")
    args = parser.parse_args()

    shell = extract_v2_shell()
    if not shell["style"]:
        print("ERROR: Could not extract V2 CSS from reference article")
        sys.exit(1)

    print(f"V2 shell extracted: {len(shell['style']):,} chars CSS")

    locales = [args.locale] if args.locale else LOCALES
    files_to_process = []

    if args.file:
        files_to_process = [Path(args.file)]
    else:
        for locale in locales:
            locale_dir = BLOG_DIR / locale
            if not locale_dir.is_dir():
                print(f"SKIP: {locale_dir} not found")
                continue
            files_to_process.extend(sorted(locale_dir.glob("*.html")))

    total = len(files_to_process)
    success = 0
    errors = []

    for filepath in files_to_process:
        relpath = filepath.relative_to(BLOG_DIR)

        result, error = build_v2_article(filepath, shell)

        if error:
            errors.append(f"{relpath}: {error}")
            continue

        if args.dry_run:
            print(f"  OK {relpath} ({len(result):,} bytes)")
        else:
            filepath.write_text(result, encoding="utf-8")
            print(f"  ✓ {relpath} ({len(result):,} bytes)")

        success += 1

    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Processed {success}/{total} articles")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")


if __name__ == "__main__":
    main()
