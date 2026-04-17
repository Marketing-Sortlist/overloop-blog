# Overloop Blog: SEO Migration Audit & Go-Live Checklist

**Date**: 2026-04-15
**Migration**: Webflow -> Static HTML on GitHub Pages + Cloudflare reverse proxy
**Scope**: 75 EN articles + 10 VS pages + 20 DE + 20 FR + 20 ES localized articles

---

## Part 1: SEO Migration Best Practices Audit

### 1. 301 Redirects

**Status: WARNING -- 1 self-redirect found, 1 coverage gap**

**What is correct:**
- 98 EN blog redirect rules covering kills, consolidations, and VS redirects
- 646 international page redirects (FR/DE/ES/IT -> EN equivalents)
- All use 301 (permanent) status codes
- Trailing slash normalization is handled
- `?origin=` query parameter stripping is in place
- tools.overloop.com redirects to overloop.com/tools/

**Issues found:**

1. **SELF-REDIRECT (BUG)**: Line 39 of the worker has:
   ```
   '/blog/best-ai-sales-tools': '/blog/best-ai-sales-tools'
   ```
   This creates an infinite redirect loop. The browser will show ERR_TOO_MANY_REDIRECTS. Since `best-ai-sales-tools` IS a kept page (it exists as a static file on GitHub Pages), this rule must be **removed entirely** from `BLOG_REDIRECTS`. The Worker checks redirects BEFORE proxying to GitHub Pages, so this redirect fires before the reverse proxy can serve the actual page.

   **Fix**: Remove the line `'/blog/best-ai-sales-tools': '/blog/best-ai-sales-tools',` from the worker.

2. **Missing /de/blog/overloop-vs-reply redirect**: The FR version `/fr/blog/overloop-vs-reply` redirects to `/versus/overloop-vs-reply`, but no DE, ES, or IT equivalent exists. Check if `/de/blog/overloop-vs-reply` was a Webflow page. If so, add it.

3. **Intl catch-all only covers `/blog/*`**: The catch-all regex at line 838 is:
   ```
   /^\/(fr|es|it|de)\/blog(\/.*)?$/
   ```
   This does NOT catch `/<lang>/versus/*`. If any locale VS pages ever existed on Webflow, they would 404. See hreflang issue in section 3 below.

**No redirect chains detected** (other than the self-redirect above). All other redirect targets resolve to final destination URLs.

---

### 2. Canonical URLs

**Status: COMPLIANT**

All sampled articles have correct canonical tags pointing to production URLs:
- `https://overloop.com/blog/10-best-ai-sales-assistant-tools` (correct)
- `https://overloop.com/blog/455-email-spam-trigger-words-avoid-2018` (correct)
- `https://overloop.com/blog/get-email-from-linkedin-profile` (correct)
- VS pages: `https://overloop.com/versus/overloop-vs-apollo` (correct)

Canonical URLs use `overloop.com` (production), not `sortlist.github.io` (staging). This is correct.

---

### 3. Hreflang Tags

**Status: WARNING -- Hreflang targets point to non-existent pages**

**The problem:**

Every article and VS page declares 4 hreflang alternates:
```html
<link rel="alternate" hreflang="en" href="https://overloop.com/blog/slug">
<link rel="alternate" hreflang="de" href="https://overloop.com/de/blog/slug">
<link rel="alternate" hreflang="fr" href="https://overloop.com/fr/blog/slug">
<link rel="alternate" hreflang="es" href="https://overloop.com/es/blog/slug">
<link rel="alternate" hreflang="x-default" href="https://overloop.com/blog/slug">
```

But the /de/, /fr/, /es/ URLs all **301 redirect to the EN page**. Google says: *"hreflang annotations must be between canonical (non-redirecting) pages."* Having hreflang point to URLs that 301 to the same EN page violates this rule. Google will eventually ignore these hreflang tags, which is harmless but noisy in GSC.

**For blog articles (blog/de/, blog/fr/, blog/es/):**
- You have 20 articles in each locale (DE, FR, ES) which are actual pages on GitHub Pages. For THESE articles, the hreflang is correct since the locale page exists.
- For the remaining ~55 EN articles that have no locale equivalent, the hreflang tags point to URLs that redirect. This is incorrect per Google guidelines.

**For VS pages:**
- Hreflang tags point to `/de/versus/overloop-vs-apollo`, `/fr/versus/...` etc.
- NO locale VS pages exist on disk
- NO redirect rules exist for `/<lang>/versus/*`
- The intl catch-all regex only matches `/<lang>/blog/*`, not `/<lang>/versus/*`
- Result: these hreflang URLs will **404**, which is worse than redirecting

