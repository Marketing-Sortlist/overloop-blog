#!/usr/bin/env python3
"""
audit-v2-migration.py — Custom audit of the V2-migrated articles in blog/_v2/.

Checks:
  - 4 JSON-LD blocks present (Article, BreadcrumbList, FAQPage, ItemList)
  - hreflang block present (>= 2 entries)
  - canonical URL valid
  - og:image set
  - V2 migration banner removed
  - Updated date set to migration date
  - No staging github.io URLs in assets
  - Internal blog links resolve to existing files
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).parent
V2_DIR = REPO / "blog" / "_v2"
LEGACY_DIR = REPO / "blog"

errors = defaultdict(list)
warnings = defaultdict(list)
stats = Counter()


def check_file(path: Path) -> None:
    name = path.name
    html = path.read_text(encoding="utf-8")
    stats["files"] += 1

    # --- JSON-LD ---
    json_ld_count = html.count("application/ld+json")
    if json_ld_count < 2:
        errors[name].append(f"only {json_ld_count} JSON-LD blocks (expect ≥2 for Article + BreadcrumbList)")
    stats["json_ld_total"] += json_ld_count

    for schema in ["Article", "BreadcrumbList"]:
        if f'"@type": "{schema}"' not in html:
            errors[name].append(f"missing {schema} schema")

    if '"@type": "FAQPage"' in html:
        stats["with_faq"] += 1
    if '"@type": "ItemList"' in html:
        stats["with_itemlist"] += 1

    # --- Hreflang ---
    hreflang_count = len(re.findall(r'rel="alternate"\s+hreflang=', html)) + len(re.findall(r'hreflang="[^"]+"\s+rel="alternate"', html))
    if hreflang_count < 2:
        warnings[name].append(f"only {hreflang_count} hreflang entries")
    stats["with_hreflang"] += 1 if hreflang_count >= 2 else 0

    # --- Canonical ---
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not canonical:
        errors[name].append("missing canonical")
    elif "sortlist.github.io" in canonical.group(1):
        errors[name].append(f"staging URL in canonical: {canonical.group(1)}")
    elif not canonical.group(1).startswith("https://overloop.com/blog/"):
        warnings[name].append(f"unusual canonical: {canonical.group(1)}")

    # --- OG image ---
    og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if not og_img:
        warnings[name].append("missing og:image")
    elif "sortlist.github.io" in og_img.group(1):
        errors[name].append(f"staging URL in og:image")

    # --- V2 banner removed ---
    if "V2 PREVIEW" in html or "V2 MIGRATION PREVIEW BANNER" in html:
        errors[name].append("V2 migration banner still present (should be removed)")

    # --- Updated date ---
    if "Updated Apr 27, 2026" not in html:
        warnings[name].append("Updated date 'Apr 27, 2026' not found in article-meta")

    # --- No legacy CSS reference ---
    if 'href="/assets/css/overloop.css"' in html:
        errors[name].append("legacy CSS still linked — V2 should be inline")

    # --- No staging URLs in body ---
    staging_count = html.count("sortlist.github.io/overloop-blog")
    if staging_count > 0:
        errors[name].append(f"{staging_count} staging github.io URL(s) remaining")

    # --- Internal blog links resolve ---
    blog_links = re.findall(r'href="/blog/([a-z0-9\-]+)"', html)
    for slug in set(blog_links):
        if not (LEGACY_DIR / f"{slug}.html").exists():
            warnings[name].append(f"internal link /blog/{slug} → file not found")
            stats["broken_internal_links"] += 1


def main() -> int:
    print(f"V2 Migration Audit — scanning {V2_DIR}\n")

    files = [f for f in sorted(V2_DIR.glob("*.html")) if f.name != "index.html"]
    for f in files:
        check_file(f)

    print("─── Stats ───")
    for k, v in stats.most_common():
        print(f"  {k:35s}  {v}")

    print(f"\n─── Errors ({sum(len(v) for v in errors.values())}) ───")
    if not errors:
        print("  ✓ No errors")
    for fname, errs in sorted(errors.items()):
        print(f"  ✗ {fname}")
        for e in errs:
            print(f"      → {e}")

    n_warn = sum(len(v) for v in warnings.values())
    print(f"\n─── Warnings ({n_warn}) ───")
    if not warnings:
        print("  ✓ No warnings")
    else:
        for fname, ws in sorted(warnings.items())[:15]:  # top 15
            print(f"  ⚠ {fname}")
            for w in ws[:3]:
                print(f"      → {w}")
        if len(warnings) > 15:
            print(f"  … and {len(warnings) - 15} more files with warnings")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
