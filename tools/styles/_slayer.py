"""
Slayer collection: Pokemon as demon slayers, each in a patterned haori over a dark uniform, with a breathing style
(inspired by the Demon Slayer anime; the patterns are traditional Japanese motifs).

Looks (one per line, three lines each):
  checkered  ichimatsu: a green-and-black checked haori, with the sun's fire flickering at the hem
  water      seigaiha: blue-and-white wave scales; flowing water glows along them
  flame      a white haori with flames licking up from the hem; the flames flicker
  thunder    uroko: a yellow haori of white triangle scales; lightning crackles across it
  insect     a butterfly-wing haori, lilac fading to violet with black veins and glowing spots
  mist       pale mist-white fading to sky cyan, with mist drifting over it
Every look: the haori over the upper body, a dark navy uniform below with a white belt; the breathing style glows in an
emissive animated layer (BREATH). The eyes keep their own colours.
Shiny: the haori's colours turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._arc import bolts, dilate
from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

BREATH = {"name": "breath", "emissive": True, "translucent": True, "frames": 4, "fps": 6}
HEM = 0.38


def cloth(c, colour, k=0.45):
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None])


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    haori = (c.hm >= HEM) & body
    breath = np.zeros_like(c.alpha)
    bcol = col((255, 255, 255))
    if look == "checkered":
        g = 3 * u
        chk = ((c.xx // g + c.yy // g) % 2) == 0
        pat = np.where(chk[..., None], cloth(c, col((36, 130, 84))), cloth(c, (22, 22, 26)))
        hem = (c.hm >= HEM) & (c.hm < HEM + 0.12) & body
        breath = hem & (noise(c.h, c.w, max(1, u), rng, 1) > 0.5)
        bcol = col((255, 120, 40))
    elif look == "water":
        cell = 4 * u
        row = c.yy // cell
        off = (row % 2) * cell / 2
        lx = ((c.xx + off) % cell) - cell / 2
        ly = (c.yy % cell) - cell                                                     # arcs rise from the cell's foot
        r = np.hypot(lx, ly)
        ring = ((r // max(1, u)) % 2) == 0
        pat = np.where(ring[..., None], cloth(c, col((40, 90, 190))), cloth(c, (236, 244, 252)))
        breath = (np.abs((r / max(1, u)) % 2 - 1) < 0.25) & haori
        bcol = col((120, 210, 255))
        c.extra["water_r"] = r
    elif look == "flame":
        pat = cloth(c, (244, 236, 222))
        tongue = (c.hm < HEM + 0.12 + 0.18 * noise(c.h, c.w, 2 * u, rng, 2)) & haori
        heat = np.clip((HEM + 0.3 - c.hm) / 0.3, 0, 1)[..., None]
        pat = np.where(tongue[..., None], col((255, 210, 60)) * (1 - heat) + col((220, 40, 20)) * heat, pat)
        breath = tongue
        bcol = col((255, 140, 30))
    elif look == "thunder":
        g = 3 * u
        lx, ly = c.xx % g, c.yy % g
        tri = ly >= np.abs(lx - g / 2) * 2
        grad = ramp(even([col((250, 200, 40)), col((240, 140, 30))]), 1 - c.hm)
        pat = np.where(tri[..., None], cloth(c, (250, 248, 236)), grad * (0.75 + 0.35 * c.lum[..., None]))
        c.extra["bolts"] = True
        bcol = col((255, 240, 120))
    elif look == "insect":
        t = np.clip((c.hm - HEM) / (1 - HEM), 0, 1)[..., None]
        pat = cloth(c, col((220, 190, 250))) * (1 - t) + cloth(c, col((110, 50, 170))) * t
        vein = bolts(c, rng, max(3, int(c.alpha.sum() / float(u * u) / 150)), 10, 1.5 * u, jitter=0.4, branch=0.3) & haori
        pat = np.where(vein[..., None], np.array([20, 14, 26], np.float32), pat)
        spots = (rng.random((c.h, c.w)) < 0.01) & haori
        spots = dilate(spots, max(0, u // 2)) & haori
        pat = np.where(spots[..., None], np.array([250, 246, 255], np.float32), pat)
        breath = spots
        bcol = col((230, 190, 255))
    elif look == "mist":
        t = np.clip((c.hm - HEM) / (1 - HEM), 0, 1)[..., None]
        pat = cloth(c, (240, 246, 250)) * (1 - t) + cloth(c, col((130, 210, 230))) * t
        c.extra["mist"] = noise(c.h, c.w, 5 * u, rng, 2)
        bcol = col((220, 245, 255))
    else:
        pat = c.a[..., :3]
    uniform = cloth(c, (20, 24, 40), 0.6)
    rgb = np.where(haori[..., None], pat, uniform)
    belt = (np.abs(c.hm - (HEM - 0.03)) < 0.015) & body
    rgb = np.where(belt[..., None], np.array([236, 236, 230], np.float32), rgb)
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra.update(breath=breath & body, bcol=bcol, haori=haori)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 5471 + frame * 389) % (2 ** 32))
    m = c.extra["breath"].copy()
    s = 0.7
    if "water_r" in c.extra:                                                         # the waves roll outward
        r = c.extra["water_r"]
        m = (np.abs(((r / max(1, c.u)) - frame * 0.5) % 2 - 1) < 0.25) & c.extra["haori"]
    elif "bolts" in c.extra:
        m = bolts(c, rng, max(1, int(c.alpha.sum() / float(c.u * c.u) / 300)), 8, 1.5 * c.u, jitter=0.8, branch=0.2) \
            & c.extra["haori"]
        s = 1.0
    elif "mist" in c.extra:
        drift = np.roll(c.extra["mist"], frame * c.u, axis=1)
        m = (drift > 0.6) & c.extra["haori"]
        s = 0.35
    else:
        flick = noise(c.h, c.w, max(1, c.u * 2), rng, 1)
        g = np.where(m, s * (0.5 + 0.5 * flick), g)
        grgb = np.where(m[..., None], c.extra["bcol"], grgb)
        c.glow_rgb = grgb
        return g
    g = np.where(m, s, g)
    grgb = np.where(m[..., None], c.extra["bcol"], grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
