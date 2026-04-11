#!/usr/bin/env python3
"""
Propagate the new Overloop blog design (nav, footer, breadcrumbs, Playfair Display,
overloop.css) to all 57 DE/FR/ES blog articles.

This script:
1. Adds Google Fonts preconnect + link tags in <head>
2. Adds overloop.css link
3. Removes old inline <style> blocks (the full old design system)
4. Injects nav HTML after <body>
5. Adds breadcrumb bar between nav and article content
6. Restructures header to use dark gradient article-header
7. Injects footer HTML before </body>
8. Adds blog.js script tag
9. Fixes internal links to use /{lang}/blog/ paths
10. Humanizes dates per locale
"""

import os
import re
import glob
import html

# ---------- CONFIG ----------
BLOG_ROOT = "/tmp/overloop-blog/blog"
ASSETS_ROOT = "/tmp/overloop-blog/assets"
LANGUAGES = ["de", "fr", "es"]

# Date mappings
MONTHS_DE = {
    "01": "Januar", "02": "Februar", "03": "M\u00e4rz", "04": "April",
    "05": "Mai", "06": "Juni", "07": "Juli", "08": "August",
    "09": "September", "10": "Oktober", "11": "November", "12": "Dezember"
}
MONTHS_FR = {
    "01": "janvier", "02": "f\u00e9vrier", "03": "mars", "04": "avril",
    "05": "mai", "06": "juin", "07": "juillet", "08": "ao\u00fbt",
    "09": "septembre", "10": "octobre", "11": "novembre", "12": "d\u00e9cembre"
}
MONTHS_ES = {
    "01": "enero", "02": "febrero", "03": "marzo", "04": "abril",
    "05": "mayo", "06": "junio", "07": "julio", "08": "agosto",
    "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"
}


def format_date_de(date_str):
    """2026-04-10 -> 10. April 2026"""
    parts = date_str.split("-")
    if len(parts) != 3:
        return date_str
    y, m, d = parts
    month = MONTHS_DE.get(m, m)
    return f"{int(d)}. {month} {y}"


def format_date_fr(date_str):
    """2026-04-10 -> 10 avril 2026"""
    parts = date_str.split("-")
    if len(parts) != 3:
        return date_str
    y, m, d = parts
    month = MONTHS_FR.get(m, m)
    return f"{int(d)} {month} {y}"


def format_date_es(date_str):
    """2026-04-10 -> 10 de abril de 2026"""
    parts = date_str.split("-")
    if len(parts) != 3:
        return date_str
    y, m, d = parts
    month = MONTHS_ES.get(m, m)
    return f"{int(d)} de {month} de {y}"


DATE_FORMATTERS = {"de": format_date_de, "fr": format_date_fr, "es": format_date_es}


