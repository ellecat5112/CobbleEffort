"""Gekomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
musician frog: a lanky green frog with huge bulging red-ringed eyes, a wide grin full of fangs, a long pink tongue, a
white throat, pale spots on its back, a golden tuba-horn coiled round its neck and long legs with round-tipped
toes. Adult stage, 15 blocks tall.

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a lanky green frog with huge bulging red-ringed eyes, a fanged grin, a long pink tongue and a golden tuba-horn "
        "coiled round its neck")
BASE = {"green": (90, 190, 80), "green_dark": (40, 120, 30), "white": (246, 246, 236), "white_dark": (190, 190, 170),
        "red": (210, 40, 40), "pupil": (20, 20, 24), "mouth": (130, 20, 30), "tooth": (250, 250, 240),
        "tongue": (240, 100, 150), "gold": (250, 210, 60), "gold_dark": (170, 120, 20), "spot": (200, 230, 160)}
SHINY = {"green": (120, 150, 230), "green_dark": (50, 70, 160)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = skin(P, "green", dark="green_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def eyef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
        d = math.hypot(x - cx, y - cy)
        if d < 0.5:
            return tone(p["pupil"], face), None
        if d < 1.1:
            return tone(p["red"], face), None
    return tone(p["white"], face), None


def build():
    m = Model("gekomon")
    top = m.bone("gekomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0.6, 3.6, 3.4, 16.0, 28.0, GREEN, cut=1)
    m.round_box(bd, 0, -2.4, 2.8, 1.0, 17.0, 26.0, skin(P, "white", dark="white_dark"), cut=1)
    hd = m.bone("head", bd, (0, 28, -1))
    m.round_box(hd, 0, -1.4, 4.6, 3.8, 27.6, 32.6, GREEN, cut=2)
    m.box(hd, -4.0, 28.4, -5.3, 4.0, 30.4, -5.0, solid(P, "mouth"))                  # fanged grin
    for j in range(7):
        spike(m, hd, (-3.6 + j * 1.2, 30.4, -5.2), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
    rod(m, hd, (1.0, 28.8, -5.0), (4.0, 24.0, -9.0), 1, skin(P, "tongue", dark="red"), extend=0.3, t2=2)
    for sx in (-1, 1):                                                                 # huge bulging eyes
        m.round_box(hd, sx * 2.6, -2.0, 2.2, 2.2, 32.0, 36.4, eyef, cut=1)
    m.round_box(hd, 0, 0.0, 5.0, 4.2, 26.4, 28.0, GOLD, cut=2)                          # tuba coiled round the neck
    m.round_box(hd, 4.6, -2.0, 2.6, 2.6, 28.0, 31.0, GOLD, cut=1)
    m.box(hd, 3.0, 28.4, -4.8, 6.2, 30.6, -4.5, solid(P, "gold_dark"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 26.0, -1.0))
        rod(m, ab, (sx * 3.4, 26.0, -1.0), (sx * 7.0, 20.0, -3.0), 1, GREEN, extend=0.3, t2=2)
        for j in range(3):
            rod(m, ab, (sx * 7.0, 20.0, -3.0), (sx * (8.0 + j * 0.8), 17.0, -4.0 + j * 0.8), 1, GREEN, extend=0.2)
            m.round_box(ab, sx * (8.0 + j * 0.8), -4.0 + j * 0.8, 0.6, 0.6, 16.4, 17.4, GREEN, cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 16.0, 0))
        rod(m, lg, (sx * 2.4, 16.0, 0), (sx * 4.6, 9.0, -2.0), 2, GREEN, extend=0.4)
        rod(m, lg, (sx * 4.6, 9.0, -2.0), (sx * 4.0, 1.0, 1.0), 2, GREEN, extend=0.4)
        for j in range(3):
            rod(m, lg, (sx * 4.0, 1.0, 1.0), (sx * (4.0 + (j - 1) * 1.6), 0.6, -3.0), 1, GREEN, extend=0.2)
            m.round_box(lg, sx * (4.0 + (j - 1) * 1.6), -3.0, 0.7, 0.7, 0.0, 1.2, GREEN, cut=0)
    return m
