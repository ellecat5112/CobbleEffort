"""Pomumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a dragon-fruit lizard: a round magenta body of leafy scales each tipped green, a violet reptile
head with a green eye and a toothy grin, long green-and-pink striped leaf antennae curling back, a tufted tail of
fruit leaves and violet clawed feet with pink talons. 1 block.

Front is -z, y is up. 26 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import scales, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a dragon-fruit lizard: a round magenta body of green-tipped leafy scales, a violet reptile head, striped leaf antennae and pink talons"
BASE = {"pink": (230, 60, 130), "pink_dark": (150, 20, 70), "green": (90, 190, 70), "green_dark": (30, 110, 30),
        "violet": (120, 80, 170), "violet_dark": (60, 30, 100), "eye": (120, 220, 80), "pupil": (20, 30, 20),
        "mouth": (170, 30, 60), "tooth": (250, 250, 240), "talon": (240, 110, 160)}
SHINY = {"pink": (250, 200, 60), "pink_dark": (190, 130, 20), "violet": (60, 150, 160), "violet_dark": (20, 80, 90)}


def P(v):
    return pal(BASE, SHINY, v)


SCALE_P = scales(P, "pink", "pink_dark", size=1.8)
HEAD = skin(P, "violet", dark="violet_dark")


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green"] if (x + y + z) % 2.6 < 1.0 else p["pink"], face), None


def build():
    m = Model("pomumon")
    top = m.bone("pomumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 12.0, 1.0), 6.6, SCALE_P, layers=5, ry=6.4)
    for i in range(14):                                                                  # green-tipped leaf scales
        ang = 2 * math.pi * i / 14
        for yy in (10.0, 15.0):
            p0 = (6.0 * math.cos(ang), yy, 1.0 + 6.0 * math.sin(ang))
            if p0[2] < -3.0:
                continue
            spike(m, bd, p0, (math.cos(ang), 0.6, math.sin(ang) + 0.4), 1.6, 3.4, leaff, tip=0.8)
    hd = m.bone("head", bd, (0, 14, -4))
    m.round_box(hd, 0, -7.0, 3.6, 3.8, 12.6, 18.6, HEAD, cut=1)
    m.round_box(hd, 0, -11.0, 2.4, 2.0, 12.4, 15.6, HEAD, cut=1)                          # snout
    m.box(hd, -2.0, 12.6, -13.2, 2.0, 13.6, -8.0, solid(P, "mouth"))
    for j in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.8, 13.6, -12.6 + j * 1.2), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.6, sx * 3.8), 15.6, -9.0, max(sx * 3.6, sx * 3.8), 17.4, -7.2, solid(P, "eye"))
        pts = [(sx * 1.6, 18.4, -6.0), (sx * 3.0, 22.0, -2.0), (sx * 4.6, 23.0, 4.0), (sx * 5.0, 19.0, 8.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                  # striped leaf antennae
            rod(m, hd, p0, p1, 1, leaff, extend=0.2, t2=2)
    tl = m.bone("tail", bd, (0, 10, 7))
    for j in range(5):
        spike(m, tl, (0, 10.0, 7.0), ((j - 2) * 0.4, 0.2 + j * 0.1, 1), 1.6, 6.0, leaff, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 7.0, 0))
        rod(m, lg, (sx * 3.0, 7.0, 0.6), (sx * 3.4, 2.0, -0.6), 2, HEAD, extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 3.4 + (f - 1) * 1.0, 1.0, -1.0), ((f - 1) * 0.3, -0.4, -1), 0.8, 2.6,
                  solid(P, "talon"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 12.0, -3.0))
        rod(m, ab, (sx * 5.0, 12.0, -3.0), (sx * 6.6, 9.0, -6.0), 1, HEAD, extend=0.2, t2=2)
        for f in range(3):
            spike(m, ab, (sx * 6.6, 9.0, -6.0), ((f - 1) * 0.3, -1, -0.4), 0.8, 1.6, solid(P, "talon"), tip=0.8)
    return m
