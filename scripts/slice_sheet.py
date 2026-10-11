#!/usr/bin/env python3
"""Slice a tall page screenshot into an overview contact sheet.

Usage: python3 scripts/slice_sheet.py <page.png> <out.png> <cols> <slice_h> <cell_w>
"""
import os
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    cols = int(sys.argv[3])
    slice_h = int(sys.argv[4])
    cell_w = int(sys.argv[5])

    import struct
    with open(src, "rb") as fh:
        head = fh.read(26)
    pw, ph = struct.unpack(">II", head[16:24])

    s = cell_w / float(pw)
    cell_h = int(slice_h * s)
    n = (ph + slice_h - 1) // slice_h
    cells = []
    for i in range(n):
        y = i * slice_h
        cells.append(
            '<figure><div class="m" style="width:%dpx;height:%dpx">'
            '<img src="file://%s" style="width:%dpx;margin-top:%dpx"></div>'
            '<figcaption>slice %02d · y=%d</figcaption></figure>'
            % (cell_w, cell_h, src, cell_w, int(-y * s), i, y)
        )
    rows = (n + cols - 1) // cols
    html = """<!doctype html><meta charset="utf-8"><style>
    body{margin:0;background:#888;font:11px -apple-system,sans-serif;padding:10px}
    .g{display:grid;grid-template-columns:repeat(%d,%dpx);gap:8px}
    figure{margin:0;background:#fff;border:1px solid #444}
    .m{overflow:hidden;position:relative}
    img{display:block;position:absolute;left:0}
    figcaption{color:#333;font-size:11px;padding:3px 4px;text-align:center}
    </style><div class="g">%s</div>""" % (cols, cell_w, "".join(cells))
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html)
        path = fh.name
    w = cols * cell_w + 40
    h = rows * (cell_h + 22) + 30
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--screenshot=%s" % out,
         "--window-size=%d,%d" % (w, h), "file://%s" % path],
        check=False, capture_output=True,
    )
    os.unlink(path)
    print("%s  (%dx%d, %d slices)" % (out, w, h, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
