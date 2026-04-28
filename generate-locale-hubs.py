#!/usr/bin/env python3
"""
generate-locale-hubs.py
=======================
Generates locale blog hub pages and pillar pages for FR / DE / ES / IT.

Usage:
    python3 generate-locale-hubs.py                 # generate all
    python3 generate-locale-hubs.py --dry-run       # preview without writing
    python3 generate-locale-hubs.py --locale fr     # only French
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("BeautifulSoup4 is required: pip install beautifulsoup4")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

BLOG_DIR = Path(__file__).parent / "blog"
VERSUS_DIR = Path(__file__).parent / "versus"
LOCALES = ["fr", "de", "es", "it"]

PILLARS_ORDER = ["prospecting", "sequence", "linkedin", "contact-db", "verification"]

PILLAR_NUMBERS = {
    "prospecting": "01",
    "sequence": "02",
    "linkedin": "03",
    "contact-db": "04",
    "verification": "05",
}

PILLAR_KEYWORDS = {
    "prospecting": [
        "prospect", "lead-gen", "lead_gen", "bdr", "sdr", "agent", "pipeline",
        "sales-tool", "sales-growth", "inside-sales", "outside-sales", "roi",
        "broken", "process", "closing", "tips", "best-practice", "saas-sales",
        "seasonal", "value-proposition", "assistant", "prospezione", "prospection",
        "prospeccion", "vertrieb", "vendita", "vente", "akquise", "pmi", "crescita",
        "crecimiento", "wachstum",
    ],
    "sequence": [
        "multichannel", "multicanal", "multicanale", "mehrkanalsequenz", "sequence",
        "follow-up", "relance", "nachfassen", "seguimiento", "outreach",
        "email-outreach", "cold-email", "engagement", "reply-rate", "open-rate",
        "subject-line", "email-length", "scheduling", "template", "swipe", "cadence",
        "signature", "objet-email", "betreffzeile", "asunto", "oggetto",
    ],
    "linkedin": ["linkedin"],
    "contact-db": [
        "contact", "database", "find-email", "trouver-email", "email-finden",
        "encontrar-email", "trovare-email", "b2b-data", "donnees", "daten",
        "datos", "dati", "enrichment",
    ],
    "verification": [
        "verif", "spam", "deliverability", "bounce", "domain-health", "dkim",
        "spf", "dmarc", "gdpr", "rgpd", "legal", "illegal", "compliance",
        "zustellbarkeit", "entregabilidad", "recapitabilit",
    ],
}

LOCALE_TEXT = {
    "fr": {
        "lang_code": "FR",
        "lang_attr": "fr",
        "flag_emoji": "&#127467;&#127479;",
        "lang_label": "Fran&ccedil;ais",
        "hero_h1": 'Construire un <em>meilleur outbound</em>.',
        "hero_lead": "Guides pratiques sur le cold email, la prospection LinkedIn, les outils de vente IA et l'automatisation outbound — écrits et testés par nos 3 experts.",
        "latest_h2": "Derniers articles",
        "latest_desc": "Récemment publiés et mis à jour",
        "trust_articles": "articles",
        "trust_tested": "Testés indépendamment",
        "trust_no_paid": "Sans placement payant",
        "trust_reviewed": "Révisés trimestriellement",
        "viewall_prefix": "Voir les",
        "viewall_suffix": "articles de ce pilier",
        "pillar_names": {
            "prospecting": ("Prospection Commerciale IA", "Stratégie, tactiques et processus pour trouver et qualifier des prospects B2B."),
            "sequence": ("Séquences Multicanal", "Orchestrer email, LinkedIn et téléphone dans des séquences personnalisées."),
            "linkedin": ("Automatisation LinkedIn", "Automatiser la prospection LinkedIn tout en restant dans les limites de la plateforme."),
            "contact-db": ("Base de Données Contacts", "Trouver des emails, numéros de téléphone et données d'entreprise B2B."),
            "verification": ("Vérification Email", "Délivrabilité, conformité RGPD et hygiène de liste."),
        },
        "meta_title": "Blog Overloop — Meilleures pratiques outbound en français",
        "meta_desc": "Guides pratiques sur le cold email, la prospection LinkedIn et les outils de vente IA — écrits et testés par nos 3 experts.",
        "breadcrumb_blog": "Blog",
        "pillar_page_all": "Tous les articles",
        "pillar_page_browse": "Parcourir la bibliothèque",
        "pillar_feat_label": "À la une",
        "pillar_discover": "Découvrir Overloop &rarr;",
        "versus_kicker": "Comparer les outils ?",
        "versus_h3": 'Comparez Overloop <em>avec les alternatives</em>.',
        "versus_p": "Comparaisons indépendantes des meilleurs outils de sales-tech — Apollo, Lemlist, Outreach, Salesloft, Instantly, La Growth Machine, et plus. Tarifs réels, fonctionnalités réelles, sans placements payants.",
        "versus_cta1": "Voir toutes les comparaisons &rarr;",
        "versus_cta2": "Essayer Overloop gratuitement",
        "newsletter_h3": 'Recevez <em>l\'Outbound Edge</em> dans votre boîte mail.',
        "newsletter_p": "Un email par semaine. Tactiques de cold email testées, avis sur les outils de vente IA, sans remplissage.",
        "newsletter_placeholder": "vous@entreprise.com",
        "newsletter_btn": "S'abonner",
        "newsletter_privacy": "Pas de spam. Désabonnement en 1 clic. Conforme au RGPD.",
        "experts_h2": 'Rédigé et testé par de <em>vrais praticiens</em>.',
        "experts_p": "Chaque article est rédigé ou révisé par l'un de nos trois experts internes qui dirigent quotidiennement des campagnes outbound pour des équipes SaaS B2B.",
        "experts_link": "Rencontrer l'équipe &rarr;",
    },
    "de": {
        "lang_code": "DE",
        "lang_attr": "de",
        "flag_emoji": "&#127465;&#127466;",
        "lang_label": "Deutsch",
        "hero_h1": 'Einblicke in <em>besseren Outbound</em>.',
        "hero_lead": "Praktische Guides zu Cold Email, LinkedIn Outreach, KI-Vertriebstools und Outbound-Automatisierung — geschrieben und getestet von unseren 3 Experten.",
        "latest_h2": "Neueste Artikel",
        "latest_desc": "Kürzlich veröffentlicht und aktualisiert",
        "trust_articles": "Artikel",
        "trust_tested": "Unabhängig getestet",
        "trust_no_paid": "Keine bezahlten Platzierungen",
        "trust_reviewed": "Vierteljährlich überprüft",
        "viewall_prefix": "Alle",
        "viewall_suffix": "Artikel in diesem Bereich ansehen",
        "pillar_names": {
            "prospecting": ("KI B2B Vertriebsprospecting", "Strategie, Taktiken und Prozesse für B2B-Prospecting im großen Maßstab."),
            "sequence": ("Multichannel-Sequenzen", "E-Mail, LinkedIn und Telefon in personalisierten Sequenzen orchestrieren."),
            "linkedin": ("LinkedIn-Automatisierung", "LinkedIn-Outreach automatisieren und dabei innerhalb der Plattformgrenzen bleiben."),
            "contact-db": ("Kontaktdatenbank", "E-Mails, Telefonnummern und B2B-Unternehmensdaten finden."),
            "verification": ("E-Mail-Verifizierung", "Zustellbarkeit, DSGVO-Konformität und Listenhygiene."),
        },
        "meta_title": "Overloop Blog — Outbound-Einblicke auf Deutsch",
        "meta_desc": "Praktische Guides zu Cold Email, LinkedIn Outreach und KI-Vertriebstools — geschrieben und getestet von unseren 3 Experten.",
        "breadcrumb_blog": "Blog",
        "pillar_page_all": "Alle Artikel",
        "pillar_page_browse": "Bibliothek durchsuchen",
        "pillar_feat_label": "Featured",
        "pillar_discover": "Overloop entdecken &rarr;",
        "versus_kicker": "Tools vergleichen?",
        "versus_h3": 'Sehen Sie, wie Overloop <em>im Vergleich</em> abschneidet.',
        "versus_p": "Unabhängige Vergleiche der besten Sales-Tech-Tools — Apollo, Lemlist, Outreach, Salesloft, Instantly, La Growth Machine und mehr. Echte Preise, echte Funktionen, keine bezahlten Platzierungen.",
        "versus_cta1": "Alle Vergleiche ansehen &rarr;",
        "versus_cta2": "Overloop kostenlos testen",
        "newsletter_h3": 'Erhalten Sie den <em>Outbound Edge</em> in Ihr Postfach.',
        "newsletter_p": "Eine E-Mail pro Woche. Getestete Cold-Email-Taktiken, KI-Vertriebstools-Reviews, kein Füllmaterial.",
        "newsletter_placeholder": "sie@unternehmen.de",
        "newsletter_btn": "Abonnieren",
        "newsletter_privacy": "Kein Spam. Abmeldung in 1 Klick. DSGVO-konform.",
        "experts_h2": 'Geschrieben und getestet von <em>echten Praktikern</em>.',
        "experts_p": "Jeder Artikel wird von einem unserer drei internen Experten verfasst oder überprüft, die täglich Outbound-Kampagnen für B2B-SaaS-Teams durchführen.",
        "experts_link": "Das Team kennenlernen &rarr;",
    },
    "es": {
        "lang_code": "ES",
        "lang_attr": "es",
        "flag_emoji": "&#127466;&#127480;",
        "lang_label": "Espa&ntilde;ol",
        "hero_h1": 'Ideas para un <em>mejor outbound</em>.',
        "hero_lead": "Guías prácticas sobre cold email, prospección en LinkedIn, herramientas de ventas IA y automatización outbound — escritas y probadas por nuestros 3 expertos.",
        "latest_h2": "Últimos artículos",
        "latest_desc": "Publicados y actualizados recientemente",
        "trust_articles": "artículos",
        "trust_tested": "Probados independientemente",
        "trust_no_paid": "Sin colocaciones pagadas",
        "trust_reviewed": "Revisados trimestralmente",
        "viewall_prefix": "Ver los",
        "viewall_suffix": "artículos de este pilar",
        "pillar_names": {
            "prospecting": ("Prospección Comercial IA", "Estrategia, tácticas y procesos para encontrar y cualificar prospectos B2B."),
            "sequence": ("Secuencias Multicanal", "Orquestar email, LinkedIn y teléfono en secuencias personalizadas."),
            "linkedin": ("Automatización LinkedIn", "Automatizar el outreach en LinkedIn manteniéndose dentro de los límites de la plataforma."),
            "contact-db": ("Base de Datos de Contactos", "Encontrar emails, números de teléfono y datos de empresas B2B."),
            "verification": ("Verificación de Email", "Entregabilidad, cumplimiento GDPR e higiene de listas."),
        },
        "meta_title": "Blog Overloop — Insights outbound en Español",
        "meta_desc": "Guías prácticas sobre cold email, prospección en LinkedIn y herramientas de ventas IA — escritas y probadas por nuestros 3 expertos.",
        "breadcrumb_blog": "Blog",
        "pillar_page_all": "Todos los artículos",
        "pillar_page_browse": "Explorar la biblioteca",
        "pillar_feat_label": "Destacados",
        "pillar_discover": "Descubrir Overloop &rarr;",
        "versus_kicker": "¿Comparando herramientas?",
        "versus_h3": 'Vea cómo Overloop <em>se compara</em> con las alternativas.',
        "versus_p": "Comparaciones independientes de las mejores herramientas de sales-tech — Apollo, Lemlist, Outreach, Salesloft, Instantly, La Growth Machine y más. Precios reales, funciones reales, sin colocaciones pagadas.",
        "versus_cta1": "Ver todas las comparaciones &rarr;",
        "versus_cta2": "Probar Overloop gratis",
        "newsletter_h3": 'Recibe el <em>Outbound Edge</em> en tu bandeja de entrada.',
        "newsletter_p": "Un email por semana. Tácticas de cold email probadas, reseñas de herramientas de ventas IA, sin relleno.",
        "newsletter_placeholder": "tu@empresa.com",
        "newsletter_btn": "Suscribirse",
        "newsletter_privacy": "Sin spam. Cancelación en 1 clic. Cumple con el GDPR.",
        "experts_h2": 'Escrito y probado por <em>profesionales reales</em>.',
        "experts_p": "Cada artículo es escrito o revisado por uno de nuestros tres expertos internos que ejecutan campañas outbound diariamente para equipos SaaS B2B.",
        "experts_link": "Conocer al equipo &rarr;",
    },
    "it": {
        "lang_code": "IT",
        "lang_attr": "it",
        "flag_emoji": "&#127470;&#127481;",
        "lang_label": "Italiano",
        "hero_h1": 'Costruire un <em>outbound migliore</em>.',
        "hero_lead": "Guide pratiche su cold email, prospecting LinkedIn, strumenti di vendita AI e automazione outbound — scritte e testate dai nostri 3 esperti.",
        "latest_h2": "Ultimi articoli",
        "latest_desc": "Pubblicati e aggiornati di recente",
        "trust_articles": "articoli",
        "trust_tested": "Testati indipendentemente",
        "trust_no_paid": "Nessun posizionamento a pagamento",
        "trust_reviewed": "Revisionati trimestralmente",
        "viewall_prefix": "Vedi tutti i",
        "viewall_suffix": "articoli di questo pilastro",
        "pillar_names": {
            "prospecting": ("Prospezione Commerciale AI", "Strategia, tattiche e processi per trovare e qualificare prospect B2B."),
            "sequence": ("Sequenze Multicanale", "Orchestrare email, LinkedIn e telefono in sequenze personalizzate."),
            "linkedin": ("Automazione LinkedIn", "Automatizzare l'outreach LinkedIn restando nei limiti della piattaforma."),
            "contact-db": ("Database Contatti", "Trovare email, numeri di telefono e dati aziendali B2B."),
            "verification": ("Verifica Email", "Deliverability, conformità GDPR e igiene delle liste."),
        },
        "meta_title": "Blog Overloop — Insights outbound in Italiano",
        "meta_desc": "Guide pratiche su cold email, prospecting LinkedIn e strumenti di vendita AI — scritte e testate dai nostri 3 esperti.",
        "breadcrumb_blog": "Blog",
        "pillar_page_all": "Tutti gli articoli",
        "pillar_page_browse": "Sfoglia la libreria",
        "pillar_feat_label": "In primo piano",
        "pillar_discover": "Scopri Overloop &rarr;",
        "versus_kicker": "Confrontando gli strumenti?",
        "versus_h3": 'Scopri come Overloop <em>si confronta</em> con le alternative.',
        "versus_p": "Confronti indipendenti dei migliori strumenti sales-tech — Apollo, Lemlist, Outreach, Salesloft, Instantly, La Growth Machine e altri. Prezzi reali, funzionalità reali, nessun posizionamento a pagamento.",
        "versus_cta1": "Vedi tutti i confronti &rarr;",
        "versus_cta2": "Prova Overloop gratis",
        "newsletter_h3": 'Ricevi l\'<em>Outbound Edge</em> nella tua casella di posta.',
        "newsletter_p": "Una email alla settimana. Tattiche di cold email testate, recensioni di strumenti di vendita AI, senza riempitivo.",
        "newsletter_placeholder": "tu@azienda.com",
        "newsletter_btn": "Iscriviti",
        "newsletter_privacy": "Nessuno spam. Cancellazione in 1 clic. Conforme al GDPR.",
        "experts_h2": 'Scritto e testato da <em>veri professionisti</em>.',
        "experts_p": "Ogni articolo è scritto o revisionato da uno dei nostri tre esperti interni che gestiscono quotidianamente campagne outbound per team SaaS B2B.",
        "experts_link": "Conosci il team &rarr;",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# ARTICLE EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_article_meta(html_path: Path) -> dict:
    """Extract metadata from a locale article HTML file."""
    slug = html_path.stem  # filename without .html
    try:
        content = html_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [WARN] Could not read {html_path}: {e}")
        return None

    soup = BeautifulSoup(content, "html.parser")

    # Title
    title_tag = soup.find("title")
    title = title_tag.get_text() if title_tag else slug
    # Strip " | Overloop" suffix
    title = re.sub(r"\s*\|\s*Overloop\s*$", "", title).strip()

    # Description
    desc_tag = soup.find("meta", {"name": "description"})
    description = desc_tag.get("content", "") if desc_tag else ""

    # Canonical
    canonical_tag = soup.find("link", {"rel": "canonical"})
    canonical = canonical_tag.get("href", "") if canonical_tag else ""

    # Author: try JSON-LD first
    author = ""
    for script in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "{}")
            # Handle @graph
            if "@graph" in data:
                for node in data["@graph"]:
                    if "author" in node:
                        a = node["author"]
                        if isinstance(a, dict):
                            author = a.get("name", "")
                        break
            elif "author" in data:
                a = data["author"]
                if isinstance(a, dict):
                    author = a.get("name", "")
                elif isinstance(a, str):
                    author = a
            if author:
                break
        except Exception:
            pass

    # Author fallback: article-meta__author div
    if not author:
        meta_div = soup.find("div", class_="article-meta__author")
        if meta_div:
            author = meta_div.get_text(strip=True)

    # Author fallback: look for common author name patterns in text
    if not author:
        # Try finding author in JSON-LD by looking more broadly
        for script in soup.find_all("script", {"type": "application/ld+json"}):
            try:
                data = json.loads(script.string or "{}")
                if isinstance(data, list):
                    for item in data:
                        if "author" in item:
                            a = item["author"]
                            if isinstance(a, dict):
                                author = a.get("name", "")
                            elif isinstance(a, str):
                                author = a
                            if author:
                                break
            except Exception:
                pass
            if author:
                break

    # datePublished / dateModified from JSON-LD
    date_published = ""
    date_modified = ""
    for script in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "{}")
            nodes = []
            if "@graph" in data:
                nodes = data["@graph"]
            elif isinstance(data, list):
                nodes = data
            else:
                nodes = [data]
            for node in nodes:
                if not date_published and "datePublished" in node:
                    date_published = node["datePublished"]
                if not date_modified and "dateModified" in node:
                    date_modified = node["dateModified"]
            if date_published or date_modified:
                break
        except Exception:
            pass

    # Estimate read time: word count from article body
    article_body = soup.find("article") or soup.find("main") or soup.body
    word_count = 0
    if article_body:
        text = article_body.get_text(" ", strip=True)
        word_count = len(text.split())
    read_time = max(3, round(word_count / 200)) if word_count else 7

    return {
        "slug": slug,
        "title": title,
        "description": description,
        "canonical": canonical,
        "author": author or "Vincenzo Ruggiero",
        "date_published": date_published,
        "date_modified": date_modified,
        "read_time": read_time,
        "word_count": word_count,
    }


def assign_pillar(slug: str, title: str) -> str:
    """Assign an article to a pillar based on slug keywords."""
    text = (slug + " " + title).lower()
    # linkedin gets priority because 'linkedin' keyword is very specific
    if "linkedin" in text:
        return "linkedin"
    for pillar in ["verification", "contact-db", "sequence"]:
        for kw in PILLAR_KEYWORDS[pillar]:
            if kw in text:
                return pillar
    for kw in PILLAR_KEYWORDS["prospecting"]:
        if kw in text:
            return "prospecting"
    # catch-all
    return "prospecting"


def get_card_type(slug: str, title: str) -> tuple:
    """Returns (css_class, pill_label) for a post card."""
    t = (slug + " " + title).lower()
    if "vs" in slug.split("-") or "versus" in slug or "compar" in t:
        return "versus", "Comparison"
    if "alternative" in t:
        return "versus", "Alternatives"
    if ("best" in t or "meilleur" in t or "mejor" in t or "miglio" in t
            or "besten" in t or t.startswith("top-") or "-top-" in slug):
        return "besttools", "Best Tools"
    if ("how-to" in slug or "guide" in t or "comment" in t or "wie" in t
            or "cómo" in t or slug.startswith("come-") or "-come-" in slug):
        return "howto", "How-To"
    if "template" in t or "script" in t or "swipe" in t:
        return "templates", "Templates"
    if "review" in t or "avis" in t:
        return "review", "Review"
    if "strategy" in t or "strateg" in t or "playbook" in t:
        return "strategy", "Strategy"
    return "tactical", "Tactical"


def format_date(date_str: str) -> str:
    """Format ISO date string to human-readable e.g. 'Jan 15, 2025'."""
    if not date_str:
        return ""
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str[:19], fmt[:len(fmt)])
            return dt.strftime("%b %d, %Y").replace(" 0", " ")
        except ValueError:
            continue
    return date_str[:10]


def get_initials(name: str) -> str:
    """Get initials from an author name."""
    parts = name.split()
    if len(parts) >= 2:
        return parts[0][0].upper() + parts[-1][0].upper()
    return name[:2].upper() if name else "??"


def truncate(text: str, max_chars: int = 120) -> str:
    """Truncate text to max_chars, breaking at word boundary."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_space = truncated.rfind(" ")
    if last_space > max_chars * 0.7:
        truncated = truncated[:last_space]
    return truncated.rstrip(".,;:") + "…"


