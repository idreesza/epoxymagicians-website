# -*- coding: utf-8 -*-
"""
Bakes real business data from _data/business.json and _data/reviews.json into
every HTML/XML/txt file across the site, in one pass, with no client-side JS
injection (tel: links and JSON-LD must be present in the static HTML for
crawlers and for click-to-call to work at all).

Usage (from repo root or _gen/):
    python _gen/apply_business_config.py [--dry-run]

Safe to run at any time, repeatedly:
- Any field still shaped like "[[TOKEN]]" in business.json is skipped, so
  unset values are left untouched (and stay visibly marked incomplete).
- Only fields with a real value actually get substituted.
- Reviews only replace a placeholder block if a matching real review exists;
  city pages match by exact city name, homepage/reviews page fill in order.

This does not fabricate anything — it only ever copies values you typed into
_data/business.json / _data/reviews.json.
"""
import os, re, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = "--dry-run" in sys.argv

def is_placeholder(v):
    if v is None:
        return True
    s = str(v).strip()
    return s == "" or (s.startswith("[[") and s.endswith("]]"))

def load_json(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)

biz = load_json("_data/business.json")
reviews_doc = load_json("_data/reviews.json")
reviews = reviews_doc.get("reviews", [])

# ---------------------------------------------------------------- simple tokens
TOKEN_MAP = {
    "[[PHONE]]": biz.get("phone_display"),
    "[[PHONE_E164]]": biz.get("phone_e164"),
    "[[LICENSE]]": biz.get("license_number"),
    "[[INSURANCE]]": biz.get("insurance_carrier"),
    "[[YEARS]]": biz.get("years_in_business"),
    "[[JOBS]]": biz.get("jobs_completed"),
    "[[FOUNDING_YEAR]]": biz.get("founding_year"),
    "[[GRATING]]": biz.get("google_rating"),
    "[[GREVIEWS]]": biz.get("google_review_count"),
    "[[FINANCING_PARTNER]]": biz.get("financing_partner"),
    "[[GOOGLE_MAPS_EMBED_API_KEY]]": biz.get("google_maps_embed_api_key"),
    "[[PRIVACY_CONTACT_EMAIL]]": biz.get("privacy_contact_email"),
    "[[ADDRESS]]": biz.get("street_address"),
}
ACTIVE_TOKENS = {k: str(v) for k, v in TOKEN_MAP.items() if not is_placeholder(v)}

