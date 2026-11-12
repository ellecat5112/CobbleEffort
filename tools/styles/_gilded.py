"""
Gilded collection: Pokemon made precious with gold.

Looks (one per line, three lines each):
  gold_leaf  burnished gold leaf laid in squares over dark red lacquer, flaking at the edges
  kintsugi   the Pokemon's own colours as glazed ceramic, its cracks mended with seams of gold
  filigree   black velvet worked all over with fine gold scrollwork and spirals
  rose_gold  polished rose gold set with tiny diamonds that sparkle
  jewelled   polished gold studded with cabochon rubies, emeralds, sapphires and amethysts
  marble     white marble veined with grey and threaded with gold
Every look: polished metal shading (bright bands like reflections), gem-bright eyes, and an emissive animated layer
(GLINT) where light glints and sparkles off the gold.
Shiny: platinum and silver instead of gold (rose gold turns platinum too), gems turned round the colour wheel.
"""
from __future__ import annotations

import math

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make
from ._void import voronoi_cracks

GLINT = {"name": "glint", "emissive": True, "translucent": True, "frames": 4, "fps": 4}

GOLD = even([(60, 36, 8), (140, 92, 26), (212, 162, 56), (250, 220, 120), (255, 248, 210)])
PLATINUM = even([(36, 36, 44), (104, 104, 116), (184, 186, 198), (230, 232, 240), (255, 255, 255)])
ROSE = even([(80, 40, 36), (170, 100, 90), (226, 160, 142), (250, 210, 196), (255, 244, 238)])
GEMS = [(200, 20, 40), (20, 160, 80), (30, 70, 210), (140, 50, 200)]


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def metal(c, stops, mottle):
    """Polished metal: the original's shading plus bright reflection bands."""
    refl = 0.5 + 0.5 * np.sin(c.hm * 14 + c.xx / (9.0 * c.u) + mottle * 2)
    return ramp(stops, c.lum * 0.45 + refl * 0.4 + mottle * 0.15)


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 6 * u, rng, 2)
    turn = 0.45 if c.shiny else 0.0
    gcol = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    gold_stops = PLATINUM if c.shiny else GOLD
    gold = metal(c, gold_stops, mottle)
    glint_col = (235, 240, 255) if c.shiny else (255, 240, 180)
    eye_col = gcol((60, 220, 120))
    body = c.alpha & ~c.eye
    if look == "gold_leaf":
        lacquer = ramp(even([(24, 8, 6), (56, 18, 14), (84, 30, 22)]), c.lum * 0.6 + mottle * 0.4)
        leaf = noise(c.h, c.w, 4 * u, rng, 2) > 0.22
        rgb = np.where(leaf[..., None], gold, lacquer)
        seam = ((c.xx % (4 * u)) < max(1, u // 3)) | ((c.yy % (4 * u)) < max(1, u // 3))
        rgb = np.where((seam & leaf)[..., None], rgb * 0.82, rgb)
        eye_col = gcol((60, 220, 120))
    elif look == "kintsugi":
        glaze = c.a[..., :3] * 0.55 + np.array([236, 228, 212], np.float32) * 0.45
        rgb = glaze * (0.85 + 0.25 * mottle[..., None])
        crackle = voronoi_cracks(c, rng, 3 * u) & body
        rgb = np.where(crackle[..., None], rgb * 0.88, rgb)
        seam = voronoi_cracks(c, rng, 8 * u) & body
        seam = dilate(seam, max(0, u // 3)) & body
        rgb = np.where(seam[..., None], gold, rgb)
        c.extra["seam"] = seam
        eye_col = (255, 220, 120) if not c.shiny else (230, 236, 250)
    elif look == "filigree":
        rgb = ramp(even([(6, 4, 10), (22, 16, 30), (44, 34, 56)]), c.lum * 0.5 + mottle * 0.4)
        sp = max(9, 8 * u)                                                          # an open gold trellis
        d1 = (c.xx + c.yy) % sp
        d2 = (c.xx - c.yy) % sp
        lw = max(1.0, 0.5 * u)
        fil = (d1 < lw) | (d2 < lw)
        knot = (np.abs(((c.xx + sp / 2) % sp) - sp / 2) <= lw) & (np.abs(((c.yy) % sp) - 0) <= lw)
        if u >= 2:
            fil |= dilate(knot, u // 2)                                             # beads where the lines cross
        if u >= 2:                                                                  # scroll spirals in the gaps
            cell = 10 * u
            lx, ly = (c.xx % cell) - cell / 2, (c.yy % cell) - cell / 2
            r, th = np.sqrt(lx ** 2 + ly ** 2), np.arctan2(ly, lx)
            spiral = (np.abs(((r / (1.2 * u) - th / (2 * math.pi)) % 1) - 0.5) < 0.18) & (r < 3.5 * u)
            fil = (fil & (r >= 3.8 * u)) | spiral
        fil &= body
        rgb = np.where(fil[..., None], gold, rgb)
        eye_col = gcol((220, 30, 60))
    elif look == "rose_gold":
        rgb = metal(c, PLATINUM if c.shiny else ROSE, mottle)
        diamonds = (rng.random((c.h, c.w)) < 0.012) & body
        rgb = np.where(diamonds[..., None], np.array([255, 255, 255], np.float32), rgb)
        c.extra["diamonds"] = diamonds
        eye_col = gcol((120, 220, 255))
    elif look == "jewelled":
        rgb = gold
        ys, xs = np.nonzero(body)
        gems = np.zeros(body.shape, np.int32) - 1
        dist = np.full(body.shape, 1e9, np.float32)
        rad = np.zeros(body.shape, np.float32)
        for i in range(max(3, int(_area(c) / 70))):
            k = rng.integers(len(xs))
            gx, gy, gr = float(xs[k]), float(ys[k]), rng.uniform(0.9, 1.5) * u
            d = np.sqrt((c.xx - gx) ** 2 + (c.yy - gy) ** 2)
            sel = (d <= gr) & (d < dist)
            gems = np.where(sel, i % len(GEMS), gems)
            dist = np.where(sel, d, dist)
            rad = np.where(sel, gr, rad)
        gems = np.where(body, gems, -1)
        for i, g in enumerate(GEMS):
            m = gems == i
            t = np.clip(1 - dist / np.maximum(rad, 1e-3), 0, 1)[..., None]          # domed: brighter in the middle
            colour = gcol(g) * (0.55 + 0.6 * t) + 255 * 0.25 * t ** 3
            rgb = np.where(m[..., None], colour, rgb)
            c.shine(m, gcol(g), 0.25)
        bezel = (dist <= rad + max(0.6, u * 0.4)) & (gems < 0) & body
        rgb = np.where(bezel[..., None], gold * 0.7, rgb)
        eye_col = gcol((200, 20, 40))
    elif look == "marble":
        vein_n = noise(c.h, c.w, 7 * u, rng, 3)
        rgb = ramp(even([(190, 188, 184), (224, 222, 218), (246, 246, 242)]), c.lum * 0.4 + mottle * 0.5)
        grey = (np.abs(np.sin(vein_n * 26)) < 0.07) & body
        rgb = np.where(grey[..., None], rgb * 0.7, rgb)
        gv = bolts(c, rng, max(2, int(_area(c) / 220)), 12, 1.6 * u, jitter=0.4, branch=0.2) & body
        gv = dilate(gv, max(0, u // 3)) & body
        rgb = np.where(gv[..., None], gold, rgb)
        c.extra["seam"] = gv
        eye_col = gcol((30, 70, 210))
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], np.asarray(eye_col, np.float32), rgb)
    c.shine(c.eye, eye_col, 1.0)
    # glints: the brightest parts of the metal catch the light
    lum = rgb.mean(-1) / 255.0
    c.extra["bright"] = (lum > 0.82) & body
    c.extra["glint_col"] = np.asarray(glint_col, np.float32)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 4099 + frame * 131) % (2 ** 32))
    spark = c.extra["bright"] & (rng.random(g.shape) < 0.08)
    if "diamonds" in c.extra:
        spark |= c.extra["diamonds"] & (rng.random(g.shape) < 0.5)
    if "seam" in c.extra:
        band = np.abs(((c.hm * 2 - frame / 4.0) % 1) - 0.5) < 0.08                    # light running along the seams
        spark |= c.extra["seam"] & band
    g = np.where(spark, 0.8, g)
    grgb = np.where(spark[..., None], c.extra["glint_col"], grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, layer_alpha=170, paint_layers=True)
