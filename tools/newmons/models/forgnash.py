"""Forgnash, the Forge Shark Pokémon (Steel/Fire), built from boxes from the user's design.

Sharkindle standing up on two legs: a round dark-grey shark head and body in one, a huge grin full of teeth, glowing
orange eyes and two grey horns, a tall yellow-orange crest fin on top and more orange fins sweeping back from its
shoulders, flames exploding from its back, huge powerful red claws tipped with white, red-and-black legs, and a short
shark tail.

Front is -z, y is up. 26 units tall to its flames; baseScale 0.86 (1.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod, spike
from _landshark import P, fin, flame, solid, teeth_band
from _route import tone

SCALE = 0.86
HITBOX = [1.0, 1.4]
KIND = "biped"
K = 4
HEIGHT = 26
LOOK = ("a standing land shark with a huge toothy grin, glowing orange eyes, horns, orange fins, flames exploding from "
        "its back and huge red claws")

TEETH = teeth_band(14.4, 12.6, 0.9)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 2.4, y - 16.6
            if (dx / 1.1) ** 2 + (dy / 0.9) ** 2 < 1:
                if (dx / 0.45) ** 2 + (dy / 0.6) ** 2 < 1:
                    return (24, 20, 20), None
                return p["orange"], p["orange"]                         # glowing orange eyes
        if abs(x) < 4.6 - 0.15 * (y - 13.5) ** 2 and 11.6 < y < 15.2:
            return (p["tooth"] if TEETH(x, y) or TEETH(x + 0.45, 26.0 - y) else (70, 14, 20)), None   # the grin
    if face in ("north", "down") and y < 11.5:
        return tone(p["black"], face), (p["orange"] if abs((y % 1.6) - 0.8) < 0.12 else None)   # banded belly
    return tone(p["grey"] if y > 13 else p["black"], face), None


def claw(x, y, z, face, variant, **k):
    return tone(P(variant)["claw"], face), None


def build() -> Model:
    m = Model("forgnash")
    top = m.bone("forgnash", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0, 6, 5, 8, 21, bodyf, cut=2)                      # head and body in one
    hd = m.bone("head", bd, (0, 18, 0))
    for sx in (-1, 1):                                                      # horns
        spike(m, hd, (sx * 3.6, 20.5, -1.5), (sx * 0.5, 1, 0.1), 2, 4, solid("grey"), tip=1)
    m.box(hd, 0, 20.5, -2, 0, 27, 5, fin([(-2, 20.5), (1.5, 26.5), (5, 20.5)], "zy", "yellow"))    # crest fin
    m.box(bd, -6, 15, 5, 6, 26, 5, flame("xy", 15, [(-4.5, 8), (-1.5, 10.5), (1.5, 9.5), (4.5, 7.5)], 3.6))  # flames
    for sx in (-1, 1):                                                      # fins sweeping back from its shoulders
        m.box(bd, sx * 5.8, 10, -1, sx * 5.8, 21, 9, fin([(-1, 20), (9, 11), (3, 10), (0, 14)], "zy"),
              rotation=(0, sx * -20, 0), pivot=(sx * 5.8, 15, -1))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                   # huge powerful claws
        a = m.bone(nm, bd, (sx * 6, 16, 0))
        rod(m, a, (sx * 6, 16, 0), (sx * 8, 12.5, -2), 2.5, solid("red"))
        m.round_box(a, sx * 8.6, -3.5, 2.6, 2.4, 8.5, 13, solid("red"), cut=1)
        for dx in (-1.2, 0, 1.2):
            rod(m, a, (sx * 8.6 + dx, 9, -5.5), (sx * 8.6 + dx, 7.6, -7.4), 1, claw)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3, 9, 1))
        m.round_box(lg, sx * 3, 1, 2.2, 2.2, 4, 9.5, solid("red"), cut=1)
        m.box(lg, sx * 3 - 1.6, 0, -1.5, sx * 3 + 1.6, 4.5, 2.5, solid("black"))
        for dx in (-1, 1):
            m.box(lg, sx * 3 + dx - 0.5, 0, -2.5, sx * 3 + dx + 0.5, 1, -1.5, claw)
    tail = m.bone("tail", bd, (0, 10, 4.5))
    chain(m, tail, [(0, 10, 4.5), (0, 8.5, 9)], [3], solid("grey"))
    m.box(tail, 0, 4, 8, 0, 14, 13, fin([(8.5, 8.5), (12.5, 13), (11, 8.6), (12.5, 4.5)], "zy", "grey", False))
    return m
