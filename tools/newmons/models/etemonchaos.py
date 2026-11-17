"""Etemon Chaos (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net): Etemon
fused with the network itself. A huge sphere of tangled dark-violet cables and pale grey conduits knotted round and
round, plugs and connectors poking out all over it, cable ends dangling from its underside, and a tiny Etemon riding
on top with its arms thrown up. 25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a huge sphere of tangled dark-violet cables and grey conduits with plugs poking out, cable ends dangling below "
        "and a tiny Etemon riding on top")
BASE = {"cable": (60, 50, 110), "cable_dark": (20, 16, 50), "cable_light": (120, 110, 180), "conduit": (190, 190, 196),
        "conduit_dark": (110, 110, 120), "plug": (60, 60, 66), "orange": (240, 130, 40), "cream": (250, 236, 210),
        "black": (24, 24, 28)}
SHINY = {"cable": (130, 40, 50), "cable_dark": (60, 10, 14), "cable_light": (210, 110, 120)}


def P(v):
    return pal(BASE, SHINY, v)


CABLE = skin(P, "cable", dark="cable_dark", light="cable_light", var=0.04)
CONDUIT = metal(P, "conduit", dark="conduit_dark")


def build():
    m = Model("etemonchaos")
    top = m.bone("etemonchaos", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    ball(m, bd, (0, 26.0, 0), 13.0, CABLE, layers=9)                                # the tangled core
    for i in range(36):                                                             # cables looping round it
        a = i * 2.39996
        b = math.acos(1 - 2 * (i + 0.5) / 36)
        d = (math.sin(b) * math.cos(a), math.cos(b), math.sin(b) * math.sin(a))
        perp = (-math.sin(a), 0.0, math.cos(a))
        p0 = tuple(14.0 * d[j] - 5.0 * perp[j] for j in range(3))
        p1 = tuple(14.0 * d[j] + 5.0 * perp[j] for j in range(3))
        p0 = (p0[0], p0[1] + 26.0, p0[2])
        p1 = (p1[0], p1[1] + 26.0, p1[2])
        rod(m, bd, p0, p1, 2, CONDUIT if i % 4 == 0 else CABLE, extend=0.6)
        if i % 6 == 0:
            m.round_box(bd, p1[0], p1[2], 1.0, 1.0, p1[1] - 1.0, p1[1] + 1.0, solid(P, "plug"), cut=0)
    for j in range(10):                                                             # dangling cable ends
        ang = 2 * math.pi * j / 10
        base = (8.0 * math.cos(ang), 15.0, 8.0 * math.sin(ang))
        tip = (9.0 * math.cos(ang), 2.0 + (j % 3) * 2.0, 9.0 * math.sin(ang))
        rod(m, bd, base, tip, 1, CABLE, extend=0.4)
        m.round_box(bd, tip[0], tip[2], 0.6, 0.6, tip[1] - 1.0, tip[1], CONDUIT, cut=0)
    hd = m.bone("head", bd, (0, 40, 0))                                             # tiny Etemon on top
    m.round_box(hd, 0, 0, 1.2, 1.0, 38.0, 41.0, fur(P, "orange", "orange", length=0.6), cut=0)
    m.round_box(hd, 0, 0, 1.2, 1.2, 41.0, 43.4, solid(P, "cream"), cut=0)
    m.box(hd, -1.0, 42.4, -1.3, 1.0, 42.8, -1.1, solid(P, "black"))
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.0, 40.6, 0), (sx * 2.6, 43.6, 0), 1, solid(P, "orange"), extend=0.2)
    return m
