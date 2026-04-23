#!/usr/bin/env node
// Generator script for Overloop playbook static pages
// Run: node _generate.js
// Creates 14 EN pages + 14 FR pages + 2 index pages = 30 files

const fs = require('fs');
const path = require('path');

// ============================================================
// NAV + FOOTER (from blog assets)
// ============================================================
const NAV = `<!-- Overloop Navigation -->
<nav class="nav">
    <div class="nav-inner">
        <a href="https://overloop.com" class="nav-logo">
            <img src="https://cdn.prod.website-files.com/6836b1fcfa0b25a3fed39db6/69d4cb02974de95cb4df5bd0_Logotype%20-%20Black.png" alt="Overloop AI" height="28">
        </a>

        <ul class="nav-links">
            <li class="nav-dropdown">
                <a href="https://overloop.com/features" class="nav-dropdown-trigger">Features</a>
                <div class="nav-dropdown-menu nav-dropdown-wide">
                    <ul class="nav-dropdown-content nav-features-grid">
                        <li><a href="https://overloop.com/f/linkedin-automation">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                            <div><strong>LinkedIn Automation</strong><span class="dropdown-desc">Automate outreach without risking your account</span></div>
                        </a></li>
                        <li><a href="https://overloop.com/f/email-verification">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                            <div><strong>Email Bulk Verification</strong><span class="dropdown-desc">Verify addresses, improve deliverability</span></div>
                        </a></li>
                        <li><a href="https://overloop.com/f/b2b-contact-database">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                            <div><strong>B2B Contact Database</strong><span class="dropdown-desc">450M+ verified contacts</span></div>
                        </a></li>
                        <li><a href="https://overloop.com/f/multi-channel-outreach">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><polyline points="22 12 16 12 14 15 10 9 8 12 2 12"/></svg>
                            <div><strong>Multi-Channel Prospecting</strong><span class="dropdown-desc">Email + LinkedIn in one sequence</span></div>
                        </a></li>
                    </ul>
                </div>
            </li>
            <li><a href="https://overloop.com/pricing">Pricing</a></li>
            <li class="nav-dropdown">
                <a href="/blog" class="nav-dropdown-trigger">Resources</a>
                <div class="nav-dropdown-menu nav-dropdown-wide">
                    <ul class="nav-dropdown-content nav-resources-grid">
                        <li><a href="/blog">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                            <div><strong>Blog</strong><span class="dropdown-desc">Outbound strategies and guides</span></div>
                        </a></li>
                        <li><a href="/versus">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                            <div><strong>Versus</strong><span class="dropdown-desc">Tool-by-tool comparisons</span></div>
                        </a></li>
                        <li><a href="https://tools.overloop.com/spam-checker">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                            <div><strong>Spam Checker</strong><span class="dropdown-desc">Free email analysis tool</span></div>
                        </a></li>
                        <li><a href="https://tools.overloop.com/roi-calculator">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="12" y2="14"/></svg>
                            <div><strong>ROI Calculator</strong><span class="dropdown-desc">Estimate your outbound ROI</span></div>
                        </a></li>
                        <li><a href="https://tools.overloop.com/domain-health">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                            <div><strong>Domain Health</strong><span class="dropdown-desc">Check SPF, DKIM, DMARC</span></div>
                        </a></li>
                        <li><a href="/playbooks">
                            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7C3AED" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                            <div><strong>Playbooks</strong><span class="dropdown-desc">Industry-specific strategies</span></div>
                        </a></li>
                    </ul>
                </div>
            </li>
        </ul>

        <div class="nav-cta">
            <a href="https://app.overloop.ai/session/signup" class="btn-ghost">Sign up</a>
            <a href="https://app.overloop.ai/session/login" class="btn-login">Login</a>
            <a href="https://overloop.com/book-demo" class="btn-primary"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>Book a demo</a>
        </div>

        <button class="nav-mobile-toggle" aria-label="Menu">
            <span></span><span></span><span></span>
        </button>
    </div>
<script>
document.querySelector('.nav-mobile-toggle').addEventListener('click', function() {
    document.querySelector('.nav-links').classList.toggle('nav-open');
    document.querySelector('.nav-cta').classList.toggle('nav-open');
});
</script>
</nav>`;

const FOOTER = `<!-- Overloop Footer -->
<footer class="footer">
    <div class="footer-inner">
        <div class="footer-grid">
            <div class="footer-brand">
                <img src="https://cdn.prod.website-files.com/6836b1fcfa0b25a3fed39db6/69cd287353b6d46f18b30305_Logotype%20-%20Color.png" alt="Overloop" height="24" style="filter: brightness(0) invert(1);">
                <p>AI-powered outbound sales platform. Find prospects, write personalized emails, and book meetings on autopilot.</p>
            </div>
            <div class="footer-col">
                <h4>Platform</h4>
                <a href="/features">Features</a>
                <a href="/pricing">Pricing</a>
                <a href="https://app.overloop.ai/session/signup">Start Free Trial</a>
                <a href="/book-demo">Book a Demo</a>
            </div>
            <div class="footer-col">
                <h4>Resources</h4>
                <a href="/blog">Blog</a>
                <a href="/playbooks">Playbooks</a>
                <a href="/tools/spam-checker">Spam Checker</a>
                <a href="/tools/roi-calculator">ROI Calculator</a>
                <a href="/tools/domain-health-checker">Domain Health</a>
            </div>
            <div class="footer-col">
                <h4>Company</h4>
                <a href="/about">About</a>
                <a href="/testimonials">Testimonials</a>
                <a href="mailto:hello@overloop.com">Contact</a>
                <a href="/careers">Careers</a>
            </div>
            <div class="footer-col">
                <h4>Legal</h4>
                <a href="/terms">Terms</a>
                <a href="/privacy">Privacy</a>
                <a href="/gdpr">GDPR</a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 Overloop AI. Rue des Peres Blancs 4, 1040 Brussels, Belgium.</span>
            <div>
                <a href="https://www.linkedin.com/company/overloop-ai/">LinkedIn</a>
                <a href="https://www.youtube.com/@overloop-ai">YouTube</a>
            </div>
        </div>
    </div>
</footer>`;

