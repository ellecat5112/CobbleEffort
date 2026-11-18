"""Pawn Shoutmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net): Shoutmon
drafted as a pawn soldier: a little red dragon with a big yellow beak-like mouth and blue eyes, red horn-ears, a white
belly, red jacket, yellow gloves, wearing a gold pawn helmet with a barred visor and green ear-pieces, holding a forked
spear. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage (no level on wikimon).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little red dragon in a gold pawn helmet with a barred visor, a red jacket, yellow gloves and a forked spear"
BASE = {"red": (220, 50, 40), "red_dark": (130, 20, 14), "white": (240, 240, 246), "yellow": (250, 210, 50),
        "gold": (230, 190, 70), "gold_dark": (150, 110, 20), "green": (70, 170, 70), "black": (24, 22, 28),
        "eye": (60, 120, 220), "steel": (200, 204, 216), "beak": (240, 180, 40)}
SHINY = {"red": (70, 110, 210), "red_dark": (24, 50, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("pawnshoutmon")
    top = m.bone("pawnshoutmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 3.4, 2.8, 8.0, 17.0, skin(P, "white", dark="red_dark"), cut=1)
    for sx in (-1, 1):                                                                   # red jacket sides
        x0, x1 = sorted((sx * 2.4, sx * 3.8))
        m.box(bd, x0, 8.0, -3.0, x1, 17.0, 3.0, fabric(P, "red", "red_dark"))
    m.box(bd, -3.8, 8.0, 2.8, 3.8, 17.0, 3.2, fabric(P, "red", "red_dark"))
    hd = m.bone("head", bd, (0, 17, 0))
    ball(m, hd, (0, 20.6, -0.4), 3.6, skin(P, "red", dark="red_dark"), layers=4, ry=3.2)
    m.round_box(hd, 0, -3.6, 2.4, 1.2, 18.2, 19.6, solid(P, "beak"), cut=0)
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.6, 20.6, -3.75, sx * 1.4 + 0.6, 21.8, -3.6, solid(P, "eye"))
        spike(m, hd, (sx * 2.6, 23.0, 0), (sx * 0.6, 1, 0), 1.4, 3.6, skin(P, "red", dark="red_dark"), tip=0.8)
        ball(m, hd, (sx * 3.6, 21.6, 0), 0.9, solid(P, "green"), layers=1)
    m.round_box(hd, 0, 0, 3.8, 3.8, 22.4, 24.4, armour(P, "gold", "gold_dark"), cut=1)    # gold pawn helmet
    for j in range(4):
        m.box(hd, -2.0 + j * 1.2, 21.8, -3.9, -1.6 + j * 1.2, 23.0, -3.7, armour(P, "gold", "gold_dark"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 15.0, 0))
        rod(m, ab, (sx * 3.6, 15.0, 0), (sx * 4.4, 11.0, -1.0), 2, fabric(P, "red", "red_dark"), extend=0.3)
        ball(m, ab, (sx * 4.6, 10.4, -1.2), 1.2, solid(P, "yellow"), layers=2)
    rod(m, "arm_left", (4.6, 2.0, -1.2), (4.6, 24.0, -1.2), 1, metal(P, "steel"), extend=0.2)   # forked spear
    for sx in (-1, 1):
        rod(m, "arm_left", (4.6, 22.0, -1.2), (4.6 + sx * 1.6, 26.0, -1.2), 1, metal(P, "steel"), extend=0.1)
    spike(m, "arm_left", (4.6, 24.0, -1.2), (0, 1, 0), 1.0, 3.0, metal(P, "steel"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 8.0, 0))
        rod(m, lg, (sx * 1.6, 8.0, 0), (sx * 2.0, 1.0, 0), 2, skin(P, "white", dark="red_dark"), extend=0.3)
        m.round_box(lg, sx * 2.0, -0.8, 1.4, 2.0, 0.0, 1.4, skin(P, "white", dark="red_dark"), cut=0)
    return m
