"""Ornismon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ancient bird: a vast long-necked bird of violet and sky-blue plumage, a sharp-beaked head with a
pink crest, enormous wings whose feathers shade from violet to hot pink at the tips, taloned feet and a long trailing
tail of pink plumes. 35 blocks wide.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = ("a vast long-necked ancient bird of violet and sky-blue plumage with a pink-crested sharp-beaked head, enormous "
        "violet-to-pink wings and a long tail of pink plumes")
BASE = {"violet": (120, 90, 190), "violet_dark": (60, 40, 120), "blue": (90, 190, 230), "blue_dark": (30, 110, 170),
        "pink": (240, 110, 180), "pink_dark": (170, 50, 110), "beak": (230, 200, 160), "eye": (240, 60, 60),
        "claw": (230, 230, 236)}
SHINY = {"violet": (230, 170, 60), "violet_dark": (160, 100, 20), "blue": (230, 90, 70), "blue_dark": (150, 40, 30)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = feathers(P, "violet", "violet_dark")
NECK = feathers(P, "blue", "blue_dark")
WING = feathers(P, "violet", "violet_dark", tip="pink")


def build():
    m = Model("ornismon")
    top = m.bone("ornismon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 24, 0))
    ball(m, bd, (0, 26.0, 2.0), 7.0, BODY, layers=5, ry=6.0, squash=1.4)
    nk = m.bone("neck", bd, (0, 30, -6))
    pts = [(0, 30.0, -6.0), (0, 36.0, -10.0), (0, 40.0, -14.0), (0, 40.0, -18.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, nk, p0, p1, 3, NECK, extend=0.6)
    hd = m.bone("head", nk, pts[-1])
    h = pts[-1]
    m.round_box(hd, h[0], h[2] - 1.0, 2.2, 3.0, h[1] - 1.6, h[1] + 2.0, NECK, cut=1)
    spike(m, hd, (h[0], h[1] - 0.2, h[2] - 4.0), (0, -0.3, -1), 1.6, 5.0, solid(P, "beak"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, h[0] + min(sx * 2.2, sx * 2.4), h[1] + 0.4, h[2] - 2.6, h[0] + max(sx * 2.2, sx * 2.4), h[1] + 1.2,
              h[2] - 1.4, solid(P, "eye", glow=True))
    for j in range(4):
        spike(m, hd, (h[0], h[1] + 2.0, h[2] + j * 0.6), (0, 0.6, 1), 1.0, 5.0 - j * 0.6, solid(P, "pink"), tip=0.8)
    for side in (1, -1):                                                                 # enormous wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 30.0, 0))
        feather_wing(m, wb, (side * 5.0, 30.0, 0), 34.0, 18.0, 8, WING, side=side, sweep=20, droop=-8.0)
    for i in range(5):                                                                   # long tail plumes
        ang = math.radians(-30 + i * 15)
        rod(m, bd, (0, 24.0, 9.0), (10.0 * math.sin(ang), 18.0 - i, 30.0), 1, feathers(P, "pink", "pink_dark"),
            extend=0.2, t2=3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 3.0, 20.0, 2.0))
        rod(m, lg, (sx * 3.0, 20.0, 2.0), (sx * 3.4, 12.0, 0), 2, solid(P, "beak"), extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 3.4, 12.0, 0), ((f - 1) * 0.5, -0.6, -1), 1.0, 3.0, solid(P, "claw"), tip=0.8)
    return m