// ============================================================
// EN PLAYBOOKS DATA
// ============================================================
const EN_PLAYBOOKS = [
{id:'marketing-agency',slug:'marketing-agencies',cat:'Agencies',title:'Marketing Agencies',desc:'Sell outbound as a service. White-label Overloop, charge 3-4x, keep the margin.',
  stats:{open:'38%',reply:'5.1%',meetings:'12/mo'},
  icp:[{l:'Titles',v:'CEO, CMO, Head of Growth'},{l:'Company size',v:'10-200 employees'},{l:'Industries to target',v:'SaaS, e-commerce, fintech'},{l:'Trigger',v:'Hiring for marketing roles'},{l:'Budget signal',v:'Running paid ads (visible in ads library)'},{l:'Geography',v:'Tier 1 markets (US, UK, EU)'}],
  angles:[
    {name:'White-label pitch',desc:'Offer outbound as a new service line. You handle the ops, they get the meetings.',why:'Agencies always want new revenue streams. Outbound has 70%+ margins when white-labeled.'},
    {name:'Competitor comparison',desc:'"3 of your competitors already offer outbound. Here\'s the playbook they use."',why:'FOMO + concrete proof. Nobody wants to be the agency that doesn\'t offer what competitors do.'},
    {name:'Client results angle',desc:'Lead with a specific result: "We helped [agency] book 18 meetings/mo for their SaaS clients."',why:'Agencies sell results. Show them the result, they\'ll figure out how to sell it.'}
  ],
  templates:[
    {name:'White-label intro',score:91,subject:"Your clients' outbound",body:"Hi {{firstName}},\n\nI run Overloop. We work with agencies like {{company}} who want to add outbound as a service for their clients.\n\nThe model: you white-label our platform, charge your clients 3-4x what you pay us, and we handle the infrastructure.\n\nThree of your competitors already do this. Happy to share the playbook.\n\nOpen to a quick call?\n\nJohn"},
    {name:'Revenue angle',score:88,subject:'New revenue stream for {{company}}',body:"Hi {{firstName}},\n\nMost agencies I talk to are stuck at the same revenue ceiling: retainers + project work. Adding outbound as a service changes the math.\n\nOur agency partners charge $2,500-4,000/mo per client for outbound. Their cost: $800/mo. That's 70% margin on a recurring service.\n\nWant me to walk through how it works?\n\nJohn"},
    {name:'Case study',score:89,subject:'How [Agency X] added $40K MRR',body:"Hi {{firstName}},\n\nA 15-person agency like {{company}} added $40K in monthly recurring revenue last quarter by offering cold email to their existing clients.\n\nThey didn't hire anyone. They white-labeled our platform, created 3 service tiers, and upsold their current book of business.\n\n6 clients signed in the first month.\n\nWorth 15 min to see if this fits {{company}}?\n\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'White-label pitch',desc:'Lead with the model. Short, direct.'},
    {day:'Day 2',ch:'linkedin',action:'View profile + connect',desc:'Personalized note: "Saw you run an agency -- sent you something on outbound as a service."'},
    {day:'Day 5',ch:'email',action:'Revenue angle',desc:'Different angle. Focus on the 70% margin opportunity.'},
    {day:'Day 7',ch:'linkedin',action:'Engage with their content',desc:'Like or comment on a recent post. Build familiarity before the next email.'},
    {day:'Day 10',ch:'email',action:'Case study',desc:'Social proof. Specific numbers from a similar agency.'},
    {day:'Day 12',ch:'linkedin',action:'Send InMail or message',desc:'"Hey {{firstName}}, did you get a chance to look at the outbound-as-a-service model? Happy to walk through the economics."'},
    {day:'Day 15',ch:'email',action:'Breakup',desc:'"Should I close your file?" Direct and honest.'}
  ],
  benchmarks:{open:'38%',reply:'5.1%',meeting:'2.1%',close:'25%'},
  objections:[
    {q:'"We already do outbound internally"',a:'Ask: <em>how many meetings per client per month?</em> Most agencies doing it internally manage 3-5. With a dedicated platform, their clients get 15-20. It\'s not about doing outbound -- it\'s about doing it at scale.'},
    {q:'"Our clients wouldn\'t pay for outbound"',a:'Reframe: <em>your clients are already paying for leads</em> through ads, SEO, events. Outbound is just another channel -- and it\'s the only one with predictable unit economics. Start with one client as a pilot.'},
    {q:'"We don\'t have the expertise"',a:'That\'s the point of white-labeling. <em>You don\'t need to be an outbound expert.</em> We handle the infrastructure, deliverability, and optimization. Your team focuses on the client relationship and messaging.'}
  ]
},
{id:'saas',slug:'saas-b2b',cat:'Tech',title:'SaaS B2B',desc:'The highest-ROI outbound vertical. Long LTV, clear ICP, measurable results.',
  stats:{open:'45%',reply:'3.2%',meetings:'18/mo'},
  icp:[{l:'Titles',v:'VP Sales, Head of Growth, CRO, CEO (< 50 people)'},{l:'Company size',v:'20-500 employees'},{l:'Trigger',v:'Recent funding, hiring SDRs, new leadership'},{l:'Tech stack',v:'Using competitor tools or adjacent products'},{l:'Budget signal',v:'Series A+ or $2M+ ARR'},{l:'Geography',v:'US, UK, DACH, Nordics'}],
  angles:[
    {name:'Hiring trigger',desc:'"I noticed you\'re hiring an SDR. Cold email can fill the pipeline gap while you recruit."',why:'Hiring takes 3 months. Outbound takes 3 weeks. The timing argument is irresistible.'},
    {name:'Post-funding',desc:'"Congrats on the raise. The pressure to hit pipeline targets just went up."',why:'Newly funded = budget available + board pressure. The window of opportunity is 90 days.'},
    {name:'Competitor displacement',desc:'"Companies like [competitor\'s customer] switched from [competitor] because [specific reason]."',why:'SaaS buyers are always evaluating. Give them a reason and they\'ll take the meeting.'}
  ],
  templates:[
    {name:'Hiring trigger',score:89,subject:'Quick question about {{company}}',body:"Hi {{firstName}},\n\nI noticed {{company}} is hiring a Head of Sales. Usually means outbound is becoming a priority.\n\nWe help B2B teams book 15-20 qualified meetings per month through cold email, without hiring an SDR.\n\nCompanies like Datadog and Notion use this approach to fill pipeline while keeping headcount lean.\n\nWorth a 15-min call this week?\n\nBest,\nJohn"},
    {name:'Post-funding',score:87,subject:'{{firstName}}, quick thought',body:"Hi {{firstName}},\n\nSaw that {{company}} just raised a Series B. Congrats.\n\nUsually after a raise, the pressure to hit pipeline targets goes up fast. Hiring SDRs takes 3 months. Cold email can fill the gap in 3 weeks.\n\nWe run the outbound engine for 200+ B2B SaaS companies. Average: 18 qualified meetings per month, $0 in ad spend.\n\nWould it make sense to chat for 15 min this week?\n\nJohn"},
    {name:'Pain point',score:90,subject:'{{company}} pipeline',body:"Hi {{firstName}},\n\nMost SaaS companies I talk to have the same problem after Series A: the CEO is still the best salesperson, and the pipeline depends on inbound that doesn't scale.\n\nWe help fix that. Cold email, fully automated, 15-20 meetings/mo. No SDR hire needed.\n\nIs that a problem {{company}} is dealing with right now?\n\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Hiring trigger or post-funding',desc:'Pick the most relevant trigger for this prospect.'},
    {day:'Day 2',ch:'linkedin',action:'View profile + connect',desc:'Personalized note referencing the trigger. No pitch.'},
    {day:'Day 5',ch:'email',action:'Pain point angle',desc:'Different angle. Focus on the problem, not your product.'},
    {day:'Day 7',ch:'linkedin',action:'Comment on their post',desc:'Genuine engagement. Build familiarity before next touch.'},
    {day:'Day 10',ch:'email',action:'Social proof',desc:'Case study from a similar company. Specific numbers.'},
    {day:'Day 13',ch:'linkedin',action:'Send message',desc:'"Saw you\'re scaling the sales team -- the case study I sent might be relevant. Worth 15 min?"'},
    {day:'Day 18',ch:'email',action:'Breakup',desc:'"Should I close your file?" Clean and direct.'}
  ],
  benchmarks:{open:'45%',reply:'3.2%',meeting:'1.2%',close:'20%'},
  objections:[
    {q:'"We already have an outbound team"',a:'Perfect. Ask: <em>what\'s their meeting rate?</em> Most SDR teams book 8-12 meetings/mo. AI-powered outbound books 18-20. It\'s not about replacing the team -- it\'s about multiplying their output.'},
    {q:'"Cold email doesn\'t work in our market"',a:'Ask: <em>which market?</em> Then share a specific example. We have customers in fintech, healthtech, devtools, HR tech, and martech. Cold email works when the targeting is right and the copy is relevant.'},
    {q:'"We\'re focused on inbound right now"',a:'Inbound is great for brand. But it <em>doesn\'t scale linearly</em>. Outbound does. The best companies run both. Outbound fills the pipeline while inbound builds the brand.'}
  ]
},
{id:'digital-agency',slug:'digital-web-agencies',cat:'Agencies',title:'Digital & Web Agencies',desc:'Sell to companies that need websites, apps, or digital transformation. High deal values, long cycles.',
  stats:{open:'36%',reply:'4.8%',meetings:'10/mo'},
  icp:[{l:'Titles',v:'CEO, CTO, VP Marketing, Digital Director'},{l:'Company size',v:'50-1000 employees'},{l:'Trigger',v:'Outdated website, rebrand, new product launch'},{l:'Industry focus',v:'Professional services, manufacturing, healthcare'},{l:'Budget signal',v:'Website older than 3 years'},{l:'Geography',v:'Local/regional focus'}],
  angles:[
    {name:'Website audit',desc:'"I looked at {{company}}.com. A few things stood out that might be costing you conversions."',why:'Specific observation = credibility. Nobody ignores an email that says their website has problems.'},
    {name:'Competitor comparison',desc:'"Your competitor just relaunched their site. Here\'s what they changed and why it matters."',why:'Competitive pressure + specific intel. The prospect has to click.'},
    {name:'Industry benchmark',desc:'"The average conversion rate in [industry] is 3.2%. Most sites we audit are at 1.5%."',why:'Data-driven. Makes the prospect wonder where they stand.'}
  ],
  templates:[
    {name:'Website audit opener',score:88,subject:'{{company}}.com',body:"Hi {{firstName}},\n\nI took a look at {{company}}.com. Two things stood out:\n\n1. Your mobile load time is 4.8s (Google penalizes anything over 2.5s)\n2. Your main CTA is below the fold on every page\n\nBoth are fixable in a week and would likely improve your conversion rate by 20-30%.\n\nWe've done this for 40+ companies in [industry]. Want me to send the full audit?\n\nBest,\nSarah"},
    {name:'Competitor move',score:86,subject:'Did you see what [competitor] just did?',body:"Hi {{firstName}},\n\nI noticed [competitor] just relaunched their website with a new booking flow and localized landing pages for each market.\n\nIn our experience, companies that fall behind on web experience lose 15-20% of their pipeline to competitors who make it easier to buy.\n\nIs refreshing {{company}}'s site on your radar for this year?\n\nSarah"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Website audit',desc:'Specific, researched observation about their site.'},
    {day:'Day 2',ch:'linkedin',action:'View profile + connect',desc:'"I sent you a quick audit of {{company}}.com -- thought you\'d find it useful."'},
    {day:'Day 5',ch:'linkedin',action:'Like/comment on post',desc:'Engage with their content. Show you follow their space.'},
    {day:'Day 7',ch:'email',action:'Competitor move',desc:'Different trigger. Competitive pressure.'},
    {day:'Day 11',ch:'linkedin',action:'Send message',desc:'"Did you get a chance to review the site audit? Happy to walk through the findings."'},
    {day:'Day 14',ch:'email',action:'Case study',desc:'Similar company, specific results, before/after.'},
    {day:'Day 21',ch:'email',action:'Breakup',desc:'Short and clean.'}
  ],
  benchmarks:{open:'36%',reply:'4.8%',meeting:'1.8%',close:'22%'},
  objections:[
    {q:'"We\'re happy with our current agency"',a:'Great. Ask: <em>when was the last time they audited your site performance?</em> Most agencies do the build and move on. We focus on ongoing optimization. Different model.'},
    {q:'"We just redid our website"',a:'Perfect timing. Ask: <em>are you tracking conversion rates?</em> Most new sites launch without proper tracking. We can help set up the measurement framework so you know what\'s working.'}
  ]
},
{id:'seo-agency',slug:'seo-agencies',cat:'Agencies',title:'SEO Agencies',desc:'Sell to companies struggling with organic traffic. Data-driven angles, clear ROI arguments.',
  stats:{open:'40%',reply:'4.2%',meetings:'11/mo'},
  icp:[{l:'Titles',v:'CEO, Head of Marketing, Content Director'},{l:'Company size',v:'20-500 employees'},{l:'Trigger',v:'Traffic drop, algorithm update, competitor ranking'},{l:'Budget signal',v:'Running Google Ads (buying traffic they could earn)'},{l:'Industry focus',v:'SaaS, e-commerce, professional services'},{l:'Geography',v:'English-speaking markets'}],
  angles:[
    {name:'Traffic loss',desc:'"I noticed {{company}} lost 30% organic traffic after the March update. Here\'s likely why."',why:'Specific, data-driven, urgent. They\'re already worried about it.'},
    {name:'Competitor ranking',desc:'"Your competitor ranks #1 for [keyword]. They get ~2,400 visits/mo from it. You\'re on page 3."',why:'Quantified competitive gap. Hard to ignore when you see the numbers.'},
    {name:'Paid-to-organic',desc:'"You\'re spending $X/mo on Google Ads for keywords you could rank for organically."',why:'Direct cost savings argument. CFO-friendly.'}
  ],
  templates:[
    {name:'Traffic drop',score:87,subject:'{{company}} organic traffic',body:"Hi {{firstName}},\n\nI ran a quick analysis on {{company}}.com. Looks like you lost about 30% organic traffic after the last Google core update.\n\nThe likely cause: thin content on your top 5 pages and missing schema markup on your service pages.\n\nWe fixed the same issue for a SaaS company your size last month. They recovered 85% of lost traffic in 6 weeks.\n\nWant me to send the detailed audit?\n\nBest,\nSarah"},
    {name:'Competitor gap',score:89,subject:'{{company}} vs [competitor]',body:"Hi {{firstName}},\n\nI compared {{company}}'s SEO to [competitor]. Three things stood out:\n\n1. They rank for 340 keywords you don't\n2. Their domain authority is 12 points higher\n3. They publish 4x more content per month\n\nThe gap is closable in 6-9 months with the right strategy. We've done it 50+ times.\n\nWorth a 15-min call to review the data?\n\nSarah"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Traffic drop or competitor gap',desc:'Data-driven opener with specific numbers.'},
    {day:'Day 2',ch:'linkedin',action:'Connect + view profile',desc:'"I ran a quick SEO comparison for {{company}} -- sent it over email."'},
    {day:'Day 5',ch:'linkedin',action:'Share SEO insight on their post',desc:'Comment with a genuine SEO observation. Build credibility.'},
    {day:'Day 6',ch:'email',action:'Paid-to-organic angle',desc:'Cost savings argument.'},
    {day:'Day 10',ch:'linkedin',action:'Send message',desc:'"Quick question -- are you tracking the impact of the latest core update on {{company}}?"'},
    {day:'Day 12',ch:'email',action:'Case study with timeline',desc:'"Month 1: audit. Month 3: content live. Month 6: traffic recovered."'},
    {day:'Day 18',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'40%',reply:'4.2%',meeting:'1.6%',close:'23%'},
  objections:[
    {q:'"SEO takes too long"',a:'It does take 3-6 months for full results. But <em>the alternative is paying for ads forever</em>. SEO compounds. Ads don\'t. In month 12, SEO traffic is free. Ad traffic costs the same as month 1.'},
    {q:'"We tried SEO before and it didn\'t work"',a:'Ask what they tried. 90% of the time it was <em>content without strategy</em>. We start with keyword research, competitor analysis, and technical audit before writing a single word.'}
  ]
},
{id:'pr-agency',slug:'pr-communications',cat:'Agencies',title:'PR & Communications',desc:'Sell media coverage and reputation management. Relationship-heavy, results hard to measure, retainer model.',
  stats:{open:'37%',reply:'4.6%',meetings:'9/mo'},
  icp:[{l:'Titles',v:'CEO, VP Marketing, Head of Comms'},{l:'Company size',v:'50-500 employees'},{l:'Trigger',v:'Product launch, funding, crisis, rebrand'},{l:'Budget signal',v:'Hiring comms roles, active on social'},{l:'Industry focus',v:'Tech, consumer brands, healthcare'},{l:'Geography',v:'Tier 1 media markets'}],
  angles:[
    {name:'Launch timing',desc:'"{{company}} just raised. The press window is 2-3 weeks. After that, nobody cares."',why:'Urgency tied to a real event. PR has a shelf life -- they know this.'},
    {name:'Competitor coverage',desc:'"Your competitor got covered in TechCrunch last week. Here\'s the angle they used."',why:'FOMO + actionable intel. Nobody wants their competitor in the press and not them.'},
    {name:'Measurement gap',desc:'"Most PR agencies can\'t tell you the ROI of a placement. We can."',why:'Measurement is PR\'s biggest weakness. If you can solve it, you win the meeting.'}
  ],
  templates:[
    {name:'Post-funding PR',score:88,subject:'{{company}} press strategy',body:"Hi {{firstName}},\n\nCongrats on the raise. You have a 2-3 week window where journalists will care about {{company}}. After that, you're just another funded startup.\n\nWe help companies turn funding announcements into 5-8 media placements in the first month. Not vanity press -- outlets your buyers actually read.\n\nWant to see the playbook we used for [similar company]?\n\nBest,\nJohn"},
    {name:'Competitor angle',score:87,subject:'Did you see the [competitor] piece?',body:"Hi {{firstName}},\n\n[Competitor] landed a feature in TechCrunch last week. The angle: \"how [their product] is changing [industry].\"\n\nThe journalist who wrote it covers your space too. We have a relationship with her and a story angle that positions {{company}} as the counter-narrative.\n\nWorth a quick call to discuss the pitch?\n\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Post-funding or competitor angle',desc:'Timely, specific, tied to a real event.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'"Sent you a note on {{company}}\'s press timing."'},
    {day:'Day 5',ch:'linkedin',action:'Engage with their content',desc:'Comment on a recent company announcement.'},
    {day:'Day 6',ch:'email',action:'Measurement angle',desc:'Position PR ROI as your differentiator.'},
    {day:'Day 10',ch:'linkedin',action:'Send message',desc:'"The press window is closing. Want to chat this week?"'},
    {day:'Day 14',ch:'email',action:'Case study',desc:'Similar company, specific placements + pipeline impact.'},
    {day:'Day 20',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'37%',reply:'4.6%',meeting:'1.8%',close:'21%'},
  objections:[
    {q:'"We already have a PR agency"',a:'Ask: <em>how many qualified leads came from their last campaign?</em> If they can\'t answer, that\'s the problem we solve.'},
    {q:'"PR doesn\'t drive pipeline directly"',a:'It does when you <em>choose the right outlets and track attribution</em>. We measure PR by meetings sourced, not clip count.'}
  ]
},
{id:'branding-agency',slug:'branding-design',cat:'Agencies',title:'Branding & Design',desc:'Sell brand strategy and visual identity. High deal values, emotional decisions, portfolio-driven.',
  stats:{open:'35%',reply:'4.2%',meetings:'7/mo'},
  icp:[{l:'Titles',v:'CEO, CMO, VP Brand, Creative Director'},{l:'Company size',v:'20-500 employees'},{l:'Trigger',v:'Rebrand, new market, M&A, Series B+'},{l:'Budget signal',v:'Outdated brand (3+ years), inconsistent presence'},{l:'Industry focus',v:'Tech, consumer, professional services'},{l:'Geography',v:'Design-forward markets (US, UK, Nordics)'}],
  angles:[
    {name:'Brand audit',desc:'"I looked at {{company}}\'s brand across 5 touchpoints. There are 3 inconsistencies that might be confusing your buyers."',why:'Specific, researched, non-threatening. You\'re not saying their brand is bad -- you\'re saying it\'s inconsistent.'},
    {name:'Growth inflection',desc:'"You just raised Series B. Your brand was built for a 10-person startup. Now you\'re selling to enterprise."',why:'Post-funding brands often lag behind the company\'s evolution. This observation resonates.'},
    {name:'Competitor design comparison',desc:'"Your competitor just rebranded. Here\'s what changed and what it signals about their positioning."',why:'Visual comparison is powerful. CEOs care about looking worse than competitors.'}
  ],
  templates:[
    {name:'Brand audit opener',score:89,subject:'{{company}} brand consistency',body:"Hi {{firstName}},\n\nI did a quick audit of {{company}}'s brand across website, LinkedIn, pitch deck, and product screenshots. Three things stood out:\n\n1. The color palette shifts between your site and your product\n2. Your LinkedIn header still references an old tagline\n3. Your website says one thing, your pitch deck says another\n\nSmall things, but they add up. Buyers notice inconsistency even if they can't articulate it.\n\nWe fixed this for a SaaS company your size in 6 weeks. Want to see the before/after?\n\nBest,\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Brand audit',desc:'Specific observations across touchpoints.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'"Sent you a quick brand audit for {{company}}."'},
    {day:'Day 5',ch:'linkedin',action:'Share design insight',desc:'Comment on a branding trend post. Show you think about this space.'},
    {day:'Day 7',ch:'email',action:'Growth inflection angle',desc:'Connect their stage to their brand maturity.'},
    {day:'Day 11',ch:'linkedin',action:'Send message',desc:'"The brand gap usually widens after Series B. Worth a chat?"'},
    {day:'Day 14',ch:'email',action:'Before/after case study',desc:'Visual proof. Side-by-side of a rebrand you did.'},
    {day:'Day 20',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'35%',reply:'4.2%',meeting:'1.5%',close:'24%'},
  objections:[
    {q:'"We\'re not ready for a rebrand"',a:'Rebranding is the nuclear option. We start with <em>brand alignment</em> -- making what you already have consistent. That\'s a 4-6 week project, not a 6-month overhaul.'},
    {q:'"We have an in-house designer"',a:'Perfect. We work alongside in-house teams. <em>We do strategy and direction, they do execution.</em> Most in-house designers are waiting for someone to give them a brief.'}
  ]
},
{id:'social-agency',slug:'social-media',cat:'Agencies',title:'Social Media',desc:'Sell social strategy and content creation. High churn market, creative-driven, results-focused.',
  stats:{open:'39%',reply:'5.0%',meetings:'11/mo'},
  icp:[{l:'Titles',v:'Head of Marketing, CMO, Social Media Manager'},{l:'Company size',v:'20-200 employees'},{l:'Trigger',v:'Inconsistent posting, low engagement, competitor going viral'},{l:'Budget signal',v:'Active ad spend, hiring for social roles'},{l:'Industry focus',v:'DTC, food & bev, fashion, tech'},{l:'Geography',v:'US, UK, EU'}],
  angles:[
    {name:'Engagement audit',desc:'"Your last 20 posts averaged 0.3% engagement. Industry average is 1.2%. Here\'s why."',why:'Specific data they can verify. Hard to argue with numbers.'},
    {name:'Competitor viral moment',desc:'"Your competitor\'s last reel hit 500K views. Here\'s the format they used."',why:'Competitive jealousy + actionable playbook = irresistible.'},
    {name:'Content-to-pipeline gap',desc:'"You post 4x/week but your pipeline is still driven by ads. Social should be sourcing 20% of leads."',why:'Connects vanity metrics (posts) to business metrics (pipeline). CEO language.'}
  ],
  templates:[
    {name:'Engagement audit',score:90,subject:'{{company}} social engagement',body:"Hi {{firstName}},\n\nI analyzed {{company}}'s last 30 days on LinkedIn and Instagram. A few things stood out:\n\n- Average engagement: 0.3% (industry avg: 1.2%)\n- Posting frequency is good (4x/week) but format mix is off -- 80% static images, 0% video\n- Best performing post: the one with a real person in it, not a graphic\n\nThe fix isn't posting more. It's posting differently.\n\nWant me to share what's working for similar brands right now?\n\nBest,\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Engagement audit',desc:'Specific numbers from their social presence.'},
    {day:'Day 2',ch:'linkedin',action:'Connect + engage',desc:'Like their latest post. Connect with a note referencing it.'},
    {day:'Day 4',ch:'linkedin',action:'Comment on their content',desc:'Leave a substantive comment. Show you actually follow their brand.'},
    {day:'Day 6',ch:'email',action:'Competitor viral moment',desc:'Share a specific example they can learn from.'},
    {day:'Day 9',ch:'linkedin',action:'Send message',desc:'"Saw your latest campaign. Have a few ideas on the format mix."'},
    {day:'Day 13',ch:'email',action:'Case study',desc:'Similar brand, specific engagement lift.'},
    {day:'Day 18',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'39%',reply:'5.0%',meeting:'2.0%',close:'20%'},
  objections:[
    {q:'"We manage social in-house"',a:'Most companies do. The question is: <em>is it generating pipeline or just impressions?</em> We turn social from a brand tax into a lead source.'},
    {q:'"Social doesn\'t drive B2B sales"',a:'LinkedIn drove $2.3B in B2B leads last year. <em>Social works in B2B when the content is built for buyers, not marketers.</em>'}
  ]
},
{id:'performance-agency',slug:'performance-paid-media',cat:'Agencies',title:'Performance & Paid Media',desc:'Sell ad management and CRO. Data-driven buyers, ROAS-obsessed, easy to prove value.',
  stats:{open:'36%',reply:'4.4%',meetings:'10/mo'},
  icp:[{l:'Titles',v:'Head of Growth, CMO, CEO (DTC), E-com Director'},{l:'Company size',v:'$1M-50M revenue'},{l:'Trigger',v:'Rising CAC, scaling ad spend, new markets'},{l:'Budget signal',v:'$10K+/mo in Meta/Google ads'},{l:'Industry focus',v:'DTC, e-commerce, SaaS, apps'},{l:'Geography',v:'US, UK, EU, AU'}],
  angles:[
    {name:'CAC trend',desc:'"Your Meta CPM went up 40% this year. Your ROAS probably went down. There\'s a fix."',why:'Every performance marketer feels CPM inflation. You\'re naming their pain.'},
    {name:'Ad library audit',desc:'"I checked your Meta Ad Library. You have 12 active creatives. Only 2 have been running more than 7 days."',why:'Specific, verifiable, shows you did the work. They know creative fatigue is a problem.'},
    {name:'Channel diversification',desc:'"80% of your budget is in Meta. If they change the algorithm tomorrow, you lose 80% of pipeline."',why:'Concentration risk is real. CFOs especially respond to this argument.'}
  ],
  templates:[
    {name:'CAC trend',score:87,subject:'{{company}} ad performance',body:"Hi {{firstName}},\n\nMeta CPMs in your vertical went up 40% this year. For most companies that means ROAS is down 20-30% on the same spend.\n\nWe help brands like {{company}} get ROAS back up without increasing budget -- through creative testing, audience optimization, and channel diversification.\n\nLast quarter, we improved ROAS by 35% for a DTC brand your size.\n\nWorth a 15-min review of your current setup?\n\nBest,\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'CAC trend or ad library audit',desc:'Lead with data they can verify.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'"Sent you a note on {{company}}\'s ad performance."'},
    {day:'Day 5',ch:'linkedin',action:'Share industry benchmark',desc:'Post or DM a relevant CPM/ROAS trend for their vertical.'},
    {day:'Day 6',ch:'email',action:'Channel diversification angle',desc:'Risk argument. CFO-friendly.'},
    {day:'Day 10',ch:'linkedin',action:'Send message',desc:'"Quick q -- what % of your pipeline comes from Meta vs other channels?"'},
    {day:'Day 13',ch:'email',action:'ROAS case study',desc:'Similar brand, specific ROAS improvement.'},
    {day:'Day 18',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'36%',reply:'4.4%',meeting:'1.7%',close:'22%'},
  objections:[
    {q:'"We manage ads in-house"',a:'Most companies do. But <em>managing and optimizing aren\'t the same thing</em>. We audit 100+ accounts per year. The patterns we see across all of them = an unfair advantage for each one.'},
    {q:'"Our ROAS is fine"',a:'Fine compared to what? <em>Industry benchmarks shift every quarter.</em> "Fine" 6 months ago might be "below average" today. Happy to run a free benchmark comparison.'}
  ]
},
{id:'content-agency',slug:'content-marketing',cat:'Agencies',title:'Content Marketing',desc:'Sell content strategy, SEO writing, and thought leadership. Long cycles, hard to prove ROI, retainer model.',
  stats:{open:'38%',reply:'4.3%',meetings:'9/mo'},
  icp:[{l:'Titles',v:'Head of Marketing, VP Content, CMO, CEO (startups)'},{l:'Company size',v:'20-500 employees'},{l:'Trigger',v:'Blog with no traffic, content team of 1, SEO decline'},{l:'Budget signal',v:'Active blog but low organic traffic'},{l:'Industry focus',v:'SaaS, professional services, fintech'},{l:'Geography',v:'English-speaking markets'}],
  angles:[
    {name:'Traffic audit',desc:'"Your blog has 150 posts but only 3 bring organic traffic. The other 147 are invisible to Google."',why:'Specific, surprising, and slightly painful. They\'ll want to know which 3.'},
    {name:'Content ROI gap',desc:'"You\'re publishing 4 posts/week but can you tie a single one to a closed deal?"',why:'Content teams rarely track to revenue. Pointing this out signals you think differently.'},
    {name:'Competitor content comparison',desc:'"Your competitor publishes half as much as you but gets 3x the organic traffic. Here\'s why."',why:'Quality vs quantity. Most content teams are stuck on the hamster wheel.'}
  ],
  templates:[
    {name:'Traffic audit',score:89,subject:'{{company}} blog performance',body:"Hi {{firstName}},\n\nI ran a quick analysis on {{company}}'s blog. 150+ published posts, but only 3 pages drive meaningful organic traffic.\n\nThe other 147 are essentially invisible -- no rankings, no clicks, no leads. That's a lot of writing with no return.\n\nThe fix isn't more content. It's a different content strategy: fewer posts, higher quality, built around keywords with actual search volume.\n\nWe did this for a SaaS company your size. They went from 2,000 to 18,000 organic visits/mo in 5 months. With fewer posts.\n\nWant to see the strategy?\n\nBest,\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Traffic audit',desc:'Specific numbers from their blog/site.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'"Ran a content analysis for {{company}}. Sent it over email."'},
    {day:'Day 4',ch:'linkedin',action:'Engage with their content',desc:'Leave a thoughtful comment on their blog or LinkedIn article.'},
    {day:'Day 6',ch:'email',action:'Content ROI gap',desc:'Connect content to revenue. Different angle.'},
    {day:'Day 9',ch:'linkedin',action:'Share a relevant insight',desc:'DM a content strategy tip relevant to their industry.'},
    {day:'Day 12',ch:'email',action:'Competitor comparison',desc:'Show them the quality vs quantity gap.'},
    {day:'Day 18',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'38%',reply:'4.3%',meeting:'1.6%',close:'23%'},
  objections:[
    {q:'"We already have a content team"',a:'Content teams produce content. <em>Content strategists produce results.</em> We don\'t replace your writers -- we give them the right briefs so every post has a shot at ranking.'},
    {q:'"Content takes too long to show results"',a:'Bad content takes long. <em>Strategic content shows traffic within 8-12 weeks</em> because we target keywords your site can actually rank for, not aspirational ones.'}
  ]
},
{id:'dev-agency',slug:'dev-product-studios',cat:'Agencies',title:'Dev & Product Studios',desc:'Sell custom development, MVP builds, and product consulting. Technical buyers, long sales cycles, high deal values.',
  stats:{open:'34%',reply:'3.8%',meetings:'6/mo'},
  icp:[{l:'Titles',v:'CTO, VP Engineering, CEO (non-technical), Product Director'},{l:'Company size',v:'20-200 employees'},{l:'Trigger',v:'Funding, product rewrite, legacy migration, new product line'},{l:'Budget signal',v:'Job postings for senior devs, tech debt discussions'},{l:'Industry focus',v:'SaaS, fintech, healthtech, marketplace'},{l:'Geography',v:'Same timezone preferred'}],
  angles:[
    {name:'Build vs hire',desc:'"You have 3 open senior engineer roles. Average time to fill: 4 months. We can ship the feature in 6 weeks."',why:'Hiring is painful and slow. An agency that ships faster than you can hire wins.'},
    {name:'Tech debt observation',desc:'"I looked at your public repo / job posts. Sounds like you\'re migrating from [old tech] to [new tech]."',why:'Specific technical observation = instant credibility with CTOs.'},
    {name:'MVP speed',desc:'"You\'re spending 6 months building V1. Your competitor shipped theirs in 6 weeks with a studio."',why:'Speed to market is everything for funded startups. Time = money.'}
  ],
  templates:[
    {name:'Build vs hire',score:86,subject:'{{company}} engineering bandwidth',body:"Hi {{firstName}},\n\nI noticed {{company}} has 3 open engineering roles. Senior devs are taking 4+ months to hire right now.\n\nMeanwhile, the product roadmap isn't waiting.\n\nWe're a 20-person dev studio that embeds with your team. We ship production-ready features in 4-6 week sprints while you hire. When your team is ready, we hand off clean code with full documentation.\n\nWorth a 15-min call to see if the model fits?\n\nBest,\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Build vs hire',desc:'Reference their specific open roles.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'"Noticed {{company}} is scaling the eng team. Sent you a note."'},
    {day:'Day 5',ch:'linkedin',action:'Engage with tech content',desc:'Comment on a CTO post about hiring challenges or tech decisions.'},
    {day:'Day 7',ch:'email',action:'Tech debt or MVP speed angle',desc:'Different trigger, same pain.'},
    {day:'Day 11',ch:'linkedin',action:'Send message',desc:'"Quick q -- is the migration timeline on track or falling behind?"'},
    {day:'Day 14',ch:'email',action:'Case study with timeline',desc:'"Week 1: onboarding. Week 3: first PR merged. Week 6: feature live."'},
    {day:'Day 21',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'34%',reply:'3.8%',meeting:'1.2%',close:'26%'},
  objections:[
    {q:'"We only build in-house"',a:'We embed IN your house. <em>Same codebase, same PRs, same standups.</em> The difference: we\'re productive on day 1, not month 4.'},
    {q:'"Agencies produce throwaway code"',a:'Bad agencies do. Ask for our GitHub history. <em>100% test coverage, typed, documented.</em> Our code has to survive the handoff -- that\'s how we get rehired.'}
  ]
},
{id:'ecommerce',slug:'ecommerce-b2b',cat:'Tech',title:'E-commerce B2B',desc:'Sell to online stores and DTC brands. Fast cycles, clear metrics, performance-driven buyers.',
  stats:{open:'35%',reply:'4.5%',meetings:'14/mo'},
  icp:[{l:'Titles',v:'CEO, Head of Growth, E-commerce Manager'},{l:'Company size',v:'$1M-50M revenue'},{l:'Trigger',v:'Scaling ad spend, launching new markets'},{l:'Platform',v:'Shopify Plus, WooCommerce, Magento'},{l:'Budget signal',v:'Running Meta/Google ads at scale'},{l:'Geography',v:'US, UK, EU, AU'}],
  angles:[
    {name:'CRO angle',desc:'"I looked at your checkout flow. You\'re probably leaving 15-20% of revenue on the table."',why:'Every e-com founder obsesses over conversion rate. Specific = credible.'},
    {name:'Ad spend comparison',desc:'"You\'re spending $X/mo on Meta. Outbound can generate the same pipeline at 1/10th the cost."',why:'E-com founders understand CAC. Show them a better channel.'},
    {name:'Competitor intel',desc:'"Your competitor just launched in [market]. Here\'s what their strategy looks like."',why:'E-com is hyper-competitive. Competitor moves get attention.'}
  ],
  templates:[
    {name:'CRO opener',score:86,subject:'{{company}} conversion rates',body:"Hi {{firstName}},\n\nI looked at {{company}} and noticed a few things on the checkout flow that might be leaving revenue on the table.\n\nWe helped 3 DTC brands in your space increase checkout conversion by 15-25% in the last quarter. Average uplift: $48K/mo in recovered revenue.\n\nWould a 15-min walkthrough of what we found be useful?\n\nBest,\nSarah"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'CRO or competitor angle',desc:'Specific observation about their store.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'Short note. "Sent you something on {{company}}\'s checkout flow."'},
    {day:'Day 5',ch:'linkedin',action:'Engage with content',desc:'Like their product launch post. Show you know their brand.'},
    {day:'Day 6',ch:'email',action:'Ad spend comparison',desc:'CAC argument with numbers.'},
    {day:'Day 10',ch:'linkedin',action:'Send message',desc:'"Curious -- what\'s your main acquisition channel right now besides Meta?"'},
    {day:'Day 12',ch:'email',action:'Case study',desc:'Similar brand, specific revenue impact.'},
    {day:'Day 18',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'35%',reply:'4.5%',meeting:'1.8%',close:'18%'},
  objections:[
    {q:'"We only do performance marketing"',a:'Outbound IS performance marketing. <em>Measurable, attributable, predictable.</em> The difference: no ad platform takes a 30% cut.'},
    {q:'"Our AOV is too low for outbound"',a:'If your LTV is above $500, outbound works. We target based on <em>lifetime value, not first purchase</em>. B2B e-com and wholesale are especially strong.'}
  ]
},
{id:'consulting',slug:'consulting-firms',cat:'Professional',title:'Consulting Firms',desc:'Sell expertise and advisory. Relationship-driven, high deal values, long trust-building cycles.',
  stats:{open:'40%',reply:'4.0%',meetings:'8/mo'},
  icp:[{l:'Titles',v:'CEO, CFO, COO, VP Strategy'},{l:'Company size',v:'100-5000 employees'},{l:'Trigger',v:'Restructuring, M&A, new market entry'},{l:'Industry focus',v:'Pick 2-3 verticals you know deeply'},{l:'Budget signal',v:'Leadership changes, board announcements'},{l:'Geography',v:'Headquarters cities'}],
  angles:[
    {name:'Peer-level insight',desc:'"I was looking at {{company}} and noticed you recently expanded into EU. Most companies hit a wall at that stage."',why:'CEO-to-CEO tone. Observation, not pitch. Consultants sell by demonstrating they understand the problem.'},
    {name:'Contrarian point of view',desc:'"Most companies in [industry] are doing X. The data says Y works better. Here\'s why."',why:'Consultants need to show they think differently. A contrarian POV demands a response.'},
    {name:'Benchmark data',desc:'"We benchmarked 200 companies in [industry]. Here\'s where the top 10% differ from the rest."',why:'Data is catnip for C-suite. Especially when it implies they might not be in the top 10%.'}
  ],
  templates:[
    {name:'Peer-level insight',score:90,subject:'Noticed something about {{company}}',body:"Hi {{firstName}},\n\nI was looking at {{company}} and noticed you recently expanded into the EU market.\n\nMost B2B companies we work with hit a wall at that stage: the playbook that worked domestically doesn't translate. Messaging, compliance, buyer behavior -- all different.\n\nWe helped 4 companies navigate that exact transition this year.\n\nWorth comparing notes over a quick call?\n\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Peer-level insight',desc:'Observation + experience. No hard sell.'},
    {day:'Day 2',ch:'linkedin',action:'Connect with personal note',desc:'"Enjoyed your take on [topic]. Sent you a note on something I noticed about {{company}}."'},
    {day:'Day 4',ch:'linkedin',action:'Comment on their post',desc:'Substantive comment, not "Great post!" Show you think at their level.'},
    {day:'Day 8',ch:'email',action:'Contrarian POV',desc:'Share a data point that challenges conventional wisdom.'},
    {day:'Day 12',ch:'linkedin',action:'Share relevant article',desc:'Send them a relevant industry report via DM. Give value before asking.'},
    {day:'Day 15',ch:'email',action:'Benchmark data',desc:'Offer to share research. Low-commitment ask.'},
    {day:'Day 22',ch:'email',action:'Breakup',desc:'Respectful close.'}
  ],
  benchmarks:{open:'40%',reply:'4.0%',meeting:'1.4%',close:'22%'},
  objections:[
    {q:'"We only work with referrals"',a:'Referrals are great but <em>they don\'t scale</em>. What happens when you need to grow 40% next year? Outbound lets you target exactly the companies you want to work with, not wait for them to find you.'},
    {q:'"Our sales cycle is too long for cold email"',a:'That\'s exactly why you need outbound. <em>Start conversations now that close in 6 months.</em> The pipeline you build today is the revenue you close next quarter.'}
  ]
},
{id:'fintech',slug:'fintech',cat:'Tech',title:'Fintech',desc:'Sell to financial companies navigating regulation, scale, and trust. High deal values, complex buyers.',
  stats:{open:'41%',reply:'2.8%',meetings:'8/mo'},
  icp:[{l:'Titles',v:'CTO, VP Engineering, Head of Compliance, CFO'},{l:'Company size',v:'50-1000 employees'},{l:'Trigger',v:'New regulation (MiCA, PSD3), funding round'},{l:'Tech signal',v:'Legacy banking core, API migration'},{l:'Budget signal',v:'Series B+ or $5M+ ARR'},{l:'Geography',v:'US, UK, EU, Singapore'}],
  angles:[
    {name:'Compliance urgency',desc:'"MiCA enforcement starts in Q3. Most companies we talk to are scrambling."',why:'Regulatory deadlines are non-negotiable. Creates natural urgency without being salesy.'},
    {name:'Infrastructure modernization',desc:'"Still running on [legacy system]? The migration doesn\'t have to take 18 months."',why:'Specific tech observation = credibility. Every fintech CTO has this pain.'},
    {name:'Competitor move',desc:'"[Competitor] just launched [feature]. Here\'s the infrastructure they used."',why:'Competitive intelligence in fintech is gold. They\'ll take the meeting just for the intel.'}
  ],
  templates:[
    {name:'Compliance urgency',score:86,subject:'{{company}} and MiCA compliance',body:"Hi {{firstName}},\n\nWith MiCA enforcement starting in Q3, most crypto companies we talk to are scrambling to get compliance sorted. The ones that started 6 months ago are fine. The ones starting now are stressed.\n\nWe helped 8 fintech companies pass their compliance audits on the first try this year.\n\nWould it be useful to compare your current setup against what we typically see?\n\nBest,\nSarah"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Compliance or infrastructure angle',desc:'Lead with the most relevant regulatory trigger.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'"Noticed {{company}} is navigating MiCA. Sent you something relevant."'},
    {day:'Day 5',ch:'linkedin',action:'Share regulatory update',desc:'Post or DM a relevant regulatory news item. Position as an expert.'},
    {day:'Day 8',ch:'email',action:'Competitor intelligence',desc:'Share something they didn\'t know about a competitor\'s approach.'},
    {day:'Day 11',ch:'linkedin',action:'Send message',desc:'"Are you tracking how [competitor] is handling the compliance timeline?"'},
    {day:'Day 14',ch:'email',action:'Case study',desc:'Similar fintech, specific compliance result.'},
    {day:'Day 20',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'41%',reply:'2.8%',meeting:'0.9%',close:'20%'},
  objections:[
    {q:'"We handle compliance internally"',a:'Most companies do until they fail an audit. Ask: <em>when was your last external audit?</em> The companies that pass consistently have external partners validating their approach.'},
    {q:'"We\'re too early for outbound"',a:'If you\'re post-seed, you need pipeline. <em>Outbound is the fastest path from zero to predictable meetings.</em> Content takes 6-12 months. Outbound takes 3 weeks.'}
  ]
},
{id:'recruiting',slug:'recruiting-staffing',cat:'Professional',title:'Recruiting & Staffing',desc:'Sell to companies that hire at scale. Fast-moving market, relationship-driven, volume plays.',
  stats:{open:'42%',reply:'5.5%',meetings:'16/mo'},
  icp:[{l:'Titles',v:'VP HR, Head of Talent, CEO (startups), CHRO'},{l:'Company size',v:'50-2000 employees'},{l:'Trigger',v:'10+ open roles, new office, leadership change'},{l:'Industry focus',v:'Tech, healthcare, professional services'},{l:'Budget signal',v:'Active job postings on LinkedIn/Indeed'},{l:'Geography',v:'Major hiring markets'}],
  angles:[
    {name:'Hiring velocity',desc:'"You have 23 open roles right now. Most companies at that scale struggle with time-to-fill."',why:'Specific number from their job board. Shows you did the research.'},
    {name:'Cost per hire',desc:'"The average cost per hire in [industry] is $4,700. Our clients average $2,100."',why:'HR speaks the language of cost-per-hire. Beat the benchmark and they\'ll listen.'},
    {name:'Passive candidates',desc:'"80% of the best candidates aren\'t actively looking. Here\'s how we reach them."',why:'Every recruiter knows this stat. Few have a solution for it.'}
  ],
  templates:[
    {name:'Hiring velocity',score:88,subject:'{{company}} open roles',body:"Hi {{firstName}},\n\nI noticed {{company}} has 23 open roles right now across engineering and sales. At that volume, time-to-fill usually balloons to 60+ days.\n\nWe help companies cut time-to-fill by 40% by reaching passive candidates who aren't on job boards. Average: 12 qualified candidates per role per month.\n\nWorth a 15-min call to see if it fits?\n\nJohn"}
  ],
  sequence:[
    {day:'Day 1',ch:'email',action:'Hiring velocity',desc:'Reference their specific open roles.'},
    {day:'Day 2',ch:'linkedin',action:'Connect',desc:'"Noticed {{company}} is hiring aggressively. Sent you a note on sourcing passive candidates."'},
    {day:'Day 4',ch:'linkedin',action:'Engage with HR content',desc:'Comment on their employer branding posts. Show you understand their culture.'},
    {day:'Day 5',ch:'email',action:'Cost per hire',desc:'Benchmark comparison with specific numbers.'},
    {day:'Day 8',ch:'linkedin',action:'Send message',desc:'"Quick q -- are you finding it harder to source [role type] this quarter vs last?"'},
    {day:'Day 10',ch:'email',action:'Case study',desc:'Similar company, time-to-fill reduction.'},
    {day:'Day 15',ch:'email',action:'Breakup',desc:'Clean close.'}
  ],
  benchmarks:{open:'42%',reply:'5.5%',meeting:'2.3%',close:'20%'},
  objections:[
    {q:'"We use an ATS that handles outreach"',a:'ATS outreach has a 2% response rate. <em>Cold email done right gets 5-8%.</em> The difference: personalization, sequencing, and deliverability. Your ATS blasts. We target.'}
  ]
}
];

// ============================================================
// FR PLAYBOOKS DATA
// ============================================================
const FR_PLAYBOOKS = [
{id:'marketing-agency',slug:'agences-marketing',cat:'Agences',title:'Agences Marketing',desc:"Vendez l'outbound en tant que service. White-labelisez Overloop, facturez 3-4x, gardez la marge.",
  stats:{open:'38%',reply:'5.1%',meetings:'12/mois'},
  icp:[{l:'Titres',v:'CEO, CMO, Head of Growth'},{l:'Taille entreprise',v:'10-200 employes'},{l:'Industries cibles',v:'SaaS, e-commerce, fintech'},{l:'Declencheur',v:'Recrutement en marketing'},{l:'Signal budget',v:'Campagnes paid ads (visibles dans ads library)'},{l:'Geographie',v:'Marches Tier 1 (US, UK, EU)'}],
  angles:[
    {name:'Pitch white-label',desc:"Proposez l'outbound comme nouvelle ligne de service. Vous gerez les operations, ils obtiennent les rendez-vous.",why:"Les agences cherchent toujours de nouvelles sources de revenus. L'outbound a 70%+ de marge en white-label."},
    {name:'Comparaison concurrents',desc:'"3 de vos concurrents proposent deja l\'outbound. Voici le playbook qu\'ils utilisent."',why:"FOMO + preuve concrete. Personne ne veut etre l'agence qui ne propose pas ce que les concurrents offrent."},
    {name:'Resultats clients',desc:'Commencez par un resultat precis : "On a aide [agence] a booker 18 rendez-vous/mois pour ses clients SaaS."',why:"Les agences vendent des resultats. Montrez le resultat, elles trouveront comment le vendre."}
  ],
  templates:[
    {name:'Intro white-label',score:91,subject:"L'outbound de vos clients",body:"Bonjour {{firstName}},\n\nJe dirige Overloop. On travaille avec des agences comme {{company}} qui veulent ajouter l'outbound comme service pour leurs clients.\n\nLe modele : vous white-labelisez notre plateforme, facturez vos clients 3-4x ce que vous nous payez, et on gere l'infrastructure.\n\nTrois de vos concurrents le font deja. Je peux vous partager le playbook.\n\nOuvert a un rapide echange ?\n\nJohn"},
    {name:'Angle revenus',score:88,subject:'Nouvelle source de revenus pour {{company}}',body:"Bonjour {{firstName}},\n\nLa plupart des agences que je rencontre sont bloquees au meme plafond : retainers + projets. Ajouter l'outbound comme service change la donne.\n\nNos agences partenaires facturent 2 500-4 000 EUR/mois par client pour l'outbound. Leur cout : 800 EUR/mois. Ca fait 70% de marge sur un service recurrent.\n\nJe vous montre comment ca fonctionne ?\n\nJohn"},
    {name:'Etude de cas',score:89,subject:'Comment [Agence X] a ajoute 40K EUR de MRR',body:"Bonjour {{firstName}},\n\nUne agence de 15 personnes comme {{company}} a ajoute 40K EUR de revenus mensuels recurrents le trimestre dernier en proposant le cold email a ses clients existants.\n\nIls n'ont recrute personne. Ils ont white-labelise notre plateforme, cree 3 offres de service, et upselle leur portefeuille actuel.\n\n6 clients ont signe le premier mois.\n\n15 min pour voir si ca colle avec {{company}} ?\n\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Pitch white-label',desc:'Commencez par le modele. Court, direct.'},
    {day:'Jour 2',ch:'linkedin',action:'Voir profil + connecter',desc:'Note personnalisee : "J\'ai vu que vous dirigez une agence, je vous ai envoye quelque chose sur l\'outbound as a service."'},
    {day:'Jour 5',ch:'email',action:'Angle revenus',desc:"Angle different. Focus sur l'opportunite a 70% de marge."},
    {day:'Jour 7',ch:'linkedin',action:'Engager avec leur contenu',desc:'Likez ou commentez un post recent. Creez de la familiarite avant le prochain email.'},
    {day:'Jour 10',ch:'email',action:'Etude de cas',desc:"Preuve sociale. Chiffres precis d'une agence similaire."},
    {day:'Jour 12',ch:'linkedin',action:'Envoyer InMail ou message',desc:'"Hey {{firstName}}, vous avez eu le temps de regarder le modele outbound-as-a-service ? Je peux vous presenter les chiffres."'},
    {day:'Jour 15',ch:'email',action:'Breakup',desc:'"Je clos votre dossier ?" Direct et honnete.'}
  ],
  benchmarks:{open:'38%',reply:'5.1%',meeting:'2.1%',close:'25%'},
  objections:[
    {q:'"On fait deja de l\'outbound en interne"',a:"Demandez : <em>combien de rendez-vous par client par mois ?</em> La plupart des agences qui le font en interne arrivent a 3-5. Avec une plateforme dediee, leurs clients obtiennent 15-20. Ce n'est pas une question de faire de l'outbound, c'est de le faire a l'echelle."},
    {q:'"Nos clients ne paieraient pas pour l\'outbound"',a:"Recadrez : <em>vos clients paient deja pour des leads</em> via les ads, le SEO, les evenements. L'outbound est juste un canal de plus, et c'est le seul avec un cout unitaire previsible. Commencez avec un client pilote."},
    {q:'"On n\'a pas l\'expertise"',a:"C'est tout l'interet du white-label. <em>Vous n'avez pas besoin d'etre expert en outbound.</em> On gere l'infrastructure, la delivrabilite et l'optimisation. Votre equipe se concentre sur la relation client et le messaging."}
  ]
},
{id:'saas',slug:'saas-b2b',cat:'Tech',title:'SaaS B2B',desc:'Le vertical outbound avec le meilleur ROI. LTV elevee, ICP clair, resultats mesurables.',
  stats:{open:'45%',reply:'3.2%',meetings:'18/mois'},
  icp:[{l:'Titres',v:'VP Sales, Head of Growth, CRO, CEO (< 50 pers.)'},{l:'Taille entreprise',v:'20-500 employes'},{l:'Declencheur',v:'Levee recente, recrutement SDR, nouveau leadership'},{l:'Stack technique',v:'Utilise des outils concurrents ou adjacents'},{l:'Signal budget',v:'Series A+ ou $2M+ ARR'},{l:'Geographie',v:'US, UK, DACH, Nordics'}],
  angles:[
    {name:'Declencheur recrutement',desc:'"J\'ai vu que vous recrutez un SDR. Le cold email peut combler le gap pipeline pendant que vous recrutez."',why:"Recruter prend 3 mois. L'outbound prend 3 semaines. L'argument timing est irresistible."},
    {name:'Post-levee',desc:'"Felicitations pour la levee. La pression sur les objectifs pipeline vient de monter."',why:"Fraichement financee = budget disponible + pression du board. La fenetre d'opportunite est de 90 jours."},
    {name:'Deplacement concurrent',desc:'"Des entreprises comme [client du concurrent] ont quitte [concurrent] parce que [raison precise]."',why:"Les acheteurs SaaS evaluent en permanence. Donnez-leur une raison et ils prendront le rendez-vous."}
  ],
  templates:[
    {name:'Declencheur recrutement',score:89,subject:'Question rapide sur {{company}}',body:"Bonjour {{firstName}},\n\nJ'ai vu que {{company}} recrute un Head of Sales. Ca veut generalement dire que l'outbound devient prioritaire.\n\nOn aide les equipes B2B a booker 15-20 rendez-vous qualifies par mois via le cold email, sans recruter de SDR.\n\nDes entreprises comme Datadog et Notion utilisent cette approche pour remplir leur pipeline tout en gardant les effectifs legers.\n\n15 min cette semaine pour en parler ?\n\nJohn"},
    {name:'Post-levee',score:87,subject:'{{firstName}}, une idee rapide',body:"Bonjour {{firstName}},\n\nJ'ai vu que {{company}} venait de lever une Series B. Felicitations.\n\nEn general apres une levee, la pression sur les objectifs pipeline monte vite. Recruter des SDR prend 3 mois. Le cold email peut combler le gap en 3 semaines.\n\nOn gere le moteur outbound de 200+ entreprises SaaS B2B. Moyenne : 18 rendez-vous qualifies par mois, 0 EUR de budget pub.\n\n15 min cette semaine pour en discuter ?\n\nJohn"},
    {name:'Point de douleur',score:90,subject:'Pipeline de {{company}}',body:"Bonjour {{firstName}},\n\nLa plupart des entreprises SaaS que je rencontre ont le meme probleme apres la Series A : le CEO reste le meilleur commercial, et le pipeline depend de l'inbound qui ne scale pas.\n\nOn resout ca. Cold email, entierement automatise, 15-20 rendez-vous/mois. Pas besoin de recruter un SDR.\n\nC'est un probleme que {{company}} rencontre en ce moment ?\n\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Declencheur recrutement ou post-levee',desc:'Choisissez le declencheur le plus pertinent pour ce prospect.'},
    {day:'Jour 2',ch:'linkedin',action:'Voir profil + connecter',desc:'Note personnalisee en lien avec le declencheur. Pas de pitch.'},
    {day:'Jour 5',ch:'email',action:'Angle point de douleur',desc:'Angle different. Focus sur le probleme, pas sur votre produit.'},
    {day:'Jour 7',ch:'linkedin',action:'Commenter leur post',desc:'Engagement sincere. Creez de la familiarite avant le prochain touch.'},
    {day:'Jour 10',ch:'email',action:'Preuve sociale',desc:"Etude de cas d'une entreprise similaire. Chiffres precis."},
    {day:'Jour 13',ch:'linkedin',action:'Envoyer message',desc:'"J\'ai vu que vous scalez l\'equipe sales, l\'etude de cas que je vous ai envoyee pourrait etre pertinente. 15 min ?"'},
    {day:'Jour 18',ch:'email',action:'Breakup',desc:'"Je clos votre dossier ?" Net et direct.'}
  ],
  benchmarks:{open:'45%',reply:'3.2%',meeting:'1.2%',close:'20%'},
  objections:[
    {q:'"On a deja une equipe outbound"',a:"Parfait. Demandez : <em>quel est leur taux de rendez-vous ?</em> La plupart des equipes SDR bookent 8-12 rendez-vous/mois. L'outbound propulse par l'IA en booke 18-20. Il ne s'agit pas de remplacer l'equipe, mais de multiplier leur output."},
    {q:'"Le cold email ne marche pas dans notre marche"',a:"Demandez : <em>quel marche ?</em> Puis partagez un exemple precis. On a des clients en fintech, healthtech, devtools, HR tech et martech. Le cold email fonctionne quand le ciblage est bon et le contenu pertinent."},
    {q:'"On se concentre sur l\'inbound pour le moment"',a:"L'inbound c'est bien pour la marque. Mais ca <em>ne scale pas lineairement</em>. L'outbound si. Les meilleures entreprises font les deux. L'outbound remplit le pipeline pendant que l'inbound construit la marque."}
  ]
},
{id:'digital-agency',slug:'agences-web-digitales',cat:'Agences',title:'Agences Digitales & Web',desc:"Vendez a des entreprises qui ont besoin de sites, d'apps ou de transformation digitale. Deals eleves, cycles longs.",
  stats:{open:'36%',reply:'4.8%',meetings:'10/mois'},
  icp:[{l:'Titres',v:'CEO, CTO, VP Marketing, Directeur Digital'},{l:'Taille entreprise',v:'50-1000 employes'},{l:'Declencheur',v:'Site obsolete, rebrand, lancement produit'},{l:'Industries cibles',v:'Services professionnels, industrie, sante'},{l:'Signal budget',v:'Site web de plus de 3 ans'},{l:'Geographie',v:'Focus local/regional'}],
  angles:[
    {name:'Audit du site',desc:'"J\'ai regarde {{company}}.com. Quelques points m\'ont frappe qui pourraient vous couter des conversions."',why:"Observation precise = credibilite. Personne n'ignore un email qui dit que son site a des problemes."},
    {name:'Comparaison concurrents',desc:'"Votre concurrent vient de relancer son site. Voici ce qu\'il a change et pourquoi c\'est important."',why:"Pression concurrentielle + intel precise. Le prospect doit cliquer."},
    {name:'Benchmark industrie',desc:'"Le taux de conversion moyen dans [industrie] est de 3,2%. La plupart des sites qu\'on audite sont a 1,5%."',why:"Data-driven. Le prospect se demande ou il se situe."}
  ],
  templates:[
    {name:'Audit site web',score:88,subject:'{{company}}.com',body:"Bonjour {{firstName}},\n\nJ'ai regarde {{company}}.com. Deux choses m'ont frappe :\n\n1. Votre temps de chargement mobile est de 4,8s (Google penalise au-dela de 2,5s)\n2. Votre CTA principal est sous la ligne de flottaison sur chaque page\n\nLes deux sont corrigeables en une semaine et amelioreraient probablement votre taux de conversion de 20-30%.\n\nOn a fait ca pour 40+ entreprises dans [industrie]. Vous voulez l'audit complet ?\n\nCordialement,\nSarah"},
    {name:'Mouvement concurrent',score:86,subject:'Vous avez vu ce que [concurrent] vient de faire ?',body:"Bonjour {{firstName}},\n\nJ'ai remarque que [concurrent] vient de relancer son site avec un nouveau tunnel de reservation et des landing pages localisees pour chaque marche.\n\nD'experience, les entreprises qui prennent du retard sur l'experience web perdent 15-20% de leur pipeline face aux concurrents qui facilitent l'achat.\n\nRefondre le site de {{company}} est dans vos plans cette annee ?\n\nSarah"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Audit du site',desc:'Observation precise et documentee de leur site.'},
    {day:'Jour 2',ch:'linkedin',action:'Voir profil + connecter',desc:'"Je vous ai envoye un audit rapide de {{company}}.com, je pense que ca vous sera utile."'},
    {day:'Jour 5',ch:'linkedin',action:'Liker/commenter un post',desc:'Engagez avec leur contenu. Montrez que vous suivez leur secteur.'},
    {day:'Jour 7',ch:'email',action:'Mouvement concurrent',desc:'Declencheur different. Pression concurrentielle.'},
    {day:'Jour 11',ch:'linkedin',action:'Envoyer message',desc:'"Vous avez eu le temps de regarder l\'audit du site ? Je peux vous presenter les conclusions."'},
    {day:'Jour 14',ch:'email',action:'Etude de cas',desc:'Entreprise similaire, resultats precis, avant/apres.'},
    {day:'Jour 21',ch:'email',action:'Breakup',desc:'Court et propre.'}
  ],
  benchmarks:{open:'36%',reply:'4.8%',meeting:'1.8%',close:'22%'},
  objections:[
    {q:'"On est contents de notre agence actuelle"',a:"Tres bien. Demandez : <em>a quand remonte leur dernier audit de performance du site ?</em> La plupart des agences font le build et passent a autre chose. On se concentre sur l'optimisation continue. Modele different."},
    {q:'"On vient de refaire notre site"',a:"Timing parfait. Demandez : <em>vous suivez les taux de conversion ?</em> La plupart des nouveaux sites sont lances sans tracking correct. On peut mettre en place le framework de mesure pour savoir ce qui fonctionne."}
  ]
},
{id:'seo-agency',slug:'agences-seo',cat:'Agences',title:'Agences SEO',desc:'Vendez a des entreprises en difficulte sur le trafic organique. Angles data-driven, arguments ROI clairs.',
  stats:{open:'40%',reply:'4.2%',meetings:'11/mois'},
  icp:[{l:'Titres',v:'CEO, Head of Marketing, Directeur Contenu'},{l:'Taille entreprise',v:'20-500 employes'},{l:'Declencheur',v:'Chute de trafic, mise a jour algo, concurrent qui ranke'},{l:'Signal budget',v:"Google Ads actifs (ils achetent du trafic qu'ils pourraient gagner)"},{l:'Industries cibles',v:'SaaS, e-commerce, services professionnels'},{l:'Geographie',v:'Marches francophones et anglophones'}],
  angles:[
    {name:'Perte de trafic',desc:'"J\'ai remarque que {{company}} a perdu 30% de trafic organique apres la mise a jour de mars. Voici pourquoi probablement."',why:"Precis, data-driven, urgent. Ils s'en inquietent deja."},
    {name:'Classement concurrent',desc:'"Votre concurrent se positionne #1 sur [mot-cle]. Il recupere ~2 400 visites/mois dessus. Vous etes en page 3."',why:"Ecart concurrentiel quantifie. Difficile a ignorer quand on voit les chiffres."},
    {name:'Du paid vers l\'organique',desc:'"Vous depensez X EUR/mois en Google Ads pour des mots-cles sur lesquels vous pourriez ranker naturellement."',why:"Argument d'economie directe. Parle au CFO."}
  ],
  templates:[
    {name:'Chute de trafic',score:87,subject:'Trafic organique de {{company}}',body:"Bonjour {{firstName}},\n\nJ'ai fait une analyse rapide de {{company}}.com. On dirait que vous avez perdu environ 30% de trafic organique apres la derniere core update de Google.\n\nCause probable : contenu fin sur vos 5 pages principales et balisage schema manquant sur vos pages de service.\n\nOn a corrige exactement ce probleme pour une entreprise SaaS de votre taille le mois dernier. Ils ont recupere 85% du trafic perdu en 6 semaines.\n\nJe vous envoie l'audit detaille ?\n\nCordialement,\nSarah"},
    {name:'Ecart concurrent',score:89,subject:'{{company}} vs [concurrent]',body:"Bonjour {{firstName}},\n\nJ'ai compare le SEO de {{company}} a celui de [concurrent]. Trois choses ressortent :\n\n1. Ils se positionnent sur 340 mots-cles que vous n'avez pas\n2. Leur autorite de domaine est 12 points plus elevee\n3. Ils publient 4x plus de contenu par mois\n\nL'ecart est rattrapable en 6-9 mois avec la bonne strategie. On l'a fait plus de 50 fois.\n\n15 min pour revoir les donnees ensemble ?\n\nSarah"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Chute de trafic ou ecart concurrent',desc:'Ouverture data-driven avec des chiffres precis.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter + voir profil',desc:'"J\'ai fait une comparaison SEO rapide pour {{company}}, je vous l\'ai envoyee par email."'},
    {day:'Jour 5',ch:'linkedin',action:'Partager un insight SEO sur leur post',desc:'Commentez avec une observation SEO sincere. Construisez la credibilite.'},
    {day:'Jour 6',ch:'email',action:'Angle paid-vers-organique',desc:'Argument economies de couts.'},
    {day:'Jour 10',ch:'linkedin',action:'Envoyer message',desc:'"Question rapide : vous suivez l\'impact de la derniere core update sur {{company}} ?"'},
    {day:'Jour 12',ch:'email',action:'Etude de cas avec timeline',desc:'"Mois 1 : audit. Mois 3 : contenu en ligne. Mois 6 : trafic recupere."'},
    {day:'Jour 18',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'40%',reply:'4.2%',meeting:'1.6%',close:'23%'},
  objections:[
    {q:'"Le SEO prend trop de temps"',a:"Ca prend effectivement 3-6 mois pour les resultats complets. Mais <em>l'alternative c'est de payer pour les ads indefiniment</em>. Le SEO se compose. Les ads non. Au mois 12, le trafic SEO est gratuit. Le trafic ads coute toujours autant qu'au mois 1."},
    {q:'"On a deja essaye le SEO et ca n\'a pas marche"',a:"Demandez ce qu'ils ont fait. 90% du temps c'etait <em>du contenu sans strategie</em>. On commence par la recherche de mots-cles, l'analyse concurrentielle et l'audit technique avant d'ecrire un seul mot."}
  ]
},
{id:'pr-agency',slug:'agences-rp-communication',cat:'Agences',title:'RP & Communication',desc:'Vendez de la couverture media et de la gestion de reputation. Tres relationnel, resultats difficiles a mesurer, modele retainer.',
  stats:{open:'37%',reply:'4.6%',meetings:'9/mois'},
  icp:[{l:'Titres',v:'CEO, VP Marketing, Responsable Communication'},{l:'Taille entreprise',v:'50-500 employes'},{l:'Declencheur',v:'Lancement produit, levee de fonds, crise, rebrand'},{l:'Signal budget',v:'Recrutement en communication, actifs sur les reseaux'},{l:'Industries cibles',v:'Tech, marques grand public, sante'},{l:'Geographie',v:'Marches media Tier 1'}],
  angles:[
    {name:'Timing lancement',desc:'"{{company}} vient de lever. La fenetre presse dure 2-3 semaines. Apres, plus personne ne s\'en soucie."',why:"Urgence liee a un evenement reel. Les RP ont une date de peremption, ils le savent."},
    {name:'Couverture concurrents',desc:'"Votre concurrent a ete couvert dans TechCrunch la semaine derniere. Voici l\'angle qu\'ils ont utilise."',why:"FOMO + info actionnable. Personne ne veut que son concurrent soit dans la presse et pas lui."},
    {name:'Ecart de mesure',desc:'"La plupart des agences RP ne peuvent pas vous dire le ROI d\'un placement. Nous si."',why:"La mesure est la grande faiblesse des RP. Si vous la resolvez, vous obtenez le rendez-vous."}
  ],
  templates:[
    {name:'RP post-levee',score:88,subject:'Strategie presse de {{company}}',body:"Bonjour {{firstName}},\n\nFelicitations pour la levee. Vous avez une fenetre de 2-3 semaines pendant laquelle les journalistes s'interesseront a {{company}}. Apres, vous n'etes qu'une startup financee de plus.\n\nOn aide les entreprises a transformer les annonces de levee en 5-8 placements media le premier mois. Pas de la presse vanite, des medias que vos acheteurs lisent vraiment.\n\nVous voulez voir le playbook qu'on a utilise pour [entreprise similaire] ?\n\nCordialement,\nJohn"},
    {name:'Angle concurrent',score:87,subject:"Vous avez vu l'article sur [concurrent] ?",body:"Bonjour {{firstName}},\n\n[Concurrent] a decroche un article dans TechCrunch la semaine derniere. L'angle : \"comment [leur produit] transforme [l'industrie].\"\n\nLa journaliste qui l'a ecrit couvre votre secteur aussi. On la connait et on a un angle qui positionne {{company}} comme le contre-recit.\n\nUn rapide echange pour discuter du pitch ?\n\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Post-levee ou angle concurrent',desc:'Timely, precis, lie a un evenement reel.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'"Je vous ai envoye une note sur le timing presse de {{company}}."'},
    {day:'Jour 5',ch:'linkedin',action:'Engager avec leur contenu',desc:"Commentez une annonce recente de l'entreprise."},
    {day:'Jour 6',ch:'email',action:'Angle mesure',desc:'Positionnez le ROI des RP comme votre differenciateur.'},
    {day:'Jour 10',ch:'linkedin',action:'Envoyer message',desc:'"La fenetre presse se ferme. On en parle cette semaine ?"'},
    {day:'Jour 14',ch:'email',action:'Etude de cas',desc:'Entreprise similaire, placements precis + impact pipeline.'},
    {day:'Jour 20',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'37%',reply:'4.6%',meeting:'1.8%',close:'21%'},
  objections:[
    {q:'"On a deja une agence RP"',a:"Demandez : <em>combien de leads qualifies a genere leur derniere campagne ?</em> S'ils ne peuvent pas repondre, c'est le probleme qu'on resout."},
    {q:'"Les RP ne generent pas de pipeline directement"',a:"Si, quand vous <em>choisissez les bons medias et trackez l'attribution</em>. On mesure les RP en rendez-vous generes, pas en nombre de coupures presse."}
  ]
},
{id:'branding-agency',slug:'agences-branding-design',cat:'Agences',title:'Branding & Design',desc:'Vendez strategie de marque et identite visuelle. Deals eleves, decisions emotionnelles, vente par le portfolio.',
  stats:{open:'35%',reply:'4.2%',meetings:'7/mois'},
  icp:[{l:'Titres',v:'CEO, CMO, VP Brand, Directeur Creatif'},{l:'Taille entreprise',v:'20-500 employes'},{l:'Declencheur',v:'Rebrand, nouveau marche, M&A, Series B+'},{l:'Signal budget',v:'Marque obsolete (3+ ans), presence inconsistante'},{l:'Industries cibles',v:'Tech, consumer, services professionnels'},{l:'Geographie',v:'Marches design-forward (US, UK, Nordics)'}],
  angles:[
    {name:'Audit de marque',desc:'"J\'ai regarde la marque de {{company}} sur 5 points de contact. Il y a 3 inconsistances qui pourraient troubler vos acheteurs."',why:"Precis, recherche, non menacant. Vous ne dites pas que leur marque est mauvaise, vous dites qu'elle est inconsistante."},
    {name:"Point d'inflexion croissance",desc:'"Vous venez de lever une Series B. Votre marque a ete construite pour une startup de 10 personnes. Maintenant vous vendez a l\'enterprise."',why:"Les marques post-levee sont souvent en retard sur l'evolution de l'entreprise. Cette observation resonne."},
    {name:'Comparaison design concurrents',desc:'"Votre concurrent vient de rebrander. Voici ce qui a change et ce que ca signale sur leur positionnement."',why:"La comparaison visuelle est puissante. Les CEO se soucient de paraitre moins bien que les concurrents."}
  ],
  templates:[
    {name:'Audit de marque',score:89,subject:'La marque de {{company}} sur ses points de contact',body:"Bonjour {{firstName}},\n\nJ'ai fait un audit rapide de la marque de {{company}} sur le site, LinkedIn, le pitch deck et les captures produit. Trois choses ressortent :\n\n1. La palette de couleurs change entre votre site et votre produit\n2. Votre header LinkedIn reference encore un ancien tagline\n3. Votre site dit une chose, votre pitch deck en dit une autre\n\nDes details, mais ils s'accumulent. Les acheteurs remarquent l'inconsistance meme s'ils ne savent pas l'articuler.\n\nOn a corrige ca pour une entreprise SaaS de votre taille en 6 semaines. Vous voulez voir l'avant/apres ?\n\nCordialement,\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Audit de marque',desc:'Observations precises sur plusieurs points de contact.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'"Je vous ai envoye un audit rapide de la marque de {{company}}."'},
    {day:'Jour 5',ch:'linkedin',action:'Partager un insight design',desc:'Commentez un post sur les tendances branding. Montrez que vous pensez a ce sujet.'},
    {day:'Jour 7',ch:'email',action:"Angle point d'inflexion",desc:'Connectez leur stade de croissance a la maturite de leur marque.'},
    {day:'Jour 11',ch:'linkedin',action:'Envoyer message',desc:'"L\'ecart de marque se creuse generalement apres la Series B. On en parle ?"'},
    {day:'Jour 14',ch:'email',action:'Etude de cas avant/apres',desc:"Preuve visuelle. Comparaison cote a cote d'un rebrand que vous avez fait."},
    {day:'Jour 20',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'35%',reply:'4.2%',meeting:'1.5%',close:'24%'},
  objections:[
    {q:'"On n\'est pas prets pour un rebrand"',a:"Le rebrand est l'option nucleaire. On commence par <em>l'alignement de marque</em> : rendre consistant ce que vous avez deja. C'est un projet de 4-6 semaines, pas un chantier de 6 mois."},
    {q:'"On a un designer en interne"',a:"Parfait. On travaille aux cotes des equipes internes. <em>On fait la strategie et la direction, ils font l'execution.</em> La plupart des designers internes attendent qu'on leur donne un brief."}
  ]
},
{id:'social-agency',slug:'agences-social-media',cat:'Agences',title:'Social Media',desc:'Vendez strategie social et creation de contenu. Marche a fort churn, creative-driven, oriente resultats.',
  stats:{open:'39%',reply:'5.0%',meetings:'11/mois'},
  icp:[{l:'Titres',v:'Head of Marketing, CMO, Social Media Manager'},{l:'Taille entreprise',v:'20-200 employes'},{l:'Declencheur',v:'Publication irreguliere, faible engagement, concurrent qui buzze'},{l:'Signal budget',v:'Budget ads actif, recrutement pour le social'},{l:'Industries cibles',v:'DTC, food & bev, mode, tech'},{l:'Geographie',v:'US, UK, EU'}],
  angles:[
    {name:'Audit engagement',desc:'"Vos 20 derniers posts ont un engagement moyen de 0,3%. La moyenne industrie est de 1,2%. Voici pourquoi."',why:"Donnees precises qu'ils peuvent verifier. Difficile d'argumenter contre les chiffres."},
    {name:'Moment viral concurrent',desc:'"Le dernier reel de votre concurrent a fait 500K vues. Voici le format qu\'ils ont utilise."',why:"Jalousie concurrentielle + playbook actionnable = irresistible."},
    {name:'Ecart contenu-pipeline',desc:'"Vous publiez 4x/semaine mais votre pipeline est toujours alimente par les ads. Le social devrait sourcer 20% des leads."',why:"Connecte les vanity metrics (posts) aux metriques business (pipeline). Langage CEO."}
  ],
  templates:[
    {name:'Audit engagement',score:90,subject:'Engagement social de {{company}}',body:"Bonjour {{firstName}},\n\nJ'ai analyse les 30 derniers jours de {{company}} sur LinkedIn et Instagram. Quelques points :\n\n- Engagement moyen : 0,3% (moyenne industrie : 1,2%)\n- Frequence de publication correcte (4x/semaine) mais le mix de formats est desequilibre : 80% images statiques, 0% video\n- Meilleur post : celui avec une vraie personne, pas un visuel graphique\n\nLa solution n'est pas de publier plus. C'est de publier differemment.\n\nJe vous montre ce qui fonctionne pour des marques similaires en ce moment ?\n\nCordialement,\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Audit engagement',desc:'Chiffres precis de leur presence social.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter + engager',desc:'Likez leur dernier post. Connectez avec une note qui le reference.'},
    {day:'Jour 4',ch:'linkedin',action:'Commenter leur contenu',desc:'Laissez un commentaire de fond. Montrez que vous suivez vraiment leur marque.'},
    {day:'Jour 6',ch:'email',action:'Moment viral concurrent',desc:"Partagez un exemple precis dont ils peuvent s'inspirer."},
    {day:'Jour 9',ch:'linkedin',action:'Envoyer message',desc:'"J\'ai vu votre derniere campagne. J\'ai quelques idees sur le mix de formats."'},
    {day:'Jour 13',ch:'email',action:'Etude de cas',desc:"Marque similaire, hausse d'engagement precise."},
    {day:'Jour 18',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'39%',reply:'5.0%',meeting:'2.0%',close:'20%'},
  objections:[
    {q:'"On gere le social en interne"',a:"La plupart des entreprises le font. La question c'est : <em>est-ce que ca genere du pipeline ou juste des impressions ?</em> On transforme le social d'un cout de marque en source de leads."},
    {q:'"Le social ne genere pas de ventes B2B"',a:"LinkedIn a genere $2,3Mds de leads B2B l'annee derniere. <em>Le social fonctionne en B2B quand le contenu est construit pour les acheteurs, pas pour les marketeurs.</em>"}
  ]
},
{id:'performance-agency',slug:'agences-performance-ads',cat:'Agences',title:'Performance & Paid Media',desc:'Vendez gestion ads et CRO. Acheteurs data-driven, obsedes par le ROAS, facile de prouver la valeur.',
  stats:{open:'36%',reply:'4.4%',meetings:'10/mois'},
  icp:[{l:'Titres',v:'Head of Growth, CMO, CEO (DTC), Directeur E-com'},{l:'Taille entreprise',v:'$1M-50M de CA'},{l:'Declencheur',v:'CAC en hausse, budget ads qui scale, nouveaux marches'},{l:'Signal budget',v:'10K+ EUR/mois en Meta/Google ads'},{l:'Industries cibles',v:'DTC, e-commerce, SaaS, apps'},{l:'Geographie',v:'US, UK, EU, AU'}],
  angles:[
    {name:'Tendance CAC',desc:'"Votre CPM Meta a augmente de 40% cette annee. Votre ROAS a probablement baisse. Il y a une solution."',why:"Chaque performance marketer ressent l'inflation des CPM. Vous nommez leur douleur."},
    {name:'Audit Ad Library',desc:'"J\'ai regarde votre Meta Ad Library. Vous avez 12 creatives actives. Seulement 2 tournent depuis plus de 7 jours."',why:"Precis, verifiable, montre que vous avez fait le travail. Ils savent que la fatigue creative est un probleme."},
    {name:'Diversification canaux',desc:'"80% de votre budget est sur Meta. Si l\'algorithme change demain, vous perdez 80% du pipeline."',why:"Le risque de concentration est reel. Les CFO repondent particulierement a cet argument."}
  ],
  templates:[
    {name:'Tendance CAC',score:87,subject:'Performance ads de {{company}}',body:"Bonjour {{firstName}},\n\nLes CPM Meta dans votre vertical ont augmente de 40% cette annee. Pour la plupart des entreprises, ca signifie un ROAS en baisse de 20-30% sur le meme budget.\n\nOn aide des marques comme {{company}} a remonter le ROAS sans augmenter le budget, grace au testing creatif, l'optimisation d'audience et la diversification canaux.\n\nLe trimestre dernier, on a ameliore le ROAS de 35% pour une marque DTC de votre taille.\n\n15 min pour revoir votre setup actuel ?\n\nCordialement,\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Tendance CAC ou audit Ad Library',desc:"Commencez par de la data qu'ils peuvent verifier."},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'"Je vous ai envoye une note sur la performance ads de {{company}}."'},
    {day:'Jour 5',ch:'linkedin',action:'Partager un benchmark industrie',desc:'Postez ou envoyez en DM une tendance CPM/ROAS pertinente pour leur vertical.'},
    {day:'Jour 6',ch:'email',action:'Angle diversification canaux',desc:'Argument risque. CFO-friendly.'},
    {day:'Jour 10',ch:'linkedin',action:'Envoyer message',desc:'"Question rapide : quel % de votre pipeline vient de Meta vs les autres canaux ?"'},
    {day:'Jour 13',ch:'email',action:'Etude de cas ROAS',desc:'Marque similaire, amelioration ROAS precise.'},
    {day:'Jour 18',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'36%',reply:'4.4%',meeting:'1.7%',close:'22%'},
  objections:[
    {q:'"On gere les ads en interne"',a:"La plupart des entreprises le font. Mais <em>gerer et optimiser, ce n'est pas la meme chose</em>. On audite 100+ comptes par an. Les patterns qu'on voit sur l'ensemble donnent un avantage injuste a chacun."},
    {q:'"Notre ROAS est correct"',a:"Correct compare a quoi ? <em>Les benchmarks industrie changent chaque trimestre.</em> \"Correct\" il y a 6 mois est peut-etre \"en dessous de la moyenne\" aujourd'hui. On peut faire une comparaison benchmark gratuite."}
  ]
},
{id:'content-agency',slug:'agences-content-marketing',cat:'Agences',title:'Content Marketing',desc:'Vendez strategie de contenu, redaction SEO et thought leadership. Cycles longs, ROI difficile a prouver, modele retainer.',
  stats:{open:'38%',reply:'4.3%',meetings:'9/mois'},
  icp:[{l:'Titres',v:'Head of Marketing, VP Contenu, CMO, CEO (startups)'},{l:'Taille entreprise',v:'20-500 employes'},{l:'Declencheur',v:'Blog sans trafic, equipe contenu de 1, declin SEO'},{l:'Signal budget',v:'Blog actif mais faible trafic organique'},{l:'Industries cibles',v:'SaaS, services professionnels, fintech'},{l:'Geographie',v:'Marches francophones et anglophones'}],
  angles:[
    {name:'Audit trafic',desc:'"Votre blog a 150 articles mais seulement 3 generent du trafic organique. Les 147 autres sont invisibles pour Google."',why:"Precis, surprenant, et legerement douloureux. Ils voudront savoir lesquels sont les 3."},
    {name:'Ecart ROI contenu',desc:'"Vous publiez 4 articles/semaine mais pouvez-vous en relier un seul a un deal signe ?"',why:"Les equipes contenu trackent rarement jusqu'au CA. Le souligner montre que vous pensez differemment."},
    {name:'Comparaison contenu concurrent',desc:'"Votre concurrent publie deux fois moins que vous mais obtient 3x le trafic organique. Voici pourquoi."',why:"Qualite vs quantite. La plupart des equipes contenu sont coincees dans la course aux publications."}
  ],
  templates:[
    {name:'Audit trafic',score:89,subject:'Performance du blog de {{company}}',body:"Bonjour {{firstName}},\n\nJ'ai fait une analyse rapide du blog de {{company}}. 150+ articles publies, mais seulement 3 pages generent du trafic organique significatif.\n\nLes 147 autres sont essentiellement invisibles : pas de classement, pas de clics, pas de leads. Ca fait beaucoup de redaction sans retour.\n\nLa solution, ce n'est pas plus de contenu. C'est une strategie de contenu differente : moins d'articles, meilleure qualite, construits autour de mots-cles avec un vrai volume de recherche.\n\nOn a fait ca pour une entreprise SaaS de votre taille. Ils sont passes de 2 000 a 18 000 visites organiques/mois en 5 mois. Avec moins d'articles.\n\nVous voulez voir la strategie ?\n\nCordialement,\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Audit trafic',desc:'Chiffres precis de leur blog/site.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'"J\'ai fait une analyse de contenu pour {{company}}. Je vous l\'ai envoyee par email."'},
    {day:'Jour 4',ch:'linkedin',action:'Engager avec leur contenu',desc:'Laissez un commentaire reflechi sur leur blog ou article LinkedIn.'},
    {day:'Jour 6',ch:'email',action:'Ecart ROI contenu',desc:'Connectez contenu et CA. Angle different.'},
    {day:'Jour 9',ch:'linkedin',action:'Partager un insight pertinent',desc:'Envoyez en DM un conseil strategie contenu pertinent pour leur industrie.'},
    {day:'Jour 12',ch:'email',action:'Comparaison concurrent',desc:"Montrez l'ecart qualite vs quantite."},
    {day:'Jour 18',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'38%',reply:'4.3%',meeting:'1.6%',close:'23%'},
  objections:[
    {q:'"On a deja une equipe contenu"',a:"Les equipes contenu produisent du contenu. <em>Les strateges contenu produisent des resultats.</em> On ne remplace pas vos redacteurs, on leur donne les bons briefs pour que chaque article ait une chance de ranker."},
    {q:'"Le contenu met trop longtemps a donner des resultats"',a:"Le mauvais contenu prend du temps. <em>Le contenu strategique montre du trafic en 8-12 semaines</em> parce qu'on cible des mots-cles sur lesquels votre site peut reellement ranker, pas des mots-cles aspirationnels."}
  ]
},
{id:'dev-agency',slug:'studios-dev-produit',cat:'Agences',title:'Studios Dev & Produit',desc:'Vendez du developpement custom, des MVP et du conseil produit. Acheteurs techniques, longs cycles, deals eleves.',
  stats:{open:'34%',reply:'3.8%',meetings:'6/mois'},
  icp:[{l:'Titres',v:'CTO, VP Engineering, CEO (non technique), Directeur Produit'},{l:'Taille entreprise',v:'20-200 employes'},{l:'Declencheur',v:'Levee de fonds, reecriture produit, migration legacy, nouvelle ligne produit'},{l:'Signal budget',v:"Offres d'emploi devs seniors, discussions dette technique"},{l:'Industries cibles',v:'SaaS, fintech, healthtech, marketplace'},{l:'Geographie',v:'Meme fuseau horaire prefere'}],
  angles:[
    {name:'Build vs recruter',desc:'"Vous avez 3 postes d\'ingenieur senior ouverts. Temps moyen pour recruter : 4 mois. On peut livrer la feature en 6 semaines."',why:"Recruter est douloureux et lent. Une agence qui livre plus vite que vous ne recrutez gagne."},
    {name:'Observation dette technique',desc:'"J\'ai regarde votre repo public / vos offres d\'emploi. On dirait que vous migrez de [ancien tech] vers [nouveau tech]."',why:"Observation technique precise = credibilite instantanee aupres des CTO."},
    {name:'Vitesse MVP',desc:'"Vous passez 6 mois a construire la V1. Votre concurrent a livre la sienne en 6 semaines avec un studio."',why:"La vitesse de mise sur le marche est cruciale pour les startups financees. Temps = argent."}
  ],
  templates:[
    {name:'Build vs recruter',score:86,subject:'Bande passante engineering de {{company}}',body:"Bonjour {{firstName}},\n\nJ'ai remarque que {{company}} a 3 postes d'ingenieur ouverts. Les devs seniors prennent 4+ mois a recruter en ce moment.\n\nEn attendant, la roadmap produit n'attend pas.\n\nOn est un studio dev de 20 personnes qui s'integre a votre equipe. On livre des features production-ready en sprints de 4-6 semaines pendant que vous recrutez. Quand votre equipe est prete, on transmet du code propre avec documentation complete.\n\n15 min pour voir si le modele convient ?\n\nCordialement,\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Build vs recruter',desc:'Referencez leurs postes ouverts specifiques.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'"J\'ai vu que {{company}} scale l\'equipe engineering. Je vous ai envoye une note."'},
    {day:'Jour 5',ch:'linkedin',action:'Engager avec le contenu tech',desc:'Commentez un post CTO sur les defis de recrutement ou les decisions techniques.'},
    {day:'Jour 7',ch:'email',action:'Angle dette technique ou vitesse MVP',desc:'Declencheur different, meme douleur.'},
    {day:'Jour 11',ch:'linkedin',action:'Envoyer message',desc:'"Question rapide : le planning de migration est dans les temps ou ca prend du retard ?"'},
    {day:'Jour 14',ch:'email',action:'Etude de cas avec timeline',desc:'"Semaine 1 : onboarding. Semaine 3 : premiere PR mergee. Semaine 6 : feature en production."'},
    {day:'Jour 21',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'34%',reply:'3.8%',meeting:'1.2%',close:'26%'},
  objections:[
    {q:'"On ne construit qu\'en interne"',a:"On s'integre DANS votre equipe. <em>Meme codebase, memes PR, memes standups.</em> La difference : on est productifs au jour 1, pas au mois 4."},
    {q:'"Les agences produisent du code jetable"',a:"Les mauvaises agences oui. Demandez notre historique GitHub. <em>100% de couverture de tests, type, documente.</em> Notre code doit survivre au transfert, c'est comme ca qu'on est re-engages."}
  ]
},
{id:'ecommerce',slug:'ecommerce-b2b',cat:'Tech',title:'E-commerce B2B',desc:'Vendez aux boutiques en ligne et marques DTC. Cycles rapides, metriques claires, acheteurs orientes performance.',
  stats:{open:'35%',reply:'4.5%',meetings:'14/mois'},
  icp:[{l:'Titres',v:'CEO, Head of Growth, Responsable E-commerce'},{l:'Taille entreprise',v:'$1M-50M de CA'},{l:'Declencheur',v:'Budget ads en hausse, lancement nouveaux marches'},{l:'Plateforme',v:'Shopify Plus, WooCommerce, Magento'},{l:'Signal budget',v:'Ads Meta/Google a grande echelle'},{l:'Geographie',v:'US, UK, EU, AU'}],
  angles:[
    {name:'Angle CRO',desc:'"J\'ai regarde votre tunnel d\'achat. Vous laissez probablement 15-20% de CA sur la table."',why:"Chaque fondateur e-com est obsede par le taux de conversion. Precis = credible."},
    {name:'Comparaison budget ads',desc:'"Vous depensez X EUR/mois sur Meta. L\'outbound peut generer le meme pipeline a 1/10e du cout."',why:"Les fondateurs e-com comprennent le CAC. Montrez-leur un meilleur canal."},
    {name:'Intel concurrent',desc:'"Votre concurrent vient de se lancer sur [marche]. Voici a quoi ressemble sa strategie."',why:"Le e-com est ultra-competitif. Les mouvements des concurrents captent l'attention."}
  ],
  templates:[
    {name:'Ouverture CRO',score:86,subject:'Taux de conversion de {{company}}',body:"Bonjour {{firstName}},\n\nJ'ai regarde {{company}} et repere quelques points sur le tunnel d'achat qui pourraient laisser du CA sur la table.\n\nOn a aide 3 marques DTC dans votre secteur a augmenter la conversion checkout de 15-25% le trimestre dernier. Hausse moyenne : 48K EUR/mois de CA recupere.\n\n15 min pour vous montrer ce qu'on a trouve ?\n\nCordialement,\nSarah"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'CRO ou angle concurrent',desc:'Observation precise sur leur boutique.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'Note courte. "Je vous ai envoye quelque chose sur le tunnel d\'achat de {{company}}."'},
    {day:'Jour 5',ch:'linkedin',action:'Engager avec le contenu',desc:'Likez leur post de lancement produit. Montrez que vous connaissez la marque.'},
    {day:'Jour 6',ch:'email',action:'Comparaison budget ads',desc:'Argument CAC avec chiffres.'},
    {day:'Jour 10',ch:'linkedin',action:'Envoyer message',desc:'"Curieux : quel est votre principal canal d\'acquisition en dehors de Meta ?"'},
    {day:'Jour 12',ch:'email',action:'Etude de cas',desc:'Marque similaire, impact CA precis.'},
    {day:'Jour 18',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'35%',reply:'4.5%',meeting:'1.8%',close:'18%'},
  objections:[
    {q:'"On ne fait que du performance marketing"',a:"L'outbound EST du performance marketing. <em>Mesurable, attribuable, previsible.</em> La difference : aucune plateforme pub ne prend 30% de commission."},
    {q:'"Notre panier moyen est trop bas pour l\'outbound"',a:"Si votre LTV depasse 500 EUR, l'outbound fonctionne. On cible sur la <em>valeur vie client, pas le premier achat</em>. Le B2B e-com et le wholesale marchent particulierement bien."}
  ]
},
{id:'consulting',slug:'cabinets-conseil',cat:'Professionnel',title:'Cabinets de Conseil',desc:"Vendez de l'expertise et du conseil. Relationnel, deals eleves, longs cycles de construction de confiance.",
  stats:{open:'40%',reply:'4.0%',meetings:'8/mois'},
  icp:[{l:'Titres',v:'CEO, CFO, COO, VP Strategy'},{l:'Taille entreprise',v:'100-5000 employes'},{l:'Declencheur',v:'Restructuration, M&A, entree sur un nouveau marche'},{l:'Industries cibles',v:'Choisissez 2-3 verticaux que vous connaissez bien'},{l:'Signal budget',v:'Changements de direction, annonces board'},{l:'Geographie',v:'Capitales et grandes metropoles'}],
  angles:[
    {name:'Insight entre pairs',desc:'"Je regardais {{company}} et j\'ai remarque que vous venez de vous etendre en Europe. La plupart des entreprises se heurtent a un mur a cette etape."',why:"Ton CEO-to-CEO. Observation, pas pitch. Les consultants vendent en montrant qu'ils comprennent le probleme."},
    {name:'Point de vue contrarian',desc:'"La plupart des entreprises dans [industrie] font X. Les donnees montrent que Y fonctionne mieux. Voici pourquoi."',why:"Les consultants doivent montrer qu'ils pensent differemment. Un point de vue contrarian exige une reponse."},
    {name:'Donnees benchmark',desc:'"On a benchmark 200 entreprises dans [industrie]. Voici ce qui differencie le top 10% du reste."',why:"La data est irresistible pour les C-level. Surtout quand ca sous-entend qu'ils ne sont peut-etre pas dans le top 10%."}
  ],
  templates:[
    {name:'Insight entre pairs',score:90,subject:"J'ai remarque quelque chose sur {{company}}",body:"Bonjour {{firstName}},\n\nJe regardais {{company}} et j'ai vu que vous venez de vous etendre sur le marche europeen.\n\nLa plupart des entreprises B2B avec lesquelles on travaille se heurtent a un mur a cette etape : le playbook qui marchait en domestique ne se traduit pas. Messaging, conformite, comportement d'achat, tout est different.\n\nOn a accompagne 4 entreprises dans cette transition exacte cette annee.\n\nCa vaut le coup de comparer nos notes lors d'un rapide echange ?\n\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Insight entre pairs',desc:'Observation + experience. Pas de hard sell.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter avec note personnelle',desc:'"J\'ai aime votre prise de position sur [sujet]. Je vous ai envoye une note sur quelque chose que j\'ai remarque chez {{company}}."'},
    {day:'Jour 4',ch:'linkedin',action:'Commenter leur post',desc:'Commentaire de fond, pas "Super post !". Montrez que vous pensez a leur niveau.'},
    {day:'Jour 8',ch:'email',action:'Point de vue contrarian',desc:'Partagez une donnee qui challenge la pensee conventionnelle.'},
    {day:'Jour 12',ch:'linkedin',action:'Partager un article pertinent',desc:'Envoyez-leur un rapport sectoriel par DM. Donnez de la valeur avant de demander.'},
    {day:'Jour 15',ch:'email',action:'Donnees benchmark',desc:'Proposez de partager la recherche. Demande a faible engagement.'},
    {day:'Jour 22',ch:'email',action:'Breakup',desc:'Cloture respectueuse.'}
  ],
  benchmarks:{open:'40%',reply:'4.0%',meeting:'1.4%',close:'22%'},
  objections:[
    {q:'"On ne travaille que par recommandation"',a:"Les recommandations c'est bien mais <em>ca ne scale pas</em>. Que se passe-t-il quand vous devez croitre de 40% l'annee prochaine ? L'outbound vous permet de cibler exactement les entreprises avec lesquelles vous voulez travailler, au lieu d'attendre qu'elles vous trouvent."},
    {q:'"Notre cycle de vente est trop long pour le cold email"',a:"C'est justement pour ca que vous avez besoin d'outbound. <em>Commencez des conversations maintenant qui closent dans 6 mois.</em> Le pipeline que vous construisez aujourd'hui, c'est le CA que vous closez le trimestre prochain."}
  ]
},
{id:'fintech',slug:'fintech',cat:'Tech',title:'Fintech',desc:'Vendez aux entreprises financieres qui naviguent regulation, scale et confiance. Deals eleves, acheteurs complexes.',
  stats:{open:'41%',reply:'2.8%',meetings:'8/mois'},
  icp:[{l:'Titres',v:'CTO, VP Engineering, Head of Compliance, CFO'},{l:'Taille entreprise',v:'50-1000 employes'},{l:'Declencheur',v:'Nouvelle regulation (MiCA, PSD3), levee de fonds'},{l:'Signal tech',v:'Core bancaire legacy, migration API'},{l:'Signal budget',v:'Series B+ ou $5M+ ARR'},{l:'Geographie',v:'US, UK, EU, Singapour'}],
  angles:[
    {name:'Urgence conformite',desc:'"L\'application de MiCA demarre au Q3. La plupart des entreprises qu\'on contacte sont en panique."',why:"Les deadlines reglementaires sont non negociables. Ca cree une urgence naturelle sans etre commercial."},
    {name:'Modernisation infrastructure',desc:'"Toujours sur [systeme legacy] ? La migration ne doit pas forcement prendre 18 mois."',why:"Observation technique precise = credibilite. Chaque CTO fintech ressent cette douleur."},
    {name:'Mouvement concurrent',desc:'"[Concurrent] vient de lancer [feature]. Voici l\'infrastructure qu\'ils ont utilisee."',why:"L'intelligence concurrentielle en fintech vaut de l'or. Ils prendront le rendez-vous juste pour l'info."}
  ],
  templates:[
    {name:'Urgence conformite',score:86,subject:'{{company}} et la conformite MiCA',body:"Bonjour {{firstName}},\n\nAvec l'application de MiCA qui demarre au Q3, la plupart des entreprises crypto qu'on contacte sont en mode urgence pour la conformite. Celles qui ont commence il y a 6 mois sont tranquilles. Celles qui commencent maintenant sont stressees.\n\nOn a aide 8 fintechs a passer leurs audits de conformite du premier coup cette annee.\n\nCa serait utile de comparer votre setup actuel avec ce qu'on voit habituellement ?\n\nCordialement,\nSarah"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Angle conformite ou infrastructure',desc:'Commencez par le declencheur reglementaire le plus pertinent.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'"J\'ai vu que {{company}} navigue MiCA. Je vous ai envoye quelque chose de pertinent."'},
    {day:'Jour 5',ch:'linkedin',action:'Partager une mise a jour reglementaire',desc:'Postez ou envoyez en DM une actualite reglementaire pertinente. Positionnez-vous comme expert.'},
    {day:'Jour 8',ch:'email',action:'Intelligence concurrentielle',desc:"Partagez quelque chose qu'ils ne savaient pas sur l'approche d'un concurrent."},
    {day:'Jour 11',ch:'linkedin',action:'Envoyer message',desc:'"Vous suivez comment [concurrent] gere le calendrier de conformite ?"'},
    {day:'Jour 14',ch:'email',action:'Etude de cas',desc:'Fintech similaire, resultat conformite precis.'},
    {day:'Jour 20',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'41%',reply:'2.8%',meeting:'0.9%',close:'20%'},
  objections:[
    {q:'"On gere la conformite en interne"',a:"La plupart des entreprises le font jusqu'a ce qu'elles ratent un audit. Demandez : <em>a quand remonte votre dernier audit externe ?</em> Les entreprises qui passent systematiquement ont des partenaires externes qui valident leur approche."},
    {q:'"On est trop tot pour l\'outbound"',a:"Si vous etes post-seed, vous avez besoin de pipeline. <em>L'outbound est le chemin le plus rapide de zero a des rendez-vous previsibles.</em> Le contenu prend 6-12 mois. L'outbound prend 3 semaines."}
  ]
},
{id:'recruiting',slug:'recrutement-staffing',cat:'Professionnel',title:'Recrutement & Staffing',desc:"Vendez aux entreprises qui recrutent a grande echelle. Marche rapide, relationnel, logique de volume.",
  stats:{open:'42%',reply:'5.5%',meetings:'16/mois'},
  icp:[{l:'Titres',v:'VP RH, Head of Talent, CEO (startups), DRH'},{l:'Taille entreprise',v:'50-2000 employes'},{l:'Declencheur',v:'10+ postes ouverts, nouveau bureau, changement de direction'},{l:'Industries cibles',v:'Tech, sante, services professionnels'},{l:'Signal budget',v:"Offres d'emploi actives sur LinkedIn/Indeed"},{l:'Geographie',v:"Principaux marches de l'emploi"}],
  angles:[
    {name:'Velocite de recrutement',desc:'"Vous avez 23 postes ouverts en ce moment. La plupart des entreprises a cette echelle galere sur le time-to-fill."',why:"Chiffre precis de leur site emploi. Montre que vous avez fait la recherche."},
    {name:'Cout par recrutement',desc:'"Le cout moyen par embauche dans [industrie] est de 4 700 EUR. Nos clients sont a 2 100 EUR en moyenne."',why:"Les RH parlent le langage du cout par embauche. Battez le benchmark et ils ecouteront."},
    {name:'Candidats passifs',desc:'"80% des meilleurs candidats ne cherchent pas activement. Voici comment on les atteint."',why:"Tous les recruteurs connaissent cette stat. Peu ont une solution."}
  ],
  templates:[
    {name:'Velocite de recrutement',score:88,subject:'Les 23 postes ouverts de {{company}}',body:"Bonjour {{firstName}},\n\nJ'ai remarque que {{company}} a 23 postes ouverts en ce moment en engineering et sales. A ce volume, le time-to-fill explose generalement a 60+ jours.\n\nOn aide les entreprises a reduire le time-to-fill de 40% en atteignant des candidats passifs qui ne sont pas sur les job boards. Moyenne : 12 candidats qualifies par poste par mois.\n\n15 min pour voir si ca colle ?\n\nJohn"}
  ],
  sequence:[
    {day:'Jour 1',ch:'email',action:'Velocite de recrutement',desc:'Referencez leurs postes ouverts specifiques.'},
    {day:'Jour 2',ch:'linkedin',action:'Connecter',desc:'"J\'ai vu que {{company}} recrute agressivement. Je vous ai envoye une note sur le sourcing de candidats passifs."'},
    {day:'Jour 4',ch:'linkedin',action:'Engager avec le contenu RH',desc:'Commentez leurs posts marque employeur. Montrez que vous comprenez leur culture.'},
    {day:'Jour 5',ch:'email',action:'Cout par recrutement',desc:'Comparaison benchmark avec chiffres precis.'},
    {day:'Jour 8',ch:'linkedin',action:'Envoyer message',desc:'"Question rapide : vous trouvez que c\'est plus dur de sourcer des [type de poste] ce trimestre vs le dernier ?"'},
    {day:'Jour 10',ch:'email',action:'Etude de cas',desc:'Entreprise similaire, reduction du time-to-fill.'},
    {day:'Jour 15',ch:'email',action:'Breakup',desc:'Cloture propre.'}
  ],
  benchmarks:{open:'42%',reply:'5.5%',meeting:'2.3%',close:'20%'},
  objections:[
    {q:'"On utilise un ATS qui gere le sourcing"',a:"Le sourcing ATS a un taux de reponse de 2%. <em>Le cold email bien fait obtient 5-8%.</em> La difference : la personnalisation, le sequencage et la delivrabilite. Votre ATS envoie en masse. Nous ciblons."}
  ]
}
];

// ============================================================
// RELATED PLAYBOOKS LOGIC
// ============================================================
function getRelated(slug, allPlaybooks) {
  const current = allPlaybooks.find(p => p.slug === slug);
  if (!current) return allPlaybooks.filter(p => p.slug !== slug).slice(0, 4);
  // Prefer same category first, then others
  const sameCategory = allPlaybooks.filter(p => p.slug !== slug && p.cat === current.cat);
  const diffCategory = allPlaybooks.filter(p => p.slug !== slug && p.cat !== current.cat);
  return [...sameCategory, ...diffCategory].slice(0, 4);
}

// ============================================================
// ESCAPE HTML HELPER
// ============================================================
function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

// Truncate for meta descriptions
function metaDesc(desc, extra) {
  const full = desc + (extra ? ' ' + extra : '');
  if (full.length <= 155) return full;
  return full.substring(0, 152) + '...';
}

// ============================================================
// PAGE TEMPLATE
// ============================================================
function buildPage(p, lang, allPlaybooks) {
  const isEn = lang === 'en';
  const related = getRelated(p.slug, allPlaybooks);
  const canonical = isEn
    ? `https://overloop.com/playbooks/${p.slug}`
    : `https://overloop.com/playbooks/fr/${p.slug}`;
  const enSlug = isEn ? p.slug : EN_PLAYBOOKS.find(e => e.id === p.id)?.slug || p.slug;
  const frSlug = isEn ? FR_PLAYBOOKS.find(f => f.id === p.id)?.slug || p.slug : p.slug;
  const hrefEn = `https://overloop.com/playbooks/${enSlug}`;
  const hrefFr = `https://overloop.com/playbooks/fr/${frSlug}`;

  // Title: keep under 60 chars
  let pageTitle = isEn
    ? `${p.title} Cold Email Playbook | Overloop`
    : `Playbook Cold Email ${p.title} | Overloop`;
  if (pageTitle.length > 60) {
    pageTitle = isEn
      ? `${p.title} Playbook | Overloop`
      : `Playbook ${p.title} | Overloop`;
  }
  if (pageTitle.length > 60) {
    pageTitle = `${p.title} | Overloop`;
  }

  const description = metaDesc(
    p.desc,
    isEn
      ? `ICP, messaging angles, email sequences, templates, benchmarks. ${p.stats.open} open rate, ${p.stats.reply} reply rate.`
      : `ICP, angles de messaging, sequences email, templates, benchmarks. ${p.stats.open} taux d'ouverture, ${p.stats.reply} taux de reponse.`
  );

  const l = {
    whoToTarget: isEn ? 'Who to target' : 'Qui cibler',
    anglesTitle: isEn ? 'Messaging angles that work' : 'Angles de messaging qui fonctionnent',
    anglesDesc: isEn
      ? 'These are the 3 approaches that consistently get replies in this vertical. Pick the one that fits your prospect best.'
      : 'Voici les 3 approches qui obtiennent des reponses de maniere constante dans ce vertical. Choisissez celle qui correspond le mieux a votre prospect.',
    whyWorks: isEn ? 'Why it works:' : 'Pourquoi ca marche :',
    sequenceTitle: isEn ? `The ${p.sequence.length}-step sequence` : `La sequence en ${p.sequence.length} etapes`,
    sequenceDesc: isEn
      ? `Email + LinkedIn, orchestrated over ${p.sequence[p.sequence.length-1].day.replace('Day ','').trim()} days. The channel alternation is what makes this work.`
      : `Email + LinkedIn, orchestre sur ${p.sequence[p.sequence.length-1].day.replace('Jour ','').trim()} jours. C'est l'alternance de canaux qui fait fonctionner cette approche.`,
    templatesTitle: isEn ? 'Ready-to-use templates' : 'Templates prets a l\'emploi',
    templatesDesc: isEn
      ? 'Copy these directly into your campaign. Each one is pre-scored for deliverability.'
      : 'Copiez-les directement dans votre campagne. Chacun est pre-score en delivrabilite.',
    copyEmail: isEn ? 'Copy email' : 'Copier l\'email',
    subjectLabel: isEn ? 'Subject' : 'Objet',
    scoreLabel: isEn ? 'Score' : 'Score',
    objectionsTitle: isEn ? 'When they push back' : 'Quand ils repoussent',
    objectionsDesc: isEn
      ? 'The most common objections in this vertical and exactly what to say.'
      : 'Les objections les plus courantes dans ce vertical et exactement quoi repondre.',
    ctaTitle: isEn ? 'Run this playbook in <em>Overloop</em>' : 'Lancez ce playbook dans <em>Overloop</em>',
    ctaDesc: isEn
      ? 'Every template is ready to paste into a campaign. First meetings in 3 weeks.'
      : 'Chaque template est pret a coller dans une campagne. Premiers rendez-vous en 3 semaines.',
    ctaBtn: isEn ? 'Try Overloop free' : 'Essayer Overloop gratuitement',
    relatedTitle: isEn ? 'More playbooks' : 'Autres playbooks',
    readPlaybook: isEn ? 'Read playbook' : 'Lire le playbook',
    openRate: isEn ? 'open rate' : 'taux d\'ouverture',
    replyRate: isEn ? 'reply rate' : 'taux de reponse',
    meetings: isEn ? 'meetings' : 'rendez-vous',
    meetingRate: isEn ? 'meeting rate' : 'taux de rendez-vous',
    closeRate: isEn ? 'close rate' : 'taux de closing',
    avgOpen: isEn ? 'avg open rate' : 'taux d\'ouverture moy.',
    avgReply: isEn ? 'avg reply rate' : 'taux de reponse moy.',
    breadcrumbHome: 'Overloop',
    breadcrumbPlaybooks: isEn ? 'Playbooks' : 'Playbooks',
    backToAll: isEn ? 'All playbooks' : 'Tous les playbooks',
    backLink: isEn ? '/playbooks/' : '/playbooks/fr/',
  };

  const seqLastDay = p.sequence[p.sequence.length-1].day;

  return `<!DOCTYPE html>
<html lang="${lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(pageTitle)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${canonical}">
<link rel="alternate" hreflang="en" href="${hrefEn}">
<link rel="alternate" hreflang="fr" href="${hrefFr}">
<link rel="alternate" hreflang="x-default" href="${hrefEn}">
<link rel="stylesheet" href="/assets/css/overloop.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
.pb-hero{text-align:center;max-width:720px;margin:0 auto 3rem;padding-top:2rem}
.pb-hero h1{font-size:clamp(28px,4vw,42px);font-weight:800;line-height:1.15;margin-bottom:16px}
.pb-hero h1 em{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:400}
.pb-hero .subtitle{font-size:1.05rem;color:#6B7280;line-height:1.6;max-width:560px;margin:0 auto 2rem}
.pb-breadcrumb{font-size:13px;color:#9CA3AF;margin-bottom:12px}
.pb-breadcrumb a{color:#7C3AED;text-decoration:none}
.pb-breadcrumb a:hover{text-decoration:underline}
.bench-row{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:560px;margin:0 auto}
@media(min-width:640px){.bench-row{grid-template-columns:repeat(4,1fr)}}
.bench-card{background:#fff;border:1px solid #F3F4F6;border-radius:10px;padding:18px 12px;text-align:center}
.bench-num{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:#7C3AED}
.bench-label{font-size:11px;color:#9CA3AF;margin-top:4px}
.pb-content{max-width:720px;margin:0 auto}
.pb-section{padding:48px 0;border-top:1px solid #F3F4F6}
.pb-section:first-of-type{border-top:none;padding-top:0}
.pb-section-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#9CA3AF;margin-bottom:20px}
.pb-section-desc{font-size:14px;color:#6B7280;line-height:1.6;margin-bottom:20px}
.pb-section--shaded{background:#F3F4F6;margin-left:-24px;margin-right:-24px;padding-left:24px;padding-right:24px;border-radius:12px;border-top:none}
@media(min-width:640px){.pb-section--shaded{margin-left:-32px;margin-right:-32px;padding-left:32px;padding-right:32px}}
.icp-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
@media(min-width:640px){.icp-grid{grid-template-columns:repeat(3,1fr)}}
.icp-item{background:#fff;border:1px solid #F3F4F6;border-radius:8px;padding:14px}
.icp-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:#9CA3AF;margin-bottom:6px}
.icp-val{font-size:15px;font-weight:600;line-height:1.4}
.angle-card{background:#fff;border:1px solid #F3F4F6;border-radius:10px;padding:20px;margin-bottom:12px}
.angle-name{font-weight:700;font-size:15px;margin-bottom:6px}
.angle-desc{font-size:14px;color:#6B7280;line-height:1.6}
.angle-why{font-size:13px;color:#6B7280;margin-top:10px;padding:12px 14px;background:#F9FAFB;border-left:3px solid #7C3AED;border-radius:0 8px 8px 0;line-height:1.5}
.angle-why strong{color:#1F2937;font-weight:700}
.seq-timeline{display:flex;flex-direction:column;gap:4px}
.seq-step{display:grid;grid-template-columns:48px 1fr;gap:0 16px;padding:16px 20px;border-radius:10px;align-items:start}
.seq-step--email{background:#FAFAFF}
.seq-step--linkedin{background:#F8FBFF}
.seq-icon{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;grid-row:span 3;align-self:start}
.seq-icon-email{background:#EDE9FE}
.seq-icon-linkedin{background:#DBEAFE}
.seq-day{font-family:'JetBrains Mono',monospace;font-size:11px;color:#9CA3AF}
.seq-action{font-weight:600;font-size:14px;margin-top:2px}
.seq-desc{font-size:13px;color:#6B7280;margin-top:4px;line-height:1.5}
.pb-tpl{background:#fff;border:1px solid #F3F4F6;border-radius:12px;padding:1.5rem;margin-bottom:14px}
.pb-tpl-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.pb-tpl-name{font-weight:700;font-size:15px}
.pb-tpl-score{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:#10B981}
.pb-tpl-subject{font-family:'JetBrains Mono',monospace;font-size:12px;color:#6B7280;margin-bottom:8px;padding:8px 12px;background:#FAFAFA;border-radius:6px}
.pb-tpl-body{font-size:13.5px;line-height:1.75;white-space:pre-wrap;color:#4B5563}
.pb-tpl-copy{display:inline-flex;align-items:center;gap:6px;margin-top:12px;padding:8px 16px;border-radius:8px;font-size:12px;font-weight:600;background:#F3F4F6;color:#1F2937;border:none;cursor:pointer;font-family:inherit;transition:all 150ms}
.pb-tpl-copy:hover{background:#7C3AED;color:#fff}
.obj-card{margin-bottom:8px;border:1px solid #F3F4F6;border-radius:10px;overflow:hidden}
.obj-q{padding:16px 20px;font-weight:600;font-size:14px;background:#fff;cursor:pointer;display:flex;justify-content:space-between;align-items:center}
.obj-q::after{content:'+';font-size:18px;color:#9CA3AF;transition:transform 200ms}
.obj-q.open::after{content:'\\2212'}
.obj-a{padding:0 20px 16px;font-size:14px;color:#6B7280;line-height:1.6;display:none;background:#fff}
.obj-a.open{display:block}
.obj-a em{color:#1F2937;font-style:normal;font-weight:700}
.pb-cta-block{text-align:center;padding:3rem 2rem;background:linear-gradient(135deg,#1F2937,#111827);border-radius:16px;color:#fff;margin:3rem 0}
.pb-cta-block h2{font-size:1.5rem;font-weight:700;margin-bottom:8px}
.pb-cta-block h2 em{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:400}
.pb-cta-block p{opacity:.8;margin-bottom:20px;font-size:15px}
.pb-cta-btn{display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#7C3AED,#5B21B6);color:#fff;padding:14px 32px;border:none;border-radius:12px;font-size:1rem;font-weight:600;cursor:pointer;text-decoration:none;box-shadow:0 0 40px rgba(124,58,237,0.25);transition:all 200ms}
.pb-cta-btn:hover{box-shadow:0 0 60px rgba(124,58,237,0.4);transform:translateY(-2px)}
.related-grid{display:grid;grid-template-columns:1fr;gap:14px;margin-top:20px}
@media(min-width:640px){.related-grid{grid-template-columns:repeat(2,1fr)}}
.related-card{background:#fff;border:1px solid #E5E7EB;border-top:3px solid #E5E7EB;border-radius:12px;padding:20px;text-decoration:none;color:inherit;transition:all 200ms;display:block}
.related-card:hover{border-top-color:#7C3AED;box-shadow:0 8px 24px rgba(0,0,0,0.06);transform:translateY(-2px)}
.related-card .r-cat{font-size:11px;font-weight:600;color:#6B7280;margin-bottom:6px}
.related-card .r-title{font-size:16px;font-weight:700;margin-bottom:4px}
.related-card .r-desc{font-size:13px;color:#6B7280;line-height:1.5}
.related-card .r-stats{display:flex;gap:16px;margin-top:12px;font-size:12px;color:#9CA3AF}
.related-card .r-stats strong{color:#1F2937;font-weight:700}
</style>
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "${esc(pageTitle.replace(' | Overloop',''))}",
    "description": "${esc(description)}",
    "url": "${canonical}",
    "publisher": {
      "@type": "Organization",
      "name": "Overloop",
      "url": "https://overloop.com"
    }
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "${l.breadcrumbHome}", "item": "https://overloop.com"},
      {"@type": "ListItem", "position": 2, "name": "${l.breadcrumbPlaybooks}", "item": "https://overloop.com${l.backLink}"},
      {"@type": "ListItem", "position": 3, "name": "${esc(p.title)}"}
    ]
  }
]
</script>
</head>
<body>

${NAV}

<main class="article-container" style="max-width:840px;margin:0 auto;padding:0 20px">

<div class="pb-hero">
  <div class="pb-breadcrumb"><a href="https://overloop.com">${l.breadcrumbHome}</a> / <a href="${l.backLink}">${l.breadcrumbPlaybooks}</a> / ${esc(p.title)}</div>
  <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:#9CA3AF;margin-bottom:12px">${esc(p.cat)}</div>
  <h1>${isEn ? 'Cold Email Playbook:' : 'Playbook Cold Email :'} <em>${esc(p.title)}</em></h1>
  <p class="subtitle">${esc(p.desc)}</p>
  <div class="bench-row">
    <div class="bench-card"><div class="bench-num">${p.benchmarks.open}</div><div class="bench-label">${l.avgOpen}</div></div>
    <div class="bench-card"><div class="bench-num">${p.benchmarks.reply}</div><div class="bench-label">${l.avgReply}</div></div>
    <div class="bench-card"><div class="bench-num">${p.benchmarks.meeting}</div><div class="bench-label">${l.meetingRate}</div></div>
    <div class="bench-card"><div class="bench-num">${p.benchmarks.close}</div><div class="bench-label">${l.closeRate}</div></div>
  </div>
</div>

<div class="pb-content">

<!-- ICP -->
<div class="pb-section pb-section--shaded">
  <h2 class="pb-section-title">${l.whoToTarget}</h2>
  <div class="icp-grid">
    ${p.icp.map(i => `<div class="icp-item"><div class="icp-label">${esc(i.l)}</div><div class="icp-val">${esc(i.v)}</div></div>`).join('\n    ')}
  </div>
</div>

<!-- Angles -->
<div class="pb-section">
  <h2 class="pb-section-title">${l.anglesTitle}</h2>
  <p class="pb-section-desc">${l.anglesDesc}</p>
  ${p.angles.map((a, i) => `<div class="angle-card">
    <div class="angle-name">${i+1}. ${esc(a.name)}</div>
    <div class="angle-desc">${a.desc}</div>
    <div class="angle-why"><strong>${l.whyWorks}</strong> ${a.why}</div>
  </div>`).join('\n  ')}
</div>

<!-- Sequence -->
<div class="pb-section pb-section--shaded">
  <h2 class="pb-section-title">${l.sequenceTitle}</h2>
  <p class="pb-section-desc">${l.sequenceDesc}</p>
  <div class="seq-timeline">
    ${p.sequence.map(s => {
      const isLi = s.ch === 'linkedin';
      return `<div class="seq-step seq-step--${isLi ? 'linkedin' : 'email'}">
      <div class="seq-icon seq-icon-${isLi ? 'linkedin' : 'email'}">${isLi ? '\uD83D\uDCBC' : '\u2709\uFE0F'}</div>
      <div class="seq-day">${esc(s.day)}</div>
      <div class="seq-action">${esc(s.action)}</div>
      <div class="seq-desc">${esc(s.desc)}</div>
    </div>`;
    }).join('\n    ')}
  </div>
</div>

<!-- Templates -->
<div class="pb-section">
  <h2 class="pb-section-title">${l.templatesTitle}</h2>
  <p class="pb-section-desc">${l.templatesDesc}</p>
  ${p.templates.map(t => `<div class="pb-tpl">
    <div class="pb-tpl-header">
      <div class="pb-tpl-name">${esc(t.name)}</div>
      <div class="pb-tpl-score">${l.scoreLabel}: ${t.score}/100</div>
    </div>
    <div class="pb-tpl-subject">${l.subjectLabel}: ${esc(t.subject)}</div>
    <div class="pb-tpl-body">${esc(t.body)}</div>
    <button class="pb-tpl-copy" onclick="navigator.clipboard.writeText(this.closest('.pb-tpl').querySelector('.pb-tpl-body').textContent);this.textContent='Copied!';setTimeout(()=>this.textContent='${l.copyEmail}',2000)">${l.copyEmail}</button>
  </div>`).join('\n  ')}
</div>

<!-- Objections -->
<div class="pb-section">
  <h2 class="pb-section-title">${l.objectionsTitle}</h2>
  <p class="pb-section-desc">${l.objectionsDesc}</p>
  ${p.objections.map(o => `<div class="obj-card">
    <div class="obj-q" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open')">${o.q}</div>
    <div class="obj-a">${o.a}</div>
  </div>`).join('\n  ')}
</div>

<!-- CTA -->
<div class="pb-cta-block">
  <h2>${l.ctaTitle}</h2>
  <p>${l.ctaDesc}</p>
  <a href="https://app.overloop.ai/session/signup" class="pb-cta-btn">${l.ctaBtn}</a>
</div>

<!-- Related -->
<div class="pb-section">
  <h2 class="pb-section-title">${l.relatedTitle}</h2>
  <div class="related-grid">
    ${related.map(r => {
      const rLink = isEn ? `/playbooks/${r.slug}` : `/playbooks/fr/${r.slug}`;
      return `<a href="${rLink}" class="related-card">
      <div class="r-cat">${esc(r.cat)}</div>
      <div class="r-title">${esc(r.title)}</div>
      <div class="r-desc">${esc(r.desc)}</div>
      <div class="r-stats"><span>${l.openRate}: <strong>${r.stats.open}</strong></span><span>${l.replyRate}: <strong>${r.stats.reply}</strong></span></div>
    </a>`;
    }).join('\n    ')}
  </div>
</div>

</div><!-- /pb-content -->
</main>

${FOOTER}

</body>
</html>`;
}

// ============================================================
// INDEX PAGE TEMPLATE
// ============================================================
function buildIndex(lang, playbooks) {
  const isEn = lang === 'en';
  const canonical = isEn ? 'https://overloop.com/playbooks/' : 'https://overloop.com/playbooks/fr/';
  const pageTitle = isEn
    ? 'Cold Email Playbooks by Industry | Overloop'
    : 'Playbooks Cold Email par Industrie | Overloop';
  const description = isEn
    ? 'Complete outbound playbooks for 14 industries. ICP, messaging angles, email templates, sequences, benchmarks. Built for agencies and B2B teams.'
    : 'Playbooks outbound complets pour 14 industries. ICP, angles de messaging, templates email, sequences, benchmarks. Concu pour les agences et equipes B2B.';

  const agencies = playbooks.filter(p => p.cat === (isEn ? 'Agencies' : 'Agences'));
  const industries = playbooks.filter(p => p.cat !== (isEn ? 'Agencies' : 'Agences'));

  const l = {
    heroTitle: isEn ? 'Outbound playbooks for <em>every industry</em>' : 'Playbooks outbound pour <em>chaque industrie</em>',
    heroDesc: isEn
      ? 'Complete multi-channel strategies. ICP, messaging angles, email + LinkedIn sequences, templates, benchmarks. Pick yours, run it.'
      : 'Strategies multicanal completes. ICP, angles de messaging, sequences email + LinkedIn, templates, benchmarks. Choisissez le votre, lancez-le.',
    agenciesLabel: isEn ? 'For agencies' : 'Pour les agences',
    agenciesDesc: isEn ? 'Sell outbound as a service. White-label, resell, keep the margin.' : "Vendez l'outbound en tant que service. White-label, revendez, gardez la marge.",
    industriesLabel: isEn ? 'By industry' : 'Par industrie',
    industriesDesc: isEn ? "Outbound strategies adapted to each vertical's buying patterns." : "Strategies outbound adaptees aux cycles d'achat de chaque vertical.",
    readPlaybook: isEn ? 'Read playbook' : 'Lire le playbook',
    openRate: isEn ? 'open rate' : "taux d'ouverture",
    replyRate: isEn ? 'reply rate' : 'taux de reponse',
    meetingsLabel: isEn ? 'meetings' : 'rendez-vous',
    ctaTitle: isEn ? 'Pick a playbook. Run it in <em>Overloop.</em>' : 'Choisissez un playbook. Lancez-le dans <em>Overloop.</em>',
    ctaDesc: isEn ? 'Every template is ready to paste into a campaign. First meetings in 3 weeks.' : 'Chaque template est pret a coller dans une campagne. Premiers rendez-vous en 3 semaines.',
    ctaBtn: isEn ? 'Try Overloop free' : 'Essayer Overloop gratuitement',
  };

  function card(p) {
    const link = isEn ? `/playbooks/${p.slug}` : `/playbooks/fr/${p.slug}`;
    return `<a href="${link}" class="idx-card">
      <div class="idx-cat">${esc(p.cat)}</div>
      <div class="idx-title">${esc(p.title)}</div>
      <div class="idx-desc">${esc(p.desc)}</div>
      <div class="idx-stats">
        <div class="idx-stat"><div class="idx-stat-val">${p.stats.open}</div><div class="idx-stat-label">${l.openRate}</div></div>
        <div class="idx-stat"><div class="idx-stat-val">${p.stats.reply}</div><div class="idx-stat-label">${l.replyRate}</div></div>
        <div class="idx-stat"><div class="idx-stat-val">${p.stats.meetings}</div><div class="idx-stat-label">${l.meetingsLabel}</div></div>
      </div>
      <div class="idx-cta">${l.readPlaybook} &rarr;</div>
    </a>`;
  }

  return `<!DOCTYPE html>
<html lang="${lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(pageTitle)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${canonical}">
<link rel="alternate" hreflang="en" href="https://overloop.com/playbooks/">
<link rel="alternate" hreflang="fr" href="https://overloop.com/playbooks/fr/">
<link rel="alternate" hreflang="x-default" href="https://overloop.com/playbooks/">
<link rel="stylesheet" href="/assets/css/overloop.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
.idx-hero{text-align:center;max-width:720px;margin:0 auto;padding:3rem 0 2rem}
.idx-hero h1{font-size:clamp(28px,4.5vw,44px);font-weight:800;line-height:1.15;margin-bottom:14px}
.idx-hero h1 em{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:400}
.idx-hero p{font-size:1.05rem;color:#6B7280;max-width:560px;margin:0 auto}
.idx-section{max-width:960px;margin:0 auto 3rem}
.idx-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#7C3AED;margin-bottom:4px}
.idx-subtitle{font-size:15px;color:#6B7280;margin-bottom:20px}
.idx-grid{display:grid;grid-template-columns:1fr;gap:16px}
@media(min-width:640px){.idx-grid{grid-template-columns:repeat(2,1fr);gap:20px}}
@media(min-width:900px){.idx-grid{grid-template-columns:repeat(3,1fr)}}
.idx-card{background:#fff;border:1px solid #E5E7EB;border-top:3px solid #E5E7EB;border-radius:12px;padding:24px 20px 20px;text-decoration:none;color:inherit;transition:all 200ms;display:flex;flex-direction:column}
.idx-card:hover{border-top-color:#7C3AED;box-shadow:0 8px 30px rgba(0,0,0,0.08);transform:translateY(-3px)}
.idx-cat{font-size:11px;font-weight:600;color:#6B7280;margin-bottom:8px}
.idx-title{font-size:17px;font-weight:700;margin-bottom:6px}
.idx-desc{font-size:14px;color:#6B7280;line-height:1.55;margin-bottom:20px;flex:1}
.idx-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:0;padding-top:14px;border-top:1px solid #F3F4F6;margin-bottom:14px}
.idx-stat{text-align:center}
.idx-stat:not(:last-child){border-right:1px solid #F3F4F6}
.idx-stat-val{font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:700;color:#1F2937}
.idx-stat-label{font-size:11px;color:#9CA3AF;margin-top:2px}
.idx-cta{font-size:13px;font-weight:600;color:#1F2937;display:inline-flex;align-items:center;gap:4px;transition:gap 200ms,color 200ms}
.idx-card:hover .idx-cta{gap:8px;color:#7C3AED}
.idx-cta-block{text-align:center;padding:3rem 2rem;background:linear-gradient(135deg,#1F2937,#111827);border-radius:16px;color:#fff;margin:2rem auto 3rem;max-width:800px}
.idx-cta-block h2{font-size:1.35rem;font-weight:700;margin-bottom:6px}
.idx-cta-block h2 em{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:400}
.idx-cta-block p{opacity:.8;margin-bottom:18px;font-size:14px}
.idx-cta-btn{display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#7C3AED,#5B21B6);color:#fff;padding:14px 32px;border:none;border-radius:12px;font-size:1rem;font-weight:600;cursor:pointer;text-decoration:none;box-shadow:0 0 40px rgba(124,58,237,0.25);transition:all 200ms}
.idx-cta-btn:hover{box-shadow:0 0 60px rgba(124,58,237,0.4);transform:translateY(-2px)}
</style>
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "${esc(pageTitle.replace(' | Overloop',''))}",
    "description": "${esc(description)}",
    "url": "${canonical}",
    "publisher": {"@type": "Organization", "name": "Overloop", "url": "https://overloop.com"}
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Overloop", "item": "https://overloop.com"},
      {"@type": "ListItem", "position": 2, "name": "${isEn ? 'Playbooks' : 'Playbooks'}"}
    ]
  }
]
</script>
</head>
<body>

${NAV}

<main class="article-container" style="max-width:1060px;margin:0 auto;padding:0 20px">

<div class="idx-hero">
  <h1>${l.heroTitle}</h1>
  <p>${l.heroDesc}</p>
</div>

<div class="idx-section">
  <div class="idx-label">${l.agenciesLabel}</div>
  <div class="idx-subtitle">${l.agenciesDesc}</div>
  <div class="idx-grid">
    ${agencies.map(card).join('\n    ')}
  </div>
</div>

<div class="idx-section">
  <div class="idx-label">${l.industriesLabel}</div>
  <div class="idx-subtitle">${l.industriesDesc}</div>
  <div class="idx-grid">
    ${industries.map(card).join('\n    ')}
  </div>
</div>

<div class="idx-cta-block">
  <h2>${l.ctaTitle}</h2>
  <p>${l.ctaDesc}</p>
  <a href="https://app.overloop.ai/session/signup" class="idx-cta-btn">${l.ctaBtn}</a>
</div>

</main>

${FOOTER}

</body>
</html>`;
}

// ============================================================
// GENERATE ALL FILES
// ============================================================
const OUT_DIR = path.join(__dirname);
const FR_DIR = path.join(OUT_DIR, 'fr');

// Ensure fr dir exists
if (!fs.existsSync(FR_DIR)) fs.mkdirSync(FR_DIR, { recursive: true });

let count = 0;

// EN individual pages
EN_PLAYBOOKS.forEach(p => {
  const html = buildPage(p, 'en', EN_PLAYBOOKS);
  fs.writeFileSync(path.join(OUT_DIR, `${p.slug}.html`), html);
  count++;
  console.log(`EN: ${p.slug}.html`);
});

// FR individual pages
FR_PLAYBOOKS.forEach(p => {
  const html = buildPage(p, 'fr', FR_PLAYBOOKS);
  fs.writeFileSync(path.join(FR_DIR, `${p.slug}.html`), html);
  count++;
  console.log(`FR: fr/${p.slug}.html`);
});

// EN index
fs.writeFileSync(path.join(OUT_DIR, 'index.html'), buildIndex('en', EN_PLAYBOOKS));
count++;
console.log('EN: index.html');

// FR index
fs.writeFileSync(path.join(FR_DIR, 'index.html'), buildIndex('fr', FR_PLAYBOOKS));
count++;
console.log('FR: fr/index.html');

console.log(`\nDone. ${count} files created.`);
