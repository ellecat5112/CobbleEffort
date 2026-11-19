"""Tsumemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little lavender blob of a creature with one big fiery orange eye, a long curling feeler, lumpy
rounded limbs and sharp white claws. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, plane, skin, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "biped"
K = 4
LOOK = "a little lavender blob with one big fiery orange eye, a long curling feeler and sharp white claws"
BASE = {"lav": (150, 150, 220), "lav_dark": (90, 90, 170), "eye": (250, 140, 40), "pupil": (40, 10, 10),
        "white": (255, 255, 255), "claw": (250, 250, 250)}
SHINY = {"lav": (200, 220, 140), "lav_dark": (130, 160, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        c = eye(p, a, b - 11.0, 2.2, "eye", ring="pupil")
        if c is not None:
            return c, None
    return skin(P, "lav", dark="lav_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tsumemon")
    top = m.bone("tsumemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 10.0, 0), 5.0, bodyf, layers=5)
    pts = [(0, 14.6, 0), (2.0, 17.0, 1.0), (5.0, 19.4, 1.0), (8.0, 18.6, 0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, skin(P, "lav", dark="lav_dark"), extend=0.3)
    for i, (sx, sz) in enumerate(((1, -1), (-1, -1), (1, 1), (-1, 1))):
        nm = ("leg_front_" if sz < 0 else "leg_back_") + ("left" if sx > 0 else "right")
        lg = m.bone(nm, bd, (sx * 3.0, 6.0, sz * 2.0))
        ball(m, lg, (sx * 4.2, 3.4, sz * 2.4 - 0.6), 2.6, skin(P, "lav", dark="lav_dark"), layers=2)
        spike(m, lg, (sx * 4.6, 1.4, sz * 2.4 - 2.6), (sx * 0.2, -0.6, -1), 0.9, 2.4, solid(P, "claw"), tip=0.8)
    return m
