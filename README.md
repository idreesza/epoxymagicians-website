# Epoxy Magicians — Website

Fast, static, semantic HTML/CSS site for **epoxymagicians.com** (epoxy flooring, Dallas–Fort Worth).
No framework, no build step, no render-blocking JS. Deploy the folder as-is.

## What's built — full site (34 pages)

| Section | Pages |
|---|---|
| Homepage | `index.html` — hero + above-fold quote form, trust bar, before/after slider, service cards, city grid, testimonials, FAQ, sticky mobile call bar |
| Services | `/services/` hub + all **9** service pages (garage, metallic, flake, polyaspartic, commercial/industrial, concrete polishing, patio/pool deck, driveway, basement) |
| Service areas | `/service-areas/` hub + all **13** city pages (Dallas, Fort Worth, Arlington, Plano, Frisco, McKinney, Irving, Grand Prairie, Southlake, Flower Mound, Denton, Mansfield, Rockwall) |
| Support pages | `/gallery/`, `/about/`, `/reviews/`, `/faq/`, `/blog/` (+1 full sample post), `/contact/`, `/thank-you/`, `/privacy/` |
| Infra | `assets/css/styles.css` (shared, async-loaded), `robots.txt`, `sitemap.xml` (all 34 URLs) |

Every service and city page has genuinely unique copy — real neighborhoods, real slab/soil notes, distinct pricing color — not a find-and-replace template. Full JSON-LD (LocalBusiness/Service, FAQPage, BreadcrumbList, Article) is inline on every page and validates as well-formed JSON (checked programmatically). Critical CSS is inlined in each page's `<head>`; the rest loads async via `media="print" onload`. Every page has exactly one H1 and zero broken internal links (also checked programmatically).

The `_gen/` folder holds the Python generator used to produce the 8 service + 12 city pages from structured content data (`services_data.py`, `cities_data.py`) — it's a build tool, not part of the shipped site. Re-run `python _gen/render.py` from `_gen/` after editing that data if you want to regenerate those pages.

---

## ⚠️ BEFORE LAUNCH — replace every placeholder

Search the whole project for `[[` and replace:

| Token | Replace with |
|---|---|
| ~~`[[PHONE]]` / `[[PHONE_E164]]`~~ | ✅ Done — (254) 435-5877 baked in everywhere via `_data/business.json` |
| `[[LICENSE]]` | Real contractor license # |
| `[[INSURANCE]]` | Insurance carrier + coverage |
| `[[YEARS]]` | Real years in business |
| `[[JOBS]]` | Completed-jobs count |
| `[[GRATING]]` / `[[GREVIEWS]]` | Real Google rating + review count |
| `[[Name]]`, review text | **Real** Google reviews (name + city) |
| `[[FINANCING_PARTNER]]` | Financing provider name |

⚠️ **Do NOT ship fake license #, fake review counts, or fake ratings in the JSON-LD** — that's a schema/GBP trust violation and can get you penalized. Leave `aggregateRating` out entirely until you have real reviews.

### Images (replace every file in `/assets/img/`)
All `<img>` tags already have explicit `width`/`height` (prevents CLS), `srcset`, and `loading="lazy"` below the fold. You only need to drop in **real WebP photos** at the referenced names/sizes. Never use stock photography.
- `hero-garage-metallic-{800,1600}.webp` — homepage LCP image
- `ba-before-800.webp` / `ba-after-800.webp` — real before/after pair
- `garage-epoxy-{800,1600}.webp`, `plano-{800,1600}.webp` — page heroes
- `og-cover.jpg` + per-page `*-og.jpg` — social share images (1200×630)

Export tip: `cwebp -q 78 input.jpg -o output.webp` (or Squoosh). Target hero < 120 KB.

---

## Still to build

**More blog posts** — only "How Long Does Garage Epoxy Last in Texas Heat?" is written. `/blog/index.html` has 5 more teaser cards (marked "Coming soon" and unlinked) for: cost guide, epoxy vs. polyaspartic, why DIY fails, maintenance, and choosing a commercial system. Write each as a full page before linking it live.

**Real photography** — every page ships with placeholder image paths (see Images section above). This is the biggest remaining gap between "structurally complete" and "launch ready."

> Every city page already has genuinely unique content (real neighborhoods, a local slab/soil note, distinct pricing color) — this is what keeps them from reading as doorway-spam duplicates. Don't let anyone "simplify" them back into a single template later.

---

## Security headers (`vercel.json`)

