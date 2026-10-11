#!/usr/bin/env python3
"""Build a contact-sheet HTML from SVG files and screenshot it with headless Chrome.

Usage:
  python3 scripts/contact.py <output.png> <cols> <cell_w> <cell_h> <file.svg> [more.svg ...]
  python3 scripts/contact.py preview/chars.png 3 320 420 assets/characters/*.svg
"""
import os
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    out = sys.argv[1]
    cols = int(sys.argv[2])
    cw = int(sys.argv[3])
    ch = int(sys.argv[4])
    files = [os.path.abspath(f) for f in sys.argv[5:]]
    if not files:
        print("no input files")
        return 1

    cells = []
    for f in files:
        rel = os.path.relpath(f, ROOT)
        name = os.path.basename(f)
        cells.append(
            '<figure class="c"><img src="file://%s" style="width:%dpx;height:%dpx">'
            "<figcaption>%s</figcaption></figure>" % (f, cw - 30, ch - 54, name)
        )
    rows = (len(files) + cols - 1) // cols
    html = """<!doctype html><meta charset="utf-8"><style>
    body{margin:0;background:#fff;font:12px -apple-system,sans-serif;padding:16px}
    .g{display:grid;grid-template-columns:repeat(%d,%dpx);gap:8px}
    .c{margin:0;border:1px solid #e6e6e6;display:flex;flex-direction:column;
       align-items:center;justify-content:center;height:%dpx;background:#fff}
    .c img{object-fit:contain;max-width:100%%;max-height:100%%}
    figcaption{color:#999;font-size:11px;margin-top:6px}
    </style><div class="g">%s</div>""" % (cols, cw, ch, "".join(cells))

    w = cols * cw + 40
    h = rows * ch + 40
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html)
        path = fh.name
    out_abs = os.path.abspath(out)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1",
         "--screenshot=%s" % out_abs, "--window-size=%d,%d" % (w, h),
         "file://%s" % path],
        check=False, capture_output=True,
    )
    os.unlink(path)
    print(out_abs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
