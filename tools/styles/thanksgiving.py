"""
Thanksgiving collection look: "Harvest".

* every colour is moved onto an autumn harvest palette, keeping its lightness so the original
  markings stay readable: deep reds become cranberry, pinks peach, oranges pumpkin, yellows maize gold, greens sage,
  blues and cyans chestnut and toasted squash, purples plum
* greys, whites and blacks become warm neutrals: pie-crust cream, cinnamon, dark roast
* a golden-brown "roast glaze" darkens the edges of each painted area
* a few fallen maple leaves (pumpkin / amber / gold) are stuck to the fur
* eyes keep their original colours (found with Cobblemon's alpha-eyes masks)
* shinies become a "golden harvest" version: everything pulled toward honey-gold
* glowing (emissive) parts keep glowing, recoloured like candlelight
"""
from __future__ import annotations

import colorsys
import random

from PIL import Image

EMISSIVE = "retexture"

# original hue (degrees) -> harvest hue (degrees, may be unwrapped) and saturation multiplier
HUE_ANCHORS = [
    (0, -6, 0.95),     # red     -> cranberry
    (30, 24, 1.00),    # orange  -> pumpkin
    (60, 43, 0.95),    # yellow  -> maize gold
    (120, 72, 0.55),   # green   -> sage / olive
    (180, 36, 0.60),   # cyan    -> toasted squash
    (240, 22, 0.55),   # blue    -> chestnut
    (285, -40, 0.55),  # purple  -> plum
    (330, -18, 0.80),  # magenta -> cranberry wine
    (360, -6, 0.95),   # red again (wrap)
]
GOLD_HUE = 40
# warm neutrals by lightness: dark roast -> cinnamon -> pie crust -> whipped cream
NEUTRALS = [
    (0.00, (38, 22, 14)),
    (0.30, (92, 54, 30)),
    (0.55, (176, 118, 64)),
    (0.80, (232, 196, 140)),
    (1.00, (250, 238, 214)),
]
# warm oranges and golds only: dark red leaves read as stains from a distance
LEAF_COLOURS = [(224, 122, 36), (236, 172, 48), (210, 96, 30)]
# 7x7 maple leaf; 2 = vein (darker)
LEAF = [
    "...1...",
    ".1.1.1.",
    "1112111",
    ".11211.",
    "1112111",
    "...2...",
    "...2...",
]


def lerp(a, b, t):
    return a + (b - a) * t


def neutral(l: float):
    l = max(0.0, min(1.0, l))
    for (p0, c0), (p1, c1) in zip(NEUTRALS, NEUTRALS[1:]):
        if l <= p1:
            t = (l - p0) / (p1 - p0)
            return tuple(lerp(c0[i], c1[i], t) for i in range(3))
    return NEUTRALS[-1][1]


def harvest_hue(h_deg: float):
    for (h0, t0, s0), (h1, t1, s1) in zip(HUE_ANCHORS, HUE_ANCHORS[1:]):
        if h_deg <= h1:
            t = (h_deg - h0) / (h1 - h0)
            return lerp(t0, t1, t) % 360, lerp(s0, s1, t)
    return HUE_ANCHORS[-1][1] % 360, HUE_ANCHORS[-1][2]


def recolour(r: int, g: int, b: int, shiny: bool):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    nr, ng, nb = neutral(l)
    if s < 0.12 or l < 0.06 or l > 0.97:
        out = (nr, ng, nb)
    else:
        th, smul = harvest_hue(h * 360)
        # light reds and pinks become peach / apricot (pie filling) instead of staying pink
        red_dist = min(abs(th - 0), abs(th - 360)) if th > 180 or th < 20 else 99
        if red_dist < 25 and l > 0.5:
            t = min(1.0, (l - 0.5) / 0.25)
            th = (th + (((22 - th + 180) % 360) - 180) * t) % 360
        ts = max(0.30, min(0.85, s * smul + 0.12))
        tl = max(0.10, min(0.90, l * 0.92 + 0.03))
        cr, cg, cb = colorsys.hls_to_rgb(th / 360, tl, ts)
        # very pale or dull colours lean toward the warm neutral for the same lightness
        w = max(0.0, min(1.0, (s - 0.12) / 0.35))
        out = (lerp(nr, cr * 255, w), lerp(ng, cg * 255, w), lerp(nb, cb * 255, w))
    if shiny:
        gh, gl, gs = colorsys.rgb_to_hls(out[0] / 255, out[1] / 255, out[2] / 255)
        dh = ((GOLD_HUE / 360 - gh + 0.5) % 1.0) - 0.5
        gr, gg, gb = colorsys.hls_to_rgb((gh + dh * 0.7) % 1.0, min(0.92, gl * 1.06 + 0.03), min(1.0, gs * 0.9 + 0.2))
        out = (gr * 255, gg * 255, gb * 255)
    return tuple(int(max(0, min(255, c))) for c in out)


def retexture(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool,
              frame: int = 0, layer: bool = False) -> Image.Image:
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)

    eye = [[False] * w for _ in range(h)]
    if eyes is not None:
        e = eyes.convert("RGBA").resize((w, h), Image.NEAREST).load()
        for y in range(h):
            for x in range(w):
                eye[y][x] = e[x, y][3] > 0 and src[x, y][3] > 0

    out = Image.new("RGBA", (w, h))
    o = out.load()
    cache: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a == 0:
                o[x, y] = (0, 0, 0, 0)
            elif eye[y][x]:
                o[x, y] = (r, g, b, a)
            else:
                key = (r, g, b)
                if key not in cache:
                    cache[key] = recolour(r, g, b, shiny)
                o[x, y] = cache[key] + (a,)

    # roast glaze: pixels on the edge of a painted area turn a deeper golden brown
    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and src[x, y][3] > 0

    edges = [(x, y) for y in range(h) for x in range(w)
             if src[x, y][3] > 0 and not eye[y][x]
             and not all(opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in edges:
        r, g, b, a = o[x, y]
        o[x, y] = (int(r * 0.80 + 18), int(g * 0.70 + 6), int(b * 0.55), a)

    # fallen maple leaves stuck to the fur
    size = len(LEAF) * scale
    wanted = max(2, (w * h) // (64 * 64) * 2 + rng.randint(1, 3))
    placed, tries = 0, 0
    while placed < wanted and tries < 400:
        tries += 1
        x0, y0 = rng.randrange(0, max(1, w - size)), rng.randrange(0, max(1, h - size))
        cells = [(x0 + i, y0 + j) for j in range(size) for i in range(size)]
        if not all(src[x, y][3] > 0 and not eye[y][x] for x, y in cells):
            continue
        colour = rng.choice(LEAF_COLOURS)
        if shiny:
            colour = (230, 176, 52)
        flip = rng.random() < 0.5
        for j, row in enumerate(LEAF):
            for i, ch in enumerate(row):
                if ch == ".":
                    continue
                c = colour if ch == "1" else tuple(int(v * 0.74) for v in colour)
                ii = len(row) - 1 - i if flip else i
                for sy in range(scale):
                    for sx in range(scale):
                        px, py = x0 + ii * scale + sx, y0 + j * scale + sy
                        o[px, py] = c + (src[px, py][3],)
        placed += 1
    return out
