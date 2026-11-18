"""Navimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the manga art on
wikimon.net): a cheerful little navigator: a girl-like figure with long teal hair under a big floppy pink jester's
cap with yellow bobbles, a winking face, a pink top under a black-and-white caped coat with a pink bow, and boots.
1 block tall.

Front is -z, y is up. 32 units tall; Child stage (no level on wikimon). Built covered (a full coat).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape
from _digidetail import fabric, skin, solid, strands
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1, HEIGHT, 1.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a cheerful little navigator with long teal hair under a floppy pink jester's cap, a winking face and a black-and-white caped coat"
BASE = {"skin": (250, 226, 200), "skin_dark": (210, 170, 140), "hair": (60, 170, 190), "hair_dark": (20, 100, 120),
        "pink": (240, 150, 170), "pink_dark": (190, 90, 110), "yellow": (250, 220, 60), "black": (30, 28, 34),
        "white": (246, 244, 240), "eye": (180, 70, 50), "mouth": (200, 60, 70)}
SHINY = {"hair": (230, 160, 60), "hair_dark": (170, 100, 20), "pink": (150, 200, 240), "pink_dark": (90, 140, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("navimon")
    top = m.bone("navimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0.2, 2.6, 2.0, 8.0, 17.0, fabric(P, "pink", "pink_dark"), cut=1)   # pink top
    for j in range(3):                                                                   # coat skirt
        r = 3.2 + j * 0.8
        m.round_box(bd, 0, 0.4, r, r * 0.8, 9.0 - (j + 1) * 1.6, 9.4 - j * 1.6, fabric(P, "black", "black"), cut=1)
    cape(m, bd, 17.0, 8.0, 12.0, fabric(P, "white", "black"), z=2.2, flare=0.8, panels=4, seed=2)
    m.box(bd, -1.2, 15.0, -2.4, 1.2, 16.4, -2.1, solid(P, "pink"))                         # bow
    hd = m.bone("head", bd, (0, 17, 0))
    ball(m, hd, (0, 21.0, -0.2), 3.6, skin(P, "skin", dark="skin_dark"), layers=4, ry=3.4)
    m.box(hd, 0.6, 21.4, -3.7, 1.8, 22.6, -3.55, solid(P, "eye"))                         # open eye
    m.box(hd, -1.8, 21.8, -3.7, -0.6, 22.2, -3.55, solid(P, "black"))                     # wink
    m.box(hd, -0.8, 19.4, -3.65, 0.8, 20.2, -3.5, solid(P, "mouth"))
    for i in range(9):                                                                   # long teal hair
        ang = math.radians(-80 + i * 20)
        rod(m, hd, (3.0 * math.sin(ang), 23.0, 0.6 + math.cos(ang)), (4.6 * math.sin(ang), 13.0, 2.0), 1,
            strands(P, "hair", "hair_dark"), extend=0.2, t2=2)
    m.round_box(hd, 0, 0, 4.6, 4.4, 23.4, 25.0, fabric(P, "pink", "pink_dark"), cut=1)     # floppy jester cap
    for sx in (-1, 1):
        pts = [(sx * 2.0, 25.0, 0), (sx * 6.0, 27.0, 0), (sx * 9.0, 25.0, 0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 3, fabric(P, "pink", "pink_dark"), extend=0.3)
        ball(m, hd, (sx * 9.6, 24.0, 0), 1.2, solid(P, "yellow"), layers=2)
    ball(m, hd, (0, 28.4, 1.0), 1.2, solid(P, "yellow"), layers=2)
    rod(m, hd, (0, 25.0, 0.4), (0, 27.6, 1.0), 2, fabric(P, "pink", "pink_dark"), extend=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.8, 16.0, 0))
        rod(m, ab, (sx * 2.8, 16.0, 0), (sx * 3.6, 11.0, -0.6), 1, fabric(P, "black", "black"), extend=0.2, t2=2)
        ball(m, ab, (sx * 3.6, 10.4, -0.8), 0.8, skin(P, "skin", dark="skin_dark"), layers=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.2, 6.0, 0))
        rod(m, lg, (sx * 1.2, 6.0, 0), (sx * 1.4, 1.0, 0), 1, skin(P, "skin", dark="skin_dark"), extend=0.2, t2=2)
        m.round_box(lg, sx * 1.4, -0.4, 1.0, 1.6, 0.0, 2.6, fabric(P, "black", "black"), cut=0)
    return m