CSP, HSTS, X-Frame-Options, COOP, X-Content-Type-Options and Referrer-Policy are set at the hosting level in `vercel.json` (not HTML meta tags, since `frame-ancestors`/HSTS aren't enforceable via `<meta>`). Two things to know before you change site architecture:

- **`script-src`/`style-src` include `'unsafe-inline'`** because every page uses inline critical CSS and inline `<script>` (the before/after slider, JSON-LD, footer year, gallery filter). This is the pragmatic tradeoff for a no-build static site — tightening it to a nonce/hash-based policy would require a build step to inject a fresh nonce per request, which is a real architecture change, not a launch-prep fix.
- **`frame-src` only allows `https://www.google.com`**, for the contact page's embedded map. When you pick a Google reviews widget provider for the `#live-reviews` / `#live-reviews-home` slots (see below), you'll likely need to add that provider's domain to `script-src`/`frame-src` in `vercel.json` — it'll otherwise be silently blocked by CSP.

---

## Domain setup — one manual step still needed

`epoxymagicians.com` and `www.epoxymagicians.com` are both already attached to the Vercel project and DNS-verified (`vercel domains verify <domain>` returns `configured-correctly` for both). **But the live redirect currently points the wrong way**: hitting `https://epoxymagicians.com/` returns a 308 redirect to `www.epoxymagicians.com`, while every canonical tag, JSON-LD `url`/`@id`, the sitemap, and `robots.txt` in this codebase all use the non-www form. That mismatch is exactly the duplicate-content risk to fix before relying on Search Console.

Vercel's bulk `redirects` CLI feature needs a Pro plan (not available on the current tier), so this has to be flipped in the dashboard:

1. Go to **vercel.com/idreeszas-projects/epoxymagicians/settings/domains**.
2. Find `www.epoxymagicians.com` in the list and edit it — there's a per-domain redirect option (redirect to another domain in the project).
3. Set `www.epoxymagicians.com` → redirect to → `epoxymagicians.com`, and make sure `epoxymagicians.com` itself has no redirect (i.e., it's the one actually serving content).
4. Re-check with `curl -I https://epoxymagicians.com/` (expect `200`) and `curl -I https://www.epoxymagicians.com/` (expect a `301`/`308` to the apex) once the change propagates.

---

## Deploy + index (do this launch day)

1. **Deploy** — already done; the project auto-deploys from `git push` to `main` via the connected GitHub repo.
2. **Verify** in [PageSpeed Insights](https://pagespeed.web.dev) — test the live URL (once the redirect above is fixed) and send me the scores; I'll fix any regressions.
3. **Fix the domain redirect** (see above) before submitting anything to Search Console — submitting the non-www sitemap while www serves the actual content will confuse indexing.
4. **Google Search Console** — add `epoxymagicians.com` as a property (domain property, which covers both www and non-www automatically), verify via DNS TXT record, then Sitemaps → submit `https://epoxymagicians.com/sitemap.xml`.
5. **Bing Webmaster Tools** — add the site (Bing can import verification straight from Google Search Console if you connect the same Google account), then Sitemaps → submit the same sitemap URL.
6. **IndexNow** — the key file is already in the repo: `857c8d8740c7779de1180f1914e9f893.txt` (content = the key itself), which needs to be live at `https://epoxymagicians.com/857c8d8740c7779de1180f1914e9f893.txt` for Bing/IndexNow to accept pings. Once the domain redirect is fixed and that key file resolves over HTTPS, ping it for anything new or changed:
   ```bash
   curl "https://api.indexnow.org/indexnow?url=https://epoxymagicians.com/blog/epoxy-flooring-cost-dallas-2026/&key=857c8d8740c7779de1180f1914e9f893"
   ```
   For multiple URLs at once (e.g., right after this launch-prep round), POST a JSON body instead of one `curl` per URL — see the [IndexNow docs](https://www.indexnow.org/documentation) for the batch format.

---

## The real #1-ranking lever (not a code change)

For a local contractor, the **Google Business Profile + reviews** drive the map 3-pack far more than any on-page tweak. Priority order:

1. **Claim & fully build the Google Business Profile** — every service listed, 40+ real photos, correct NAP (must match this site *exactly*), weekly Posts, seeded Q&A.
2. **Review workflow** — text/email every customer within ~2 hours of job completion. Review count + freshness is one of the strongest local signals there is.
3. **Citations (consistent NAP):** Bing Places, Apple Maps, Yelp, BBB, Nextdoor, Angi, HomeAdvisor, Houzz, Thumbtack, Porch, Foursquare, DFW Chamber.
4. **Real backlinks:** local builders/realtors, epoxy-product "certified installer" directories, youth-sports/community sponsorships, DFW home-improvement guest posts, local press for milestones.

## Homepage headline options (A/B test)
- "Epoxy & Metallic Floor Coatings in Dallas–Fort Worth" *(current)*
- "DFW's Garage Floor Experts — One-Day Polyaspartic Install, Backed by a [[YEARS]]-Year Warranty"
- "Garage Floors That Survive Texas Heat — Free Estimates Across Dallas–Fort Worth"
