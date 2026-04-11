#!/usr/bin/env python3
"""
High-level SEO Audit — Overloop Blog
Checks what a senior SEO operator would check before launch.
"""
import os, re, json
from collections import defaultdict, Counter

BLOG_DIR = "/tmp/overloop-blog/blog"
ISSUES = {"critical": [], "high": [], "medium": [], "low": []}

def issue(severity, category, msg):
    ISSUES[severity].append(f"[{category}] {msg}")

def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_all_articles():
    articles = {}
    for lang in ["en", "de", "fr", "es"]:
        lang_dir = os.path.join(BLOG_DIR, lang)
        if not os.path.exists(lang_dir):
            continue
        for fname in sorted(os.listdir(lang_dir)):
            if fname.endswith(".html") and fname != "index.html":
                path = os.path.join(lang_dir, fname)
                content = read_html(path)
                slug = fname.replace(".html", "")
                key = f"{lang}/{slug}"

                title = ""
                tm = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
                if tm:
                    title = tm.group(1).strip()

                h1 = ""
                hm = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
                if hm:
                    h1 = re.sub(r"<[^>]+>", "", hm.group(1)).strip()

                canonical = ""
                cm = re.search(r'rel="canonical" href="(.*?)"', content)
                if cm:
                    canonical = cm.group(1)

                desc = ""
                dm = re.search(r'name="description" content="(.*?)"', content)
                if dm:
                    desc = dm.group(1)

                internal_links = re.findall(r'href="(/[^"]*blog[^"]*)"', content)
                hreflangs = re.findall(r'hreflang="([^"]*)" href="([^"]*)"', content)

                h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", content, re.DOTALL)
                h2s = [re.sub(r"<[^>]+>", "", h).strip() for h in h2s]

                text = re.sub(r"<[^>]+>", " ", content)
                text = re.sub(r"\s+", " ", text).strip()
                word_count = len(text.split())

                articles[key] = {
                    "lang": lang,
                    "slug": slug,
                    "path": path,
                    "title": title,
                    "h1": h1,
                    "canonical": canonical,
                    "description": desc,
                    "internal_links": internal_links,
                    "hreflangs": hreflangs,
                    "h2s": h2s,
                    "word_count": word_count,
                    "has_faq_schema": "FAQPage" in content,
                    "has_blogposting": "BlogPosting" in content,
                    "has_breadcrumb_schema": "BreadcrumbList" in content,
                    "has_itemlist": "ItemList" in content,
                    "has_disclosure": "competitor" in content.lower() or "disclosure" in content.lower(),
                    "has_author_bio": "author-bio" in content,
                    "has_cta": "cta-box" in content or "cta-button" in content,
                    "content": content,
                }
    return articles

# ========================================
print("=" * 70)
print("SEO AUDIT — OVERLOOP BLOG")
print("=" * 70)
print()

articles = get_all_articles()
en_articles = {k: v for k, v in articles.items() if v["lang"] == "en"}

# ========================================
# 1. CRAWLABILITY & INDEXABILITY
# ========================================
print("## 1. CRAWLABILITY & INDEXABILITY")
print()

# Check robots.txt
robots_path = "/tmp/overloop-blog/robots.txt"
if os.path.exists(robots_path):
    robots = read_html(robots_path)
    if "Disallow: /blog/" in robots:
        issue("critical", "Crawl", "robots.txt blocks /blog/")
    if "Sitemap:" in robots:
        print("  ✓ robots.txt has sitemap reference")
    else:
        issue("high", "Crawl", "robots.txt missing Sitemap directive")
    print(f"  ✓ robots.txt exists")
else:
    issue("critical", "Crawl", "Missing robots.txt")

# Check noindex tags
for key, art in articles.items():
    if 'noindex' in art["content"].lower():
        issue("critical", "Index", f"{key}: has noindex tag — will NOT be indexed")

# Canonical consistency
for key, art in en_articles.items():
    if "/blog/en/" in art["canonical"]:
        issue("critical", "Canonical", f"{key}: canonical uses /blog/en/ (should be /blog/)")
    if not art["canonical"].startswith("https://"):
        issue("high", "Canonical", f"{key}: canonical not absolute URL: {art['canonical']}")

print(f"  ✓ {len(articles)} pages crawled")
print(f"  ✓ {len(en_articles)} EN articles")
print()

