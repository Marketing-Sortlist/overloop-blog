#!/usr/bin/env python3
"""Cross-reference 95 untriaged slugs with GSC data"""
import json, csv, re

# Load GSC data
with open('gsc-data.json') as f:
    gsc_data = json.load(f)

# Build slug -> GSC data map (EN only)
gsc_map = {}
for row in gsc_data:
    url = row['page']
    if '/blog/' in url and not re.search(r'/(de|fr|es|it)/blog/', url):
        slug = url.split('/blog/')[-1].rstrip('/')
        if slug:
            gsc_map[slug] = row

# Load webflow slugs
webflow_slugs = {}
with open('/Users/tanguy/Downloads/Overloop - blog export 14_04_26 - EN - primary.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        webflow_slugs[row['Slug'].strip()] = {
            'title': row['Title'].strip(),
            'category': row.get('Category', '').strip(),
            'date': row.get('Publication date', '').strip(),
            'description': row.get('Seo Description', '').strip()
        }

# Load triaged slugs
triaged = set()
with open('redirects/redirects.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row['current_url'].strip()
        if url.startswith('/blog/'):
            slug = url.replace('/blog/', '')
            triaged.add(slug)

# Cross-reference
results = []
for slug in sorted(webflow_slugs.keys()):
    if slug in triaged:
        continue
    info = webflow_slugs[slug]
    gsc = gsc_map.get(slug, {})
    clicks = gsc.get('clicks', 0)
    impressions = gsc.get('impressions', 0)
    ctr = gsc.get('ctr', 0)
    position = gsc.get('position', 0)
    date_str = info['date'][:11] if info['date'] else ''
    results.append((slug, clicks, impressions, ctr, position, date_str, info['category'], info['title']))

results.sort(key=lambda x: x[2], reverse=True)

print("{:<70s} {:>6s} {:>8s} {:>6s} {:>5s} {}".format('SLUG', 'CLICKS', 'IMPR', 'CTR', 'POS', 'CATEGORY'))
print('-' * 115)

for slug, clicks, impr, ctr, pos, date, cat, title in results:
    pos_str = "{:.1f}".format(pos) if pos > 0 else '-'
    ctr_str = "{:.1%}".format(ctr) if ctr > 0 else '-'
    print("{:<70s} {:>6d} {:>8d} {:>6s} {:>5s} {}".format(slug, clicks, impr, ctr_str, pos_str, cat))

print()
print("Total untriaged: {}".format(len(results)))
print("With impressions > 0: {}".format(sum(1 for r in results if r[2] > 0)))
print("With clicks > 0: {}".format(sum(1 for r in results if r[1] > 0)))
print("Zero impressions: {}".format(sum(1 for r in results if r[2] == 0)))
