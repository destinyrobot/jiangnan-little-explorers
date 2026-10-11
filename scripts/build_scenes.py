#!/usr/bin/env python3
"""Generate the key-visual (hero) and lifestyle scene SVGs."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgkit as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1600, 900
SKY = ('<defs>\n'
       '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">\n'
       '<stop offset="0" stop-color="#FDF9F1"/>\n'
       '<stop offset=".52" stop-color="#E9F1EA"/>\n'
       '<stop offset="1" stop-color="#F7E7D1"/>\n'
       '</linearGradient>\n'
       '<radialGradient id="sun" cx=".7" cy=".66" r=".45">\n'
       '<stop offset="0" stop-color="#F7D9AE" stop-opacity=".85"/>\n'
       '<stop offset="1" stop-color="#F7D9AE" stop-opacity="0"/>\n'
       '</radialGradient>\n'
       '<linearGradient id="water" gradientUnits="userSpaceOnUse" x1="0" y1="660" x2="0" y2="900">\n'
       '<stop offset="0" stop-color="#34908A"/>\n'
       '<stop offset="1" stop-color="#22655F"/>\n'
       '</linearGradient>\n'
       '</defs>\n')


def skyline(base_y, houses, fill, eave=14):
    """Row of water-town houses: wall block + overhanging gable roof."""
    d = []
    for x, w, wall, roof in houses:
        top = base_y - wall
        d.append(
            "M%g %g L%g %g L%g %g L%g %g L%g %g L%g %g L%g %g L%g %g Z"
            % (x, base_y,
               x, top,
               x - eave, top - 7,
               x + w * 0.16, top - roof,
               x + w * 0.84, top - roof,
               x + w + eave, top - 7,
               x + w, top,
               x + w, base_y)
        )
    return '<path d="%s" fill="%s"/>' % (" ".join(d), fill)


def bridge(x0, x1, y0, apex, bottom, arch_rx, arch_ry, fill):
    cx = (x0 + x1) / 2.0
    cy = 2 * apex - y0
    return (
        '<path d="M%g %g L%g %g Q%g %g %g %g L%g %g Z '
        'M%g %g A%g %g 0 0 1 %g %g Z" fill="%s" fill-rule="evenodd"/>'
        % (x0, bottom, x0, y0, cx, cy, x1, y0, x1, bottom,
           cx - arch_rx, bottom, arch_rx, arch_ry, cx + arch_rx, bottom, fill)
    ), cx, cy


def quad(t, p0, p1, p2):
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2


def railing(x0, x1, y0, apex, fill):
    cx = (x0 + x1) / 2.0
    cy = 2 * apex - y0
    top = (cy - 24)
    rail = ('<path d="M%g %g Q%g %g %g %g" fill="none" stroke="%s" '
            'stroke-width="7" stroke-linecap="round"/>'
            % (x0, y0 - 24, cx, top, x1, y0 - 24, fill))
    posts = []
    for i in range(1, 12):
        t = i / 12.0
        x = quad(t, x0, cx, x1)
        y = quad(t, y0, cy, y0)
        yt = quad(t, y0 - 24, top, y0 - 24)
        posts.append('<path d="M%g %g V%g" stroke="%s" stroke-width="5" '
                     'stroke-linecap="round"/>' % (x, y + 4, yt, fill))
    return rail + "".join(posts)


def ripples(y0, y1, fill, n=7, seed=3):
    out, s = [], seed
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        x = 60 + (s % 1180)
        s = (s * 1103515245 + 12345) % 2147483648
        y = y0 + (s % max(1, int(y1 - y0)))
        w = 54 + (s % 70)
        out.append('<path d="M%g %g q%g -7 %g 0 t%g 0" fill="none" stroke="%s" '
                   'stroke-width="4" stroke-linecap="round" opacity=".3"/>'
                   % (x, y, w / 2.0, w, w, fill))
    return "".join(out)


def boat(x, y, s=1.0, fill="#26364F"):
    return ('<g transform="translate(%g %g) scale(%g)">'
            '<path d="M-76 0h152l-18 32h-116z" fill="%s"/>'
            '<path d="M-50 0a50 46 0 0 1 100 0z" fill="%s"/>'
            '<path d="M-26 0a26 25 0 0 1 52 0z" fill="#F4ECDD" opacity=".22"/>'
            '</g>' % (x, y, s, fill, fill))


def lotus(x, y, s=1.0, fill="#79B473"):
    return ('<g transform="translate(%g %g) scale(%g)">'
            '<path d="M0 0L15-7A17 12 0 1 0 15 7Z" fill="%s"/>'
            '<path d="M2 0h12" stroke="#5E9E58" stroke-width="2.4" '
            'stroke-linecap="round" fill="none"/></g>' % (x, y, s, fill))


def willow():
    out = ['<g fill="#79B473" stroke="#5E9E58">']
    branches = [(-10, -20, 300, 210, 120, 340), (-30, -10, 210, 330, 60, 470),
                (60, -30, 380, 120, 300, 240)]
    for x0, y0, cx, cy, x1, y1 in branches:
        out.append('<path d="M%g %g Q%g %g %g %g" fill="none" stroke="#5E9E58" '
                   'stroke-width="5" stroke-linecap="round"/>' % (x0, y0, cx, cy, x1, y1))
        for i in range(1, 7):
            t = i / 7.0
            x = quad(t, x0, cx, x1)
            y = quad(t, y0, cy, y1)
            out.append('<ellipse cx="%g" cy="%g" rx="15" ry="6.5" fill="#79B473" '
                       'stroke="none" transform="rotate(%g %g %g)"/>'
                       % (x, y, -35 + i * 6, x, y))
            out.append('<ellipse cx="%g" cy="%g" rx="15" ry="6.5" fill="#79B473" '
                       'stroke="none" transform="rotate(%g %g %g)"/>'
                       % (x + 16, y + 14, 20 + i * 6, x + 16, y + 14))
    out.append('</g>')
    return "".join(out)


def hero():
    parts = [SKY]
    parts.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))
    parts.append('<rect width="%d" height="%d" fill="url(#sun)"/>' % (W, H))

    far = [(40, 220, 66, 40), (300, 170, 54, 34), (520, 250, 72, 46),
           (820, 180, 58, 36), (1050, 240, 68, 44), (1340, 210, 60, 38)]
    mid = [(0, 190, 78, 46), (240, 150, 62, 40), (430, 210, 84, 50),
           (700, 160, 66, 42), (910, 200, 80, 46), (1160, 170, 70, 44),
           (1380, 220, 86, 52)]
    near = [(-20, 240, 96, 56), (270, 180, 82, 50), (500, 230, 100, 58),
            (790, 190, 88, 52), (1030, 250, 104, 60), (1330, 200, 92, 54)]
    parts.append(skyline(614, far, "#DFEAE4", 10))
    parts.append(skyline(648, mid, "#C4D6D0", 12))
    parts.append(skyline(684, near, "#A2BBB6", 14))

    parts.append('<rect x="0" y="660" width="%d" height="%d" fill="url(#water)"/>'
                 % (W, H - 660))

    b, cx, _ = bridge(760, 1420, 700, 552, 772, 212, 112, "#EFE7D6")
    parts.append(b)
    parts.append('<path d="M760 700 Q%g %g 1420 700" fill="none" stroke="#DCD3BC" '
                 'stroke-width="6"/>' % (cx, 2 * 552 - 700))
    parts.append(railing(760, 1420, 700, 552, "#C9C0A8"))
    parts.append('<path d="M%g 772 A212 112 0 0 1 %g 772" fill="none" '
                 'stroke="#DCD3BC" stroke-width="7"/>' % (cx - 212, cx + 212))
    parts.append('<rect x="0" y="756" width="%d" height="%d" fill="url(#water)" '
                 'opacity=".86"/>' % (W, H - 756))

    parts.append(ripples(700, 880, "#F4ECDD", 11))
    parts.append(boat(330, 748, 1.0))
    for x, y, s in ((170, 812, 1.0), (300, 846, 0.8), (90, 872, 0.7),
                    (1430, 806, 0.9), (1520, 858, 0.75)):
        parts.append(lotus(x, y, s))

    parts.append(K.group(os.path.join(ROOT, "assets", "characters",
                                      "xiaozhou-back.svg"),
                         991 - 0.42 * 200, 565 - 0.42 * 462, 0.42))
    parts.append(K.group(os.path.join(ROOT, "assets", "characters",
                                      "xiaohe-back.svg"),
                         1123 - 0.42 * 200, 554 - 0.42 * 462, 0.42))

    parts.append(willow())
    out = K.wrap("0 0 %d %d" % (W, H), "\n".join(parts),
                 title="主视觉 / Key Visual · 江南小小探索家")
    K.write(os.path.join(ROOT, "assets", "final", "hero.svg"), out)


def lifestyle():
    parts = [SKY]
    parts.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))
    parts.append('<rect width="%d" height="%d" fill="url(#sun)" opacity=".7"/>'
                 % (W, H))

    far = [(60, 230, 62, 40), (340, 180, 54, 34), (570, 250, 70, 44),
           (880, 170, 56, 36), (1110, 240, 66, 42), (1400, 190, 58, 38)]
    mid = [(0, 200, 76, 46), (250, 160, 64, 40), (460, 220, 82, 50),
           (740, 170, 68, 42), (960, 210, 78, 48), (1220, 180, 72, 44),
           (1440, 210, 84, 50)]
    near = [(-20, 250, 94, 56), (280, 190, 84, 50), (520, 240, 98, 58),
            (820, 200, 90, 54), (1080, 250, 100, 58), (1380, 220, 92, 54)]
    parts.append(skyline(596, far, "#DFEAE4", 10))
    parts.append(skyline(630, mid, "#C4D6D0", 12))
    parts.append(skyline(666, near, "#A2BBB6", 14))

    parts.append('<rect x="0" y="642" width="%d" height="%d" fill="url(#water)"/>'
                 % (W, H - 642))

    b, cx, _ = bridge(120, 760, 664, 546, 726, 190, 96, "#EFE7D6")
    parts.append(b)
    parts.append(railing(120, 760, 664, 546, "#C9C0A8"))
    parts.append('<path d="M%g 726 A190 96 0 0 1 %g 726" fill="none" '
                 'stroke="#DCD3BC" stroke-width="7"/>' % (cx - 190, cx + 190))
    parts.append('<rect x="0" y="706" width="%d" height="%d" fill="url(#water)" '
                 'opacity=".86"/>' % (W, H - 706))

    parts.append(ripples(676, 790, "#F4ECDD", 9, seed=11))
    parts.append(boat(1240, 706, 0.72))
    for x, y, s in ((880, 742, 1.0), (1010, 772, 0.8), (1480, 756, 0.9),
                    (560, 764, 0.75)):
        parts.append(lotus(x, y, s))

    parts.append('<path d="M0 900 L0 812 Q420 786 840 806 Q1240 824 1600 794 '
                 'L1600 900 Z" fill="#F1E8D5"/>')
    parts.append('<path d="M0 812 Q420 786 840 806 Q1240 824 1600 794" fill="none" '
                 'stroke="#E0D6BE" stroke-width="5"/>')

    parts.append(K.group(os.path.join(ROOT, "assets", "characters",
                                      "xiaozhou-magnifier.svg"),
                         1080 - 0.46 * 200, 872 - 0.46 * 470, 0.46))
    parts.append(K.group(os.path.join(ROOT, "assets", "characters",
                                      "xiaohe-notebook.svg"),
                         1215 - 0.46 * 200, 880 - 0.46 * 470, 0.46))

    parts.append(willow())
    out = K.wrap("0 0 %d %d" % (W, H), "\n".join(parts),
                 title="场景应用 / Lifestyle · 水乡研学")
    K.write(os.path.join(ROOT, "assets", "mockups", "lifestyle-study.svg"), out)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "assets", "final"), exist_ok=True)
    hero()
    lifestyle()