# ─────────────────────────────────────────────────────────────────────────────
# HTML COMPONENT BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

SHARED_STYLE = """\
    /* ============= TOKENS ============= */
    :root {
      --color-primary: #6366F1; --color-primary-dark: #4F46E5; --color-primary-light: #818CF8;
      --color-primary-50: #EEF2FF; --color-primary-100: #E0E7FF;
      --color-secondary: #A855F7; --color-secondary-dark: #9333EA; --color-secondary-50: #FAF5FF;
      --gradient-brand: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
      --gradient-brand-soft: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(168,85,247,0.08) 100%);
      --gradient-hero-bg: linear-gradient(180deg, #FFFFFF 0%, #EEF2FF 50%, #FAFAFA 100%);
      --color-bg: #FAFAFA; --color-surface: #F3F4F6; --color-surface-alt: #F8FAFC;
      --color-white: #FFFFFF; --color-border: #E5E7EB; --color-border-light: #F3F4F6;
      --color-text: #1A1A2E; --color-text-body: #374151; --color-text-secondary: #64748B;
      --color-muted: #94A3B8; --color-dark: #1F2937;
      --color-success: #10B981;
      --font-sans: 'Epilogue', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-accent: 'Playfair Display', Georgia, serif;
      --font-mono: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace;
      --r-sm: 8px; --r: 12px; --r-lg: 16px; --r-xl: 24px; --r-pill: 100px;
      --shadow-sm: 0 2px 8px rgba(0,0,0,0.04);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
      --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
      --shadow-glow: 0 8px 32px rgba(99, 102, 241, 0.30);
      --container-max: 1200px;
      --page-px: 48px;
      --t: 200ms ease;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }
    body { font-family: var(--font-sans); color: var(--color-text-body); background: var(--color-bg); line-height: 1.7; font-size: 17px; }
    a { color: var(--color-primary); text-decoration: none; transition: var(--t); }
    a:hover { color: var(--color-primary-dark); text-decoration: underline; }
    .gradient-text { background: var(--gradient-brand); -webkit-background-clip: text; background-clip: text; color: transparent; -webkit-text-fill-color: transparent; }

    /* ============= NAV ============= */
    .nav { position: sticky; top: 0; z-index: 100; display: flex; align-items: center; gap: 2rem; height: 72px; padding: 0 var(--page-px); background: rgba(255,255,255,0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--color-border-light); }
    .nav-logo { display: flex; align-items: center; text-decoration: none; flex-shrink: 0; }
    .nav-logo img { height: 28px; width: auto; }
    .nav-links { display: flex; gap: 1.5rem; margin-right: auto; }
    .nav-links a { font-size: 14px; font-weight: 500; color: var(--color-text-secondary); }
    .nav-links a:hover, .nav-links a.active { color: var(--color-text); text-decoration: none; }
    .nav-right { display: flex; align-items: center; gap: 0.75rem; }
    .nav-login { font-size: 14px; font-weight: 500; color: var(--color-text-secondary); }

    /* ============= BUTTONS ============= */
    .btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 12px 24px; background: var(--color-primary); color: #fff; border: none; border-radius: var(--r); font-family: var(--font-sans); font-size: 15px; font-weight: 600; text-decoration: none !important; cursor: pointer; box-shadow: var(--shadow-md); transition: var(--t); }
    .btn:hover { background: var(--color-primary-dark); box-shadow: var(--shadow-glow); transform: translateY(-1px); color: #fff; }
    .btn-sm { padding: 8px 18px; font-size: 13px; }
    .btn-ghost { background: transparent; color: var(--color-text); border: 1.5px solid var(--color-text); box-shadow: none; }
    .btn-ghost:hover { background: var(--color-text); color: #fff; box-shadow: none; transform: none; }

    /* ============= HERO ============= */
    .blog-hero { background: var(--gradient-hero-bg); padding: 80px var(--page-px) 56px; position: relative; overflow: hidden; }
    .blog-hero::before { content: ''; position: absolute; top: -100px; right: -100px; width: 500px; height: 500px; border-radius: 50%; background: radial-gradient(circle, rgba(168,85,247,0.10) 0%, rgba(99,102,241,0) 70%); pointer-events: none; }
    .blog-hero-inner { max-width: var(--container-max); margin: 0 auto; position: relative; z-index: 1; }
    .breadcrumb { font-size: 13px; color: var(--color-text-secondary); margin-bottom: 20px; font-family: var(--font-mono); letter-spacing: 0.02em; }
    .breadcrumb a { color: var(--color-text-secondary); }
    .breadcrumb a:hover { color: var(--color-primary); text-decoration: none; }
    .blog-hero h1 { font-size: clamp(40px, 5.5vw, 64px); font-weight: 800; color: var(--color-text); line-height: 1.05; letter-spacing: -0.025em; margin-bottom: 20px; max-width: 880px; }
    .blog-hero h1 em { font-family: var(--font-accent); font-style: italic; font-weight: 400; }
    .blog-hero .lead { font-size: 20px; line-height: 1.5; color: var(--color-text-secondary); max-width: 640px; margin: 0 0 28px; }
    .trust-line { display: inline-flex; gap: 14px; flex-wrap: wrap; align-items: center; padding: 10px 16px; background: rgba(255,255,255,0.65); border: 1px solid var(--color-border-light); border-radius: var(--r-pill); font-family: var(--font-mono); font-size: 11px; font-weight: 600; letter-spacing: 0.04em; color: var(--color-text-secondary); }
    .trust-line .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--color-success); box-shadow: 0 0 0 4px rgba(16,185,129,0.15); }
    .trust-line span { color: var(--color-text-secondary); }
    .trust-line span strong { color: var(--color-text); font-weight: 700; }
    .trust-line span + span::before { content: '·'; margin-right: 14px; color: var(--color-muted); }

    /* ============= EXPERTS BAND (E-E-A-T) ============= */
    .experts-band { max-width: var(--container-max); margin: 0 auto; padding: 56px var(--page-px) 24px; }
    .experts-head { display: flex; justify-content: space-between; align-items: end; margin-bottom: 32px; gap: 32px; flex-wrap: wrap; }
    .experts-head h2 { font-size: 28px; font-weight: 800; letter-spacing: -0.018em; color: var(--color-text); margin: 0 0 6px; }
    .experts-head h2 em { font-family: var(--font-accent); font-style: italic; font-weight: 400; }
    .experts-head p { color: var(--color-text-secondary); font-size: 15px; margin: 0; max-width: 540px; }
    .experts-head a { font-size: 14px; font-weight: 600; color: var(--color-primary); white-space: nowrap; }
    .experts-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .expert-card { background: #fff; border: 1px solid var(--color-border-light); border-radius: var(--r-lg); padding: 22px; display: flex; gap: 16px; align-items: flex-start; transition: var(--t); }
    .expert-card:hover { box-shadow: var(--shadow-md); border-color: var(--color-primary-100); }
    .expert-photo { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 2px solid #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    .expert-photo-fallback { width: 56px; height: 56px; border-radius: 50%; background: var(--gradient-brand); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    .expert-info strong { font-size: 15px; font-weight: 700; color: var(--color-text); display: block; margin-bottom: 2px; }
    .expert-info .role { font-family: var(--font-mono); font-size: 11px; color: var(--color-primary); letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 8px; }
    .expert-info p { font-size: 13px; line-height: 1.55; color: var(--color-text-secondary); margin: 0; }

    /* ============= LATEST ARTICLES ============= */
    .latest-section { max-width: var(--container-max); margin: 0 auto; padding: 48px var(--page-px) 32px; }
    .latest-head { margin-bottom: 24px; }
    .latest-head h2 { font-size: 24px; font-weight: 800; color: var(--color-text); margin: 0 0 4px; letter-spacing: -0.015em; }
    .latest-head p { font-size: 14px; color: var(--color-text-secondary); margin: 0; }
    .latest-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    @media (max-width: 991px) { .latest-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 479px) { .latest-grid { grid-template-columns: 1fr; } }
    .latest-card {
      background: #fff; border: 1px solid var(--color-border-light); border-radius: var(--r);
      padding: 20px; display: flex; flex-direction: column; gap: 8px;
      text-decoration: none; color: inherit; transition: var(--t);
    }
    .latest-card:hover { box-shadow: var(--shadow-md); border-color: var(--color-primary-100); transform: translateY(-2px); }
    .latest-pill {
      font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
      color: var(--color-primary); background: var(--color-primary-50); border-radius: 100px;
      padding: 3px 10px; width: fit-content;
    }
    .latest-card h3 { font-size: 16px; font-weight: 700; line-height: 1.3; color: var(--color-text); margin: 0; }
    .latest-card p { font-size: 13px; line-height: 1.5; color: var(--color-text-secondary); margin: 0; flex: 1;
      display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .latest-meta {
      display: flex; align-items: center; gap: 8px; margin-top: auto; padding-top: 8px;
      border-top: 1px solid var(--color-border-light); font-size: 12px; color: var(--color-text-secondary);
    }
    .latest-photo { width: 24px; height: 24px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
    .latest-photo-fb {
      width: 24px; height: 24px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #A855F7);
      color: #fff; display: flex; align-items: center; justify-content: center;
      font-size: 9px; font-weight: 700; flex-shrink: 0;
    }

    /* ============= STICKY PILLAR NAV ============= */
    .pillar-nav { background: rgba(255,255,255,0.92); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--color-border-light); position: sticky; top: 72px; z-index: 90; padding: 14px 0; }
    .pillar-nav-inner { max-width: var(--container-max); margin: 0 auto; padding: 0 var(--page-px); display: flex; gap: 24px; overflow-x: auto; scrollbar-width: none; }
    .pillar-nav-inner::-webkit-scrollbar { display: none; }
    .pillar-anchor { font-size: 14px; font-weight: 500; color: var(--color-text-secondary); text-decoration: none !important; white-space: nowrap; padding: 6px 0; border-bottom: 2px solid transparent; transition: var(--t); }
    .pillar-anchor:hover { color: var(--color-text); }
    .pillar-anchor.active { color: var(--color-primary); border-bottom-color: var(--color-primary); }
    .pillar-anchor .count { color: var(--color-muted); font-family: var(--font-mono); font-size: 12px; font-weight: 400; margin-left: 4px; }

    /* ============= PILLAR SECTION ============= */
    .pillar-section { padding: 80px var(--page-px) 32px; max-width: var(--container-max); margin: 0 auto; scroll-margin-top: 160px; }
    .pillar-section + .pillar-section { border-top: 1px solid var(--color-border-light); }
    .pillar-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; gap: 32px; flex-wrap: wrap; }
    .pillar-kicker { font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--color-primary); margin-bottom: 10px; }
    .pillar-title { font-size: 36px; line-height: 1.1; letter-spacing: -0.02em; font-weight: 800; color: var(--color-text); margin: 0 0 8px; }
    .pillar-title em { font-family: var(--font-accent); font-style: italic; font-weight: 400; }
    .pillar-desc { font-size: 16px; color: var(--color-text-secondary); margin: 0; max-width: 580px; }

    .pillar-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
    .pillar-grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 18px; }
    .post-card { background: #fff; border-radius: var(--r); border: 1px solid var(--color-border-light); border-top: 4px solid var(--color-text); display: flex; flex-direction: column; transition: var(--t); overflow: hidden; }
    .post-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); text-decoration: none; border-color: var(--color-primary-100); }
    .post-card.pc-tactical { border-top-color: #6366F1; }
    .post-card.pc-howto { border-top-color: #A855F7; }
    .post-card.pc-pillar { border-top-color: #1A1A2E; }
    .post-card.pc-versus { border-top-color: #C026D3; }
    .post-card.pc-besttools { border-top-color: #4F46E5; }
    .post-card.pc-templates { border-top-color: #818CF8; }
    .post-card.pc-strategy { border-top-color: #2D1B69; }
    .post-card.pc-review { border-top-color: #C084FC; }
    .post-body { padding: 18px 20px 18px; flex: 1; display: flex; flex-direction: column; }
    .post-pill { display: inline-block; font-family: var(--font-mono); font-size: 9px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--color-text-secondary); margin-bottom: 10px; align-self: flex-start; }
    .post-title { font-size: 16px; line-height: 1.35; font-weight: 600; color: var(--color-text); margin: 0 0 8px; letter-spacing: -0.005em; }
    .pillar-grid-5 .post-title { font-size: 14px; }
    .post-excerpt { font-size: 13px; line-height: 1.5; color: var(--color-text-secondary); margin: 0 0 14px; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .pillar-grid-5 .post-excerpt { -webkit-line-clamp: 2; font-size: 12px; }

    /* ============= AUTHOR MINI (card footer) ============= */
    .author-mini { display: flex; align-items: center; gap: 8px; margin-top: auto; padding-top: 12px; }
    .author-mini__photo { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
    .author-mini__photo-fallback { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #A855F7); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; flex-shrink: 0; }
    .author-mini__text { display: flex; flex-direction: column; gap: 1px; }
    .author-mini__name { font-size: 13px; font-weight: 600; color: var(--color-text); line-height: 1.2; }
    .author-mini__date { font-size: 12px; color: var(--color-muted); line-height: 1.2; }

    .pillar-viewall { text-align: right; margin-top: 28px; }
    .pillar-viewall a { color: var(--color-primary); font-size: 14px; font-weight: 600; text-decoration: none; }
    .pillar-viewall a:hover { text-decoration: underline; }

    /* ============= FEATURED STRIP (pillar pages) ============= */
    .featured-strip { display: grid; grid-template-columns: 1.6fr 1fr 1fr; gap: 24px; max-width: var(--container-max); margin: 0 auto; padding: 32px var(--page-px) 80px; }
    .feat-card { background: #fff; border-radius: var(--r-lg); overflow: hidden; box-shadow: var(--shadow-md); display: flex; flex-direction: column; transition: var(--t); border: 1px solid var(--color-border-light); text-decoration: none; color: inherit; }
    .feat-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); text-decoration: none; }
    .feat-img { aspect-ratio: 16/9; background: var(--gradient-brand-soft); position: relative; overflow: hidden; }
    .feat-card.small .feat-img { aspect-ratio: 4/3; }
    .feat-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .feat-img-fallback { position: absolute; inset: 0; padding: 28px; display: flex; flex-direction: column; justify-content: space-between; align-items: stretch; color: #fff; background: var(--gradient-brand); overflow: hidden; }
    .feat-img-fallback::after { content: ''; position: absolute; top: -30%; right: -15%; width: 60%; height: 130%; background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 60%); pointer-events: none; }
    .feat-img-fallback .fb-pill { font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(255,255,255,0.85); position: relative; z-index: 1; }
    .feat-img-fallback .fb-title { font-family: var(--font-accent); font-style: italic; font-size: 32px; font-weight: 500; line-height: 1.1; letter-spacing: -0.015em; color: #fff; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; position: relative; z-index: 1; max-width: 95%; }
    .feat-card.small .feat-img-fallback { padding: 20px; }
    .feat-card.small .feat-img-fallback .fb-title { font-size: 22px; }
    .feat-img-fallback .fb-mono { position: absolute; bottom: 18px; right: 20px; font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.45); letter-spacing: 0.06em; z-index: 1; }
    .feat-body { padding: 24px 26px 22px; flex: 1; display: flex; flex-direction: column; }
    .feat-pill { display: inline-block; font-family: var(--font-mono); font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--color-primary); margin-bottom: 12px; align-self: flex-start; }
    .feat-title { font-size: 24px; line-height: 1.25; font-weight: 700; color: var(--color-text); margin-bottom: 10px; letter-spacing: -0.015em; }
    .feat-card.small .feat-title { font-size: 17px; }
    .feat-excerpt { font-size: 14px; line-height: 1.55; color: var(--color-text-secondary); margin-bottom: 18px; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .feat-card:not(.small) .feat-excerpt { -webkit-line-clamp: 3; }

    /* ============= VERSUS BAND (BOFU) ============= */
    .versus-band { max-width: var(--container-max); margin: 64px auto 0; padding: 0 var(--page-px); }
    .versus-card { background: linear-gradient(135deg, #1A1A2E 0%, #2D1B69 100%); color: #fff; border-radius: var(--r-xl); padding: 48px; position: relative; overflow: hidden; }
    .versus-card::before { content: ''; position: absolute; bottom: -100px; right: -100px; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(168,85,247,0.30) 0%, transparent 70%); pointer-events: none; }
    .versus-grid { position: relative; z-index: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; }
    .versus-left h3 { font-size: 32px; line-height: 1.15; margin: 0 0 14px; letter-spacing: -0.02em; font-weight: 800; }
    .versus-left h3 em { font-family: var(--font-accent); font-style: italic; font-weight: 400; }
    .versus-left p { color: rgba(255,255,255,0.75); font-size: 15px; margin: 0 0 24px; line-height: 1.6; }
    .versus-cta-row { display: flex; gap: 12px; flex-wrap: wrap; }
    .versus-cta-row .btn { background: #fff; color: var(--color-text); }
    .versus-cta-row .btn:hover { background: var(--color-primary-50); color: var(--color-primary); }
    .versus-cta-row .btn-secondary { background: transparent; color: #fff; border: 1.5px solid rgba(255,255,255,0.3); box-shadow: none; }
    .versus-cta-row .btn-secondary:hover { background: rgba(255,255,255,0.1); color: #fff; box-shadow: none; }
    .versus-right { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
    .versus-tile { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10); border-radius: var(--r); padding: 14px 12px; text-align: center; transition: var(--t); text-decoration: none !important; color: #fff; }
    .versus-tile:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.25); transform: translateY(-2px); color: #fff; }
    .versus-tile-name { font-size: 13px; font-weight: 700; margin-bottom: 2px; }
    .versus-tile-label { font-size: 10px; color: rgba(255,255,255,0.55); font-family: var(--font-mono); letter-spacing: 0.06em; text-transform: uppercase; }

    /* ============= NEWSLETTER ============= */
    .newsletter-band { max-width: var(--container-max); margin: 64px auto; padding: 0 var(--page-px); }
    .newsletter-card { background: var(--gradient-brand); color: #fff; border-radius: var(--r-xl); padding: 56px 48px; text-align: center; box-shadow: var(--shadow-glow); }
    .newsletter-card h3 { font-size: 32px; margin-bottom: 12px; font-weight: 800; letter-spacing: -0.02em; color: #fff; }
    .newsletter-card h3 em { font-family: var(--font-accent); font-style: italic; font-weight: 400; }
    .newsletter-card p { opacity: 0.92; margin-bottom: 28px; font-size: 16px; }
    .newsletter-card form { display: flex; gap: 10px; max-width: 480px; margin: 0 auto 14px; }
    .newsletter-card input { flex: 1; padding: 14px 18px; border-radius: var(--r); border: none; font-family: var(--font-sans); font-size: 14px; }
    .newsletter-card input:focus { outline: none; box-shadow: 0 0 0 3px rgba(255,255,255,0.4); }
    .newsletter-card button { background: var(--color-text); color: #fff; padding: 14px 28px; border-radius: var(--r); border: none; font-weight: 600; cursor: pointer; font-family: var(--font-sans); font-size: 14px; }
    .newsletter-card button:hover { background: #000; }
    .newsletter-privacy { font-size: 12px; opacity: 0.75; font-family: var(--font-mono); }

    /* ============= FOOTER ============= */
    .footer { background: var(--color-text); color: rgba(255,255,255,0.7); padding: 48px var(--page-px) 32px; margin-top: 0; }
    .footer-inner { max-width: var(--container-max); margin: 0 auto; }
    .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1fr; gap: 32px; margin-bottom: 32px; }
    .footer h4 { font-family: var(--font-mono); color: #fff; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 14px; }
    .footer a { font-size: 14px; color: rgba(255,255,255,0.7); line-height: 2; }
    .footer a:hover { color: #fff; text-decoration: none; }
    .footer-bottom { border-top: 1px solid #374151; padding-top: 24px; font-size: 13px; display: flex; justify-content: space-between; gap: 20px; }

    /* Language switcher */
    .lang-switcher { position: relative; }
    .lang-switcher-btn { display: flex; align-items: center; gap: 6px; background: none; border: 1px solid var(--color-border); border-radius: 100px; padding: 6px 12px; font-size: 13px; font-weight: 600; color: var(--color-text-secondary); cursor: pointer; font-family: var(--font-sans); }
    .lang-switcher-btn:hover { border-color: var(--color-primary); color: var(--color-primary); }
    .lang-dropdown { display: none; position: absolute; top: 100%; right: 0; margin-top: 8px; background: #fff; border: 1px solid var(--color-border); border-radius: var(--r); box-shadow: var(--shadow-lg); min-width: 160px; z-index: 1000; overflow: hidden; }
    .lang-dropdown.open { display: block; }
    .lang-dropdown a { display: block; padding: 10px 16px; font-size: 14px; color: var(--color-text); text-decoration: none; }
    .lang-dropdown a:hover { background: var(--color-surface); }
    .lang-dropdown a.active { font-weight: 700; color: var(--color-primary); }

    /* ============= RESPONSIVE ============= */
    @media (max-width: 1100px) {
      .pillar-grid-5 { grid-template-columns: repeat(3, 1fr); }
      .versus-grid { grid-template-columns: 1fr; gap: 32px; }
    }
    @media (max-width: 960px) {
      .featured-strip { grid-template-columns: 1fr; }
      .pillar-grid { grid-template-columns: repeat(2, 1fr); }
      .pillar-grid-5 { grid-template-columns: repeat(2, 1fr); }
      .experts-grid { grid-template-columns: 1fr; }
      .footer-grid { grid-template-columns: 1fr 1fr 1fr; }
      .versus-right { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 640px) {
      :root { --page-px: 16px; }
      .blog-hero { padding: 56px var(--page-px) 32px; }
      .blog-hero h1 { font-size: 36px; }
      .blog-hero .lead { font-size: 17px; }
      .pillar-grid, .pillar-grid-5 { grid-template-columns: 1fr; }
      .pillar-section { padding: 56px var(--page-px) 24px; }
      .pillar-title { font-size: 28px; }
      .newsletter-card, .versus-card { padding: 40px 24px; }
      .newsletter-card form { flex-direction: column; }
      .footer-grid { grid-template-columns: 1fr 1fr; }
    }
"""


