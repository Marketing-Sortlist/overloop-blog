#!/usr/bin/env python3
"""
migrate-v2.py — Migrate 75 published EN blog articles from V1 (overloop.css, Inter)
to V2 templates (inline CSS, Epilogue font, indigo-to-purple gradient).

Usage:
    python3 migrate-v2.py          # migrate all 75 articles
    python3 migrate-v2.py --dry-run  # preview without writing
"""

import csv
import json
import os
import re
import sys
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
BLOG_DIR = Path("/Users/tanguy/Documents/sortlist/overloop-blog/blog")
TEMPLATES_DIR = Path("/Users/tanguy/Documents/overloop-design-system/templates-v2")
CSV_PATH = Path("/tmp/content-calendar.csv")

# ─── Template mapping (calendar TEMPLATE value → V2 template filename) ───────
TEMPLATE_MAP = {
    "Best tool for X":                      "best-tools.html",
    "Alternatives to X":                    "alternatives.html",
    "Pillar / ultimate guide":              "pillar-guide.html",
    "How-to tutorial":                      "how-to.html",
    "X vs Y":                               "versus.html",
    "Templates & swipe file — Email templates": "swipe-files.html",
    "Templates & swipe file — Subject lines":   "swipe-files.html",
    "Data list / directory":                "data-list.html",
    "Statistics & benchmarks":              "statistics.html",
    "Strategy / playbook":                  "strategy.html",
    "Tactical article — Product review":    "tool-review.html",
    # All other Tactical article sub-types → tactical.html
    "Tactical article — Best practices":    "tactical.html",
    "Tactical article — Tips":              "tactical.html",
    "Tactical article — Mistakes to avoid": "tactical.html",
    "Tactical article — Checklist":         "tactical.html",
    "Tactical article — Metrics & KPIs":    "tactical.html",
    "Tactical article — Automation":        "tactical.html",
    "Tactical article — Timing":            "tactical.html",
    "Tactical article — Types":             "tactical.html",
    "Tactical article — Ideas":             "tactical.html",
    "Tactical article — Case study":        "tactical.html",
    "Tactical article — FAQ":               "tactical.html",
}


def resolve_template(template_label: str) -> str:
    """Map calendar TEMPLATE label to a V2 template filename, with fallback."""
    if template_label in TEMPLATE_MAP:
        return TEMPLATE_MAP[template_label]
    # Catch-all for any "Tactical article — *" or unknown sub-type
    if template_label.startswith("Tactical article"):
        return "tactical.html"
    if template_label.startswith("Templates & swipe file"):
        return "swipe-files.html"
    # Fallback to tactical (simplest)
    return "tactical.html"


# ─── CSV reader ───────────────────────────────────────────────────────────────
def load_calendar() -> dict:
    """Return {slug: template_filename} for 'Already Published' EN articles."""
    mapping = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get("Status") or "").strip()
            if status != "Already Published":
                continue
            url_slug = (row.get("URL Slug") or "").strip()
            template_label = (row.get("TEMPLATE") or "").strip()
            if not url_slug or not template_label:
                continue
            # URL Slug is like "/blog/slug-name" — extract just the slug
            slug = url_slug.rstrip("/").split("/")[-1]
            mapping[slug] = resolve_template(template_label)
    return mapping


# ─── Template cache ───────────────────────────────────────────────────────────
_template_cache: dict[str, dict] = {}