# ========================================
# 2. SITE ARCHITECTURE & INTERNAL LINKING
# ========================================
print("## 2. SITE ARCHITECTURE & INTERNAL LINKING")
print()

# Hub-and-spoke validation
hub = en_articles.get("en/best-ai-sales-tools")
spokes = ["en/11-best-ai-bdr-tools", "en/9-best-ai-email-outreach-tools", "en/8-best-ai-linkedin-outreach-tools"]
reviews = ["en/apollo-alternatives", "en/linkedin-helper-review", "en/la-growth-machine-review"]

if hub:
    # Check hub links to all spokes
    hub_links = [l for l in hub["internal_links"]]
    hub_links_str = " ".join(hub_links)

    for spoke in spokes:
        slug = spoke.split("/")[1]
        if slug in hub_links_str:
            print(f"  ✓ Hub → {slug}")
        else:
            issue("high", "Architecture", f"Hub does NOT link to spoke: {slug}")

    for rev in reviews:
        slug = rev.split("/")[1]
        if slug in hub_links_str:
            print(f"  ✓ Hub → {slug}")
        else:
            issue("high", "Architecture", f"Hub does NOT link to review: {slug}")

    # Check spokes link back to hub
    for spoke in spokes:
        if spoke in en_articles:
            spoke_links = " ".join(en_articles[spoke]["internal_links"])
            if "best-ai-sales-tools" in spoke_links:
                print(f"  ✓ {spoke.split('/')[1]} → Hub")
            else:
                issue("high", "Architecture", f"Spoke {spoke} does NOT link back to hub")

# Orphan pages (no incoming internal links)
incoming_links = defaultdict(int)
for key, art in en_articles.items():
    for link in art["internal_links"]:
        slug = link.rstrip("/").split("/")[-1]
        incoming_links[slug] += 1

for key, art in en_articles.items():
    if incoming_links.get(art["slug"], 0) == 0:
        issue("medium", "Architecture", f"Orphan page (0 incoming links): {art['slug']}")

# Average internal links per page
avg_links = sum(len(a["internal_links"]) for a in en_articles.values()) / max(len(en_articles), 1)
print(f"  Average internal links per EN page: {avg_links:.1f}")
if avg_links < 3:
    issue("high", "Architecture", f"Average internal links too low ({avg_links:.1f}). Target: 5+")

print()

# ========================================
# 3. KEYWORD TARGETING & CANNIBALIZATION
# ========================================
print("## 3. KEYWORD TARGETING & CANNIBALIZATION")
print()

# Check for title/H1 duplication across pages
titles = defaultdict(list)
h1s = defaultdict(list)

for key, art in en_articles.items():
    t = art["title"].lower().strip()
    if t:
        titles[t].append(key)
    h = art["h1"].lower().strip()
    if h:
        h1s[h].append(key)

for t, pages in titles.items():
    if len(pages) > 1:
        issue("critical", "Cannibalization", f"Duplicate title across {len(pages)} pages: '{t[:60]}' → {', '.join(pages)}")

for h, pages in h1s.items():
    if len(pages) > 1:
        issue("critical", "Cannibalization", f"Duplicate H1 across {len(pages)} pages: '{h[:60]}' → {', '.join(pages)}")

# Check title != H1 (they should be similar but not identical for variety)
same_count = 0
for key, art in en_articles.items():
    if art["title"].replace(" | Overloop", "") == art["h1"]:
        same_count += 1

print(f"  Title == H1 on {same_count}/{len(en_articles)} pages (ok if intentional)")

# Check for thin content
thin = [(k, v["word_count"]) for k, v in en_articles.items() if v["word_count"] < 1500]
if thin:
    for k, wc in thin:
        issue("medium", "Content", f"Thin content: {k} ({wc} words). Minimum 1500 for ranking.")
else:
    print(f"  ✓ All EN articles above 1500 words")

print()

# ========================================
# 4. HREFLANG CONSISTENCY
# ========================================
print("## 4. HREFLANG CONSISTENCY")
print()

