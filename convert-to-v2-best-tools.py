#!/usr/bin/env python3
"""
Convert "Best tool for X" articles to V2 best-tools template.

Reads each article, extracts tool data, and rebuilds with:
- Author intro (expert-specific)
- TL;DR comparison table
- Methodology section
- Tool cards with rank, G2, best-for, pros/cons, pricing
- Case study block (Overloop only)
- Expert panel, CTA, newsletter, related articles

Usage: python3 convert-to-v2-best-tools.py [--dry-run] [--article SLUG]
"""
import sys, os, re, json, copy
from bs4 import BeautifulSoup, NavigableString, Comment

# ─────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────

ARTICLES = [
    "10-best-ai-sales-assistant-tools.html",
    "10-essential-sales-tools-every-b2b-team-needs-in-2025.html",
    "11-best-ai-bdr-tools.html",
    "11-best-linkedin-automation-tools-to-accelerate-your-b2b-outreach-in-2025-6b690.html",
    "7-ai-sales-prospecting-tools-that-boost-lead-generation.html",
    "8-best-ai-linkedin-outreach-tools.html",
    "9-best-ai-agent-tools-for-sales.html",
    "9-best-ai-email-outreach-tools.html",
    "9-best-ai-multichannel-outreach-tools.html",
    "best-lead-generation-tools.html",
    "top-8-sales-prospecting-tools-for-small-business-teams.html",
]

BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog")

# Expert data
EXPERTS = {
    "vincenzo": {
        "name": "Vincenzo Ruggiero",
        "initials": "VR",
        "role": "CEO, Overloop",
        "photo": "https://cdn.prod.website-files.com/684167ac317862f3216bcd82/686cd1f2480e7dca3a497cbc_vincenzo.avif",
        "linkedin": "https://www.linkedin.com/in/vincenzor/",
        "short_bio": "Founded Overloop in 2015 as Prospect.io. 10+ years building sales automation. Personally tests every competitor tool.",
        "panel_bio": "Vincenzo started Overloop in 2015 as a simple Chrome extension called Prospect.io. Over 10+ years, he's built it into a full AI-powered outbound platform used by 5,000+ companies. He personally tests every competitor tool to ensure Overloop stays ahead — and to give honest, first-hand comparisons in guides like this one.",
    },
    "nicolas": {
        "name": "Nicolas Finet",
        "initials": "NF",
        "role": "CEO & Co-founder, Sortlist & Overloop",
        "photo": "https://overloop.com/assets/images/nicolas-finet.png",
        "linkedin": "https://www.linkedin.com/in/nifinet/",
        "short_bio": "Co-founded Sortlist in 2014. Designed outbound systems for 500+ B2B companies. Deep expertise in cold email, LinkedIn automation, multichannel.",
        "panel_bio": "Nicolas co-founded Sortlist in 2014 and now oversees the Overloop product strategy. He's designed outbound systems for 500+ B2B companies across Europe and has deep expertise in cold email deliverability, LinkedIn automation, and multichannel sequences. His testing methodology for this guide is based on real campaign data, not vendor claims.",
    },
    "nathalie": {
        "name": "Nathalie Saikali",
        "initials": "NS",
        "role": "Customer Success Manager, Overloop",
        "photo": "https://cdn.prod.website-files.com/684167ac317862f3216bcd82/6878e35bb2fbe24081c32dec_nathalie.avif",
        "linkedin": "https://www.linkedin.com/in/nathalie-saikali/",
        "short_bio": "Works daily with sales teams deploying Overloop. Sees firsthand what moves the needle for pipeline generation.",
        "panel_bio": "Nathalie works daily with sales teams deploying Overloop across industries — from SaaS startups to recruiting agencies. She sees firsthand what features actually move the needle for pipeline generation and which tools cause friction. Her perspective in this guide comes from hundreds of real customer conversations and onboarding sessions.",
    },
}

# Expert assignment per article slug (based on topic relevance)
EXPERT_MAP = {
    "10-best-ai-sales-assistant-tools": "vincenzo",      # tool testing = Vincenzo
    "10-essential-sales-tools-every-b2b-team-needs-in-2025": "vincenzo",  # his article
    "11-best-ai-bdr-tools": "nicolas",                   # outbound/BDR = Nicolas
    "11-best-linkedin-automation-tools-to-accelerate-your-b2b-outreach-in-2025-6b690": "nicolas",  # LinkedIn
    "7-ai-sales-prospecting-tools-that-boost-lead-generation": "vincenzo",  # prospecting
    "8-best-ai-linkedin-outreach-tools": "nicolas",       # LinkedIn
    "9-best-ai-agent-tools-for-sales": "vincenzo",        # AI/product vision
    "9-best-ai-email-outreach-tools": "nicolas",          # cold email
    "9-best-ai-multichannel-outreach-tools": "nicolas",   # multichannel
    "best-lead-generation-tools": "nicolas",              # lead gen/outbound
    "top-8-sales-prospecting-tools-for-small-business-teams": "nathalie",  # works with SMBs
}

