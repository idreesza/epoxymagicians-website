# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import ROOT, header_footer_shell, faq_details, faq_jsonld, DEFAULT_FOOT_SERVICES, DEFAULT_FOOT_AREAS
from blog_data import POSTS

HEAD_CSS = """
:root{--navy:#0d1b2a;--navy-2:#12263a;--ink:#14202b;--mist:#f4f6f8;--line:#dfe5ea;--muted:#4a5a68;--brand:#ff6a00;--brand-hover:#e85d00;--gold:#f5b301;--radius:14px;--wrap:1160px;--font:"Inter",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:var(--font);color:var(--ink);line-height:1.6}
img{max-width:100%;height:auto;display:block}
h1,h2{line-height:1.15;margin:0 0 .5em;letter-spacing:-.02em}
h1{font-size:clamp(1.9rem,4.5vw,2.7rem);font-weight:800}
.wrap{max-width:var(--wrap);margin-inline:auto;padding-inline:20px}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;background:#fff;padding:12px;z-index:200}
.btn{display:inline-flex;align-items:center;gap:.5rem;font-weight:700;text-decoration:none;border-radius:10px;padding:14px 22px;min-height:48px}
.btn-cta{background:var(--brand);color:var(--navy)}.btn-cta:hover{background:var(--brand-hover)}
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
.page-hero{background:var(--navy);color:#fff;padding-block:40px}
.page-hero h1{color:#fff;max-width:26ch}
.page-hero .meta{color:#9fb0bd;font-size:.85rem;margin-top:10px}
.breadcrumbs{font-size:.82rem;color:#9fb0bd;margin-bottom:12px}.breadcrumbs a{color:#c8d3dc;text-decoration:none}
@media(max-width:900px){.nav{display:none}}
@media(max-width:560px){.header-actions .tel{display:none}.topbar{display:none}}
""".strip("\n")

def build_faq_jsonld(faqs):
    items = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faqs]
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":items}, ensure_ascii=False)

def render_post(post):
    slug = post["slug"]
    canonical = f"https://epoxymagicians.com/blog/{slug}/"

    article_jsonld = {
        "@context":"https://schema.org","@type":"Article",
        "headline": post["h1"],
        "description": post["meta_desc"],
        "author":{"@type":"Organization","name":"Epoxy Magicians"},
        "publisher":{"@type":"Organization","name":"Epoxy Magicians","logo":{"@type":"ImageObject","url":"https://epoxymagicians.com/assets/img/logo.png"}},
        "datePublished":"[[PUBLISH_DATE]]","dateModified":"[[PUBLISH_DATE]]",
        "mainEntityOfPage": canonical,
        "image": f"https://epoxymagicians.com/assets/img/blog-{slug}-og.jpg",
    }
    breadcrumb_jsonld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://epoxymagicians.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://epoxymagicians.com/blog/"},
        {"@type":"ListItem","position":3,"name":post["h1"],"item":canonical}]}

    schema_blocks = (
        f'<script type="application/ld+json">{json.dumps(article_jsonld, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{json.dumps(breadcrumb_jsonld, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{build_faq_jsonld(post["faqs"])}</script>'
    )

    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{post["title"]}</title>
<meta name="description" content="{post["meta_desc"]}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0d1b2a">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:title" content="{post["h1"]}">
<meta property="og:description" content="{post["meta_desc"]}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://epoxymagicians.com/assets/img/blog-{slug}-og.jpg">
<style>
{HEAD_CSS}
</style>
{schema_blocks}
</head>
"""

    hero_html = f"""<section class="page-hero"><div class="wrap">
  <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; {post["h1"]}</nav>
  <h1>{post["h1"]}</h1>
  <p class="meta">{post["tag"]} guide &middot; Epoxy Magicians &middot; Updated [[PUBLISH_DATE]]</p>
</div></section>"""

    sections_html = "\n\n  ".join(f"<h2>{h2}</h2>\n  {body}" for h2, body in post["sections"])
    related_html = " &middot; ".join(f'<a href="{href}">{text}</a>' for href, text in post["related"])

    article_html = f"""<article class="content">
  <p class="lead">{post["lead"]}</p>

  {sections_html}

  <div class="inline-cta">
    <h3>Ready to get your floor priced?</h3>
    <p>Free on-site estimate anywhere in Dallas&ndash;Fort Worth &mdash; usually within 24&ndash;48 hours.</p>
    <a class="btn btn-cta" href="/contact/" aria-label="Get a free estimate for {post["h1"]}">Get My Free Estimate</a>
  </div>

  <h2>FAQ</h2>
  {faq_details(post["faqs"])}

  <p style="margin-top:24px">{related_html}</p>
  <p style="margin-top:12px"><a class="btn btn-call" href="/blog/">&larr; Back to all guides</a></p>
</article>"""

    body = header_footer_shell(
        hero_html=hero_html, article_html=article_html,
        final_cta_h2="Ready for a floor that lasts?",
        final_cta_p="Free on-site estimate anywhere in Dallas–Fort Worth.",
        foot_services_extra=DEFAULT_FOOT_SERVICES, foot_areas_extra=DEFAULT_FOOT_AREAS,
    )

    out_path = os.path.join(ROOT, "blog", slug, "index.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(head + body)
    print("wrote", os.path.relpath(out_path, ROOT))

for post in POSTS:
    render_post(post)
