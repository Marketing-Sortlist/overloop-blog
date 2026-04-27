#!/usr/bin/env python3
"""
Build ALL Spanish (ES) blog articles for the Overloop blog migration.
Same pipeline as FR — reads EN decisions, maps to ES slugs, pulls ES body content from Webflow CSV.
"""

import csv
import os
import re
import html
from datetime import datetime

# === PATHS ===
ES_CSV = "/Users/tanguy/Downloads/es-blog-webflow.csv"
MAPPING_CSV = "/Users/tanguy/Downloads/Overloop - blog export 14_04_26 - matching ID.csv"
DECISIONS_CSV = "/Users/tanguy/Documents/sortlist/overloop-blog/redirects/redirects.csv"
NAV_HTML = "/Users/tanguy/Documents/sortlist/overloop-blog/assets/nav.html"
FOOTER_HTML = "/Users/tanguy/Documents/sortlist/overloop-blog/assets/footer.html"
OUTPUT_DIR = "/Users/tanguy/Documents/sortlist/overloop-blog/blog/es"

# === SPANISH MONTH NAMES ===
ES_MONTHS = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def format_date_es(date_str):
    """Convert Webflow date string to Spanish format: '10 de abril de 2026'"""
    if not date_str:
        return "15 de abril de 2026"
    try:
        # Parse various Webflow date formats
        # "Sun Jun 15 2025 23:0" or "Thu Dec 11 2025 14:3" etc.
        # Try to extract date parts
        parts = date_str.strip().split()
        if len(parts) >= 4:
            month_str = parts[1]
            day = int(parts[2])
            year = int(parts[3])
            month_map = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            month_num = month_map.get(month_str, 1)
            return f"{day} de {ES_MONTHS[month_num]} de {year}"
    except:
        pass
    return "15 de abril de 2026"

def format_date_iso(date_str):
    """Convert Webflow date string to ISO format: '2026-04-15'"""
    if not date_str:
        return "2026-04-15"
    try:
        parts = date_str.strip().split()
        if len(parts) >= 4:
            month_str = parts[1]
            day = int(parts[2])
            year = int(parts[3])
            month_map = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            month_num = month_map.get(month_str, 1)
            return f"{year}-{month_num:02d}-{day:02d}"
    except:
        pass
    return "2026-04-15"


def clean_webflow_html(body):
    """Clean Webflow body HTML: remove empty id attributes, fix links, clean up."""
    if not body:
        return ""

    # Remove empty id="" attributes
    body = re.sub(r'\s+id=""', '', body)
    body = re.sub(r'\s+id="[^"]*"', '', body)

    # Remove Webflow-specific attributes
    body = re.sub(r'\s+class="w-[^"]*"', '', body)

    # Fix double quotes in attributes
    body = body.replace('""', '"')

    # Remove empty paragraphs
    body = re.sub(r'<p>\s*</p>', '', body)

    # Remove empty divs
    body = re.sub(r'<div>\s*</div>', '', body)

    # Fix rel="noindex nofollow" -> rel="nofollow"
    body = body.replace('rel="noindex nofollow"', 'rel="nofollow"')

    # Fix relative links to overloop features
    body = re.sub(r'href="/features"', 'href="https://overloop.com/features"', body)
    body = re.sub(r'href="/pricing"', 'href="https://overloop.com/pricing"', body)
    body = re.sub(r'href="/blog"', 'href="https://overloop.com/blog"', body)

    return body.strip()


