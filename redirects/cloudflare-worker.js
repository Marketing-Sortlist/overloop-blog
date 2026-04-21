/**
 * Overloop Blog Migration — Cloudflare Worker
 * Generated: 2026-04-15
 *
 * Handles:
 * 1. 301 redirects for killed/consolidated blog pages (98 EN URLs)
 * 2. 301 redirects for VS pages: /blog/* → /versus/* (10 URLs)
 * 3. 301 redirects for international pages: specific locale → EN targets (646 URLs)
 * 4. 301 redirects from tools.overloop.com → overloop.com/tools/
 * 5. Query parameter stripping (?origin=prospectio)
 * 6. Reverse proxy: /blog/*, /versus/*, /tools/*, /playbooks/* → GitHub Pages
 */

// ──────────────────────────────────────────────
// EN BLOG REDIRECT RULES — 98 total
// ──────────────────────────────────────────────

const BLOG_REDIRECTS = {
  // === VS Pages: /blog/* → /versus/* (10) ===
  '/blog/apollo-vs-lemlist-which-prospecting-tool-wins-for-b2b-sales-teams-95e78': '/versus/apollo-vs-lemlist',
  '/blog/instantly-vs-lemlist': '/versus/instantly-vs-lemlist',
  '/blog/lemlist-vs-apollo': '/versus/lemlist-vs-apollo',
  '/blog/overloop-vs-apollo': '/versus/overloop-vs-apollo',
  '/blog/overloop-vs-artisan': '/versus/overloop-vs-artisan',
  '/blog/overloop-vs-hubspot': '/versus/overloop-vs-hubspot',
  '/blog/overloop-vs-instantly': '/versus/overloop-vs-instantly',
  '/blog/overloop-vs-lemlist': '/versus/overloop-vs-lemlist',
  '/blog/overloop-vs-reply': '/versus/overloop-vs-reply',
  '/blog/overloop-vs-saleshandy': '/versus/overloop-vs-saleshandy',
  '/versus/apollo-vs-lemlist': '/versus/lemlist-vs-apollo',

  // === Consolidations: redirect to stronger article (26) ===
  '/blog/10-essential-b2b-prospect-sourcing-tools-for-2025-a-checklist-for-success': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/blog/5-deadly-email-prospecting-mistakes': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/blog/6-cold-email-rules': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/blog/7-cold-email-subject-lines': '/blog/500-trigger-words',
  '/blog/9-best-ai-sales-workflow-tools': '/blog/best-ai-sales-tools',
  '/blog/Heyreach-Review': '/blog/8-best-ai-linkedin-outreach-tools',
  '/blog/ai-email-writer-revolution-how-to-use-ai-for-cold-outreach-in-outbound-sales': '/blog/9-best-ai-email-outreach-tools',
  // '/blog/best-ai-sales-tools' — REMOVED: page exists, was self-redirect loop
  '/blog/best-cold-email-software': '/blog/9-best-ai-email-outreach-tools',
  '/blog/cold-email-campaigns-reply-rates': '/blog/increase-reply-rate',
  '/blog/cold-email-software': '/blog/9-best-ai-email-outreach-tools',
  '/blog/ethics-of-ai-in-sales-key-challenges': '/blog/best-ai-sales-tools',
  '/blog/find-and-verify-emails-within-the-app': '/blog/how-to-find-someone-email-address-efficiently',
  '/blog/find-emails-with-name-organization-domain': '/blog/how-to-find-someone-email-address-efficiently',
  '/blog/how-ai-email-writer-technology-transforms-cold-outreach-a-case-study-on-overloop': '/blog/9-best-ai-email-outreach-tools',
  '/blog/how-an-ai-sales-tool-transformed-b2b-sales-teams-case-study-and-ai-sales-tool-reviews-2025': '/blog/best-ai-sales-tools',
  '/blog/how-to-master-sales-prospecting-with-overloop-s-automation-tools': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/blog/how-to-write-good-emails': '/blog/whats-the-best-email-length-for-sales-outreach',
  '/blog/linkedin-outreach': '/blog/8-best-ai-linkedin-outreach-tools',
  '/blog/main-sales-objections': '/blog/deal-objections',
  '/blog/the-ultimate-guide-to-b2b-sales-automation-solutions-in-2025': '/blog/best-ai-sales-tools',
  '/blog/the-ultimate-guide-to-email-outreach-automation-for-b2b-sales-teams': '/blog/9-best-ai-email-outreach-tools',
  '/blog/the-ultimate-guide-to-sales-leads-generation-for-b2b-teams-automation-strategies-and-tools': '/blog/best-ai-sales-tools',
  '/blog/top-ai-sdr-strategies-to-boost-your-b2b-sales-in-2025': '/blog/11-best-ai-bdr-tools',
  '/blog/ultimate-cold-email-checklist': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/blog/write-cold-email-make-hot': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',

  // === Killed: redirect to /blog index (62) ===
  '/blog/11-sales-influencers-crush-competition': '/blog',
  '/blog/3-essential-qualities-sdr': '/blog',
  '/blog/3-sales-kpi': '/blog',
  '/blog/5-reasons-deleted-cold-email': '/blog',
  '/blog/7-bad-habits-salespeople': '/blog',
  '/blog/7-sales-tips': '/blog',
  '/blog/8-key-events-for-overloop-in-2020': '/blog',
  '/blog/ab-testing-case-study': '/blog',
  '/blog/ai-sales-tools-scalability-vs-customization': '/blog',
  '/blog/attachments': '/blog',
  '/blog/attract-hire-lead-talent': '/blog',
  '/blog/b2b-lead-generation-manual-vs-ai-powered-methods': '/blog',
  '/blog/calendly-integration': '/blog',
  '/blog/deals-pipelines': '/blog',
  '/blog/document-automate-sales-process': '/blog',
  '/blog/emailing-important-people': '/blog',
  '/blog/essential-mastering-social-selling': '/blog',
  '/blog/get-started-startup-sales': '/blog',
  '/blog/how-ai-improves-follow-up-scheduling-in-sales': '/blog',
  '/blog/how-ai-improves-multi-channel-campaign-scalability': '/blog',
  '/blog/how-ai-improves-real-time-data-sync-for-sales-teams': '/blog',
  '/blog/how-ai-improves-sales-roi-over-time': '/blog',
  '/blog/how-long-build-sales-process': '/blog',
  '/blog/how-to-automate-sales-leads-list-management-for-small-businesses-the-ultimate-guide': '/blog',
  '/blog/how-to-scale-b2b-sales-with-ai-platforms': '/blog',
  '/blog/how-to-use-an-ai-sales-assistant-the-b2b-sales-team-s-step-by-step-guide': '/blog',
  '/blog/how-to-use-sales-software-for-b2b-lead-generation-and-tracking-a-step-by-step-guide-for-startups': '/blog',
  '/blog/increase-your-saas-sales-during-holiday-season': '/blog',
  '/blog/lead-generation-hire': '/blog',
  '/blog/lists-improvements': '/blog',
  '/blog/manage-sales-pipeline': '/blog/pre-call-planning',
  '/blog/manage-team-hit-sales-target': '/blog',
  '/blog/multiple-events': '/blog',
  '/blog/new-dashboard': '/blog',
  '/blog/new-integration-settings': '/blog',
  '/blog/not-doing-social-selling-youre-wrong': '/blog',
  '/blog/overloop-ai-the-future-of-sales': '/blog',
  '/blog/overloop-reshapes-outbound-workflows-with-a-simpler-more-flexible-platform-update': '/blog',
  '/blog/quick-guide-lead-generation-for-2019': '/blog',
  '/blog/real-time-data-sync-how-it-boosts-multi-channel-campaigns': '/blog',
  '/blog/reports-v2': '/blog',
  '/blog/revolutionize-b2b-sales-how-to-automate-multi-channel-follow-ups-with-an-ai-email-assistant': '/blog',
  '/blog/sales-automation-account-based-selling': '/blog',
  '/blog/sales-lessons-fbi-hostage-negotiator': '/blog',
  '/blog/sales-prospecting-guide-from-cold-leads-to-meetings': '/blog',
  '/blog/sales-skills': '/blog',
  '/blog/sales-strategies-analyse-the-prospects-that-turn-you-down': '/blog',
  '/blog/salesforce-2-way-sync': '/blog',
  '/blog/startup-founders-mistake-sales': '/blog',
  '/blog/store': '/blog',
  '/blog/team-retreat-important': '/blog',
  '/blog/the-3-most-common-mistakes-when-it-comes-to-outreach-emailing': '/blog',
  '/blog/the-guide-to-incorporating-video-into-your-sales-strategy': '/blog',
  '/blog/the-sate-of-field-sales-infographic': '/blog',
  '/blog/the-ultimate-guide-to-choosing-a-sales-platform-for-outbound-lead-generation': '/blog',
  '/blog/the-ultimate-guide-to-outbound-sales-strategies-software-and-success-for-b2b-companies': '/blog',
  '/blog/the-ultimate-guide-to-sales-platform-features-and-benefits-for-outbound-lead-generation': '/blog',
  '/blog/the-ultimate-guide-to-sales-tools-for-modern-b2b-teams-in-2025': '/blog',
  '/blog/unique-selling-proposition': '/blog',
  '/blog/unsubscribe-link': '/blog',
  '/blog/web-application-re-design': '/blog',
  '/blog/why-are-we-starting-this-blog': '/blog',
};