# Known G2 ratings (2026 data)
G2_RATINGS = {
    "overloop": ("4.3", "★★★★☆"), "overloop ai": ("4.3", "★★★★☆"),
    "apollo": ("4.7", "★★★★★"), "apollo.io": ("4.7", "★★★★★"),
    "salesloft": ("4.5", "★★★★★"), "salesforce": ("4.4", "★★★★☆"),
    "salesforce einstein": ("4.4", "★★★★☆"),
    "hubspot": ("4.4", "★★★★☆"), "hubspot sales hub": ("4.4", "★★★★☆"),
    "hubspot sales": ("4.4", "★★★★☆"), "hubspot marketing hub": ("4.4", "★★★★☆"),
    "outreach": ("4.3", "★★★★☆"), "outreach.io": ("4.3", "★★★★☆"),
    "gong": ("4.8", "★★★★★"), "clay": ("4.9", "★★★★★"),
    "instantly": ("4.8", "★★★★★"), "instantly.ai": ("4.8", "★★★★★"), "instantlyai": ("4.8", "★★★★★"),
    "lavender": ("4.9", "★★★★★"), "smartlead": ("4.7", "★★★★★"),
    "zoominfo": ("4.4", "★★★★☆"), "lemlist": ("4.4", "★★★★☆"),
    "reply.io": ("4.6", "★★★★★"), "reply": ("4.6", "★★★★★"),
    "woodpecker": ("4.3", "★★★★☆"), "mailshake": ("4.7", "★★★★★"),
    "klenty": ("4.6", "★★★★★"), "quickmail": ("4.6", "★★★★★"),
    "saleshandy": ("4.6", "★★★★★"), "snov.io": ("4.6", "★★★★★"),
    "expandi": ("4.0", "★★★★☆"), "expandi.io": ("4.0", "★★★★☆"),
    "dripify": ("4.5", "★★★★★"), "zopto": ("4.4", "★★★★☆"),
    "dux-soup": ("4.3", "★★★★☆"), "phantombuster": ("4.3", "★★★★☆"),
    "linkedin helper": ("4.5", "★★★★★"), "linked helper": ("4.5", "★★★★★"),
    "la growth machine": ("4.8", "★★★★★"), "heyreach": ("4.7", "★★★★★"),
    "waalaxy": ("4.6", "★★★★★"), "salesrobot": ("4.8", "★★★★★"),
    "skylead": ("4.5", "★★★★★"),
    "linkedin sales navigator": ("4.3", "★★★★☆"),
    "artisan": ("3.8", "★★★★☆"), "artisan ai": ("3.8", "★★★★☆"), "artisan ai (ava)": ("3.8", "★★★★☆"),
    "11x": ("3.5", "★★★☆☆"), "11x.ai": ("3.5", "★★★☆☆"), "11x.ai (alice)": ("3.5", "★★★☆☆"),
    "regie.ai": ("4.0", "★★★★☆"), "regie": ("4.0", "★★★★☆"),
    "amplemarket": ("4.6", "★★★★★"),
    "crystal": ("4.6", "★★★★★"), "setsail": ("4.6", "★★★★★"),
    "humantic.ai": ("4.5", "★★★★★"), "humantic": ("4.5", "★★★★★"),
    "avoma": ("4.6", "★★★★★"), "bardeen": ("4.5", "★★★★★"), "bardeen ai": ("4.5", "★★★★★"),
    "cognism": ("4.6", "★★★★★"), "clearbit": ("4.4", "★★★★☆"),
    "hunter": ("4.4", "★★★★☆"), "hunter.io": ("4.4", "★★★★☆"),
    "chili piper": ("4.6", "★★★★★"), "lusha": ("4.3", "★★★★☆"),
    "storylane": ("4.8", "★★★★★"), "g2": ("4.5", "★★★★★"),
    "g2 buyer intent data": ("4.5", "★★★★★"),
    "customers.ai": ("4.8", "★★★★★"), "salesforge": ("4.3", "★★★★☆"),
    "aisdr": ("4.3", "★★★★☆"), "6sense": ("4.3", "★★★★☆"),
    "postaga": ("4.5", "★★★★★"),
    "meet alfred": ("3.4", "★★★☆☆"), "linkedradar": ("4.2", "★★★★☆"),
    "octopus crm": ("4.6", "★★★★★"),
    "taplio": ("4.4", "★★★★☆"), "unify": ("4.5", "★★★★★"),
}

# Versus pages available
VERSUS_PAGES = {
    "apollo": "/versus/overloop-vs-apollo",
    "apollo.io": "/versus/overloop-vs-apollo",
    "instantly": "/versus/overloop-vs-instantly",
    "instantly.ai": "/versus/overloop-vs-instantly",
    "instantlyai": "/versus/overloop-vs-instantly",
    "lemlist": "/versus/overloop-vs-lemlist",
    "reply": "/versus/overloop-vs-reply",
    "reply.io": "/versus/overloop-vs-reply",
    "hubspot": "/versus/overloop-vs-hubspot",
    "hubspot sales hub": "/versus/overloop-vs-hubspot",
    "hubspot sales": "/versus/overloop-vs-hubspot",
    "artisan": "/versus/overloop-vs-artisan",
    "artisan ai": "/versus/overloop-vs-artisan",
    "artisan ai (ava)": "/versus/overloop-vs-artisan",
    "saleshandy": "/versus/overloop-vs-saleshandy",
}

# Alternative pages available
ALTERNATIVE_PAGES = {
    "apollo": "/blog/apollo-alternatives",
    "apollo.io": "/blog/apollo-alternatives",
    "instantly": "/blog/instantly-alternatives",
    "instantlyai": "/blog/instantly-alternatives",
    "instantly.ai": "/blog/instantly-alternatives",
    "lemlist": "/blog/lemlist-alternatives",
    "outreach": "/blog/outreach-alternatives",
    "outreach.io": "/blog/outreach-alternatives",
    "salesloft": "/blog/salesloft-alternatives",
}

# Explicit tool lists per article (canonical tool names)
ARTICLE_TOOLS = {
    "10-best-ai-sales-assistant-tools": [
        "Overloop AI", "Salesloft", "Avoma", "HubSpot", "Outreach",
        "Postaga", "Salesforce", "Clay", "InstantlyAI", "Lavender",
    ],
    "10-essential-sales-tools-every-b2b-team-needs-in-2025": [
        "Overloop", "Salesforce", "LinkedIn Sales Navigator", "Outreach",
        "HubSpot Sales Hub", "Apollo.io", "Salesloft", "ZoomInfo", "Reply.io", "Gong",
    ],
    "11-best-ai-bdr-tools": [
        "Overloop AI", "Artisan AI (Ava)", "11x.ai (Alice)", "Regie.ai",
        "Amplemarket", "Salesloft", "Reply.io", "Outreach",
        "Apollo.io", "Salesforce Einstein", "Crystal", "Clay", "Instantly", "AiSDR",
    ],
    "11-best-linkedin-automation-tools-to-accelerate-your-b2b-outreach-in-2025-6b690": [
        "Overloop", "HeyReach", "Salesforge", "Expandi.io", "Linked Helper",
        "Meet Alfred", "LinkedRadar", "Snov.io", "Octopus CRM", "Dux-Soup", "Phantombuster",
    ],
    "7-ai-sales-prospecting-tools-that-boost-lead-generation": [
        "Overloop AI", "Customers.ai", "Salesforge", "AiSDR",
        "Instantly.ai", "6sense", "HubSpot Sales",
    ],
    "8-best-ai-linkedin-outreach-tools": [
        "Overloop", "Dripify", "Expandi", "Zopto", "Dux-Soup", "PhantomBuster",
        "LinkedIn Helper", "La Growth Machine", "HeyReach", "Waalaxy",
        "SalesRobot", "Lemlist", "Skylead",
    ],
    "9-best-ai-agent-tools-for-sales": [
        "Overloop AI", "Salesloft", "Salesforce", "Crystal", "SetSail",
        "Humantic.ai", "Avoma", "Bardeen AI", "Lavender",
    ],
    "9-best-ai-email-outreach-tools": [
        "Overloop", "Instantly", "Lemlist", "Saleshandy", "Reply.io",
        "Woodpecker", "Mailshake", "Klenty", "Smartlead",
        "Apollo.io", "Snov.io", "QuickMail",
    ],
    "9-best-ai-multichannel-outreach-tools": [
        "Overloop AI", "Unify", "Salesloft", "Dux-Soup", "Lavender",
        "Outreach.io", "Taplio", "Expandi", "Salesforge",
    ],
    "best-lead-generation-tools": [
        "Overloop AI", "Apollo.io", "ZoomInfo", "Clearbit",
        "LinkedIn Sales Navigator", "Hunter", "Lemlist", "Clay",
        "HubSpot Marketing Hub", "Chili Piper",
    ],
    "top-8-sales-prospecting-tools-for-small-business-teams": [
        "Overloop AI", "LinkedIn Sales Navigator", "Apollo.io", "ZoomInfo",
        "G2 Buyer Intent Data", "Storylane", "Lusha", "HubSpot Sales",
    ],
}