**Recommendations:**
1. **Quick fix**: Remove hreflang de/fr/es tags from all VS pages immediately, since no locale versions exist and no redirects cover them
2. **Quick fix**: For EN articles that DON'T have a locale counterpart, remove hreflang de/fr/es tags
3. **For articles that DO have locale versions** (the 20 per locale): keep hreflang, these are valid
4. **Alternative**: Add a catch-all for `/<lang>/versus/*` to the Cloudflare Worker:
   ```javascript
   const versusMatch = path.match(/^\/(fr|es|it|de)\/versus(\/.*)?$/);
   if (versusMatch) {
     return Response.redirect(`https://overloop.com/versus${versusMatch[2] || ''}`, 301);
   }
   ```
   This at least prevents 404s, though Google will still ignore redirecting hreflang.

---

### 4. Sitemap

**Status: WARNING -- Sitemap exists in CI but not on disk**

- `sitemap.xml` is **generated at build time** in the GitHub Actions workflow (deploy.yml)
- It is NOT checked into the repository -- it only exists after deployment
- The generation logic is correct: it finds all `.html` files in blog/tools/playbooks/templates, uses git log dates for lastmod, and outputs valid XML
- `robots.txt` correctly points to `https://overloop.com/sitemap.xml`

**Issues:**
1. The sitemap generator uses `find blog tools playbooks templates` but the files are in `blog/en/`, `blog/de/`, `blog/fr/`, `blog/es/`, so all locale articles WILL be included. Since locale articles 301 to EN, you'll have redirecting URLs in the sitemap. Google recommends only indexable (non-redirecting) URLs in sitemaps.
2. The `versus/` directory is not included in the find command. **VS pages will be missing from the sitemap.**
3. No `<changefreq>` or `<priority>` tags (minor -- Google largely ignores these)

**Fixes needed:**
1. Add `versus` to the find command: `find blog/en versus tools playbooks templates`
2. Exclude locale directories: use `blog/en` instead of `blog`, or explicitly exclude `blog/de blog/fr blog/es`
3. Consider generating the sitemap locally and committing it so you can inspect it before deploy

---

### 5. Robots.txt

**Status: WARNING -- Partial issues**

Current robots.txt:
```
User-agent: *
Allow: /blog/
Allow: /tools/
Allow: /playbooks/
Allow: /templates/
Disallow: /assets/
Disallow: /redirects/

Sitemap: https://overloop.com/sitemap.xml
```

**What is correct:**
- Allows crawling of all content directories
- Blocks /assets/ and /redirects/ (no SEO value)
- Points to correct sitemap URL

**Issues:**
1. **Missing `/versus/`**: The `Allow: /versus/` rule is not present. Since this robots.txt is served from GitHub Pages (not the overloop.com root), AND there's no `Disallow: /`, the absence of an Allow directive for /versus/ doesn't technically block it. But adding it explicitly is best practice for clarity.
2. **No User-agent blocks for bad bots**: Consider adding blocks for known scrapers (GPTBot, CCBot etc.) if you want to control AI training crawlers. Optional.
3. The robots.txt is correct for staging (noindex is handled via meta tags, not robots.txt). On go-live, it should work as-is.

**Fix**: Add `Allow: /versus/` to robots.txt.

---

### 6. Internal Linking

**Status: CRITICAL -- All internal links use staging paths**

Every HTML file uses staging paths that will break in production:

- **CSS**: `href="/overloop-blog/assets/css/overloop.css"` (778 occurrences across 75 files)
  - Production should be: `href="/assets/css/overloop.css"`

- **Internal article links**: `href="/overloop-blog/blog/en/slug.html"`
  - Production should be: `href="/blog/slug"`

- **OG images**: `content="https://sortlist.github.io/overloop-blog/assets/images/og/..."` (148 occurrences across 74 files)
  - Production should be: `content="https://overloop.com/assets/images/og/..."`

These are known staging artifacts (documented in CLAUDE.md go-live checklist). They MUST be fixed before go-live.

**Note**: The Cloudflare reverse proxy rewrites the URL path but does NOT rewrite HTML content. The browser will request `/overloop-blog/assets/css/overloop.css` from `overloop.com`, which will 404 since the Cloudflare Worker only proxies `/blog/*`, `/versus/*`, `/tools/*`, `/playbooks/*`, `/templates/*` -- not `/overloop-blog/*`.

---

### 7. Content Parity

