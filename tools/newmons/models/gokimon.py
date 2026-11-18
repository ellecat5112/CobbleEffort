"""Gokimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
cockroach: a big glossy brown roach crouching on six spiny legs, a grinning mandibled face with red eyes, long
whip-like antennae, a skull-and-crossbones mark on its flank and two pairs of tattered dark-red wings marked with a
white bone symbol. Adult stage, 15 blocks long.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import local, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a big glossy brown cockroach on six spiny legs with a grinning mandibled face, long antennae and tattered "
        "dark-red wings marked with a bone symbol")
BASE = {"brown": (110, 70, 40), "brown_dark": (50, 30, 14), "brown_light": (170, 120, 80), "wing": (140, 40, 50),
        "wing_dark": (80, 20, 24), "white": (240, 236, 220), "eye": (230, 40, 40), "tooth": (250, 250, 240),
        "mouth": (40, 14, 14)}
SHINY = {"brown": (60, 110, 60), "brown_dark": (20, 60, 20), "brown_light": (120, 180, 120), "wing": (60, 60, 140)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL0 = metal(P, "brown", dark="brown_dark", light="brown_light")


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z - 2.0, y - 10.0) < 1.4:
        return tone(p["white"], face), None
    return SHELL0(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u - W * 0.5) < 2.0 and abs(v - H * 0.5) < 0.5 or abs(v - H * 0.5) < 2.0 and abs(u - W * 0.5) < 0.5:
        return tone(p["white"], face), None
    return tone(p["wing"] if (u + v) % 3.0 > 0.4 else p["wing_dark"], face), None


def build():
    m = Model("gokimon")
    top = m.bone("gokimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for j, (r, z0) in enumerate(((5.0, -6.0), (6.0, -1.0), (5.6, 5.0), (4.4, 10.0))):     # segmented body
        m.round_box(bd, 0, z0, r, 2.6, 6.0, 6.0 + r * 1.2, shellf, cut=1)
    hd = m.bone("head", bd, (0, 10, -8))
    m.round_box(hd, 0, -10.0, 3.6, 2.6, 6.0, 12.0, shellf, cut=1)
    m.box(hd, -2.6, 7.0, -12.8, 2.6, 8.6, -12.5, solid(P, "mouth"))
    for j in range(5):
        spike(m, hd, (-2.2 + j * 1.1, 8.6, -12.6), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.6), 10.0, -12.7, max(sx * 1.0, sx * 2.6), 11.0, -12.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.6, 7.0, -12.0), (-sx * 0.4, -0.6, -1), 0.8, 2.6, SHELL0, tip=0.8)        # mandibles
        pts = [(sx * 1.6, 12.0, -10.0), (sx * 6.0, 20.0, -14.0), (sx * 10.0, 26.0, -10.0), (sx * 14.0, 28.0, -4.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                       # whip antennae
            rod(m, hd, p0, p1, 1, solid(P, "brown_dark"), extend=0.2, t2=1)
    for side in (1, -1):                                                                        # tattered wings
        for j in range(2):
            x0, x1 = sorted((side * 1.0, side * (14.0 - j * 3.0)))
            m.box(bd, x0, 13.0 + j, -4.0 + j * 2.0, x1, 13.4 + j, 14.0 + j * 2.0, wingf,
                  rotation=(-25 - j * 10, 0, side * (25 + j * 12)), pivot=(side * 1.0, 13.0, -4.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                          # six spiny legs
        lg = m.bone(nm, bd, (sx * 4.0, 8.0, 0))
        for j, z in enumerate((-5.0, 0.0, 6.0)):
            knee = (sx * 9.0, 10.0, z - 1.0)
            rod(m, lg, (sx * 4.0, 7.0, z), knee, 2, SHELL0, extend=0.4)
            rod(m, lg, knee, (sx * 11.0, 0.6, z + (j - 1) * 2.0), 1, SHELL0, extend=0.3, t2=2)
            spike(m, lg, knee, (sx * 0.4, 0.4, 0.6), 0.8, 2.0, SHELL0, tip=0.8)
    return m
