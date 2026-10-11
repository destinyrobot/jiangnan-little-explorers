#!/usr/bin/env python3
"""Derive character pose / expression / composition assets from the two base files."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgkit as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "assets", "characters")

BOY = os.path.join(CH, "xiaozhou-front.svg")
GIRL = os.path.join(CH, "xiaohe-front.svg")

TEAL, GREEN = "#2E7D77", "#79B473"

ARMS_START = "  <!-- arms (behind torso) -->"
NECK = "  <!-- neck -->"


def split(src):
    i = src.index(ARMS_START)
    j = src.index("  <circle", i)          # end of the two hand circles
    j = src.index("\n", j) + 1
    k = src.index(NECK)
    return src[:i], src[j:k], src[k:]


def arms_block(paths):
    out = [ARMS_START, '  <g stroke-linecap="round" fill="none">']
    out += ["    " + p for p in paths]
    out.append("  </g>")
    return "\n".join(out) + "\n"


def hands(pts, r=13):
    return "".join(
        '  <circle cx="%s" cy="%s" r="%s" fill="#F7DCC4"/>\n' % (x, y, r) for x, y in pts
    )


ARM_NORMAL = dict(
    L_up='M160 246c-9 20-15 38-17 58', L_lo='M143 304c-2 12-4 24-5 34',
    R_up='M240 246c9 20 15 38 17 58', R_lo='M257 304c2 12 4 24 5 34',
)


def arm_paths(sleeve, l_up, l_lo, r_up, r_lo):
    return [
        '<path d="%s" stroke="%s" stroke-width="27"/>' % (l_up, sleeve),
        '<path d="%s" stroke="#F7DCC4" stroke-width="22"/>' % l_lo,
        '<path d="%s" stroke="%s" stroke-width="27"/>' % (r_up, sleeve),
        '<path d="%s" stroke="#F7DCC4" stroke-width="22"/>' % r_lo,
    ]


def build_variant(src, name, sleeve, l_up, l_lo, r_up, r_lo, hand_pts, prop=""):
    head, mid, tail = split(src)
    body = head + arms_block(arm_paths(sleeve, l_up, l_lo, r_up, r_lo))
    body = body + mid + prop + tail
    body = body.rstrip()
    assert body.endswith("</svg>")
    body = body[: -len("</svg>")].rstrip() + "\n" + hands(hand_pts) + "</svg>\n"
    K.write(os.path.join(CH, name), body)


# ---------------------------------------------------------------- props
PROP_MAP = """  <g>
    <path d="M150 296l38-11 33 11 33-11 6 56-33 11-33-11-38 11z" fill="#F8F2E6"/>
    <path d="M188 285v68M221 296v68" stroke="#DFD5BE" stroke-width="3"/>
    <path d="M162 322c13-9 24-4 35-11s22-4 31 2" stroke="#2E7D77" stroke-width="4"
          fill="none" stroke-linecap="round" stroke-dasharray="2 10"/>
    <path d="M166 340q13-15 26 0" stroke="#26364F" stroke-width="4" fill="none"
          stroke-linecap="round"/>
    <path d="M161 346h36" stroke="#26364F" stroke-width="3" stroke-linecap="round" opacity=".55"/>
    <circle cx="246" cy="310" r="7" fill="#E9793B"/>
    <circle cx="246" cy="310" r="12" fill="none" stroke="#E9793B" stroke-width="3" opacity=".5"/>
  </g>
"""

PROP_MAG = """  <g>
    <path d="M274 174l-14 22" stroke="#E9793B" stroke-width="12" stroke-linecap="round"/>
    <circle cx="284" cy="164" r="26" fill="#DCEDEA" opacity=".8"/>
    <circle cx="284" cy="164" r="26" fill="none" stroke="#2E7D77" stroke-width="7"/>
    <path d="M274 172q10-13 20 0" stroke="#2E7D77" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M270 184h28" stroke="#2E7D77" stroke-width="3" stroke-linecap="round" opacity=".55"/>
    <path d="M274 192h20" stroke="#2E7D77" stroke-width="3" stroke-linecap="round" opacity=".35"/>
  </g>
"""

PROP_NOTEBOOK = """  <g>
    <rect x="158" y="284" width="84" height="64" rx="8" fill="#F8F2E6"/>
    <rect x="158" y="284" width="14" height="64" rx="7" fill="#79B473"/>
    <rect x="232" y="288" width="12" height="56" rx="5" fill="#E4DAC6"/>
    <rect x="196" y="284" width="8" height="64" fill="#E9793B"/>
    <path d="M174 318c5-13 20-15 27-6-5 13-20 15-27 6z" fill="#79B473" opacity=".92"/>
    <path d="M176 320c8-6 15-8 23-8" stroke="#F8F2E6" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  </g>