def build_nav(locale: str, txt: dict, page: str = "hub") -> str:
    """Build navigation HTML with language switcher."""
    lang_code = txt["lang_code"]
    a_fr = 'class="active"' if locale == "fr" else ""
    a_de = 'class="active"' if locale == "de" else ""
    a_es = 'class="active"' if locale == "es" else ""
    a_it = 'class="active"' if locale == "it" else ""
    return f"""\
  <nav class="nav" aria-label="Main navigation">
    <a href="https://overloop.com" class="nav-logo">
      <img src="https://cdn.prod.website-files.com/6836b1fcfa0b25a3fed39db6/69d4cb02974de95cb4df5bd0_Logotype%20-%20Black.png" alt="Overloop">
    </a>
    <div class="nav-links">
      <a href="https://overloop.com/features">Features</a>
      <a href="https://overloop.com/pricing">Pricing</a>
      <a href="https://overloop.com/{locale}/blog/" class="active">Blog</a>
      <a href="https://overloop.com/tools">Free tools</a>
    </div>
    <div class="nav-right">
      <div class="lang-switcher">
        <button class="lang-switcher-btn" id="lang-toggle" aria-label="Switch language">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          {lang_code}
        </button>
        <div class="lang-dropdown" id="lang-dropdown">
          <a href="/blog/">&#127468;&#127463; English</a>
          <a href="/fr/blog/" {a_fr}>&#127467;&#127479; Fran&ccedil;ais</a>
          <a href="/de/blog/" {a_de}>&#127465;&#127466; Deutsch</a>
          <a href="/es/blog/" {a_es}>&#127466;&#127480; Espa&ntilde;ol</a>
          <a href="/it/blog/" {a_it}>&#127470;&#127481; Italiano</a>
        </div>
      </div>
      <a href="https://app.overloop.ai/session/login" class="nav-login">Login</a>
      <a href="https://app.overloop.ai/session/signup" class="btn btn-sm">Sign up free</a>
    </div>
  </nav>"""


