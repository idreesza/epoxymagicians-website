# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import ROOT, head, header_footer_shell, faq_details, faq_jsonld, DEFAULT_FOOT_SERVICES, DEFAULT_FOOT_AREAS
from services_data import SERVICES
from cities_data import CITIES

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)

# ---------------------------------------------------------------- SERVICES
def render_service(svc):
    slug = svc["slug"]
    canonical = f"https://epoxymagicians.com/services/{slug}/"
    img_base = slug  # e.g. metallic-epoxy-800.webp / -1600.webp

    price_range_offer = ""
    if svc["price_low"]:
        price_range_offer = f',"offers":{{"@type":"Offer","priceCurrency":"USD","priceSpecification":{{"@type":"UnitPriceSpecification","price":"{svc["price_low"]}.00","priceCurrency":"USD","unitText":"square foot","minPrice":"{svc["price_low"]}.00","maxPrice":"{svc["price_high"]}.00"}}}}'

    service_jsonld = {
        "@context":"https://schema.org","@type":"Service","serviceType": svc["name"].replace("&amp;","&"),
        "name": svc["name"].replace("&amp;","&"),
        "description": svc["lead"].replace("<strong>","").replace("</strong>","")[:300],
        "provider":{"@type":"HomeAndConstructionBusiness","name":"Epoxy Magicians","telephone":"[[PHONE_E164]]","url":"https://epoxymagicians.com/","priceRange":"$$"},
        "areaServed":["Dallas TX","Fort Worth TX","Arlington TX","Plano TX","Frisco TX","McKinney TX","Irving TX","Grand Prairie TX","Southlake TX","Flower Mound TX","Denton TX","Mansfield TX","Rockwall TX"],
    }
    breadcrumb_jsonld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://epoxymagicians.com/"},
        {"@type":"ListItem","position":2,"name":"Services","item":"https://epoxymagicians.com/services/"},
        {"@type":"ListItem","position":3,"name":svc["name"].replace("&amp;","&"),"item":canonical}]}

    schema_blocks = (
        f'<script type="application/ld+json">{json.dumps(service_jsonld, ensure_ascii=False)}{price_range_offer if False else ""}</script>\n'
        f'<script type="application/ld+json">{json.dumps(breadcrumb_jsonld, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{faq_jsonld([(q.replace("&mdash;","-").replace("&ndash;","-"), a.replace("&mdash;","-").replace("&ndash;","-").replace("<a href=","<a href=")) for q,a in svc["faqs"]])}</script>'
    )

    price_note = f'<strong>{svc["name"].replace("&amp;","&")} cost in DFW:</strong> ' + (
        f'<strong>${svc["price_low"]}&ndash;${svc["price_high"]}/sq ft</strong> installed. ' if svc["price_low"] else ""
    ) + svc["price_note"]

    steps_html = "\n    ".join(f"<li>{s}</li>" for s in svc["process_steps"])

    hero_html = f"""<section class="page-hero">
  <img class="hbg" src="/assets/img/{img_base}-1600.webp" srcset="/assets/img/{img_base}-800.webp 800w, /assets/img/{img_base}-1600.webp 1600w" sizes="100vw" width="1600" height="720" alt="{svc['hero_img_alt']}" fetchpriority="high" decoding="async">
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/services/">Services</a> &rsaquo; {svc['name']}</nav>
    <h1>{svc['h1']}</h1>
    <p>{svc['hero_p']}</p>
    <div class="hero-cta">
      <a class="btn btn-cta" href="/contact/">Get My Free Estimate</a>
      <a class="btn btn-ghost" href="tel:[[PHONE_E164]]">&#9742; Call [[PHONE]]</a>
    </div>
  </div>
</section>"""

    article_html = f"""<article class="content">
  <p class="lead">{svc['lead']}</p>

  <div class="pricebox">{price_note}</div>

  <h2>{svc['why_h2']}</h2>
  <p>{svc['why_p']}</p>

  <h2>{svc['process_h2']}</h2>
  <p>{svc['process_intro']}</p>
  <ol>
    {steps_html}
  </ol>

  <div class="inline-cta">
    <h3>Want your floor priced?</h3>
    <p>Send a couple of photos and your city &mdash; we'll get you a written estimate, usually within 24&ndash;48 hours.</p>
    <a class="btn btn-cta" href="/contact/">Get My Free Estimate</a>
  </div>

  <h2>{svc['extra_h2']}</h2>
  <p>{svc['extra_p']}</p>

  <h2>{svc['name']} FAQs</h2>
  {faq_details(svc['faqs'])}

  <p style="margin-top:32px"><a class="btn btn-call" href="/services/">&larr; Back to all services</a></p>
</article>"""

    html = head(
        title=svc["title"], desc=svc["meta_desc"], canonical=canonical,
        og_title=svc["og_title"], og_desc=svc["og_desc"], og_image=f"{slug}-og.jpg",
        preload_base=img_base, schema_blocks=schema_blocks,
    ) + header_footer_shell(
        hero_html=hero_html, article_html=article_html,
        final_cta_h2=f"Ready to upgrade your {svc['name'].replace('&amp;','&').lower()} floor?",
        final_cta_p="Free on-site estimate anywhere in Dallas–Fort Worth.",
        foot_services_extra=DEFAULT_FOOT_SERVICES, foot_areas_extra=DEFAULT_FOOT_AREAS,
    )
    write(f"services/{slug}/index.html", html)

for svc in SERVICES:
    render_service(svc)

