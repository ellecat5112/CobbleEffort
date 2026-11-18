"""Pickmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little steel helmet of a creature: a domed grey metal shell with a slit visor, one round black eye
peering out, steel horn spikes sticking out on each side and two pointed steel feet. 0.5 blocks tall.

Front is -z, y is up. 14 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.5, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a little domed steel helmet with a slit visor, one round black eye, horn spikes and two pointed steel feet"
BASE = {"steel": (200, 204, 214), "steel_dark": (100, 104, 116), "black": (24, 24, 28), "white": (240, 240, 240)}
SHINY = {"steel": (230, 200, 120), "steel_dark": (150, 110, 40)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("pickmon")
    top = m.bone("pickmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 6.0, 0), 5.0, STEEL, layers=5, ry=5.4)
    spike(m, bd, (0, 10.6, 0), (0, 1, 0.1), 3.0, 3.0, STEEL, tip=0.8)
    m.box(bd, -3.6, 7.0, -4.8, 3.6, 8.0, -4.4, solid(P, "black"))                          # slit visor
    ball(m, bd, (-1.4, 4.6, -4.4), 1.2, solid(P, "black"), layers=2, squash=0.4)            # one round eye
    m.box(bd, -1.8, 5.0, -4.95, -1.4, 5.4, -4.9, solid(P, "white"))
    for sx in (-1, 1):
        spike(m, bd, (sx * 4.6, 6.0, 0), (sx * 1, 0.3, 0), 1.6, 3.6, STEEL, tip=0.8)
        spike(m, bd, (sx * 2.0, 1.4, -0.4), (sx * 0.3, -1, -0.3), 1.6, 2.6, STEEL, tip=0.8)
    return m
