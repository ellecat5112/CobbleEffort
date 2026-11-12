"""
Ancient Ruins collection: Pokemon as relics of lost temples (carved blocks with glyphs; the plain Stone Statues are #8).

Looks (one per line, three lines each):
  aztec       warm sandstone blocks with stepped-fret bands, jade inlays and turquoise-glowing glyphs
  hieroglyph  pale limestone with lapis-and-gold painted bands and rows of carved glyphs glowing amber
  overgrown   grey jungle-temple stone swallowed by moss with vines hanging down, faint green glyph light
  sunken      blue-grey sea-worn stone with barnacles, coral and seaweed, glyphs glowing aqua
  sandstone   wind-eroded sandstone strata in bands of ochre and cream, sand drifted round the feet
  guardian    black basalt cut with glowing orange dot-glyph circuits, like an ancient automaton
Every look: the body cut into stone courses and blocks, cracks and weathering, glowing eyes, and an emissive animated
layer (GLYPH) where the glyphs slowly pulse.
Shiny: the glyph light turned round the colour wheel (and paler stone).
"""
from __future__ import annotations

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

GLYPH = {"name": "glyph", "emissive": True, "translucent": True, "frames": 4, "fps": 3}


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def courses(c, n=9):
    """Mortar lines: horizontal courses by height on the model, staggered vertical joints."""
    row = np.floor(c.hm * n).astype(int)
    frac = (c.hm * n) % 1
    horiz = (frac < 0.07)
    bw = 5 * c.u
    joint = (((c.xx + (row % 2) * bw / 2) % bw) < max(1, c.u * 0.5))
    return (horiz | joint) & c.alpha & ~c.eye


