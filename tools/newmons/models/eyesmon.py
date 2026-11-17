"""Eyesmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the many-eyed shadow dragon. A long, writhing serpent-dragon made of jagged black shadow, its whole
body studded with staring red eyes, a long crocodile head with a jagged maw of white teeth and a purple tongue, a crown
of tall blade-spines each holding an eye, clawed shadow arms and a ragged tail fraying into wisps of black smoke.
15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "floater"
K = 3
LOOK = ("a long writhing serpent-dragon of jagged black shadow studded with staring red eyes, a crocodile head with a "
        "jagged white-toothed maw, a crown of eyed blade-spines and a tail fraying into smoke")
BASE = {"black": (26, 24, 30), "black_light": (70, 66, 80), "eye": (240, 240, 240), "pupil": (220, 30, 40),
        "tooth": (250, 248, 240), "mouth": (40, 10, 30), "tongue": (130, 60, 170), "smoke": (60, 60, 66, 170)}
SHINY = {"black": (220, 220, 230), "black_light": (255, 255, 255), "pupil": (60, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def shadowf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a = (x * 0.9 + y * 0.6) % 4.6 - 2.3
    b = (z * 0.9 - y * 0.4) % 4.6 - 2.3
    if face != "down":
        r = math.hypot(a, b * 1.6)
        if r < 0.45:
            return p["pupil"], p["pupil"]
        if r < 0.9:
            return tone(p["eye"], face), None                           # staring eyes all over
    return tone(p["black_light"] if face == "up" else p["black"], face), None


def build():
    m = Model("eyesmon")
    top = m.bone("eyesmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    pts = [(0, 30.0, -6.0), (2.0, 26.0, 0.0), (5.0, 20.0, 5.0), (3.0, 13.0, 10.0), (-2.0, 9.0, 15.0),
           (-6.0, 7.0, 21.0), (-8.0, 6.0, 27.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # writhing serpent body
        rod(m, bd, p0, p1, max(2, 6 - j), shadowf, extend=0.8)
        spike(m, bd, p0, (0.3 * (-1) ** j, 1, 0.3), 1.6, 4.0 - j * 0.4, shadowf, tip=0.4)
    for j in range(4):                                                               # smoke wisps
        m.round_box(bd, -9.0 - j * 1.6, 28.0 + j * 2.0, 1.4 + j * 0.4, 1.4 + j * 0.4, 5.0 + j, 7.4 + j,
                    solid(P, "smoke"), cut=0)
    hd = m.bone("head", bd, (0, 32, -8))
    m.round_box(hd, 0, -12.0, 3.4, 6.0, 30.0, 35.0, shadowf, cut=1)                   # long crocodile head
    m.box(hd, -3.0, 28.0, -22.0, 3.0, 30.0, -10.0, shadowf)                           # lower jaw
    m.box(hd, -2.6, 29.6, -21.6, 2.6, 30.4, -10.0, solid(P, "mouth"))
    m.box(hd, -1.0, 29.0, -24.0, 1.0, 29.8, -18.0, solid(P, "tongue"))
    for j in range(8):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.6, 30.4, -21.0 + j * 1.4), (0, 1, 0), 0.7, 1.4, solid(P, "tooth"))
            spike(m, hd, (sx * 2.6, 30.2, -21.0 + j * 1.4), (0, -1, 0), 0.7, 1.4, solid(P, "tooth"))
    for i in range(6):                                                               # crown of eyed blade-spines
        sx = -1 if i % 2 else 1
        spike(m, hd, (sx * 2.0, 35.0, -10.0 + (i // 2) * 3.0), (sx * 0.4, 1, 0.8), 2.0, 8.0 - (i // 2), shadowf, tip=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # clawed shadow arms
        ab = m.bone(nm, bd, (sx * 4.0, 24.0, -2.0))
        rod(m, ab, (sx * 4.0, 24.0, -2.0), (sx * 10.0, 18.0, -6.0), 2, shadowf, extend=0.4)
        rod(m, ab, (sx * 10.0, 18.0, -6.0), (sx * 12.0, 12.0, -8.0), 2, shadowf, extend=0.4)
        for j in range(4):
            spike(m, ab, (sx * 12.0 + (j - 1.5) * 0.8, 12.0, -8.0), (sx * 0.3, -1, -0.5), 0.7, 3.4, shadowf, tip=0.2)
    return m
