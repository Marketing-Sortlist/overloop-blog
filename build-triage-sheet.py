#!/usr/bin/env python3
"""Build a Google Sheets-ready CSV with ALL 165+ EN articles: GSC + Oncrawl + triage decisions."""
import json, csv, re

# ── 1. Load GSC data ──
gsc_map = {}
with open('gsc-data.json') as f:
    gsc_data = json.load(f)
for row in gsc_data:
    url = row['page']
    if '/blog/' in url and not re.search(r'/(de|fr|es|it)/blog/', url):
        slug = url.split('/blog/')[-1].rstrip('/')
        if slug:
            gsc_map[slug] = row

# ── 2. Load Oncrawl bot data ──
oncrawl_map = {}
with open('oncrawl-blog-logs.json') as f:
    data = json.load(f)
for r in data.get('urls', []):
    url = r.get('url', '')
    if '/blog/' in url and not re.search(r'/(de|fr|es|it)/blog/', url):
        slug = url.split('/blog/')[-1].rstrip('/')
        if not slug:
            continue
        if slug not in oncrawl_map:
            oncrawl_map[slug] = {'google': 0, 'gpt': 0, 'oai_search': 0, 'claude': 0, 'perplexity': 0, 'gemini': 0, 'mistral': 0}
        oncrawl_map[slug]['google'] += (r.get('crawl_hits_google', 0) or 0)
        oncrawl_map[slug]['gpt'] += (r.get('crawl_hits_openai_gpt_bot', 0) or 0) + (r.get('crawl_hits_openai_chat_gpt_user', 0) or 0)
        oncrawl_map[slug]['oai_search'] += (r.get('crawl_hits_openai_search_bot', 0) or 0)
        oncrawl_map[slug]['claude'] += (r.get('crawl_hits_claude_bot', 0) or 0) + (r.get('crawl_hits_claude_search_bot', 0) or 0) + (r.get('crawl_hits_claude_user', 0) or 0)
        oncrawl_map[slug]['perplexity'] += (r.get('crawl_hits_perplexity_bot', 0) or 0) + (r.get('crawl_hits_perplexity_user', 0) or 0)
        oncrawl_map[slug]['gemini'] += (r.get('crawl_hits_google_gemini_deep_research', 0) or 0) + (r.get('crawl_hits_google_agent_search', 0) or 0)
        oncrawl_map[slug]['mistral'] += (r.get('crawl_hits_mistral_user', 0) or 0)