def load_asset(name):
    path = os.path.join(ASSETS_ROOT, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


# Load nav and footer HTML
NAV_HTML = load_asset("nav.html")
FOOTER_HTML = load_asset("footer.html")

# Google Fonts tags to inject
GOOGLE_FONTS_TAGS = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">"""

CSS_LINK = '    <link rel="stylesheet" href="/assets/css/overloop.css">'
JS_TAG = '<script src="/assets/js/blog.js" defer></script>'


def extract_title_from_h1(content):
    """Extract the text content of the first <h1> tag."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
    if m:
        # Strip HTML tags from inside h1
        raw = re.sub(r"<[^>]+>", "", m.group(1))
        # Decode HTML entities
        raw = html.unescape(raw)
        return raw.strip()
    return ""


def extract_short_title(full_title):
    """Create a short breadcrumb title from the full h1 title.
    Remove year references, parentheticals, and trailing descriptors."""
    short = full_title
    # Remove parenthetical content
    short = re.sub(r"\s*\([^)]*\)\s*", " ", short)
    # Remove year patterns like "2026" at the end
    short = re.sub(r"\s+20\d{2}\s*$", "", short)
    # Take the part before a colon if it exists (for titles like "X: Y Z")
    if ":" in short:
        short = short.split(":")[0].strip()
    # Truncate if still too long (>50 chars)
    if len(short) > 50:
        short = short[:47] + "..."
    return short.strip()


def extract_breadcrumb_title_from_old(content):
    """Try to extract the breadcrumb title from old nav.breadcrumb block."""
    m = re.search(
        r'<nav\s+class="breadcrumb">\s*'
        r'<a[^>]*>Overloop</a>\s*&rsaquo;\s*'
        r'<a[^>]*>Blog</a>\s*&rsaquo;\s*'
        r'(.*?)\s*</nav>',
        content,
        re.DOTALL,
    )
    if m:
        title = m.group(1).strip()
        title = re.sub(r"<[^>]+>", "", title)
        title = html.unescape(title)
        return title.strip()
    return None


def remove_old_inline_style(content):
    """Remove the old design system <style> block.
    This matches the large inline style block that defines the old design.
    We identify it by looking for the :root CSS variable block pattern."""
    # Match <style> blocks containing the old design system (with :root vars)
    pattern = r'\s*<style>\s*:root\s*\{[^}]*--color-primary[^}]*\}.*?</style>'
    content = re.sub(pattern, "", content, flags=re.DOTALL)
    return content


def remove_old_font_preload(content):
    """Remove old font preload link that's no longer needed."""
    content = re.sub(
        r'\s*<link\s+rel="preload"\s+href="/assets/fonts/inter\.woff2"[^>]*>',
        "",
        content,
    )
    return content


def add_google_fonts(content):
    """Add Google Fonts tags after <meta charset> if not already present."""
    if "Playfair+Display" in content or "Playfair Display" in content:
        return content  # Already has Playfair Display

    # Insert after <meta charset="UTF-8">
    content = re.sub(
        r'(<meta\s+charset="UTF-8"\s*/?>)',
        r"\1\n" + GOOGLE_FONTS_TAGS,
        content,
        count=1,
    )
    return content


def add_css_link(content):
    """Add overloop.css link if not already present."""
    if "overloop.css" in content:
        return content
    # Insert after Google Fonts (or after charset if fonts weren't added)
    # Place it after the last font link or after charset
    if "Playfair+Display" in content:
        # Insert after the Google Fonts stylesheet link
        content = re.sub(
            r'(href="https://fonts\.googleapis\.com/css2\?family=Playfair\+Display[^"]*"\s+rel="stylesheet">)',
            r"\1\n" + CSS_LINK,
            content,
            count=1,
        )
    else:
        # Insert after charset
        content = re.sub(
            r'(<meta\s+charset="UTF-8"\s*/?>)',
            r"\1\n" + CSS_LINK,
            content,
            count=1,
        )
    return content


def restructure_body(content, lang, filepath):
    """Major restructuring: replace old body structure with new nav+breadcrumb+header+footer."""

    # Determine blog link path prefix
    lang_prefix = f"/{lang}/blog"

    # Extract breadcrumb title from old structure or from h1
    breadcrumb_title = extract_breadcrumb_title_from_old(content)
    if not breadcrumb_title:
        breadcrumb_title = extract_short_title(extract_title_from_h1(content))

    # Extract h1 and article-meta from old header
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
    h1_content = h1_match.group(1).strip() if h1_match else "Article"

    meta_match = re.search(
        r'<div\s+class="article-meta">(.*?)</div>',
        content,
        re.DOTALL,
    )
    meta_content = meta_match.group(1).strip() if meta_match else ""

    # Extract the subtitle from meta if it looks like "Von ... · Published ... · Updated ..."
    # We'll extract the parts to build the new meta line

    # --- Step 1: Check if already has new nav ---
    if '<nav class="nav">' in content:
        return content  # Already migrated

    # --- Step 2: Remove old body>container>breadcrumb structure ---
    # Old pattern: <body>\n    <div class="container">\n        <nav class="breadcrumb">...</nav>\n\n        <header class="article-header">

    # Remove the opening <div class="container"> wrapper right after <body>
    # and the old breadcrumb nav

    # First, extract everything between </head> and the article content
    # Old structure:
    #   </head>
    #   <body>
    #       <div class="container">
    #           <nav class="breadcrumb">...</nav>
    #           <header class="article-header">
    #               <h1>...</h1>
    #               <div class="article-meta">...</div>
    #           </header>
    #           <article class="article-content">
    #               ... article body ...
    #           </article>
    #           ... (cta-box, author-bio, related-posts) ...
    #       </div>
    #   </body>

    # New structure:
    #   </head>
    #   <body>
    #   <!-- nav -->
    #   <div class="breadcrumb-bar">...</div>
    #   <header class="article-header">
    #       <span class="header-badge">Short Title</span>
    #       <h1>...</h1>
    #       <p class="subtitle">...</p>
    #   </header>
    #   <main class="article-body">
    #       <div class="container">
    #           <div class="article-meta">...</div>
    #           <article class="article-content">
    #               ...
    #           </article>
    #           ... (cta-box, author-bio, related-posts) ...
    #       </div>
    #   </main>
    #   <!-- footer -->
    #   <script src="/assets/js/blog.js" defer></script>
    #   </body>

    # Strategy: parse the body section and rebuild it

    # Split at <body> and </body>
    body_start = content.find("<body>")
    body_end = content.find("</body>")
    if body_start == -1 or body_end == -1:
        print(f"  WARNING: Could not find <body> tags in {filepath}")
        return content

    head_part = content[:body_start + len("<body>")]
    body_content = content[body_start + len("<body>"):body_end]
    tail_part = content[body_end:]  # </body></html>

    # Remove the old opening <div class="container">
    body_content = re.sub(r'^\s*<div\s+class="container">\s*', '\n', body_content, count=1)

    # Remove old breadcrumb nav
    body_content = re.sub(
        r'\s*<nav\s+class="breadcrumb">.*?</nav>\s*',
        '\n',
        body_content,
        flags=re.DOTALL,
        count=1,
    )

    # Remove old <header class="article-header"> and extract its content
    header_match = re.search(
        r'<header\s+class="article-header">\s*(.*?)\s*</header>',
        body_content,
        re.DOTALL,
    )
    if header_match:
        old_header_inner = header_match.group(1)
        body_content = body_content[:header_match.start()] + "<!-- HEADER_PLACEHOLDER -->" + body_content[header_match.end():]
    else:
        old_header_inner = ""

    # Wrap article content in <main class="article-body"><div class="container">
    # Find the <article class="article-content"> start
    article_start = body_content.find('<article class="article-content">')
    if article_start == -1:
        article_start = body_content.find("<!-- HEADER_PLACEHOLDER -->")
        if article_start != -1:
            article_start += len("<!-- HEADER_PLACEHOLDER -->")

    # Find the closing </div> that was the container wrapper (at the very end)
    # Remove closing </div> for old container
    # The old structure ends with: </div>\n</div>\n  (related-posts div + container div)
    # We need to remove just the outermost container closing </div>
    body_content_stripped = body_content.rstrip()
    if body_content_stripped.endswith("</div>"):
        # Remove the last </div> which was the container wrapper
        last_div = body_content.rfind("</div>")
        body_content = body_content[:last_div] + body_content[last_div + len("</div>"):]

    # Now replace the HEADER_PLACEHOLDER with the new structure
    # Build the new meta line from old meta content
    new_meta = meta_content

    # Build new header
    new_header = f"""<header class="article-header">
    <span class="header-badge">{html.escape(breadcrumb_title)}</span>
    <h1>{h1_content}</h1>
</header>"""

    # Build breadcrumb bar
    breadcrumb_bar = f"""
<div class="breadcrumb-bar">
    <div class="container">
        <a href="https://overloop.com">Overloop</a>
        <span class="sep">/</span>
        <a href="/{lang}/blog">Blog</a>
        <span class="sep">/</span>
        <span class="current">{html.escape(breadcrumb_title)}</span>
    </div>
</div>
"""

    # Replace placeholder and wrap in main
    if "<!-- HEADER_PLACEHOLDER -->" in body_content:
        parts = body_content.split("<!-- HEADER_PLACEHOLDER -->", 1)
        before_header = parts[0]
        after_header = parts[1]

        # Build article meta div for inside main
        meta_div = f"""
        <div class="article-meta">
            <div class="meta-avatar">NF</div>
            <div class="meta-info">
                {new_meta}
            </div>
        </div>
"""

        new_body = f"""
{NAV_HTML}
{breadcrumb_bar}
{new_header}

<main class="article-body">
    <div class="container">
{meta_div}
{after_header.rstrip()}
    </div>
</main>

{FOOTER_HTML}

{JS_TAG}
"""
    else:
        # Fallback: just wrap everything
        new_body = f"""
{NAV_HTML}
{breadcrumb_bar}
{new_header}

<main class="article-body">
    <div class="container">
{body_content.rstrip()}
    </div>
</main>

{FOOTER_HTML}

{JS_TAG}
"""

    result = head_part + new_body + "\n</body>\n</html>"
    return result


def fix_internal_links(content, lang):
    """Fix internal blog links to use correct language prefix.
    /blog/de/slug -> /de/blog/slug
    /blog/fr/slug -> /fr/blog/slug
    /blog/es/slug -> /es/blog/slug
    """
    # Fix /blog/{lang}/ pattern to /{lang}/blog/
    for l in LANGUAGES:
        content = content.replace(f'href="/blog/{l}/', f'href="/{l}/blog/')
    return content


def humanize_dates(content, lang):
    """Replace ISO dates (YYYY-MM-DD) with localized format in visible text.
    Only replace dates in visible text, not in structured data or meta tags."""
    formatter = DATE_FORMATTERS[lang]

    # Find all ISO date patterns and replace them in article text
    # But be careful not to replace dates in JSON-LD or meta tags

    # Strategy: replace dates that appear in the visible content areas
    # (article-meta, article-content) but not in <script> or <meta> tags

    def replace_date_in_text(match):
        date_str = match.group(0)
        return formatter(date_str)

    # Split content into segments: script blocks and non-script blocks
    segments = re.split(r'(<script[^>]*>.*?</script>|<meta[^>]*>|<link[^>]*>)', content, flags=re.DOTALL)

    result = []
    for i, segment in enumerate(segments):
        if segment and (segment.startswith("<script") or segment.startswith("<meta") or segment.startswith("<link")):
            result.append(segment)
        else:
            # Replace dates in non-script/meta content
            # Match YYYY-MM-DD patterns (but not in href or src attributes)
            # Use a lookbehind/lookahead to avoid replacing in URLs
            segment = re.sub(
                r'(?<!href=")(?<!src=")(?<!content=")(?<!item":\s")(?<!/)\b(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b(?!/)',
                lambda m: formatter(m.group(0)),
                segment,
            )
            result.append(segment)

    return "".join(result)


def process_file(filepath, lang):
    """Process a single blog article file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    filename = os.path.basename(filepath)

    # Step 1: Remove old inline style
    content = remove_old_inline_style(content)

    # Step 2: Remove old font preload
    content = remove_old_font_preload(content)

    # Step 3: Add Google Fonts
    content = add_google_fonts(content)

    # Step 4: Add CSS link
    content = add_css_link(content)

    # Step 5: Restructure body (nav, breadcrumb, header, footer, script)
    content = restructure_body(content, lang, filepath)

    # Step 6: Fix internal links
    content = fix_internal_links(content, lang)

    # Step 7: Humanize dates
    content = humanize_dates(content, lang)

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    changed = content != original
    return changed


def main():
    total = 0
    changed = 0
    errors = 0

    for lang in LANGUAGES:
        lang_dir = os.path.join(BLOG_ROOT, lang)
        files = sorted(glob.glob(os.path.join(lang_dir, "*.html")))
        print(f"\n--- Processing {lang.upper()} ({len(files)} files) ---")

        for filepath in files:
            filename = os.path.basename(filepath)
            total += 1
            try:
                was_changed = process_file(filepath, lang)
                status = "UPDATED" if was_changed else "SKIPPED (already migrated)"
                print(f"  [{status}] {lang}/{filename}")
                if was_changed:
                    changed += 1
            except Exception as e:
                errors += 1
                print(f"  [ERROR] {lang}/{filename}: {e}")
                import traceback
                traceback.print_exc()

    print(f"\n=== DONE: {total} files processed, {changed} updated, {errors} errors ===")


if __name__ == "__main__":
    main()