def glyphs(c, bands, cell=None, seed=0):
    """Little carved symbols (left-right symmetric 3x3 bitmaps) in cells, only inside height bands [(lo, hi), ...]."""
    u = c.u
    g = cell or 4 * u
    cx, cy = (c.xx // g).astype(np.int64), (c.yy // g).astype(np.int64)
    lx, ly = ((c.xx % g) - u / 2) / u, ((c.yy % g) - u / 2) / u
    inside = (lx >= 0) & (lx < 3) & (ly >= 0) & (ly < 3)
    bit_col = np.clip(lx, 0, 2.99).astype(np.int64)
    bit_col = np.where(bit_col == 2, 0, bit_col)                                  # symmetric: col 2 mirrors col 0
    bit = np.clip(ly, 0, 2.99).astype(np.int64) * 2 + bit_col
    h = (cx * 73856093) ^ (cy * 19349663) ^ (seed * 83492791 + c.seed)
    h = (h * 2654435761) % (2 ** 31)
    on = ((h >> bit) & 1).astype(bool) & inside
    band = np.zeros_like(c.alpha)
    for lo, hi in bands:
        band |= (c.hm >= lo) & (c.hm < hi)
    return on & band & c.alpha & ~c.eye


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 5 * u, rng, 3)
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    shade = c.lum * 0.45 + mottle * 0.45
    bands = [(0.42, 0.52), (0.7, 0.76)]
    if look == "aztec":
        rgb = ramp(even([(84, 56, 38), (160, 116, 76), (206, 164, 112), (236, 208, 160)]), shade)
        glow = col((80, 255, 220))
        fret = glyphs(c, [(0.6, 0.66)], cell=2 * u, seed=7)                        # stepped-fret band
        rgb = np.where(fret[..., None], rgb * 0.55, rgb)
        jade = (noise(c.h, c.w, 3 * u, rng, 1) > 0.78) & c.alpha & ~c.eye & ~fret
        rgb = np.where(jade[..., None], np.array([60, 160, 120], np.float32) * (0.7 + 0.4 * mottle[..., None]), rgb)
    elif look == "hieroglyph":
        rgb = ramp(even([(130, 118, 92), (196, 184, 152), (226, 216, 186), (246, 240, 220)]), shade)
        glow = col((255, 190, 90))
        for lo, hi in bands:                                                     # painted borders round each band
            edge = ((np.abs(c.hm - lo) < 0.012) | (np.abs(c.hm - hi) < 0.012)) & c.alpha & ~c.eye
            rgb = np.where(edge[..., None], np.array([40, 66, 160], np.float32), rgb)
            gold = ((np.abs(c.hm - lo + 0.02) < 0.007) | (np.abs(c.hm - hi - 0.02) < 0.007)) & c.alpha & ~c.eye
            rgb = np.where(gold[..., None], np.array([226, 182, 70], np.float32), rgb)
    elif look == "overgrown":
        rgb = ramp(even([(46, 50, 46), (100, 104, 96), (146, 148, 138), (186, 188, 178)]), shade)
        glow = col((150, 255, 120))
        moss = (noise(c.h, c.w, 4 * u, rng, 2) + c.hm * 0.35 > 0.78) & c.alpha & ~c.eye
        rgb = np.where(moss[..., None], ramp(even([(40, 70, 24), (80, 120, 40), (130, 170, 70)]), mottle), rgb)
        vine = np.zeros_like(c.alpha)
        ys, xs = np.nonzero(c.alpha)
        for _ in range(max(2, int(_area(c) / 120))):
            k = rng.integers(len(xs))
            x0, y0, L = xs[k], ys[k], rng.integers(3, 9) * u
            wob = (np.sin((c.yy - y0) / (1.5 * u)) * 0.6 * u).astype(np.float32)
            vine |= (np.abs(c.xx - x0 - wob) < max(0.6, u * 0.45)) & (c.yy >= y0) & (c.yy < y0 + L)
        vine &= c.alpha & ~c.eye
        rgb = np.where(vine[..., None], np.array([50, 104, 36], np.float32), rgb)
        bands = [(0.45, 0.5)]
    elif look == "sunken":
        rgb = ramp(even([(30, 44, 56), (70, 90, 104), (112, 132, 142), (160, 178, 184)]), shade)
        glow = col((90, 230, 255))
        barn = (rng.random((c.h, c.w)) < 0.02) & c.alpha & ~c.eye
        barn = dilate(barn, max(0, u // 3)) & c.alpha & ~c.eye
        rgb = np.where(barn[..., None], np.array([214, 206, 186], np.float32), rgb)
        coral = (noise(c.h, c.w, 3 * u, rng, 1) > 0.8) & c.alpha & ~c.eye
        rgb = np.where(coral[..., None], np.array([236, 110, 110], np.float32) * (0.7 + 0.4 * mottle[..., None]), rgb)
        weed = (np.abs(np.sin(c.xx / (2.0 * u) + np.sin(c.yy / (1.2 * u)))) < 0.18) & (c.hm < 0.3) & c.alpha & ~c.eye
        rgb = np.where(weed[..., None], np.array([36, 92, 52], np.float32), rgb)
    elif look == "sandstone":
        strata = (c.hm * 14 + mottle * 1.5) % 4
        rgb = ramp([(0, (170, 118, 74)), (1, (220, 178, 118)), (2, (186, 134, 86)), (3, (234, 204, 152)),
                    (4, (170, 118, 74))], strata / 4.0)
        rgb = rgb * (0.75 + 0.35 * c.lum[..., None])
        glow = col((255, 210, 120))
        sand = (c.hm < 0.1 + 0.06 * mottle) & c.alpha & ~c.eye
        rgb = np.where(sand[..., None], np.array([236, 214, 164], np.float32) * (0.9 + 0.15 * mottle[..., None]), rgb)
    elif look == "guardian":
        rgb = ramp(even([(10, 10, 14), (34, 34, 40), (64, 64, 70), (104, 102, 106)]), shade)
        glow = col((255, 160, 50))
        g2 = 2 * u
        dots = (((c.xx % g2) < max(1, u)) & ((c.yy % g2) < max(1, u)))
        h = ((c.xx // g2).astype(np.int64) * 92821 ^ (c.yy // g2).astype(np.int64) * 68917 ^ c.seed) % 5
        circuit = dots & (h < 2) & (((c.hm * 3) % 1) < 0.35) & c.alpha & ~c.eye
        c.extra["circuit"] = circuit
    else:
        rgb, glow = c.a[..., :3], col((255, 255, 255))
    if c.shiny:
        rgb = rgb * 0.8 + 255 * 0.2
    mortar = courses(c)
    rgb = np.where(mortar[..., None], rgb * 0.6, rgb)
    crack = bolts(c, rng, max(2, int(_area(c) / 300)), 6, 1.2 * u, jitter=0.8, branch=0.2) & ~c.eye
    rgb = np.where(crack[..., None], rgb * 0.45, rgb)
    carved = c.extra.get("circuit") if look == "guardian" else glyphs(c, bands)
    rgb = np.where(carved[..., None], rgb * 0.35 + glow * 0.5, rgb)
    c.shine(carved, glow, 1.0)
    c.extra["carved"] = carved
    rgb = np.where(c.eye[..., None], glow, rgb)
    c.shine(c.eye, glow, 1.0)
    return rgb


def animate(glow, frame, c):
    return np.where(c.extra["carved"], glow * [1.0, 0.75, 0.5, 0.75][frame % 4], glow)


def make(look):
    return _make(paint, look, animate, paint_layers=True)
