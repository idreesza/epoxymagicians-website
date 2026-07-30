# -*- coding: utf-8 -*-
"""
Adds distinguishing aria-labels to the repeated "Get (My) Free Estimate"
buttons on each page so screen reader users navigating a links list can tell
them apart, per WCAG 2.4.4/2.4.9 best practice (axe/Lighthouse
"identical-links-same-purpose"). Does not change visible button text or
destinations — only adds/replaces aria-label.

Run: python _gen/fix_duplicate_cta_labels.py
"""
import os, re, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CTA_RE = re.compile(
    r'<a class="btn btn-cta" href="([^"]*)"(?: aria-label="[^"]*")?>(Get( My)? Free Estimate)</a>'
)
CALL_RE = re.compile(
    r'<a class="btn btn-ghost" href="(tel:[^"]*)"(?: aria-label="[^"]*")?>(&#9742;|☎) Call \[\[PHONE\]\]</a>'
)

ZONE_MARKERS = [
    ('class="finalcta"', "final"),
    ('class="inline-cta"', "inline"),
    ('class="hero-cta"', "hero"),
    ('class="page-hero"', "hero"),
    ('<section class="hero"', "hero"),
    ('class="header-actions"', "header"),
]

def get_page_topic(html_text):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, re.S)
    if not m:
        return "your project"
    text = re.sub(r"<[^>]+>", "", m.group(1))
    text = html.unescape(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text

def classify_zone(text, pos):
    best_marker_pos = -1
    best_zone = "header"
    for marker, zone in ZONE_MARKERS:
        idx = text.rfind(marker, 0, pos)
        if idx > best_marker_pos:
            best_marker_pos = idx
            best_zone = zone
    return best_zone

def build_cta_label(zone, topic):
    if zone == "header":
        return "Get a free epoxy flooring estimate"
    if zone == "hero":
        return f"Get a free estimate for {topic}"
    if zone == "inline":
        return f"Request a written estimate for {topic}"
    if zone == "final":
        return f"Get your free {topic} estimate now"
    return "Get a free estimate"

def build_call_label(zone, topic):
    if zone == "hero":
        return f"Call now about {topic}"
    if zone == "final":
        return f"Call us now to discuss {topic}"
    return f"Call about {topic}"

def process(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    topic = get_page_topic(text)

    jobs = []  # (start, end, replacement)
    for m in CTA_RE.finditer(text):
        href, visible_text = m.group(1), m.group(2)
        zone = classify_zone(text, m.start())
        label = build_cta_label(zone, topic)
        jobs.append((m.start(), m.end(), f'<a class="btn btn-cta" href="{href}" aria-label="{label}">{visible_text}</a>'))
    for m in CALL_RE.finditer(text):
        href, symbol = m.group(1), m.group(2)
        zone = classify_zone(text, m.start())
        label = build_call_label(zone, topic)
        jobs.append((m.start(), m.end(), f'<a class="btn btn-ghost" href="{href}" aria-label="{label}">{symbol} Call [[PHONE]]</a>'))

    if not jobs:
        return False
    jobs.sort(key=lambda j: j[0], reverse=True)
    out = text
    for start, end, replacement in jobs:
        out = out[:start] + replacement + out[end:]
    if out != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        return True
    return False

if __name__ == "__main__":
    changed = 0
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if os.sep + "_gen" + os.sep in f:
            continue
        if process(f):
            changed += 1
    print(f"Added distinguishing aria-labels in {changed} files")
