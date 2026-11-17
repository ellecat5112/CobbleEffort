"""Dogmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
puppet dog. A floppy orange plush hound with a round body stamped with a big black "D", a goofy grin with a lolling
red tongue and little fangs, bulging googly eyes, long navy ears, stubby paws with black pads and white claws held
up in a pounce, and a navy tail. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a floppy orange plush hound with a big black D on its belly, a goofy grin and lolling tongue, googly eyes, long "
        "navy ears and stubby black-padded paws")
BASE = {"orange": (250, 170, 40), "orange_dark": (200, 100, 10), "navy": (40, 40, 120), "navy_dark": (14, 14, 60),
        "black": (24, 22, 24), "red": (220, 40, 50), "tongue": (240, 80, 90), "white": (250, 250, 250),
        "eye": (90, 160, 60), "pupil": (16, 16, 16)}
SHINY = {"orange": (170, 210, 250), "orange_dark": (90, 130, 200), "navy": (160, 40, 70), "navy_dark": (80, 10, 30)}


def P(v):
    return pal(BASE, SHINY, v)


PLUSH = fur(P, "orange", "orange_dark", length=0.8, density=3.0)
NAVY = fabric(P, "navy", "navy_dark", axis="y")


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 10.0 < y < 18.0:                                    # the big "D"
        u, v = x + 1.0, y - 14.0
        if (abs(u + 2.0) < 0.6 and abs(v) < 3.4) or (abs(math.hypot(u + 2.0, v) - 3.2) < 0.6 and u > -2.0):
            return tone(p["black"], face), None
    return PLUSH(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, y - 31.0)
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.5:
                return tone(p["white"], face), None
            if d < 1.7:
                return tone(p["eye"], face), None
    return PLUSH(x, y, z, face, variant, box=box, **k)


def pawf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "down"):
        return tone(p["black"], face), None
    return PLUSH(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dogmon")
    top = m.bone("dogmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 15.0, 0), 8.0, bellyf, layers=7, squash=0.9)                      # round plush body
    hd = m.bone("head", bd, (0, 24, -2))
    m.round_box(hd, 0, -1.0, 5.4, 4.6, 23.0, 33.0, headf, cut=2)
    m.round_box(hd, 0, -6.6, 3.4, 2.0, 24.0, 28.0, PLUSH, cut=1)                      # muzzle
    m.round_box(hd, 0, -8.6, 1.2, 0.8, 27.0, 28.6, solid(P, "black"), cut=0)          # nose
    m.box(hd, -3.0, 23.0, -8.6, 3.0, 24.6, -5.0, solid(P, "red"))                     # open mouth
    m.box(hd, -0.6, 19.0, -8.8, 2.6, 23.6, -8.0, solid(P, "tongue"), rotation=(-10, 0, -10), pivot=(1.0, 23.6, -8.4))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 24.6, -7.6), (0, -1, 0), 0.8, 1.6, solid(P, "white"))     # little fangs
        pts = [(sx * 4.6, 32.0, 0), (sx * 7.0, 38.0, 2.0), (sx * 9.0, 40.0, 4.0)]
        for p0, p1 in zip(pts, pts[1:]):                                               # long navy ears
            rod(m, hd, p0, p1, 2, NAVY, extend=0.5, t2=4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                               # paws up in a pounce
        ab = m.bone(nm, bd, (sx * 7.0, 18.0, -2.0))
        rod(m, ab, (sx * 7.0, 18.0, -2.0), (sx * 12.0, 28.0, -4.0), 3, PLUSH, extend=0.6)
        m.round_box(ab, sx * 13.0, -4.0, 3.0, 2.0, 28.0, 34.0, pawf, cut=1)
        for j in range(3):
            spike(m, ab, (sx * 13.0 + (j - 1) * 1.6, 34.0, -4.0), ((j - 1) * 0.3, 1, -0.3), 0.8, 2.0,
                  solid(P, "white"), tip=0.25)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 8.0, 0))
        rod(m, lg, (sx * 4.0, 9.0, 0), (sx * 5.0, 3.0, -2.0), 3, PLUSH, extend=0.6)
        m.round_box(lg, sx * 5.0, -3.0, 3.0, 3.6, 0.0, 4.0, pawf, cut=1)
    tl = m.bone("tail", bd, (0, 10, 7))
    for p0, p1 in zip([(0, 10.0, 7.0), (2.0, 13.0, 12.0)], [(2.0, 13.0, 12.0), (6.0, 14.0, 15.0)]):
        rod(m, tl, p0, p1, 2, NAVY, extend=0.5)
    return m