def build_experts_band(txt: dict) -> str:
    return f"""\
  <section class="experts-band">
    <div class="experts-head">
      <div>
        <h2>{txt["experts_h2"]}</h2>
        <p>{txt["experts_p"]}</p>
      </div>
      <a href="https://overloop.com/about">{txt["experts_link"]}</a>
    </div>
    <div class="experts-grid">
      <div class="expert-card">
        <img class="expert-photo" src="https://cdn.prod.website-files.com/684167ac317862f3216bcd82/686cd1f2480e7dca3a497cbc_vincenzo.avif" alt="Vincenzo Ruggiero" width="56" height="56" loading="lazy" decoding="async" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"><div class="expert-photo-fallback" style="display:none;" aria-label="Vincenzo Ruggiero avatar">VR</div>
        <div class="expert-info">
          <strong>Vincenzo Ruggiero</strong>
          <span class="role">Head of AI Sales · 8 yrs</span>
          <p>Runs AI sales prospecting playbooks for B2B SaaS. Tested 100+ outbound tools across 30+ campaigns since 2018.</p>
        </div>
      </div>
      <div class="expert-card">
        <img class="expert-photo" src="https://overloop.com/assets/images/nicolas-finet.png" alt="Nicolas Finet" width="56" height="56" loading="lazy" decoding="async" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="expert-photo-fallback" style="display:none;" aria-label="Nicolas Finet avatar">NF</div>
        <div class="expert-info">
          <strong>Nicolas Finet</strong>
          <span class="role">Co-founder · 12 yrs</span>
          <p>Co-founded Sortlist (acquired Overloop 2024). Built outbound engines that closed 1,000+ B2B clients across Europe.</p>
        </div>
      </div>
      <div class="expert-card">
        <img class="expert-photo" src="https://cdn.prod.website-files.com/684167ac317862f3216bcd82/6878e35bb2fbe24081c32dec_nathalie.avif" alt="Nathalie Saikali" width="56" height="56" loading="lazy" decoding="async" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"><div class="expert-photo-fallback" style="display:none;" aria-label="Nathalie Saikali avatar">NS</div>
        <div class="expert-info">
          <strong>Nathalie Saikali</strong>
          <span class="role">Email Deliverability Lead · 6 yrs</span>
          <p>Specialist in email deliverability, GDPR compliance, and inbox placement. Manages sender reputation for 500+ domains.</p>
        </div>
      </div>
    </div>
  </section>"""


