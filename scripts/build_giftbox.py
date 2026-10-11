#!/usr/bin/env python3
"""Generate assets/mockups/gift-box.svg — 研学礼盒 (concept packaging)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgkit as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1400, 900


def product(name, x, y, scale, flip=False):
    """Inline a SKU without its studio background card."""
    body = K.inner(os.path.join(ROOT, "assets", "products", name))
    body = re.sub(r'<rect width="900" height="700" fill="#F7F4ED"/>', "", body, count=1)
    body = re.sub(r'<ellipse[^>]*fill="#26364F" opacity="0\.10"/>', "", body, count=1)
    body = K.remap_ids(body, "gb_" + name[:4])
    t = "translate(%s %s) scale(%s)" % (K.fmt(x), K.fmt(y), K.fmt(scale))
    if flip:
        t += " scale(-1 1)"
    return '<g transform="%s">\n%s\n</g>' % (t, body)


def main():
    p = ['<style>.cn{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",'
         '"Noto Sans SC",sans-serif}.en{font-family:"Helvetica Neue",Helvetica,'
         'Arial,sans-serif}</style>']
    p.append('<rect width="%d" height="%d" fill="#F7F4ED"/>' % (W, H))
    p.append('<ellipse cx="700" cy="756" rx="600" ry="34" fill="#26364F" opacity=".10"/>')

    # box body
    p.append('<rect x="430" y="384" width="540" height="344" rx="10" fill="#F4ECDD"/>')
    p.append('<rect x="430" y="384" width="540" height="344" rx="10" fill="none" '
             'stroke="#E4DBC4" stroke-width="3"/>')
    p.append('<path d="M430 384h540v26c-180 18-360 18-540 0z" fill="#EDE4D0"/>')

    # lid — flat top sliver + front face (square top corners, rounded bottom)
    p.append('<path d="M408 302 448 266h504l40 36z" fill="#3A8E88"/>')
    p.append('<path d="M408 302h584v76a10 10 0 0 1-10 10H418a10 10 0 0 1-10-10z" '
             'fill="#2E7D77"/>')
    p.append('<path d="M408 368h584v10a10 10 0 0 1-10 10H418a10 10 0 0 1-10-10z" '
             'fill="#276C68"/>')
    p.append('<text class="en" x="700" y="352" text-anchor="middle" font-size="19" '
             'font-weight="700" letter-spacing="7" fill="#F4ECDD">LITTLE EXPLORERS · JIANGNAN</text>')

    # box front print
    p.append(K.group(os.path.join(ROOT, "assets", "identity", "logo-mark.svg"),
                     700 - 60 * 0.62, 424, 0.62))
    p.append('<text class="cn" x="700" y="580" text-anchor="middle" font-size="44" '
             'font-weight="700" letter-spacing="6" fill="#26364F">江南小小探索家</text>')
    p.append('<path d="M620 606h160" stroke="#E9793B" stroke-width="5" stroke-linecap="round"/>')
    p.append('<text class="en" x="700" y="646" text-anchor="middle" font-size="15" '
             'font-weight="700" letter-spacing="6" fill="#2E7D77">STUDY TOUR MERCH · 6 SKU</text>')
    p.append('<text class="en" x="700" y="692" text-anchor="middle" font-size="11" '
             'font-weight="600" letter-spacing="4" fill="#26364F" opacity=".45">'
             'PERSONAL CONCEPT PROJECT</text>')

    # products beside the box, bases aligned with the box base
    p.append(product("sku03-notebook.svg", 96, 482, 0.44))
    p.append(product("sku05-badge-magnet.svg", 946, 547, 0.40))

    body = "\n".join(p)
    out = os.path.join(ROOT, "assets", "mockups", "gift-box.svg")
    K.write(out, K.wrap("0 0 %d %d" % (W, H), body,
                        title="礼盒 / Gift Box · 研学周边套装"))


if __name__ == "__main__":
    main()
