"""
Glacial collection: Pokemon in the grip of the deep cold (frost and glacier ice; the clear carved Ice Sculptures are #7).

Looks (one per line, three lines each):
  frostbite  its own colours frosted pale, white rime feathers creeping in from every edge and over the top
  glacier    deep blue banded glacier ice with dark crevasses and a snow cap on top
  permafrost frozen dark earth threaded with bands of pale ice lenses and speckled with hoarfrost
  aurora     pale, clear ice with the northern lights' greens and violets shimmering across it
  frozen_in  its own colours seen through a block of blue ice, with trapped bubbles and white cracks
  blizzard   crusted with drifts of snow, snowflakes and wind-blown streaks over frosted colours
Every look: icy glowing eyes and an emissive animated layer (FROST) where the ice glints and sparkles (the aurora
ripples).
Shiny: the ice's light turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import edges, even, hue_turn_fast, noise, ramp
from ._fx import make as _make

FROST = {"name": "frost", "emissive": True, "translucent": True, "frames": 4, "fps": 4}
WHITE = np.array([240, 248, 255], np.float32)


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def edge_dist(c, steps):
    """0 at the painted area's edge rising to 1 `steps` pixels in."""
    d = np.zeros((c.h, c.w), np.float32)
    cur = c.alpha.copy()
    for i in range(steps):
        e = edges(cur, 1)
        d = np.where(e, i / float(steps), d)
        cur = cur & ~e
    return np.where(cur, 1.0, d)


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 5 * u, rng, 2)
    fine = noise(c.h, c.w, max(1, u), rng, 1)
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    orig = c.a[..., :3]
    body = c.alpha & ~c.eye
    ice = np.zeros_like(c.alpha)
    if look == "frostbite":
        frost = np.clip(1.2 - edge_dist(c, 3 * u) + (c.hm - 0.6) * 2, 0, 1)
        rime = (fine + frost * 0.9 > 1.05) & body
        rgb = orig * 0.5 + col((196, 220, 244)) * 0.5
        rgb = rgb * (1 - 0.6 * frost[..., None]) + WHITE * 0.6 * frost[..., None]
        rgb = np.where(rime[..., None], WHITE, rgb)
        ice = rime
    elif look == "glacier":
        rgb = ramp(even([(8, 34, 80), (30, 96, 168), (110, 186, 232), (216, 242, 255)]),
                   c.lum * 0.35 + 0.35 + 0.25 * np.sin(c.hm * 40 + mottle * 6))
        crev = bolts(c, rng, max(2, int(_area(c) / 260)), 6, 1.2 * u, angle=np.pi / 2, jitter=0.5, branch=0.1) & body
        rgb = np.where(crev[..., None], col((6, 24, 60)), rgb)
        snow = (c.hm > 0.8 - 0.08 * mottle) & body
        rgb = np.where(snow[..., None], WHITE * (0.92 + 0.08 * mottle[..., None]), rgb)
        ice = body & ~crev
    elif look == "permafrost":
        rgb = ramp(even([(20, 16, 14), (50, 40, 34), (90, 76, 64), (130, 116, 102)]), c.lum * 0.5 + mottle * 0.4)
        lens = (np.abs(np.sin(c.hm * 34 + mottle * 4)) < 0.16) & body
        rgb = np.where(lens[..., None], col((168, 210, 236)) * (0.9 + 0.2 * fine[..., None]), rgb)
        hoar = (rng.random((c.h, c.w)) < 0.04) & body
        rgb = np.where(hoar[..., None], WHITE, rgb)
        ice = lens | hoar
    elif look == "aurora":
        rgb = ramp(even([(140, 170, 196), (200, 222, 238), (236, 246, 252), (252, 254, 255)]), c.lum * 0.45 + mottle * 0.4)
        band = 0.5 + 0.5 * np.sin(c.hm * 9 + c.xx / (12.0 * u) + mottle * 3)
        tint = band[..., None] * col((70, 255, 170)) + (1 - band[..., None]) * col((180, 110, 255))
        rgb = rgb * 0.75 + tint * 0.25
        c.extra["aurora"] = body
        ice = body
    elif look == "frozen_in":
        rgb = orig * 0.42 + col((110, 176, 236)) * 0.58
        bubbles = dilate((rng.random((c.h, c.w)) < 0.006) & body, max(0, u // 2)) & body
        rgb = np.where(bubbles[..., None], rgb * 0.5 + WHITE * 0.5, rgb)
        crack = bolts(c, rng, max(2, int(_area(c) / 240)), 8, 1.4 * u, jitter=0.7, branch=0.25) & body
        rgb = np.where(crack[..., None], WHITE, rgb)
        sheen = (np.abs(((c.xx + c.yy) / (7.0 * u)) % 1 - 0.5) < 0.05) & body           # glassy diagonal sheen
        rgb = np.where(sheen[..., None], rgb * 0.7 + WHITE * 0.3, rgb)
        ice = crack | bubbles | sheen
    elif look == "blizzard":
        snow = ((mottle + c.hm * 0.4 > 0.7) | (fine > 0.92)) & body
        rgb = orig * 0.55 + col((190, 210, 230)) * 0.45
        rgb = np.where(snow[..., None], WHITE * (0.9 + 0.1 * fine[..., None]), rgb)
        flake = np.zeros_like(c.alpha)
        ys, xs = np.nonzero(body)
        for _ in range(max(3, int(_area(c) / 60))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            fx, fy, r = xs[k], ys[k], max(1, u)
            flake |= ((np.abs(c.xx - fx) <= r) & (np.abs(c.yy - fy) < max(1, u * 0.4))) | \
                     ((np.abs(c.yy - fy) <= r) & (np.abs(c.xx - fx) < max(1, u * 0.4)))
        flake &= body
        streak = (np.abs(((c.xx - c.yy * 0.5) / (6.0 * u)) % 1 - 0.5) < 0.03) & (fine > 0.5) & body
        rgb = np.where(streak[..., None], rgb * 0.6 + WHITE * 0.4, rgb)
        rgb = np.where(flake[..., None], WHITE, rgb)
        ice = snow | flake
    else:
        rgb = orig
    eye = col((170, 240, 255))
    rgb = np.where(c.eye[..., None], eye, rgb)
    c.shine(c.eye, eye, 1.0)
    c.extra["ice"] = ice & body
    c.extra["col"] = col
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 6151 + frame * 977) % (2 ** 32))
    if "aurora" in c.extra:
        band = 0.5 + 0.5 * np.sin(c.hm * 9 + c.xx / (12.0 * c.u) - frame * np.pi / 2)
        m = c.extra["aurora"] & (band > 0.7)
        col = c.extra["col"]((80, 255, 180)) * band[..., None] + c.extra["col"]((190, 110, 255)) * (1 - band[..., None])
        g = np.where(m, 0.45 * band, g)
        grgb = np.where(m[..., None], col, grgb)
    spark = c.extra["ice"] & (rng.random(g.shape) < 0.03)
    g = np.where(spark, 0.85, g)
    grgb = np.where(spark[..., None], np.array([235, 250, 255], np.float32), grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, layer_alpha=190, paint_layers=True)
