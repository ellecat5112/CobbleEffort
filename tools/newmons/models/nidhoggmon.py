"""Nidhoggmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the demon dragon gnawing at the world tree's roots: a long serpentine dragon of navy-black scales
spotted with glowing yellow, coiled in great loops, a narrow horned head with a fanged jaw, clawed forelimbs, and
four wings of blazing orange-and-yellow energy spread wide, smoke billowing about its coils. 35 blocks long.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, metal, scales, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a long serpentine demon dragon of navy-black scales spotted glowing yellow, coiled in loops, with a horned "
        "fanged head, clawed forelimbs and four wings of blazing orange energy")
BASE = {"navy": (40, 46, 80), "navy_dark": (14, 16, 34), "spot": (250, 210, 60), "red": (210, 50, 40),
        "claw": (220, 220, 230), "mouth": (130, 20, 30), "tooth": (250, 250, 240), "eye": (250, 220, 60),
        "wing": (255, 160, 50, 200), "wing_core": (255, 240, 140, 230), "smoke": (90, 90, 96, 140)}
SHINY = {"navy": (110, 40, 40), "navy_dark": (50, 10, 10), "wing": (110, 170, 255, 200), "wing_core": (220, 240, 255, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SC0 = scales(P, "navy", "navy_dark", size=1.4)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and math.sin(x * 1.3 + z * 0.9) * math.sin(y * 1.2 - z * 0.7) > 0.8:
        return p["spot"], p["spot"]
    return SC0(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["wing_core"] if u / max(W, 1e-6) < 0.35 else p["wing"]
    return c, c[:3]


def build():
    m = Model("nidhoggmon")
    top = m.bone("nidhoggmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    pts = []
    for i in range(30):                                                                  # great coils
        t = i / 29
        ang = t * 4.0 * math.pi
        r = 4.0 + 10.0 * t
        pts.append((r * math.cos(ang), 40.0 - 36.0 * t, r * math.sin(ang) + 2.0))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, max(2, 5 - j // 8), hidef, extend=0.7)
    h = pts[0]
    hd = m.bone("head", bd, h)
    hx, hy, hz = h[0], h[1] + 3.0, h[2] - 2.0
    m.round_box(hd, hx, hz - 4.0, 2.6, 6.0, hy - 1.0, hy + 2.6, hidef, cut=1)               # narrow head
    m.round_box(hd, hx, hz - 4.0, 2.2, 5.4, hy - 2.6, hy - 1.0, hidef, cut=0)
    m.box(hd, hx - 1.8, hy - 1.2, hz - 10.0, hx + 1.8, hy - 0.8, hz - 2.0, solid(P, "mouth"))
    for j in range(5):
        for sx in (-1, 1):
            spike(m, hd, (hx + sx * 1.8, hy - 0.8, hz - 9.4 + j * 1.4), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, hx + min(sx * 2.6, sx * 2.8), hy + 1.0, hz - 6.0, hx + max(sx * 2.6, sx * 2.8), hy + 1.8, hz - 4.6,
              solid(P, "eye", glow=True))
        spike(m, hd, (hx + sx * 1.6, hy + 2.6, hz), (sx * 0.4, 0.6, 1), 1.4, 7.0, solid(P, "navy_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # clawed forelimbs
        p = pts[4]
        ab = m.bone(nm, bd, p)
        rod(m, ab, p, (p[0] + sx * 7.0, p[1] - 4.0, p[2] - 4.0), 2, hidef, extend=0.4)
        for f in range(3):
            spike(m, ab, (p[0] + sx * 7.0, p[1] - 4.0, p[2] - 4.0), (sx * 0.3, -0.6, -1 + f * 0.4), 1.0, 3.6,
                  solid(P, "red"), tip=0.8)
    for sx in (-1, 1):                                                                   # four energy wings
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, pts[6])
        root = pts[6]
        for j, ang in enumerate((35, 5)):
            x0, x1 = sorted((root[0], root[0] + sx * 24.0))
            m.box(wb, x0, root[1] - 3.0, root[2] + 2.0 + j, x1, root[1] + 3.0, root[2] + 2.0 + j, wingf,
                  rotation=(0, 0, sx * ang), pivot=(root[0], root[1], root[2] + 2.0 + j))
    for i in range(6):                                                                   # billowing smoke
        ang = 2 * math.pi * i / 6
        ball(m, bd, (12.0 * math.cos(ang), 3.0, 12.0 * math.sin(ang) + 2.0), 3.0, solid(P, "smoke"), layers=2,
             ry=1.6)
    return m