def get_author_info(author_slug):
    """Return author name, role (ES), LinkedIn URL, image file, credentials."""
    authors = {
        'nicolas-finet': {
            'name': 'Nicolas Finet',
            'role': 'CEO en Overloop',
            'linkedin': 'https://www.linkedin.com/in/nicolasfinet/',
            'image': 'nicolas-finet.png',
            'credentials': 'CEO de Sortlist & Overloop. Ha construido sistemas outbound para mas de 500 empresas B2B.'
        },
        'vincenzo-ruggiero': {
            'name': 'Vincenzo Ruggiero',
            'role': 'Redactor en Overloop',
            'linkedin': 'https://www.linkedin.com/in/vincenzo-ruggiero/',
            'image': 'nicolas-finet.png',
            'credentials': 'Experto en ventas outbound y automatizacion B2B.'
        },
        'forster-perelsztejn': {
            'name': 'Forster Perelsztejn',
            'role': 'Redactor en Overloop',
            'linkedin': 'https://www.linkedin.com/in/forster-perelsztejn/',
            'image': 'nicolas-finet.png',
            'credentials': 'Especialista en cold email y estrategia de prospección B2B.'
        },
        'alexandra-tallon': {
            'name': 'Alexandra Tallon',
            'role': 'Redactora en Overloop',
            'linkedin': 'https://www.linkedin.com/company/overloop-ai/',
            'image': 'nicolas-finet.png',
            'credentials': 'Especialista en estrategia de outbound sales.'
        },
        'gabka-ko-ov': {
            'name': 'Gabka Kosova',
            'role': 'Redactora en Overloop',
            'linkedin': 'https://www.linkedin.com/company/overloop-ai/',
            'image': 'nicolas-finet.png',
            'credentials': 'Especialista en cold email y link building.'
        },
        'carina-gotovcenco': {
            'name': 'Carina Gotovcenco',
            'role': 'Redactora en Overloop',
            'linkedin': 'https://www.linkedin.com/company/overloop-ai/',
            'image': 'nicolas-finet.png',
            'credentials': 'Especialista en funcionalidades de la plataforma Overloop.'
        },
        'claudia-martinez': {
            'name': 'Claudia Martinez',
            'role': 'Redactora en Overloop',
            'linkedin': 'https://www.linkedin.com/company/overloop-ai/',
            'image': 'nicolas-finet.png',
            'credentials': 'Especialista en ventas y automatizacion.'
        },
        'jazmin-villarino': {
            'name': 'Jazmin Villarino',
            'role': 'Redactora en Overloop',
            'linkedin': 'https://www.linkedin.com/company/overloop-ai/',
            'image': 'nicolas-finet.png',
            'credentials': 'Especialista en contenidos de ventas B2B.'
        },
    }

    # Normalize slug
    slug = (author_slug or '').strip().lower()
    if slug in authors:
        return authors[slug]

    # Default to Nicolas Finet
    return authors['nicolas-finet']


def truncate_title(title, max_len=60):
    """Ensure meta title is under max_len chars (with ' | Overloop' suffix)."""
    suffix = " | Overloop"
    available = max_len - len(suffix)
    if len(title) <= available:
        return title
    # Truncate at word boundary
    truncated = title[:available-3].rsplit(' ', 1)[0] + "..."
    return truncated


def make_meta_description(seo_desc, body, target_min=130, target_max=155):
    """Create meta description 130-155 chars."""
    desc = (seo_desc or '').strip()
    if desc:
        # Strip HTML
        desc = re.sub(r'<[^>]+>', '', desc)
        desc = html.unescape(desc)
        if len(desc) >= target_min and len(desc) <= target_max:
            return desc
        if len(desc) > target_max:
            desc = desc[:target_max-3].rsplit(' ', 1)[0] + "..."
            return desc
        if len(desc) >= 80:
            return desc  # Accept shorter if it's reasonable

    # Fallback: extract from body
    if body:
        text = re.sub(r'<[^>]+>', '', body)
        text = html.unescape(text).strip()
        text = re.sub(r'\s+', ' ', text)
        if len(text) > target_max:
            text = text[:target_max-3].rsplit(' ', 1)[0] + "..."
        return text[:target_max]

    return desc or "Descubre estrategias de ventas outbound y automatizacion para equipos B2B."


def count_table_rows(body):
    """Count rows in tables to decide if table-keep class is needed."""
    # Find all tables and count their rows
    tables = re.findall(r'<table[^>]*>(.*?)</table>', body, re.DOTALL)
    results = []
    for table in tables:
        rows = len(re.findall(r'<tr', table))
        results.append(rows)
    return results


def add_table_keep_class(body):
    """Add class='table-keep' to tables with 15+ rows."""
    def replace_table(match):
        table_content = match.group(0)
        rows = len(re.findall(r'<tr', table_content))
        if rows >= 15:
            # Add or replace class
            if 'class=' in table_content[:50]:
                return re.sub(r'<table([^>]*?)class="([^"]*)"', r'<table\1class="\2 table-keep"', table_content, count=1)
            else:
                return table_content.replace('<table', '<table class="table-keep"', 1)
        return table_content

    return re.sub(r'<table[^>]*>.*?</table>', replace_table, body, flags=re.DOTALL)


