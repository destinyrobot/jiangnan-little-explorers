#!/usr/bin/env python3
"""Screenshot one <section> of index.html standalone (headless Chrome).

Usage: python3 scripts/section_shot.py <section_id> <out.png> [window_h]
"""
import os
import re
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    sid = sys.argv[1]
    out = os.path.abspath(sys.argv[2])
    wh = int(sys.argv[3]) if len(sys.argv) > 3 else 2000

    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
        page = fh.read()
    css = re.search(r"<style>(.*?)</style>", page, re.S).group(1)
    m = re.search(r'<section[^>]*id="%s".*?</section>' % sid, page, re.S)
    if not m:
        print("section not found:", sid)
        return 1
    tmp = os.path.join(ROOT, ".sec_%s.html" % sid)
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(
            '<!DOCTYPE html><meta charset="utf-8"><style>%s</style><body>%s</body>'
            % (css, m.group(0))
        )
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         "--virtual-time-budget=9000", "--screenshot=%s" % out,
         "--window-size=1440,%d" % wh, "file://%s" % tmp],
        check=False, capture_output=True,
    )
    os.unlink(tmp)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
