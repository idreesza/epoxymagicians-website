# -*- coding: utf-8 -*-
"""Generates a simple favicon (navy square, orange "EM" mark) and inserts
<link rel="icon"> into every page's <head> if not already present."""
import os, re, glob
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY = (13, 27, 42)
BRAND = (255, 106, 0)

def font(size):
    for c in (r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"):
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def make_icon(size):
    img = Image.new("RGB", (size, size), NAVY)
    d = ImageDraw.Draw(img)
    f = font(int(size * 0.52))
    text = "E"
    bb = d.textbbox((0, 0), text, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - w) / 2 - bb[0], (size - h) / 2 - bb[1]), text, font=f, fill=BRAND)
    return img

img32 = make_icon(32)
img32.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
make_icon(180).save(os.path.join(ROOT, "assets", "img", "apple-touch-icon.png"), "PNG")
print("favicon.ico + apple-touch-icon.png written")

ICON_TAGS = (
    '<link rel="icon" href="/favicon.ico" sizes="any">\n'
    '<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">'
)

count = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith("_gen"):
        continue
    txt = open(f, encoding="utf-8").read()
    if 'rel="icon"' in txt:
        continue
    new_txt, n = re.subn(
        r'(<meta name="theme-color"[^>]*>)',
        r'\1\n' + ICON_TAGS,
        txt,
        count=1,
    )
    if n:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(new_txt)
        count += 1

print(f"Inserted favicon links into {count} pages")
