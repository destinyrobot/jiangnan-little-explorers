#!/usr/bin/env python3
"""Mean absolute pixel diff between two images (headless Chrome canvas).

Usage: python3 scripts/imgdiff.py a.png b.png
"""
import json
import os
import re
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    a, b = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    html = """<!doctype html><meta charset="utf-8"><body style="margin:0">
<img id="a" src="file://%s"><img id="b" src="file://%s">
<div id="out">pending</div>
<script>
Promise.all([a.decode(), b.decode()]).then(() => {
  const W = Math.min(a.naturalWidth, b.naturalWidth);
  const H = Math.min(a.naturalHeight, b.naturalHeight);
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const x = c.getContext('2d');
  x.drawImage(a, 0, 0); const da = x.getImageData(0, 0, W, H).data;
  x.clearRect(0, 0, W, H);
  x.drawImage(b, 0, 0); const db = x.getImageData(0, 0, W, H).data;
  let s = 0;
  for (let i = 0; i < da.length; i += 4)
    s += Math.abs(da[i]-db[i]) + Math.abs(da[i+1]-db[i+1]) + Math.abs(da[i+2]-db[i+2]);
  const pct = s / (W * H * 3) / 255 * 100;
  document.getElementById('out').textContent =
    'DIFF ' + pct.toFixed(4) + '% over ' + W + 'x' + H +
    ' | ' + a.naturalWidth + 'x' + a.naturalHeight +
    ' vs ' + b.naturalWidth + 'x' + b.naturalHeight;
});
</script>""" % (a, b)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html)
        path = fh.name
    out = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=8000",
         "--dump-dom", "file://%s" % path],
        capture_output=True, text=True, check=False,
    )
    os.unlink(path)
    m = re.search(r"DIFF[^<]*", out.stdout)
    print(m.group(0) if m else "no result")


if __name__ == "__main__":
    sys.exit(main())