# ---------------------------------------------------------------- helpers
def target_files():
    for f in glob.glob(os.path.join(ROOT, "**", "*.*"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith("_gen") or rel.startswith(".git") or rel.startswith("_data"):
            continue
        if rel.split(os.sep)[0] == "node_modules":
            continue
        if os.path.splitext(f)[1].lower() in (".html", ".xml", ".txt"):
            yield f

def replace_block(html, pattern, builder, match_filter=None):
    """Replace regex matches in reverse order so spans stay valid; builder(i, m) -> new str or None to skip."""
    matches = list(pattern.finditer(html))
    if match_filter:
        matches = [m for m in matches if match_filter(m)]
    out = html
    for i in reversed(range(len(matches))):
        m = matches[i]
        new = builder(i, m)
        if new is not None:
            out = out[: m.start()] + new + out[m.end():]
    return out

def stars(rating):
    try:
        n = int(rating)
    except (TypeError, ValueError):
        n = 5
    n = max(1, min(5, n))
    return "★" * n

# ---------------------------------------------------------------- review blocks
HOME_REVIEW_RE = re.compile(r'<blockquote class="review">.*?</blockquote>', re.S)
RCARD_RE = re.compile(r'<div class="rcard">.*?</cite></div>', re.S)
CITY_QUOTE_RE = re.compile(
    r'<blockquote style="border-left:4px solid var\(--brand\).*?</blockquote>', re.S
)

def build_home_block(i, m):
    if i >= len(reviews):
        return None
    r = reviews[i]
    return (
        '<blockquote class="review">\n'
        f'        <div class="stars" aria-label="{r.get("rating",5)} out of 5 stars">{stars(r.get("rating",5))}</div>\n'
        f'        <p>“{r["text"]}”</p>\n'
        f'        <cite>— {r["name"]}, {r["city"]}</cite>\n'
        '      </blockquote>'
    )

def build_rcard_block(i, m):
    if i >= len(reviews):
        return None
    r = reviews[i]
    svc = f' <span class="svc">— {r["service"]}</span>' if r.get("service") else ""
    return (
        '<div class="rcard">'
        f'<div class="stars" aria-label="{r.get("rating",5)} out of 5 stars">{stars(r.get("rating",5))}</div>'
        f'<p>“{r["text"]}”</p>'
        f'<cite>{r["name"]}, {r["city"]}{svc}</cite></div>'
    )

def build_city_block(city_name):
    match = next((r for r in reviews if r.get("city", "").strip().lower() == city_name.lower()), None)
    if not match:
        return None
    def builder(i, m):
        return (
            '<blockquote style="border-left:4px solid var(--brand);background:var(--mist);margin:0;padding:16px 20px;border-radius:10px">\n'
            f'    <p style="margin:0 0 6px">{stars(match.get("rating",5))} {match["text"]}</p>\n'
            f'    <cite style="font-style:normal;font-weight:600;color:var(--navy)">— {match["name"]}, {city_name}</cite>\n'
            '  </blockquote>'
        )
    return builder

# ---------------------------------------------------------------- about-page team
MEMBER_RE = re.compile(r'<div class="member">.*?</div>\s*</div>', re.S)

def build_member_block(i, m):
    team = biz.get("team", [])
    if i >= len(team):
        return None
    t = team[i]
    if is_placeholder(t.get("name")):
        return None
    photo = t.get("photo") or "REPLACE-ME"
    role = t.get("role", "")
    bio = t.get("bio", "")
    if is_placeholder(bio):
        bio = "[[Real bio.]]"
    slug = ["owner", "2", "3"][i] if i < 3 else str(i + 1)
    return (
        '<div class="member">\n'
        f'      <img src="/assets/img/team-{slug}-600.webp" width="480" height="600" alt="{t["name"]}, {role} at Epoxy Magicians" loading="lazy" decoding="async">\n'
        f'      <div class="info"><h3>{t["name"]}</h3><p class="role">{role}</p><p>{bio}</p></div>\n'
        '    </div>'
    )

# ---------------------------------------------------------------- city slug -> display name
CITY_NAMES = {
    "dallas": "Dallas", "fort-worth": "Fort Worth", "arlington": "Arlington",
    "plano": "Plano", "frisco": "Frisco", "mckinney": "McKinney", "irving": "Irving",
    "grand-prairie": "Grand Prairie", "southlake": "Southlake", "flower-mound": "Flower Mound",
    "denton": "Denton", "mansfield": "Mansfield", "rockwall": "Rockwall",
}

# ---------------------------------------------------------------- main pass
changed_files = []
for f in target_files():
    rel = os.path.relpath(f, ROOT)
    with open(f, encoding="utf-8") as fh:
        html = fh.read()
    original = html

    for token, value in ACTIVE_TOKENS.items():
        if token in html:
            html = html.replace(token, value)

    if rel.replace("\\", "/") == "index.html":
        html = replace_block(html, HOME_REVIEW_RE, build_home_block)

    if rel.replace("\\", "/") == "reviews/index.html":
        html = replace_block(html, RCARD_RE, build_rcard_block)

    if rel.replace("\\", "/") == "about/index.html":
        html = replace_block(html, MEMBER_RE, build_member_block)

    parts = rel.replace("\\", "/").split("/")
    if len(parts) == 3 and parts[0] == "service-areas" and parts[2] == "index.html":
        city_name = CITY_NAMES.get(parts[1])
        if city_name:
            builder = build_city_block(city_name)
            if builder:
                html = replace_block(html, CITY_QUOTE_RE, builder)

    if html != original:
        changed_files.append(rel)
        if not DRY_RUN:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(html)

print(f"Active (real-value) tokens this run: {len(ACTIVE_TOKENS)} of {len(TOKEN_MAP)}")
print(f"Reviews available: {len(reviews)}")
print(f"Files changed: {len(changed_files)}{' (dry run, nothing written)' if DRY_RUN else ''}")
for f in changed_files:
    print(" -", f)
