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
| `[[PHONE]]` | Display phone, e.g. `(214) 555-0100` |
| `[[PHONE_E164]]` | Dialable form, e.g. `+12145550100` (used in every `tel:` link) |
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

## Deploy + index (do this launch day)

1. **Deploy** the folder to any static host with a CDN + HTTPS (Netlify, Vercel, Cloudflare Pages). Ask me to run the `deploy-to-vercel` skill and I'll push it live.
2. **Verify** in [PageSpeed Insights](https://pagespeed.web.dev) — I can only test a live URL, so run it once deployed and send me the scores; I'll fix any regressions.
3. **Search Console + Bing Webmaster Tools** — verify the domain, submit `sitemap.xml` in both.
4. **IndexNow** (near-instant crawl of new/changed pages). Generate a key, host it at `/{key}.txt`, then on each publish:
   ```bash
   curl "https://www.bing.com/indexnow?url=https://epoxymagicians.com/services/metallic-epoxy/&key=YOUR_KEY"
   ```

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