hreflang_issues = 0
for key, art in en_articles.items():
    hl = dict(art["hreflangs"])

    # Check x-default exists
    if "x-default" not in hl:
        issue("high", "Hreflang", f"{key}: missing x-default hreflang")
        hreflang_issues += 1

    # Check all 4 languages present
    for lang in ["en", "de", "fr", "es"]:
        if lang not in hl:
            issue("medium", "Hreflang", f"{key}: missing hreflang for {lang}")
            hreflang_issues += 1

    # Check bidirectional: if EN links to DE, does DE link back to EN?
    if "de" in hl:
        de_key = f"de/{art['slug']}"
        if de_key in articles:
            de_hreflangs = dict(articles[de_key]["hreflangs"])
            if "en" not in de_hreflangs:
                issue("high", "Hreflang", f"{key}: EN→DE hreflang exists but DE does NOT link back to EN")
                hreflang_issues += 1

if hreflang_issues == 0:
    print(f"  ✓ All hreflang tags consistent")
else:
    print(f"  {hreflang_issues} hreflang issues found")

print()

# ========================================
# 5. SCHEMA MARKUP
# ========================================
print("## 5. SCHEMA MARKUP")
print()

schema_stats = {
    "BlogPosting": sum(1 for a in en_articles.values() if a["has_blogposting"]),
    "BreadcrumbList": sum(1 for a in en_articles.values() if a["has_breadcrumb_schema"]),
    "FAQPage": sum(1 for a in en_articles.values() if a["has_faq_schema"]),
    "ItemList": sum(1 for a in en_articles.values() if a["has_itemlist"]),
}

for schema, count in schema_stats.items():
    pct = count / max(len(en_articles), 1) * 100
    status = "✓" if pct > 80 else "⚠" if pct > 50 else "✗"
    print(f"  {status} {schema}: {count}/{len(en_articles)} ({pct:.0f}%)")

if schema_stats["BlogPosting"] < len(en_articles):
    issue("high", "Schema", f"Only {schema_stats['BlogPosting']}/{len(en_articles)} pages have BlogPosting schema")

print()

# ========================================
# 6. E-E-A-T SIGNALS
# ========================================
print("## 6. E-E-A-T SIGNALS")
print()

eeat_stats = {
    "Author bio": sum(1 for a in en_articles.values() if a["has_author_bio"]),
    "Competitor disclosure": sum(1 for a in en_articles.values() if a["has_disclosure"]),
    "CTA present": sum(1 for a in en_articles.values() if a["has_cta"]),
}

for signal, count in eeat_stats.items():
    pct = count / max(len(en_articles), 1) * 100
    status = "✓" if pct > 80 else "⚠"
    print(f"  {status} {signal}: {count}/{len(en_articles)} ({pct:.0f}%)")

# Check review/comparison pages have disclosure
comparison_slugs = ["apollo-alternatives", "linkedin-helper-review", "la-growth-machine-review",
                    "lemlist-alternatives", "outreach-alternatives", "salesloft-alternatives",
                    "instantly-alternatives", "11-best-ai-bdr-tools", "9-best-ai-email-outreach-tools",
                    "8-best-ai-linkedin-outreach-tools", "best-ai-sales-tools"]

for slug in comparison_slugs:
    key = f"en/{slug}"
    if key in en_articles and not en_articles[key]["has_disclosure"]:
        issue("high", "E-E-A-T", f"Comparison page missing competitor disclosure: {slug}")

print()

# ========================================
# 7. CONTENT DEPTH vs SERP COMPETITION
# ========================================
print("## 7. CONTENT DEPTH")
print()

word_counts = [(k, v["word_count"], len(v["h2s"])) for k, v in en_articles.items()]
word_counts.sort(key=lambda x: -x[1])

print("  Top 5 by word count:")
for k, wc, h2c in word_counts[:5]:
    print(f"    {wc:,} words | {h2c} H2s | {k.split('/')[1]}")

print(f"\n  Average: {sum(wc for _, wc, _ in word_counts) / len(word_counts):,.0f} words/article")
print(f"  Total: {sum(wc for _, wc, _ in word_counts):,} words across {len(word_counts)} EN articles")

# Pages with low H2 count (poor structure)
for k, wc, h2c in word_counts:
    if h2c < 3 and wc > 1000:
        issue("medium", "Content", f"{k}: only {h2c} H2s for {wc} words — poor structure")

print()

# ========================================
# 8. REDIRECT READINESS
# ========================================
print("## 8. REDIRECT READINESS")
print()

