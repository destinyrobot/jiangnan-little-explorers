#!/usr/bin/env python3
"""Generate assets/mockups/product-grid.svg (3x2 series matrix) from the 6 SKU files."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgkit as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKUS = [
    "sku01-canvas-bag.svg",
    "sku02-water-bottle.svg",
    "sku03-notebook.svg",
    "sku04-sticker-set.svg",
    "sku05-badge-magnet.svg",
    "sku06-tshirt-cap.svg",
]

W, H = 1600, 900
MARGIN_X, MARGIN_Y, GAP = 70, 70, 40
COLS, ROWS = 3, 2
CELL_W = (W - 2 * MARGIN_X - (COLS - 1) * GAP) / COLS  # 460
SCALE = CELL_W / 900.0
CELL_H = 700 * SCALE  # 357.8


def main():
    cells = []
    for i, name in enumerate(SKUS):
        c, r = i % COLS, i // COLS
        x = MARGIN_X + c * (CELL_W + GAP)
        y = MARGIN_Y + r * (CELL_H + GAP)
        body = K.inner(os.path.join(ROOT, "assets", "products", name))
        body = K.remap_ids(body, "sku%d" % (i + 1))
        cells.append(
            '<g transform="translate(%s %s) scale(%s)">\n%s\n</g>'
            % (K.fmt(x), K.fmt(y), K.fmt(SCALE), body)
        )

    body = (
        '<rect width="%d" height="%d" fill="#F4ECDD"/>\n'
        '<rect x="40" y="40" width="%d" height="%d" rx="26" fill="#F7F4ED"/>\n%s'
        % (W, H, W - 80, H - 80, "\n".join(cells))
    )
    out = os.path.join(ROOT, "assets", "mockups", "product-grid.svg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    K.write(
        out,
        K.wrap("0 0 %d %d" % (W, H), body, title="系列产品矩阵 / Product Grid 3×2"),
    )


if __name__ == "__main__":
    main()
