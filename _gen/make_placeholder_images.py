# -*- coding: utf-8 -*-
"""
Generates lightweight, clearly-labeled placeholder WebP images for every
image path referenced across the site, so nothing 404s pre-launch. These
are NOT real project photos — every filename this script writes is also
listed in PLACEHOLDER_IMAGES.md at the repo root as a to-replace checklist.

Run: python _gen/make_placeholder_images.py
"""
import os, re, glob, hashlib
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG_DIR, exist_ok=True)

NAVY = (13, 27, 42)
NAVY2 = (18, 38, 58)
BRAND = (255, 106, 0)
LINE = (60, 78, 94)

def find_font(size):
    candidates = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def find_font_bold(size):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return find_font(size)

def label_from_filename(name):
    base = re.sub(r"-(1600|800|600)$", "", os.path.splitext(name)[0])
    words = base.replace("-", " ").title()
    return words

def make_image(path, w, h):
    name = os.path.splitext(os.path.basename(path))[0]
    # deterministic subtle color variation per filename so the grid isn't monotonous
    seed = int(hashlib.md5(name.encode()).hexdigest(), 16)
    shift = seed % 18
    bg = tuple(min(255, c + shift) for c in NAVY)
    bg2 = tuple(min(255, c + shift) for c in NAVY2)

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    # simple diagonal gradient band for visual variety, cheap to encode
    for i in range(0, w + h, 6):
        draw.line([(i, 0), (0, i)], fill=bg2, width=3)

    # dashed border to read as "placeholder", not a real photo
    dash = 14
    for x in range(0, w, dash * 2):
        draw.line([(x, 4), (min(x + dash, w), 4)], fill=BRAND, width=4)
        draw.line([(x, h - 4), (min(x + dash, w), h - 4)], fill=BRAND, width=4)
    for y in range(0, h, dash * 2):
        draw.line([(4, y), (4, min(y + dash, h))], fill=BRAND, width=4)
        draw.line([(w - 4, y), (w - 4, min(y + dash, h))], fill=BRAND, width=4)

    label = label_from_filename(os.path.basename(path))
    title_font = find_font_bold(max(20, w // 22))
    sub_font = find_font(max(14, w // 42))

    title = "PLACEHOLDER PHOTO"
    tb = draw.textbbox((0, 0), title, font=title_font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    draw.text(((w - tw) / 2, h / 2 - th - 10), title, font=title_font, fill=BRAND)

    sb = draw.textbbox((0, 0), label, font=sub_font)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    draw.text(((w - sw) / 2, h / 2 + 12), label, font=sub_font, fill=(224, 231, 237))

    footer = "Replace with a real project photo before launch"
    ff = find_font(max(11, w // 62))
    fb = draw.textbbox((0, 0), footer, font=ff)
    fw = fb[2] - fb[0]
    draw.text(((w - fw) / 2, h - fb[3] - 14), footer, font=ff, fill=(150, 165, 178))

    out_path = os.path.join(ROOT, path.lstrip("/"))
    if path.lower().endswith(".jpg") or path.lower().endswith(".jpeg"):
        img.save(out_path, "JPEG", quality=72, optimize=True)
    else:
        img.save(out_path, "WEBP", quality=68, method=6)

def collect_referenced_paths():
    paths = set()
    og_paths = set()
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if os.sep + "_gen" + os.sep in f:
            continue
        txt = open(f, encoding="utf-8").read()
        for m in re.findall(r'(?:src|href|imagesrcset|srcset)="([^"]*)"', txt):
            for part in m.split(","):
                p = part.strip().split(" ")[0]
                if p.startswith("/assets/img/") and p.endswith(".webp"):
                    paths.add(p)
        for m in re.findall(r'property="og:image" content="([^"]*)"', txt):
            local = re.sub(r"^https?://[^/]+", "", m)
            if local.startswith("/assets/img/"):
                og_paths.add(local)
    return sorted(paths), sorted(og_paths)

def size_for(path):
    if "-1600" in path:
        return 1600, 720
    if "-800" in path and ("hero" in path or re.search(r"(garage-epoxy|metallic-epoxy|flake-epoxy|polyaspartic-coatings|commercial-industrial-epoxy|concrete-polishing|patio-pool-deck-coating|driveway-coating|basement-floor-coating)-800", path)):
        return 800, 360
    if re.search(r"(dallas|fort-worth|arlington|plano|frisco|mckinney|irving|grand-prairie|southlake|flower-mound|denton|mansfield|rockwall)-800", path):
        return 800, 360
    if "ba-after" in path or "ba-before" in path:
        return 1200, 750
    if "-600" in path:
        return 600, 450
    return 800, 600

if __name__ == "__main__":
    paths, og_paths = collect_referenced_paths()
    made = []
    for p in paths:
        w, h = size_for(p)
        make_image(p, w, h)
        made.append(p)
    for p in og_paths:
        make_image(p, 1200, 630)
        made.append(p)
    print(f"Generated {len(made)} placeholder images in assets/img/ ({len(paths)} webp + {len(og_paths)} og:image jpg)")
    total_kb = sum(os.path.getsize(os.path.join(ROOT, p.lstrip("/"))) for p in made) / 1024
    print(f"Total size: {total_kb:.0f} KB, avg {total_kb/len(made):.1f} KB/image")
