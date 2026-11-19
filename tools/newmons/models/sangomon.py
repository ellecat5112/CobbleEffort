"""Sangomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a coral-reef blob: a pink coral head branching into a crown of stubby coral horns, big yellow eyes, a
grinning fanged mouth, a little clownfish hiding in its branches, and a round blue body with two long blue arms
ending in star-shaped flowers. 1 block.

Front is -z, y is up. 24 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a pink coral-headed blob with a crown of coral horns, big yellow eyes, a clownfish in its branches and long blue star-flower arms"
BASE = {"pink": (240, 80, 150), "pink_dark": (170, 30, 90), "blue": (80, 180, 230), "blue_dark": (30, 110, 170),
        "eye": (250, 200, 40), "black": (24, 20, 24), "white": (255, 255, 255), "mouth": (100, 30, 60),
        "orange": (250, 130, 40), "flower": (240, 60, 110)}
SHINY = {"pink": (250, 160, 60), "pink_dark": (190, 100, 20), "blue": (140, 220, 120), "blue_dark": (70, 160, 60)}


def P(v):
    return pal(BASE, SHINY, v)


CORAL = skin(P, "pink", dark="pink_dark", var=0.04)
BLUE = skin(P, "blue", dark="blue_dark", var=0.02)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 14.0)
            if d < 0.5:
                return tone(p["black"], face), None
            if d < 1.3:
                return tone(p["eye"], face), None
        if 10.6 < y < 11.8 and abs(x) < 3.0:
            return tone(p["mouth"], face), None
    return CORAL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("sangomon")
    top = m.bone("sangomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 6.0, 0), 5.0, BLUE, layers=4, ry=4.0)
    hd = m.bone("head", bd, (0, 10, 0))
    ball(m, hd, (0, 13.0, -0.4), 5.0, headf, layers=4, ry=4.2)
    for j in range(4):
        spike(m, hd, (-2.4 + j * 1.6, 10.6, -4.4), (0, -1, 0), 0.8, 1.0, solid(P, "white"), tip=0.8)
    for j in range(7):                                                                   # coral crown
        ang = math.radians(-70 + j * 23)
        p0 = (3.6 * math.sin(ang), 16.0, 0.6)
        p1 = (p0[0] + 2.0 * math.sin(ang), 22.0 + (j % 2), 0.6 + (j % 3) * 0.6)
        rod(m, hd, p0, p1, 2, CORAL, extend=0.3)
        rod(m, hd, p1, (p1[0] + 1.6 * math.sin(ang + 0.8), p1[1] + 1.6, p1[2]), 1, CORAL, extend=0.2, t2=2)
    ball(m, hd, (3.4, 19.0, 1.0), 1.0, solid(P, "orange"), layers=1)                         # clownfish
    m.box(hd, 3.0, 18.4, 0.4, 3.8, 19.6, 0.6, solid(P, "white"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # long star-flower arms
        ab = m.bone(nm, bd, (sx * 4.0, 6.0, 0))
        pts = [(sx * 4.0, 6.0, 0), (sx * 9.0, 4.0, -1.0), (sx * 13.0, 6.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, BLUE, extend=0.4)
        for j in range(5):
            ang = 2 * math.pi * j / 5
            spike(m, ab, (sx * 14.0, 6.0, -1.0), (math.cos(ang) * 0.4 * sx, math.sin(ang), -0.6), 1.4, 2.6, BLUE, tip=0.8)
        m.box(ab, sx * 14.0 - 0.6, 5.4, -2.0, sx * 14.0 + 0.6, 6.6, -1.6, solid(P, "flower"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 3.0, 0))
        m.round_box(lg, sx * 2.6, -0.4, 1.8, 2.2, 0.0, 3.0, BLUE, cut=0)
    return m
