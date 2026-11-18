"""Metal Piranimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a piranha whose whole front half is a great steel box of a head: a riveted steel snout
with a jagged steel jaw of triangular teeth, small red eyes, a round red-orange fish body behind it with a crest of
spiny green fins, a brass collar, and a heavy steel weight swinging from a chain under its chin. 35 blocks long.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, riveted, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a piranha whose front half is a great riveted steel box of a head with a jagged steel jaw, a round red-orange "
        "fish body with spiny green fins and a heavy steel weight on a chain")
BASE = {"steel": (200, 204, 214), "steel_dark": (100, 104, 116), "fish": (220, 90, 40), "fish_dark": (130, 40, 14),
        "fin": (110, 170, 60), "fin_dark": (50, 100, 24), "brass": (220, 180, 70), "eye": (240, 40, 40),
        "mouth": (40, 20, 24), "chain": (130, 134, 146)}
SHINY = {"steel": (230, 200, 110), "steel_dark": (150, 110, 40), "fish": (80, 140, 220), "fish_dark": (30, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = riveted(P, "steel", "steel_dark", spacing=2.6)
FISH = scales(P, "fish", "fish_dark", size=1.6)


def build():
    m = Model("metalpiranimon")
    top = m.bone("metalpiranimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 22.0, 8.0), 10.0, FISH, layers=6, squash=1.0)                           # round fish body
    for j in range(7):                                                                   # spiny green fin crest
        spike(m, bd, (0, 30.0 - j * 0.8, 2.0 + j * 2.4), (0, 1, 0.5), 1.8, 10.0 - abs(j - 3) * 1.4,
              scales(P, "fin", "fin_dark", size=1.0), tip=0.8)
    for sx in (-1, 1):
        spike(m, bd, (sx * 9.0, 18.0, 10.0), (sx * 1, -0.3, 0.6), 1.6, 6.0, solid(P, "fin"), tip=0.8)
    spike(m, bd, (0, 22.0, 18.0), (0, 0, 1), 3.0, 6.0, solid(P, "fin"), tip=0.8)              # tail fin
    m.round_box(bd, 0, -2.0, 7.0, 1.6, 15.0, 29.0, metal(P, "brass"), cut=1)                 # brass collar
    hd = m.bone("head", bd, (0, 22, -4))
    m.round_box(hd, 0, -12.0, 8.0, 8.0, 24.0, 34.0, STEEL, cut=1)                           # steel box head
    m.round_box(hd, 0, -13.0, 7.0, 7.0, 13.0, 21.0, STEEL, cut=1)                           # lower jaw box
    m.box(hd, -6.4, 21.0, -20.2, 6.4, 24.0, -6.0, solid(P, "mouth"))
    for j in range(8):                                                                   # jagged steel teeth
        for sx in (-1, 1):
            spike(m, hd, (sx * 6.0, 24.0, -19.0 + j * 1.8), (0, -1, 0), 1.4, 2.4, metal(P, "steel"), tip=0.8)
            spike(m, hd, (sx * 6.0, 21.0, -18.0 + j * 1.8), (0, 1, 0), 1.4, 2.0, metal(P, "steel"), tip=0.8)
        spike(m, hd, (-5.0 + j * 1.4, 24.0, -20.0), (0, -1, 0), 1.2, 2.2, metal(P, "steel"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 8.0, sx * 8.2), 30.0, -8.0, max(sx * 8.0, sx * 8.2), 31.6, -6.4, solid(P, "eye", glow=True))
    cb = m.bone("weight", hd, (0, 13, -8))                                               # chain + steel weight
    for j in range(5):
        y0 = 13.0 - j * 1.8
        m.box(cb, -0.5 if j % 2 else -0.2, y0 - 1.8, -8.5 if j % 2 else -8.2, 0.5 if j % 2 else 0.2, y0,
              -7.5 if j % 2 else -7.8, solid(P, "chain"))
    m.round_box(cb, 0, -8.0, 3.0, 3.0, 0.0, 4.0, metal(P, "steel"), cut=1)
    m.round_box(cb, 0, -8.0, 2.2, 2.2, 4.0, 4.6, metal(P, "steel"), cut=0)
    return m