def load_template(template_filename: str) -> dict:
    """Parse and cache the V2 template into its structural parts.

    Returns dict with keys:
        head_before_style  — everything from <!DOCTYPE> to right before <style>
        style              — the full <style>...</style> block
        head_after_style   — from after </style> to </head> (lucide script + </head>)
        nav                — from <nav ...> to </nav>
        hero_structure     — the <header class="article-hero">...</header> as-is (sample content)
        post_article_sections — from </main> closing to </article> (CTA, author card, newsletter, related, expert panel)
        footer             — from <footer ...> to </footer>
        scripts            — from after </footer> to </body> (JSON-LD schemas + JS)
    """
    if template_filename in _template_cache:
        return _template_cache[template_filename]

    path = TEMPLATES_DIR / template_filename
    html = path.read_text(encoding="utf-8")

    parts = {}

    # ── <style> block ──
    style_match = re.search(r"(<style>.*?</style>)", html, re.DOTALL)
    parts["style"] = style_match.group(1) if style_match else ""

    # ── head_before_style: from start to <style> ──
    style_start = html.find("<style>")
    parts["head_before_style"] = html[:style_start] if style_start > 0 else ""

    # ── head_after_style: from </style> to </head> ──
    style_end = html.find("</style>")
    if style_end > 0:
        after_style_start = style_end + len("</style>")
        head_end = html.find("</head>")
        parts["head_after_style"] = html[after_style_start:head_end] if head_end > 0 else ""
    else:
        parts["head_after_style"] = ""

    # ── Nav: <nav class="nav"> to </nav> ──
    nav_match = re.search(r'(<nav class="nav">.*?</nav>)', html, re.DOTALL)
    parts["nav"] = nav_match.group(1) if nav_match else ""

    # ── Footer: <footer class="footer"> to </footer> ──
    footer_match = re.search(r'(<footer class="footer">.*?</footer>)', html, re.DOTALL)
    parts["footer"] = footer_match.group(1) if footer_match else ""

    # ── Scripts after footer (reading progress, TOC scroll-spy, lucide init) ──
    footer_end_pos = html.find("</footer>")
    body_end_pos = html.find("</body>")
    if footer_end_pos > 0 and body_end_pos > 0:
        scripts_block = html[footer_end_pos + len("</footer>"):body_end_pos].strip()
        # Remove the sample JSON-LD schemas from the template (we use the article's own)
        scripts_block = re.sub(
            r'<script type="application/ld\+json">.*?</script>\s*',
            "", scripts_block, flags=re.DOTALL
        )
        parts["scripts"] = scripts_block
    else:
        parts["scripts"] = ""

    _template_cache[template_filename] = parts
    return parts


# ─── Article parser ───────────────────────────────────────────────────────────
def extract_meta(html: str) -> dict:
    """Extract all metadata from the current V1 article <head>."""
    meta = {}

    # Title
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    meta["title_tag"] = m.group(1).strip() if m else ""

    # Meta description
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.DOTALL)
    meta["description"] = m.group(1).strip() if m else ""

    # Canonical
    m = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', html)
    meta["canonical"] = m.group(1) if m else ""

    # Hreflang tags (all of them, including x-default)
    hreflang_tags = re.findall(r'(<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>)', html)
    meta["hreflang_tags"] = "\n    ".join(hreflang_tags) if hreflang_tags else ""

    # OG tags
    og_tags = re.findall(r'(<meta\s+property="og:[^"]*"\s+content="[^"]*"\s*/?>)', html)
    meta["og_tags"] = "\n    ".join(og_tags) if og_tags else ""

    # Twitter tags
    twitter_tags = re.findall(r'(<meta\s+name="twitter:[^"]*"\s+content="[^"]*"\s*/?>)', html)
    meta["twitter_tags"] = "\n    ".join(twitter_tags) if twitter_tags else ""

    # JSON-LD scripts (all of them)
    jsonld_blocks = re.findall(r'(<script type="application/ld\+json">.*?</script>)', html, re.DOTALL)
    meta["jsonld"] = "\n    ".join(jsonld_blocks) if jsonld_blocks else ""

    # Extract from JSON-LD: author, datePublished, dateModified, headline
    for block in jsonld_blocks:
        try:
            json_str = re.search(r"<script[^>]*>(.*?)</script>", block, re.DOTALL).group(1)
            data = json.loads(json_str)
            if data.get("@type") in ("BlogPosting", "Article"):
                meta["headline"] = data.get("headline", "")
                meta["date_published"] = data.get("datePublished", "")
                meta["date_modified"] = data.get("dateModified", "")
                author = data.get("author", {})
                if isinstance(author, dict):
                    meta["author_name"] = author.get("name", "")
                elif isinstance(author, list) and author:
                    meta["author_name"] = author[0].get("name", "")
        except (json.JSONDecodeError, AttributeError):
            continue

    # Fallbacks
    meta.setdefault("headline", meta["title_tag"].replace(" | Overloop", ""))
    meta.setdefault("author_name", "Nicolas Finet")
    meta.setdefault("date_published", "")
    meta.setdefault("date_modified", "")

    return meta


