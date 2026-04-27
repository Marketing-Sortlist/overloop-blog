#!/usr/bin/env python3
"""Generate the complete redirect map for Cloudflare Worker from redirects.csv."""
import csv

redirects = {}
vs_redirects = {}

with open('redirects/redirects.csv', 'r') as f:
    reader = csv.DictReader(f)
    for r in reader:
        action = r['action'].strip()
        source = r['current_url'].strip()
        target = r['target_url'].strip()

        if action == '301-KILL' and target and target != 'KEEP URL':
            redirects[source] = target
        elif action == '301-CONSOLIDATE' and target and target != 'KEEP URL':
            redirects[source] = target
        elif action == 'VS-REDIRECT' and target:
            vs_redirects[source] = target

# Output as JS object
print("// ──────────────────────────────────────────────")
print("// Overloop Blog Migration — Redirect Rules")
print("// Generated from redirects.csv — {} rules total".format(len(redirects) + len(vs_redirects)))
print("// ──────────────────────────────────────────────")
print()
print("const BLOG_REDIRECTS = {")

# Group by type for readability
# VS redirects
print("  // === VS Pages: /blog/* → /versus/* ({}) ===".format(len(vs_redirects)))
for src, tgt in sorted(vs_redirects.items()):
    print("  '{}': '{}',".format(src, tgt))
print()

# 301-CONSOLIDATE
consolidate = {k: v for k, v in sorted(redirects.items()) if '/blog/' in v and v != '/blog'}
print("  // === Consolidations: redirect to stronger article ({}) ===".format(len(consolidate)))
for src, tgt in sorted(consolidate.items()):
    print("  '{}': '{}',".format(src, tgt))
print()

# 301-KILL to /blog
kills_to_blog = {k: v for k, v in sorted(redirects.items()) if v == '/blog'}
print("  // === Killed: redirect to /blog index ({}) ===".format(len(kills_to_blog)))
for src, tgt in sorted(kills_to_blog.items()):
    print("  '{}': '{}',".format(src, tgt))

# 301-KILL to specific pages
kills_to_specific = {k: v for k, v in sorted(redirects.items()) if v != '/blog' and '/blog/' not in v}
if kills_to_specific:
    print()
    print("  // === Killed: redirect to specific page ({}) ===".format(len(kills_to_specific)))
    for src, tgt in sorted(kills_to_specific.items()):
        print("  '{}': '{}',".format(src, tgt))

print("};")
print()
print("// Total: {} redirects".format(len(redirects) + len(vs_redirects)))
print("// - {} VS redirects (/blog → /versus)".format(len(vs_redirects)))
print("// - {} consolidations (→ stronger article)".format(len(consolidate)))
print("// - {} kills (→ /blog or specific page)".format(len(kills_to_blog) + len(kills_to_specific)))