**Status: COMPLIANT -- High-value pages preserved**

Analysis of redirects.csv shows disciplined content triage:

**High-backlink pages KEPT (all MIGRATE or REWRITE):**
| Page | Backlink note | Action |
|------|--------------|--------|
| `/blog/455-email-spam-trigger-words-avoid-2018` | GoDaddy DR93, Etsy DR94, CampaignMonitor DR90, Kajabi DR86 | REWRITE (URL kept) |
| `/blog/whats-the-best-email-length-for-sales-outreach` | 10+ Zendesk DR93, Beehiiv DR91, Instantly DR78 | REWRITE (URL kept) |
| `/blog/cold-email-stats-2018` | GoDaddy DR93, OptinMonster DR88, SingleGrain DR79 | REWRITE (URL kept) |
| `/blog/cold-email-illegal` | GitHub DR97, SEMrush DR92, IndieHackers DR80 | REWRITE (URL kept) |
| `/blog/cold-emailing-link-building` | Shoptet DR91 | REWRITE (URL kept) |
| `/blog/how-to-find-someone-email-address-efficiently` | 98K impr, 2221 keywords, #1 rank | REWRITE (URL kept) |
| `/blog/get-email-from-linkedin-profile` | 62K impr, explosive growth | REWRITE (URL kept) |

**Key killed pages with some value (correctly redirected to relevant targets):**
- `/blog/ethics-of-ai-in-sales-key-challenges` (Substack DR93 backlink) -> `/blog/best-ai-sales-tools` (captures link juice)
- `/blog/ai-sales-tools-scalability-vs-customization` (976 impr) -> `/blog/best-ai-sales-tools`
- `/blog/the-ultimate-guide-to-sales-platform-features-and-benefits-for-outbound-lead-generation` (40 AI hits) -> `/blog` (could be redirected to a more relevant target)

**No high-value content is being lost.** The 82 killed pages are genuinely low-value (most under 100 impressions, 0 clicks). Consolidation targets are sensible.

---

### 8. Page Speed

**Status: EXPECTED IMPROVEMENT**

Static HTML with no JavaScript framework overhead will be significantly faster than Webflow. Key observations:

**Positives:**
- Font preconnect hints are in place (`fonts.googleapis.com`, `fonts.gstatic.com`)
- Single CSS file (25.9 KB -- under render-blocking threshold)
- No heavy JS bundles
- GitHub Pages CDN + Cloudflare edge caching

**Concerns:**
1. **Google Fonts are render-blocking**: Two font families (Playfair Display + Inter) loaded via Google Fonts CSS. Consider self-hosting or using `font-display: swap` (check if the Google Fonts URL already includes `&display=swap` -- it does, so this is handled).
2. **No image optimization pipeline**: Check that OG images and in-article images are compressed. Static HTML means no automatic WebP conversion.
3. **No `<link rel="preload">` for critical CSS**: The CSS is at `/overloop-blog/assets/css/overloop.css` (staging path). Once fixed to production path, consider preloading it.
4. **Cloudflare double-hop**: Request goes User -> Cloudflare -> GitHub Pages CDN -> back to Cloudflare -> User. Ensure Cloudflare caches the GitHub Pages response (set appropriate cache headers in the Worker).

**Recommendation**: After go-live, add cache headers in the Worker response:
```javascript
newResponse.headers.set('Cache-Control', 'public, max-age=3600, s-maxage=86400');
```

---

### 9. Schema Markup

**Status: COMPLIANT (with minor inconsistencies)**

All sampled articles include:
- `BlogPosting` schema with headline, description, author, publisher, dates, mainEntityOfPage
- `BreadcrumbList` schema (Blog -> Article Title)
- `FAQPage` schema (where applicable -- confirmed on spam-trigger-words and get-email-from-linkedin)

VS pages use `WebPage` schema instead of `BlogPosting` -- this is correct since they're comparison pages, not blog posts.

**Minor inconsistencies:**
1. **Image URLs in schema differ from OG images**: For example, `10-best-ai-sales-assistant-tools` has:
   - Schema image: `https://overloop.com/assets/images/og-10-best-ai-sales-assistant-tools.png`
   - OG image: `https://sortlist.github.io/overloop-blog/assets/images/og/10-best-ai-sales-assistant-tools.png`
   - These should both be `https://overloop.com/assets/images/og/10-best-ai-sales-assistant-tools.png`
