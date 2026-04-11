#!/usr/bin/env python3
"""Inject breadcrumb bar into all EN articles."""
import os, re

ARTICLES_DIR = "/tmp/overloop-blog/blog/en"

# Short titles for breadcrumbs
SHORT_TITLES = {
    "11-best-ai-bdr-tools": "AI BDR Tools",
    "455-email-spam-trigger-words-avoid-2018": "Spam Trigger Words",
    "500-trigger-words": "Trigger Words",
    "8-best-ai-linkedin-outreach-tools": "LinkedIn Outreach Tools",
    "9-best-ai-email-outreach-tools": "Email Outreach Tools",
    "apollo-alternatives": "Apollo Alternatives",
    "best-ai-sales-tools": "Best AI Sales Tools",
    "cold-email-illegal": "Cold Email Legal Guide",
    "cold-email-stats-2018": "Cold Email Statistics",
    "cold-emailing-link-building": "Cold Email Link Building",
    "get-email-from-linkedin-profile": "Get Email from LinkedIn",
    "how-to-find-someone-email-address-efficiently": "Find Email Addresses",
    "instantly-alternatives": "Instantly Alternatives",
    "la-growth-machine-review": "La Growth Machine Review",
    "lemlist-alternatives": "Lemlist Alternatives",
    "linkedin-helper-review": "LinkedIn Helper Review",
    "outreach-alternatives": "Outreach Alternatives",
    "salesloft-alternatives": "Salesloft Alternatives",
    "whats-the-best-email-length-for-sales-outreach": "Cold Email Length",
}

BREADCRUMB_TPL = """<div class="breadcrumb-bar">
    <div class="container">
        <a href="https://overloop.com">Overloop</a>
        <span class="sep">/</span>
        <a href="/blog/en/">Blog</a>
        <span class="sep">/</span>
        <span class="current">{title}</span>
    </div>
</div>"""

for fname in os.listdir(ARTICLES_DIR):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, "r") as f:
        content = f.read()

    # Skip if already has breadcrumb
    if "breadcrumb-bar" in content:
        print(f"  SKIP (already has breadcrumb): {fname}")
        continue

    slug = fname.replace(".html", "")
    title = SHORT_TITLES.get(slug, slug.replace("-", " ").title())
    breadcrumb = BREADCRUMB_TPL.format(title=title)

    # Insert between </nav> and <header
    content = content.replace("</nav>\n\n<header", f"</nav>\n\n{breadcrumb}\n\n<header", 1)
    if "</nav>\n<header" in content:
        content = content.replace("</nav>\n<header", f"</nav>\n\n{breadcrumb}\n\n<header", 1)

    with open(fpath, "w") as f:
        f.write(content)
    print(f"  OK: {fname} -> {title}")

print("Done!")
