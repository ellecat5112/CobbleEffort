"""
Zelda collection: Pokemon of the kingdom of Hyrule (inspired by The Legend of Zelda; original patterns, no game art).

Looks (one per line, three lines each):
  tunic    the hero's green tunic with a brown belt, pale leggings and a golden triangle emblem on the chest
  ancient  ancient tech: slate stone carved with glowing cyan circuit arcs that pulse
  zora     sleek blue scales with a silver-white belly
  goron    rocky brown hide split by darker cracks, a warm orange belly
  gerudo   desert crimson with gold bands and turquoise gems, sand at the feet
  korok    wood bark with a crown of leaves on top
Emissive layer (SHEIKAH) for the ancient tech's glow and the gems' gleam. The eyes keep their own colours.
Shiny: twilight: the colours turned round the colour wheel.
"""
from __future__ import annotations

import math

import numpy as np

from ._arc import bolts
from ._cosmic import centre_of, even, hue_turn_fast, noise, ramp
from ._fx import make as _make
from ._pinkan import leaf_mask
from ._void import voronoi_cracks

SHEIKAH = {"name": "sheikah", "emissive": True, "translucent": True, "frames": 4, "fps": 3}


def shade(c, colour, k=0.5):
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None])


def triangle(c, x, y, s):
    """An upward triangle with top vertex (x, y) and side s."""
    h = s * 0.866
    dy = c.yy - y
    return (dy >= 0) & (dy <= h) & (np.abs(c.xx - x) <= dy / h * s / 2)


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    mottle = noise(c.h, c.w, 5 * u, rng, 2)
    glow_m = np.zeros_like(c.alpha)
    gcol = (90, 230, 255)
    if look == "tunic":
        rgb = np.where((c.hm > 0.3)[..., None], shade(c, (46, 140, 60)), shade(c, (232, 226, 206)))
        belt = (np.abs(c.hm - 0.42) < 0.025) & body
        rgb = np.where(belt[..., None], shade(c, (110, 66, 34)), rgb)
        cx, cy, r = centre_of(c.face, c.alpha)
        s = max(4.0, min(r * 1.1, 6 * u))
        h = s * 0.866
        top = cy - h / 2
        big = triangle(c, cx, top, s)
        dy2 = (top + h) - c.yy                                                     # the inverted middle triangle
        hole = (dy2 >= 0) & (dy2 <= h / 2) & (np.abs(c.xx - cx) <= dy2 / (h / 2) * s / 4)
        emblem = big & ~hole & body
        rgb = np.where(emblem[..., None], np.array([240, 200, 60], np.float32), rgb)
        glow_m = emblem
        gcol = (255, 220, 100)
    elif look == "ancient":
        rgb = ramp(even([(24, 28, 34), (52, 58, 66), (96, 102, 108)]), c.lum * 0.5 + mottle * 0.4)
        arcs = np.zeros_like(c.alpha)
        ys, xs = np.nonzero(body)
        for _ in range(max(2, int(c.alpha.sum() / float(u * u) / 160))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            R = rng.uniform(1.5, 3.0) * u
            d = np.hypot(c.xx - xs[k], c.yy - ys[k])
            a = np.arctan2(c.yy - ys[k], c.xx - xs[k])
            arcs |= (np.abs(d - R) < max(0.5, 0.35 * u)) & (np.cos(a + rng.uniform(0, 6.3)) > -0.3)
        arcs |= bolts(c, rng, max(2, int(c.alpha.sum() / float(u * u) / 250)), 6, 1.5 * u, jitter=0.15, branch=0.1)
        arcs &= body
        rgb = np.where(arcs[..., None], np.array([120, 236, 255], np.float32), rgb)
        glow_m = arcs
    elif look == "zora":
        cell = 3 * u
        row = c.yy // cell
        lx = ((c.xx + (row % 2) * cell / 2) % cell) - cell / 2
        ly = (c.yy % cell) - cell
        scale_edge = np.abs(np.hypot(lx, ly) - cell * 0.9) < max(0.5, 0.3 * u)
        rgb = shade(c, (60, 130, 210))
        rgb = np.where(scale_edge[..., None], rgb * 0.75, rgb)
        belly = (c.hm < 0.4) & body
        rgb = np.where(belly[..., None], shade(c, (226, 236, 246)), rgb)
    elif look == "goron":
        rgb = shade(c, (124, 92, 62)) * (0.85 + 0.3 * mottle[..., None])
        crack = voronoi_cracks(c, rng, 5 * u) & body
        rgb = np.where(crack[..., None], np.array([60, 40, 26], np.float32), rgb)
        belly = (c.hm < 0.45) & (mottle > 0.45) & body
        rgb = np.where(belly[..., None], shade(c, (226, 150, 80)), rgb)
    elif look == "gerudo":
        rgb = shade(c, (176, 40, 50))
        gold = ((np.abs(c.hm - 0.56) < 0.02) | (np.abs(c.hm - 0.78) < 0.02)) & body
        rgb = np.where(gold[..., None], np.array([236, 190, 70], np.float32), rgb)
        gem = gold & (((c.xx // max(1, 2 * u)) % 3) == 0)
        rgb = np.where(gem[..., None], np.array([60, 210, 190], np.float32), rgb)
        sand = (c.hm < 0.12 + 0.05 * mottle) & body
        rgb = np.where(sand[..., None], shade(c, (226, 196, 140)), rgb)
        glow_m = gem
        gcol = (90, 240, 210)
    elif look == "korok":
        grain = (np.abs(np.sin(c.xx / (0.9 * u) + mottle * 4)) < 0.3)
        rgb = shade(c, (140, 98, 56))
        rgb = np.where((grain & body)[..., None], rgb * 0.75, rgb)
        leaves = leaf_mask(c, rng) & (c.hm > 0.6) & body
        rgb = np.where(leaves[..., None], shade(c, (90, 170, 60)), rgb)
    else:
        rgb = c.a[..., :3]
    if c.shiny:
        rgb = hue_turn_fast(rgb, 0.45)
        gcol = tuple(hue_turn_fast(np.array(gcol, np.float32)[None, None], 0.45)[0, 0])
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.shine(glow_m & body, gcol, 0.8)
    c.extra["glow_m"] = glow_m & body
    return rgb


def animate(glow, frame, c):
    return np.where(c.extra["glow_m"], glow * [1.0, 0.7, 0.45, 0.7][frame % 4], glow)


def make(look):
    return _make(paint, look, animate, paint_layers=True)
