"""Mojyamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a shaggy snow-white yeti with a mop of icy fur over its eyes, a wide roaring red mouth full of
square teeth, a violet star mark on its brow, small round ears, and enormous bare tan hands and feet with pink nails,
one great fist raised high. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a shaggy snow-white yeti with icy fur over its eyes, a roaring red mouth, a violet star on its brow and enormous "
        "bare tan hands and feet")
BASE = {"fur": (236, 240, 250), "fur_dark": (160, 170, 200), "tan": (240, 190, 150), "tan_dark": (190, 130, 100),
        "nail": (250, 200, 210), "mouth": (180, 30, 40), "tooth": (250, 250, 240), "star": (130, 90, 200),
        "eye": (240, 200, 40), "ear": (150, 140, 180)}
SHINY = {"fur": (240, 200, 210), "fur_dark": (190, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", length=1.8, density=2.0)
TAN = skin(P, "tan", dark="tan_dark")


def hand(m, bone, c, sx, up=False):
    ball(m, bone, c, 3.4, TAN, layers=3, squash=0.8)
    for f in range(4):
        d = (sx * 0.2, 1 if up else -1, -0.4)
        p0 = (c[0] + (f - 1.5) * 1.6, c[1] + (3.0 if up else -3.0), c[2] - 1.0)
        p1 = (p0[0], p0[1] + (2.6 if up else -2.6), p0[2] - 0.8)
        rod(m, bone, p0, p1, 2, TAN, extend=0.3)
        m.box(bone, p1[0] - 0.6, p1[1] - 0.5, p1[2] - 1.1, p1[0] + 0.6, p1[1] + 0.5, p1[2] - 0.9, solid(P, "nail"))


def build():
    m = Model("mojyamon")
    top = m.bone("mojyamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    ball(m, bd, (0, 22.0, 0.6), 8.0, FUR, layers=6, ry=9.0, squash=0.85)                  # shaggy body
    for i in range(10):
        ang = math.radians(-90 + i * 20)
        spike(m, bd, (8.0 * math.sin(ang), 18.0, -6.6 * math.cos(ang)), (math.sin(ang) * 0.4, -1, -math.cos(ang) * 0.4),
              2.0, 4.0, FUR, tip=0.8)
    hd = m.bone("head", bd, (0, 30, 0))
    ball(m, hd, (0, 34.0, -1.0), 5.6, FUR, layers=5, ry=5.0, squash=0.9)
    m.round_box(hd, 0, -6.0, 3.6, 0.8, 30.4, 34.0, solid(P, "mouth"), cut=1)              # roaring mouth
    for j in range(5):
        m.box(hd, -3.0 + j * 1.3, 33.0, -6.9, -2.2 + j * 1.3, 34.0, -6.7, solid(P, "tooth"))
        m.box(hd, -3.0 + j * 1.3, 30.4, -6.9, -2.2 + j * 1.3, 31.2, -6.7, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, sx * 2.0 - 0.6, 35.4, -6.0, sx * 2.0 + 0.6, 36.0, -5.8, solid(P, "eye"))
        ball(m, hd, (sx * 4.6, 37.6, 0), 1.4, solid(P, "ear"), layers=2, squash=0.5)
    for i in range(7):                                                                   # mop of icy fur
        spike(m, hd, ((i - 3) * 1.4, 39.0, -3.0), ((i - 3) * 0.2, 0.3, -1), 1.6, 4.0, FUR, tip=0.8)
    m.box(hd, -0.9, 38.2, -6.6, 0.9, 40.0, -6.4, solid(P, "star"))
    al = m.bone("arm_left", bd, (7.0, 26.0, 0))                                          # raised fist
    rod(m, al, (7.0, 26.0, 0), (11.0, 36.0, -2.0), 4, FUR, extend=0.6)
    hand(m, al, (12.0, 41.0, -2.6), 1, up=True)
    ar = m.bone("arm_right", bd, (-7.0, 25.0, 0))
    rod(m, ar, (-7.0, 25.0, 0), (-11.0, 17.0, -3.0), 4, FUR, extend=0.6)
    hand(m, ar, (-12.0, 12.0, -4.0), -1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 14.0, 0))
        rod(m, lg, (sx * 4.0, 15.0, 0), (sx * 4.6, 5.0, 0), 5, FUR, extend=0.6)
        m.round_box(lg, sx * 4.8, -2.0, 3.0, 4.6, 0.0, 3.0, TAN, cut=1)                 # big bare feet
        for f in range(4):
            m.box(lg, sx * 4.8 + (f - 1.5) * 1.4 - 0.5, 0.0, -6.8, sx * 4.8 + (f - 1.5) * 1.4 + 0.5, 1.2, -6.4,
                  solid(P, "nail"))
    return m
