"""Piccolomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little pink fairy with a big round cream face, huge black eyes, a happy open mouth, rosy
cheeks, a shaggy pink body, a long spear with a spiked steel head and red tassels, and two pairs of long white
feathered wings marked with red stitches. 25 blocks tall.

Front is -z, y is up. 36 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a little pink fairy with a big round cream face, huge black eyes, a long spiked spear and two pairs of long white wings"
BASE = {"pink": (240, 130, 180), "pink_dark": (180, 70, 120), "cream": (250, 236, 210), "cream_dark": (210, 190, 160),
        "black": (20, 18, 24), "white": (246, 246, 250), "white_dark": (190, 190, 210), "red": (210, 40, 60),
        "steel": (200, 204, 216), "steel_dark": (90, 94, 108), "blue": (60, 80, 180), "cheek": (250, 170, 190)}
SHINY = {"pink": (150, 200, 240), "pink_dark": (80, 130, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("piccolomon")
    top = m.bone("piccolomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 9.0, 0.6), 4.0, fur(P, "pink", "pink_dark"), layers=4, ry=4.6)
    ball(m, bd, (0, 13.6, -0.6), 4.6, skin(P, "cream", dark="cream_dark"), layers=4, ry=4.4)   # big round face
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.8, 14.6, -4.6), 1.3, solid(P, "black"), layers=2, squash=0.5)
        m.box(bd, sx * 3.2 - 0.6, 12.6, -4.6, sx * 3.2 + 0.6, 13.2, -4.4, solid(P, "cheek"))
    m.round_box(bd, 0, -4.8, 1.2, 0.3, 11.4, 12.6, solid(P, "red"), cut=0)
    for i in range(6):
        ang = math.radians(-60 + i * 24)
        spike(m, bd, (4.0 * math.sin(ang), 17.4, -0.6), (math.sin(ang) * 0.5, 1, 0.3), 1.2, 2.4, fur(P, "pink", "pink_dark"),
              tip=0.8)
    for side in (1, -1):                                                                 # two pairs of long wings
        for j in range(2):
            x0, x1 = sorted((side * 2.0, side * (16.0 - j * 3.0)))
            m.box(bd, x0, 13.0 - j * 3.0, 3.0 + j * 0.5, x1, 16.0 - j * 3.0, 3.0 + j * 0.5,
                  feathers(P, "white", "white_dark", tip="red"), rotation=(0, side * 10, side * (55 - j * 25)),
                  pivot=(side * 2.0, 14.0, 3.0))
    rod(m, bd, (-12.0, 6.0, -4.0), (14.0, 12.0, -4.0), 1, solid(P, "blue"), extend=0.2)    # long spear
    spike(m, bd, (-12.0, 6.0, -4.0), (-1, -0.2, 0), 1.6, 4.0, metal(P, "steel", dark="steel_dark"), tip=0.8)
    for j in range(3):
        spike(m, bd, (-12.0 + j * 1.0, 6.6, -4.0), (0, 1, 0), 0.8, 1.4, metal(P, "steel"), tip=0.8)
    rod(m, bd, (-9.0, 6.4, -4.0), (-9.6, 2.0, -4.0), 1, solid(P, "red"), extend=0.1, t2=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 5.0, 0))
        rod(m, lg, (sx * 1.6, 5.4, 0), (sx * 2.0, 2.0, -0.6), 1, fur(P, "pink", "pink_dark"), extend=0.2, t2=2)
    return m