2. **Some author URLs are empty**: `get-email-from-linkedin-profile` has `"url": ""` for author Vincenzo Ruggiero. Add LinkedIn URLs for all authors for E-E-A-T signals.
3. **Publisher logo path**: `https://overloop.com/assets/images/overloop-logo.png` -- verify this file exists on GitHub Pages.

---

### 10. Mobile-Friendliness

**Status: COMPLIANT (based on markup)**

- All pages have `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- CSS file is 25.9 KB (reasonable for responsive styles)
- CLAUDE.md documents a `table-keep` class for large tables on mobile
- No fixed-width layout detected in markup

**Cannot fully verify without rendering**, but the responsive meta tag and documented mobile table handling suggest this is addressed. Recommend running Google's Mobile-Friendly Test on 3 representative pages after go-live:
1. A listicle: `/blog/best-ai-sales-tools`
2. A data-heavy page: `/blog/455-email-spam-trigger-words-avoid-2018`
3. A VS page: `/versus/overloop-vs-apollo`

---

## Summary of Critical Issues to Fix Before Go-Live

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | **CRITICAL** | Self-redirect loop on `/blog/best-ai-sales-tools` | Remove from BLOG_REDIRECTS |
| 2 | **CRITICAL** | All internal links use staging `/overloop-blog/` prefix | Find-and-replace across all HTML |
| 3 | **CRITICAL** | All OG images point to `sortlist.github.io` | Replace with `overloop.com` URLs |
| 4 | **HIGH** | Hreflang on VS pages point to 404ing locale URLs | Remove locale hreflang from VS pages OR add catch-all redirect |
| 5 | **HIGH** | Sitemap excludes `/versus/` pages | Add `versus` to find command in deploy.yml |
| 6 | **HIGH** | Sitemap includes locale articles that 301 | Change `blog` to `blog/en` in find command |
| 7 | **MEDIUM** | `noindex, nofollow` meta tags on all pages | Remove on go-live day |
| 8 | **MEDIUM** | robots.txt missing `Allow: /versus/` | Add the line |
| 9 | **LOW** | Schema image URLs inconsistent with OG image URLs | Align during content QA |
| 10 | **LOW** | Some author URLs empty in schema | Fill in LinkedIn URLs |

---

## Part 2: Post-Migration Monitoring Checklist

### First 24 Hours (D-Day)

**Immediate checks (within 1 hour of go-live):**

- [ ] **Manual spot-check**: Visit these 10 high-value pages in an incognito browser and verify they load correctly:
  1. `https://overloop.com/blog` (index page)
  2. `https://overloop.com/blog/how-to-find-someone-email-address-efficiently` (#1 ranked, 98K impr)
  3. `https://overloop.com/blog/get-email-from-linkedin-profile` (62K impr, explosive growth)
  4. `https://overloop.com/blog/whats-the-best-email-length-for-sales-outreach` (37K impr, Zendesk backlinks)
  5. `https://overloop.com/blog/how-to-write-a-successful-cold-email` (34K impr)
  6. `https://overloop.com/blog/the-ultimate-guide-to-linkedin-automation-boost-b2b-sales-in-2025` (24.8K impr)
  7. `https://overloop.com/blog/linkedin-vs-email-which-performs-better-for-b2b-outreach` (25K impr)
  8. `https://overloop.com/blog/455-email-spam-trigger-words-avoid-2018` (high-DR backlinks)
  9. `https://overloop.com/versus/overloop-vs-apollo` (VS page)
  10. `https://overloop.com/blog/best-ai-sales-tools` (hub page, was self-redirect bug)

- [ ] **Verify noindex is removed**: View page source on 3 random pages, confirm `<meta name="robots" content="noindex, nofollow">` is gone
- [ ] **Check canonical tags**: View source on 5 pages, confirm canonical points to `https://overloop.com/blog/slug` (not staging URLs)
- [ ] **Test redirects**: Try 5 old Webflow URLs and verify 301 redirect:
  - `https://overloop.com/blog/7-cold-email-subject-lines` -> should redirect to `/blog/500-trigger-words`
  - `https://overloop.com/fr/blog/obtenir-emails-linkedin` -> should redirect to `/blog/get-email-from-linkedin-profile`
  - `https://overloop.com/blog/overloop-vs-apollo` -> should redirect to `/versus/overloop-vs-apollo`
  - `https://overloop.com/blog/calendly-integration` -> should redirect to `/blog`
  - `https://overloop.com/es/blog/correos-perfil-linkedin` -> should redirect to `/blog/get-email-from-linkedin-profile`
- [ ] **Test a non-blog page**: Verify `https://overloop.com/pricing` still loads from Webflow (passthrough working)
- [ ] **Check CSS/assets loading**: Verify styles render correctly (not broken layout from wrong asset paths)
- [ ] **Check sitemap**: Visit `https://overloop.com/sitemap.xml`, verify it loads and contains correct URLs
- [ ] **Check robots.txt**: Visit `https://overloop.com/robots.txt`, verify it loads

**Within 2-4 hours:**

- [ ] **Submit sitemap in GSC**: Go to Google Search Console -> Sitemaps -> submit `https://overloop.com/sitemap.xml`
- [ ] **Request indexing**: In GSC URL Inspection, submit the top 10 high-value pages for re-indexing
- [ ] **Cloudflare Analytics**: Check for any 404 or 500 errors in Cloudflare dashboard
- [ ] **Monitor Cloudflare Worker errors**: Workers -> your worker -> Logs -> filter for errors
- [ ] **Google Cache check**: Search `cache:overloop.com/blog/how-to-find-someone-email-address-efficiently` to see what Google has cached (will still be old -- this is baseline)

**Within 12-24 hours:**

- [ ] **GSC Coverage report**: Check for any new 404 errors or crawl anomalies
- [ ] **Check redirect report**: In GSC, look at Pages -> "Page with redirect" -- should see the expected 301s
- [ ] **Uptime monitoring**: Verify no intermittent downtime from CF Worker or GitHub Pages

### First Week (D+1 to D+7)

- [ ] **Daily GSC check**: Monitor these metrics in Performance report:
  - Total clicks (should stabilize within 3-5 days, may dip initially)
  - Total impressions (leading indicator -- should hold steady)
  - Average position (should remain stable; any 3+ position drop on key pages = investigate)
  - CTR (may fluctuate as Google re-evaluates)

- [ ] **Track these specific queries in GSC** (your highest-value keywords):
  | Query | Pre-migration position | Watch for |
  |-------|----------------------|-----------|
  | "find someone's email address" | #1 | Any drop below #3 |
  | "get email from linkedin profile" | Top 5 | Any drop |
  | "email spam trigger words" | Top 10 | Position change |
  | "best email length sales" | Top 10 | Position change |
  | "cold email illegal" | Top 10 | Position change |
  | "ai bdr tools" | #2.4 | Any drop |
  | "apollo alternatives" | ~#10 | Movement direction |
  | "cold email power words" | #6 | Any drop |

- [ ] **Ahrefs backlink check**: Verify that backlinks to key pages (455-spam-trigger-words, cold-email-stats, email-length) are still resolving to 200 (not 404 or redirect loop)
- [ ] **Check 404 log in Cloudflare**: Look for any URLs being requested that aren't in your redirect map (organic traffic to old URLs you missed)
- [ ] **Verify locale redirects in GSC**: Check that /fr/blog/*, /de/blog/* etc. show as redirected (not errored)
- [ ] **Run Screaming Frog crawl** on `overloop.com/blog/` to check for:
  - Broken internal links
  - Missing canonical tags
  - Redirect chains
  - 404s
  - Mixed content (http:// in https:// pages)

### First Month (D+7 to D+30)

- [ ] **Weekly GSC position tracking**: Export positions for top 20 keywords, compare to pre-migration baseline
- [ ] **Organic traffic trend**: Compare organic sessions week-over-week in GA4
  - Expect: flat or slight dip in week 1-2, recovery by week 3-4
  - Red flag: >20% sustained drop after 2 weeks
- [ ] **Indexed pages count**: In GSC Coverage, track "Valid" pages count. Should match ~85 (75 EN articles + 10 VS pages)
- [ ] **Crawl stats**: GSC Settings -> Crawl stats. Watch for:
  - Crawl rate changes
  - Average response time (should decrease with static HTML)
  - Crawled vs. indexed ratio
- [ ] **Backlink monitoring**: Check Ahrefs weekly for:
  - New backlinks (are people still linking to your content?)
  - Lost backlinks (are referring pages getting 404?)
  - Referring domains trend
- [ ] **AEO monitoring**: Check AI search visibility for top pages using Ahrefs or manual queries in ChatGPT/Perplexity
- [ ] **Core Web Vitals**: After 28 days, check CWV data in GSC. Static HTML should show improved LCP and FID.
- [ ] **Re-submit sitemap**: Submit updated sitemap in GSC after any content changes during the month

### Red Flags That Require Immediate Action

| Signal | Severity | Action |
|--------|----------|--------|
| >30% traffic drop sustained for 3+ days | CRITICAL | Check for noindex tags still present, broken redirects |
| #1 keyword drops to #5+ | CRITICAL | Check canonical, content, schema on affected page |
| GSC shows "Excluded" for kept pages | HIGH | Check for noindex, canonical pointing elsewhere |
| Spike in 404 errors in Cloudflare | HIGH | Add missing redirects for missed URLs |
| Backlink donors reporting broken links | HIGH | Verify the specific URLs resolve correctly |
| Crawl rate drops to near zero | CRITICAL | Check robots.txt, server errors, Cloudflare Worker health |

### Rollback Plan

**If critical issues are detected within 24 hours:**

1. **Quick rollback** (5 minutes):
   - In Cloudflare Workers: disable the route that points `/blog/*` to the Worker
   - Traffic falls through to Webflow (original site still running)
   - Webflow was your origin for blog -- as long as you haven't deleted Webflow content, it serves as the fallback

2. **Partial rollback** (if only some pages are affected):
   - Add specific routes in the Worker to bypass GitHub Pages for broken pages
   - Example: Add a condition to proxy specific paths directly to Webflow:
     ```javascript
     const BYPASS_TO_WEBFLOW = ['/blog/best-ai-sales-tools'];
     if (BYPASS_TO_WEBFLOW.includes(path)) {
       return fetch(request); // pass through to Webflow
     }
     ```

3. **Full rollback** (nuclear option):
   - Disable the entire Cloudflare Worker
   - All traffic goes to Webflow
   - Redirects stop working (old locale pages return to Webflow versions)
   - Only do this if the Worker itself is crashing

**Rollback decision criteria:**
- Rollback if: 404 on more than 5 high-traffic pages AND fix will take >2 hours
- Do NOT rollback for: cosmetic issues, minor 404s on low-traffic pages, temporary GSC fluctuations
- Remember: every rollback and re-migration creates additional temporary ranking flux. Only rollback for genuine breakage.

**Pre-conditions for safe rollback:**
- [ ] Keep Webflow site active (do not delete) for at least 30 days after migration
- [ ] Document the exact Cloudflare Worker route configuration so you can re-enable it
- [ ] Have the Worker code in version control (it is: `redirects/cloudflare-worker.js`)

---

## Part 3: Go-Live Checklist

### T-minus 3 days: Pre-Flight

**Engineering:**

- [ ] Fix the `/blog/best-ai-sales-tools` self-redirect in `cloudflare-worker.js` (remove line 39)
- [ ] Add intl catch-all for `/versus/` paths in the Worker:
  ```javascript
  const versusMatch = path.match(/^\/(fr|es|it|de)\/versus(\/.*)?$/);
  if (versusMatch) {
    return Response.redirect(`https://overloop.com/versus${versusMatch[2] || ''}`, 301);
  }
  ```
- [ ] Run global find-and-replace on all HTML files:
  - Replace `href="/overloop-blog/` with `href="/` (CSS, JS, internal links)
  - Replace `src="/overloop-blog/` with `src="/` (images)
  - Replace `/overloop-blog/blog/en/slug.html` links with `/blog/slug` format
  - Replace `https://sortlist.github.io/overloop-blog/` with `https://overloop.com/` in OG/Twitter images
- [ ] Fix sitemap generation in `deploy.yml`:
  - Change `find blog tools playbooks templates` to `find blog/en versus tools playbooks templates`
  - This excludes locale directories (which redirect) and includes VS pages
- [ ] Add `Allow: /versus/` to `robots.txt`
- [ ] Remove hreflang `de`/`fr`/`es` tags from VS pages (OR rely on the new catch-all redirect)
- [ ] Align schema image URLs with OG image URLs across all articles
- [ ] Fill in empty author URLs in schema markup
- [ ] Verify `overloop-logo.png` exists at `/assets/images/overloop-logo.png` on GitHub Pages
- [ ] Add cache headers to Cloudflare Worker response:
  ```javascript
  newResponse.headers.set('Cache-Control', 'public, max-age=3600, s-maxage=86400');
  ```
- [ ] Change deploy.yml trigger from `workflow_dispatch` to `on: push` (or keep manual and trigger)
- [ ] Deploy to GitHub Pages (manual trigger or push)
- [ ] Verify deployment at `https://sortlist.github.io/overloop-blog/blog/en/` (staging check)

**Marketing:**

- [ ] Export current GSC data as baseline:
  - Performance report: last 3 months, all pages, export CSV
  - Coverage report: screenshot of valid/excluded/error counts
  - Sitemaps report: screenshot
- [ ] Export current Ahrefs data as baseline:
  - Organic keywords report
  - Top pages by traffic
  - Backlinks profile
- [ ] Prepare GSC URL inspection list (top 10 URLs to re-index on go-live day)
- [ ] Draft announcement for any stakeholders
- [ ] Verify Webflow site is still running (fallback)

### T-minus 1 day: Final Staging Check

**Engineering:**

- [ ] Deploy final version to GitHub Pages
- [ ] Curl-test 10 key pages on GitHub Pages directly (sortlist.github.io) to verify:
  - Pages return 200
  - `noindex` is gone
  - Canonical tags are correct
  - Internal links use production paths (`/blog/slug`, not `/overloop-blog/...`)
  - OG images point to `overloop.com`
  - CSS loads from `/assets/css/overloop.css`

```bash
# Quick verification script
for slug in how-to-find-someone-email-address-efficiently get-email-from-linkedin-profile best-ai-sales-tools 455-email-spam-trigger-words-avoid-2018 whats-the-best-email-length-for-sales-outreach; do
  echo "=== $slug ==="
  curl -s "https://sortlist.github.io/overloop-blog/blog/en/$slug.html" | head -20
  echo
done
```

- [ ] Test Cloudflare Worker in staging/preview mode (if available) with the fixed code
- [ ] Verify sitemap.xml was generated correctly in the latest deployment

### Go-Live Day (T=0)

**Recommended: Tuesday or Wednesday morning (avoid Friday deploys)**

**Step 1: Deploy Cloudflare Worker (Engineering, ~10 min)**

- [ ] 09:00 -- Upload the production `cloudflare-worker.js` to Cloudflare Workers
- [ ] Configure the Worker route: `overloop.com/blog/*`, `overloop.com/versus/*`, `overloop.com/tools/*`, `overloop.com/playbooks/*`, `overloop.com/templates/*`
- [ ] Verify Worker is active in Cloudflare dashboard

**Step 2: Immediate Smoke Tests (Engineering, ~15 min)**

- [ ] 09:15 -- Test each page type loads correctly:
  - `curl -I https://overloop.com/blog/how-to-find-someone-email-address-efficiently` (should be 200)
  - `curl -I https://overloop.com/versus/overloop-vs-apollo` (should be 200)
  - `curl -I https://overloop.com/blog/calendly-integration` (should be 301 -> /blog)
  - `curl -I https://overloop.com/fr/blog/obtenir-emails-linkedin` (should be 301 -> EN)
  - `curl -I https://overloop.com/pricing` (should be 200, from Webflow)
  - `curl -I https://overloop.com/blog/best-ai-sales-tools` (verify NO redirect loop!)
- [ ] Check in browser: CSS loads, images render, navigation works
- [ ] Check on mobile device: responsive layout, readable text
- [ ] Verify `X-Robots-Tag: index, follow` header is present (Worker sets this)
- [ ] Verify `noindex` meta tag is NOT in page source

**Step 3: Search Engine Notification (Marketing, ~20 min)**

- [ ] 09:30 -- Go to Google Search Console:
  - Submit sitemap: `https://overloop.com/sitemap.xml`
  - Use URL Inspection tool -> "Request Indexing" for top 10 pages:
    1. `/blog/how-to-find-someone-email-address-efficiently`
    2. `/blog/get-email-from-linkedin-profile`
    3. `/blog/whats-the-best-email-length-for-sales-outreach`
    4. `/blog/how-to-write-a-successful-cold-email`
    5. `/blog/the-ultimate-guide-to-linkedin-automation-boost-b2b-sales-in-2025`
    6. `/blog/linkedin-vs-email-which-performs-better-for-b2b-outreach`
    7. `/blog/455-email-spam-trigger-words-avoid-2018`
    8. `/blog/best-ai-sales-tools`
    9. `/blog/9-best-ai-agent-tools-for-sales`
    10. `/blog/11-best-ai-bdr-tools`
- [ ] Go to Bing Webmaster Tools: Submit sitemap (if configured)

**Step 4: Monitoring Setup (Engineering, ~10 min)**

- [ ] 09:50 -- Set up Cloudflare Worker monitoring:
  - Enable Worker analytics
  - Set up alert for error rate >1%
  - Set up alert for p99 latency >5s
- [ ] Verify Cloudflare is caching responses (check `CF-Cache-Status` header)

**Step 5: Hourly Monitoring (Both, rest of the day)**

- [ ] 10:00, 11:00, 12:00, 14:00, 16:00 -- Quick checks:
  - Cloudflare dashboard: any errors?
  - GSC: any new crawl errors appearing?
  - Spot-check 2-3 pages still working
  - Check Worker CPU/memory usage in Cloudflare

**Step 6: End-of-Day Review (Both, ~30 min)**

- [ ] 17:00 -- Review the day:
  - Total Worker requests processed
  - Error rate
  - Any 404s in Cloudflare analytics
  - GSC: has Google started re-crawling? (Check crawl stats)
  - All critical pages still loading
- [ ] Document any issues found and their fixes
- [ ] Confirm: Webflow site still running as fallback (do NOT turn off yet)

### Post Go-Live: Day 2-7

- [ ] D+1: Check GSC for first crawl data, note any anomalies
- [ ] D+2: Run Screaming Frog full crawl from `https://overloop.com/blog/`
- [ ] D+3: Compare GSC impressions to pre-migration baseline (same day of week)
- [ ] D+5: Check Ahrefs for any lost backlinks or ranking changes
- [ ] D+7: Full review meeting (Engineering + Marketing):
  - Are rankings stable?
  - Any unexpected 404s or errors?
  - Performance improvement measured?
  - Decision: keep monitoring or declare migration successful

### Post Go-Live: Week 2-4

- [ ] Weekly: Export GSC positions for top 20 keywords, compare to baseline
- [ ] Weekly: Check Ahrefs organic traffic estimate
- [ ] D+14: If stable, begin Phase 2 (content rewrites for REWRITE articles)
- [ ] D+21: Review Core Web Vitals data (needs 28 days to populate)
- [ ] D+30: Final migration review:
  - Compare 30-day post vs. 30-day pre traffic
  - Confirm all redirects are working
  - Close out any remaining issues
  - **Decision: Turn off Webflow** (if everything is stable)

---

## Quick Reference: Key URLs to Monitor

| URL | Why it matters | Pre-migration impressions (3m) |
|-----|---------------|-------------------------------|
| `/blog/how-to-find-someone-email-address-efficiently` | #1 keyword, highest value page | 98,000+ |
| `/blog/get-email-from-linkedin-profile` | Explosive growth, core use case | 62,283 |
| `/blog/whats-the-best-email-length-for-sales-outreach` | Zendesk backlinks (DR93) | 37,005 |
| `/blog/how-to-write-a-successful-cold-email` | Core topic, high volume | 34,057 |
| `/blog/linkedin-vs-email-which-performs-better-for-b2b-outreach` | High impressions | 25,186 |
| `/blog/the-ultimate-guide-to-linkedin-automation-boost-b2b-sales-in-2025` | 4.5K impr, 241 kws | 24,870 |
| `/blog/9-best-ai-agent-tools-for-sales` | High impressions | 20,299 |
| `/blog/ai-sales-tools-roi-key-metrics-to-track` | High impressions | 21,911 |
| `/blog/best-practices-for-links-in-your-emails` | Pos 8.5, good CTR | 18,159 |
| `/blog/apollo-alternatives` | 7.7K impr, almost page 1, high purchase intent | 16,902 |
| `/blog/455-email-spam-trigger-words-avoid-2018` | GoDaddy/Etsy/CampaignMonitor backlinks | 4,767 |
| `/blog/cold-email-stats-2018` | GoDaddy/OptinMonster backlinks | 39 (but high-DR backlinks) |
| `/blog/cold-email-illegal` | GitHub DR97 backlink | 5,417 |

---

## Appendix: Cloudflare Worker Request Flow

```
User request to overloop.com/blog/slug
        |
        v
  Cloudflare Edge
        |
        v
  Worker: Strip ?origin= param?
        |-- yes -> 301 redirect (clean URL)
        |-- no
        v
  Worker: tools.overloop.com?
        |-- yes -> 301 to overloop.com/tools/*
        |-- no
        v
  Worker: Strip trailing slash
        |
        v
  Worker: Path in BLOG_REDIRECTS?
        |-- yes -> 301 to target
        |-- no
        v
  Worker: Path in INTL_REDIRECTS?
        |-- yes -> 301 to EN target
        |-- no
        v
  Worker: Path matches /<lang>/blog/*?
        |-- yes -> 301 to /blog/* (catch-all)
        |-- no
        v
  Worker: Path starts with /blog, /versus, /tools, /playbooks, /templates?
        |-- yes -> Reverse proxy to sortlist.github.io/overloop-blog/*
        |--        Set X-Robots-Tag: index, follow
        |-- no
        v
  Worker: Pass through to origin (Webflow)
```