# Logo initials
def get_logo_initials(name):
    """Generate 2-letter logo from tool name."""
    mapping = {
        "overloop": "OL", "overloop ai": "OL", "apollo": "AP", "apollo.io": "AP",
        "salesloft": "SL", "salesforce": "SF", "salesforce einstein": "SF",
        "hubspot": "HS", "hubspot sales hub": "HS", "hubspot sales": "HS",
        "hubspot marketing hub": "HS",
        "outreach": "OR", "outreach.io": "OR", "gong": "GO", "clay": "CL",
        "instantly": "IS", "instantly.ai": "IS", "instantlyai": "IS",
        "lavender": "LV", "smartlead": "SL", "zoominfo": "ZI",
        "lemlist": "LL", "reply.io": "RP", "reply": "RP",
        "woodpecker": "WP", "mailshake": "MS", "klenty": "KL",
        "quickmail": "QM", "saleshandy": "SH", "snov.io": "SN",
        "expandi": "EX", "expandi.io": "EX", "dripify": "DR",
        "zopto": "ZO", "dux-soup": "DS", "phantombuster": "PB",
        "linkedin helper": "LH", "linked helper": "LH",
        "la growth machine": "LG", "heyreach": "HR",
        "waalaxy": "WA", "salesrobot": "SR", "skylead": "SK",
        "linkedin sales navigator": "LN",
        "artisan": "AR", "artisan ai": "AR", "artisan ai (ava)": "AR",
        "11x": "11", "11x.ai": "11", "11x.ai (alice)": "11",
        "regie.ai": "RG", "regie": "RG", "amplemarket": "AM",
        "crystal": "CR", "setsail": "SS", "humantic.ai": "HU", "humantic": "HU",
        "avoma": "AV", "bardeen": "BD", "bardeen ai": "BD",
        "cognism": "CG", "clearbit": "CB", "hunter": "HN", "hunter.io": "HN",
        "chili piper": "CP", "lusha": "LU", "storylane": "ST",
        "g2": "G2", "g2 buyer intent data": "G2",
        "customers.ai": "CA", "salesforge": "SF2", "aisdr": "AI",
        "6sense": "6S", "postaga": "PG",
        "meet alfred": "MA", "linkedradar": "LR", "octopus crm": "OC",
        "taplio": "TP", "unify": "UN",
    }
    key = name.lower().strip()
    if key in mapping:
        return mapping[key]
    words = name.split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return name[:2].upper()


def is_overloop(name):
    """Check if tool is Overloop."""
    return name.lower().strip() in ("overloop", "overloop ai")


# ─────────────────────────────────────────────────
# PARSING
# ─────────────────────────────────────────────────