def extract_article_body(html: str) -> str:
    """Extract the article body content from <article class="article-content">...</article>."""

    # Pattern 1: <article class="article-content">...</article>
    m = re.search(
        r'<article\s+class="article-content">\s*(.*?)\s*</article>',
        html, re.DOTALL
    )
    if m:
        return m.group(1).strip()

    # Pattern 2: fall back to <main class="article-body">...<article>...</article>...</main>
    m = re.search(
        r'<article[^>]*>\s*(.*?)\s*</article>',
        html, re.DOTALL
    )
    if m:
        return m.group(1).strip()

    # Pattern 3: everything inside <main>...</main> minus nav/footer elements
    m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if m:
        return m.group(1).strip()

    return ""


def extract_hero_parts(html: str) -> dict:
    """Extract title, subtitle, badge from the existing article's hero/header."""
    hero = {}

    # h1
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    hero["h1"] = m.group(1).strip() if m else ""

    # subtitle / lead paragraph
    m = re.search(r'<p\s+class="subtitle"[^>]*>(.*?)</p>', html, re.DOTALL)
    hero["subtitle"] = m.group(1).strip() if m else ""

    # header badge
    m = re.search(r'<span\s+class="header-badge"[^>]*>(.*?)</span>', html, re.DOTALL)
    hero["badge"] = m.group(1).strip() if m else ""

    return hero


