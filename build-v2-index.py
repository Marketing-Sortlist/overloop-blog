#!/usr/bin/env python3
"""
build-v2-index.py — Generate blog/_v2/index.html: navigation page for the
                    75 V2-migrated articles. Groups by template type with
                    visual color-coding.
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).parent
V2_DIR = REPO / "blog" / "_v2"

# Same mapping as in migrate-to-v2.py — copied here to avoid import cycle
sys.path.insert(0, str(REPO))
from importlib import import_module
mig = import_module("migrate-to-v2".replace("-", "_") if False else None) if False else None

# Simpler: re-extract from migrated articles directly
TEMPLATE_PATTERNS = {
    "best-tools.html":         {"label": "Best Tools",      "color": "#6366F1", "bg": "#EEF2FF"},
    "alternatives.html":       {"label": "Alternatives",    "color": "#A855F7", "bg": "#FAF5FF"},
    "pillar-guide.html":       {"label": "Pillar / Guide",  "color": "#7C3AED", "bg": "#F5F3FF"},
    "how-to.html":             {"label": "How-To",          "color": "#10B981", "bg": "#ECFDF5"},
    "versus.html":             {"label": "X vs Y",          "color": "#F59E0B", "bg": "#FFFBEB"},
    "swipe-files.html":        {"label": "Swipe Files",     "color": "#EC4899", "bg": "#FCE7F3"},
    "data-list.html":          {"label": "Data List",       "color": "#8B5CF6", "bg": "#F3E8FF"},
    "statistics.html":         {"label": "Statistics",      "color": "#3B82F6", "bg": "#DBEAFE"},
    "best-agency.html":        {"label": "Best Agency",     "color": "#0EA5E9", "bg": "#E0F2FE"},
    "strategy.html":           {"label": "Strategy",        "color": "#F97316", "bg": "#FFEDD5"},
    "lead-gen-industry.html":  {"label": "Lead Gen / X",    "color": "#06B6D4", "bg": "#CFFAFE"},
    "what-is.html":            {"label": "What is X?",      "color": "#84CC16", "bg": "#ECFCCB"},
    "role-guide.html":         {"label": "Role Guide",      "color": "#14B8A6", "bg": "#CCFBF1"},
    "tactical.html":           {"label": "Tactical",        "color": "#EF4444", "bg": "#FEE2E2"},
    "tool-review.html":        {"label": "Tool Review",     "color": "#DC2626", "bg": "#FEE2E2"},
}


def detect_template(html: str) -> str:
    """Heuristic: find which V2 template was used by looking at signature CSS classes."""
    # Look for distinctive class signatures (most → least common)
    signatures = [
        ('class="tool-card', 'best-tools.html'),
        ('class="alt-card', 'alternatives.html'),
        ('class="chapter"', 'pillar-guide.html'),
        ('howto-meta', 'how-to.html'),
        ('vs-head', 'versus.html'),
        ('class="tpl ', 'swipe-files.html'),
        ('data-table-wrap', 'data-list.html'),
        ('hero-stats', 'statistics.html'),
        ('agency-card', 'best-agency.html'),
        ('framework-flow', 'strategy.html'),
        ('icp__grid', 'lead-gen-industry.html'),
        ('definition__box', 'what-is.html'),
        ('role-overview', 'role-guide.html'),
        ('verdict-box', 'tool-review.html'),
        ('class="point"', 'tactical.html'),
    ]
    for sig, tmpl in signatures:
        if sig in html:
            return tmpl
    return "tactical.html"  # fallback


def extract_meta(html: str) -> dict:
    title_m = re.search(r'<title>([^<]+)</title>', html)
    title = title_m.group(1).replace(" | Overloop", "").strip() if title_m else ""
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
    desc = desc_m.group(1) if desc_m else ""
    canonical_m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    canonical = canonical_m.group(1) if canonical_m else ""
    author_m = re.search(r'<div class="article-meta__author">([^<]+)</div>', html)
    author = author_m.group(1).strip() if author_m else "—"
    dates_m = re.search(r'<div class="article-meta__dates">([^<]+)</div>', html)
    dates = dates_m.group(1).strip() if dates_m else ""
    read_time_m = re.search(r'(\d+)\s*min\s*read', html)
    read_time = f"{read_time_m.group(1)} min" if read_time_m else ""
    return {"title": title, "description": desc, "canonical": canonical, "author": author, "dates": dates, "read_time": read_time}


def build_index() -> str:
    articles_by_template = defaultdict(list)
    for f in sorted(V2_DIR.glob("*.html")):
        if f.name == "index.html":
            continue
        html = f.read_text(encoding="utf-8")
        tmpl = detect_template(html)
        meta = extract_meta(html)
        meta["slug"] = f.stem
        meta["template"] = tmpl
        articles_by_template[tmpl].append(meta)

    total = sum(len(v) for v in articles_by_template.values())

    # Build HTML
    cards_html = []
    # Order templates by article count (most populated first)
    sorted_templates = sorted(
        articles_by_template.items(),
        key=lambda kv: -len(kv[1])
    )
    for tmpl, articles in sorted_templates:
        info = TEMPLATE_PATTERNS.get(tmpl, {"label": tmpl, "color": "#64748B", "bg": "#F1F5F9"})
        cards_html.append(f'''
        <section class="group">
          <h2 class="group__h" style="--c:{info['color']};--bg:{info['bg']}">
            <span class="group__badge">{info['label']}</span>
            <span class="group__count">{len(articles)} article{'s' if len(articles)>1 else ''}</span>
            <span class="group__tmpl">{tmpl}</span>
          </h2>
          <div class="grid">''')
        for a in articles:
            short_desc = a['description'][:140] + ('…' if len(a['description']) > 140 else '')
            cards_html.append(f'''
            <a class="card" href="{a['slug']}.html" style="--c:{info['color']};--bg:{info['bg']}">
              <div class="card__title">{a['title']}</div>
              <div class="card__desc">{short_desc}</div>
              <div class="card__meta">
                <span class="card__author">{a['author']}</span>
                <span class="card__sep">·</span>
                <span class="card__time">{a['read_time']}</span>
                <span class="card__sep">·</span>
                <span class="card__slug">/{a['slug']}</span>
              </div>
            </a>''')
        cards_html.append('</div></section>')

    # Build filter chips outside f-string to avoid escaping issues
    filter_chips = []
    for tmpl, articles in sorted_templates:
        info = TEMPLATE_PATTERNS.get(tmpl, {"label": tmpl, "color": "#64748B"})
        filter_chips.append(
            f'<button class="filter-chip" data-filter="{tmpl}" style="--c:{info["color"]}">'
            f'{info["label"]} ({len(articles)})</button>'
        )
    filter_chips_html = "\n      ".join(filter_chips)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>V2 Migration Preview · {total} articles | Overloop Blog</title>
  <meta name="robots" content="noindex, nofollow">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    html{{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}}
    body{{font-family:'Epilogue',-apple-system,sans-serif;color:#374151;background:#FAFAFA;line-height:1.6;font-size:16px}}
    a{{color:#6366F1;text-decoration:none}}
    a:hover{{text-decoration:underline}}

    .nav{{position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between;height:64px;padding:0 32px;background:rgba(255,255,255,.85);backdrop-filter:blur(12px);border-bottom:1px solid #F3F4F6}}
    .nav-logo{{display:flex;align-items:center;gap:12px;font-weight:800;color:#1A1A2E}}
    .nav-logo img{{height:24px}}
    .nav-badge{{padding:4px 10px;background:linear-gradient(135deg,#6366F1,#A855F7);color:#fff;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;border-radius:6px}}
    .nav-stat{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#64748B}}

    .hero{{padding:64px 32px 40px;background:linear-gradient(180deg,#FFFFFF 0%,#EEF2FF 50%,#FAFAFA 100%);text-align:center;position:relative;overflow:hidden}}
    .hero::before{{content:'';position:absolute;top:-100px;right:-80px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(168,85,247,.12) 0%,transparent 70%)}}
    .hero-inner{{position:relative;max-width:880px;margin:0 auto}}
    .hero h1{{font-size:clamp(28px,4vw,40px);font-weight:800;color:#1A1A2E;line-height:1.15;margin-bottom:14px;letter-spacing:-.02em}}
    .hero h1 em{{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:400;background:linear-gradient(135deg,#6366F1,#A855F7);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}}
    .hero p{{font-size:17px;color:#64748B;max-width:620px;margin:0 auto 22px}}
    .hero-stats{{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}}
    .hero-stat{{padding:8px 14px;background:#fff;border:1px solid #F3F4F6;border-radius:100px;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:#1A1A2E;box-shadow:0 2px 8px rgba(0,0,0,.04)}}
    .hero-stat strong{{background:linear-gradient(135deg,#6366F1,#A855F7);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;font-size:14px;margin-right:4px}}

    .container{{max-width:1280px;margin:0 auto;padding:32px}}
    .filter-bar{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:32px;padding:16px;background:#fff;border:1px solid #F3F4F6;border-radius:12px}}
    .filter-bar__label{{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;color:#64748B;letter-spacing:.05em;text-transform:uppercase;align-self:center;margin-right:6px}}
    .filter-chip{{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;background:#F8FAFC;border:1px solid #F3F4F6;border-radius:100px;font-size:12.5px;font-weight:600;color:#374151;cursor:pointer;transition:all 200ms;font-family:inherit}}
    .filter-chip:hover{{border-color:#6366F1;color:#6366F1}}
    .filter-chip.is-active{{background:linear-gradient(135deg,#6366F1,#A855F7);color:#fff;border-color:transparent}}

    .group{{margin-bottom:48px}}
    .group__h{{display:flex;align-items:center;gap:14px;margin-bottom:18px;padding:14px 18px;background:var(--bg);border-left:4px solid var(--c);border-radius:8px}}
    .group__badge{{font-size:18px;font-weight:800;color:var(--c)}}
    .group__count{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#64748B;font-weight:600}}
    .group__tmpl{{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:11px;color:#94A3B8}}

    .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}
    .card{{display:block;padding:18px 20px;background:#fff;border:1px solid #F3F4F6;border-radius:12px;color:#1A1A2E;transition:all 200ms;text-decoration:none!important;border-left:3px solid var(--c)}}
    .card:hover{{box-shadow:0 4px 12px rgba(0,0,0,.06);transform:translateY(-2px);border-color:var(--c);text-decoration:none}}
    .card__title{{font-size:15px;font-weight:700;line-height:1.35;margin-bottom:6px;color:#1A1A2E}}
    .card__desc{{font-size:13px;color:#64748B;line-height:1.5;margin-bottom:10px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
    .card__meta{{display:flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#94A3B8;flex-wrap:wrap}}
    .card__author{{font-weight:600;color:#374151}}
    .card__sep{{opacity:.5}}
    .card__slug{{color:var(--c);font-weight:600}}

    .footer{{padding:32px;text-align:center;color:#94A3B8;font-size:13px;font-family:'JetBrains Mono',monospace;border-top:1px solid #F3F4F6;margin-top:32px}}
    .footer a{{color:#6366F1}}

    @media(max-width:639px){{
      .nav{{padding:0 16px}}
      .container{{padding:16px}}
      .hero{{padding:48px 16px 32px}}
      .grid{{grid-template-columns:1fr}}
    }}
  </style>
</head>
<body>
  <nav class="nav">
    <div class="nav-logo">
      <img src="https://overloop.com/assets/images/overloop-logo.png" alt="Overloop">
      <span>Overloop Blog</span>
      <span class="nav-badge">V2 Preview</span>
    </div>
    <div class="nav-stat">{total} articles · {len(sorted_templates)} templates</div>
  </nav>

  <header class="hero">
    <div class="hero-inner">
      <h1>V2 Migration <em>Preview</em></h1>
      <p>Browse the 75 EN articles migrated to the new design system. Click any card to open the V2 version. Compare with the live legacy version at <a href="https://overloop.com/blog">overloop.com/blog</a>.</p>
      <div class="hero-stats">
        <div class="hero-stat"><strong>{total}</strong>articles migrated</div>
        <div class="hero-stat"><strong>{len(sorted_templates)}</strong>templates</div>
        <div class="hero-stat"><strong>0</strong>migration errors</div>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="filter-bar" id="filter-bar">
      <span class="filter-bar__label">Filter</span>
      <button class="filter-chip is-active" data-filter="all">All ({total})</button>
      {filter_chips_html}
    </div>

    {''.join(cards_html)}
  </main>

  <footer class="footer">
    Generated {sum(len(v) for v in articles_by_template.values())} cards · <a href="https://github.com/Marketing-Sortlist/overloop-blog/pull/1">Source PR</a> · <a href="https://overloop.com/blog">Live blog</a>
  </footer>

  <script>
    // Filter
    document.getElementById('filter-bar').addEventListener('click', e => {{
      const b = e.target.closest('.filter-chip');
      if (!b) return;
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('is-active'));
      b.classList.add('is-active');
      const f = b.dataset.filter;
      document.querySelectorAll('.group').forEach(g => {{
        if (f === 'all') {{ g.style.display = ''; return; }}
        const tmpl = g.querySelector('.group__tmpl').textContent.trim();
        g.style.display = (tmpl === f) ? '' : 'none';
      }});
    }});
  </script>
</body>
</html>
'''


def main():
    out = V2_DIR / "index.html"
    out.write_text(build_index(), encoding="utf-8")
    size_kb = out.stat().st_size / 1024
    print(f"✓ Built {out} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