def build_versus_band(locale: str, txt: dict, has_locale_versus: bool) -> str:
    versus_url = f"/{locale}/versus/" if has_locale_versus else "/versus/"
    return f"""\
  <div class="versus-band">
    <section class="versus-card">
      <div class="versus-grid">
        <div class="versus-left">
          <div class="pillar-kicker" style="color:#A855F7; margin-bottom:12px;">{txt["versus_kicker"]}</div>
          <h3>{txt["versus_h3"]}</h3>
          <p>{txt["versus_p"]}</p>
          <div class="versus-cta-row">
            <a class="btn" href="{versus_url}">{txt["versus_cta1"]}</a>
            <a class="btn btn-secondary" href="https://app.overloop.ai/session/signup">{txt["versus_cta2"]}</a>
          </div>
        </div>
        <div class="versus-right">
          <a class="versus-tile" href="/blog/apollo-alternatives"><div class="versus-tile-name">Apollo</div><div class="versus-tile-label">Alternatives</div></a>
          <a class="versus-tile" href="/blog/lemlist-alternatives"><div class="versus-tile-name">Lemlist</div><div class="versus-tile-label">Alternatives</div></a>
          <a class="versus-tile" href="/blog/outreach-alternatives"><div class="versus-tile-name">Outreach</div><div class="versus-tile-label">Alternatives</div></a>
          <a class="versus-tile" href="/blog/salesloft-alternatives"><div class="versus-tile-name">Salesloft</div><div class="versus-tile-label">Alternatives</div></a>
          <a class="versus-tile" href="/blog/instantly-alternatives"><div class="versus-tile-name">Instantly</div><div class="versus-tile-label">Alternatives</div></a>
          <a class="versus-tile" href="/blog/la-growth-machine-review"><div class="versus-tile-name">La Growth M.</div><div class="versus-tile-label">Review</div></a>
          <a class="versus-tile" href="/blog/best-ai-sales-tools"><div class="versus-tile-name">AI Sales</div><div class="versus-tile-label">Best Tools</div></a>
          <a class="versus-tile" href="/blog/11-best-ai-bdr-tools"><div class="versus-tile-name">AI BDR</div><div class="versus-tile-label">Best Tools</div></a>
          <a class="versus-tile" href="/blog/best-lead-generation-tools"><div class="versus-tile-name">Lead Gen</div><div class="versus-tile-label">Best Tools</div></a>
        </div>
      </div>
    </section>
  </div>"""


