"""Pipismon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the vampire bat of the night: a small fierce navy bat with a white furry chest, huge pointed
ears, a gaping fanged mouth unleashing rings of sonar, great red-and-navy bat wings, steel rings round its ears and
limbs, and curled clawed feet. 15 blocks wide.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a small fierce navy bat with a white furry chest, huge pointed ears, a fanged mouth unleashing sonar rings and great red bat wings"
BASE = {"navy": (40, 50, 110), "navy_dark": (14, 18, 50), "white": (240, 240, 236), "white_dark": (180, 180, 176),
        "red": (210, 40, 40), "red_dark": (120, 14, 14), "steel": (200, 204, 216), "mouth": (180, 40, 60),
        "tooth": (250, 250, 240), "sonar": (255, 240, 120, 170), "pink": (240, 160, 180)}
SHINY = {"navy": (140, 60, 140), "navy_dark": (70, 20, 70), "red": (240, 190, 60), "red_dark": (170, 120, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("pipismon")
    top = m.bone("pipismon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 16.0, 0.6), 4.6, skin(P, "navy", dark="navy_dark"), layers=4, ry=5.4)
    ball(m, bd, (0, 15.0, -2.6), 3.2, fur(P, "white", "white_dark"), layers=3, ry=4.0, squash=0.5)
    hd = m.bone("head", bd, (0, 21, 0))
    ball(m, hd, (0, 23.4, -0.6), 3.6, skin(P, "navy", dark="navy_dark"), layers=4, ry=3.2)
    m.round_box(hd, 0, -4.0, 2.4, 0.8, 21.4, 23.6, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.4, 23.6, -4.2), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
        spike(m, hd, (sx * 2.4, 25.6, 0), (sx * 0.4, 1, 0.2), 2.6, 7.0, skin(P, "navy", dark="navy_dark"), tip=0.8)  # ears
        m.round_box(hd, sx * 3.0, 0, 1.4, 1.4, 27.0, 27.6, metal(P, "steel"), cut=0)
    for j in range(3):                                                                   # sonar rings
        r = 2.0 + j * 1.6
        for i in range(10):
            ang = 2 * math.pi * i / 10
            m.box(hd, r * math.cos(ang) - 0.4, 22.4 + r * math.sin(ang) - 0.4, -6.0 - j * 3.0, r * math.cos(ang) + 0.4,
                  22.4 + r * math.sin(ang) + 0.4, -5.6 - j * 3.0, solid(P, "sonar", glow=True))
    wb = m.bone("wings", bd, (0, 18, 2))
    for side in (1, -1):
        bat_wing(m, wb, (side * 3.0, 18.0, 2.0), 22.0, 18.0, 4, solid(P, "navy"), skin(P, "red", dark="red_dark"),
                 side=side, sweep=15)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.0, 12.0, 0))
        rod(m, lg, (sx * 2.0, 12.0, 0), (sx * 3.0, 6.0, 1.0), 1, skin(P, "navy", dark="navy_dark"), extend=0.2, t2=2)
        m.round_box(lg, sx * 2.6, 0.6, 1.2, 1.2, 8.0, 8.6, metal(P, "steel"), cut=0)
        for f in range(2):
            pts = [(sx * 3.0, 6.0, 1.0), (sx * (4.0 + f), 4.0, 0), (sx * (3.6 + f), 3.0, -1.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, lg, p0, p1, 1, solid(P, "navy_dark"), extend=0.1)
    return m
