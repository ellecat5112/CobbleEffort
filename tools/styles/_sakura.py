"""
Sakura collection: Pokemon in cherry-blossom season.

Looks (one per line, three lines each):
  blossom      blush pink scattered with five-petalled white-pink blossoms
  hanami       pale petal cream with dark cherry branches carrying clusters of blossom
  yozakura     night sakura: deep navy with glowing pink blossoms and warm paper lanterns
  kimono       pink silk printed with sakura, a red obi with a gold cord round the middle
  petal_storm  soft blush with loose petals blowing across, drifting in the dark
  spring       fresh spring green dotted with pink blossoms
The eyes keep their own colours. Emissive layer (BLOOM) for the night blossoms, lanterns and drifting petals.
Shiny: white-and-gold blossoms (pale ume plum colours).
"""
from __future__ import annotations

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

BLOOM = {"name": "bloom", "emissive": True, "translucent": True, "frames": 4, "fps": 3}


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def flower(c, x, y, R):
    """A five-petalled blossom: petals, and a small centre."""
    r = np.hypot(c.xx - x, c.yy - y)
    th = np.arctan2(c.yy - y, c.xx - x)
    return r <= R * (0.62 + 0.38 * np.cos(5 * th)), r <= R * 0.28


def scatter(c, rng, n, rmin, rmax, where=None):
    petals = np.zeros_like(c.alpha)
    centres = np.zeros_like(c.alpha)
    ys, xs = np.nonzero((c.alpha & ~c.eye) if where is None else where)
    for _ in range(n):
        if len(xs) == 0:
            break
        k = rng.integers(len(xs))
        p, cc = flower(c, xs[k], ys[k], max(2.2, rng.uniform(rmin, rmax) * c.u))   # readable at 1 px per unit
        petals |= p
        centres |= cc
    return petals, centres


def silk(c, colour, k=0.4):
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None])


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    mottle = noise(c.h, c.w, 6 * u, rng, 2)
    petal = np.array([255, 250, 236] if c.shiny else [255, 236, 244], np.float32)
    centre = np.array([230, 180, 60] if c.shiny else [220, 70, 120], np.float32)
    pink = (lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], 0.12)[0, 0]) if c.shiny else (lambda rgb: np.array(rgb, np.float32))
    n = max(3, int(_area(c) / 90))
    if look == "blossom":
        rgb = ramp(even([pink((196, 110, 140)), pink((246, 180, 204)), pink((255, 230, 240))]), c.lum * 0.6 + mottle * 0.3)
        p, cc = scatter(c, rng, n, 1.2, 2.0)
    elif look == "hanami":
        rgb = ramp(even([(200, 180, 170), (240, 226, 222), (255, 246, 244)]), c.lum * 0.6 + mottle * 0.3)
        branch = bolts(c, rng, max(1, int(_area(c) / 400)), 10, 1.5 * u, jitter=0.4, branch=0.25) & body
        if u >= 3:
            branch = dilate(branch, u // 3) & body
        rgb = np.where(branch[..., None], np.array([104, 78, 70], np.float32) * (0.85 + 0.3 * mottle[..., None]), rgb)
        near = dilate(branch, 2 * u) & body
        p, cc = scatter(c, rng, n * 2, 0.9, 1.5, where=near)
        p2, cc2 = scatter(c, rng, n, 1.0, 1.6)
        p, cc = p | p2, cc | cc2
        centre = np.array([250, 214, 120], np.float32)
        petal = pink((240, 150, 186)) if not c.shiny else petal
    elif look == "yozakura":
        rgb = ramp(even([(10, 12, 34), (28, 32, 70), (60, 66, 120)]), c.lum * 0.6 + mottle * 0.3)
        p, cc = scatter(c, rng, n, 1.1, 1.8)
        petal = pink((255, 170, 210)) if not c.shiny else petal
        c.shine(p & body, petal, 0.7)
        lantern = np.zeros_like(c.alpha)
        ys, xs = np.nonzero(body)
        for _ in range(max(1, n // 6)):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            lantern |= ((c.xx - xs[k]) / (1.2 * u)) ** 2 + ((c.yy - ys[k]) / (1.7 * u)) ** 2 <= 1
        lantern &= body
        rgb = np.where(lantern[..., None], np.array([255, 180, 90], np.float32), rgb)
        c.shine(lantern, (255, 170, 80), 0.9)
        c.extra["lantern"] = lantern
    elif look == "kimono":
        rgb = silk(c, pink((226, 120, 156)))
        sheen = (np.abs(((c.xx + c.yy) / (6.0 * u)) % 1 - 0.5) < 0.08)
        rgb = np.where(sheen[..., None], rgb * 1.12, rgb)
        p, cc = scatter(c, rng, n, 1.0, 1.6)
        obi = (np.abs(c.hm - 0.5) < 0.05) & body
        cord = (np.abs(c.hm - 0.5) < 0.01) & body
        rgb = np.where(obi[..., None], silk(c, (176, 26, 44)), rgb)
        p &= ~obi
        cc &= ~obi
        rgb = np.where(cord[..., None], np.array([236, 190, 70], np.float32), rgb)
    elif look == "petal_storm":
        rgb = ramp(even([pink((206, 150, 166)), pink((244, 206, 216)), pink((255, 240, 244))]), c.lum * 0.6 + mottle * 0.3)
        p = loose_petals(c, rng, n * 2, 0) & body
        cc = np.zeros_like(c.alpha)
        c.extra["storm"] = (rng.integers(1 << 30), n * 2)
    elif look == "spring":
        rgb = ramp(even([(90, 140, 70), (150, 196, 120), (206, 232, 176)]), c.lum * 0.6 + mottle * 0.3)
        p, cc = scatter(c, rng, n, 1.0, 1.6)
    else:
        rgb, p, cc = c.a[..., :3], np.zeros_like(c.alpha), np.zeros_like(c.alpha)
    p &= body
    cc &= body
    rgb = np.where(p[..., None], petal * (0.92 + 0.1 * c.lum[..., None]), rgb)
    rgb = np.where(cc[..., None], centre, rgb)
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def loose_petals(c, rng, n, frame):
    """Small rotated oval petals, blown down and to the side by `frame`."""
    m = np.zeros_like(c.alpha)
    ys, xs = np.nonzero(c.alpha & ~c.eye)
    for _ in range(n):
        if len(xs) == 0:
            break
        k = rng.integers(len(xs))
        x0, y0 = xs[k] + frame * c.u * 1.5, ys[k] + frame * c.u
        a = rng.uniform(0, np.pi)
        dx, dy = c.xx - x0, c.yy - y0
        al, ac = dx * np.cos(a) + dy * np.sin(a), -dx * np.sin(a) + dy * np.cos(a)
        m |= (al / (1.0 * c.u)) ** 2 + (ac / (0.55 * c.u)) ** 2 <= 1
    return m


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    if "storm" in c.extra:
        seed, n = c.extra["storm"]
        m = loose_petals(c, np.random.default_rng(seed), n, frame) & c.alpha & ~c.eye
        g = np.where(m, 0.5, g)
        grgb = np.where(m[..., None], np.array([255, 210, 230], np.float32), grgb)
    if "lantern" in c.extra:
        g = np.where(c.extra["lantern"], g0 * [1.0, 0.85, 0.95, 0.8][frame % 4], g)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
