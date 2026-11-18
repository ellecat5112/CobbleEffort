"""Pagumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a mischievous lavender blob with sly red-orange eyes, a cat-like smirk and two long ears spread like
wings, floating over its shadow. 0.5 blocks tall.

Front is -z, y is up. 14 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.5, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a mischievous lavender blob with sly red-orange eyes, a cat-like smirk and long ears spread like wings"
BASE = {"lav": (170, 160, 230), "lav_dark": (110, 100, 180), "eye": (230, 100, 40), "black": (30, 26, 40)}
SHINY = {"lav": (240, 190, 140), "lav_dark": (190, 130, 80)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "lav", dark="lav_dark", var=0.02)


def build():
    m = Model("pagumon")
    top = m.bone("pagumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 6.0, 0), 5.4, BODY, layers=5, ry=4.0, squash=0.85)
    for sx in (-1, 1):
        m.box(bd, sx * 1.8 - 0.9, 7.0, -4.75, sx * 1.8 + 0.9, 7.8, -4.6, solid(P, "eye"))
        x0, x1 = sorted((sx * 4.4, sx * 11.0))                                          # wing-like ears
        m.box(bd, x0, 8.0, -0.6, x1, 10.6, 0.6, BODY, rotation=(0, 0, sx * 12), pivot=(sx * 4.4, 9.0, 0))
    m.box(bd, -1.4, 5.0, -4.75, 1.4, 5.4, -4.6, solid(P, "black"))
    m.round_box(top, 0, 0, 3.6, 3.0, 0.0, 0.3, solid(P, "black"), cut=1)
    return m
