"""
St. Patrick's Day collection: Pokemon with the luck of the Irish.

Looks (one per line, three lines each):
  shamrock     emerald green scattered with three-leaf shamrocks, lucky sparkles twinkling
  leprechaun   a green coat with a black belt and gold buckle, orange-brown britches, a gold hat band up top
  pot_of_gold  heaped gold coins over a black iron pot; the gold glints
  rainbow      bands of rainbow from the feet up, white clouds at the bottom
  celtic       deep green worked with gold Celtic knotwork
  tartan       an Irish green tartan with white and orange stripes
The eyes keep their own colours. Emissive layer (LUCK) for the glints and sparkles.
Shiny: the green turned to gold.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

LUCK = {"name": "luck", "emissive": True, "translucent": True, "frames": 4, "fps": 4}
GOLD = np.array([240, 196, 60], np.float32)


def cloth(c, colour, k=0.5):
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None])


def shamrock(c, x, y, R):
    m = np.zeros_like(c.alpha)
    for a in (-np.pi / 2, np.pi / 6, 5 * np.pi / 6):
        lx, ly = x + np.cos(a) * R * 0.55, y + np.sin(a) * R * 0.55
        m |= np.hypot(c.xx - lx, c.yy - ly) <= R * 0.5
    stem = (np.abs(c.xx - x - (c.yy - y) * 0.3) <= max(0.5, R * 0.12)) & (c.yy >= y) & (c.yy <= y + R * 1.2)
    return m | stem


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    green = (lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], -0.2)[0, 0]) if c.shiny else (lambda rgb: np.array(rgb, np.float32))
    mottle = noise(c.h, c.w, 5 * u, rng, 2)
    glow_m = np.zeros_like(c.alpha)
    if look == "shamrock":
        rgb = cloth(c, green((40, 150, 70)))
        ys, xs = np.nonzero(body)
        for i in range(max(3, int(c.alpha.sum() / float(u * u) / 80))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            m = shamrock(c, xs[k], ys[k], max(2.5, rng.uniform(1.6, 2.6) * u)) & body
            rgb = np.where(m[..., None], cloth(c, green((120, 220, 110) if i % 2 else (20, 100, 40))), rgb)
        glow_m = (rng.random((c.h, c.w)) < 0.01) & body
    elif look == "leprechaun":
        rgb = np.where((c.hm > 0.38)[..., None], cloth(c, green((30, 120, 50))), cloth(c, (150, 90, 50)))
        belt = (np.abs(c.hm - 0.42) < 0.03) & body
        rgb = np.where(belt[..., None], np.array([20, 18, 18], np.float32), rgb)
        if c.face.torso:
            x, y, w, h = c.face.torso
            buckle = belt & (np.abs(c.xx - (x + w / 2)) <= max(1.0, 1.2 * u))
            rgb = np.where(buckle[..., None], GOLD, rgb)
            glow_m |= buckle
        hat = (np.abs(c.hm - 0.9) < 0.02) & body
        rgb = np.where(hat[..., None], GOLD, rgb)
        glow_m |= hat
    elif look == "pot_of_gold":
        pot = (c.hm < 0.45) & body
        g = 3 * u
        lx, ly = (c.xx % g) - g / 2, (c.yy % g) - g / 2
        coin = np.hypot(lx, ly) <= g * 0.45
        rgb = np.where(coin[..., None], GOLD * (0.8 + 0.3 * c.lum[..., None]), GOLD * 0.55)
        rim = (np.abs(np.hypot(lx, ly) - g * 0.38) < max(0.4, 0.25 * u))
        rgb = np.where(rim[..., None], GOLD * 0.7, rgb)
        rgb = np.where(pot[..., None], cloth(c, (30, 30, 34), 0.6), rgb)
        glow_m = coin & ~pot & body & (rng.random((c.h, c.w)) < 0.15)
    elif look == "rainbow":
        bands = [(230, 40, 40), (250, 140, 30), (250, 220, 40), (60, 180, 70), (50, 110, 220), (130, 60, 190)]
        idx = np.clip(((c.hm - 0.15) / 0.85 * len(bands)).astype(int), 0, len(bands) - 1)
        rgb = np.asarray(bands, np.float32)[idx] * (0.75 + 0.35 * c.lum[..., None])
        cloud = (c.hm < 0.15 + 0.06 * mottle) & body
        rgb = np.where(cloud[..., None], np.array([248, 250, 255], np.float32) * (0.85 + 0.15 * c.lum[..., None]), rgb)
        glow_m = (rng.random((c.h, c.w)) < 0.01) & body & ~cloud
    elif look == "celtic":
        rgb = cloth(c, green((20, 90, 46)))
        s = 3.0 * u
        a = np.abs(np.sin((c.xx + c.yy) * np.pi / s))
        b = np.abs(np.sin((c.xx - c.yy) * np.pi / s))
        over = ((c.xx // s + c.yy // s) % 2) == 0
        knot = ((a < 0.25) & (over | (b > 0.35))) | ((b < 0.25) & (~over | (a > 0.35)))
        knot &= body
        rgb = np.where(knot[..., None], GOLD * (0.8 + 0.3 * c.lum[..., None]), rgb)
    elif look == "tartan":
        base = cloth(c, green((24, 110, 50)))
        va = ((c.xx // (2 * u)) % 4 == 0)
        hb = ((c.yy // (2 * u)) % 4 == 0)
        rgb = np.where((va | hb)[..., None], base * 0.6, base)
        rgb = np.where((va & hb)[..., None], base * 0.4, rgb)
        white = ((c.xx % (8 * u)) == 2 * u) | ((c.yy % (8 * u)) == 2 * u)
        orange = ((c.xx % (8 * u)) == 6 * u) | ((c.yy % (8 * u)) == 6 * u)
        rgb = np.where(white[..., None], cloth(c, (240, 240, 236)), rgb)
        rgb = np.where(orange[..., None], cloth(c, (240, 140, 40)), rgb)
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra["glow_m"] = glow_m & body
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    rng = np.random.default_rng((c.seed * 811 + frame * 29) % (2 ** 32))
    m = c.extra["glow_m"] & (rng.random(glow.shape) < 0.6)
    c.glow_rgb = np.where(m[..., None], np.array([255, 236, 150], np.float32), rgb0)
    return np.where(m, 0.85, g0)


def make(look):
    return _make(paint, look, animate, paint_layers=True)
