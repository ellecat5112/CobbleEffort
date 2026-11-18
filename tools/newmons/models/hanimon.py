"""Hanimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
haniwa: a little brown clay figure shaped like a hollow-eyed haniwa with a surprised round mouth, a sprout of green
leaves on its head, two long noodle arms, a thick braided rope belt and a flared base with a zigzag hem. Child stage,
1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import skin, solid, twisted
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = "a little brown clay haniwa with hollow eyes, a round mouth, a leaf sprout, noodle arms and a braided rope belt"
BASE = {"clay": (190, 130, 80), "clay_dark": (130, 80, 40), "hole": (24, 18, 16), "leaf": (80, 170, 60),
        "leaf_dark": (30, 110, 30), "rope": (230, 210, 170), "rope_dark": (170, 150, 110)}
SHINY = {"clay": (150, 150, 160), "clay_dark": (90, 90, 100)}


def P(v):
    return pal(BASE, SHINY, v)


CLAY = skin(P, "clay", dark="clay_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - sx * 2.0) * 0.8, y - 21.0) < 1.4:
                return tone(p["hole"], face), None
        if math.hypot(x, y - 17.0) < 0.9:
            return tone(p["hole"], face), None
    if box is not None and box.lo[1] < 4.0 and face in ("north", "south", "east", "west"):
        u = x if face in ("north", "south") else z
        if y > 3.0 - 1.4 * abs(((u * 0.8) % 2.0) - 1.0):
            return tone(p["clay_dark"], face), None
    return CLAY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hanimon")
    top = m.bone("hanimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 0.0, 6.0, bodyf, cut=2)                            # flared base
    m.round_box(bd, 0, 0, 4.6, 4.0, 5.0, 25.0, bodyf, cut=3)                           # haniwa body
    m.round_box(bd, 0, 0, 5.2, 4.6, 6.0, 8.6, twisted(P, "rope", "rope_dark", period=1.2, angle=0.8), cut=2)
    hd = m.bone("head", bd, (0, 25, 0))
    for j in range(5):                                                                  # leaf sprout
        ang = math.radians(-60 + j * 30)
        spike(m, hd, (0, 24.6, 0), (math.sin(ang), 1, 0.2), 1.4, 6.0, skin(P, "leaf", dark="leaf_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.4, 16.0, 0))
        pts = [(sx * 4.4, 16.0, 0), (sx * 8.0, 20.0, -1.0), (sx * 10.0, 24.0, -1.0)] if sx < 0 else \
              [(sx * 4.4, 16.0, 0), (sx * 8.0, 12.0, -1.0), (sx * 10.0, 6.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, CLAY, extend=0.4)
    return m
