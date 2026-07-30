# -*- coding: utf-8 -*-
"""
Page generator for Epoxy Magicians static site.
Produces service pages and city pages from the same design-system shell
used in services/garage-floor-epoxy/ and service-areas/plano/.
Run: python build_pages.py   (from repo root or _gen/, paths are relative to repo root)
This script is a build tool, not part of the shipped site.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD_CSS = """
:root{--navy:#0d1b2a;--navy-2:#12263a;--ink:#14202b;--paper:#fff;--mist:#f4f6f8;--line:#dfe5ea;--muted:#4a5a68;--brand:#ff6a00;--brand-ink:#7a2f00;--brand-hover:#e85d00;--gold:#f5b301;--ok:#0a7d3c;--shadow:0 6px 24px rgba(13,27,42,.12);--radius:14px;--wrap:1160px;--font:"Inter",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:var(--font);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
h1,h2,h3{line-height:1.15;margin:0 0 .5em;letter-spacing:-.02em}
h1{font-size:clamp(1.9rem,4.5vw,2.9rem);font-weight:800}
.wrap{max-width:var(--wrap);margin-inline:auto;padding-inline:20px}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;background:#fff;padding:12px;z-index:200}
.btn{display:inline-flex;align-items:center;gap:.5rem;font-weight:700;text-decoration:none;border-radius:10px;padding:14px 22px;line-height:1;min-height:48px}
.btn-cta{background:var(--brand);color:#fff}.btn-cta:hover{background:var(--brand-hover)}
.btn-ghost{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.55)}
.btn-call{background:#fff;color:var(--navy);border:2px solid var(--navy)}
:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.topbar{background:var(--navy);color:#fff;font-size:.85rem}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;min-height:38px}
.topbar a{color:#fff;text-decoration:none;font-weight:600}
.site-header{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.96);border-bottom:1px solid var(--line)}
.site-header .wrap{display:flex;align-items:center;gap:16px;min-height:64px}
.brand{font-weight:800;font-size:1.15rem;color:var(--navy);text-decoration:none}.brand span{color:var(--brand)}
.nav{margin-left:auto;display:flex;gap:20px}.nav a{text-decoration:none;color:var(--ink);font-weight:600;font-size:.95rem}
.header-actions{display:flex;gap:10px;align-items:center}
.header-actions .tel{font-weight:800;color:var(--navy);text-decoration:none}
.page-hero{position:relative;background:var(--navy);color:#fff;overflow:hidden}
.page-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(13,27,42,.93),rgba(13,27,42,.55));z-index:1}
.page-hero .hbg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.page-hero .wrap{position:relative;z-index:2;padding-block:44px}
.page-hero h1{color:#fff;max-width:22ch}
.page-hero p{color:#cdd7df;max-width:52ch}
.breadcrumbs{font-size:.82rem;color:#9fb0bd;margin-bottom:12px}
.breadcrumbs a{color:#c8d3dc;text-decoration:none}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
@media(max-width:900px){.nav{display:none}}
@media(max-width:560px){.header-actions .tel{display:none}.topbar{display:none}}
""".strip("\n")

def head(title, desc, canonical, og_title, og_desc, og_image, preload_base, schema_blocks):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0d1b2a">
<meta property="og:type" content="article">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://epoxymagicians.com/assets/img/{og_image}">
<link rel="preload" as="image" href="/assets/img/{preload_base}-1600.webp" imagesrcset="/assets/img/{preload_base}-800.webp 800w, /assets/img/{preload_base}-1600.webp 1600w" imagesizes="100vw" fetchpriority="high">
<style>
{HEAD_CSS}
</style>
{schema_blocks}
</head>
"""

def header_footer_shell(hero_html, article_html, final_cta_h2, final_cta_p, foot_services_extra="", foot_areas_extra=""):
    body = f"""<body>
<a class="skip" href="#main">Skip to main content</a>

<div class="topbar"><div class="wrap"><span>Serving all of Dallas–Fort Worth · Free estimates</span><a href="tel:[[PHONE_E164]]">Call [[PHONE]]</a></div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/">Epoxy<span>Magicians</span></a>
  <nav class="nav" aria-label="Primary">
    <a href="/services/">Services</a><a href="/service-areas/">Service Areas</a><a href="/gallery/">Gallery</a><a href="/reviews/">Reviews</a><a href="/faq/">FAQ</a><a href="/about/">About</a>
  </nav>
  <div class="header-actions">
    <a class="tel" href="tel:[[PHONE_E164]]" aria-label="Call [[PHONE]]">☎ [[PHONE]]</a>
    <a class="btn btn-cta" href="/contact/">Get Free Estimate</a>
  </div>
</div></header>

<main id="main">
{hero_html}

<link rel="stylesheet" href="/assets/css/styles.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/assets/css/styles.css"></noscript>

{article_html}

<section class="finalcta">
  <div class="wrap">
    <h2>{final_cta_h2}</h2>
    <p>{final_cta_p}</p>
    <div class="cta-row">
      <a class="btn btn-cta" href="/contact/">Get My Free Estimate</a>
      <a class="btn btn-ghost" href="tel:[[PHONE_E164]]">☎ Call [[PHONE]]</a>
    </div>
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="wrap foot-grid">
    <div><a class="brand" href="/" style="color:#fff">Epoxy<span>Magicians</span></a>
      <p class="nap">Epoxy Magicians<br>Serving Dallas–Fort Worth, TX<br><a href="tel:[[PHONE_E164]]">[[PHONE]]</a><br>License #[[LICENSE]] · Insured</p></div>
    <nav aria-label="Services"><h3>Services</h3>{foot_services_extra}<a href="/services/">All services →</a></nav>
    <nav aria-label="Service areas"><h3>Service Areas</h3>{foot_areas_extra}<a href="/service-areas/">All areas →</a></nav>
    <nav aria-label="Company"><h3>Company</h3><a href="/about/">About</a><a href="/gallery/">Gallery</a><a href="/reviews/">Reviews</a><a href="/contact/">Contact</a></nav>
  </div>
  <div class="wrap foot-legal"><span>© <span id="yr">2026</span> Epoxy Magicians. All rights reserved.</span><span><a href="/privacy/">Privacy</a> · <a href="/sitemap.xml">Sitemap</a></span></div>
</footer>

<div class="mobilebar" role="navigation" aria-label="Quick contact">
  <a href="tel:[[PHONE_E164]]" class="mb-call">☎ Call Now</a>
  <a href="/contact/" class="mb-quote">Free Estimate</a>
</div>
<script>(function(){{var y=document.getElementById('yr');if(y)y.textContent=new Date().getFullYear();}})();</script>
</body>
</html>
"""
    return body

DEFAULT_FOOT_SERVICES = '<a href="/services/garage-floor-epoxy/">Garage Floor Epoxy</a><a href="/services/metallic-epoxy/">Metallic Epoxy</a><a href="/services/polyaspartic-coatings/">Polyaspartic</a>'
DEFAULT_FOOT_AREAS = '<a href="/service-areas/dallas/">Dallas</a><a href="/service-areas/fort-worth/">Fort Worth</a><a href="/service-areas/plano/">Plano</a>'

def faq_details(faqs, first_open=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        open_attr = " open" if (i == 0 and first_open) else ""
        out.append(f'<details name="faq"{open_attr}><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>')
    return "\n  ".join(out)

def faq_jsonld(faqs):
    import json
    items = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":items}, ensure_ascii=False)

print("build_pages module loaded OK")
