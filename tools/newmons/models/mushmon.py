"""Mushmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a mischievous little mushroom: a big purple cap ringed with yellow, a pale cream face with a sly
buck-toothed grin, a string of purple beads, and huge magenta boxing gloves (one with a skull and crossbones) and
studded strapped boots. 1 block tall.

Front is -z, y is up. 34 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import leather, local, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little mushroom with a big purple cap ringed yellow, a sly buck-toothed grin, huge magenta boxing gloves and studded boots"
BASE = {"cap": (140, 90, 180), "cap_dark": (80, 40, 110), "ring": (240, 220, 80), "cream": (250, 244, 200),
        "cream_dark": (210, 200, 150), "magenta": (220, 50, 140), "magenta_dark": (130, 20, 80), "black": (30, 26, 30),
        "white": (250, 250, 250), "bead": (160, 100, 200)}
SHINY = {"cap": (230, 100, 60), "cap_dark": (150, 50, 20), "magenta": (60, 170, 220), "magenta_dark": (20, 100, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def capf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    for (a, b) in ((0.0, 0.0), (3.6, 2.0), (-3.6, 2.0), (2.0, -3.0), (-2.0, -3.0)):
        if face == "up" and abs(math.hypot(x - a, z - b) - 1.4) < 0.4:
            return tone(p["ring"], face), None
        if face == "north" and abs(math.hypot(x - a * 1.2, y - 28.0) - 1.2) < 0.35:
            return tone(p["ring"], face), None
    return tone(p["cap"], face), None


FACE = skin(P, "cream", dark="cream_dark")
GLOVE = skin(P, "magenta", dark="magenta_dark")


def build():
    m = Model("mushmon")
    top = m.bone("mushmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 15.0, 0), 5.0, FACE, layers=5, ry=6.0)                               # pale body/face
    for sx in (-1, 1):
        m.box(bd, sx * 1.6 - 0.4, 17.0, -4.9, sx * 1.6 + 0.4, 17.8, -4.75, solid(P, "black"))
    m.box(bd, -1.6, 13.6, -4.95, 1.6, 14.2, -4.8, solid(P, "black"))
    m.box(bd, -0.8, 12.8, -4.95, 0.8, 13.6, -4.8, solid(P, "white"))                      # buck teeth
    hd = m.bone("head", bd, (0, 21, 0))
    m.round_box(hd, 0, 0, 9.0, 8.0, 21.0, 27.0, capf, cut=3)                             # big purple cap
    m.round_box(hd, 0, 0, 6.0, 5.6, 27.0, 30.0, capf, cut=2)
    for i in range(7):                                                                   # bead string
        ang = math.radians(-60 + i * 20)
        ball(m, bd, (5.0 * math.sin(ang), 19.0 - abs(i - 3) * 0.6, -4.0 * math.cos(ang)), 0.7, solid(P, "bead"),
             layers=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # huge boxing gloves
        ab = m.bone(nm, bd, (sx * 4.6, 15.0, 0))
        rod(m, ab, (sx * 4.6, 15.0, 0), (sx * 7.0, 12.0, -1.0), 1, FACE, extend=0.2)
        ball(m, ab, (sx * 8.6, 11.0, -1.6), 3.4, GLOVE, layers=3)
        if sx < 0:
            m.box(ab, -10.0, 10.0, -5.15, -7.2, 12.4, -5.0, solid(P, "white"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # studded strapped boots
        lg = m.bone(nm, top, (sx * 2.6, 9.0, 0))
        rod(m, lg, (sx * 2.6, 10.0, 0), (sx * 3.0, 6.0, 0), 1, FACE, extend=0.2)
        m.round_box(lg, sx * 3.0, -0.8, 2.8, 3.6, 0.0, 6.0, GLOVE, cut=1)
        m.round_box(lg, sx * 3.0, -0.8, 3.0, 3.8, 4.0, 4.8, leather(P, "black", "black"), cut=1)
        for j in range(3):
            ball(m, lg, (sx * 3.0 + (j - 1) * 1.6, 1.0, -4.4), 0.6, GLOVE, layers=1)
    return m