# ---------------------------------------------------------------- CITIES
def render_city(c):
    slug = c["slug"]
    canonical = f"https://epoxymagicians.com/service-areas/{slug}/"
    img_base = slug

    biz_jsonld = {
        "@context":"https://schema.org","@type":"HomeAndConstructionBusiness",
        "name": f"Epoxy Magicians — {c['name']}",
        "url": canonical, "telephone":"[[PHONE_E164]]", "priceRange":"$$",
        "image": f"https://epoxymagicians.com/assets/img/{slug}-og.jpg",
        "description": f"Garage, metallic, flake and polyaspartic floor coating services in {c['name']}, Texas and surrounding {c['county']} neighborhoods.",
        "areaServed":{"@type":"City","name":c["name"]},
        "address":{"@type":"PostalAddress","addressLocality":c["name"],"addressRegion":"TX","addressCountry":"US"},
        "geo":{"@type":"GeoCoordinates","latitude":c["lat"],"longitude":c["lng"]},
    }
    breadcrumb_jsonld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://epoxymagicians.com/"},
        {"@type":"ListItem","position":2,"name":"Service Areas","item":"https://epoxymagicians.com/service-areas/"},
        {"@type":"ListItem","position":3,"name":c["name"],"item":canonical}]}

    schema_blocks = (
        f'<script type="application/ld+json">{json.dumps(biz_jsonld, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{json.dumps(breadcrumb_jsonld, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{faq_jsonld(c["faqs"])}</script>'
    )

    hero_html = f"""<section class="page-hero">
  <img class="hbg" src="/assets/img/{img_base}-1600.webp" srcset="/assets/img/{img_base}-800.webp 800w, /assets/img/{img_base}-1600.webp 1600w" sizes="100vw" width="1600" height="720" alt="{c['hero_img_alt']}" fetchpriority="high" decoding="async">
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/service-areas/">Service Areas</a> &rsaquo; {c['name']}</nav>
    <h1>Epoxy Flooring in {c['name']}, TX</h1>
    <p>{c['hero_p']}</p>
    <div class="hero-cta">
      <a class="btn btn-cta" href="/contact/">Get My Free Estimate</a>
      <a class="btn btn-ghost" href="tel:[[PHONE_E164]]">&#9742; Call [[PHONE]]</a>
    </div>
  </div>
</section>"""

    popular_html = "\n    ".join(f"<li>{item}</li>" for item in c["popular_items"])

    article_html = f"""<article class="content">
  <p class="lead">{c['intro']}</p>

  <h2>{c['neighborhoods_h2']}</h2>
  <p>{c['neighborhoods_p']}</p>

  <h2>{c['soil_h2']}</h2>
  <p>{c['soil_p']}</p>

  <div class="pricebox">{c['pricebox']}</div>

  <h2>{c['popular_h2']}</h2>
  <ul>
    {popular_html}
  </ul>

  <div class="inline-cta">
    <h3>Get your {c['name']} floor priced free</h3>
    <p>Text a couple of photos and your neighborhood &mdash; we'll send a written estimate, usually within 24&ndash;48 hours.</p>
    <a class="btn btn-cta" href="/contact/">Get My Free Estimate</a>
  </div>

  <h2>What a {c['name']} neighbor said</h2>
  <blockquote style="border-left:4px solid var(--brand);background:var(--mist);margin:0;padding:16px 20px;border-radius:10px">
    <p style="margin:0 0 6px">&#9733;&#9733;&#9733;&#9733;&#9733; <em>[[Replace with a real Google review from a {c['name']} customer &mdash; name + neighborhood.]]</em></p>
    <cite style="font-style:normal;font-weight:600;color:var(--navy)">&mdash; [[Name]], {c['review_area']}</cite>
  </blockquote>

  <h2>{c['name']} epoxy flooring FAQs</h2>
  {faq_details(c['faqs'])}

  <h2>Services available in {c['name']}</h2>
  <p><a href="/services/garage-floor-epoxy/">Garage floor epoxy</a> &middot; <a href="/services/metallic-epoxy/">Metallic epoxy</a> &middot; <a href="/services/flake-epoxy/">Flake epoxy</a> &middot; <a href="/services/polyaspartic-coatings/">Polyaspartic coatings</a> &middot; <a href="/services/patio-pool-deck-coating/">Patio &amp; pool deck</a> &middot; <a href="/services/commercial-industrial-epoxy/">Commercial &amp; industrial</a></p>

  <p style="margin-top:24px"><a class="btn btn-call" href="/service-areas/">&larr; All DFW service areas</a></p>
</article>"""

    html = head(
        title=c["title"], desc=c["meta_desc"], canonical=canonical,
        og_title=f"Epoxy Flooring in {c['name']}, TX | Epoxy Magicians",
        og_desc=f"Garage, metallic &amp; polyaspartic floor coatings in {c['name']}. Free estimates, same-week install.",
        og_image=f"{slug}-og.jpg", preload_base=img_base, schema_blocks=schema_blocks,
    ) + header_footer_shell(
        hero_html=hero_html, article_html=article_html,
        final_cta_h2=f"Serving {c['name']} &amp; all of {c['county']}",
        final_cta_p="Free on-site estimate — usually within 24–48 hours.",
        foot_services_extra=DEFAULT_FOOT_SERVICES, foot_areas_extra=DEFAULT_FOOT_AREAS,
    )
    write(f"service-areas/{slug}/index.html", html)

for c in CITIES:
    render_city(c)

print("DONE:", len(SERVICES), "service pages +", len(CITIES), "city pages")
