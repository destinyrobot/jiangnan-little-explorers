#!/usr/bin/env python3
"""Inject inlined character artwork into product/mockup SVGs.

Markers look like:  <!--INJECT:path/to.svg|scale|x|y-->
and are replaced (once) with a self-contained <g>. Re-running is a no-op.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgkit as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = re.compile(r"<!--INJECT:([^|]+)\|([\d.]+)\|(-?[\d.]+)\|(-?[\d.]+)-->")


def main(patterns):
    total = 0
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "assets")):
        for name in sorted(files):
            if not name.endswith(".svg"):
                continue
            if patterns and not any(p in name for p in patterns):
                continue
            path = os.path.join(dirpath, name)
            src = K.read(path)
            if "<!--INJECT:" not in src:
                continue

            def repl(m):
                rel, s, x, y = m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4))
                target = os.path.join(ROOT, rel)
                return K.group(target, x, y, s)

            out = MARK.sub(repl, src)
            K.write(path, out)
            total += 1
    print("injected into", total, "file(s)")


if __name__ == "__main__":
    main(sys.argv[1:])