def build_newsletter(txt: dict) -> str:
    return f"""\
  <div class="newsletter-band">
    <section class="newsletter-card">
      <h3>{txt["newsletter_h3"]}</h3>
      <p>{txt["newsletter_p"]}</p>
      <form action="https://overloop.com/api/newsletter/subscribe" method="POST">
        <input type="email" placeholder="{txt["newsletter_placeholder"]}" required>
        <button type="submit">{txt["newsletter_btn"]}</button>
      </form>
      <div class="newsletter-privacy">{txt["newsletter_privacy"]}</div>
    </section>
  </div>"""


def build_footer() -> str:
    return """\
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
          <a href="https://overloop.com/about#editorial-standards">Editorial standards</a><br>
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
  </footer>"""


def build_scripts() -> str:
    return """\
  <script>
    (function() {
      const links = document.querySelectorAll('.pillar-anchor');
      const sections = Array.from(links).map(a => {
        const id = a.getAttribute('href').slice(1);
        return { link: a, el: document.getElementById(id) };
      }).filter(s => s.el);
      function onScroll() {
        const y = window.scrollY + 200;
        let active = sections[0];
        for (const s of sections) if (s.el && s.el.offsetTop <= y) active = s;
        links.forEach(a => a.classList.remove('active'));
        if (active) active.link.classList.add('active');
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    })();
  </script>
  <script>
    document.getElementById('lang-toggle')?.addEventListener('click', function(e) {
      e.stopPropagation();
      document.getElementById('lang-dropdown').classList.toggle('open');
    });
    document.addEventListener('click', function() {
      document.getElementById('lang-dropdown')?.classList.remove('open');
    });
  </script>"""


def build_post_card(article: dict, locale: str, grid_class: str = "pillar-grid") -> str:
    """Build a post card HTML block."""
    card_type, pill_label = get_card_type(article["slug"], article["title"])
    desc = truncate(article["description"], 120)
    initials = get_initials(article["author"])
    date_str = format_date(article.get("date_modified") or article.get("date_published", ""))
    read_time = article.get("read_time", 7)
    date_display = f"{date_str} · {read_time} min" if date_str else f"{read_time} min"

    return f"""\
      <a class="post-card pc-{card_type}" href="/{locale}/blog/{article['slug']}">
        <div class="post-body">
          <div class="post-pill">{pill_label}</div>
          <h3 class="post-title">{article['title']}</h3>
          <p class="post-excerpt">{desc}</p>
          <div class="author-mini">
            <div class="author-mini__photo-fallback">{initials}</div>
            <div class="author-mini__text">
              <span class="author-mini__name">{article['author']}</span>
              <span class="author-mini__date">{date_display}</span>
            </div>
          </div>
        </div>
      </a>"""


def build_latest_card(article: dict, locale: str) -> str:
    """Build a latest-card for the 4-up latest section."""
    card_type, pill_label = get_card_type(article["slug"], article["title"])
    desc = truncate(article["description"], 100)
    initials = get_initials(article["author"])
    date_str = format_date(article.get("date_modified") or article.get("date_published", ""))
    date_display = f"{article['author']} · {date_str}" if date_str else article["author"]

    return f"""\
      <a class="latest-card" href="/{locale}/blog/{article['slug']}">
        <div class="latest-pill">{pill_label}</div>
        <h3>{article['title']}</h3>
        <p>{desc}</p>
        <div class="latest-meta">
          <div class="latest-photo-fb">{initials}</div>
          <span>{date_display}</span>
        </div>
      </a>"""


