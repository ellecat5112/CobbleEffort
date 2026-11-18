"""Gasamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
wandering octopus samurai: a little black octopus with one big red eye peeking from under a huge woven straw hat with
a blue horn and a white paper charm, pink-and-red curling tentacles beneath and a katana in a long grey scabbard
clutched in one tentacle. Child stage, 1 block tall.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = ("a little black octopus with one big red eye under a huge woven straw hat with a blue horn and a paper charm, "
        "pink curling tentacles and a katana in a grey scabbard")
BASE = {"black": (34, 30, 40), "black_dark": (12, 10, 16), "straw": (190, 150, 90), "straw_dark": (130, 96, 50),
        "pink": (240, 100, 140), "pink_dark": (170, 40, 80), "eye": (220, 30, 40), "white": (246, 246, 246),
        "blue": (90, 130, 220), "grey": (150, 150, 160), "grey_dark": (80, 80, 90), "red": (200, 30, 40)}
SHINY = {"pink": (120, 210, 230), "pink_dark": (50, 140, 170), "straw": (230, 230, 220), "straw_dark": (170, 170, 160)}


def P(v):
    return pal(BASE, SHINY, v)


STRAW = strands(P, "straw", "straw_dark")


def build():
    m = Model("gasamon")
    top = m.bone("gasamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 4.0, 3.6, 6.0, 13.0, skin(P, "black", dark="black_dark"), cut=2)
    m.round_box(bd, 0, -3.8, 1.6, 0.4, 8.6, 11.4, solid(P, "white"), cut=0)                # big eye
    m.box(bd, -0.8, 9.2, -4.4, 0.8, 10.8, -4.2, solid(P, "eye"))
    hd = m.bone("head", bd, (0, 13, 0))
    for j, r in enumerate((10.0, 8.0, 6.0, 4.0, 2.0)):                                       # woven cone hat
        m.round_box(hd, 0, 0, r, r, 12.0 + j * 1.6, 13.6 + j * 1.6, STRAW, cut=max(1, int(r * 0.4)))
    spike(m, hd, (4.0, 16.0, -2.0), (1, 0.4, -0.4), 1.6, 5.0, solid(P, "blue"), tip=0.8)     # horn
    m.round_box(hd, -3.0, -6.0, 1.2, 0.2, 13.0, 17.0, solid(P, "white"), cut=0)              # paper charm
    for i in range(8):                                                                         # curling tentacles
        ang = 2 * math.pi * i / 8
        p0 = (3.0 * math.cos(ang), 6.0, 3.0 * math.sin(ang))
        p1 = (6.0 * math.cos(ang), 2.0, 6.0 * math.sin(ang))
        p2 = (8.0 * math.cos(ang + 0.4), 3.0, 8.0 * math.sin(ang + 0.4))
        rod(m, bd, p0, p1, 1, skin(P, "pink", dark="pink_dark"), extend=0.3, t2=2)
        rod(m, bd, p1, p2, 1, skin(P, "pink", dark="pink_dark"), extend=0.3, t2=1)
    ab = m.bone("arm_right", bd, (-3.0, 9.0, -2.0))                                          # katana
    rod(m, ab, (-10.0, 6.0, -4.0), (6.0, 16.0, -4.0), 2, metal(P, "grey", dark="grey_dark"), extend=0)
    m.round_box(ab, -10.6, -4.0, 1.4, 1.4, 5.0, 7.0, solid(P, "red"), cut=0)
    return m
