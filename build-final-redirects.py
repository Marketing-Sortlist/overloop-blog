#!/usr/bin/env python3
"""Build the final redirects.csv with all 166 EN articles based on Tanguy's decisions."""
import csv, json, re, os

# ── 1. Load Tanguy's decision CSV ──
decisions = {}
with open('/Users/tanguy/Downloads/Overloop - blog export 14_04_26 - Decision maker.csv', 'r') as f:
    reader = csv.DictReader(f)
    for r in reader:
        slug = r.get('slug', '').strip()
        decisions[slug] = {
            'title': r.get('title', '').strip(),
            'your_decision': r.get('your_decision', '').strip(),
            'your_notes': r.get('your_notes', '').strip(),
            'recommendation': r.get('recommendation', '').strip(),
            'redirect_target': r.get('redirect_target', '').strip(),
            'reason': r.get('reason', '').strip(),
            'gsc_impressions': r.get('gsc_impressions', '0'),
            'log_ai_total': r.get('log_ai_total', '0'),
            'status': r.get('status', '').strip(),
        }

# ── 2. Load existing redirects.csv to preserve INTL rows ──
existing_intl = []
existing_en_slugs = set()
with open('redirects/redirects.csv', 'r') as f:
    reader = csv.DictReader(f)
    for r in reader:
        url = r['current_url'].strip()
        action = r['action'].strip()
        if action == '301-KILL-INTL' or re.search(r'^/(de|fr|es|it)/', url):
            existing_intl.append(r)
        elif url.startswith('/blog/'):
            existing_en_slugs.add(url.replace('/blog/', ''))

# ── 3. VS pages: tool-vs-tool only ──
vs_tool_slugs = {
    'overloop-vs-apollo', 'overloop-vs-lemlist', 'overloop-vs-instantly',
    'overloop-vs-reply', 'overloop-vs-saleshandy', 'overloop-vs-hubspot',
    'overloop-vs-artisan', 'lemlist-vs-apollo', 'instantly-vs-lemlist',
}

def vs_new_slug(old_slug):
    """Convert old blog slug to new versus slug."""
    return old_slug

# ── 4. Determine final action for each slug ──
def get_final_decision(slug, d):
    user = d['your_decision'].lower().strip().strip('"')
    notes = d['your_notes'].strip()
    reco = d['recommendation']
    target = d['redirect_target']
    reason = d['reason']

    # VS pages → redirect to /versus/
    if slug in vs_tool_slugs:
        new_slug = vs_new_slug(slug)
        return ('VS-REDIRECT', '/versus/{}'.format(new_slug), 'Redirect to new /versus/ section.')

    # User said "VS" explicitly
    if user == 'vs':
        new_slug = vs_new_slug(slug)
        return ('VS-REDIRECT', '/versus/{}'.format(new_slug), 'Redirect to new /versus/ section.')

    # User said "keep" variants
    if user.startswith('keep'):
        note = notes if notes else 'User override: keep as MIGRATE.'
        return ('MIGRATE', 'KEEP URL', note)

    # No user decision → use recommendation
    if not user:
        return (reco, target, reason)

    # Other explicit decisions
    return (user.upper(), target, reason)

# ── 5. Build all EN rows ──
en_rows = []
for slug, d in sorted(decisions.items()):
    action, target, note = get_final_decision(slug, d)
    en_rows.append({
        'action': action,
        'current_url': '/blog/{}'.format(slug),
        'target_url': target,
        'cluster': '',
        'slug_keyword': slug,
        'kw_volume': '',
        'gsc_impressions_3m': d['gsc_impressions'],
        'gsc_keywords': '',
        'backlink_domains': '',
        'note': note[:300],
    })

# ── 6. Write final CSV ──
fieldnames = ['action', 'current_url', 'target_url', 'cluster', 'slug_keyword',
              'kw_volume', 'gsc_impressions_3m', 'gsc_keywords', 'backlink_domains', 'note']

output = 'redirects/redirects.csv'
with open(output, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    # EN rows first
    for r in en_rows:
        writer.writerow(r)
    # Then INTL rows
    for r in existing_intl:
        writer.writerow({k: r.get(k, '') for k in fieldnames})

# Stats
from collections import Counter
actions = Counter(r['action'] for r in en_rows)
print("Wrote {} EN rows + {} INTL rows to {}".format(len(en_rows), len(existing_intl), output))
print()
print("EN decisions:")
for a in ['REWRITE', 'MIGRATE', 'CREATE', 'VS-REDIRECT', '301-CONSOLIDATE', '301-KILL']:
    print("  {}: {}".format(a, actions.get(a, 0)))
