#!/usr/bin/env python3
"""
migrate-to-v2.py — Full content-fidelity migration of legacy Overloop blog articles
                   into the V2 design system templates.

Strategy ("shell + body injection"):
  - Keep the V2 template's hero, TOC, author intro, expert panel, CTA, newsletter, footer.
  - Replace the V2 main content area with the legacy <article class="article-content"> body.
  - Preserve all legacy JSON-LD schemas (BlogPosting → Article, BreadcrumbList, FAQPage, ItemList).
  - Preserve hreflang block (only locales that actually exist in repo).
  - Preserve canonical URL, OG tags, title, meta description.
  - Recompute Updated date (set to migration date) → freshness signal.

Output:
  --out blog/_v2/  (default — staging)
  --out blog/      (production overwrite — replaces legacy)

Usage:
  python3 migrate-to-v2.py                       # canary on 5 articles
  python3 migrate-to-v2.py --slug X              # single article
  python3 migrate-to-v2.py --all                 # full 75 EN
  python3 migrate-to-v2.py --all --out blog      # production
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    print("ERROR: BeautifulSoup4 not installed. Run: pip3 install --user beautifulsoup4 lxml")
    sys.exit(1)

# ============================================================================
# CONFIG
# ============================================================================
REPO = Path(__file__).parent
LEGACY_DIR = REPO / "blog"  # Legacy EN articles at blog/{slug}.html
TEMPLATE_DIR = Path.home() / "Documents" / "overloop-design-system" / "templates-v2"
DEFAULT_OUT = REPO / "blog" / "_v2"
MIGRATION_DATE = dt.date(2026, 4, 27)
MIGRATION_DATE_HUMAN = "Apr 27, 2026"

# Author registry (3 experts for E-E-A-T rotation)
AUTHORS = {
    "Vincenzo Ruggiero": {
        "initials": "VR",
        "photo": "https://overloop.com/assets/images/vincenzo-ruggiero.png",
        "role_intro": "CEO, Overloop · 10+ years building sales automation · 500+ teams served",
        "bio_short": "CEO at Overloop. Founded the company in 2015 as Prospect.io. Tests every competitor tool hands-on.",
    },
    "Nicolas Finet": {
        "initials": "NF",
        "photo": "https://overloop.com/assets/images/nicolas-finet.png",
        "role_intro": "CEO, Sortlist & Overloop · 500+ B2B outbound systems built",
        "bio_short": "CEO at Overloop. Co-founded Sortlist in 2014. Designed outbound systems for 500+ B2B companies.",
    },
    "Nathalie Saikali": {
        "initials": "NS",
        "photo": "https://overloop.com/assets/images/nathalie-saikali.png",
        "role_intro": "Customer Success Manager, Overloop · Hundreds of customer conversations",
        "bio_short": "Customer Success at Overloop. Works daily with sales teams deploying multichannel outbound.",
    },
}

# Slug → template mapping (15 templates × 75 articles)
# Source: column O of Content Calendar 2026 (sheet) + manual review of legacy article types
SLUG_TO_TEMPLATE = {
    # === BEST TOOLS LISTICLE ===
    "10-best-ai-sales-assistant-tools": "best-tools.html",
    "10-essential-sales-tools-every-b2b-team-needs-in-2025": "best-tools.html",
    "11-best-ai-bdr-tools": "best-tools.html",
    "11-best-linkedin-automation-tools-to-accelerate-your-b2b-outreach-in-2025-6b690": "best-tools.html",
    "7-ai-sales-prospecting-tools-that-boost-lead-generation": "best-tools.html",
    "8-best-ai-linkedin-outreach-tools": "best-tools.html",
    "9-best-ai-agent-tools-for-sales": "best-tools.html",
    "9-best-ai-email-outreach-tools": "best-tools.html",
    "9-best-ai-multichannel-outreach-tools": "best-tools.html",
    "best-ai-sales-tools": "best-tools.html",
    "best-lead-generation-tools": "best-tools.html",
    "the-ultimate-checklist-for-selecting-the-best-ai-sdr-tools-in-2025": "best-tools.html",
    "top-8-sales-prospecting-tools-for-small-business-teams": "best-tools.html",
    # === ALTERNATIVES ===
    "apollo-alternatives": "alternatives.html",
    "instantly-alternatives": "alternatives.html",
    "lemlist-alternatives": "alternatives.html",
    "outreach-alternatives": "alternatives.html",
    "salesloft-alternatives": "alternatives.html",
    # === PILLAR / ULTIMATE GUIDE ===
    "the-ultimate-guide-to-linkedin-automation-boost-b2b-sales-in-2025": "pillar-guide.html",
    "ai-generated-value-propositions-guide": "pillar-guide.html",
    "ai-sales-tool-adoption-in-b2b-outbound-prospecting-2025-industry-review-analysis": "pillar-guide.html",
    "ai-sales-tools-roi-key-metrics-to-track": "pillar-guide.html",
    "automations": "pillar-guide.html",
    "boost-sales-motivation": "pillar-guide.html",
    "cold-email-illegal": "pillar-guide.html",
    "cold-emailing-link-building": "pillar-guide.html",
    "deal-objections": "pillar-guide.html",
    "email-automation": "pillar-guide.html",
    "how-ai-follow-up-scheduling-boosts-sales-efficiency": "pillar-guide.html",
    "how-to-build-scalable-lead-generation-workflows": "pillar-guide.html",
    "how-to-write-personalized-sales-emails-at-scale": "pillar-guide.html",
    "increase-reply-rate": "pillar-guide.html",
    "increase-saas-sales-growth-system": "pillar-guide.html",
    "kickstart-sales-career-2": "pillar-guide.html",
    "know-prospect-find": "pillar-guide.html",
    "linkedin-vs-email-which-performs-better-for-b2b-outreach": "versus.html",  # vs template
    "perfect-follow-up-email-campaign": "pillar-guide.html",
    "sales-appointment-setting": "pillar-guide.html",
    "sales-engagement-platforms-compared-top-sales-engagement-platforms-2025-versus-guide": "best-tools.html",
    "sales-presentations": "pillar-guide.html",
    # === HOW-TO ===
    "how-to-compose-a-follow-up-email": "how-to.html",
    "how-to-find-someone-email-address-efficiently": "how-to.html",
    "how-to-use-overloop-email-finder-step-by-step-for-effortless-lead-generation": "how-to.html",
    "how-to-write-a-successful-cold-email": "how-to.html",
    "how-to-write-a-successful-follow-up-email": "how-to.html",
    "get-email-from-linkedin-profile": "how-to.html",
    "following-up-surefire-techniques": "how-to.html",
    # === DATA LIST / DIRECTORY ===
    "455-email-spam-trigger-words-avoid-2018": "data-list.html",
    "500-trigger-words": "data-list.html",
    # === STATISTICS & BENCHMARKS ===
    "cold-email-stats-2018": "statistics.html",
    # === X vs Y ===
    "inside-sales-outside-sales": "versus.html",
    # === REVIEWS (single product) ===
    "la-growth-machine-review": "tool-review.html",
    "linkedin-helper-review": "tool-review.html",
    # === TACTICAL — Tips ===
    "10-best-practices-for-multi-channel-sales-campaigns": "tactical.html",
    "10-favourite-sales-movies": "tactical.html",
    "10-pro-tips-avoid-spam-folder": "tactical.html",
    "10-proven-sales-prospecting-tips-to-boost-your-pipeline-fast": "tactical.html",
    "17-sentences-never-use-sales-email": "tactical.html",
    "5-rules-more-successful-salespeople": "tactical.html",
    "6-reasons-sales-process-broken": "tactical.html",
    "7-reasons-emails-bounce": "tactical.html",
    "9-reasons-never-buy-email-lists": "tactical.html",
    "ab-testing-email-drip-campaigns": "tactical.html",
    "best-practices-for-links-in-your-emails": "tactical.html",
    "best-sales-email-template": "swipe-files.html",  # template type
    "best-subject-lines-for-sales-emails": "swipe-files.html",
    "common-sales-automation-mistakes-and-how-to-avoid-them": "tactical.html",
    "sales-email-tips-to-help-you-close-more-deals": "tactical.html",
    "seasonal-sales": "tactical.html",
    # === STRATEGY ===
    "5-main-steps-for-an-effective-cold-email-marketing-strategy": "strategy.html",
    # === MISC LEGACY ===
    "b2b-cold-email-germany-gdpr-compliance": "tactical.html",  # Tactical — Best practices
    "lead-generation-strategies-every-saas-business-should-try-today": "lead-gen-industry.html",
    "overloop-joins-sortlist": "tactical.html",
    "whats-the-best-email-length-for-sales-outreach": "tactical.html",
    "pre-call-planning": "what-is.html",  # Definition pillar (per GSC analysis)
}

# Five POC articles (default for canary runs)
POC_SLUGS = [
    "11-best-ai-bdr-tools",
    "apollo-alternatives",
    "how-to-use-overloop-email-finder-step-by-step-for-effortless-lead-generation",
    "10-proven-sales-prospecting-tips-to-boost-your-pipeline-fast",
    "the-ultimate-guide-to-linkedin-automation-boost-b2b-sales-in-2025",
]

# ============================================================================
# LEGACY ARTICLE PARSER
# ============================================================================
class LegacyArticle:
    """Parse a legacy blog/{slug}.html and expose the elements we need to migrate."""

    def __init__(self, html_path: Path):
        self.path = html_path
        self.slug = html_path.stem
        self.html = html_path.read_text(encoding="utf-8")
        self.soup = BeautifulSoup(self.html, "lxml")

    @property
    def title(self) -> str:
        t = self.soup.find("title")
        return t.get_text(strip=True) if t else ""

    @property
    def description(self) -> str:
        m = self.soup.find("meta", attrs={"name": "description"})
        return m.get("content", "") if m else ""

    @property
    def canonical(self) -> str:
        l = self.soup.find("link", attrs={"rel": "canonical"})
        return l.get("href", "") if l else f"https://overloop.com/blog/{self.slug}"

    @property
    def og_image(self) -> str:
        m = self.soup.find("meta", attrs={"property": "og:image"})
        return m.get("content", "") if m else f"https://overloop.com/assets/images/og/{self.slug}.png"

    @property
    def og_title(self) -> str:
        m = self.soup.find("meta", attrs={"property": "og:title"})
        return m.get("content", self.title) if m else self.title

    @property
    def og_description(self) -> str:
        m = self.soup.find("meta", attrs={"property": "og:description"})
        return m.get("content", self.description) if m else self.description

    @property
    def hreflang_links(self) -> list[Tag]:
        return list(self.soup.find_all("link", attrs={"rel": "alternate", "hreflang": True}))

    @property
    def json_ld_scripts(self) -> list[Tag]:
        return list(self.soup.find_all("script", attrs={"type": "application/ld+json"}))

    @property
    def author_name(self) -> str:
        # First try the article-meta block
        author_div = self.soup.find("div", class_="article-meta__author")
        if author_div:
            return author_div.get_text(strip=True)
        # Fallback: parse from BlogPosting JSON-LD
        for s in self.json_ld_scripts:
            txt = s.get_text()
            m = re.search(r'"author"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"', txt)
            if m:
                return m.group(1)
        return "Vincenzo Ruggiero"  # fallback

    @property
    def published_date(self) -> str:
        for s in self.json_ld_scripts:
            txt = s.get_text()
            m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', txt)
            if m:
                # 2024-08-29 → Aug 29, 2024
                try:
                    d = dt.date.fromisoformat(m.group(1))
                    return d.strftime("%b %d, %Y").replace(" 0", " ")
                except ValueError:
                    return m.group(1)
        return "Apr 1, 2024"  # safe fallback

    @property
    def published_iso(self) -> str:
        for s in self.json_ld_scripts:
            txt = s.get_text()
            m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', txt)
            if m:
                return m.group(1)
        return "2024-04-01"

    @property
    def read_time(self) -> str:
        # Try to find "X min read" anywhere in the meta
        m = re.search(r'(\d+)\s*min\s*read', self.html)
        return f"{m.group(1)} min read" if m else "10 min read"

    @property
    def article_body(self) -> str:
        """Return the inner HTML of <article class="article-content">."""
        a = self.soup.find("article", class_="article-content")
        if not a:
            # Fallback: try <main class="article-body">
            main = self.soup.find("main", class_="article-body")
            if main:
                return main.decode_contents()
            return "<p>(content extraction failed — manual fix needed)</p>"
        return a.decode_contents()


# ============================================================================
# V2 TEMPLATE INJECTOR
# ============================================================================
class V2TemplateMigrator:
    """Take a V2 template + a LegacyArticle and produce migrated HTML."""

    def __init__(self, template_path: Path, article: LegacyArticle):
        self.template_path = template_path
        self.article = article
        self.html = template_path.read_text(encoding="utf-8")

    def author_block(self) -> dict:
        """Lookup the AUTHOR registry for the article's author."""
        return AUTHORS.get(self.article.author_name, AUTHORS["Vincenzo Ruggiero"])

    def hreflang_html(self) -> str:
        """Build the hreflang block from the legacy article (preserve only existing locales)."""
        if not self.article.hreflang_links:
            return f'<link rel="alternate" hreflang="en" href="https://overloop.com/blog/{self.article.slug}">\n  <link rel="alternate" hreflang="x-default" href="https://overloop.com/blog/{self.article.slug}">'
        return "\n  ".join(str(l) for l in self.article.hreflang_links)

    def article_meta_dates_html(self) -> str:
        """The text inside article-meta__dates."""
        return (
            f'Published {self.article.published_date} · '
            f'Updated {MIGRATION_DATE_HUMAN} · '
            f'{self.article.read_time}'
        )

    def updated_jsonld(self) -> str:
        """Fresh BlogPosting/Article JSON-LD with dateModified set to migration date."""
        author = self.author_block()
        return f'''{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {self._json_str(self.article.title)},
  "description": {self._json_str(self.article.description)},
  "image": "{self.article.og_image}",
  "author": {{
    "@type": "Person",
    "name": "{self.article.author_name}",
    "image": "{author['photo']}"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Overloop",
    "logo": {{"@type": "ImageObject", "url": "https://overloop.com/assets/images/overloop-logo.png"}}
  }},
  "datePublished": "{self.article.published_iso}",
  "dateModified": "{MIGRATION_DATE.isoformat()}",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://overloop.com/blog/{self.article.slug}"}}
}}'''

    @staticmethod
    def _json_str(s: str) -> str:
        """Safely escape a string for embedding in a JSON-LD block."""
        import json
        return json.dumps(s)

    def breadcrumb_jsonld(self) -> str:
        """Build BreadcrumbList JSON-LD."""
        clean_title = self.article.title.replace(" | Overloop", "").strip()
        return f'''{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Blog", "item": "https://overloop.com/blog"}},
    {{"@type": "ListItem", "position": 2, "name": {self._json_str(clean_title)}, "item": "{self.article.canonical}"}}
  ]
}}'''

    def preserved_jsonld_blocks(self) -> str:
        """Return legacy JSON-LD blocks EXCEPT BlogPosting and BreadcrumbList (both replaced with our own)."""
        kept = []
        for s in self.article.json_ld_scripts:
            txt = s.get_text()
            if '"BlogPosting"' in txt or '"BreadcrumbList"' in txt:
                continue  # we replace these with our own
            kept.append(str(s))
        return "\n".join(kept)

    # === Replacements ===
    def _replace(self, pattern: str, repl: str, count: int = 1, flags=re.DOTALL) -> None:
        self.html, n = re.subn(pattern, repl, self.html, count=count, flags=flags)
        if n == 0:
            print(f"  ⚠ pattern not matched: {pattern[:50]}...")

    def patch_metadata(self) -> None:
        # <title>
        new_title = f"{self.article.title}"
        if "| Overloop" not in new_title:
            new_title = f"{new_title} | Overloop"
        self._replace(
            r"<title>[^<]+</title>",
            f"<title>{self._escape_html(new_title)}</title>",
        )
        # meta description
        self._replace(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{self._escape_attr(self.article.description)}">',
        )
        # canonical
        self._replace(
            r'<link rel="canonical" href="[^"]*">',
            f'<link rel="canonical" href="{self.article.canonical}">',
        )

    def patch_hreflang(self) -> None:
        """Inject hreflang block right after canonical link."""
        hreflang = self.hreflang_html()
        # Insert after canonical
        self._replace(
            r'(<link rel="canonical" href="[^"]*">)',
            rf'\1\n  {hreflang}',
        )

    def patch_og_tags(self) -> None:
        """Add OG + Twitter tags after hreflang block."""
        og = (
            f'<meta property="og:title" content="{self._escape_attr(self.article.og_title)}">\n'
            f'  <meta property="og:description" content="{self._escape_attr(self.article.og_description)}">\n'
            f'  <meta property="og:image" content="{self.article.og_image}">\n'
            f'  <meta property="og:url" content="{self.article.canonical}">\n'
            f'  <meta property="og:type" content="article">\n'
            f'  <meta name="twitter:card" content="summary_large_image">\n'
            f'  <meta name="twitter:title" content="{self._escape_attr(self.article.og_title)}">\n'
            f'  <meta name="twitter:description" content="{self._escape_attr(self.article.og_description)}">\n'
            f'  <meta name="twitter:image" content="{self.article.og_image}">'
        )
        # Insert after the <link href="https://fonts.googleapis.com/css2..." line
        self._replace(
            r'(<link href="https://fonts\.googleapis\.com/css2[^"]+" rel="stylesheet">)',
            rf'\1\n\n  {og}',
        )

    def patch_h1(self) -> None:
        """Replace V2 hero H1 with legacy title (strip ' | Overloop' suffix if any)."""
        clean = self.article.title.replace(" | Overloop", "").strip()
        # Try to keep existing Playfair italic accent: split on a colon or em-dash for natural accent
        # Heuristic: if title contains ":" → main:accent.  if "—" → main—accent. Otherwise use full as main.
        for sep in [":", "—", "–"]:
            if sep in clean:
                main, accent = clean.split(sep, 1)
                main, accent = main.strip(), accent.strip()
                if accent:
                    new_h1 = f'<h1>{self._escape_html(main)} <em>{self._escape_html(accent)}</em></h1>'
                    break
        else:
            new_h1 = f'<h1>{self._escape_html(clean)}</h1>'
        self._replace(
            r'<h1>[^<]*(<em>[^<]*</em>[^<]*)?</h1>',
            new_h1,
        )

    def patch_lead(self) -> None:
        """Replace V2 hero lead paragraph with the meta description (or first article para)."""
        lead = self.article.description.strip() or "..."
        self._replace(
            r'<p class="lead">[^<]*</p>',
            f'<p class="lead">{self._escape_html(lead)}</p>',
        )

    def patch_article_meta(self) -> None:
        """Update author name, initials, dates."""
        author = self.author_block()
        # Avatar initials
        self._replace(
            r'<div class="article-meta__avatar">[A-Z]{2}</div>',
            f'<div class="article-meta__avatar">{author["initials"]}</div>',
        )
        # Author name
        self._replace(
            r'<div class="article-meta__author">[^<]+</div>',
            f'<div class="article-meta__author">{self._escape_html(self.article.author_name)}</div>',
        )
        # Dates
        self._replace(
            r'<div class="article-meta__dates">[^<]+</div>',
            f'<div class="article-meta__dates">{self.article_meta_dates_html()}</div>',
        )

    def patch_author_intro_card(self) -> None:
        """Update the author-intro card (photo, name, role)."""
        author = self.author_block()
        # Photo
        self._replace(
            r'<img[^>]*class="author-intro__photo"[^>]*>',
            f'<img src="{author["photo"]}" alt="{self._escape_attr(self.article.author_name)}" class="author-intro__photo">',
        )
        # Name
        self._replace(
            r'(<div class="author-intro__info">\s*<strong>)[^<]+(</strong>)',
            rf'\g<1>{self._escape_html(self.article.author_name)}\g<2>',
        )
        # Role
        self._replace(
            r'(<div class="author-intro__info">\s*<strong>[^<]+</strong>\s*<span>)[^<]+(</span>)',
            rf'\g<1>{self._escape_html(author["role_intro"])}\g<2>',
        )

    def patch_bottom_author_card(self) -> None:
        """Update the bottom author-card (initials + name + bio)."""
        author = self.author_block()
        self.html = re.sub(
            r'(<div class="author-card__avatar">)[A-Z]{2}(</div>)',
            rf'\g<1>{author["initials"]}\g<2>',
            self.html,
        )
        self.html = re.sub(
            r'(<div class="author-card__name">)[^<]+(</div>)',
            rf'\g<1>{self._escape_html(self.article.author_name)}\g<2>',
            self.html,
        )
        self.html = re.sub(
            r'(<div class="author-card__bio">)[^<]+(</div>)',
            rf'\g<1>{self._escape_html(author["bio_short"])}\g<2>',
            self.html,
        )

    def patch_main_content(self) -> None:
        """Replace V2 template's main content body with legacy article body."""
        body = self.article.article_body
        # Find <main class="prose"> ... </main> OR <main class="main-wrap"> ... </main> OR <main class="data-main">
        main_match = re.search(
            r'(<main class="(?:prose|main-wrap|data-main)"[^>]*>)(.*?)(</main>)',
            self.html,
            flags=re.DOTALL,
        )
        if not main_match:
            print("  ⚠ <main> container not found — can't inject body")
            return
        new_main = f'{main_match.group(1)}\n{body}\n{main_match.group(3)}'
        self.html = self.html[:main_match.start()] + new_main + self.html[main_match.end():]

    def patch_jsonld(self) -> None:
        """Replace V2 template's JSON-LD blocks with: our Article + BreadcrumbList + preserved (FAQ + ItemList)."""
        new_blocks = (
            '<script type="application/ld+json">\n'
            f'{self.updated_jsonld()}\n'
            '</script>\n\n'
            '<script type="application/ld+json">\n'
            f'{self.breadcrumb_jsonld()}\n'
            '</script>\n\n'
            f'{self.preserved_jsonld_blocks()}\n'
        )
        # Replace ALL existing application/ld+json blocks in V2 template with our new set
        self.html = re.sub(
            r'<script type="application/ld\+json">.*?</script>\s*',
            "",
            self.html,
            flags=re.DOTALL,
        )
        # Now insert new blocks right before </body>
        self.html = self.html.replace(
            "</body>",
            f"  {new_blocks}\n</body>",
            1,
        )

    def remove_migration_banner(self) -> None:
        """Strip the V2 PREVIEW BANNER (legacy from POC stage)."""
        self.html = re.sub(
            r'<!-- =+\s*V2 MIGRATION PREVIEW BANNER.*?</div>\s*',
            "",
            self.html,
            flags=re.DOTALL,
        )

    @staticmethod
    def _escape_html(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    @staticmethod
    def _escape_attr(s: str) -> str:
        return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

    def run(self) -> str:
        """Apply all patches in order; return final HTML."""
        self.patch_metadata()
        self.patch_hreflang()
        self.patch_og_tags()
        self.patch_h1()
        self.patch_lead()
        self.patch_article_meta()
        self.patch_author_intro_card()
        self.patch_bottom_author_card()
        self.patch_main_content()
        self.patch_jsonld()
        self.remove_migration_banner()
        return self.html


# ============================================================================
# RUNNER
# ============================================================================
def migrate_one(slug: str, out_dir: Path, verbose: bool = True) -> Path | None:
    legacy_path = LEGACY_DIR / f"{slug}.html"
    if not legacy_path.exists():
        print(f"  ✗ {slug}: legacy file not found at {legacy_path}")
        return None

    template_name = SLUG_TO_TEMPLATE.get(slug)
    if not template_name:
        print(f"  ✗ {slug}: no template mapping defined in SLUG_TO_TEMPLATE")
        return None

    template_path = TEMPLATE_DIR / template_name
    if not template_path.exists():
        print(f"  ✗ {slug}: template not found at {template_path}")
        return None

    article = LegacyArticle(legacy_path)
    migrator = V2TemplateMigrator(template_path, article)
    html = migrator.run()

    out_path = out_dir / f"{slug}.html"
    out_path.write_text(html, encoding="utf-8")

    if verbose:
        size_kb = out_path.stat().st_size / 1024
        print(f"  ✓ {slug}.html ({size_kb:.1f} KB) → {template_name}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slug", help="Migrate a single slug")
    parser.add_argument("--all", action="store_true", help="Migrate all 75 EN articles")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output dir (default: blog/_v2)")
    parser.add_argument("--list-mappings", action="store_true", help="Print slug→template mappings and exit")
    args = parser.parse_args()

    if args.list_mappings:
        print(f"Total slug mappings defined: {len(SLUG_TO_TEMPLATE)}")
        from collections import Counter
        counts = Counter(SLUG_TO_TEMPLATE.values())
        for tmpl, n in counts.most_common():
            print(f"  {n:>3}  {tmpl}")
        return

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.slug:
        slugs = [args.slug]
    elif args.all:
        slugs = list(SLUG_TO_TEMPLATE.keys())
    else:
        slugs = POC_SLUGS  # 5-article canary

    print(f"V2 migration — {len(slugs)} article(s)")
    print(f"  Source:    {LEGACY_DIR}")
    print(f"  Templates: {TEMPLATE_DIR}")
    print(f"  Output:    {out_dir}\n")

    ok, fail = 0, 0
    for i, slug in enumerate(slugs, 1):
        try:
            result = migrate_one(slug, out_dir)
            if result:
                ok += 1
            else:
                fail += 1
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
            fail += 1

    print(f"\nDone. {ok} migrated, {fail} failed.")
    if out_dir.name == "_v2":
        print("\nPreview locally:")
        print(f"  cd {REPO} && python3 -m http.server 8765")
        print(f"  open http://localhost:8765/blog/_v2/")


if __name__ == "__main__":
    main()
