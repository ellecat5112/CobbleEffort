"""Atamadekachimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): an "unbalanced" dinosaur that is almost all head. A huge glossy red head with a wide
jagged-toothed grin, a lolling pink tongue, one big blue eye on each side and round ears, perched on a tiny red body
with a cream belly, stubby arms and legs and a thin curling tail. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, local, mix, plane, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 20}
LOOK = ("an almost-all-head dinosaur: a huge glossy red head with a jagged-toothed grin and pink tongue, big blue eyes, "
        "round ears, a tiny red body with a cream belly and a thin curling tail")
BASE = {"red": (220, 40, 50), "red_dark": (130, 14, 24), "red_light": (255, 140, 140), "cream": (250, 236, 220),
        "cream_dark": (210, 190, 170), "tongue": (240, 110, 150), "tongue_dark": (190, 60, 100), "mouth": (110, 20, 40),
        "tooth": (250, 250, 250), "eye": (90, 160, 230), "pupil": (16, 16, 24), "white": (250, 250, 250),
        "claw": (200, 210, 230)}
SHINY = {"red": (60, 170, 90), "red_dark": (20, 100, 40), "red_light": (160, 240, 170), "tongue": (240, 200, 110),
         "tongue_dark": (190, 140, 50)}


def P(v):
    return pal(BASE, SHINY, v)


def glossy(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    g = math.sin(a * 0.35 + b * 0.25)
    base = skin(P, "red", dark="red_dark", light="red_light", var=0.02)(x, y, z, face, variant, box=box, **k)[0]
    if g > 0.94:
        return mix(base, p["red_light"], 0.6), None
    return base, None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 6.0, y - 36.0, 2.4, "eye", lid="red_dark")
        if c is not None:
            return c, None
    return glossy(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("atamadekachimon")
    top = m.bone("atamadekachimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 10.0, 1.0), 5.0, glossy, layers=5, ry=6.0)
    m.box(bd, -3.2, 5.0, -4.6, 3.2, 14.0, -3.4, skin(P, "cream", dark="cream_dark"))       # cream belly
    hd = m.bone("head", bd, (0, 16, 0))
    ball(m, hd, (0, 34.0, 0.0), 13.0, headf, layers=8, squash=1.05, ry=10.0)             # the huge head (upper jaw)
    m.box(hd, -10.0, 22.0, -15.0, 10.0, 30.0, 4.0, glossy)                               # lower head mass
    m.box(hd, -9.0, 26.0, -15.6, 9.0, 30.4, -8.0, solid(P, "mouth"))                     # the grin
    for i in range(8):                                           # jagged teeth top and bottom
        x = -8.0 + i * 2.3
        spike(m, hd, (x, 30.2, -15.0), (0, -1, 0), 1.6, 2.6, solid(P, "tooth"))
        spike(m, hd, (x + 1.1, 26.2, -15.0), (0, 1, 0), 1.4, 2.0, solid(P, "tooth"))
    m.box(hd, -3.0, 22.0, -18.0, 3.0, 27.0, -10.0, skin(P, "tongue", dark="tongue_dark"),
          rotation=(20, 0, 0), pivot=(0, 27.0, -10.0))                                    # lolling tongue
    for sx in (-1, 1):                                           # round ears
        ball(m, hd, (sx * 8.0, 44.0, 4.0), 3.0, glossy, layers=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 13.0, -1.0))
        rod(m, ab, (sx * 4.0, 13.0, -1.0), (sx * 6.0, 11.0, -4.0), 2, glossy, extend=0.3)
        spike(m, ab, (sx * 6.0, 11.0, -4.0), (0, -0.3, -1), 1.0, 1.2, solid(P, "claw"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 6.0, 1.0))
        rod(m, lg, (sx * 3.0, 6.0, 1.0), (sx * 3.4, 1.0, 0.0), 3, glossy, extend=0.3)
        m.box(lg, sx * 3.4 - 1.8, 0.0, -3.4, sx * 3.4 + 1.8, 1.6, 1.0, glossy)
    tl = m.bone("tail", bd, (0, 7, 5))
    pts = [(0, 7, 5), (2, 6, 10), (6, 7, 14), (9, 11, 15), (9, 14, 13)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, glossy, extend=0.3)
    return m
