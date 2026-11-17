"""Chiropmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little bat in a hooded cloak. A round dark-blue hooded cloak with pink-lined bat ears and a pink
bat mark, a single glowing yellow eye peering out under a strap, buckled straps, tattered bat-wing sleeves and tiny
pink feet. Child stage.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, ball
from _digidetail import fabric, leather, local, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = ("a little bat in a round dark-blue hooded cloak with pink-lined ears, one glowing yellow eye, buckled straps "
        "and tattered bat-wing sleeves")
BASE = {"cloak": (50, 60, 130), "cloak_dark": (20, 24, 70), "pink": (230, 110, 170), "black": (24, 24, 30),
        "eye": (250, 220, 60), "strap": (40, 40, 50), "strap_light": (100, 100, 116), "buckle": (190, 194, 206),
        "foot": (220, 150, 170)}
SHINY = {"cloak": (130, 40, 50), "cloak_dark": (70, 14, 20), "pink": (240, 200, 90)}


def P(v):
    return pal(BASE, SHINY, v)


CLOAK = fabric(P, "cloak", "cloak_dark", axis="y", period=2.0)


def cloakf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if math.hypot(x - 0.8, y - 13.0) < 1.4:
            return p["eye"], p["eye"]
        if abs(y - 13.0) < 2.2 and abs(x) < 4.2:
            return tone(p["black"], face), None                     # the shadow inside the hood
        if abs(y - 17.4 - 0.4 * abs(x)) < 0.6 and abs(x) < 3.0:
            return tone(p["pink"], face), None                      # bat mark
        if abs(y - 10.4) < 0.6:
            return tone(p["strap"], face), None
    return CLOAK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chiropmon")
    top = m.bone("chiropmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 12.0, 0), 7.4, cloakf, layers=6, squash=0.9)
    hd = m.bone("head", bd, (0, 18, 0))
    for sx in (-1, 1):                                                     # pink-lined bat ears
        m.box(hd, min(sx * 2.4, sx * 7.0), 16.0, 0.0, max(sx * 2.4, sx * 7.0), 26.0, 0.0, solid(P, "pink"),
              rotation=(0, sx * 10, -sx * 20), pivot=(sx * 3.0, 17.0, 0))
        m.box(hd, min(sx * 2.4, sx * 7.4), 16.0, 0.4, max(sx * 2.4, sx * 7.4), 26.4, 0.4, CLOAK,
              rotation=(0, sx * 10, -sx * 20), pivot=(sx * 3.0, 17.0, 0.4))
    for side in (1, -1):                                                   # bat-wing sleeves
        bat_wing(m, bd, (side * 6.0, 11.0, 0.0), 10.0, 8.0, 3, solid(P, "black"), CLOAK, side=side, sweep=-10)
    m.round_box(bd, 0, 0.0, 6.0, 5.0, 4.0, 5.0, leather(P, "strap", "strap_light"), cut=2)
    m.box(bd, -1.0, 3.8, -5.2, 1.0, 5.2, -4.8, solid(P, "buckle"))
    for sx in (-1, 1):
        m.box(bd, sx * 2.0 - 1.0, 0.0, -1.6, sx * 2.0 + 1.0, 4.0, 0.6, solid(P, "foot"))
    return m
