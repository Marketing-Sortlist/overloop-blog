#!/usr/bin/env python3
"""
Full audit of the Overloop blog repo before launch.
Checks: HTML structure, SEO tags, internal links, assets, accessibility, consistency.
"""
import os, re, json
from collections import defaultdict

BLOG_DIR = "/tmp/overloop-blog/blog"
ASSETS_DIR = "/tmp/overloop-blog/assets"
ERRORS = []
WARNINGS = []
STATS = defaultdict(int)

def error(file, msg):
    ERRORS.append(f"ERROR [{file}] {msg}")

def warn(file, msg):
    WARNINGS.append(f"WARN  [{file}] {msg}")

def audit_html(filepath):
    rel = filepath.replace("/tmp/overloop-blog/", "")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    STATS["total_files"] += 1
    STATS["total_lines"] += content.count("\n")

    # === STRUCTURE ===
    if "<!DOCTYPE html>" not in content and "<!doctype html>" not in content:
        error(rel, "Missing <!DOCTYPE html>")
    if "</html>" not in content:
        error(rel, "Missing </html> closing tag")
    if "</body>" not in content:
        error(rel, "Missing </body> closing tag")
    if "</head>" not in content:
        error(rel, "Missing </head> closing tag")

    # === SEO TAGS ===
    # Title
    title_match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    if not title_match:
        error(rel, "Missing <title> tag")
    else:
        title = title_match.group(1).strip()
        if len(title) > 70:
            warn(rel, f"Title too long ({len(title)} chars): {title[:60]}...")
        if len(title) < 20:
            warn(rel, f"Title too short ({len(title)} chars): {title}")
        STATS["has_title"] += 1

    # Meta description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    if not desc_match:
        error(rel, "Missing meta description")
    else:
        desc = desc_match.group(1)
        if len(desc) > 160:
            warn(rel, f"Meta description too long ({len(desc)} chars)")
        if len(desc) < 50:
            warn(rel, f"Meta description too short ({len(desc)} chars)")
        STATS["has_meta_desc"] += 1

    # Canonical
    if 'rel="canonical"' in content:
        STATS["has_canonical"] += 1
        canonical_match = re.search(r'rel="canonical" href="(.*?)"', content)
        if canonical_match:
            canonical = canonical_match.group(1)
            if "/blog/en/" in canonical:
                error(rel, f"Canonical contains /blog/en/ (should be /blog/): {canonical}")
    else:
        error(rel, "Missing canonical tag")

    # Hreflang
    hreflang_count = content.count('hreflang=')
    if hreflang_count > 0:
        STATS["has_hreflang"] += 1
        if hreflang_count < 4:
            warn(rel, f"Only {hreflang_count} hreflang tags (expected 4+)")

    # OG tags
    if 'og:title' in content:
        STATS["has_og"] += 1
    else:
        warn(rel, "Missing og:title")

    # === SCHEMA MARKUP ===
    schemas = re.findall(r'application/ld\+json', content)
    STATS["total_schemas"] += len(schemas)
    if len(schemas) == 0:
        warn(rel, "No JSON-LD schema markup")

    if "BlogPosting" in content:
        STATS["has_blogposting"] += 1
    if "BreadcrumbList" in content:
        STATS["has_breadcrumb_schema"] += 1
    if "FAQPage" in content:
        STATS["has_faq_schema"] += 1

    # === DESIGN SYSTEM ===
    if "overloop.css" in content:
        STATS["has_css"] += 1
    else:
        error(rel, "Missing overloop.css link")

    if "Playfair" in content or "playfair" in content:
        STATS["has_fonts"] += 1
    else:
        warn(rel, "Missing Playfair Display font")

    if 'class="nav"' in content or 'class="nav ' in content:
        STATS["has_nav"] += 1
    else:
        error(rel, "Missing navigation")

    if 'class="footer"' in content:
        STATS["has_footer"] += 1
    else:
        error(rel, "Missing footer")

    if "breadcrumb-bar" in content:
        STATS["has_breadcrumb"] += 1
    else:
        warn(rel, "Missing breadcrumb bar")

    if "article-header" in content:
        STATS["has_dark_header"] += 1

    if "blog.js" in content:
        STATS["has_js"] += 1
    else:
        warn(rel, "Missing blog.js script")

    # === INTERNAL LINKS ===
    internal_links = re.findall(r'href="(/blog/[^"]*)"', content)
    STATS["total_internal_links"] += len(internal_links)

    for link in internal_links:
        if "/blog/en/" in link:
            error(rel, f"Internal link uses /blog/en/ (should be /blog/): {link}")
            break

    # === CONTENT QUALITY ===
    # Word count (rough)
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'\s+', ' ', text).strip()
    words = len(text.split())
    STATS["total_words"] += words

    if "index.html" not in rel and words < 1000:
        warn(rel, f"Low word count: {words} words")

    # H1 count
    h1_count = len(re.findall(r'<h1[^>]*>', content))
    if h1_count == 0:
        error(rel, "Missing H1 tag")
    elif h1_count > 1:
        warn(rel, f"Multiple H1 tags ({h1_count})")

    # H2 count
    h2_count = len(re.findall(r'<h2[^>]*>', content))
    STATS["total_h2s"] += h2_count

    # Image alt tags
    images = re.findall(r'<img[^>]+>', content)
    for img in images:
        if 'alt=' not in img:
            warn(rel, f"Image missing alt attribute")
            break

    # === PRICING CONSISTENCY ===
    # Only flag if Overloop's OWN price is $49 (not "Overloop ($69) or Apollo ($49)")
    overloop_49 = re.findall(r'Overloop[^.]{0,30}\$49', content)
    for match in overloop_49:
        if "Apollo" not in match and "apollo" not in match and "<!--" not in match:
            error(rel, f"Overloop pricing shows $49 (should be $69): ...{match[-50:]}...")

    # === CONTRAST / ACCESSIBILITY ===
    if "rgba(255, 255, 255, 0.6)" in content or "rgba(255,255,255,0.6)" in content:
        warn(rel, "Low contrast text found (0.6 opacity white on dark bg)")
    if "rgba(255, 255, 255, 0.4)" in content or "rgba(255,255,255,0.4)" in content:
        error(rel, "Very low contrast text (0.4 opacity white)")

    # === TODO REMNANTS ===
    todos = re.findall(r'<!-- TODO', content)
    if todos:
        warn(rel, f"{len(todos)} TODO comments remaining")

    # === EM DASHES ===
    if "\u2014" in content:
        warn(rel, "Contains em dash character")