// ──────────────────────────────────────────────
// INTL BLOG REDIRECT RULES — 646 total
// Specific locale → EN target (replaces pattern catch-all)
// ──────────────────────────────────────────────

const INTL_REDIRECTS = {
  // === /FR (166 rules) ===
  '/fr/blog/ameliorations-listes': '/blog',
  '/fr/blog/apollo-vs-lemlist-comparatif-prospection': '/versus/apollo-vs-lemlist',
  '/fr/blog/assistant-commercial-ia-guide-b2b': '/blog',
  '/fr/blog/attirer-recruter-talents-commerciaux': '/blog',
  '/fr/blog/automatisation-vente-account-based-selling': '/blog',
  '/fr/blog/automatisation-ventes-b2b': '/blog/best-ai-sales-tools',
  '/fr/blog/automatiser-gestion-listes-prospects-pme': '/blog',
  '/fr/blog/boutique': '/blog',
  '/fr/blog/campagnes-cold-email-taux-reponse': '/blog/increase-reply-rate',
  '/fr/blog/checklist-email-froid': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/fr/blog/cles-succes-vente': '/blog/5-rules-more-successful-salespeople',
  '/fr/blog/conseils-commerciaux-debutants': '/blog',
  '/fr/blog/conseils-prospection-commerciale-pipeline': '/blog/10-proven-sales-prospecting-tips-to-boost-your-pipeline-fast',
  '/fr/blog/construire-processus-vente': '/blog',
  '/fr/blog/copywriting-cold-email-conseils': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/fr/blog/demarrer-ventes-fondateur-startup': '/blog',
  '/fr/blog/developper-ventes-b2b-ia': '/blog',
  '/fr/blog/documenter-processus-vente-automatisation': '/blog/common-sales-automation-mistakes-and-how-to-avoid-them',
  '/fr/blog/email-personnes-influentes-conseils': '/blog',
  '/fr/blog/erreurs-outreach-email': '/blog',
  '/fr/blog/erreurs-prospection-email-eviter': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/fr/blog/erreurs-ventes-fondateurs-startup': '/blog',
  '/fr/blog/etapes-essentielles-maitriser-social-selling': '/blog',
  '/fr/blog/etat-ventes-terrain': '/blog',
  '/fr/blog/ethique-ia-ventes': '/blog/best-ai-sales-tools',
  '/fr/blog/evenements-cles-overloop': '/blog',
  '/fr/blog/generation-leads-b2b-manuel-vs-ia': '/blog',
  '/fr/blog/generation-leads-vente-b2b': '/blog/best-ai-sales-tools',
  '/fr/blog/gerer-deals-pipeline-crm': '/blog',
  '/fr/blog/gerer-pipeline-ventes': '/blog/pre-call-planning',
  '/fr/blog/heyreach-avis': '/blog/8-best-ai-linkedin-outreach-tools',
  '/fr/blog/ia-ameliore-roi-ventes': '/blog',
  '/fr/blog/ia-campagnes-multicanal-scalabilite': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/fr/blog/ia-planification-suivi-ventes': '/blog',
  '/fr/blog/ia-redacteur-emails-cold-outreach-ventes': '/blog/9-best-ai-email-outreach-tools',
  '/fr/blog/ia-redaction-emails-cold-outreach': '/blog/9-best-ai-email-outreach-tools',
  '/fr/blog/ia-synchronisation-donnees-ventes': '/blog',
  '/fr/blog/importance-seminaire-equipe': '/blog',
  '/fr/blog/indicateurs-cles-performance-vente': '/blog',
  '/fr/blog/influenceurs-vente-strategies-gagnantes': '/blog',
  '/fr/blog/instantly-vs-lemlist': '/versus/instantly-vs-lemlist',
  '/fr/blog/integration-calendly': '/blog',
  '/fr/blog/lancement-blog': '/blog',
  '/fr/blog/lead-generation-hire': '/blog',
  '/fr/blog/lecons-vente-negociation-fbi': '/blog',
  '/fr/blog/lemlist-vs-apollo': '/versus/lemlist-vs-apollo',
  '/fr/blog/lien-desabonnement': '/blog',
  '/fr/blog/lignes-objet-cold-email-performantes': '/blog/500-trigger-words',
  '/fr/blog/logiciel-vente-generation-leads-b2b': '/blog',
  '/fr/blog/maitriser-prospection-commerciale-automatisation': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/fr/blog/mauvaises-habitudes-vendeurs': '/blog',
  '/fr/blog/meilleurs-outils-workflow-ventes-ia': '/blog/best-ai-sales-tools',
  '/fr/blog/multiple-events': '/blog',
  '/fr/blog/nouveau-tableau-de-bord': '/blog',
  '/fr/blog/nouveaux-parametres-integration': '/blog',
  '/fr/blog/objections-acheteurs': '/blog/deal-objections',
  '/fr/blog/outil-ia-ventes-b2b-etude-cas': '/blog/best-ai-sales-tools',
  '/fr/blog/outils-ia-ventes-scalabilite-vs-personnalisation': '/blog/best-ai-sales-tools',
  '/fr/blog/outils-sourcing-prospects-b2b-essentiels': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/fr/blog/outils-vente-b2b': '/blog',
  '/fr/blog/overloop-ai-avenir-ventes': '/blog/best-ai-sales-tools',
  '/fr/blog/overloop-ou-saleshandy': '/versus/overloop-vs-saleshandy',
  '/fr/blog/overloop-vs-apollo': '/versus/overloop-vs-apollo',
  '/fr/blog/overloop-vs-artisan': '/versus/overloop-vs-artisan',
  '/fr/blog/overloop-vs-hubspot': '/versus/overloop-vs-hubspot',
  '/fr/blog/overloop-vs-instantly': '/versus/overloop-vs-instantly',
  '/fr/blog/overloop-vs-lemlist': '/versus/overloop-vs-lemlist',
  '/fr/blog/overloop-vs-reply': '/versus/overloop-vs-reply',
  '/fr/blog/pieces-jointes-emails': '/blog',
  '/fr/blog/plateforme-vente-prospection': '/blog',
  '/fr/blog/proposition-vente-unique-usp': '/blog',
  '/fr/blog/prospection-linkedin-obtenir-reponses': '/blog/8-best-ai-linkedin-outreach-tools',
  '/fr/blog/qualites-essentielles-sdr-commercial': '/blog',
  '/fr/blog/rapports-v2': '/blog',
  '/fr/blog/rediger-bons-emails': '/blog/whats-the-best-email-length-for-sales-outreach',
  '/fr/blog/refonte-application-web': '/blog',
  '/fr/blog/regles-cold-email-efficaces': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/fr/blog/reprendre-equipe-vente-objectifs': '/blog',
  '/fr/blog/social-selling-pourquoi-vous-devriez': '/blog',
  '/fr/blog/strategies-sdr-ia': '/blog/11-best-ai-bdr-tools',
  '/fr/blog/strategies-vente-analyser-prospects': '/blog',
  '/fr/blog/supprimer-cold-email-raisons': '/blog',
  '/fr/blog/synchronisation-bidirectionnelle-calesforce': '/blog',
  '/fr/blog/synchronisation-donnees-temps-reel-campagnes': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/fr/blog/test-ab-recrutement': '/blog',
  '/fr/blog/trouver-emails-nom-domaine-entreprise': '/blog/how-to-find-someone-email-address-efficiently',
  '/fr/blog/trouver-verifier-emails-application': '/blog/how-to-find-someone-email-address-efficiently',
  '/fr/blog/vente-sortante-b2b': '/blog',
  '/fr/blog/ventes-saas-fetes-fin-annee': '/blog',
  '/fr/blog/video-strategie-vente': '/blog',

  // === /DE (166 rules) ===
  '/de/blog/ab-test-affiliate-rekrutierung': '/blog',
  '/de/blog/abmeldelink-e-mail': '/blog',
  '/de/blog/alleinstellungsmerkmal': '/blog',
  '/de/blog/angebote-pipelines-vertrieb': '/blog',
  '/de/blog/apollo-vs-lemlist-vergleich': '/versus/apollo-vs-lemlist',
  '/de/blog/aussendienst-vertrieb-infografik': '/blog',
  '/de/blog/b2b-interessenten-beschaffung-tools': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/de/blog/b2b-leadgenerierung-manuell-vs-ki': '/blog',
  '/de/blog/b2b-vertrieb-followups-ki-assistent': '/blog',
  '/de/blog/b2b-vertrieb-skalieren-ki-plattformen': '/blog',
  '/de/blog/b2b-vertriebsautomatisierung-leitfaden': '/blog/best-ai-sales-tools',
  '/de/blog/berichte-v2': '/blog',
  '/de/blog/beste-cold-email-software': '/blog/9-best-ai-email-outreach-tools',
  '/de/blog/betreffzeilen-cold-email-bewaehrt': '/blog/500-trigger-words',
  '/de/blog/cold-e-mail-checkliste': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/de/blog/cold-email-abgelehnt-gruende': '/blog',
  '/de/blog/cold-email-copywriting-tipps': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/de/blog/cold-email-regeln-datenbasiert': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/de/blog/cold-email-software': '/blog/9-best-ai-email-outreach-tools',
  '/de/blog/e-mail-anhaenge-versenden': '/blog',
  '/de/blog/e-mail-outreach-automatisierung-b2b': '/blog/9-best-ai-email-outreach-tools',
  '/de/blog/e-mail-prospecting-fehler': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/de/blog/e-mail-wichtige-personen-kontaktieren': '/blog',
  '/de/blog/e-mails-finden-name-organisationsdomaene': '/blog/how-to-find-someone-email-address-efficiently',
  '/de/blog/e-mails-finden-verifizieren-app': '/blog/how-to-find-someone-email-address-efficiently',
  '/de/blog/echtzeit-datensynchronisierung-mehrkanalkampagnen': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/de/blog/generische-geschafts-e-mails-vermeiden': '/blog/increase-reply-rate',
  '/de/blog/grundlegende-eigenschaften-sdr': '/blog',
  '/de/blog/gute-emails-schreiben': '/blog/whats-the-best-email-length-for-sales-outreach',
  '/de/blog/heyreach-bewertung': '/blog/8-best-ai-linkedin-outreach-tools',
  '/de/blog/instantly-vs-lemlist-vergleich': '/versus/instantly-vs-lemlist',
  '/de/blog/kaufer-einwande-ueberwinden': '/blog/deal-objections',
  '/de/blog/ki-e-mail-writer-cold-outreach': '/blog/9-best-ai-email-outreach-tools',
  '/de/blog/ki-echtzeit-datensynchronisierung-vertrieb': '/blog',
  '/de/blog/ki-email-writer-kaltakquise': '/blog/9-best-ai-email-outreach-tools',
  '/de/blog/ki-followup-planung-vertrieb': '/blog',
  '/de/blog/ki-mehrkanalkampagnen-skalierbarkeit': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/de/blog/ki-sdr-strategien-b2b-umsatz': '/blog/11-best-ai-bdr-tools',
  '/de/blog/ki-vertrieb-ethik-richtlinien': '/blog/best-ai-sales-tools',
  '/de/blog/ki-vertrieb-roi-steigern': '/blog',
  '/de/blog/ki-vertriebs-workflow-tools': '/blog/best-ai-sales-tools',
  '/de/blog/ki-vertriebsassistent-anleitung': '/blog',
  '/de/blog/ki-vertriebstool-b2b': '/blog/best-ai-sales-tools',
  '/de/blog/ki-vertriebstools-skalierbarkeit-anpassung': '/blog/best-ai-sales-tools',
  '/de/blog/leadgenerierung-mitarbeiter-einstellen': '/blog',
  '/de/blog/lemlist-vs-apollo-vergleich': '/versus/lemlist-vs-apollo',
  '/de/blog/linkedin-outreach': '/blog/8-best-ai-linkedin-outreach-tools',
  '/de/blog/listen-verbesserungen': '/blog',
  '/de/blog/mehrere-ereignisse-tracking': '/blog',
  '/de/blog/neue-integrationseinstellungen': '/blog',
  '/de/blog/neues-dashboard': '/blog',
  '/de/blog/outbound-sales-leitfaden-b2b': '/blog',
  '/de/blog/outreach-e-mailing-fehler': '/blog',
  '/de/blog/overloop-ai-zukunft-vertrieb': '/blog/best-ai-sales-tools',
  '/de/blog/overloop-alternative-saleshandy': '/versus/overloop-vs-saleshandy',
  '/de/blog/overloop-calendly-integration': '/blog',
  '/de/blog/overloop-ereignisse-2020': '/blog',
  '/de/blog/overloop-plattform-update-outbound': '/blog',
  '/de/blog/overloop-vs-apollo-vergleich': '/versus/overloop-vs-apollo',
  '/de/blog/overloop-vs-artisan-vergleich': '/versus/overloop-vs-artisan',
  '/de/blog/overloop-vs-hubspot': '/versus/overloop-vs-hubspot',
  '/de/blog/overloop-vs-instantly-vergleich': '/versus/overloop-vs-instantly',
  '/de/blog/overloop-vs-lemlist-vergleich': '/versus/overloop-vs-lemlist',
  '/de/blog/saas-verkaufe-weihnachtszeit': '/blog',
  '/de/blog/salesforce-2-wege-synchronisierung': '/blog',
  '/de/blog/schlechte-angewohnheiten-verkaeufer': '/blog',
  '/de/blog/social-selling-beherrschen-schritte': '/blog',
  '/de/blog/social-selling-warum-wichtig': '/blog',
  '/de/blog/startup-gruender-fehler-vertrieb': '/blog',
  '/de/blog/startup-gruender-vertrieb-einstieg': '/blog',
  '/de/blog/store': '/blog',
  '/de/blog/team-retreat-bedeutung': '/blog',
  '/de/blog/verkaufserfolg-schlussel-vertriebskompetenz': '/blog/5-rules-more-successful-salespeople',
  '/de/blog/verkaufsprospektion-automatisierung': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/de/blog/verkaufsprospektion-leitfaden-kaltakquise': '/blog',
  '/de/blog/verkaufsstrategien-interessenten-analyse': '/blog',
  '/de/blog/vertrieb-lektionen-verhandlung-fbi': '/blog',
  '/de/blog/vertriebs-influencer-strategien': '/blog',
  '/de/blog/vertriebsautomatisierung-account-based-marketing': '/blog',
  '/de/blog/vertriebsautomatisierung-account-based-selling': '/blog',
  '/de/blog/vertriebskennzahlen-unverzichtbar': '/blog',
  '/de/blog/vertriebsleadlisten-automatisieren': '/blog',
  '/de/blog/vertriebsleads-generierung-b2b-leitfaden': '/blog/best-ai-sales-tools',
  '/de/blog/vertriebspipeline-verwalten': '/blog/pre-call-planning',
  '/de/blog/vertriebsplattform-auswaehlen-outbound': '/blog/best-ai-sales-tools',
  '/de/blog/vertriebsplattform-funktionen-outbound': '/blog',
  '/de/blog/vertriebsprozess-aufbauen': '/blog',
  '/de/blog/vertriebsprozesse-dokumentieren-automatisieren': '/blog/common-sales-automation-mistakes-and-how-to-avoid-them',
  '/de/blog/vertriebssoftware-b2b-leadgenerierung': '/blog',
  '/de/blog/vertriebstalente-anwerben-einstellen-fuehren': '/blog',
  '/de/blog/vertriebsteam-ubernehmen-ziele-erreichen': '/blog',
  '/de/blog/vertriebstipps-rookie-sales-reps': '/blog',
  '/de/blog/vertriebstools-b2b-teams-leitfaden': '/blog',
  '/de/blog/video-in-verkaufsstrategie': '/blog',
  '/de/blog/warum-wir-diesen-blog-starten': '/blog',
  '/de/blog/webanwendung-neugestaltung': '/blog',

  // === /ES (166 rules) ===
  '/es/blog/3-errores-comunes-email-outreach': '/blog',
  '/es/blog/8-eventos-clave-overloop-2020': '/blog',
  '/es/blog/adjuntos-overloop': '/blog',
  '/es/blog/apollo-vs-lemlist-comparativa': '/versus/apollo-vs-lemlist',
  '/es/blog/atraer-contratar-liderar-talento-ventas': '/blog',
  '/es/blog/aumentar-ventas-saas-temporada-festiva': '/blog',
  '/es/blog/automatizacion-ventas-habilitacion': '/blog',
  '/es/blog/automatizacion-ventas-venta-basada-cuentas': '/blog',
  '/es/blog/automatizar-seguimientos-multicanal-ia-ventas-b2b': '/blog',
  '/es/blog/buscar-correos-electronicos-nombre': '/blog/how-to-find-someone-email-address-efficiently',
  '/es/blog/calendly-integration': '/blog',
  '/es/blog/canal-de-ventas': '/blog/pre-call-planning',
  '/es/blog/checklist-email-frio': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/es/blog/como-usar-asistente-ventas-ia-b2b': '/blog',
  '/es/blog/como-usar-software-ventas-b2b': '/blog',
  '/es/blog/configuracion-integracion': '/blog',
  '/es/blog/consejos-vendedores-nuevos': '/blog',
  '/es/blog/contratar-generacion-leads': '/blog',
  '/es/blog/copywriting-email-frio-consejos': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/es/blog/correo-personas-importantes': '/blog',
  '/es/blog/cualidades-esenciales-sdr-ambicioso': '/blog',
  '/es/blog/documentar-procesos-ventas': '/blog/common-sales-automation-mistakes-and-how-to-avoid-them',
  '/es/blog/enlace-cancelar-suscripcion': '/blog',
  '/es/blog/error-fundadores-startups-ventas': '/blog',
  '/es/blog/errores-prospeccion-email-frio': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/es/blog/escalar-ventas-b2b-ia': '/blog',
  '/es/blog/escribir-correos-electronicos': '/blog/whats-the-best-email-length-for-sales-outreach',
  '/es/blog/escritores-correo-electronico-ia': '/blog/9-best-ai-email-outreach-tools',
  '/es/blog/estado-ventas-campo-infografia': '/blog',
  '/es/blog/estrategias-ia-sdr-ventas-b2b': '/blog/11-best-ai-bdr-tools',
  '/es/blog/estrategias-ventas-analizar-prospectos': '/blog',
  '/es/blog/etica-ia-ventas': '/blog/best-ai-sales-tools',
  '/es/blog/generacion-leads-b2b': '/blog',
  '/es/blog/gestion-listas-leads-ventas': '/blog',
  '/es/blog/guia-automatizacion-email-outreach-b2b': '/blog/9-best-ai-email-outreach-tools',
  '/es/blog/guia-automatizacion-ventas-b2b-2025': '/blog/best-ai-sales-tools',
  '/es/blog/guia-completa-heyreach': '/blog/8-best-ai-linkedin-outreach-tools',
  '/es/blog/guia-elegir-plataforma-ventas-salientes': '/blog/best-ai-sales-tools',
  '/es/blog/guia-generacion-leads-ventas-b2b': '/blog/best-ai-sales-tools',
  '/es/blog/guia-herramientas-ventas-equipos-b2b': '/blog',
  '/es/blog/guia-incorporar-video-estrategia-ventas': '/blog',
  '/es/blog/guia-plataformas-ventas-generacion-leads': '/blog',
  '/es/blog/guia-prospeccion-ventas': '/blog',
  '/es/blog/guia-ventas-salientes-b2b': '/blog',
  '/es/blog/habilidades-ventas': '/blog/5-rules-more-successful-salespeople',
  '/es/blog/herramienta-ia-ventas-b2b-caso-estudio': '/blog/best-ai-sales-tools',
  '/es/blog/herramientas-prospeccion-b2b-checklist': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/es/blog/herramientas-ventas-ia': '/blog/best-ai-sales-tools',
  '/es/blog/ia-campanas-multicanal': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/es/blog/ia-correo-electronico-divulgacion-fria': '/blog/9-best-ai-email-outreach-tools',
  '/es/blog/ia-roi-ventas': '/blog',
  '/es/blog/ia-seguimiento-ventas': '/blog',
  '/es/blog/influencers-ventas-como-destacar-competencia': '/blog',
  '/es/blog/informes-ventas': '/blog',
  '/es/blog/instantly-vs-lemlist-comparativa': '/versus/instantly-vs-lemlist',
  '/es/blog/lecciones-ventas-negociador-fbi': '/blog',
  '/es/blog/lemlist-vs-apollo-comparativa': '/versus/lemlist-vs-apollo',
  '/es/blog/liderar-equipo-ventas': '/blog',
  '/es/blog/lineas-asunto-correo-frio': '/blog/500-trigger-words',
  '/es/blog/malos-habitos-vendedores': '/blog',
  '/es/blog/mejor-software-correo-frio': '/blog/9-best-ai-email-outreach-tools',
  '/es/blog/mejoras-listas': '/blog',
  '/es/blog/mejores-herramientas-workflow-ventas-ia': '/blog/best-ai-sales-tools',
  '/es/blog/metricas-ventas-imprescindibles': '/blog',
  '/es/blog/nuevo-panel': '/blog',
  '/es/blog/objeciones-compradores': '/blog/deal-objections',
  '/es/blog/ofertas-pipelines': '/blog',
  '/es/blog/overloop-ai-ventas': '/blog/best-ai-sales-tools',
  '/es/blog/overloop-nueva-plataforma-workflows-salientes': '/blog',
  '/es/blog/overloop-vs-apollo-comparativa': '/versus/overloop-vs-apollo',
  '/es/blog/overloop-vs-artisan-comparativa': '/versus/overloop-vs-artisan',
  '/es/blog/overloop-vs-instantly-comparativa': '/versus/overloop-vs-instantly',
  '/es/blog/overloop-vs-lemlist-comparativa': '/versus/overloop-vs-lemlist',
  '/es/blog/overloop-vs-saleshandy': '/versus/overloop-vs-saleshandy',
  '/es/blog/por-que-iniciamos-este-blog': '/blog',
  '/es/blog/proceso-de-ventas': '/blog',
  '/es/blog/propuesta-unica-de-venta': '/blog',
  '/es/blog/prospeccion-ventas-ia': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/es/blog/pruebas-ab-reclutamiento-afiliados': '/blog',
  '/es/blog/razones-elimine-tu-email-frio': '/blog',
  '/es/blog/rediseno-aplicacion-web': '/blog',
  '/es/blog/reglas-correo-frio': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/es/blog/retiro-equipo-importancia': '/blog',
  '/es/blog/salesforce-sincronizacion-bidireccional': '/blog',
  '/es/blog/seguimiento-multiples-eventos': '/blog',
  '/es/blog/sincronizacion-datos-campanas-multicanal': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/es/blog/sincronizacion-datos-tiempo-real': '/blog',
  '/es/blog/software-prospeccion-email': '/blog/9-best-ai-email-outreach-tools',
  '/es/blog/tasas-respuesta-campanas-cold-email': '/blog/increase-reply-rate',
  '/es/blog/tienda-integraciones-overloop': '/blog',
  '/es/blog/venta-social': '/blog',
  '/es/blog/ventas-sociales': '/blog',
  '/es/blog/ventas-startups': '/blog',
  '/es/blog/verificar-correos-electronicos': '/blog/how-to-find-someone-email-address-efficiently',

  // === /IT (166 rules) ===
  '/it/blog/ab-testing-affiliati': '/blog',
  '/it/blog/aggiornamento-piattaforma-overloop': '/blog',
  '/it/blog/ai-campagne-multicanale-scalabilita': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/it/blog/ai-email-writer-cold-outreach': '/blog/9-best-ai-email-outreach-tools',
  '/it/blog/ai-email-writer-cold-outreach-caso-studio': '/blog/9-best-ai-email-outreach-tools',
  '/it/blog/ai-follow-up-vendite': '/blog',
  '/it/blog/ai-migliorare-roi-vendite': '/blog',
  '/it/blog/ai-sincronizzazione-dati-vendite': '/blog',
  '/it/blog/ai-vendite-scalabilita-personalizzazione': '/blog/best-ai-sales-tools',
  '/it/blog/allegati-email': '/blog',
  '/it/blog/analisi-prospect-rifiuti': '/blog',
  '/it/blog/apollo-vs-lemlist': '/versus/apollo-vs-lemlist',
  '/it/blog/assumere-lead-generation': '/blog',
  '/it/blog/attrarre-assumere-talenti-vendite': '/blog',
  '/it/blog/automazione-email-outreach-b2b': '/blog/9-best-ai-email-outreach-tools',
  '/it/blog/automazione-vendite-account-based': '/blog',
  '/it/blog/automazione-vendite-b2b': '/blog/best-ai-sales-tools',
  '/it/blog/cattive-abitudini-venditori': '/blog',
  '/it/blog/checklist-cold-email': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/it/blog/come-usare-assistente-vendite-ai': '/blog',
  '/it/blog/competenze-vendita-successo': '/blog/5-rules-more-successful-salespeople',
  '/it/blog/consigli-venditori-principianti': '/blog',
  '/it/blog/copywriting-cold-email': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/it/blog/costruire-processo-vendita': '/blog',
  '/it/blog/documentare-automatizzare-processo-vendita': '/blog/common-sales-automation-mistakes-and-how-to-avoid-them',
  '/it/blog/email-a-persone-importanti': '/blog',
  '/it/blog/email-aziendali-generiche': '/blog/increase-reply-rate',
  '/it/blog/errori-comuni-email-outreach': '/blog',
  '/it/blog/errori-fondatori-startup-vendite': '/blog',
  '/it/blog/errori-prospezione-email': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/it/blog/etica-ai-nelle-vendite': '/blog/best-ai-sales-tools',
  '/it/blog/eventi-overloop': '/blog',
  '/it/blog/follow-up-multicanale-ai': '/blog',
  '/it/blog/funzionalita-piattaforma-vendite': '/blog',
  '/it/blog/generazione-lead-b2b-ai': '/blog',
  '/it/blog/gestione-liste-lead-automatizzata': '/blog',
  '/it/blog/gestire-pipeline-vendite': '/blog/pre-call-planning',
  '/it/blog/gestire-team-vendite-obiettivi': '/blog',
  '/it/blog/guida-lead-generation-b2b': '/blog/best-ai-sales-tools',
  '/it/blog/guida-prospezione-vendite': '/blog',
  '/it/blog/guida-vendite-outbound-b2b': '/blog',
  '/it/blog/heyreach-recensione-linkedin': '/blog/8-best-ai-linkedin-outreach-tools',
  '/it/blog/importanza-ritiro-di-team': '/blog',
  '/it/blog/impostazioni-integrazione': '/blog',
  '/it/blog/influencer-vendite': '/blog',
  '/it/blog/iniziare-vendite-startup': '/blog',
  '/it/blog/instantly-vs-lemlist': '/versus/instantly-vs-lemlist',
  '/it/blog/integrazione-calendly': '/blog',
  '/it/blog/lemlist-vs-apollo': '/versus/lemlist-vs-apollo',
  '/it/blog/lezioni-vendita-fbi': '/blog',
  '/it/blog/link-disiscrizione': '/blog',
  '/it/blog/metriche-vendite-chiave': '/blog',
  '/it/blog/miglior-software-cold-email': '/blog/9-best-ai-email-outreach-tools',
  '/it/blog/miglioramenti-liste': '/blog',
  '/it/blog/migliori-strumenti-ai-vendite': '/blog/best-ai-sales-tools',
  '/it/blog/nuova-dashboard': '/blog',
  '/it/blog/obiezioni-acquirenti-strategie': '/blog/deal-objections',
  '/it/blog/oggetto-email-vendita-efficace': '/blog/500-trigger-words',
  '/it/blog/outreach-linkedin-risposte': '/blog/8-best-ai-linkedin-outreach-tools',
  '/it/blog/overloop-ai-futuro-vendite': '/blog/best-ai-sales-tools',
  '/it/blog/overloop-vs-apollo': '/versus/overloop-vs-apollo',
  '/it/blog/overloop-vs-artisan': '/versus/overloop-vs-artisan',
  '/it/blog/overloop-vs-hubspot': '/versus/overloop-vs-hubspot',
  '/it/blog/overloop-vs-instantly': '/versus/overloop-vs-instantly',
  '/it/blog/overloop-vs-lemlist': '/versus/overloop-vs-lemlist',
  '/it/blog/overloop-vs-saleshandy': '/versus/overloop-vs-saleshandy',
  '/it/blog/perche-blog-vendite': '/blog',
  '/it/blog/perche-eliminano-cold-email': '/blog',
  '/it/blog/piattaforma-vendite-outbound': '/blog/best-ai-sales-tools',
  '/it/blog/pipeline-trattative': '/blog',
  '/it/blog/proposta-di-valore-unica': '/blog',
  '/it/blog/prospezione-vendite-automazione': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/it/blog/qualita-sdr-ambizioso': '/blog',
  '/it/blog/rapporti-v2': '/blog',
  '/it/blog/regole-cold-email': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/it/blog/riprogettazione-applicazione-web': '/blog',
  '/it/blog/scalare-vendite-b2b-ai': '/blog',
  '/it/blog/scrivere-email-efficaci': '/blog/whats-the-best-email-length-for-sales-outreach',
  '/it/blog/sincronizzazione-dati-campagne-multicanale': '/blog/10-best-practices-for-multi-channel-sales-campaigns',
  '/it/blog/social-selling-b2b': '/blog',
  '/it/blog/social-selling-strategie': '/blog',
  '/it/blog/software-cold-email-b2b': '/blog/9-best-ai-email-outreach-tools',
  '/it/blog/software-vendite-lead-generation-b2b': '/blog',
  '/it/blog/stato-del-field-sales': '/blog',
  '/it/blog/store': '/blog',
  '/it/blog/strategie-ai-sdr-b2b': '/blog/11-best-ai-bdr-tools',
  '/it/blog/strumenti-ai-vendite-b2b-caso-studio': '/blog/best-ai-sales-tools',
  '/it/blog/strumenti-ricerca-prospect-b2b': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',
  '/it/blog/strumenti-vendite-b2b-moderni': '/blog',
  '/it/blog/strumenti-workflow-vendite-ai': '/blog/best-ai-sales-tools',
  '/it/blog/sync-salesforce-bidirezionale': '/blog',
  '/it/blog/tracciamento-eventi-multipli': '/blog',
  '/it/blog/trovare-email-da-nome-dominio': '/blog/how-to-find-someone-email-address-efficiently',
  '/it/blog/trovare-verificare-email': '/blog/how-to-find-someone-email-address-efficiently',
  '/it/blog/vendite-saas-stagionali': '/blog',
  '/it/blog/video-nella-strategia-vendite': '/blog',

};

