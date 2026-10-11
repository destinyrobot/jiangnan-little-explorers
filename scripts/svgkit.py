#!/usr/bin/env python3
"""Tiny helpers for composing self-contained SVG assets (no external refs)."""
import re

SVG_OPEN = re.compile(r"<svg[^>]*>", re.S)
SVG_CLOSE = "</svg>"


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def inner_from_string(s):
    """Strip the root <svg> element and its <title>, returning children markup."""
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    s = SVG_OPEN.sub("", s, count=1)
    if s.rstrip().endswith(SVG_CLOSE):
        s = s.rstrip()[: -len(SVG_CLOSE)]
    return s.strip()


def inner(path):
    """Return the inner markup of an SVG file (defs + content), root removed."""
    return inner_from_string(read(path))


def _unused(path):
    s = read(path)
    s = SVG_OPEN.sub("", s, count=1)
    if s.rstrip().endswith(SVG_CLOSE):
        s = s.rstrip()[: -len(SVG_CLOSE)]
    return s.strip()


def group(path, x=0, y=0, scale=1.0, rotate=0, opacity=None):
    """Inline an SVG as a <g> with transform."""
    t = "translate(%s %s)" % (fmt(x), fmt(y))
    if rotate:
        t += " rotate(%s)" % fmt(rotate)
    if scale != 1.0:
        t += " scale(%s)" % fmt(scale)
    op = ' opacity="%s"' % opacity if opacity is not None else ""
    return '<g transform="%s"%s>\n%s\n</g>' % (t, op, inner(path))


def group_at(path, cx, cy, src_cx=200, src_cy=148, scale=1.0, rotate=0):
    """Inline an SVG so that its (src_cx,src_cy) point lands on (cx,cy)."""
    x = cx - src_cx * scale
    y = cy - src_cy * scale
    return group(path, x, y, scale, rotate)


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(v):
    if isinstance(v, float) and abs(v - round(v)) < 1e-9:
        v = int(round(v))
    if isinstance(v, float):
        return ("%.4f" % v).rstrip("0").rstrip(".")
    return str(v)


def remap_ids(body, prefix):
    """Prefix every id="..." and its url(#...)/href="#..." references."""
    ids = re.findall(r'\bid="([^"]+)"', body)
    for i in ids:
        new = "%s_%s" % (prefix, i)
        body = body.replace('id="%s"' % i, 'id="%s"' % new)
        body = body.replace("url(#%s)" % i, "url(#%s)" % new)
        body = body.replace('href="#%s"' % i, 'href="#%s"' % new)
    return body



def wrap(viewbox, body, width=None, height=None, title=None):
    w, h = viewbox.split()[2], viewbox.split()[3]
    w = width or w
    h = height or h
    t = "<title>%s</title>\n" % _esc(title) if title else ""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" width="%s" '
        'height="%s" role="img">\n%s%s\n</svg>\n' % (viewbox, w, h, t, body)
    )


def write(path, content):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("wrote", path)