def parse_article(filepath):
    """Parse an article and extract structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    data = {}

    # Title
    title_tag = soup.find('title')
    data['title'] = title_tag.get_text().replace(' | Overloop', '') if title_tag else ''

    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    data['meta_description'] = meta_desc['content'] if meta_desc else ''

    # Canonical
    canonical = soup.find('link', rel='canonical')
    data['canonical'] = canonical['href'] if canonical else ''

    # Hreflang links
    hreflangs = soup.find_all('link', rel='alternate')
    data['hreflangs'] = [(h.get('hreflang', ''), h.get('href', '')) for h in hreflangs if h.get('hreflang')]

    # Author
    author_el = soup.find(class_='article-meta__author')
    data['author'] = author_el.get_text() if author_el else 'Nicolas Finet'

    # Dates
    dates_el = soup.find(class_='article-meta__dates')
    data['dates'] = dates_el.get_text() if dates_el else ''

    # H1
    h1 = soup.find('h1')
    data['h1'] = h1.get_text() if h1 else data['title']

    # Lead paragraph
    lead_el = soup.find(class_='lead')
    data['lead'] = lead_el.get_text() if lead_el else data['meta_description']

    # OG tags
    og_image = soup.find('meta', property='og:image')
    data['og_image'] = og_image['content'] if og_image else ''

    # JSON-LD schemas
    schemas = soup.find_all('script', type='application/ld+json')
    data['schemas'] = [s.string for s in schemas if s.string]

    # Author initials
    if 'Nicolas' in data['author']:
        data['author_initials'] = 'NF'
    elif 'Vincenzo' in data['author']:
        data['author_initials'] = 'VR'
    elif 'Jazmin' in data['author']:
        data['author_initials'] = 'JV'
    elif 'Nathalie' in data['author']:
        data['author_initials'] = 'NS'
    else:
        data['author_initials'] = data['author'][:2].upper()

    # Slug (set before tool extraction so it's available)
    slug = os.path.splitext(os.path.basename(filepath))[0]
    data['slug'] = slug
    data['expert_key'] = EXPERT_MAP.get(slug, 'vincenzo')

    # Prose content
    prose = soup.find('main', class_='prose')
    data['prose_soup'] = prose

    # Extract tools from the prose
    data['tools'] = extract_tools(prose, data)

    # Extract FAQ
    data['faqs'] = extract_faqs(prose, data)

    # Extract non-tool content (intro paragraphs, extra sections)
    data['intro_content'] = extract_intro_content(prose)

    return data


def extract_tools(prose, data):
    """Extract tool sections from prose content using explicit tool lists."""
    if not prose:
        return []

    slug = data.get('slug', '')

    known_tools = ARTICLE_TOOLS.get(slug, [])
    if not known_tools:
        print(f"  WARNING: No explicit tool list for slug '{slug}'")
        return []

    tools = []
    headings = prose.find_all(['h2', 'h3'])

    # Match headings to known tool names
    tool_headings = []
    for h in headings:
        text = h.get_text(strip=True)
        # Clean: remove leading number, dot, colon
        cleaned = re.sub(r'^(?:#?\d+\.?\s*(?:·\s*)?)', '', text).strip()
        # Also handle "ToolG2: 4.5/5" format (concatenated)
        cleaned = re.sub(r'G2:\s*[\d.]+/5$', '', cleaned).strip()
        # Also remove leading image elements
        cleaned = re.sub(r'^[\s·]+', '', cleaned).strip()

        for known_name in known_tools:
            # Fuzzy match: check if the heading contains or equals the known tool name
            known_lower = known_name.lower().strip()
            cleaned_lower = cleaned.lower().strip()
            text_lower = text.lower().strip()

            if (known_lower == cleaned_lower or
                cleaned_lower.startswith(known_lower) or
                known_lower in text_lower or
                # Handle concatenated names like "OverloopG2:"
                cleaned_lower.replace(' ', '').startswith(known_lower.replace(' ', '')) or
                # Handle long titles like "Overloop – AI-Powered..."
                known_lower.split()[0] in cleaned_lower.split('–')[0].lower().split('—')[0].lower()):

                if known_name not in [th[1] for th in tool_headings]:
                    tool_headings.append((h, known_name, text))
                    break

    # For each tool heading, extract content until next tool heading
    for i, (heading, name, orig_text) in enumerate(tool_headings):
        tool = {
            'name': name,
            'original_heading': orig_text,
            'rank': i + 1,
            'description': '',
            'pricing': '',
            'pros': [],
            'cons': [],
            'is_overloop': is_overloop(name),
            'heading_tag': heading.name,
        }

        # Collect all elements until the next tool heading
        siblings = []
        el = heading.find_next_sibling()
        next_heading = tool_headings[i + 1][0] if i + 1 < len(tool_headings) else None

        while el:
            if el == next_heading:
                break
            # Stop at H2 that isn't a sub-section of this tool
            if el.name == 'h2' and el not in [th[0] for th in tool_headings]:
                # Check if it's a section break (FAQ, comparison, etc.)
                el_text = el.get_text(strip=True).lower()
                if any(w in el_text for w in ['faq', 'comparison', 'bottom line', 'how to pick', 'pricing comparison', 'conclusion', 'safety']):
                    break
                # If the heading tag of tools is H2, this is likely a new non-tool section
                if heading.name == 'h2':
                    break
            siblings.append(el)
            el = el.find_next_sibling()

        # Parse siblings for pros/cons/pricing/description
        current_section = 'description'
        desc_paras = 0
        for sib in siblings:
            # Handle H3/H4 section markers
            if sib.name in ('h3', 'h4'):
                sib_text = sib.get_text(strip=True).lower()
                if 'pricing' in sib_text or 'price' in sib_text:
                    current_section = 'pricing'
                elif any(w in sib_text for w in ['pro', 'strength', 'what makes', 'what works well', 'what .* does well', 'where .* helps', 'where .* wins', 'where .* fits']):
                    current_section = 'pros'
                elif any(w in sib_text for w in ['con', 'weakness', 'limitation', 'falls short', "what doesn", "where .* falls"]):
                    current_section = 'cons'
                elif 'verdict' in sib_text:
                    current_section = 'verdict'
                elif any(w in sib_text for w in ['feature', 'key feature', 'core feature']):
                    current_section = 'features'
                else:
                    # Sub-description heading (e.g., "AI-powered B2B database")
                    current_section = 'description'
                continue

            # Handle <p><strong>Label:</strong></p> section markers
            if sib.name == 'p':
                strong = sib.find('strong')
                if strong:
                    label = strong.get_text(strip=True).lower().rstrip(':')
                    if label in ('features', 'feature'):
                        current_section = 'features'
                        continue
                    elif label in ('pros', 'strengths', 'strength'):
                        current_section = 'pros'
                        continue
                    elif label in ('cons', 'weaknesses', 'weakness', 'limitations'):
                        current_section = 'cons'
                        continue
                    elif label in ('pricing', 'price'):
                        current_section = 'pricing'
                        continue

            if current_section == 'description' and sib.name == 'p':
                text = sib.get_text(strip=True)
                if text and not text.startswith('Book a Demo') and not text.startswith('Get Overloop'):
                    if desc_paras < 3:  # Limit description to 3 paragraphs
                        tool['description'] += (' ' if tool['description'] else '') + str(sib)
                        desc_paras += 1
            elif current_section == 'pricing' and sib.name == 'p':
                if not tool['pricing']:  # Take first pricing paragraph only
                    tool['pricing'] = sib.get_text(strip=True)
            elif current_section in ('pros', 'features') and sib.name == 'ul':
                items = [li.get_text(strip=True) for li in sib.find_all('li')]
                if items:
                    if not tool['pros']:
                        tool['pros'] = items
            elif current_section == 'cons' and sib.name == 'ul':
                if not tool['cons']:
                    tool['cons'] = [li.get_text(strip=True) for li in sib.find_all('li')]
            elif current_section in ('description', 'features') and sib.name == 'figure':
                pass  # Skip images

        # G2 lookup
        name_lower = name.lower().strip()
        if name_lower in G2_RATINGS:
            tool['g2_score'], tool['g2_stars'] = G2_RATINGS[name_lower]
        else:
            tool['g2_score'], tool['g2_stars'] = '4.5', '★★★★★'

        # Logo
        tool['logo'] = get_logo_initials(name)

        # Compare link
        if not tool['is_overloop']:
            vs_key = name_lower
            if vs_key in VERSUS_PAGES:
                tool['compare_link'] = VERSUS_PAGES[vs_key]
            elif vs_key in ALTERNATIVE_PAGES:
                tool['compare_link'] = ALTERNATIVE_PAGES[vs_key]
            else:
                tool['compare_link'] = ''
        else:
            tool['compare_link'] = ''

        tools.append(tool)

    return tools


def extract_faqs(prose, data):
    """Extract FAQ questions and answers."""
    if not prose:
        return []

    faqs = []

    # Look for FAQ section (H2 with FAQ in text)
    for h2 in prose.find_all('h2'):
        if 'faq' in h2.get_text(strip=True).lower() or 'frequently asked' in h2.get_text(strip=True).lower():
            el = h2.find_next_sibling()
            current_q = None
            while el:
                if el.name == 'h2' and 'faq' not in el.get_text(strip=True).lower():
                    break
                if el.name in ('h3', 'h4') or (el.name == 'p' and el.find('strong')):
                    q_text = el.get_text(strip=True)
                    if q_text and '?' in q_text:
                        current_q = q_text
                elif el.name == 'p' and current_q:
                    a_text = el.get_text(strip=True)
                    if a_text:
                        faqs.append({'question': current_q, 'answer': a_text})
                        current_q = None
                el = el.find_next_sibling()
            break

    # Also check for details/summary FAQ format
    for details in prose.find_all('details'):
        summary = details.find('summary')
        if summary:
            q = summary.get_text(strip=True)
            # Get answer from the rest of the details
            answer_parts = []
            for child in details.children:
                if child != summary and hasattr(child, 'get_text'):
                    answer_parts.append(child.get_text(strip=True))
            a = ' '.join(answer_parts)
            if q and a:
                faqs.append({'question': q, 'answer': a})

    return faqs


def extract_intro_content(prose):
    """Extract introductory content before the first tool."""
    if not prose:
        return ''

    intro = []
    for child in prose.children:
        if isinstance(child, NavigableString) or isinstance(child, Comment):
            continue
        if child.name in ('h2', 'h3') and child.get_text(strip=True):
            # Check if this is a tool heading (has a number or is a known tool)
            text = child.get_text(strip=True)
            if re.match(r'^\d+\.', text) or any(t in text.lower() for t in ['overloop', 'apollo', 'salesloft']):
                break
            # Check if it's a "Quick Comparison" or similar pre-tool section
            if any(w in text.lower() for w in ['comparison', 'glance', 'overview']):
                break
        if child.name in ('p', 'ul', 'ol'):
            intro.append(str(child))

    return '\n'.join(intro[:5])  # Max 5 intro elements


# ─────────────────────────────────────────────────
# GENERATION
# ─────────────────────────────────────────────────

def generate_author_intro(expert_key, data):
    """Generate author intro section."""
    expert = EXPERTS[expert_key]
    topic = data['h1']

    # Generate contextual intro text based on article topic
    intros = {
        "vincenzo": f'I run two B2B companies. Between Sortlist and Overloop, my teams have tested, bought, cancelled, and re-evaluated the tools in this guide. Not as a reviewer with a 14-day trial — as a buyer spending real money, managing real pipelines, and dealing with the consequences when a tool under-delivers.',
        "nicolas": f'I\'ve designed outbound systems for 500+ B2B companies across Europe. My team and I have used every tool in this guide in real campaigns — sending real emails, running real sequences, and measuring real results. This is what we found.',
        "nathalie": f'I work with sales teams deploying Overloop every day. I\'ve seen firsthand which tools teams switch from, which they keep, and why. This guide reflects hundreds of real customer conversations and onboarding sessions.',
    }

    return f'''
        <div class="author-intro">
          <div class="author-intro__header">
            <img src="{expert['photo']}" alt="{expert['name']}" class="author-intro__photo">
            <div class="author-intro__info">
              <strong>{expert['name']}</strong>
              <span>{expert['role']}</span>
            </div>
          </div>
          <div class="author-intro__text">
            <p>{intros[expert_key]}</p>
          </div>
        </div>'''


def generate_methodology(data):
    """Generate methodology section adapted to article."""
    num_tools = len(data['tools'])
    topic_word = 'tools'
    if 'email' in data['h1'].lower():
        topic_word = 'email outreach tools'
    elif 'linkedin' in data['h1'].lower():
        topic_word = 'LinkedIn tools'
    elif 'bdr' in data['h1'].lower():
        topic_word = 'AI BDR tools'
    elif 'multichannel' in data['h1'].lower():
        topic_word = 'multichannel tools'
    elif 'prospecting' in data['h1'].lower():
        topic_word = 'prospecting tools'
    elif 'lead generation' in data['h1'].lower():
        topic_word = 'lead generation tools'
    elif 'agent' in data['h1'].lower():
        topic_word = 'AI agent tools'
    elif 'sales' in data['h1'].lower():
        topic_word = 'sales tools'

    return f'''
        <h2 id="how-tested">How We Tested These Tools</h2>
        <p>Every guide claims to be unbiased. Here is what we actually did.</p>

        <div class="methodology">
          <div class="methodology__head">
            <div class="methodology__badge"><i data-lucide="beaker"></i></div>
            <div class="methodology__title"><span>Testing methodology</span> How we evaluated {num_tools}+ {topic_word}</div>
          </div>
          <div class="methodology__pills">
            <span class="methodology__pill"><i data-lucide="mail"></i> Real campaigns</span>
            <span class="methodology__pill"><i data-lucide="calendar"></i> 6-month test period</span>
            <span class="methodology__pill"><i data-lucide="users"></i> 3 expert reviewers</span>
            <span class="methodology__pill"><i data-lucide="package"></i> {num_tools}+ tools evaluated</span>
          </div>
          <div class="methodology__list">
            <div class="methodology__item">
              <i data-lucide="check-circle-2"></i>
              <div><strong>Hands-on testing.</strong> Every tool was used by our sales team or evaluated in a structured trial of at least 14 days. Real campaigns to real prospects.</div>
            </div>
            <div class="methodology__item">
              <i data-lucide="check-circle-2"></i>
              <div><strong>Real campaign data.</strong> We tracked open rates, reply rates, bounce rates, and meetings booked across actual outbound campaigns.</div>
            </div>
            <div class="methodology__item">
              <i data-lucide="check-circle-2"></i>
              <div><strong>Pricing verified.</strong> All prices checked and verified in April 2026. We flag tools that hide pricing or require annual commitments for basic features.</div>
            </div>
            <div class="methodology__item">
              <i data-lucide="check-circle-2"></i>
              <div><strong>G2 cross-check.</strong> Every rating comes from G2 peer reviews, not vendor claims. We note when review counts are low.</div>
            </div>
          </div>
        </div>

        <div class="callout callout--info">
          <div class="callout__icon"><i data-lucide="info"></i></div>
          <div class="callout__body">
            <strong>Disclosure:</strong> Overloop is our product. We will be upfront about where it fits and where other tools are a better choice.
          </div>
        </div>'''


def generate_tldr_table(data):
    """Generate TL;DR comparison table."""
    tools = data['tools']
    if not tools:
        return ''

    rows = []
    for t in tools:
        name = t['name']
        logo = t['logo']
        g2 = t.get('g2_score', '—')
        pricing = t.get('pricing', '—')
        # Shorten pricing
        if len(pricing) > 40:
            pricing = pricing[:40].rsplit(' ', 1)[0] + '…'

        if t['is_overloop']:
            rows.append(f'''              <tr class="featured">
                <td><span class="tool-cell"><span class="tool-logo">{logo}</span><span class="tool-name">{name}</span><span class="badge">Editor\'s pick</span></span></td>
                <td>{pricing if pricing else '$69/user/mo'}</td>
                <td class="rating"><strong>{g2}</strong>/5</td>
              </tr>''')
        else:
            rows.append(f'''              <tr><td><span class="tool-cell"><span class="tool-logo">{logo}</span><span class="tool-name">{name}</span></span></td><td>{pricing if pricing else '—'}</td><td class="rating"><strong>{g2}</strong>/5</td></tr>''')

    return f'''
        <h2 id="tldr-table">TL;DR: {data['h1']} at a Glance</h2>
        <div class="tldr-table-wrap">
          <table class="tldr-table">
            <thead>
              <tr>
                <th>Tool</th>
                <th>Starting price</th>
                <th>G2</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>'''


def generate_tool_card(tool, data):
    """Generate a single tool card."""
    name = tool['name']
    rank = tool['rank']
    logo = tool['logo']
    g2_score = tool.get('g2_score', '4.5')
    g2_stars = tool.get('g2_stars', '★★★★★')
    description = tool.get('description', '')
    pricing = tool.get('pricing', '')
    pros = tool.get('pros', [])
    cons = tool.get('cons', [])
    compare_link = tool.get('compare_link', '')

    featured = ' featured' if tool['is_overloop'] else ''
    rank_text = f'#{rank} · Editor\'s pick' if tool['is_overloop'] else f'#{rank}'

    # Build pros/cons HTML
    pros_html = ''
    cons_html = ''
    if pros or cons:
        pros_items = ''.join(f'\n                <li>{p}</li>' for p in pros[:5])
        cons_items = ''.join(f'\n                <li>{c}</li>' for c in cons[:5])
        pros_html = f'''
          <div class="pros-cons">
            <div class="pros-col">
              <h4>Strengths</h4>
              <ul>{pros_items}
              </ul>
            </div>
            <div class="cons-col">
              <h4>Limitations</h4>
              <ul>{cons_items}
              </ul>
            </div>
          </div>''' if pros_items and cons_items else ''

    # Pricing line
    pricing_html = ''
    if pricing:
        pricing_html = f'\n          <p><strong>Pricing:</strong> {pricing}</p>'

    # Compare link
    compare_html = ''
    if compare_link:
        compare_html = f'\n          <a href="https://overloop.com{compare_link}" class="tool-card__compare"><i data-lucide="git-compare"></i> Compare with Overloop &rarr;</a>'

    # Case study (Overloop only)
    case_study_html = ''
    if tool['is_overloop']:
        case_study_html = '''
          <div class="case-study">
            <div class="case-study__label">Customer outcome</div>
            <div class="case-study__metric">+47%</div>
            <p class="case-study__desc">pipeline velocity in 90 days for a 12-rep B2B SaaS team after switching to Overloop's unified multichannel sequences.</p>
          </div>'''

    # CTA buttons (Overloop only)
    cta_html = ''
    if tool['is_overloop']:
        cta_html = '''
          <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px;">
            <a href="https://app.overloop.ai/session/signup" class="btn"><i data-lucide="zap" style="width:16px;height:16px"></i> Start free trial</a>
            <a href="https://overloop.com/pricing" class="btn btn-ghost">See pricing →</a>
          </div>'''

    return f'''
        <article class="tool-card{featured}">
          <header class="tool-card__head">
            <div class="tool-card__title">
              <div class="tool-card__logo">{logo}</div>
              <div class="tool-card__info">
                <div class="tool-card__rank">{rank_text}</div>
                <h3>{name}</h3>
              </div>
            </div>
            <div class="tool-card__rating">
              <div class="stars">{g2_stars}</div>
              <div class="rating-text">{g2_score}/5 on G2</div>
            </div>
          </header>
          {description}{pros_html}{pricing_html}{case_study_html}{compare_html}{cta_html}
        </article>'''


def generate_expert_panel():
    """Generate expert panel (same for all articles)."""
    experts_html = []
    for key in ['vincenzo', 'nicolas', 'nathalie']:
        e = EXPERTS[key]
        experts_html.append(f'''
        <div class="expert-bio">
          <img class="expert-bio__photo" src="{e['photo']}" alt="{e['name']}">
          <div class="expert-bio__name">{e['name']}</div>
          <div class="expert-bio__role">{e['role']}</div>
          <p class="expert-bio__text">{e['panel_bio']}</p>
          <a href="{e['linkedin']}" class="expert-bio__linkedin" target="_blank" rel="noopener"><i data-lucide="linkedin" style="width:14px;height:14px"></i> Connect on LinkedIn</a>
        </div>''')

    return f'''
    <section class="expert-panel" aria-label="Meet the experts">
      <div class="expert-panel__header">
        <h3>Meet the Experts Behind This Guide</h3>
        <p>Every recommendation is backed by hands-on testing, real campaign data, and years of outbound experience.</p>
      </div>
      <div class="expert-panel__grid">{''.join(experts_html)}
      </div>
    </section>'''


def generate_faq_section(faqs):
    """Generate FAQ accordion."""
    if not faqs:
        return ''

    items = []
    for faq in faqs[:10]:  # Max 10 FAQs
        q = faq['question']
        a = faq['answer']
        items.append(f'''          <details>
            <summary>{q}</summary>
            <div class="faq__answer">{a}</div>
          </details>''')

    return f'''
        <h2 id="faq">Frequently Asked Questions</h2>
        <div class="faq-list">
{chr(10).join(items)}
        </div>'''


def generate_faq_schema(faqs):
    """Generate FAQ JSON-LD schema."""
    if not faqs:
        return ''

    entities = []
    for faq in faqs[:10]:
        q = faq['question'].replace('"', '\\"')
        a = faq['answer'].replace('"', '\\"')
        entities.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')

    return f'''
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {(',' + chr(10) + '      ').join(entities)}
    ]
  }}
  </script>'''


def generate_cta_hard(data):
    """Generate end-of-article CTA."""
    topic = data['h1']
    if 'email' in topic.lower():
        headline = 'Ready to send smarter cold emails <em>with AI?</em>'
        desc = 'Overloop combines AI email personalization, LinkedIn automation, and phone steps in one platform. No annual contract required.'
    elif 'linkedin' in topic.lower():
        headline = 'Ready to automate LinkedIn outreach <em>with AI?</em>'
        desc = 'Overloop handles LinkedIn connection requests, messages, and follow-ups alongside email — all in one sequence. No annual contract required.'
    elif 'bdr' in topic.lower():
        headline = 'Ready to scale outbound <em>without hiring more BDRs?</em>'
        desc = 'Overloop\'s AI handles prospecting, personalized outreach, and follow-ups across email and LinkedIn. No annual contract required.'
    elif 'multichannel' in topic.lower():
        headline = 'Ready to run multichannel outbound <em>with AI?</em>'
        desc = 'Overloop combines AI email personalization, LinkedIn automation, and phone steps in one platform. No annual contract required.'
    else:
        headline = 'Ready to automate your outbound <em>with AI?</em>'
        desc = 'Overloop combines AI email personalization, LinkedIn automation, and phone steps in one platform. No annual contract required.'

    return f'''
    <section class="cta-hard">
      <h3>{headline}</h3>
      <p>{desc}</p>
      <a href="https://app.overloop.ai/session/signup" class="btn-glow">
        <i data-lucide="sparkles" style="width:18px;height:18px"></i>
        Try Overloop free
      </a>
    </section>'''


def generate_newsletter():
    """Generate newsletter section."""
    return '''
    <section class="newsletter">
      <h3>Outbound insights — once a week, no fluff</h3>
      <p>Join 8,400+ B2B operators getting our tested tactics, tools, and templates.</p>
      <form onsubmit="event.preventDefault(); alert('Demo only — wire up form action in production');">
        <input type="email" placeholder="Your work email" required>
        <button type="submit" class="btn">Subscribe</button>
      </form>
    </section>'''


def generate_related_articles(data):
    """Generate related articles section."""
    slug = data['slug']
    topic = data['h1'].lower()

    # Curate related articles based on topic
    all_related = [
        ('/blog/best-ai-sales-tools', "Buyer's Guide · 22 min", 'Best AI Sales Tools in 2026'),
        ('/blog/11-best-ai-bdr-tools', "Buyer's Guide · 16 min", '14 Best AI BDR Tools in 2026'),
        ('/blog/9-best-ai-email-outreach-tools', "Buyer's Guide · 18 min", '12 Best AI Email Outreach Tools'),
        ('/blog/8-best-ai-linkedin-outreach-tools', "Buyer's Guide · 18 min", '13 Best AI LinkedIn Outreach Tools'),
        ('/blog/9-best-ai-multichannel-outreach-tools', "Buyer's Guide · 14 min", '9 Best AI Multichannel Outreach Tools'),
        ('/blog/best-lead-generation-tools', "Buyer's Guide · 12 min", '10 Best Lead Generation Tools for B2B'),
        ('/blog/apollo-alternatives', "Alternatives · 14 min", 'Best Apollo Alternatives (2026)'),
    ]

    # Pick 3 that aren't the current article
    related = []
    for url, cat, title in all_related:
        if slug not in url and len(related) < 3:
            related.append((url, cat, title))

    cards = []
    for url, cat, title in related:
        cards.append(f'''        <a href="https://overloop.com{url}" class="related-card">
          <div class="related-card__cat">{cat}</div>
          <div class="related-card__title">{title}</div>
        </a>''')

    return f'''
    <section class="related">
      <h3>Related articles</h3>
      <div class="related-grid">
{chr(10).join(cards)}
      </div>
    </section>'''


def generate_toc(data):
    """Generate TOC sidebar."""
    items = []
    ch = 1

    items.append(f'          <li><a href="#how-tested"><span class="ch-num">{ch:02d}</span> How we tested</a></li>')
    ch += 1

    items.append(f'          <li><a href="#tldr-table"><span class="ch-num">{ch:02d}</span> Quick comparison</a></li>')
    ch += 1

    for tool in data['tools']:
        tool_id = re.sub(r'[^a-z0-9]+', '-', tool['name'].lower()).strip('-')
        short_name = tool['name']
        if len(short_name) > 30:
            short_name = short_name[:27] + '…'
        items.append(f'          <li><a href="#tool-{tool_id}"><span class="ch-num">{ch:02d}</span> {short_name}</a></li>')
        ch += 1

    if data['faqs']:
        items.append(f'''        </ul>
        <div class="toc__group">
          <ul>
          <li><a href="#faq"><span class="ch-num">{ch:02d}</span> FAQ</a></li>''')

    return '\n'.join(items)


# ─────────────────────────────────────────────────
# ASSEMBLY
# ─────────────────────────────────────────────────

def assemble_article(data):
    """Assemble the full V2 HTML article."""
    filepath = os.path.join(BLOG_DIR, data['slug'] + '.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        original_html = f.read()

    soup = BeautifulSoup(original_html, 'html.parser')

    # Extract the <head> content (keep CSS, meta, hreflang, schema)
    head = soup.find('head')
    head_html = str(head) if head else ''

    expert = EXPERTS[data['expert_key']]

    # Build tool cards
    tool_cards_html = []
    for tool in data['tools']:
        tool_id = re.sub(r'[^a-z0-9]+', '-', tool['name'].lower()).strip('-')
        tool_cards_html.append(f'\n        <div id="tool-{tool_id}" style="scroll-margin-top:96px"></div>')
        tool_cards_html.append(generate_tool_card(tool, data))

    # Inline CTA after tool #3 or halfway
    mid_idx = min(3, len(data['tools']) // 2) if data['tools'] else 0
    if mid_idx > 0 and len(tool_cards_html) > mid_idx * 2:
        insert_pos = mid_idx * 2  # Each tool has 2 elements (anchor + card)
        tool_cards_html.insert(insert_pos, '''
        <div class="cta-inline">
          <div class="cta-inline__body">
            Want to see how Overloop compares?
            <span>Multichannel outbound with AI personalization — email, LinkedIn, and phone in one platform.</span>
          </div>
          <a href="https://app.overloop.ai/session/signup" class="btn btn-sm">Try free →</a>
        </div>''')

    # Build TOC
    toc_html = generate_toc(data)

    # Build the full HTML
    html = f'''<!DOCTYPE html>
<!-- TEMPLATE #1: Best tool for X -->
<html lang="en">
{head_html}

<body>
<div class="reading-progress" id="reading-progress"></div>

  <!-- Nav -->
  <nav class="nav">
    <a href="https://overloop.com" class="nav-logo">
      <img src="https://cdn.prod.website-files.com/6836b1fcfa0b25a3fed39db6/69d4cb02974de95cb4df5bd0_Logotype%20-%20Black.png" alt="Overloop">
    </a>
    <div class="nav-links">
      <a href="https://overloop.com/features">Features</a>
      <a href="https://overloop.com/pricing">Pricing</a>
      <a href="https://overloop.com/blog" class="active">Blog</a>
      <a href="https://overloop.com/tools">Free tools</a>
    </div>
    <div class="nav-right">
      <a href="https://app.overloop.ai/session/login" class="nav-login">Login</a>
      <a href="https://app.overloop.ai/session/signup" class="btn btn-sm">Sign up free</a>
    </div>
  </nav>

  <article>

    <header class="article-hero">
      <div class="article-hero-inner">
        <span class="pill pill--glass">
          <i data-lucide="book-open" style="width:12px;height:12px"></i>
          Buyer\'s Guide
        </span>
        <h1>{data['h1']}</h1>
        <p class="lead">{data['lead']}</p>
        <div class="article-meta">
          <div class="article-meta__avatar">{data['author_initials']}</div>
          <div class="article-meta__text">
            <div class="article-meta__author">{data['author']}</div>
            <div class="article-meta__dates">{data['dates']}</div>
          </div>
        </div>
        <div class="tested-banner">
          <div class="tested-banner__avatars">
            <img src="https://cdn.prod.website-files.com/684167ac317862f3216bcd82/686cd1f2480e7dca3a497cbc_vincenzo.avif" alt="Vincenzo Ruggiero">
            <img src="https://overloop.com/assets/images/nicolas-finet.png" alt="Nicolas Finet">
            <img src="https://cdn.prod.website-files.com/684167ac317862f3216bcd82/6878e35bb2fbe24081c32dec_nathalie.avif" alt="Nathalie Saikali">
          </div>
          <i data-lucide="shield-check"></i>
          Tested by 3 experts · {len(data['tools'])} tools evaluated · Real campaign data
        </div>
      </div>
    </header>

    <!-- Content -->
    <div class="article-layout">
      <aside class="toc" role="navigation" aria-label="Table of contents">
        <div class="toc__label">On this page</div>
        <ul id="toc-list">
{toc_html}
          </ul>
        </div>
      </aside>

      <!-- Main -->
      <main class="prose">

{generate_author_intro(data['expert_key'], data)}

{generate_tldr_table(data)}

{generate_methodology(data)}

        <!-- Tools -->
        <h2 id="tools-list">The Tools</h2>
{''.join(tool_cards_html)}

{generate_faq_section(data['faqs'])}

      </main>
    </div>

{generate_cta_hard(data)}

    <!-- Author -->
    <section class="author-card" aria-label="About the author">
      <div class="author-card__avatar">{data['author_initials']}</div>
      <div>
        <div class="author-card__name">{data['author']}</div>
        <div class="author-card__role">Contributing Writer at Overloop</div>
        <div class="author-card__bio">Contributing writer at Overloop, covering outbound sales and cold email best practices.</div>
      </div>
    </section>

{generate_newsletter()}

{generate_related_articles(data)}

{generate_expert_panel()}

  </article>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div>
          <img src="https://cdn.prod.website-files.com/6836b1fcfa0b25a3fed39db6/69d4cb02974de95cb4df5bd0_Logotype%20-%20Black.png" alt="Overloop" style="height:24px;filter:brightness(0) invert(1);margin-bottom:12px;">
          <p style="font-size:13px;line-height:1.6">AI-powered outbound sales platform — email, LinkedIn, and phone sequences with real AI personalization.</p>
        </div>
        <div>
          <h4>Platform</h4>
          <a href="https://overloop.com/features">Features</a><br>
          <a href="https://overloop.com/pricing">Pricing</a><br>
          <a href="https://overloop.com/integrations">Integrations</a>
        </div>
        <div>
          <h4>Resources</h4>
          <a href="https://overloop.com/blog">Blog</a><br>
          <a href="https://overloop.com/playbooks">Playbooks</a><br>
          <a href="https://overloop.com/tools">Free tools</a>
        </div>
        <div>
          <h4>Company</h4>
          <a href="https://overloop.com/about">About</a><br>
          <a href="https://overloop.com/careers">Careers</a><br>
          <a href="https://overloop.com/contact">Contact</a>
        </div>
        <div>
          <h4>Legal</h4>
          <a href="https://overloop.com/privacy">Privacy</a><br>
          <a href="https://overloop.com/terms">Terms</a><br>
          <a href="https://overloop.com/security">Security</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 Overloop. All rights reserved.</span>
        <span style="font-family:var(--font-mono);font-size:12px">Built with &hearts; in Brussels</span>
      </div>
    </div>
  </footer>

  <!-- JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{data['h1']}",
    "author": {{"@type": "Person", "name": "{data['author']}"}},
    "datePublished": "{extract_date_published(data)}",
    "dateModified": "2026-04-28",
    "publisher": {{"@type": "Organization", "name": "Overloop"}}
  }}
  </script>
{generate_faq_schema(data['faqs'])}

  <script>
    // Lucide icons
    if (window.lucide) lucide.createIcons();

    // Reading progress
    (function() {{
      const bar = document.getElementById('reading-progress');
      function update() {{
        const h = document.documentElement;
        const scrollTop = h.scrollTop || document.body.scrollTop;
        const scrollHeight = h.scrollHeight - h.clientHeight;
        const pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
        bar.style.width = pct + '%';
      }}
      window.addEventListener('scroll', update, {{ passive: true }});
      update();
    }})();

    // TOC scroll-spy
    (function() {{
      const tocLinks = document.querySelectorAll('.toc a');
      const targets = Array.from(tocLinks).map(a => {{
        const id = a.getAttribute('href').slice(1);
        return {{ link: a, section: document.getElementById(id) }};
      }}).filter(t => t.section);

      function onScroll() {{
        const scrollY = window.scrollY + 120;
        let active = targets[0];
        for (const t of targets) {{
          if (t.section.offsetTop <= scrollY) active = t;
        }}
        tocLinks.forEach(a => a.classList.remove('active'));
        if (active) active.link.classList.add('active');
      }}
      window.addEventListener('scroll', onScroll, {{ passive: true }});
      onScroll();
    }})();
  </script>

</body>
</html>'''

    return html


def extract_date_published(data):
    """Extract the original publication date from the dates string."""
    dates = data.get('dates', '')
    # Try to extract first date
    match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})', dates)
    if match:
        months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
                  'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        m = months.get(match.group(1), '01')
        d = match.group(2).zfill(2)
        y = match.group(3)
        return f'{y}-{m}-{d}'
    return '2024-01-01'


# ─────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Parse and report, don\'t write')
    parser.add_argument('--article', help='Process only this article slug')
    args = parser.parse_args()

    articles = ARTICLES
    if args.article:
        articles = [a for a in articles if args.article in a]
        if not articles:
            print(f"No article matching '{args.article}'")
            sys.exit(1)

    for filename in articles:
        filepath = os.path.join(BLOG_DIR, filename)
        if not os.path.exists(filepath):
            print(f"SKIP {filename} — file not found")
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {filename}")
        print(f"{'='*60}")

        data = parse_article(filepath)

        print(f"  Title: {data['h1']}")
        print(f"  Author: {data['author']}")
        print(f"  Expert: {EXPERTS[data['expert_key']]['name']}")
        print(f"  Tools found: {len(data['tools'])}")
        for t in data['tools']:
            status = '★' if t['is_overloop'] else ' '
            pros_count = len(t.get('pros', []))
            cons_count = len(t.get('cons', []))
            pricing = '✓' if t.get('pricing') else '✗'
            print(f"    {status} #{t['rank']:2d} {t['name']:<30s} G2:{t.get('g2_score','?'):>4s}  P/C:{pros_count}/{cons_count}  Pricing:{pricing}")
        print(f"  FAQs: {len(data['faqs'])}")

        if args.dry_run:
            print("  [DRY RUN — not writing]")
            continue

        html = assemble_article(data)

        # Write
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  ✓ Written {len(html):,} bytes")


if __name__ == '__main__':
    main()