def build_hreflang_tags(en_slug, slug_mapping):
    """Build hreflang link tags for all available languages."""
    slugs = slug_mapping.get(en_slug, {})
    tags = []

    en = slugs.get('en', en_slug)
    fr = slugs.get('fr', '')
    de = slugs.get('de', '')
    es = slugs.get('es', '')

    if en:
        tags.append(f'    <link rel="alternate" hreflang="en" href="https://overloop.com/blog/{en}">')
    if fr:
        tags.append(f'    <link rel="alternate" hreflang="fr" href="https://overloop.com/fr/blog/{fr}">')
    if de:
        tags.append(f'    <link rel="alternate" hreflang="de" href="https://overloop.com/de/blog/{de}">')
    if es:
        tags.append(f'    <link rel="alternate" hreflang="es" href="https://overloop.com/es/blog/{es}">')
    if en:
        tags.append(f'    <link rel="alternate" hreflang="x-default" href="https://overloop.com/blog/{en}">')

    return '\n'.join(tags)


def build_article_html(es_row, en_slug, es_slug, slug_mapping, nav_html, footer_html):
    """Build complete HTML for one ES article."""

    title = (es_row.get('Title', '') or '').strip()
    body = (es_row.get('Post Body', '') or '').strip()
    seo_desc = (es_row.get('Seo Description', '') or '').strip()
    author_slug = (es_row.get('Authors', '') or '').strip()
    pub_date = (es_row.get('Publication date', '') or '').strip()
    reading_time = (es_row.get('Reading time', '') or '').strip() or '10'
    category = (es_row.get('Category', '') or '').strip()

    # Clean body
    body = clean_webflow_html(body)
    body = add_table_keep_class(body)

    # Author info
    author = get_author_info(author_slug)

    # Dates
    date_es = format_date_es(pub_date)
    date_iso = format_date_iso(pub_date)
    date_modified = "2026-04-17"

    # Meta title (< 60 chars)
    meta_title = truncate_title(title)

    # Meta description (130-155 chars)
    meta_desc = make_meta_description(seo_desc, body)

    # Hreflang tags
    hreflang_tags = build_hreflang_tags(en_slug, slug_mapping)

    # Escape for JSON-LD
    json_title = html.escape(title, quote=True)
    json_desc = html.escape(meta_desc, quote=True)

    # Build HTML
    article_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/overloop-blog/assets/css/overloop.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(meta_title)} | Overloop</title>
    <meta name="description" content="{html.escape(meta_desc)}">
    <link rel="canonical" href="https://overloop.com/es/blog/{es_slug}">

{hreflang_tags}

    <meta property="og:title" content="{html.escape(meta_title)}">
    <meta property="og:description" content="{html.escape(meta_desc)}">
    <meta property="og:image" content="https://sortlist.github.io/overloop-blog/assets/images/og/{es_slug}.png">
    <meta property="og:url" content="https://overloop.com/es/blog/{es_slug}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(meta_title)}">
    <meta name="twitter:description" content="{html.escape(meta_desc)}">
    <meta name="twitter:image" content="https://sortlist.github.io/overloop-blog/assets/images/og/{es_slug}.png">
<script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "{json_title}",
        "description": "{json_desc}",
        "image": "https://overloop.com/assets/images/og-{es_slug}.png",
        "author": {{
            "@type": "Person",
            "name": "{author['name']}",
            "url": "{author['linkedin']}"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Overloop",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://overloop.com/assets/images/overloop-logo.png"
            }}
        }},
        "datePublished": "{date_iso}",
        "dateModified": "{date_modified}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://overloop.com/es/blog/{es_slug}"
        }}
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Blog", "item": "https://overloop.com/es/blog"}},
            {{"@type": "ListItem", "position": 2, "name": "{json_title}", "item": "https://overloop.com/es/blog/{es_slug}"}}
        ]
    }}
    </script>
</head>
<body>

{nav_html}