def extract_cta_box(html: str) -> str:
    """Extract the CTA box if present."""
    m = re.search(r'(<div class="cta-box">.*?</div>)', html, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_author_bio(html: str) -> str:
    """Extract the author bio section if present."""
    m = re.search(r'(<div class="author-bio">.*?</div>\s*</div>)', html, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_related_posts(html: str) -> str:
    """Extract the related posts section if present."""
    m = re.search(r'(<div class="related-posts">.*?</div>)', html, re.DOTALL)
    return m.group(1).strip() if m else ""


# ─── Article builder ──────────────────────────────────────────────────────────
def format_date_display(date_str: str) -> str:
    """Convert 2024-09-12 to Sep 12, 2024."""
    if not date_str:
        return ""
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except ValueError:
        return date_str


def author_initials(name: str) -> str:
    """Nicolas Finet → NF."""
    parts = name.split()
    return "".join(p[0].upper() for p in parts if p)


def get_pill_label(template_filename: str, calendar_template: str) -> str:
    """Determine the hero pill label based on template type."""
    pill_map = {
        "best-tools.html": "Buyer's Guide",
        "alternatives.html": "Alternatives",
        "pillar-guide.html": "Complete Guide",
        "how-to.html": "How-To Guide",
        "versus.html": "Comparison",
        "swipe-files.html": "Templates",
        "data-list.html": "Directory",
        "statistics.html": "Data & Stats",
        "strategy.html": "Strategy",
        "tool-review.html": "Product Review",
        "tactical.html": "Tactical",
    }
    base = pill_map.get(template_filename, "Article")

    # For tactical sub-variants, add the sub-type
    if template_filename == "tactical.html" and calendar_template.startswith("Tactical article"):
        sub = calendar_template.replace("Tactical article — ", "").replace("Tactical article", "").strip()
        if sub:
            base = f"Tactical · {sub}"

    return base


def get_pill_icon(template_filename: str) -> str:
    """Lucide icon name for the pill."""
    icon_map = {
        "best-tools.html": "book-open",
        "alternatives.html": "repeat",
        "pillar-guide.html": "compass",
        "how-to.html": "list-checks",
        "versus.html": "scale",
        "swipe-files.html": "file-text",
        "data-list.html": "database",
        "statistics.html": "bar-chart-3",
        "strategy.html": "target",
        "tool-review.html": "search",
        "tactical.html": "zap",
    }
    return icon_map.get(template_filename, "book-open")


def build_migrated_article(
    slug: str,
    current_html: str,
    template_filename: str,
    calendar_template: str,
) -> str:
    """Build the new V2 article HTML from current article content + V2 template shell."""

    meta = extract_meta(current_html)
    body_content = extract_article_body(current_html)
    hero = extract_hero_parts(current_html)
    cta_box = extract_cta_box(current_html)
    author_bio = extract_author_bio(current_html)
    related_posts = extract_related_posts(current_html)
    tpl = load_template(template_filename)

    # Build date display
    pub_date = format_date_display(meta["date_published"])
    mod_date = format_date_display(meta["date_modified"])
    date_line = ""
    if pub_date:
        date_line = f"Published {pub_date}"
        if mod_date and mod_date != pub_date:
            date_line += f" · Updated {mod_date}"

    author = meta["author_name"]
    initials = author_initials(author)
    headline = meta["headline"] or hero["h1"]
    subtitle = hero["subtitle"] or meta["description"]
    pill_label = get_pill_label(template_filename, calendar_template)
    pill_icon = get_pill_icon(template_filename)

    # ── Build <head> ──
    head = f"""<!DOCTYPE html>
<html lang="en">
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

  {tpl['style']}

  {meta['og_tags']}
  {meta['twitter_tags']}
  {meta['jsonld']}
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
</head>"""

    # ── Build <body> ──
    # Reading progress bar
    body_open = """
<body>

  <!-- Reading progress -->
  <div class="reading-progress" id="reading-progress"></div>

  <!-- Nav -->"""

    # Nav
    nav = f"\n  {tpl['nav']}\n"

    # Hero
    hero_section = f"""
  <!-- Article -->
  <article>

    <!-- Hero -->
    <header class="article-hero">
      <div class="article-hero-inner">
        <span class="pill pill--glass">
          <i data-lucide="{pill_icon}" style="width:12px;height:12px"></i>
          {pill_label}
        </span>
        <h1>{headline}</h1>
        <p class="lead">{subtitle}</p>
        <div class="article-meta">
          <div class="article-meta__avatar">{initials}</div>
          <div class="article-meta__text">
            <div class="article-meta__author">{author}</div>
            <div class="article-meta__dates">{date_line}</div>
          </div>
        </div>
      </div>
    </header>
"""

    # Main content area — use the template's main wrapper class
    # For best-tools/pillar-guide, use article-layout with prose
    # For tactical/others, use main-wrap or prose directly
    if template_filename in ("best-tools.html", "pillar-guide.html", "alternatives.html", "versus.html"):
        main_open = """    <!-- Content -->
    <div class="article-layout">
      <aside class="toc" role="navigation" aria-label="Table of contents">
        <div class="toc__label">On this page</div>
        <ul id="toc-list"></ul>
      </aside>
      <main class="prose">
"""
        main_close = """      </main>
    </div>
"""
    else:
        main_open = """    <!-- Content -->
    <main class="prose" style="max-width:var(--container-blog);margin:0 auto;padding:40px var(--page-px,48px);">
"""
        main_close = """    </main>
"""

    # Build the CTA section (from template style)
    cta_section = """
    <!-- End CTA -->
    <section class="cta-hard" style="text-align:center;padding:56px 48px;background:var(--gradient-brand-soft);border-top:1px solid var(--color-border-light);border-bottom:1px solid var(--color-border-light);">
      <h3 style="font-size:28px;font-weight:800;color:var(--color-text);margin-bottom:12px;">Ready to automate your outbound <em>with AI?</em></h3>
      <p style="font-size:17px;color:var(--color-text-secondary);max-width:540px;margin:0 auto 28px;">Overloop combines AI email personalization, LinkedIn automation, and phone steps in one platform. No annual contract required.</p>
      <a href="https://app.overloop.ai/session/signup" class="btn-glow" style="display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:16px 40px;background:var(--gradient-brand);color:#fff;border:none;border-radius:16px;font-family:var(--font-sans);font-size:16px;font-weight:600;text-decoration:none;cursor:pointer;box-shadow:0 8px 32px rgba(99,102,241,0.30);">
        <i data-lucide="sparkles" style="width:18px;height:18px"></i>
        Try Overloop free
      </a>
    </section>
"""

    # Author card (V2 style)
    author_card = f"""
    <!-- Author -->
    <section class="author-card" style="display:flex;align-items:center;gap:20px;max-width:var(--container-blog);margin:40px auto;padding:0 var(--page-px,48px);">
      <div style="width:56px;height:56px;border-radius:50%;background:var(--gradient-brand);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0;">{initials}</div>
      <div>
        <div style="font-size:17px;font-weight:700;color:var(--color-text);">{author}</div>
        <div style="font-size:14px;color:var(--color-text-secondary);">Overloop</div>
      </div>
    </section>
"""

    # Newsletter (V2 style)
    newsletter = """
    <!-- Newsletter -->
    <section class="newsletter" style="text-align:center;padding:40px 48px;max-width:var(--container-blog);margin:0 auto;">
      <h3 style="font-size:22px;font-weight:800;color:var(--color-text);margin-bottom:8px;">Outbound insights — once a week, no fluff</h3>
      <p style="font-size:15px;color:var(--color-text-secondary);margin-bottom:20px;">Join 8,400+ B2B operators getting our tested tactics, tools, and templates.</p>
      <form onsubmit="event.preventDefault();" style="display:flex;gap:10px;justify-content:center;max-width:420px;margin:0 auto;">
        <input type="email" placeholder="Your work email" required style="flex:1;padding:12px 16px;border:1px solid var(--color-border);border-radius:var(--r,12px);font-family:var(--font-sans);font-size:15px;">
        <button type="submit" class="btn" style="padding:12px 24px;background:var(--color-primary,#6366F1);color:#fff;border:none;border-radius:var(--r,12px);font-family:var(--font-sans);font-size:15px;font-weight:600;cursor:pointer;">Subscribe</button>
      </form>
    </section>
"""

    # Related posts (keep original links if available, styled V2)
    related_section = ""
    if related_posts:
        # Extract the link items from the old related posts
        links = re.findall(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', related_posts, re.DOTALL)
        if links:
            related_cards = ""
            for href, text in links:
                text = text.strip()
                related_cards += f"""        <a href="{href}" class="related-card" style="display:block;padding:20px;background:var(--color-white,#fff);border:1px solid var(--color-border-light,#F3F4F6);border-radius:var(--r-lg,16px);text-decoration:none;transition:200ms ease;">
          <div style="font-size:16px;font-weight:600;color:var(--color-text,#1A1A2E);">{text}</div>
        </a>
"""
            related_section = f"""
    <!-- Related -->
    <section class="related" style="max-width:var(--container-blog);margin:40px auto;padding:0 var(--page-px,48px);">
      <h3 style="font-size:22px;font-weight:800;color:var(--color-text);margin-bottom:20px;">Related articles</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;">
{related_cards}      </div>
    </section>
"""

    # Close article tag
    article_close = "\n  </article>\n"

    # Footer
    footer = f"\n  <!-- Footer -->\n  {tpl['footer']}\n"

    # Scripts (reading progress, TOC scroll-spy, lucide init)
    # Build a consolidated script block
    has_toc = template_filename in ("best-tools.html", "pillar-guide.html", "alternatives.html", "versus.html")
    scripts = """
  <script>
    // Lucide icons
    if (window.lucide) lucide.createIcons();

    // Reading progress
    (function() {
      var bar = document.getElementById('reading-progress');
      function update() {
        var h = document.documentElement;
        var scrollTop = h.scrollTop || document.body.scrollTop;
        var scrollHeight = h.scrollHeight - h.clientHeight;
        var pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
        bar.style.width = pct + '%';
      }
      window.addEventListener('scroll', update, { passive: true });
      update();
    })();
"""

    if has_toc:
        scripts += """
    // Auto-generate TOC from h2 elements in .prose
    (function() {
      var prose = document.querySelector('.prose');
      var tocList = document.getElementById('toc-list');
      if (!prose || !tocList) return;
      var headings = prose.querySelectorAll('h2');
      headings.forEach(function(h, i) {
        if (!h.id) h.id = 'section-' + i;
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = '#' + h.id;
        a.textContent = h.textContent;
        li.appendChild(a);
        tocList.appendChild(li);
      });

      // Scroll-spy
      var tocLinks = tocList.querySelectorAll('a');
      var targets = Array.from(tocLinks).map(function(a) {
        var id = a.getAttribute('href').slice(1);
        return { link: a, section: document.getElementById(id) };
      }).filter(function(t) { return t.section; });

      function onScroll() {
        var scrollY = window.scrollY + 120;
        var active = targets[0];
        for (var j = 0; j < targets.length; j++) {
          if (targets[j].section.offsetTop <= scrollY) active = targets[j];
        }
        tocLinks.forEach(function(a) { a.classList.remove('active'); });
        if (active) active.link.classList.add('active');
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    })();
"""

    scripts += "  </script>\n"

    # ── Assemble ──
    result = head
    result += body_open
    result += nav
    result += hero_section
    result += main_open
    result += body_content + "\n"
    result += main_close
    result += cta_section
    result += author_card
    result += newsletter
    result += related_section
    result += article_close
    result += footer
    result += scripts
    result += "\n</body>\n</html>"

    return result


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 72)
    print("  migrate-v2.py — V1 → V2 Template Migration")
    print("=" * 72)
    print()

    # Load calendar mapping
    calendar = load_calendar()
    print(f"Calendar entries loaded: {len(calendar)} 'Already Published' articles")

    # Get all blog files (excluding index.html)
    blog_files = sorted([
        f for f in BLOG_DIR.glob("*.html")
        if f.name != "index.html"
    ])
    print(f"Blog files found: {len(blog_files)}")
    print()

    # Stats
    migrated = 0
    skipped = []
    errors = []
    template_counts = {}

    for blog_file in blog_files:
        slug = blog_file.stem
        template_filename = calendar.get(slug)

        if not template_filename:
            skipped.append(slug)
            continue

        # Check template file exists
        template_path = TEMPLATES_DIR / template_filename
        if not template_path.exists():
            errors.append((slug, f"Template file not found: {template_filename}"))
            continue

        try:
            current_html = blog_file.read_text(encoding="utf-8")
            new_html = build_migrated_article(
                slug=slug,
                current_html=current_html,
                template_filename=template_filename,
                calendar_template=next(
                    (row_tpl for row_slug, row_tpl in _calendar_raw.items() if row_slug == slug),
                    ""
                ),
            )

            if dry_run:
                print(f"  [DRY RUN] {slug} → {template_filename}")
            else:
                blog_file.write_text(new_html, encoding="utf-8")
                print(f"  [OK] {slug} → {template_filename}")

            migrated += 1
            template_counts[template_filename] = template_counts.get(template_filename, 0) + 1

        except Exception as e:
            errors.append((slug, str(e)))
            print(f"  [ERROR] {slug}: {e}")

    # ── Report ──
    print()
    print("=" * 72)
    print("  MIGRATION REPORT")
    print("=" * 72)
    print(f"\n  Total blog files:    {len(blog_files)}")
    print(f"  Migrated:            {migrated}")
    print(f"  Skipped (no match):  {len(skipped)}")
    print(f"  Errors:              {len(errors)}")
    if dry_run:
        print(f"\n  Mode: DRY RUN (no files written)")

    print(f"\n  Articles per template:")
    for tpl_name in sorted(template_counts.keys()):
        print(f"    {tpl_name:<25s} {template_counts[tpl_name]:>3d}")

    if skipped:
        print(f"\n  Skipped slugs (not in calendar):")
        for s in skipped:
            print(f"    - {s}")

    if errors:
        print(f"\n  Errors:")
        for slug, msg in errors:
            print(f"    - {slug}: {msg}")

    print()
    return 0 if not errors else 1


# We need the raw calendar template labels (not just resolved filenames) for pill labels
_calendar_raw: dict[str, str] = {}


def _load_calendar_raw():
    """Load raw template labels from CSV."""
    global _calendar_raw
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get("Status") or "").strip()
            if status != "Already Published":
                continue
            url_slug = (row.get("URL Slug") or "").strip()
            template_label = (row.get("TEMPLATE") or "").strip()
            if not url_slug or not template_label:
                continue
            slug = url_slug.rstrip("/").split("/")[-1]
            _calendar_raw[slug] = template_label


if __name__ == "__main__":
    _load_calendar_raw()
    sys.exit(main())