"""

PROP_LOTUS = """  <g>
    <path d="M128 96L173 79A52 34 0 1 0 173 113Z" fill="#79B473"/>
    <g stroke="#5E9E58" stroke-width="3" stroke-linecap="round" opacity=".65" fill="none">
      <path d="M128 96L86 82M128 96L94 122M128 96L128 62M128 96L124 130M128 96L164 124"/>
    </g>
    <path d="M130 126c-1 14-1 26 0 36" stroke="#5E9E58" stroke-width="9" stroke-linecap="round"/>
  </g>
"""


def build_variants():
    fwd = dict(
        l_up="M160 246c-11 18-18 34-19 54", l_lo="M141 300c4 12 10 22 17 30",
        r_up="M240 246c11 18 18 34 19 54", r_lo="M259 300c-4 12-10 22-17 30",
    )
    build_variant(K.read(BOY), "xiaozhou-map.svg", TEAL,
                  fwd["l_up"], fwd["l_lo"], fwd["r_up"], fwd["r_lo"],
                  [(158, 330), (242, 330)], PROP_MAP)
    build_variant(K.read(GIRL), "xiaohe-notebook.svg", GREEN,
                  fwd["l_up"], fwd["l_lo"], fwd["r_up"], fwd["r_lo"],
                  [(156, 332), (244, 332)], PROP_NOTEBOOK)
    build_variant(K.read(BOY), "xiaozhou-magnifier.svg", TEAL,
                  ARM_NORMAL["L_up"], ARM_NORMAL["L_lo"],
                  "M240 246c16 0 28-8 34-22", "M274 224c-4-10-10-20-14-26",
                  [(137, 342), (260, 198)], PROP_MAG)
    build_variant(K.read(GIRL), "xiaohe-lotus.svg", GREEN,
                  "M160 246c-18-4-30-16-34-32", "M126 214c0-16 0-32 2-46",
                  ARM_NORMAL["R_up"], ARM_NORMAL["R_lo"],
                  [(129, 162), (263, 342)], PROP_LOTUS)


# ---------------------------------------------------------------- expressions
MOODS = {
    "happy": dict(b1='M168 136q12-9 24-3', b2='M208 133q12-6 24 3',
                  m='<path d="M188 190q12 12 24 0" stroke="#B0574A" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    "curious": dict(b1='M168 131q12-10 24-4', b2='M208 127q12-4 24 6',
                    m='<path d="M191 188q9 11 18 0" stroke="#B0574A" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    "focused": dict(b1='M168 140q12-4 24 2', b2='M208 142q12-6 24-2',
                    m='<path d="M190 192q10 5 20 0" stroke="#B0574A" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    "excited": dict(b1='M166 130q14-12 26-4', b2='M208 126q12-2 26 8',
                    m='<path d="M184 184h32a16 16 0 0 1-32 0z" fill="#B0574A"/>'),
}


def apply_mood(src, mood):
    src = re.sub(r'<path d="M168 136q12-9 24-3"[^/]*/>',
                 '<path d="%s" stroke="#1B2839" stroke-width="5" fill="none" stroke-linecap="round"/>' % mood["b1"], src)
    src = re.sub(r'<path d="M208 133q12-6 24 3"[^/]*/>',
                 '<path d="%s" stroke="#1B2839" stroke-width="5" fill="none" stroke-linecap="round"/>' % mood["b2"], src)
    src = re.sub(r'<path d="M18[89] 19[02][^/]*/>',
                 mood["m"], src, count=1)
    return src


def build_expressions():
    cols, cw, chh = 4, 240, 260
    rows = 2
    body = ['  <defs><clipPath id="headclip"><rect x="0" y="0" width="400" height="218"/>'
            "</clipPath></defs>"]
    for r, (label, path) in enumerate([("boy", BOY), ("girl", GIRL)]):
        base = K.read(path)
        for c, mood_name in enumerate(MOODS):
            mood = MOODS[mood_name]
            cx = cw * (c + 0.5)
            cy = chh * (r + 0.5) + 6
            inner = apply_mood(base, mood)
            inner = K.inner_from_string(inner)
            body.append(
                '<g transform="translate(%.1f %.1f) scale(1.05) translate(-200 -148)">'
                '<g clip-path="url(#headclip)">%s</g></g>' % (cx, cy, inner)
            )
    # grid lines
    lines = []
    for c in range(1, cols):
        lines.append('<path d="M%d 0v%d" stroke="#ECECEC"/>' % (cw * c, chh * rows))
    lines.append('<path d="M0 %dh%d" stroke="#ECECEC"/>' % (chh, cw * cols))
    svg = K.wrap("0 0 %d %d" % (cw * cols, chh * rows),
                 "\n".join(lines) + "\n" + "\n".join(body),
                 title="角色表情设定 / Expression Sheet")
    K.write(os.path.join(CH, "expressions.svg"), svg)


def build_duo():
    boy = K.group(BOY, 20, 28, 1.0)
    girl = K.group(GIRL, 200, 28, 1.0)
    svg = K.wrap(
        "0 0 620 540",
        '  <ellipse cx="220" cy="500" rx="120" ry="16" fill="#26364F" opacity=".08"/>'
        "\n" + boy + "\n" + girl,
        title="小舟 & 小荷 双角色组合",
    )
    K.write(os.path.join(CH, "duo.svg"), svg)


def build_sheet():
    TY = 48
    boy = K.group(BOY, 80, TY, 1.0)
    girl = K.group(GIRL, 320, TY, 1.0)
    grid = []
    for x in range(0, 960, 40):
        grid.append('<path d="M%d 0v520" stroke="#EFEFEF"/>' % x)
    for y in range(0, 520, 40):
        grid.append('<path d="M0 %dh960" stroke="#EFEFEF"/>' % y)
    guides, labels = [], []
    marks = [(64, "01"), (148, "02"), (212, "03"), (336, "04"), (472, "05")]
    for cy, num in marks:
        y = TY + cy
        guides.append('<path d="M30 %dH760" stroke="#2E7D77" stroke-width="1.5" '
                      'stroke-dasharray="8 8" opacity=".5"/>' % y)
        labels.append(
            '<g><rect x="784" y="%d" width="34" height="22" rx="11" fill="#2E7D77"/>'
            '<text x="801" y="%d" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" '
            'font-size="12" font-weight="700" fill="#FFFFFF">%s</text>'
            '<text x="828" y="%d" font-family="PingFang SC, Helvetica Neue, sans-serif" '
            'font-size="13" fill="#26364F" opacity=".7">%s</text></g>'
            % (y - 11, y + 5, num, y + 5,
               {64: "头顶 / Top", 148: "眼高 / Eye line", 212: "下巴 / Chin",
                336: "衣摆 / Hem", 472: "地面 / Ground"}[cy]))
    head = [
        '<text x="30" y="40" font-family="Helvetica Neue, Arial, sans-serif" font-size="13" '
        'font-weight="700" letter-spacing="3" fill="#2E7D77">CHARACTER SCALE SHEET</text>',
        '<text x="30" y="72" font-family="PingFang SC, Helvetica Neue, sans-serif" font-size="22" '
        'font-weight="700" fill="#26364F">角色比例设定</text>',
        '<path d="M30 540h900" stroke="#E0E0E0"/>',
        '<g font-family="PingFang SC, Helvetica Neue, sans-serif" font-size="13" fill="#26364F" opacity=".72">'
        '<text x="30" y="566">头身比 <tspan font-family="Helvetica Neue, Arial, sans-serif" font-weight="700" '
        'opacity="1" fill="#26364F">1 : 2.9</tspan></text>'
        '<text x="250" y="566">网格 <tspan font-family="Helvetica Neue, Arial, sans-serif" font-weight="700" '
        'opacity="1" fill="#26364F">40 px</tspan></text>'
        '<text x="440" y="566">统一肤色 <tspan font-family="Helvetica Neue, Arial, sans-serif" font-weight="700" '
        'opacity="1" fill="#26364F">#F7DCC4</tspan></text>'
        '<text x="700" y="566">统一眼型 · 统一腮红 · 统一无描边上色</text></g>',
    ]
    body = ["  <rect width=\"960\" height=\"560\" fill=\"#FFFFFF\"/>",
            "  " + "\n  ".join(grid), "  " + "\n  ".join(guides),
            boy, girl, "  " + "\n  ".join(head), "  " + "\n  ".join(labels)]
    svg = K.wrap("0 0 960 600", "\n".join(body), title="角色比例设定表 / Character Scale Sheet")
    K.write(os.path.join(CH, "character-sheet.svg"), svg)


if __name__ == "__main__":
    build_variants()
    build_expressions()
    build_duo()
    build_sheet()
