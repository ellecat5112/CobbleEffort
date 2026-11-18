"""Marin Devimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the deep-sea devil: a lean dark navy devil body with a fanged face and red eyes, wrapped in long pale-blue-and-white
squid tentacles curling up into hooks with red-ringed suckers, bands of gold rings on its arms, and long clawed
fingers. 25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a lean dark navy devil wrapped in long pale-blue squid tentacles curling into hooks, with a fanged face, red eyes and gold arm rings"
BASE = {"navy": (40, 50, 110), "navy_dark": (14, 18, 50), "pale": (220, 232, 246), "pale_dark": (140, 160, 200),
        "red": (210, 40, 50), "gold": (230, 180, 60), "gold_dark": (150, 110, 20), "eye": (240, 40, 40),
        "black": (24, 24, 30), "tooth": (250, 248, 236)}
SHINY = {"navy": (110, 30, 50), "navy_dark": (50, 10, 20)}


def P(v):
    return pal(BASE, SHINY, v)


DARK = skin(P, "navy", dark="navy_dark")


def tentf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and (y % 3.0) < 0.6:
        return tone(p["red"], face), None
    return skin(P, "pale", dark="pale_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("marindevimon")
    top = m.bone("marindevimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    m.round_box(bd, 0, 0.6, 4.0, 3.0, 26.0, 42.0, DARK, cut=1)
    hd = m.bone("head", bd, (0, 42, -1))
    m.round_box(hd, 0, -1.0, 3.0, 3.4, 41.6, 48.6, DARK, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 46.0, -4.5, max(sx * 0.8, sx * 2.2), 46.8, -4.3, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.0, 43.0, -4.4), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
    for i in range(6):                                                               # squid tentacles
        ang = math.radians(-150 + i * 60)
        up = 1 if i in (1, 4) else -1
        pts = [(3.0 * math.cos(ang), 40.0 if up > 0 else 28.0, 2.0 + 2.0 * math.sin(ang)),
               (12.0 * math.cos(ang), 46.0 if up > 0 else 16.0, 4.0 + 4.0 * math.sin(ang)),
               (14.0 * math.cos(ang), 56.0 if up > 0 else 4.0, 2.0),
               (10.0 * math.cos(ang), 58.0 if up > 0 else 0.6, -2.0)]
        tb = m.bone("tentacle_%d" % i, bd, pts[0])
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tb, p0, p1, 2 - j // 2, tentf, extend=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 40.0, 0))
        rod(m, ab, (sx * 4.0, 40.0, 0), (sx * 8.0, 30.0, -3.0), 1, DARK, extend=0.3, t2=2)
        for j in range(3):
            m.round_box(ab, sx * (5.4 + j * 0.9), -1.0 - j * 0.6, 1.2, 1.2, 36.0 - j * 2.4, 36.8 - j * 2.4,
                        metal(P, "gold", dark="gold_dark"), cut=0)
        for j in range(4):
            spike(m, ab, (sx * 8.0 + (j - 1.5) * 0.8, 29.4, -3.4), (0, -1, -0.3), 0.8, 4.0, solid(P, "black"), tip=0.8)
    return m