# ── 3. Load Webflow CSV ──
webflow = {}
with open('/Users/tanguy/Downloads/Overloop - blog export 14_04_26 - EN - primary.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        slug = row['Slug'].strip()
        webflow[slug] = {
            'title': row['Title'].strip(),
            'category': row.get('Category', '').strip(),
            'date': row.get('Publication date', '').strip()[:15],
            'author': row.get('Authors', '').strip(),
            'description': row.get('Seo Description', '').strip(),
        }

# ── 4. Load already-triaged decisions from redirects.csv ──
existing_decisions = {}
with open('redirects/redirects.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row['current_url'].strip()
        if url.startswith('/blog/') and not re.search(r'^/(de|fr|es|it)/', url):
            slug = url.replace('/blog/', '')
            existing_decisions[slug] = {
                'action': row['action'].strip(),
                'target': row['target_url'].strip(),
                'note': row.get('note', '').strip(),
            }

# ── 5. Check which articles are already built as HTML ──
import os
built_html = set()
en_dir = 'blog/en/'
if os.path.exists(en_dir):
    for f in os.listdir(en_dir):
        if f.endswith('.html') and f != 'index.html':
            built_html.add(f.replace('.html', ''))

# ── 6. Triage decisions for the 95 untriaged ──
product_updates = {
    'new-dashboard', 'reports-v2', 'attachments', 'deals-pipelines', 'lists-improvements',
    'salesforce-2-way-sync', 'new-integration-settings', 'web-application-re-design', 'store',
    'unsubscribe-link', '8-key-events-for-overloop-in-2020', 'why-are-we-starting-this-blog'
}
product_features_to_find_email = {
    'find-and-verify-emails-within-the-app', 'find-emails-with-name-organization-domain'
}
vs_redirects = {
    'instantly-vs-lemlist': '/blog/instantly-alternatives',
    'lemlist-vs-apollo': '/blog/apollo-alternatives',
    'overloop-vs-lemlist': '/blog/lemlist-alternatives',
    'overloop-vs-artisan': '/blog/best-ai-sales-tools',
}
consolidate_targets = {
    'the-ultimate-checklist-for-selecting-the-best-ai-sdr-tools-in-2025': '/blog/11-best-ai-bdr-tools',
    'top-ai-sdr-strategies-to-boost-your-b2b-sales-in-2025': '/blog/11-best-ai-bdr-tools',
    '9-best-ai-sales-workflow-tools': '/blog/best-ai-sales-tools',
    'how-an-ai-sales-tool-transformed-b2b-sales-teams-case-study-and-ai-sales-tool-reviews-2025': '/blog/best-ai-sales-tools',
    'cold-email-campaigns-reply-rates': '/blog/increase-reply-rate',
    'main-sales-objections': '/blog/deal-objections',
    '10-essential-b2b-prospect-sourcing-tools-for-2025-a-checklist-for-success': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
    'the-ultimate-guide-to-sales-leads-generation-for-b2b-teams-automation-strategies-and-tools': '/blog/best-ai-sales-tools',
    'ai-email-writer-revolution-how-to-use-ai-for-cold-outreach-in-outbound-sales': '/blog/9-best-ai-email-outreach-tools',
    'the-ultimate-guide-to-email-outreach-automation-for-b2b-sales-teams': '/blog/9-best-ai-email-outreach-tools',
}
rewrite_articles = {
    'how-to-write-a-successful-cold-email',
    'ai-generated-value-propositions-guide',
    'how-to-write-personalized-sales-emails-at-scale',
    'increase-reply-rate',
    'how-to-compose-a-follow-up-email',
    'best-sales-email-template',
}
migrate_articles = {
    'ai-sales-tools-roi-key-metrics-to-track',
    'common-sales-automation-mistakes-and-how-to-avoid-them',
    'how-ai-follow-up-scheduling-boosts-sales-efficiency',
    'how-to-use-overloop-email-finder-step-by-step-for-effortless-lead-generation',
    'lead-generation-strategies-every-saas-business-should-try-today',
    'sales-email-tips-to-help-you-close-more-deals',
    '10-proven-sales-prospecting-tips-to-boost-your-pipeline-fast',
    'how-to-build-scalable-lead-generation-workflows',
    'deal-objections', 'email-automation', 'following-up-surefire-techniques',
    '5-rules-more-successful-salespeople',
}
rescued_by_ai = {
    '10-essential-sales-tools-every-b2b-team-needs-in-2025': ('MIGRATE', 'KEEP URL', '202 AI hits (181 GPT). Too AI-visible to kill.'),
    'sales-engagement-platforms-compared-top-sales-engagement-platforms-2025-versus-guide': ('MIGRATE', 'KEEP URL', '140 AI hits (122 GPT). LLMs cite this actively.'),
    'ai-sales-tool-adoption-in-b2b-outbound-prospecting-2025-industry-review-analysis': ('MIGRATE', 'KEEP URL', '53 AI hits. Zero GSC but LLMs crawl it.'),
    'best-subject-lines-for-sales-emails': ('MIGRATE', 'KEEP URL', '8 AI hits (6 Perplexity). High-intent keyword.'),
    'sales-presentations': ('MIGRATE', 'KEEP URL', '18 AI hits (17 Perplexity). Perplexity sources this.'),
}

def get_new_decision(slug):
    oc = oncrawl_map.get(slug, {})
    gsc = gsc_map.get(slug, {})
    ai_total = sum(oc.get(k, 0) for k in ['gpt', 'oai_search', 'claude', 'perplexity', 'gemini', 'mistral'])
    impressions = gsc.get('impressions', 0)
    clicks = gsc.get('clicks', 0)

    if slug in rescued_by_ai:
        return rescued_by_ai[slug]
    if slug in rewrite_articles:
        return ('REWRITE', 'KEEP URL', 'Core topic. Full rewrite needed.')
    if slug in migrate_articles:
        return ('MIGRATE', 'KEEP URL', 'Has traffic/value. Template conversion.')
    if slug in consolidate_targets:
        return ('301-CONSOLIDATE', consolidate_targets[slug], 'Cannibalizes stronger article.')
    if slug in vs_redirects:
        return ('301-CONSOLIDATE', vs_redirects[slug], 'VS comparison cannibalizes alternatives page.')
    if slug in product_updates:
        return ('301-KILL', '/blog', 'Product update — obsolete.')
    if slug in product_features_to_find_email:
        return ('301-KILL', '/blog/how-to-find-someone-email-address-efficiently', 'Feature doc.')
    reason_parts = []
    if impressions == 0:
        reason_parts.append('Zero GSC impressions')
    elif clicks == 0 and impressions < 500:
        reason_parts.append('{} impr, 0 clicks'.format(impressions))
    else:
        reason_parts.append('{} impr, {} clicks'.format(impressions, clicks))
    if ai_total > 20:
        reason_parts.append('{} AI hits — REVIEW'.format(ai_total))
    return ('301-KILL', '/blog', '. '.join(reason_parts))

# ── 7. Build all rows ──
rows = []
for slug, info in webflow.items():
    gsc = gsc_map.get(slug, {})
    oc = oncrawl_map.get(slug, {})
    ai_total = sum(oc.get(k, 0) for k in ['gpt', 'oai_search', 'claude', 'perplexity', 'gemini', 'mistral'])

    # Determine status and decision
    html_built = slug in built_html
    if slug in existing_decisions:
        ed = existing_decisions[slug]
        recommendation = ed['action']
        redirect_target = ed['target']
        reason = ed['note'][:200] if ed['note'] else 'Previously triaged'
        status = 'DONE' if html_built else 'TRIAGED'
    else:
        recommendation, redirect_target, reason = get_new_decision(slug)
        status = 'NEW'

    rows.append({
        'status': status,
        'slug': slug,
        'title': info['title'],
        'url': 'https://overloop.com/blog/{}'.format(slug),
        'category': info['category'],
        'pub_date': info['date'],
        'author': info['author'],
        'html_built': 'YES' if html_built else '',
        # GSC (90 days: Jan 15 - Apr 14, 2026)
        'gsc_clicks': gsc.get('clicks', 0),
        'gsc_impressions': gsc.get('impressions', 0),
        'gsc_ctr_pct': round(gsc.get('ctr', 0) * 100, 2) if gsc.get('ctr') else 0,
        'gsc_avg_position': round(gsc.get('position', 0), 1) if gsc.get('position') else '',
        # Oncrawl logs (Mar 11 - Apr 15, 2026)
        'log_googlebot': oc.get('google', 0),
        'log_gptbot': oc.get('gpt', 0),
        'log_oai_searchbot': oc.get('oai_search', 0),
        'log_claudebot': oc.get('claude', 0),
        'log_perplexitybot': oc.get('perplexity', 0),
        'log_gemini': oc.get('gemini', 0),
        'log_mistral': oc.get('mistral', 0),
        'log_ai_total': ai_total,
        # Decision
        'recommendation': recommendation,
        'redirect_target': redirect_target,
        'reason': reason,
        # Tanguy input columns
        'your_decision': '',
        'your_notes': '',
    })

# Sort: status (NEW first), then by recommendation priority, then impressions desc
status_order = {'NEW': 0, 'TRIAGED': 1, 'DONE': 2}
action_order = {'REWRITE': 0, 'MIGRATE': 1, 'CREATE': 2, '301-CONSOLIDATE': 3, '301-KILL': 4, '301-KILL-INTL': 5}
rows.sort(key=lambda r: (
    status_order.get(r['status'], 9),
    action_order.get(r['recommendation'], 9),
    -r['gsc_impressions']
))

# ── 8. Write CSV ──
output_path = 'triage-all-en-articles.csv'
fieldnames = [
    'status', 'slug', 'title', 'url', 'category', 'pub_date', 'author', 'html_built',
    'gsc_clicks', 'gsc_impressions', 'gsc_ctr_pct', 'gsc_avg_position',
    'log_googlebot', 'log_gptbot', 'log_oai_searchbot', 'log_claudebot',
    'log_perplexitybot', 'log_gemini', 'log_mistral', 'log_ai_total',
    'recommendation', 'redirect_target', 'reason',
    'your_decision', 'your_notes'
]

with open(output_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Stats
from collections import Counter
print("Wrote {} articles to {}".format(len(rows), output_path))
print()
by_status = Counter(r['status'] for r in rows)
print("By status:")
for s in ['NEW', 'TRIAGED', 'DONE']:
    print("  {}: {}".format(s, by_status.get(s, 0)))
print()
by_action = Counter(r['recommendation'] for r in rows)
print("By recommendation:")
for a in ['REWRITE', 'MIGRATE', 'CREATE', '301-CONSOLIDATE', '301-KILL']:
    print("  {}: {}".format(a, by_action.get(a, 0)))
print()
print("Columns for your input:")
print("  'your_decision' → REWRITE | MIGRATE | 301-CONSOLIDATE | 301-KILL | SKIP")
print("  'your_notes'    → free text")
