"""
Valentine's Day collection: Pokemon full of love.

Looks (one per line, three lines each):
  hearts        sweet pink covered in red and white hearts
  love_letter   cream writing paper with faint ruled lines and a red wax heart seal on the chest
  chocolate     milk chocolate with darker drizzle, sprinkles and a pink frosted heart
  cupid         angel white with golden arrows and little pink hearts
  roses         deep red rose petals swirling, with green leaves
  candy_hearts  white scattered with pastel candy hearts
Every look: hearts that glow softly and beat in the dark (LOVE). The eyes keep their own colours.
Shiny: the love turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import centre_of, even, hue_turn_fast, noise, ramp
from ._fx import make as _make
from ._pinkan import leaf_mask
from ._undertale import heart

LOVE = {"name": "love", "emissive": True, "translucent": True, "frames": 4, "fps": 3}
PASTELS = [(255, 180, 200), (190, 230, 190), (255, 230, 160), (200, 200, 255), (255, 210, 170), (230, 190, 240)]


def hearts(c, rng, n, rmin, rmax):
    out = []
    ys, xs = np.nonzero(c.alpha & ~c.eye)
    for _ in range(n):
        if len(xs) == 0:
            break
        k = rng.integers(len(xs))
        out.append(heart(c, xs[k], ys[k], max(2.0, rng.uniform(rmin, rmax) * c.u)))
    return out


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    mottle = noise(c.h, c.w, 5 * u, rng, 2)
    lit = (0.75 + 0.35 * c.lum)[..., None]
    n = max(3, int(c.alpha.sum() / float(u * u) / 90))
    glow_m = np.zeros_like(c.alpha)
    cx, cy, r = centre_of(c.face, c.alpha)
    if look == "hearts":
        rgb = col((246, 170, 196)) * lit
        for i, h in enumerate(hearts(c, rng, n, 1.0, 1.8)):
            m = h & body
            rgb = np.where(m[..., None], col((220, 30, 60)) if i % 3 else np.array([255, 246, 248], np.float32), rgb)
            glow_m |= m
    elif look == "love_letter":
        rgb = np.array([244, 234, 214], np.float32) * lit
        ruled = (((c.yy // max(1, u)) % 3) == 0) & body
        rgb = np.where(ruled[..., None], rgb * 0.9 + np.array([150, 160, 200], np.float32) * 0.1, rgb)
        seal = heart(c, cx, cy, max(2.5, min(r * 0.6, 3 * u))) & body
        rgb = np.where(seal[..., None], col((176, 20, 30)) * lit, rgb)
        glow_m = seal
    elif look == "chocolate":
        rgb = ramp(even([(60, 30, 16), (110, 62, 34), (150, 92, 56)]), c.lum * 0.5 + mottle * 0.4)
        drizzle = (np.abs(np.sin(c.xx / (1.4 * u) + np.sin(c.yy / (2.5 * u)) * 2)) < 0.2) & (c.hm > 0.5) & body
        rgb = np.where(drizzle[..., None], np.array([40, 18, 8], np.float32), rgb)
        spr = (rng.random((c.h, c.w)) < 0.02) & body
        rgb = np.where(spr[..., None], np.asarray(PASTELS, np.float32)[rng.integers(len(PASTELS), size=(c.h, c.w))], rgb)
        frost = heart(c, cx, cy, max(2.5, min(r * 0.6, 3 * u))) & body
        rgb = np.where(frost[..., None], col((250, 160, 196)), rgb)
        glow_m = frost
    elif look == "cupid":
        rgb = np.array([248, 246, 250], np.float32) * lit
        arrow = (np.abs(((c.xx - c.yy) / (7.0 * u)) % 1 - 0.5) < 0.03) & body
        rgb = np.where(arrow[..., None], np.array([226, 180, 60], np.float32), rgb)
        for h in hearts(c, rng, max(2, n // 2), 0.9, 1.3):
            m = h & body
            rgb = np.where(m[..., None], col((250, 120, 170)), rgb)
            glow_m |= m
    elif look == "roses":
        petals = np.abs(np.sin(np.hypot((c.xx % (5 * u)) - 2.5 * u, (c.yy % (5 * u)) - 2.5 * u) / (0.7 * u)
                               + np.arctan2((c.yy % (5 * u)) - 2.5 * u, (c.xx % (5 * u)) - 2.5 * u))) < 0.4
        rgb = np.where(petals[..., None], col((150, 10, 30)), col((206, 30, 50))) * lit
        leaves = leaf_mask(c, rng) & (c.hm < 0.5) & body
        rgb = np.where(leaves[..., None], np.array([50, 120, 50], np.float32) * lit, rgb)
    elif look == "candy_hearts":
        rgb = np.array([250, 248, 246], np.float32) * lit
        for i, h in enumerate(hearts(c, rng, n, 1.1, 1.7)):
            m = h & body
            rgb = np.where(m[..., None], np.asarray(PASTELS[i % len(PASTELS)], np.float32), rgb)
            glow_m |= m
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.shine(glow_m & body, col((255, 120, 170)), 0.35)
    c.extra["glow_m"] = glow_m & body
    return rgb


def animate(glow, frame, c):
    return np.where(c.extra["glow_m"], glow * [1.0, 0.6, 1.0, 0.75][frame % 4], glow)


def make(look):
    return _make(paint, look, animate, paint_layers=True)
