#!/usr/bin/env python3
"""Lay out tall PNG screenshots side by side into one overview sheet.

Usage: python3 scripts/sec_sheet.py <out.png> <cols> <cell_w> <file.png> [more.png ...]
"""
import os
import struct
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def size(path):
    with open(path, "rb") as fh:
        head = fh.read(26)
    return struct.unpack(">II", head[16:24])


def main():
    out = os.path.abspath(sys.argv[1])
    cols = int(sys.argv[2])
    cw = int(sys.argv[3])
    files = [os.path.abspath(f) for f in sys.argv[4:]]
    cells, row_h, rows = [], [], []
    for f in files:
        w, h = size(f)
        ch = int(h * cw / float(w))
        cells.append(
            '<figure><img src="file://%s" style="width:%dpx;height:%dpx">'
            "<figcaption>%s</figcaption></figure>" % (f, cw, ch, os.path.basename(f))
        )
    n = len(files)
    # pack into rows of `cols`
    idx = 0
    y = 0
    layout = ""
    gap = 10
    for r in range((n + cols - 1) // cols):
        x = 0
        rh = 0
        for c in range(cols):
            if idx >= n:
                break
            w, h = size(files[idx])
            ch = int(h * cw / float(w))
            layout += (
                '<figure style="position:absolute;left:%dpx;top:%dpx;width:%dpx">'
                '<img src="file://%s" style="width:%dpx;height:%dpx">'
                "<figcaption>%s</figcaption></figure>"
                % (x, y, cw, files[idx], cw, ch, os.path.basename(files[idx]))
            )
            rh = max(rh, ch + 20)
            x += cw + gap
            idx += 1
        y += rh + gap
    total_w = cols * cw + (cols - 1) * gap + 20
    total_h = y + 20
    html = """<!doctype html><meta charset="utf-8"><style>
    body{margin:0;background:#777;position:relative}
    figure{margin:0;background:#fff;border:1px solid #333}
    img{display:block}
    figcaption{font:11px -apple-system,sans-serif;color:#222;text-align:center;padding:3px}
    </style>%s""" % layout
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html)
        path = fh.name
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--screenshot=%s" % out,
         "--window-size=%d,%d" % (total_w, total_h), "file://%s" % path],
        check=False, capture_output=True,
    )
    os.unlink(path)
    print("%s (%dx%d)" % (out, total_w, total_h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
