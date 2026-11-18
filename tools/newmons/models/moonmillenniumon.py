"""Moon Millenniumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the wicked god sealed in time: a tall six-sided crystal of pale blue-violet, its facets
catching the light, with the dark shadow of a coiled dragon trapped inside, its eyes burning orange and a pale glow at
its heart, floating above its own shadow. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a tall six-sided blue-violet crystal with the dark shadow of a coiled dragon trapped inside, its eyes burning orange"
BASE = {"crystal": (190, 200, 250, 120), "crystal_light": (240, 244, 255, 160), "edge": (150, 160, 230),
        "shadow": (40, 40, 80), "shadow_dark": (16, 16, 40), "eye": (250, 140, 40), "core": (240, 220, 255)}
SHINY = {"crystal": (250, 200, 210, 120), "crystal_light": (255, 240, 244, 160), "edge": (230, 150, 170),
         "shadow": (80, 30, 50), "shadow_dark": (40, 10, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def crystalf(x, y, z, face, variant, box=None, **k):
    """Translucent crystal with bright facet edges and a diagonal sheen."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if u < 0.3 or u > W - 0.3:
        return tone(p["edge"], face), None
    c = p["crystal_light"] if 0.4 < (u / max(W, 1e-6) + v / max(H, 1e-6) * 0.3) % 1.0 < 0.55 else p["crystal"]
    return c, None


def shadowf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["shadow"] if (y * 0.7) % 2.0 < 1.4 else p["shadow_dark"], face), None


def build():
    m = Model("moonmillenniumon")
    top = m.bone("moonmillenniumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    sb = m.bone("shadow", bd, (0, 30, 0))                                                # the dragon inside
    pts = []
    for i in range(14):
        t = i / 13
        ang = t * 2.6 * math.pi
        pts.append((3.0 * math.cos(ang), 46.0 - 32.0 * t, 2.0 * math.sin(ang)))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, sb, p0, p1, max(1, 4 - j // 4), shadowf, extend=0.4)
    h = pts[0]
    m.round_box(sb, h[0], h[2] - 2.0, 2.0, 3.0, h[1] - 1.0, h[1] + 2.0, shadowf, cut=1)
    for sx in (-1, 1):
        m.box(sb, h[0] + sx * 1.0 - 0.4, h[1] + 0.6, h[2] - 5.1, h[0] + sx * 1.0 + 0.4, h[1] + 1.2, h[2] - 4.9,
              solid(P, "eye", glow=True))
        spike(m, sb, (h[0] + sx * 1.2, h[1] + 2.0, h[2]), (sx * 0.5, 1, 0.4), 1.0, 3.0, shadowf, tip=0.8)
    ball(m, sb, (1.0, 32.0, -1.0), 1.4, solid(P, "core", glow=True), layers=2)
    for i in range(12):                                                                  # six-sided crystal
        y0 = 10.0 + i * 4.0
        t = (y0 + 2.0 - 30.0) / 22.0
        r = 8.0 * max(0.25, min(1.0, 1.6 * (1 - abs(t)) + 0.15))
        for j in range(6):
            ang = math.radians(j * 60 + 30)
            cx, cz = r * 0.87 * math.cos(ang), r * 0.87 * math.sin(ang)
            w = r * 0.5
            m.box(bd, cx - w, y0, cz - 0.3, cx + w, y0 + 4.0, cz + 0.3, crystalf,
                  rotation=(0, -(j * 60 + 30) + 90, 0), pivot=(cx, y0, cz))
    m.round_box(top, 0, 0, 4.0, 4.0, 0.0, 0.4, solid(P, "shadow_dark"), cut=1)          # its shadow below
    return m
