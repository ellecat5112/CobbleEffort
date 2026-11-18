"""Fujitsumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the anime appearance shown on
wikimon.net): a little shellfish Digimon. A squat, lumpy brown blob like a clam's foot with three dark round eyes set
in a triangle, a wide dark mouth and a pale ridged shell rim at its base. Child stage, 1 block tall.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a squat lumpy brown blob with three dark round eyes set in a triangle, a wide dark mouth and a pale shell rim"
BASE = {"brown": (150, 120, 90), "brown_dark": (100, 76, 50), "eye": (24, 20, 18), "eye_ring": (90, 70, 50),
        "shine": (220, 220, 200), "mouth": (30, 24, 24), "shell": (230, 220, 200), "shell_dark": (170, 160, 140)}
SHINY = {"brown": (220, 150, 170), "brown_dark": (170, 100, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "brown", dark="brown_dark")
EYES = ((0.0, 17.0), (-2.6, 13.0), (2.6, 13.6))


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for ex, ey in EYES:
            d = math.hypot(x - ex, y - ey)
            if d < 0.3:
                return tone(p["shine"], face), None
            if d < 0.9:
                return tone(p["eye"], face), None
            if d < 1.3:
                return tone(p["eye_ring"], face), None
        if 7.0 < y < 9.6 and abs(x) < 3.6 - (9.6 - y) * 0.6:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (math.atan2(z, x) * 4.0) % 1.0 < 0.25:
        return tone(p["shell_dark"], face), None
    return tone(p["shell"], face), None


def build():
    m = Model("fujitsumon")
    top = m.bone("fujitsumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 7.4, 6.0, 0.0, 3.0, shellf, cut=2)                          # shell rim
    ball(m, bd, (0, 11.0, 0), 6.6, bodyf, layers=5, ry=9.0)
    hd = m.bone("head", bd, (0, 18, 0))
    ball(m, hd, (1.4, 19.0, 1.0), 3.0, SKIN, layers=3)                                  # lumpy top
    return m
