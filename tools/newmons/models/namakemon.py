"""Namakemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a lazy sloth puppet: a yellow shaggy body sewn with patches, a white-and-black panda-like face
with one red bloodshot eye and a tear, a tangle of green hair with long antennae, a huge lolling pink tongue, one long
arm wrapped in black straps ending in a grey sleeve, long green claws on its feet. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, leather, skin, solid, strands
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a lazy yellow sloth puppet with a panda-like face, one red eye, green hair and antennae, a huge lolling pink "
        "tongue, a long strapped arm and long green claws")
BASE = {"yellow": (240, 220, 60), "yellow_dark": (180, 150, 20), "white": (240, 240, 236), "black": (30, 30, 34),
        "green": (90, 200, 80), "green_dark": (30, 120, 30), "pink": (240, 150, 150), "pink_dark": (190, 90, 100),
        "grey": (130, 130, 140), "red": (220, 40, 40), "tear": (130, 200, 250)}
SHINY = {"yellow": (180, 140, 220), "yellow_dark": (110, 70, 160), "green": (240, 140, 60), "green_dark": (170, 80, 20)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "yellow", "yellow_dark", length=1.6)


def build():
    m = Model("namakemon")
    top = m.bone("namakemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 16.0, 0.6), 7.0, FUR, layers=5, ry=8.0)
    m.box(bd, -2.0, 15.0, -6.9, 2.0, 19.0, -6.6, solid(P, "green"))                       # sewn patch
    hd = m.bone("head", bd, (0, 23, 0))
    ball(m, hd, (0, 27.0, -0.6), 5.4, skin(P, "white", dark="grey"), layers=5, ry=4.8)
    m.round_box(hd, -2.0, -5.0, 1.8, 0.4, 26.0, 29.4, solid(P, "black"), cut=0)            # dark eye patch
    m.box(hd, 1.0, 27.0, -5.7, 3.0, 29.0, -5.5, solid(P, "white"))                        # red bloodshot eye
    m.box(hd, 1.6, 27.4, -5.75, 2.4, 28.6, -5.7, solid(P, "red"))
    m.box(hd, 1.6, 24.6, -5.6, 2.2, 26.8, -5.5, solid(P, "tear"))
    tg = [(0, 24.6, -5.6), (0.6, 20.0, -7.6), (1.6, 14.0, -8.0), (3.0, 10.0, -7.0)]
    for p0, p1 in zip(tg, tg[1:]):                                                       # huge lolling tongue
        rod(m, hd, p0, p1, 2, skin(P, "pink", dark="pink_dark"), extend=0.4, t2=3)
    for i in range(10):                                                                  # tangle of green hair
        ang = math.radians(-90 + i * 20)
        spike(m, hd, (4.0 * math.sin(ang), 30.0, 1.0 + math.cos(ang)), (math.sin(ang), 0.6, 0.4), 1.8, 5.0,
              strands(P, "green", "green_dark"), tip=0.8)
    for sx in (-1, 1):
        pts = [(sx * 1.0, 32.0, 0), (sx * 2.6, 38.0, 1.0), (sx * 5.0, 41.0, 3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "green"), extend=0.1)
    al = m.bone("arm_left", bd, (6.0, 20.0, 0))                                          # long strapped arm
    pts = [(6.0, 20.0, 0), (10.0, 28.0, 2.0), (8.0, 38.0, 4.0), (3.0, 42.0, 4.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, al, p0, p1, 3, leather(P, "black", "black") if j == 1 else FUR, extend=0.4)
    ball(m, al, (2.0, 42.0, 4.0), 2.0, solid(P, "grey"), layers=2)
    ar = m.bone("arm_right", bd, (-6.0, 17.0, 0))
    rod(m, ar, (-6.0, 17.0, 0), (-9.0, 11.0, -3.0), 3, FUR, extend=0.4)
    ball(m, ar, (-9.4, 10.0, -3.4), 1.8, solid(P, "white"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 9.0, 0))
        rod(m, lg, (sx * 3.6, 10.0, 0), (sx * 5.0, 2.0, -2.0), 3, FUR, extend=0.4)
        for f in range(3):
            spike(m, lg, (sx * 5.0 + (f - 1) * 1.0, 1.0, -3.0), (sx * 0.2, -0.3, -1), 1.0, 4.0, solid(P, "green"),
                  tip=0.8)
    return m