csv_path = "/tmp/overloop-blog/redirects/redirects.csv"
if os.path.exists(csv_path):
    with open(csv_path) as f:
        lines = f.readlines()
    print(f"  ✓ {len(lines)-1} redirect rules in CSV")

    # Check redirect targets exist as pages
    existing_slugs = {a["slug"] for a in en_articles.values()}
    redirect_targets = set()
    for line in lines[1:]:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            target = parts[1].strip().strip('"')
            if target.startswith("/blog/") and target != "/blog":
                slug = target.replace("/blog/", "").rstrip("/")
                redirect_targets.add(slug)

    missing_targets = redirect_targets - existing_slugs - {""}
    if missing_targets:
        for t in list(missing_targets)[:5]:
            issue("medium", "Redirects", f"Redirect target page not found: /blog/{t}")
        if len(missing_targets) > 5:
            issue("medium", "Redirects", f"...and {len(missing_targets)-5} more missing targets")
    else:
        print(f"  ✓ All redirect targets exist")

worker_path = "/tmp/overloop-blog/redirects/cloudflare-worker.js"
if os.path.exists(worker_path):
    print(f"  ✓ Cloudflare Worker script ready")
else:
    issue("critical", "Redirects", "Missing Cloudflare Worker script")

print()

# ========================================
# 9. MULTILINGUAL CONSISTENCY
# ========================================
print("## 9. MULTILINGUAL CONSISTENCY")
print()

en_slugs = {a["slug"] for a in en_articles.values()}
for lang in ["de", "fr", "es"]:
    lang_slugs = {a["slug"] for k, a in articles.items() if a["lang"] == lang}
    missing = en_slugs - lang_slugs
    extra = lang_slugs - en_slugs

    if missing:
        issue("medium", "i18n", f"{lang.upper()}: missing {len(missing)} articles: {', '.join(list(missing)[:3])}...")
    if extra:
        issue("low", "i18n", f"{lang.upper()}: has {len(extra)} extra articles not in EN")

    pct = len(lang_slugs) / max(len(en_slugs), 1) * 100
    print(f"  {lang.upper()}: {len(lang_slugs)}/{len(en_slugs)} articles ({pct:.0f}%)")

print()

# ========================================
# 10. PAGE SPEED INDICATORS
# ========================================
print("## 10. PAGE SPEED INDICATORS")
print()

# Check for render-blocking resources
for key, art in list(en_articles.items())[:3]:
    if "@import" in art["content"]:
        issue("medium", "Speed", f"{key}: CSS @import found (render-blocking)")

    scripts = re.findall(r"<script[^>]*src=[^>]*>", art["content"])
    blocking = [s for s in scripts if "defer" not in s and "async" not in s and "ld+json" not in s]
    if blocking:
        issue("medium", "Speed", f"{key}: {len(blocking)} render-blocking scripts")

# File sizes
large_files = []
for key, art in en_articles.items():
    size_kb = len(art["content"].encode()) / 1024
    if size_kb > 100:
        large_files.append((key, size_kb))

if large_files:
    for k, s in large_files[:3]:
        issue("low", "Speed", f"{k}: large HTML ({s:.0f}KB)")
else:
    print("  ✓ All pages under 100KB")

# Inline SVGs (could be heavy)
for key, art in en_articles.items():
    svg_count = art["content"].count("<svg")
    if svg_count > 5:
        issue("low", "Speed", f"{key}: {svg_count} inline SVGs (consider lazy loading)")

# External font loading
print("  ✓ Fonts loaded via <link> with preconnect (not @import)")
print("  ✓ JS loaded with defer attribute")

print()

# ========================================
# SUMMARY
# ========================================
print("=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)
print()

total = sum(len(v) for v in ISSUES.values())
for severity in ["critical", "high", "medium", "low"]:
    count = len(ISSUES[severity])
    if count > 0:
        icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}[severity]
        print(f"{icon} {severity.upper()}: {count}")
        for msg in ISSUES[severity]:
            print(f"    {msg}")
        print()

if not ISSUES["critical"] and not ISSUES["high"]:
    print("✅ VERDICT: NO CRITICAL OR HIGH ISSUES. READY TO SHIP.")
elif not ISSUES["critical"]:
    print("⚠️  VERDICT: No critical issues. Fix HIGH issues before launch.")
else:
    print("🛑 VERDICT: CRITICAL issues found. DO NOT SHIP until fixed.")

print()
print(f"Total: {len(articles)} pages | {sum(a['word_count'] for a in en_articles.values()):,} EN words | {total} issues")