<main class="blog-post">
    <div class="container">

        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="https://overloop.com">Overloop</a> &rsaquo;
            <a href="https://overloop.com/es/blog">Blog</a> &rsaquo;
            <span>{html.escape(title)}</span>
        </nav>

        <header class="article-header">
            <h1>{html.escape(title)}</h1>
        </header>

        <div class="article-meta">
            <img class="meta-avatar" src="/overloop-blog/assets/images/{author['image']}" alt="{author['name']}" width="44" height="44" style="border-radius:50%;object-fit:cover;">
            <div class="meta-info">
                <strong>{author['name']}</strong>
                <span>|</span> {date_es}
                <span>|</span> {reading_time} min de lectura
            </div>
        </div>

        <article class="article-content">
{body}
        </article>

        <div class="cta-box">
            <h3>&iquest;Listo para automatizar tu prospecci&oacute;n?</h3>
            <p>Overloop combina una base de datos de 450M+ contactos B2B, redacci&oacute;n IA y secuencias multicanal en una sola plataforma.</p>
            <a href="https://app.overloop.ai/session/signup" class="cta-button">Probar Overloop gratis</a>
        </div>

        <div class="author-bio">
            <img src="/overloop-blog/assets/images/{author['image']}" alt="{author['name']}" width="56" height="56" loading="lazy">
            <div>
                <div class="name">{author['name']}</div>
                <div class="role">{author['role']}</div>
                <div class="role">{author['credentials']}</div>
            </div>
        </div>

    </div>
</main>

{footer_html}

<script src="/overloop-blog/assets/js/blog.js" defer></script>
</body>
</html>"""

    return article_html


def main():
    # 1. Read EN decisions
    decisions = {}
    with open(DECISIONS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            action = row['action'].strip()
            if action in ('MIGRATE', 'REWRITE'):
                slug = row['slug_keyword'].strip()
                decisions[slug] = action

    print(f"[1] EN decisions loaded: {len(decisions)} MIGRATE+REWRITE articles")

    # 2. Load EN->ES slug mapping (+ FR, DE for hreflang)
    slug_mapping = {}
    en_to_es = {}
    with open(MAPPING_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            en = row['Slug /en'].strip()
            fr = row.get('Slug /fr', '').strip()
            de = row.get('Slug /de', '').strip()
            es = row.get('Slug /es', '').strip()

            slug_mapping[en] = {
                'en': en,
                'fr': fr if fr != '#N/A' else '',
                'de': de if de != '#N/A' else '',
                'es': es if es != '#N/A' else ''
            }
            if es and es != '#N/A':
                en_to_es[en] = es

    print(f"[2] Slug mapping loaded: {len(en_to_es)} EN->ES mappings")

    # 3. Load ES content from Webflow CSV
    es_content = {}
    with open(ES_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row['Slug'].strip()
            es_content[slug] = row

    print(f"[3] ES content loaded: {len(es_content)} articles")

    # 4. Load nav and footer
    with open(NAV_HTML, 'r') as f:
        nav_html = f.read().strip()
    with open(FOOTER_HTML, 'r') as f:
        footer_html = f.read().strip()

    # 5. Ensure output dir exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 6. Build articles
    built = 0
    skipped = []
    old_files_to_delete = []

    for en_slug, action in sorted(decisions.items()):
        es_slug = en_to_es.get(en_slug)
        if not es_slug:
            skipped.append(f"  SKIP (no ES slug): {en_slug}")
            continue

        es_row = es_content.get(es_slug)
        if not es_row:
            skipped.append(f"  SKIP (no ES content): {en_slug} -> {es_slug}")
            continue

        # Check if body is empty
        body = (es_row.get('Post Body', '') or '').strip()
        if not body or len(body) < 100:
            skipped.append(f"  SKIP (empty body): {en_slug} -> {es_slug}")
            continue

        # Build HTML
        article_html = build_article_html(es_row, en_slug, es_slug, slug_mapping, nav_html, footer_html)

        # Write to file
        output_path = os.path.join(OUTPUT_DIR, f"{es_slug}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(article_html)

        built += 1
        print(f"  [{built}] {action}: {es_slug}.html ({len(article_html):,} bytes)")

        # Track old EN-slug files that should be deleted
        old_file = os.path.join(OUTPUT_DIR, f"{en_slug}.html")
        if en_slug != es_slug and os.path.exists(old_file):
            old_files_to_delete.append((en_slug, old_file))

    print(f"\n[SUMMARY]")
    print(f"  Built: {built} articles")
    print(f"  Skipped: {len(skipped)}")
    for s in skipped:
        print(s)

    # 7. Delete old EN-slug files replaced by ES-slug files
    if old_files_to_delete:
        print(f"\n[CLEANUP] Deleting {len(old_files_to_delete)} old EN-slug files:")
        for en_slug, path in old_files_to_delete:
            os.remove(path)
            print(f"  DELETED: {en_slug}.html")
    else:
        print(f"\n[CLEANUP] No old EN-slug files to delete.")

    # 8. List all files now in ES dir
    es_files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.html')])
    print(f"\n[FINAL] {len(es_files)} files in {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
