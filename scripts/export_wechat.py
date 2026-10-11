#!/usr/bin/env python3
"""Render WeChat-ready PNGs into exports/.

Usage: python3 scripts/export_wechat.py
Renders single SVGs at 1600px wide and builds contact sheets for grouped assets.
"""
import os
import subprocess
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "exports")


def svg_size(path):
    import re
    head = open(path, encoding="utf-8").read(600)
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', head)
    if not m:
        m = re.search(r'width="(\d+)"[^>]*height="(\d+)"', head)
    return int(m.group(1)), int(m.group(2))


def shot(html, out, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=ROOT) as fh:
        fh.write(html)
        path = fh.name
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--screenshot=" + out,
         "--window-size=%d,%d" % (w, h), "file://" + path],
        check=False, capture_output=True,
    )
    os.unlink(path)
    print(out)


def render_single(rel, out_name, target_w=1600):
    src = os.path.join(ROOT, rel)
    sw, sh = svg_size(src)
    h = round(target_w * sh / sw)
    html = ('<!doctype html><meta charset="utf-8">'
            "<style>html,body{margin:0;background:#fff}"
            'img{display:block;width:%dpx}</style>'
            '<img src="file://%s">' % (target_w, src))
    shot(html, os.path.join(OUT, out_name), target_w, h)


def contact(out_name, cols, cw, ch, files):
    cells, wlist = [], []
    for rel in files:
        f = os.path.join(ROOT, rel)
        if not os.path.exists(f):
            raise FileNotFoundError(rel)
        name = os.path.basename(rel)
        cells.append('<figure class="c"><img src="file://%s" '
                     'style="width:%dpx;height:%dpx"><figcaption>%s</figcaption></figure>'
                     % (f, cw - 30, ch - 54, name))
        wlist.append(name)
    rows = (len(files) + cols - 1) // cols
    html = """<!doctype html><meta charset="utf-8"><style>
    body{margin:0;background:#F4ECDD;font:12px -apple-system,sans-serif;padding:20px}
    .g{display:grid;grid-template-columns:repeat(%d,%dpx);gap:10px}
    .c{margin:0;border-radius:12px;overflow:hidden;display:flex;flex-direction:column;
       align-items:center;justify-content:center;height:%dpx;background:#fff}
    .c img{object-fit:contain;max-width:100%%;max-height:100%%}
    figcaption{color:#999;font-size:11px;margin-top:6px}
    </style><div class="g">%s</div>""" % (cols, cw, ch, "".join(cells))
    w = cols * cw + 40
    h = rows * ch + 40
    shot(html, os.path.join(OUT, out_name), w, h)


def main():
    os.makedirs(OUT, exist_ok=True)

    render_single("assets/final/hero.svg", "01-hero.png")
    render_single("assets/mockups/product-grid.svg", "04-product-grid.png")
    render_single("assets/mockups/lifestyle-study.svg", "05-lifestyle.png")
    render_single("assets/mockups/gift-box.svg", "06-gift-box.png")

    contact("02-characters.png", 4, 360, 460, [
        "assets/characters/xiaozhou-front.svg",
        "assets/characters/xiaozhou-magnifier.svg",
        "assets/characters/xiaozhou-map.svg",
        "assets/characters/xiaozhou-back.svg",
        "assets/characters/xiaohe-front.svg",
        "assets/characters/xiaohe-notebook.svg",
        "assets/characters/xiaohe-lotus.svg",
        "assets/characters/xiaohe-back.svg",
        "assets/characters/duo.svg",
        "assets/characters/expressions.svg",
        "assets/characters/character-sheet.svg",
    ])
    contact("03-identity.png", 3, 380, 340, [
        "assets/identity/logo-lockup.svg",
        "assets/identity/logo-mark.svg",
        "assets/identity/color-palette.svg",
        "assets/identity/typography.svg",
        "assets/identity/pattern.svg",
        "assets/identity/icons.svg",
    ])
    contact("07-skus.png", 3, 420, 380, [
        "assets/products/sku01-canvas-bag.svg",
        "assets/products/sku02-water-bottle.svg",
        "assets/products/sku03-notebook.svg",
        "assets/products/sku04-sticker-set.svg",
        "assets/products/sku05-badge-magnet.svg",
        "assets/products/sku06-tshirt-cap.svg",
    ])


if __name__ == "__main__":
    main()
