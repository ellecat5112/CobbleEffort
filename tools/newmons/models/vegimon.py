"""Vegimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a carnivorous plant: a bulbous yellow-green head veined with dark green, a huge fanged mouth with a
pale tongue, a crown of red petals fading to blue at the tips, a long whip of a vine body ending in a coiled yellow
tail, and thin curling tendrils for arms. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a carnivorous plant with a bulbous yellow-green head, a huge fanged mouth, a crown of red petals and a long vine body"
BASE = {"yellow": (220, 230, 80), "yellow_dark": (140, 170, 30), "vein": (60, 110, 30), "red": (230, 60, 40),
        "blue": (60, 120, 220), "mouth": (120, 20, 40), "tooth": (250, 250, 240), "tongue": (240, 200, 180),
        "eye": (30, 30, 20)}
SHINY = {"yellow": (240, 160, 200), "yellow_dark": (180, 90, 140), "red": (90, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(x * 1.1 + y * 0.6) * math.cos(z * 0.9 - y * 0.4)) < 0.12:
        return tone(p["vein"], face), None
    return skin(P, "yellow", dark="yellow_dark")(x, y, z, face, variant, box=box, **k)


def petalf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["blue"] if y > 33.0 else p["red"]
    return tone(c, face), None


def build():
    m = Model("vegimon")
    top = m.bone("vegimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    pts = [(-6.0, 2.0, 0), (-2.0, 1.0, 2.0), (2.0, 3.0, 3.0), (3.0, 8.0, 2.0), (1.0, 14.0, 0.0), (0, 18.0, 0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 2, skin(P, "yellow", dark="yellow_dark"), extend=0.5)
    for i in range(8):                                                                 # coiled tail
        ang = i * 0.8
        r = 2.6 - i * 0.25
        q0 = (-6.0 - r * math.cos(ang), 2.0 + r * math.sin(ang), 0)
        q1 = (-6.0 - (r - 0.25) * math.cos(ang + 0.8), 2.0 + (r - 0.25) * math.sin(ang + 0.8), 0)
        rod(m, bd, q0, q1, 1, skin(P, "yellow", dark="yellow_dark"), extend=0.2)
    hd = m.bone("head", bd, (0, 24, 0))
    ball(m, hd, (0, 25.0, 0.6), 6.4, headf, layers=5)
    m.box(hd, -4.4, 19.6, -7.0, 4.4, 24.0, -3.0, solid(P, "mouth"))                       # gaping mouth
    m.box(hd, -2.0, 19.8, -7.2, 2.0, 20.8, -4.0, solid(P, "tongue"))
    for j in range(7):
        x = -3.8 + j * 1.27
        spike(m, hd, (x, 24.0, -6.4), (0, -1, 0), 0.9, 2.4, solid(P, "tooth"), tip=0.8)
        spike(m, hd, (x, 19.6, -6.4), (0, 1, 0), 0.9, 1.8, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 3.0), 27.6, -5.8, max(sx * 1.6, sx * 3.0), 28.4, -5.4, solid(P, "eye"))
    for j in range(9):                                                                 # petal crown
        ang = (j - 4) * 0.36
        spike(m, hd, (math.sin(ang) * 3.4, 30.0, 1.0), (math.sin(ang) * 1.2, 1, 0.3), 2.0, 7.0, petalf, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # curling tendrils
        ab = m.bone(nm, bd, (sx * 1.0, 16.0, 0))
        pts = [(sx * 1.0, 16.0, 0), (sx * 6.0, 18.0, -1.0), (sx * 9.0, 14.0, -1.0), (sx * 8.0, 11.0, 0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, solid(P, "vein"), extend=0.2)
    return m
