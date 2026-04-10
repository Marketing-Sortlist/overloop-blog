/**
 * Overloop Blog Migration — Cloudflare Worker
 * Handles:
 * 1. 301 redirects for killed blog pages (238 URLs)
 * 2. 301 redirects from tools.overloop.com -> overloop.com/tools/
 * 3. Query parameter stripping (?origin=prospectio)
 * 4. Reverse proxy: overloop.com/blog/* -> GitHub Pages
 */

// Import redirect map (load from KV or hardcode from CSV)
// In production, load from Cloudflare KV store
const BLOG_REDIRECTS = {
  // Overloop vs X -> apollo-alternatives
  '/blog/overloop-vs-reply': '/blog/apollo-alternatives',
  '/blog/overloop-vs-saleshandy': '/blog/apollo-alternatives',
  '/blog/overloop-vs-hubspot': '/blog/apollo-alternatives',
  '/blog/overloop-vs-instantly': '/blog/apollo-alternatives',
  '/blog/overloop-vs-apollo': '/blog/apollo-alternatives',
  '/blog/overloop-vs-cleverly': '/blog/apollo-alternatives',

  // Listicle consolidations
  '/blog/9-best-ai-agent-tools-for-sales': '/blog/11-best-ai-bdr-tools',
  '/blog/10-best-ai-sales-assistant-tools': '/blog/best-ai-sales-tools',
  '/blog/9-best-ai-multichannel-outreach-tools': '/blog/9-best-ai-email-outreach-tools',
  '/blog/7-ai-sales-prospecting-tools-that-boost-lead-generation': '/blog/top-8-sales-prospecting-tools-for-small-business-teams',

  // Cold email consolidations
  '/blog/cold-email-software': '/blog/9-best-ai-email-outreach-tools',
  '/blog/best-cold-email-software': '/blog/9-best-ai-email-outreach-tools',
  '/blog/ultimate-cold-email-checklist': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/blog/6-cold-email-rules': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/blog/write-cold-email-make-hot': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',
  '/blog/5-deadly-email-prospecting-mistakes': '/blog/5-main-steps-for-an-effective-cold-email-marketing-strategy',

  // LinkedIn consolidations
  '/blog/linkedin-outreach': '/blog/8-best-ai-linkedin-outreach-tools',
  '/blog/linkedin-outreach-strategy': '/blog/8-best-ai-linkedin-outreach-tools',

  // Off-topic
  '/blog/10-favourite-sales-movies': '/blog',
  '/blog/team-retreat-important': '/blog',
  '/blog/unique-selling-proposition': '/blog',

  // ... Full map loaded from KV in production
};

// tools.overloop.com -> overloop.com/tools/
const TOOLS_REDIRECTS = {
  '/roi-calculator': '/tools/roi-calculator',
  '/infrastructure-calculator': '/tools/infrastructure-calculator',
  '/domain-health': '/tools/domain-health-checker',
  '/spam-checker': '/tools/spam-checker',
  '/prompt-builder': '/tools/prompt-builder',
};

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

      // Playbooks: tools.overloop.com/playbooks/* -> overloop.com/playbooks/*
      if (path.startsWith('/playbooks')) {
        return Response.redirect(`https://overloop.com${path}`, 301);
      }

      // Tools
      const toolTarget = TOOLS_REDIRECTS[path];
      if (toolTarget) {
        return Response.redirect(`https://overloop.com${toolTarget}`, 301);
      }

      // Default: redirect to overloop.com
      return Response.redirect('https://overloop.com/tools/', 301);
    }

    // 3. Handle blog 301 redirects
    const path = url.pathname.replace(/\/$/, '');
    const redirectTarget = BLOG_REDIRECTS[path];
    if (redirectTarget) {
      return Response.redirect(`https://overloop.com${redirectTarget}`, 301);
    }

    // 4. International page redirects (pattern-based)
    // /fr/blog/* -> /blog/* (EN equivalent)
    // /es/blog/* -> /blog/*
    // /it/blog/* -> /blog/*
    // /de/blog/* -> /blog/*
    const intlMatch = path.match(/^\/(fr|es|it|de)\/blog(\/.*)?$/);
    if (intlMatch) {
      const enPath = `/blog${intlMatch[2] || ''}`;
      return Response.redirect(`https://overloop.com${enPath}`, 301);
    }

    // 5. Reverse proxy to GitHub Pages (for surviving pages)
    // Only for /blog/*, /tools/*, /playbooks/*, /templates/*
    if (path.startsWith('/blog') || path.startsWith('/tools') || path.startsWith('/playbooks') || path.startsWith('/templates')) {
      const ghPagesUrl = `https://sortlist.github.io/overloop-blog${path}`;
      const response = await fetch(ghPagesUrl, {
        headers: request.headers,
      });

      // Clone response and set correct headers
      const newResponse = new Response(response.body, response);
      newResponse.headers.set('X-Robots-Tag', 'index, follow');
      return newResponse;
    }

    // 6. Pass through everything else
    return fetch(request);
  }
};
