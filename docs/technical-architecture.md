# Architecture technique — Migration Blog Overloop

## Comment ça marche aujourd'hui (AVANT migration)

```
Visiteur → Cloudflare (DNS + proxy) → Webflow (héberge TOUT le site)
```

Webflow sert toutes les pages : homepage, /blog/*, /pricing, /features, etc.
Le CMS Webflow contient tous les articles du blog.

## Comment ça marchera APRÈS migration

```
Visiteur → Cloudflare Worker (routing intelligent) → ??
                                                      ├─ /blog/*      → GitHub Pages (nouveau blog statique)
                                                      ├─ /versus/*    → GitHub Pages
                                                      ├─ /fr/blog/*   → GitHub Pages (articles FR)
                                                      ├─ /de/blog/*   → GitHub Pages (articles DE)
                                                      ├─ /es/blog/*   → GitHub Pages (articles ES)
                                                      ├─ /it/blog/*   → GitHub Pages (articles IT)
                                                      └─ tout le reste → Webflow (homepage, pricing, etc.)
```

## Le Cloudflare Worker fait 3 choses :

### 1. Redirections 301 (510 rules)
Quand quelqu'un visite une URL supprimée, le Worker renvoie un 301 :
```
GET /blog/new-dashboard → 301 → /blog (page supprimée)
GET /blog/overloop-vs-apollo → 301 → /versus/overloop-vs-apollo (VS redirect)
GET /fr/blog/ameliorations-listes → 301 → /blog (page supprimée en FR)
```

### 2. Reverse proxy vers GitHub Pages
Quand quelqu'un visite une URL qui EXISTE dans notre blog statique :
```
GET /blog/cold-email-illegal
  → Worker fetch https://sortlist.github.io/overloop-blog/blog/en/cold-email-illegal.html
  → Renvoie le HTML au visiteur
  → Le visiteur ne sait pas que ça vient de GitHub Pages
```

### 3. Pass-through vers Webflow
Tout ce qui n'est PAS /blog/*, /versus/*, /tools/*, /playbooks/* passe normalement à Webflow :
```
GET /pricing → Webflow (inchangé)
GET /features → Webflow (inchangé)
GET / → Webflow (inchangé)
```

## FAQ

### Les articles resteront dans le CMS Webflow ?
Oui, mais personne ne les verra plus. Le Worker intercepte TOUTES les requêtes /blog/* AVANT qu'elles n'atteignent Webflow. Webflow continue à servir le reste du site normalement.

### Peut-on revenir en arrière ?
Oui, en 1 minute : désactiver le Worker Cloudflare. Tout le trafic retourne à Webflow comme avant.

### Comment on publie un nouvel article ?
1. Créer/éditer le fichier HTML dans le repo GitHub
2. `git push` → GitHub Actions déploie automatiquement
3. L'article est live en ~1 minute (pas besoin de toucher à Webflow)

### Pourquoi pas juste Webflow ?
- Vitesse de publication : git push vs éditeur Webflow
- Aucune limite de template (HTML complet)
- Versionning (git history)
- Automation avec Claude Code (production de contenu à l'échelle)
- Coût : GitHub Pages = gratuit

### Le Worker gère les trailing slashes ?
Oui. `/blog/cold-email-illegal` et `/blog/cold-email-illegal/` sont tous deux gérés.

### Et le SEO ?
- Les 301 redirects préservent le link juice
- Les canonical URLs pointent vers les bonnes URLs de production
- Les hreflang tags lient les versions linguistiques
- Schema markup (BlogPosting, BreadcrumbList) sur chaque page

## Pour Engineering : ce qui est nécessaire

1. **Ajouter le Worker Cloudflare** sur la route `overloop.com/*`
   - Fichier : `redirects/cloudflare-worker.js`
   - Le Worker vérifie d'abord les redirects, puis fait le reverse proxy, puis pass-through vers Webflow

2. **Configurer le DNS** (probablement déjà fait)
   - `overloop.com` → Cloudflare (déjà en place)
   - Le Worker remplace les Page Rules existantes pour /blog/*

3. **Pas besoin de** :
   - Changer la config Webflow
   - Modifier les DNS
   - Configurer GitHub Pages (déjà actif)
   - Supprimer les articles du CMS Webflow (ils restent en backup)
