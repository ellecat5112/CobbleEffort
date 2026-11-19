"""Earbuds Rotom (Electric/Normal), after the user's Rotom doodle sheet (artist not named): Rotom inside an earbud
charging case. A round orange clamshell case, its lid swung open; the two earbuds sitting in their wells are its eyes,
and a row of little white charging lights on the front makes its grin. Green plasma crackles round it.

Front is -z, y is up. 16 units tall; about 0.7 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _rotomform import bolt_plane, palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (130, 220, 90), "aura_light": (220, 255, 190), "iris": (90, 170, 240)})
HEIGHT = 16
SCALE = round(0.7 * 16 / HEIGHT, 3)
HITBOX = [0.8, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an open orange earbud case whose two earbuds are its eyes, with a grin of little white charging lights"


def base(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and 2.0 <= y <= 3.2:
        for lx in (-1.6, 0, 1.6):
            if abs(x - lx) < 0.5:
                return p["white"], p["white"]               # charging lights: its grin
    if face == "up" and abs(x) < 5 and z < 2:
        return p["orange_dark"], None
    return tone(p["orange"], face), None


def lid(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for ex in (-2.6, 2.6):
            e = rotom_eye(x - ex, y - 10.2, 2.0, p)
            if e:
                return e
        return p["orange_dark"], None
    return tone(p["orange_light"], face), None


def build() -> Model:
    m = Model("rotom_earbuds")
    top = m.bone("rotom_earbuds", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 6, 4, 0, 6, base, cut=1.8)                     # the case
    hd = m.bone("head", bd, (0, 6, 4))                                    # the lid, swung open: the earbuds are its eyes
    m.box(hd, -6, 5.5, 2.6, 6, 14, 4.4, lid)
    m.box(hd, -4.5, 14, 2.8, 4.5, 15.2, 4.2, lid)
    for x, y, z, w, h, pl, fl in [(-9, 4, -1, 4, 7, "xy", False), (6, 6, -1, 4, 6, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