// ──────────────────────────────────────────────
// TOOLS.OVERLOOP.COM → OVERLOOP.COM
// Subdomain redirect: tools + playbooks (41 rules)
// ──────────────────────────────────────────────

const TOOLS_REDIRECTS = {
  // Tools
  '/roi-calculator': '/tools/roi-calculator',
  '/infrastructure-calculator': '/tools/infrastructure-calculator',
  '/domain-health': '/tools/domain-health',
  '/spam-checker': '/tools/spam-checker',
  '/prompt-builder': '/tools/prompt-builder',

  // Playbooks: handled by the hostname check below (tools.overloop.com → overloop.com)
  // No entries here — the Worker already routes /playbooks/* via reverse proxy
  // and the hostname block catches tools.overloop.com/playbooks/* specifically
};

// ──────────────────────────────────────────────
// WORKER
// ──────────────────────────────────────────────

export default {
  async fetch(request) {
    const url = new URL(request.url);

    // 1. Strip ?origin= parameter
    if (url.searchParams.has('origin')) {
      url.searchParams.delete('origin');
      return Response.redirect(url.toString(), 301);
    }

    // 2. Handle tools.overloop.com redirects
    if (url.hostname === 'tools.overloop.com') {
      const path = url.pathname.replace(/\/$/, '');
      if (path.startsWith('/playbooks')) {
        return Response.redirect(`https://overloop.com${path}`, 301);
      }
      const toolTarget = TOOLS_REDIRECTS[path];
      if (toolTarget) {
        return Response.redirect(`https://overloop.com${toolTarget}`, 301);
      }
      return Response.redirect('https://overloop.com/tools/', 301);
    }

    // 3. Normalize: strip trailing slash
    const path = url.pathname.replace(/\/$/, '') || '/';

    // 4. Handle EN blog 301 redirects (kills, consolidations, VS redirects)
    const redirectTarget = BLOG_REDIRECTS[path];
    if (redirectTarget) {
      return Response.redirect(`https://overloop.com${redirectTarget}`, 301);
    }

    // 5. International page redirects: specific locale → EN target
    const intlTarget = INTL_REDIRECTS[path];
    if (intlTarget) {
      return Response.redirect(`https://overloop.com${intlTarget}`, 301);
    }

    // 5b. Catch-all for any remaining /<lang>/blog/* not in the specific map
    const intlMatch = path.match(/^\/(fr|es|it|de)\/blog(\/.*)?$/);
    if (intlMatch) {
      const enPath = `/blog${intlMatch[2] || ''}`;
      return Response.redirect(`https://overloop.com${enPath}`, 301);
    }

    // 6. Reverse proxy to GitHub Pages
    //    Routes: /blog/*, /versus/*, /tools/*, /playbooks/*, /templates/*
    if (
      path.startsWith('/blog') ||
      path.startsWith('/versus') ||
      path.startsWith('/tools') ||
      path.startsWith('/playbooks') ||
      path.startsWith('/templates')
    ) {
      const ghPagesUrl = `https://sortlist.github.io/overloop-blog${path}`;
      const response = await fetch(ghPagesUrl, {
        headers: request.headers,
      });
      const newResponse = new Response(response.body, response);
      newResponse.headers.set('X-Robots-Tag', 'index, follow');
      return newResponse;
    }

    // 7. Pass through everything else (Webflow)
    return fetch(request);
  }
};