def audit_assets():
    # Check screenshots exist
    screenshots_dir = os.path.join(ASSETS_DIR, "images/screenshots")
    if os.path.exists(screenshots_dir):
        STATS["screenshots"] = len(os.listdir(screenshots_dir))

    logos_dir = os.path.join(ASSETS_DIR, "images/logos")
    if os.path.exists(logos_dir):
        STATS["logos"] = len(os.listdir(logos_dir))

    og_dir = os.path.join(ASSETS_DIR, "images/og")
    if os.path.exists(og_dir):
        STATS["og_images"] = len(os.listdir(og_dir))

    if os.path.exists(os.path.join(ASSETS_DIR, "images/nicolas-finet.png")):
        STATS["has_author_photo"] = 1
    elif os.path.exists(os.path.join(ASSETS_DIR, "images/nicolas-finet.jpg")):
        STATS["has_author_photo"] = 1
    else:
        error("assets", "Missing author photo (nicolas-finet.jpg/png)")

    # Check CSS exists
    if not os.path.exists(os.path.join(ASSETS_DIR, "css/overloop.css")):
        error("assets", "Missing overloop.css")

    # Check JS exists
    if not os.path.exists(os.path.join(ASSETS_DIR, "js/blog.js")):
        error("assets", "Missing blog.js")

    # Check nav/footer
    if not os.path.exists(os.path.join(ASSETS_DIR, "nav.html")):
        error("assets", "Missing nav.html")
    if not os.path.exists(os.path.join(ASSETS_DIR, "footer.html")):
        error("assets", "Missing footer.html")

def audit_redirects():
    csv_path = "/tmp/overloop-blog/redirects/redirects.csv"
    if os.path.exists(csv_path):
        with open(csv_path) as f:
            lines = f.readlines()
        STATS["redirect_rules"] = len(lines) - 1  # minus header
    else:
        error("redirects", "Missing redirects.csv")

    worker_path = "/tmp/overloop-blog/redirects/cloudflare-worker.js"
    if not os.path.exists(worker_path):
        error("redirects", "Missing cloudflare-worker.js")
    else:
        STATS["has_worker"] = 1

def check_internal_link_targets():
    """Verify all internal links point to files that exist."""
    all_slugs = set()
    for lang in ["en", "de", "fr", "es"]:
        lang_dir = os.path.join(BLOG_DIR, lang)
        if os.path.exists(lang_dir):
            for f in os.listdir(lang_dir):
                if f.endswith(".html") and f != "index.html":
                    all_slugs.add(f.replace(".html", ""))

    for lang in ["en", "de", "fr", "es"]:
        lang_dir = os.path.join(BLOG_DIR, lang)
        if not os.path.exists(lang_dir):
            continue
        for fname in os.listdir(lang_dir):
            if not fname.endswith(".html"):
                continue
            filepath = os.path.join(lang_dir, fname)
            rel = filepath.replace("/tmp/overloop-blog/", "")
            with open(filepath) as f:
                content = f.read()

            links = re.findall(r'href="/blog/([^"]*)"', content)
            for link in links:
                slug = link.rstrip("/")
                if slug and slug not in all_slugs and not slug.endswith("index"):
                    STATS["broken_internal_links"] += 1
                    if STATS["broken_internal_links"] <= 10:
                        warn(rel, f"Internal link target may not exist: /blog/{slug}")

# === RUN AUDIT ===
print("=" * 60)
print("OVERLOOP BLOG AUDIT")
print("=" * 60)
print()

# Audit all HTML files
for lang in ["en", "de", "fr", "es"]:
    lang_dir = os.path.join(BLOG_DIR, lang)
    if os.path.exists(lang_dir):
        for fname in sorted(os.listdir(lang_dir)):
            if fname.endswith(".html"):
                audit_html(os.path.join(lang_dir, fname))

# Audit assets
audit_assets()

# Audit redirects
audit_redirects()

# Check link targets
check_internal_link_targets()

# === REPORT ===
print("STATS")
print("-" * 40)
for k, v in sorted(STATS.items()):
    print(f"  {k:30s} {v}")

print()
print(f"ERRORS ({len(ERRORS)})")
print("-" * 40)
for e in sorted(ERRORS):
    print(f"  {e}")

print()
print(f"WARNINGS ({len(WARNINGS)})")
print("-" * 40)
for w in sorted(WARNINGS)[:30]:
    print(f"  {w}")
if len(WARNINGS) > 30:
    print(f"  ... and {len(WARNINGS) - 30} more warnings")

print()
print("=" * 60)
print(f"VERDICT: {len(ERRORS)} errors, {len(WARNINGS)} warnings across {STATS['total_files']} files")
if len(ERRORS) == 0:
    print("SHIP IT.")
elif len(ERRORS) <= 5:
    print("FIX ERRORS THEN SHIP.")
else:
    print("FIX ERRORS BEFORE SHIPPING.")
print("=" * 60)
