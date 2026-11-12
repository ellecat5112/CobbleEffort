"""
Shadow collection: Pokemon whose hearts have been closed, wreathed in a dark aura (after the shadow Pokemon of
Colosseum and XD).

Looks (one per line, three lines each):
  aura     darkened to violet-black, a purple aura flickering up from every edge
  hyper    hyper mode: crimson-black with a raging red aura and burning red eyes
  eclipse  near black, every edge rimmed with a thin violet light
  smoke    smoky grey-black with dark wisps rising off it
  ember    charred dark with crimson cracks smouldering through
  cipher   dark violet broken up by glitching scanlines, as if the machine that made it still hums
Every look: an emissive animated layer (DARKAURA) where the aura burns.
Shiny: the aura's colour turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._arc import dilate
from ._cosmic import edges, hue_turn_fast, noise
from ._fx import make as _make
from ._void import voronoi_cracks

DARKAURA = {"name": "darkaura", "emissive": True, "translucent": True, "frames": 4, "fps": 6}


def darken(c, tint, k):
    return c.a[..., :3] * k + np.asarray(tint, np.float32) * (1 - k) * 0.35


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    rim = edges(c.alpha, max(1, u)) & body
    aura_c, eye_c, aura_mask = col((170, 60, 230)), None, None
    if look == "aura":
        rgb = darken(c, col((70, 20, 100)), 0.35)
        aura_mask = rim | ((c.hm > 0.8) & body)
    elif look == "hyper":
        rgb = darken(c, col((120, 10, 20)), 0.3)
        aura_c, eye_c = col((255, 40, 40)), col((255, 60, 40))
        aura_mask = dilate(rim, max(1, u // 2)) & body | ((c.hm > 0.72) & body)
    elif look == "eclipse":
        rgb = darken(c, (10, 6, 16), 0.15)
        aura_c = col((190, 120, 255))
        aura_mask = edges(c.alpha, 1) & body
        rgb = np.where(aura_mask[..., None], rgb * 0.6 + aura_c * 0.25, rgb)
    elif look == "smoke":
        rgb = darken(c, (40, 40, 46), 0.28) + 18
        wisp = np.abs(np.sin(c.xx / (2.5 * u) + noise(c.h, c.w, 4 * u, rng, 2) * 6)) < 0.2
        rgb = np.where((wisp & body)[..., None], rgb * 0.55, rgb)
        aura_c = col((120, 100, 150))
        c.extra["wisp_noise"] = noise(c.h, c.w, 3 * u, rng, 2)
        aura_mask = body & (c.hm > 0.55)
    elif look == "ember":
        rgb = darken(c, (30, 10, 10), 0.22)
        crack = voronoi_cracks(c, rng, 5 * u) & body
        rgb = np.where(crack[..., None], col((220, 40, 30)), rgb)
        aura_c = col((255, 60, 30))
        aura_mask = crack
    elif look == "cipher":
        rgb = darken(c, col((60, 20, 90)), 0.3)
        scan = ((c.yy // max(1, u)) % 3 == 0) & body
        rgb = np.where(scan[..., None], rgb * 0.6, rgb)
        rows = (rng.random(c.h) < 0.08)[:, None] & body                             # glitch rows, shifted
        shifted = np.roll(rgb, 3 * u, axis=1)
        rgb = np.where(rows[..., None], shifted * 0.7 + col((200, 40, 220)) * 0.3, rgb)
        aura_c = col((220, 60, 240))
        aura_mask = rows | (scan & (rng.random((c.h, c.w)) < 0.15))
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], (eye_c if eye_c is not None else c.a[..., :3]), rgb)
    if eye_c is not None:
        c.shine(c.eye, eye_c, 1.0)
    c.extra.update(aura=aura_mask if aura_mask is not None else np.zeros_like(c.alpha), aura_c=aura_c, look=look)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 7121 + frame * 499) % (2 ** 32))
    m = c.extra["aura"]
    if c.extra["look"] in ("aura", "hyper", "smoke"):                                # flames / wisps flicker upward
        fl = noise(c.h, c.w, max(1, c.u * 2), rng, 2)
        strength = np.clip(fl * 1.4 - 0.25, 0, 1) * (0.55 if c.extra["look"] == "smoke" else 0.85)
    else:
        strength = np.full(g.shape, [0.9, 0.7, 0.55, 0.75][frame % 4], np.float32)
        if c.extra["look"] == "eclipse":
            strength = strength * 0.45
    g = np.where(m, np.maximum(g, strength), g)
    grgb = np.where(m[..., None], c.extra["aura_c"], grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
