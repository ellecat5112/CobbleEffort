"""Minnolith, the Fossil Fry Pokémon (Rock/Water): a round little prehistoric fish revived from a Minnow Fossil. A
pale blue ball of a body with a white face that comes to a point between its big dark eyes, a brown band over its
back, two upright brown fins like ears on top, a third fin behind them, small side fins and a fan of little tail fins.

Front is -z, y is up. 12 units tall to the fin tips; baseScale 0.55 (0.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod
from _minnow import P, finf, round_eye
from _route import tone

SCALE = 0.55
HITBOX = [0.5, 0.5]
KIND = "floater"
K = 6
HEIGHT = 12
LOOK = "a round pale-blue prehistoric fish with a white face, big dark eyes, brown ear-like fins and a fan of tail fins"


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        e = round_eye(face, z, y, -2.6, 4.6, 0.9, p)
        if e:
            return e, None
    if face == "north":
        for sx in (-1, 1):
            e = round_eye(face, x, y, sx * 2.0, 4.6, 0.85, p)
            if e:
                return e, None
    # the white face: the lower front, coming to a point up between the eyes
    white = (face == "north" and y < 4.0 + max(0.0, 2.6 - abs(x) * 1.5)) or face == "down" or \
            (face in ("east", "west") and z < -1.5 and y < 3.6 - (z + 1.5) * 0.4)
    if white:
        return tone(p["white"] if face != "down" else p["white_shade"], face), None
    if face == "up" and abs(z - 1.2) < 0.9:
        return tone(p["fin"], face), None                                  # brown band over the back
    if face in ("east", "west") and abs(z - 1.2 + (y - 6) * 0.3) < 0.8 and y > 4.5:
        return tone(p["fin"], face), None
    c = p["blue_light"] if face == "up" else p["blue"]
    return tone(c, face), None


def build() -> Model:
    m = Model("minnolith")
    top = m.bone("minnolith", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0, 4, 4, 0.6, 7.6, bodyf, cut=1.6)                    # ball body
    m.round_box(bd, 0, 0, 3.4, 3.4, 0, 8.2, bodyf, cut=1.4)
    m.box(bd, -1, 0.2, -4.6, 1, 1.2, -3.8, bodyf)                             # little chin
    hd = m.bone("head", bd, (0, 8, -1))
    for sx in (-1, 1):                                                       # two upright ear-like fins
        m.box(hd, sx * 1.6 - 0.5, 7.5, -2.2, sx * 1.6 + 0.5, 12, 0.2, finf,
              rotation=(-10, 0, sx * -14), pivot=(sx * 1.6, 7.8, -1))
    tl = m.bone("tail", bd, (0, 5, 3.5))
    m.box(tl, -0.5, 6.5, 1, 0.5, 10.5, 3.5, finf, rotation=(-28, 0, 0), pivot=(0, 7.5, 2))   # third fin behind
    for i, (dy, ln) in enumerate(((5.5, 3), (4, 3.6), (2.5, 3))):           # fan of little tail fins
        rod(m, tl, (0, dy, 3.6), (0, dy + (i - 1) * 1.4, 3.6 + ln), 1.6, finf, extend=0.5, t2=0.6)
    for sx in (-1, 1):
        rod(m, bd, (sx * 3.8, 2.5, -0.5), (sx * 5.5, 1.5, 0.8), 1.6, finf, extend=0.3, t2=0.6)   # side fins
    return m
