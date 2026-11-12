"""
Nimbus collection: Pokemon made of sky and cloud.

Looks (one per line, three lines each):
  cumulus        a bright blue sky with fluffy white cumulus clouds billowing over it
  storm          a dark thunderhead with slanting rain and lightning that strikes in the dark
  sunset         clouds lit gold, pink and violet by a setting sun, their edges glowing
  rain           grey rain clouds over the top, raindrops falling down the body
  silver_lining  dark slate clouds whose every edge shines silver
  dream          cloud nine: pastel lavender and pink clouds with tiny twinkling stars
Every look: soft glowing eyes and an emissive animated layer (SKY).
Shiny: the sky turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import edges, even, hue_turn_fast, noise, ramp
from ._fx import make as _make

SKY = {"name": "sky", "emissive": True, "translucent": True, "frames": 4, "fps": 4}
WHITE = np.array([250, 252, 255], np.float32)


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def clouds(c, rng, cover, smooth=False):
    """Billowy cloud mask (about `cover` of the area), its puffiness 0..1 and its rim."""
    if smooth:
        n = noise(c.h, c.w, 10 * c.u, rng, 2)
    else:
        n = noise(c.h, c.w, 7 * c.u, rng, 3) * 0.7 + noise(c.h, c.w, 2 * c.u, rng, 1) * 0.3
    t = np.quantile(n[c.alpha], 1 - cover) if c.alpha.any() else 0.5
    m = (n > t) & c.alpha
    puff = np.clip((n - t) / 0.15, 0, 1)
    rim = edges(m, max(1, c.u // 2)) & m & ~edges(c.alpha, max(1, c.u // 2))     # cloud edges, not face borders
    return m, puff, rim


def paint(look, c):
    rng, u = c.rng, c.u
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    body = c.alpha & ~c.eye
    lit = (0.75 + 0.35 * c.lum)[..., None]
    if look == "cumulus":
        sky = ramp([(0, col((80, 140, 220))), (1, col((170, 214, 252)))], c.hm)
        m, puff, rim = clouds(c, rng, 0.55)
        cloud = WHITE * (0.8 + 0.2 * puff[..., None]) * np.clip(lit, 0, 1.05)
        rgb = np.where(m[..., None], cloud, sky * lit)
        rgb = np.where((rim & m)[..., None], rgb * 0.9, rgb)
        eye = col((255, 255, 255))
    elif look == "storm":
        m, puff, rim = clouds(c, rng, 0.75)
        rgb = ramp(even([(26, 28, 38), (60, 64, 80), (110, 116, 134)]), c.lum * 0.4 + puff * 0.5)
        rainline = (np.abs(((c.xx + c.yy * 0.35) / (2.5 * u)) % 1 - 0.5) < 0.06) & (c.hm < 0.6) & body
        rgb = np.where(rainline[..., None], rgb * 0.6 + col((150, 170, 210)) * 0.4, rgb)
        c.extra["bolt"] = col((255, 250, 200))
        eye = col((255, 245, 180))
    elif look == "sunset":
        m, puff, rim = clouds(c, rng, 0.6)
        grad = ramp([(0, col((90, 50, 130))), (0.45, col((240, 110, 140))), (1, col((255, 196, 90)))], c.hm)
        sky = ramp([(0, col((40, 30, 80))), (1, col((240, 130, 90)))], c.hm)
        rgb = np.where(m[..., None], grad * (0.85 + 0.25 * puff[..., None]), sky * lit)
        c.shine(rim, col((255, 210, 120)), 0.7)
        rgb = np.where(rim[..., None], col((255, 220, 140)), rgb)
        eye = col((255, 220, 150))
    elif look == "rain":
        top = c.hm > 0.55
        m, puff, rim = clouds(c, rng, 0.85)
        rgb = np.where(top[..., None], ramp(even([(80, 88, 104), (140, 148, 162), (196, 202, 212)]), puff * 0.7 + c.lum * 0.3),
                       ramp(even([(50, 70, 100), (90, 120, 160)]), c.lum * 0.6 + 0.2))
        c.extra["rain"] = body & ~top
        eye = col((200, 230, 255))
    elif look == "silver_lining":
        m, puff, rim = clouds(c, rng, 0.6, smooth=True)
        rgb = ramp(even([(18, 22, 32), (44, 52, 70), (80, 90, 110)]), c.lum * 0.5 + puff * 0.3)
        lining = rim & body
        rgb = np.where(lining[..., None], col((236, 242, 255)), rgb)
        c.shine(lining, col((220, 232, 255)), 0.9)
        c.extra["lining"] = lining
        eye = col((230, 240, 255))
    elif look == "dream":
        m, puff, rim = clouds(c, rng, 0.6)
        rgb = np.where(m[..., None], ramp([(0, col((236, 200, 240))), (1, col((255, 240, 252)))], puff),
                       ramp([(0, col((150, 130, 220))), (1, col((200, 180, 250)))], c.hm) * lit)
        stars = (rng.random((c.h, c.w)) < 0.012) & body & ~m
        rgb = np.where(stars[..., None], WHITE, rgb)
        c.shine(stars, (255, 250, 220), 0.9)
        c.extra["stars"] = stars
        eye = col((255, 230, 255))
    else:
        rgb, eye = c.a[..., :3], np.array([255, 255, 255], np.float32)
    rgb = np.where(c.eye[..., None], eye, rgb)
    c.shine(c.eye, eye, 0.8)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 3301 + frame * 211) % (2 ** 32))
    u = c.u
    if "bolt" in c.extra and frame in (0, 2):                                       # lightning now and then
        b = bolts(c, rng, max(1, int(_area(c) / 400)), 12, 2.0 * u, angle=np.pi / 2, jitter=0.8, branch=0.2)
        b = b & ~c.eye
        g = np.where(b, 1.0, g)
        grgb = np.where(b[..., None], c.extra["bolt"], grgb)
    if "rain" in c.extra:                                                           # drops falling
        drop = (((c.yy - frame * u) % (4 * u)) < u) & ((c.xx % (3 * u)) == 0) & c.extra["rain"]
        g = np.where(drop, 0.6, g)
        grgb = np.where(drop[..., None], np.array([170, 210, 255], np.float32), grgb)
    if "stars" in c.extra:
        g = np.where(c.extra["stars"], g0 * (rng.random(g.shape) < 0.6), g)
    if "lining" in c.extra:
        g = np.where(c.extra["lining"], g0 * [1.0, 0.8, 0.65, 0.8][frame % 4], g)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