def sort_by_date(articles: list) -> list:
    """Sort articles by dateModified desc, then datePublished desc."""
    def sort_key(a):
        d = a.get("date_modified") or a.get("date_published") or "1900-01-01"
        return d
    return sorted(articles, key=sort_key, reverse=True)


def parse_date_for_sort(a: dict) -> str:
    return a.get("date_modified") or a.get("date_published") or "1900-01-01"


# ─────────────────────────────────────────────────────────────────────────────
# HUB PAGE GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_hub(locale: str, articles: list, pillars: dict, txt: dict,
                 has_locale_versus: bool, dry_run: bool) -> None:
    total = len(articles)
    lang_attr = txt["lang_attr"]

    # hreflang block
    hreflang = """\
  <link rel="alternate" hreflang="en" href="https://overloop.com/blog">
  <link rel="alternate" hreflang="fr" href="https://overloop.com/fr/blog">
  <link rel="alternate" hreflang="de" href="https://overloop.com/de/blog">
  <link rel="alternate" hreflang="es" href="https://overloop.com/es/blog">
  <link rel="alternate" hreflang="it" href="https://overloop.com/it/blog">
  <link rel="alternate" hreflang="x-default" href="https://overloop.com/blog">"""

    # Latest: 4 most recent
    sorted_all = sort_by_date(articles)
    latest_4 = sorted_all[:4]
    latest_html = "\n".join(build_latest_card(a, locale) for a in latest_4)

    # Pillar nav
    nav_items = []
    for pillar_id in PILLARS_ORDER:
        count = len(pillars.get(pillar_id, []))
        name = txt["pillar_names"][pillar_id][0]
        nav_items.append(
            f'      <a class="pillar-anchor" href="#{pillar_id}">{name} <span class="count">({count})</span></a>'
        )
    # Versus link
    versus_url = f"/{locale}/versus/" if has_locale_versus else "/versus/"
    nav_items.append(f'      <a class="pillar-anchor" href="{versus_url}">Versus</a>')
    nav_items.append(f'      <a class="pillar-anchor" href="#all-articles">All ({total})</a>')
    pillar_nav_html = "\n".join(nav_items)

    # Pillar sections
    pillar_sections_html = ""
    for i, pillar_id in enumerate(PILLARS_ORDER, start=1):
        pname, pdesc = txt["pillar_names"][pillar_id]
        pnum = PILLAR_NUMBERS[pillar_id]
        pillar_articles = pillars.get(pillar_id, [])
        count = len(pillar_articles)
        top6 = pillar_articles[:6]

        # Use 5-column grid for linkedin (usually small set), 3-col for others
        grid_class = "pillar-grid-5" if pillar_id == "linkedin" else "pillar-grid"

        cards_html = "\n".join(build_post_card(a, locale, grid_class) for a in top6)

        view_all_text = f"{txt['viewall_prefix']} {count} {txt['viewall_suffix']}"
        viewall_html = f'\n    <div class="pillar-viewall"><a href="/{locale}/blog/{pillar_id}/">{view_all_text} &rarr;</a></div>' if count > 0 else ""

        pillar_sections_html += f"""
  <!-- ============= PILLAR {pnum} — {pname} ============= -->
  <section class="pillar-section" id="{pillar_id}">
    <div class="pillar-header">
      <div>
        <div class="pillar-kicker">Pillar {pnum}</div>
        <h2 class="pillar-title"><em>{pname}.</em></h2>
        <p class="pillar-desc">{pdesc}</p>
      </div>
      <a class="btn btn-ghost" href="https://overloop.com">Discover Overloop &rarr;</a>
    </div>
    <div class="{grid_class}">
{cards_html}
    </div>{viewall_html}
  </section>
"""

    # All articles index (flat list by pillar)
    all_index_html = ""
    for pillar_id in PILLARS_ORDER:
        pname = txt["pillar_names"][pillar_id][0]
        pillar_articles = pillars.get(pillar_id, [])
        if not pillar_articles:
            continue
        items = "\n".join(
            f'          <li><a href="/{locale}/blog/{a["slug"]}">{a["title"]}</a></li>'
            for a in sort_by_date(pillar_articles)
        )
        all_index_html += f"""\
      <div>
        <h4>{pname}</h4>
        <ul>
{items}
        </ul>
      </div>
"""

    # JSON-LD
    item_list = []
    for idx, a in enumerate(sorted_all, start=1):
        canonical = a.get("canonical") or f"https://overloop.com/{locale}/blog/{a['slug']}"
        item_list.append(
            f'      {{"@type": "ListItem", "position": {idx}, "name": {json.dumps(a["title"])}, "url": {json.dumps(canonical)}}}'
        )
    item_list_str = ",\n".join(item_list)

    json_ld = f"""\
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "Overloop Blog",
    "description": "{txt['meta_desc']}",
    "url": "https://overloop.com/{locale}/blog",
    "publisher": {{"@type": "Organization", "name": "Overloop", "url": "https://overloop.com"}},
    "inLanguage": "{lang_attr}"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://overloop.com"}},
      {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://overloop.com/{locale}/blog"}}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Overloop Blog — {txt['lang_code']}",
    "numberOfItems": {total},
    "itemListElement": [
{item_list_str}
    ]
  }}
  </script>"""

    html = f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{txt['meta_title']}</title>
  <meta name="description" content="{txt['meta_desc']}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://overloop.com/{locale}/blog">

{hreflang}

  <meta property="og:title" content="{txt['meta_title']}">
  <meta property="og:description" content="{txt['meta_desc']}">
  <meta property="og:image" content="https://overloop.com/assets/images/og/blog-hub.png">
  <meta property="og:url" content="https://overloop.com/{locale}/blog">
  <meta property="og:type" content="website">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <noscript><link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet"></noscript>
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet" media="print" onload="this.media='all'">

  <style>
{SHARED_STYLE}
  </style>
</head>
<body>

{build_nav(locale, txt)}

  <!-- ============= HERO ============= -->
  <header class="blog-hero">
    <div class="blog-hero-inner">
      <div class="breadcrumb"><a href="https://overloop.com">Home</a> &nbsp;›&nbsp; {txt['breadcrumb_blog']}</div>
      <h1>{txt['hero_h1']}</h1>
      <p class="lead">{txt['hero_lead']}</p>
      <div class="trust-line">
        <span class="dot"></span>
        <span><strong>{total} {txt['trust_articles']}</strong></span>
        <span>{txt['trust_tested']}</span>
        <span>{txt['trust_no_paid']}</span>
        <span>{txt['trust_reviewed']}</span>
      </div>
    </div>
  </header>

  <!-- ============= LATEST ARTICLES ============= -->
  <section class="latest-section">
    <div class="latest-head">
      <h2>{txt['latest_h2']}</h2>
      <p>{txt['latest_desc']}</p>
    </div>
    <div class="latest-grid">
{latest_html}
    </div>
  </section>

  <!-- ============= STICKY PILLAR NAV ============= -->
  <nav class="pillar-nav" aria-label="Blog pillar sections">
    <div class="pillar-nav-inner">
{pillar_nav_html}
    </div>
  </nav>

{pillar_sections_html}

{build_experts_band(txt)}

{build_versus_band(locale, txt, has_locale_versus)}

{build_newsletter(txt)}

  <!-- ============= ALL ARTICLES ============= -->
  <section style="background:#fff; padding:80px 0; margin-top:64px; border-top:1px solid var(--color-border-light);" id="all-articles">
    <div style="max-width:var(--container-max); margin:0 auto; padding:0 var(--page-px);">
      <h2 style="font-size:36px; letter-spacing:-0.02em; margin:0 0 8px; font-weight:800; color:var(--color-text);">
        All <em style="font-family:var(--font-accent);font-style:italic;font-weight:400;">{total} {txt['trust_articles']}</em>
      </h2>
      <p style="color:var(--color-text-secondary); margin:0 0 40px; font-size:16px;">{txt['latest_desc']}</p>
      <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:40px 56px;">
{all_index_html}
      </div>
    </div>
  </section>

{build_footer()}

{json_ld}

{build_scripts()}

