"""Antenna Rotom (Electric/Fairy), after the user's Rotom doodle sheet (artist not named): Rotom inside a pair of
rabbit-ear TV antennas. A round orange head with two tall rabbit-ear antennas (pink inside), blue lens eyes, two buck
teeth over a black grin of braces, and a drippy body of glowing pink plasma with white fangs below.

Front is -z, y is up. 30 units tall; about 1.2 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import ball, palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (250, 120, 170), "aura_light": (255, 210, 230), "iris": (80, 140, 220), "plasma": (250, 120, 170, 200)},
            {"plasma": (130, 230, 250, 200)})
HEIGHT = 30
SCALE = round(1.2 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a round orange head with rabbit-ear antennas and braces, over a drippy body of glowing pink plasma"


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = rotom_eye(x - 2.2 * sx, y - 17.4, 1.5, p)
            if e:
                return e
        if 13.2 <= y <= 14.8 and abs(x) <= 3.4:            # a black grin of braces with white rivets
            return (p["white"] if abs((x + 3.4) % 1.1 - 0.55) < 0.25 and abs(y - 14.0) < 0.3 else p["black"]), None
        if 14.8 < y <= 15.8 and 0.15 < abs(x) <= 1.1:
            return p["white"], None                         # buck teeth
    return tone(p["orange"], face), None


def plasma(x, y, z, face, variant, **k):
    c = P(variant)["plasma"]
    return c, c[:3]


def build() -> Model:
    m = Model("rotom_antenna")
    top = m.bone("rotom_antenna", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 4.0, 2.6, 4, 11.5, plasma, cut=1.2)            # the drippy plasma body
    for x in (-2.6, -0.8, 1.0, 2.8):
        rod(m, bd, (x, 5, 0), (x * 1.2, 1.5 - abs(x) * 0.3, 0.2), 1.0, plasma, extend=0.3)   # drips
        rod(m, bd, (x * 0.8, 9, -2.7), (x * 0.8, 6.2, -2.9), 0.7, solid(P, "white"), extend=0.2)   # fangs
    for sx in (-1, 1):
        rod(m, bd, (3.6 * sx, 9, 0), (7.5 * sx, 4, -1), 1.6, plasma, extend=0.4)            # plasma arms
    hd = m.bone("head", bd, (0, 16, 0))
    ball(m, hd, 0, 16, 0, 5.0, head)                                     # the round head
    for sx in (-1, 1):                                                    # rabbit-ear antennas
        rod(m, hd, (2.2 * sx, 20, 0.5), (4.2 * sx, 30, 1.5), 2.4, solid(P, "orange"), extend=0.4)
        rod(m, hd, (2.2 * sx, 20.5, -0.8), (4.1 * sx, 29, 0.3), 1.0, solid(P, "aura"), extend=0.2)
    return m
