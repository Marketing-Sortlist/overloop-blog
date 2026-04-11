#!/usr/bin/env python3
"""Fix all logo and screenshot image paths across all HTML files."""
import os, re

BLOG_DIR = "/tmp/overloop-blog/blog"
LOGOS_DIR = "/tmp/overloop-blog/assets/images/logos"
SCREENSHOTS_DIR = "/tmp/overloop-blog/assets/images/screenshots"

# Map expected filenames (in HTML) to actual filenames (on disk)
LOGO_MAP = {
    "overloop-logo.png": "overloop.com.png",
    "apollo-logo.png": "apollo.io.png",
    "clay-logo.png": "clay.com.png",
    "cognism-logo.png": None,  # doesn't exist, create placeholder
    "expandi-logo.png": "expandi.io.svg",
    "instantly-logo.png": "instantly.ai.svg",
    "lgm-logo.png": "lagrowthmachine.com.svg",
    "linkedin-helper-logo.png": "linkedhelper.com.svg",
    "outreach-logo.png": "outreach.io.png",
    "salesloft-logo.png": "salesloft.com.svg",
    "seamless-logo.png": "seamless.ai.png",
    "smartlead-logo.png": "smartlead.ai.svg",
    "zoominfo-logo.png": "zoominfo.com.png",
    "lavender-logo.png": None,
    "gong-logo.png": None,
    "fireflies-logo.png": None,
    "sybill-logo.png": None,
    "copyai-logo.png": None,
    "amplemarket-logo.png": None,
    "lemlist-logo.png": "lemlist.com.png",
    "reply-logo.png": "reply.io.svg",
    "saleshandy-logo.png": "saleshandy.com.svg",
    "hubspot-logo.png": "hubspot.com.png",
    "hunter-logo.png": "hunter.io.png",
    "woodpecker-logo.png": "woodpecker.co.svg",
    "dripify-logo.png": "dripify.io.svg",
    "lusha-logo.png": "lusha.com.png",
    "linkedin-logo.png": "linkedin.com.png",
}

# Create missing logo SVGs
MISSING_LOGOS = {
    "cognism": ("#1A237E", "C"),
    "lavender": ("#7C3AED", "L"),
    "gong": ("#6B46C1", "G"),
    "fireflies": ("#FF6B35", "F"),
    "sybill": ("#2563EB", "S"),
    "copyai": ("#6366F1", "C"),
    "amplemarket": ("#059669", "A"),
}

SVG_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="56" height="56" viewBox="0 0 56 56">
  <rect width="56" height="56" rx="12" fill="{color}"/>
  <text x="28" y="36" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="24" font-weight="700" fill="white">{letter}</text>
</svg>'''

# Create missing logos
for name, (color, letter) in MISSING_LOGOS.items():
    svg_path = os.path.join(LOGOS_DIR, f"{name}.svg")
    if not os.path.exists(svg_path):
        with open(svg_path, "w") as f:
            f.write(SVG_TEMPLATE.format(color=color, letter=letter))
        print(f"  Created: {name}.svg")
    LOGO_MAP[f"{name}-logo.png"] = f"{name}.svg"

# Build replacement map
replacements = {}
for old_name, new_name in LOGO_MAP.items():
    if new_name:
        replacements[f"/assets/images/logos/{old_name}"] = f"/assets/images/logos/{new_name}"

# Also fix screenshot paths
SCREENSHOT_MAP = {
    "overloop-dashboard.png": "overloop.com.png",
    "overloop-campaign-builder.png": "overloop.com.png",
    "zoominfo-contact-profile.png": "zoominfo.com.png",
    "cognism-prospector.png": None,
    "seamless-ai-search.png": None,
    "lusha-chrome-extension.png": None,
    "clay-waterfall-enrichment.png": "clay.com.png",
    "lemlist-personalization.png": "lemlist.com.png",
    "instantly-campaign-analytics.png": "instantly.ai.svg",
    "saleshandy-sequences.png": "saleshandy.com.svg",
    "apollo-search.png": "apollo.io.png",
    "hubspot-sequences.png": "hubspot.com.png",
    "reply-sequences.png": "reply.io.svg",
    "hunter-email-finder.png": "hunter.io.png",
    "rocketreach-search.png": None,
    "snov-dashboard.png": None,
    "linkedin-sales-navigator.png": "linkedin.com.png",
    "leadiq-capture.png": None,
}

# Create placeholder screenshots for missing ones
for name, actual in SCREENSHOT_MAP.items():
    if actual is None:
        tool_name = name.replace(".png", "").replace("-", " ").title().split(" ")[0]
        svg_path = os.path.join(SCREENSHOTS_DIR, name.replace(".png", ".svg"))
        if not os.path.exists(svg_path):
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="405" viewBox="0 0 720 405">
  <rect width="720" height="405" rx="8" fill="#f3f4f6" stroke="#e5e7eb"/>
  <text x="360" y="195" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="18" font-weight="600" fill="#6b7280">{tool_name}</text>
  <text x="360" y="225" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="14" fill="#9ca3af">Screenshot coming soon</text>
</svg>'''
            with open(svg_path, "w") as f:
                f.write(svg)
            print(f"  Created screenshot placeholder: {name.replace('.png', '.svg')}")
        SCREENSHOT_MAP[name] = name.replace(".png", ".svg")

for old_name, new_name in SCREENSHOT_MAP.items():
    if new_name:
        replacements[f"/assets/images/screenshots/{old_name}"] = f"/assets/images/screenshots/{new_name}"

# Apply replacements across all HTML files
fixed_count = 0
for lang in ["en", "de", "fr", "es"]:
    lang_dir = os.path.join(BLOG_DIR, lang)
    if not os.path.exists(lang_dir):
        continue
    for fname in os.listdir(lang_dir):
        if not fname.endswith(".html"):
            continue
        filepath = os.path.join(lang_dir, fname)
        with open(filepath, "r") as f:
            content = f.read()

        original = content
        for old_path, new_path in replacements.items():
            content = content.replace(old_path, new_path)

        if content != original:
            with open(filepath, "w") as f:
                f.write(content)
            fixed_count += 1

print(f"\nFixed image paths in {fixed_count} files")
print(f"Total replacements defined: {len(replacements)}")
