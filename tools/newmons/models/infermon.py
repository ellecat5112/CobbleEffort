"""Infermon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
spider of the net: a round white shell-body with red markings and a crown of brass spikes, a small pale head with a
green eye and a fanged mouth slung beneath, and eight very long thin grey legs, each jointed with a red knuckle and
ending in a long golden point. 25 blocks wide.

Front is -z, y is up. 30 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 10.0)
KIND = "quadruped"
K = 3
LOOK = "a spider with a round white red-marked shell crowned with brass spikes, a small pale head and eight very long legs"
BASE = {"white": (240, 236, 236), "white_dark": (170, 160, 164), "red": (180, 30, 40), "red_dark": (100, 10, 20),
        "grey": (150, 154, 166), "grey_dark": (70, 72, 84), "gold": (240, 200, 90), "gold_dark": (160, 120, 30),
        "eye": (60, 200, 90), "mouth": (40, 20, 24), "tooth": (250, 250, 246)}
SHINY = {"white": (40, 40, 46), "white_dark": (12, 12, 16), "red": (60, 160, 230), "red_dark": (20, 80, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(math.atan2(z - 3.0, x) * 2.0)) > 0.75 and 14.0 < y < 21.0:
        return tone(p["red"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if math.hypot(x - 1.0, y - 16.6) < 0.8:
            return tone(p["eye"], face), p["eye"]
        if abs(y - 14.4) < 0.4 and abs(x) < 1.6:
            return tone(p["mouth"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("infermon")
    top = m.bone("infermon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 3))
    ball(m, bd, (0, 18.0, 3.0), 6.0, shellf, layers=5)
    for j in range(7):                                                              # crown of brass spikes
        ang = 2 * math.pi * j / 7
        spike(m, bd, (4.6 * math.cos(ang), 22.0, 3.0 + 4.6 * math.sin(ang)), (math.cos(ang) * 0.5, 1, math.sin(ang) * 0.5),
              1.2, 3.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 16, -4))
    m.round_box(hd, 0, -5.6, 2.6, 2.4, 13.4, 18.4, headf, cut=1)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.0, 13.6, -7.8), (sx * 0.2, -1, -0.3), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
    for i in range(8):                                                              # eight long legs
        sx = 1 if i < 4 else -1
        j = i % 4
        ang = math.radians(-50 + j * 34)
        nm = ("leg_front_left", "leg_back_left", "leg_mid_left", "leg_mid2_left",
              "leg_front_right", "leg_back_right", "leg_mid_right", "leg_mid2_right")[i]
        root = (sx * 4.0, 18.0, 3.0 + 4.0 * math.sin(ang))
        knee = (sx * 13.0, 26.0, 3.0 + 13.0 * math.sin(ang))
        foot = (sx * 21.0, 0.6, 3.0 + 21.0 * math.sin(ang))
        lg = m.bone(nm, bd, root)
        rod(m, lg, root, knee, 1, metal(P, "grey", dark="grey_dark"), extend=0.3, t2=1)
        m.round_box(lg, knee[0], knee[2], 1.0, 1.0, knee[1] - 1.0, knee[1] + 1.0, solid(P, "red"), cut=0)
        mid = (sx * 18.0, 10.0, 3.0 + 18.0 * math.sin(ang))
        rod(m, lg, knee, mid, 1, metal(P, "grey", dark="grey_dark"), extend=0.3, t2=1)
        m.round_box(lg, mid[0], mid[2], 1.0, 1.0, mid[1] - 1.0, mid[1] + 1.0, solid(P, "red"), cut=0)
        spike(m, lg, mid, (foot[0] - mid[0], foot[1] - mid[1], foot[2] - mid[2]), 1.0, 10.0,
              metal(P, "gold", dark="gold_dark"), tip=0.8)
    return m
