"""Wrapiglet, the Snug Piglet Pokémon (Normal), the first stage of the pigs-in-a-blanket line: a round pink piglet
wrapped snugly in a crescent roll of golden layered dough, its head poking out of the top with a little upturned
snout and its trotters resting on the dough, its pink feet peeking out underneath.

Front is -z, y is up. 16 units tall; baseScale 0.6 (0.6 m).
"""
from __future__ import annotations

import math

from _blanket import P, dough_shade, hooff, layers, snoutf
from _boxmodel import Model, mix, rod
from _route import tone

SCALE = 0.6
HITBOX = [0.6, 0.6]
KIND = "biped"
K = 6
HEIGHT = 16
LOOK = "a round pink piglet wrapped snugly in a golden crescent roll of dough, its head poking out of the top"


def rollf(x, y, z, face, variant, **k):
    """The roll's layers run round it horizontally, wrapping diagonally a little across the front."""
    p = P(variant)
    t = layers(y + (0.18 * x if face == "north" else 0) + (0.3 * z if face in ("east", "west") else 0))
    if face == "north" and abs(y - 6.2 - 0.25 * x) < 0.45 and x > -2.5:
        return tone(p["crumb"], face), None                             # the tucked end of the roll
    return dough_shade(p, t, face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot((x - sx * 1.5) / 0.38, (y - 14.0) / 0.45) < 1:
                return p["eye"], None
    c = p["pig"] if face != "down" else p["pig_dark"]
    return tone(c, face), None


def build() -> Model:
    m = Model("wrapiglet")
    top = m.bone("wrapiglet", None, (0, 0, 0))
    for nm, lx in (("leg_left", -2.2), ("leg_right", 2.2)):
        lg = m.bone(nm, top, (lx, 2, 0))
        m.box(lg, lx - 1.2, 0, -1.8, lx + 1.2, 2.2, 0.8, hooff)              # pink feet peeking out
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 5, 4, 1.5, 11.5, rollf, cut=1.6)                     # the crescent roll
    m.round_box(bd, 0.6, 0, 5.4, 4.4, 4.5, 8.5, rollf, cut=1.7)                # its thick middle layer
    hd = m.bone("head", bd, (0, 11, 0))
    m.round_box(hd, 0, 0.2, 3.8, 3.2, 10.5, 16, headf, cut=1.3)                # pink head on top
    m.box(hd, -1.7, 12.2, -3.8, 1.7, 14.4, -2.8, snoutf(0, 13.3, 3.4, 2.2))    # upturned snout
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.2, sx * 3.6), 15.4, -1.2, max(sx * 2.2, sx * 3.6), 16.8, 0.4, headf,
              rotation=(0, 0, sx * -25), pivot=(sx * 2.2, 15.6, -0.4))         # little ears
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        ar = m.bone(nm, bd, (sx * 3, 11, -2))
        m.box(ar, sx * 3 - 1, 10.4, -4.4, sx * 3 + 1, 12, -2.6, headf)         # trotters resting on the dough
        m.box(ar, sx * 3 - 1, 10.4, -4.6, sx * 3 + 1, 11, -4.2, hooff)
    return m
