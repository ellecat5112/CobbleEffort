"""Pandamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a stuffed toy panda: a plump black-and-white plush bear with a grumpy half-lidded face, a crossed
sticking plaster on its white belly, a red scarf streaming out behind it like flame, and stubby clawed paws. 25 blocks
tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a plump black-and-white plush panda with a grumpy face, a crossed plaster on its belly and a streaming red scarf"
BASE = {"white": (246, 246, 244), "white_dark": (190, 190, 186), "black": (40, 38, 40), "black_dark": (14, 14, 16),
        "red": (220, 50, 40), "red_dark": (140, 20, 14), "plaster": (240, 230, 220), "eye": (220, 130, 40),
        "claw": (230, 220, 200)}
SHINY = {"black": (150, 90, 60), "black_dark": (90, 50, 30)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fur(P, "white", "white_dark", length=1.2)
BLACK = fur(P, "black", "black_dark", length=1.2)


def build():
    m = Model("pandamon")
    top = m.bone("pandamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 20.0, 0.4), 8.0, BLACK, layers=6, ry=10.0, squash=0.85)
    ball(m, bd, (0, 19.0, -4.6), 5.4, WHITE, layers=4, ry=7.0, squash=0.4)
    for ang in (40, -40):
        m.box(bd, -3.0, 18.4, -7.1, 3.0, 19.6, -6.9, solid(P, "plaster"), rotation=(0, 0, ang), pivot=(0, 19.0, -7.0))
    for j in range(5):                                                                   # streaming red scarf
        m.box(bd, 6.0 + j * 3.0, 29.0 + j * 0.6, 1.0, 9.0 + j * 3.0, 31.0 + j * 0.6, 1.2, fabric(P, "red", "red_dark"),
              rotation=(0, 0, 10 + j * 5), pivot=(7.5 + j * 3.0, 30.0 + j * 0.6, 1.1))
    m.round_box(bd, 0, 0, 5.4, 4.8, 28.0, 30.4, fabric(P, "red", "red_dark"), cut=1)
    hd = m.bone("head", bd, (0, 30, 0))
    ball(m, hd, (0, 36.0, -0.6), 6.6, WHITE, layers=6, ry=5.8, squash=0.9)
    for sx in (-1, 1):
        m.round_box(hd, sx * 2.6, -6.2, 1.8, 0.6, 35.0, 37.6, solid(P, "black"), cut=0)
        m.box(hd, sx * 2.6 - 0.8, 35.8, -6.85, sx * 2.6 + 0.8, 36.4, -6.75, solid(P, "eye"))
        ball(m, hd, (sx * 5.0, 41.0, 0), 2.2, BLACK, layers=2, squash=0.5)
    m.box(hd, -0.8, 33.4, -6.85, 0.8, 34.0, -6.75, solid(P, "black"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 26.0, 0))
        rod(m, ab, (sx * 7.0, 26.0, 0), (sx * 10.0, 18.0, -2.0), 5, BLACK, extend=0.6)
        for f in range(3):
            spike(m, ab, (sx * 10.0 + (f - 1) * 1.0, 15.6, -3.0), (0, -0.6, -1), 0.8, 1.6, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 12.0, 0))
        rod(m, lg, (sx * 4.0, 13.0, 0), (sx * 4.4, 3.0, -0.6), 7, BLACK, extend=0.8)
        m.round_box(lg, sx * 4.4, -1.4, 3.4, 4.0, 0.0, 2.6, BLACK, cut=1)
    return m
