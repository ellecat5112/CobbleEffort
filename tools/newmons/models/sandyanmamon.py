"""Sand Yanmamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a grey desert dragonfly: a segmented grey-steel body, big bulging green compound eyes, a
fanged mouth trailing a dark red scarf, four long pale translucent veined wings and spindly hooked legs. 1 block.

Front is -z, y is up. 18 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(1, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a grey desert dragonfly with big green compound eyes, a fanged mouth, a dark red scarf and four long translucent wings"
BASE = {"grey": (150, 154, 164), "grey_dark": (80, 84, 96), "green": (80, 220, 90), "white": (240, 255, 240),
        "wing": (220, 236, 246, 150), "red": (120, 20, 30), "tooth": (250, 250, 240), "black": (30, 30, 34)}
SHINY = {"grey": (200, 170, 110), "grey_dark": (130, 100, 50), "green": (240, 80, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SEG = armour(P, "grey", "grey_dark")


def build():
    m = Model("sandyanmamon")
    top = m.bone("sandyanmamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 10.0, -1.0), 2.6, SEG, layers=3)
    for j in range(8):                                                                   # segmented tail
        m.round_box(bd, 0, 2.0 + j * 2.0, 1.4 - j * 0.08, 1.0, 9.0 + j * 0.2, 11.0 + j * 0.2, SEG, cut=0)
    hd = m.bone("head", bd, (0, 10, -4))
    ball(m, hd, (0, 10.0, -5.0), 2.4, SEG, layers=2)
    for sx in (-1, 1):
        ball(m, hd, (sx * 2.0, 11.0, -5.6), 1.6, gem(P, "green", "white"), layers=2)
        spike(m, hd, (sx * 1.0, 8.6, -7.0), (0, -1, -0.3), 0.8, 2.0, solid(P, "tooth"), tip=0.8)
    m.box(hd, -2.0, 7.0, -6.0, 2.0, 8.0, -3.0, solid(P, "red"))                             # dark red scarf
    m.box(hd, -1.4, 3.0, -4.0, 1.0, 7.4, -3.6, solid(P, "red"), rotation=(20, 0, 10), pivot=(0, 7.0, -3.8))
    for sx in (-1, 1):                                                                   # four long wings
        for j, zz in enumerate((-1.6, 0.6)):
            x0, x1 = sorted((sx * 1.6, sx * 14.0))
            m.box(bd, x0, 12.0, zz - 1.0, x1, 12.0, zz + 1.2, solid(P, "wing"),
                  rotation=(0, -sx * (10 - j * 20), sx * 8), pivot=(sx * 1.6, 12.0, zz))
    for sx in (-1, 1):
        for j in range(3):
            lg = (sx * 1.4, 8.0, -2.0 + j * 1.4)
            rod(m, bd, lg, (sx * 3.4, 4.0, -3.0 + j * 1.6), 1, solid(P, "black"), extend=0.1, t2=1)
            spike(m, bd, (sx * 3.4, 4.0, -3.0 + j * 1.6), (sx * 0.2, -1, -0.4), 0.8, 2.6, metal(P, "grey"), tip=0.8)
    return m
