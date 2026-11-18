"""Ohakadamon (a Digimon of the CobbleEffort: Digital crossover; after the official sprite on wikimon.net): the data of
a fallen Digimon resting as a little black gravestone marked with a white cross, on a small mound. 0.5 blocks tall.

Front is -z, y is up. 16 units tall; Baby II stage (no level on wikimon).
"""
from __future__ import annotations

from _boxmodel import Model
from _digi import sized
from _digidetail import armour, solid
from _route import pal

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a little black gravestone marked with a white cross on a small mound"
BASE = {"stone": (40, 40, 46), "stone_dark": (14, 14, 18), "white": (246, 246, 246), "grey": (120, 120, 126)}
SHINY = {"stone": (220, 220, 230), "stone_dark": (150, 150, 160), "white": (40, 40, 46)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("ohakadamon")
    top = m.bone("ohakadamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.round_box(bd, 0, 0, 6.0, 4.0, 0.0, 2.0, solid(P, "grey"), cut=1)                    # mound
    m.round_box(bd, 0, 0, 4.0, 1.6, 2.0, 14.0, armour(P, "stone", "stone_dark"), cut=1)   # gravestone
    m.box(bd, -0.8, 5.0, -1.75, 0.8, 12.0, -1.6, solid(P, "white"))                       # white cross
    m.box(bd, -2.6, 9.0, -1.75, 2.6, 10.6, -1.6, solid(P, "white"))
    return m