</body>
</html>
"""

    out_path = BLOG_DIR / locale / "index.html"
    if dry_run:
        print(f"  [DRY-RUN] Would write {out_path} ({len(html)} chars)")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  Written: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# PILLAR PAGE GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_pillar_page(locale: str, pillar_id: str, articles: list,
                         all_pillars: dict, txt: dict, dry_run: bool) -> None:
    if not articles:
        print(f"  [SKIP] No articles for {locale}/{pillar_id}")
        return

    lang_attr = txt["lang_attr"]
    pnum = PILLAR_NUMBERS[pillar_id]
    pname, pdesc = txt["pillar_names"][pillar_id]
    sorted_articles = sort_by_date(articles)
    total = len(sorted_articles)

    # Featured strip: top 3
    featured = sorted_articles[:3]
    rest = sorted_articles[3:]

    def feat_card(a, is_small=False):
        card_type, pill_label = get_card_type(a["slug"], a["title"])
        initials = get_initials(a["author"])
        date_str = format_date(a.get("date_modified") or a.get("date_published", ""))
        read_time = a.get("read_time", 7)
        date_upper = f"UPDATED {date_str.upper()} · {read_time} MIN" if date_str else f"{read_time} MIN"
        small_cls = " small" if is_small else ""
        return f"""\
    <a class="feat-card{small_cls}" href="/{locale}/blog/{a['slug']}">
      <div class="feat-img">
        <div class="feat-img-fallback">
          <div class="fb-pill">{pill_label}</div>
          <div class="fb-title">{a['title']}</div>
          <div class="fb-mono">OL</div>
        </div>
      </div>
      <div class="feat-body">
        <span class="feat-pill">{pill_label}</span>
        <h2 class="feat-title">{a['title']}</h2>
        <p class="feat-excerpt">{truncate(a['description'], 150)}</p>
        <div class="author-mini">
          <div class="author-mini__photo-fallback">{initials}</div>
          <div class="author-mini__text">
            <span class="author-mini__name">{a['author']}</span>
            <span class="author-mini__date">{date_upper}</span>
          </div>
        </div>
      </div>
    </a>"""

    featured_html = ""
    for idx, fa in enumerate(featured):
        featured_html += feat_card(fa, is_small=(idx > 0)) + "\n"

    # All articles grid
    all_cards_html = "\n".join(build_post_card(a, locale) for a in sorted_articles)

    # Cross-links to other pillars
    other_pillars_html = ""
    for other_id in PILLARS_ORDER:
        if other_id == pillar_id:
            continue
        other_count = len(all_pillars.get(other_id, []))
        if other_count == 0:
            continue
        other_name = txt["pillar_names"][other_id][0]
        other_desc = txt["pillar_names"][other_id][1]
        other_num = PILLAR_NUMBERS[other_id]
        other_pillars_html += f"""\
      <a class="post-card pc-tactical" href="/{locale}/blog/{other_id}/" style="text-decoration:none;">
        <div class="post-body">
          <div class="post-pill">Pillar {other_num}</div>
          <h3 class="post-title">{other_name}</h3>
          <p class="post-excerpt">{other_desc}</p>
          <div style="font-size:13px; color:var(--color-primary); font-weight:600; margin-top:auto; padding-top:12px;">{other_count} articles &rarr;</div>
        </div>
      </a>
"""

    # JSON-LD for pillar page
    item_list = []
    for idx, a in enumerate(sorted_articles, start=1):
        canonical = a.get("canonical") or f"https://overloop.com/{locale}/blog/{a['slug']}"
        item_list.append(
            f'      {{"@type": "ListItem", "position": {idx}, "name": {json.dumps(a["title"])}, "url": {json.dumps(canonical)}}}'
        )
    item_list_str = ",\n".join(item_list)

    json_ld = f"""\
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "{pname} — Overloop Blog",
    "description": "{pdesc}",
    "url": "https://overloop.com/{locale}/blog/{pillar_id}/",
    "inLanguage": "{lang_attr}",
    "publisher": {{"@type": "Organization", "name": "Overloop", "url": "https://overloop.com"}}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://overloop.com"}},
      {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://overloop.com/{locale}/blog"}},
      {{"@type": "ListItem", "position": 3, "name": "{pname}", "item": "https://overloop.com/{locale}/blog/{pillar_id}/"}}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "{pname}",
    "numberOfItems": {total},
    "itemListElement": [
{item_list_str}
    ]
  }}
  </script>"""

    html = f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{pname} — Overloop Blog</title>
  <meta name="description" content="{pdesc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://overloop.com/{locale}/blog/{pillar_id}/">

  <meta property="og:title" content="{pname} — Overloop Blog">
  <meta property="og:description" content="{pdesc}">
  <meta property="og:image" content="https://overloop.com/assets/images/og/blog-{pillar_id}.png">
  <meta property="og:url" content="https://overloop.com/{locale}/blog/{pillar_id}/">
  <meta property="og:type" content="website">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <noscript><link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet"></noscript>
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet" media="print" onload="this.media='all'">

  <style>
{SHARED_STYLE}
  </style>
</head>
<body>

{build_nav(locale, txt)}

  <!-- ============= HERO ============= -->
  <header class="blog-hero">
    <div class="blog-hero-inner">
      <div class="breadcrumb">
        <a href="https://overloop.com">Home</a> &nbsp;›&nbsp;
        <a href="/{locale}/blog/">{txt['breadcrumb_blog']}</a> &nbsp;›&nbsp;
        {pname}
      </div>
      <div style="font-family:var(--font-mono);font-size:11px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--color-primary);margin-bottom:14px;">Pillar {pnum}</div>
      <h1><em>{pname}</em></h1>
      <p class="lead">{pdesc}</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
        <a class="btn" href="https://overloop.com">{txt['pillar_discover']}</a>
        <span class="trust-line"><span class="dot"></span><span><strong>{total} {txt['trust_articles']}</strong></span><span>{txt['trust_reviewed']}</span></span>
      </div>
    </div>
  </header>

  <!-- ============= FEATURED STRIP ============= -->
  <section class="featured-strip">
{featured_html}
  </section>

  <!-- ============= ALL ARTICLES ============= -->
  <section class="pillar-section" id="all-pillar-articles" style="border-top:1px solid var(--color-border-light);padding-top:56px;">
    <div class="pillar-header">
      <div>
        <div class="pillar-kicker">{txt['pillar_page_all']}</div>
        <h2 class="pillar-title"><em>{txt['pillar_page_browse']} — {pname}.</em></h2>
        <p class="pillar-desc">{total} {txt['trust_articles']}.</p>
      </div>
    </div>
    <div class="pillar-grid">
{all_cards_html}
    </div>
  </section>

  <!-- ============= CROSS-LINKS TO OTHER PILLARS ============= -->
  <section class="pillar-section" style="border-top:1px solid var(--color-border-light);">
    <div class="pillar-header">
      <div>
        <div class="pillar-kicker">Explorer</div>
        <h2 class="pillar-title"><em>Other pillars.</em></h2>
      </div>
    </div>
    <div class="pillar-grid">
{other_pillars_html}
    </div>
  </section>

{build_experts_band(txt)}

{build_versus_band(locale, txt, has_locale_versus=(VERSUS_DIR / locale).exists())}

{build_newsletter(txt)}

{build_footer()}

{json_ld}

{build_scripts()}

</body>
</html>
"""

    out_path = BLOG_DIR / locale / pillar_id / "index.html"
    if dry_run:
        print(f"  [DRY-RUN] Would write {out_path} ({len(html)} chars)")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  Written: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def process_locale(locale: str, dry_run: bool) -> None:
    print(f"\n{'='*60}")
    print(f"  Processing locale: {locale.upper()}")
    print(f"{'='*60}")

    locale_dir = BLOG_DIR / locale
    if not locale_dir.exists():
        print(f"  [ERROR] Directory not found: {locale_dir}")
        return

    txt = LOCALE_TEXT[locale]
    has_locale_versus = (VERSUS_DIR / locale).exists()

    # Scan articles
    html_files = sorted(locale_dir.glob("*.html"))
    if not html_files:
        print(f"  [WARN] No HTML files found in {locale_dir}")
        return

    print(f"  Found {len(html_files)} HTML files — extracting metadata...")
    articles = []
    for f in html_files:
        meta = extract_article_meta(f)
        if meta:
            articles.append(meta)
        else:
            print(f"  [SKIP] {f.name}")

    print(f"  Extracted metadata for {len(articles)} articles")

    # Assign pillars
    pillars: dict[str, list] = {p: [] for p in PILLARS_ORDER}
    for a in articles:
        p = assign_pillar(a["slug"], a["title"])
        pillars[p].append(a)

    # Sort each pillar by date descending
    for p in pillars:
        pillars[p] = sort_by_date(pillars[p])

    print("  Pillar distribution:")
    for p in PILLARS_ORDER:
        print(f"    {p}: {len(pillars[p])} articles")

    # Generate hub
    print(f"\n  Generating hub: blog/{locale}/index.html")
    generate_hub(locale, articles, pillars, txt, has_locale_versus, dry_run)

    # Generate pillar pages
    for pillar_id in PILLARS_ORDER:
        print(f"  Generating pillar: blog/{locale}/{pillar_id}/index.html")
        generate_pillar_page(locale, pillar_id, pillars[pillar_id],
                             pillars, txt, dry_run)

    print(f"\n  Done: {locale.upper()} — hub + 5 pillar pages")


def main():
    parser = argparse.ArgumentParser(
        description="Generate locale blog hub + pillar pages for Overloop Blog"
    )
    parser.add_argument(
        "--locale", choices=LOCALES, default=None,
        help="Generate for a single locale only (fr/de/es/it)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview output paths without writing files"
    )
    args = parser.parse_args()

    print("Overloop Locale Hub Generator")
    print(f"Blog directory: {BLOG_DIR}")
    if args.dry_run:
        print("[DRY-RUN MODE — no files will be written]")

    target_locales = [args.locale] if args.locale else LOCALES
    for locale in target_locales:
        process_locale(locale, args.dry_run)

    print("\nAll done.")


if __name__ == "__main__":
    main()
