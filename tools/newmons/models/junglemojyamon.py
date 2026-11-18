"""Jungle Mojyamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the jungle yeti: a shaggy orange-brown ape-beast with a great mane of fur round a scowling face with red eyes and
fangs, a dark star tuft on its brow, huge tan hands with pink nails, big tan feet with spiral soles and a short
fluffy tail. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a shaggy orange-brown jungle yeti with a great mane round a fanged face, huge tan hands and big tan feet"
BASE = {"fur": (200, 110, 40), "fur_dark": (120, 60, 14), "fur_light": (240, 170, 90), "tan": (230, 190, 140),
        "tan_dark": (180, 130, 90), "nail": (250, 190, 200), "eye": (220, 40, 30), "mouth": (160, 30, 30),
        "tooth": (250, 250, 246), "dark": (90, 40, 10)}
SHINY = {"fur": (120, 140, 70), "fur_dark": (60, 80, 24), "fur_light": (180, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=2.0)
TAN = skin(P, "tan", dark="tan_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.0) < 0.7 and abs(y - 25.0) < 0.4:
                return tone(p["eye"], face), None
        if 19.6 < y < 22.6 and abs(x) < 2.6 - abs(y - 21.0) * 0.6:
            if y > 21.8 and abs(abs(x) - 1.6) < 0.4:
                return tone(p["tooth"], face), None
            return tone(p["mouth"], face), None
        if math.hypot(x, y - 27.6) < 0.8:
            return tone(p["dark"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("junglemojyamon")
    top = m.bone("junglemojyamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 18.0, 0.6), 9.0, FUR, layers=6, squash=1.1)
    hd = m.bone("head", bd, (0, 24, -3))
    m.round_box(hd, 0, -4.0, 4.6, 4.0, 18.0, 30.0, facef, cut=2)
    for i in range(14):                                                              # great mane
        ang = 2 * math.pi * i / 14
        spike(m, hd, (5.0 * math.cos(ang), 24.0 + 5.4 * math.sin(ang), -3.0), (math.cos(ang), math.sin(ang), 0.3), 2.4,
              4.0, FUR, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # huge hands
        ab = m.bone(nm, bd, (sx * 8.0, 22.0, 0))
        rod(m, ab, (sx * 8.0, 22.0, 0), (sx * 13.0, 17.0, -4.0), 3, FUR, extend=0.6)
        m.round_box(ab, sx * 14.4, -6.0, 3.6, 3.0, 12.0, 18.0, TAN, cut=1)
        for j in range(4):
            m.round_box(ab, sx * 14.4 + (j - 1.5) * 1.6, -9.4, 0.7, 0.6, 15.4, 18.6, TAN, cut=0)
            m.round_box(ab, sx * 14.4 + (j - 1.5) * 1.6, -10.0, 0.6, 0.2, 17.6, 18.6, solid(P, "nail"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # big feet
        lg = m.bone(nm, top, (sx * 4.0, 9.0, 0))
        rod(m, lg, (sx * 4.0, 10.0, 0), (sx * 4.6, 4.0, -1.0), 3, FUR, extend=0.6)
        m.round_box(lg, sx * 4.8, -2.6, 3.2, 4.6, 0.0, 3.4, TAN, cut=1)
        for j in range(4):
            m.round_box(lg, sx * 4.8 + (j - 1.5) * 1.5, -7.6, 0.6, 0.6, 0.0, 1.6, solid(P, "nail"), cut=0)
    tb = m.bone("tail", bd, (0, 12, 8))
    ball(m, tb, (0, 12.0, 9.4), 2.4, FUR, layers=3)
    return m
