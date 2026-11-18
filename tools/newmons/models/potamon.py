"""Potamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a potato with attitude: a round russet-brown potato body-head with sly half-lidded eyes and pink
cheeks, a crown of pale potato leaves, a red scarf, blue denim overalls, yellow shirt sleeves, little feet, and a tray
of golden fries held out in one hand. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a russet potato with sly eyes and a crown of pale leaves, a red scarf, blue overalls and a tray of golden fries"
BASE = {"potato": (190, 130, 70), "potato_dark": (130, 80, 30), "leaf": (210, 200, 150), "leaf_dark": (130, 130, 80),
        "red": (200, 40, 40), "red_dark": (120, 14, 14), "denim": (60, 90, 170), "denim_dark": (24, 44, 110),
        "yellow": (250, 200, 60), "black": (24, 20, 20), "white": (250, 250, 250), "blush": (240, 140, 140),
        "fry": (240, 190, 70), "tray": (130, 90, 50), "mouth": (200, 60, 80)}
SHINY = {"potato": (180, 90, 160), "potato_dark": (110, 40, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def potatof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.6) < 1.4 and 25.6 < y < 26.6 + (0.4 if x * sx > 2.6 else 0.0):
                return tone(p["black"] if y < 26.2 else p["white"], face), None
            if math.hypot(x - sx * 4.4, y - 23.6) < 1.0:
                return tone(p["blush"], face), None
        if 21.8 < y < 23.2 and abs(x) < 1.6 - (23.2 - y):
            return tone(p["mouth"], face), None
    if math.sin(x * 2.1) * math.sin(y * 1.7 + z) > 0.93:
        return tone(p["potato_dark"], face), None
    return skin(P, "potato", dark="potato_dark", var=0.05)(x, y, z, face, variant, box=box, **k)


DENIM = fabric(P, "denim", "denim_dark", axis="y", period=1.4)


def build():
    m = Model("potamon")
    top = m.bone("potamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 5.4, 4.6, 5.0, 14.0, DENIM, cut=1)                               # overalls
    for sx in (-1, 1):
        m.box(bd, sx * 2.6 - 0.6, 13.0, -4.8, sx * 2.6 + 0.6, 18.0, -4.4, DENIM)
    hd = m.bone("head", bd, (0, 16, 0))
    ball(m, hd, (0, 24.0, 0), 8.6, potatof, layers=7, ry=8.6, squash=0.9)                 # potato head
    m.round_box(bd, 0, 0, 6.4, 6.0, 15.0, 17.4, fabric(P, "red", "red_dark", axis="x"), cut=2)  # scarf
    rod(m, bd, (-4.0, 16.0, -4.0), (-6.0, 9.0, -6.0), 2, fabric(P, "red", "red_dark", axis="y"), extend=0.2, t2=1)
    for i in range(7):                                                                   # crown of leaves
        ang = 2 * math.pi * i / 7
        p0 = (2.0 * math.cos(ang), 31.0, 2.0 * math.sin(ang))
        m.box(hd, p0[0] - 2.4, 31.0, p0[2], p0[0] + 2.4, 38.0, p0[2], skin(P, "leaf", dark="leaf_dark", var=0.02),
              rotation=(0, -math.degrees(ang) + 90, 0), pivot=p0)
        spike(m, hd, p0, (math.cos(ang), 0.8, math.sin(ang)), 2.6, 7.0, skin(P, "leaf", dark="leaf_dark", var=0.02),
              tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.6, 14.0, 0))
        rod(m, ab, (sx * 6.6, 14.0, 0), (sx * 9.0, 10.0, -3.0), 2, solid(P, "yellow"), extend=0.3)
        ball(m, ab, (sx * 9.4, 9.4, -3.6), 1.6, potatof, layers=2)
    m.box("arm_right", -16.0, 9.0, -9.0, -7.0, 10.0, -1.0, solid(P, "tray"))              # tray of fries
    for j in range(9):
        fx, fz = -14.6 + (j % 3) * 2.6, -7.6 + (j // 3) * 2.2
        m.box("arm_right", fx, 10.0, fz, fx + 0.8, 13.0 + (j % 2), fz + 0.8, solid(P, "fry"),
              rotation=(0, 0, (j - 4) * 6), pivot=(fx, 10.0, fz))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 6.0, 0))
        m.round_box(lg, sx * 2.4, 0, 2.0, 2.0, 2.0, 7.0, DENIM, cut=0)
        m.round_box(lg, sx * 2.4, -1.0, 2.2, 3.0, 0.0, 2.4, potatof, cut=1)
    rod(m, bd, (0, 7.0, 4.0), (0, 4.0, 9.0), 1, potatof, extend=0.2, t2=2)                 # little tail
    return m
