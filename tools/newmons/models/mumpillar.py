"""Mumpillar, the Swaddled Pokémon (Water/Bug), the CobbleEffort water starter, hand-built from boxes from the user's
design.

A caterpillar swaddled in bandages like a little mummy: a round wrapped head with a black visor face and two big round
glowing yellow eyes, a loose bandage end curling up from the top of its head, and a body of bandaged segments, patched
here and there with blue, rearing up at the front and trailing off behind on stubby black feet.

Front is -z, y is up. 18 units tall to its curl; baseScale 0.4 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain
from _pharaoh import P, bandage, black, ring_eye, visor

SCALE = 0.4
HITBOX = [1.25, 1.12]
KIND = "quadruped"
K = 6
LOOK = ("a caterpillar swaddled in bandages like a little mummy, with a black visor face, two big round glowing yellow "
        "eyes, a bandage curl on its head and blue-patched bandaged segments on stubby black feet")

SEGMENTS = [(-3.5, 3.5, 3, 2, 7.5), (0.5, 3.5, 3, 1, 6), (4, 3, 2.5, 1, 5.5), (7, 2.5, 2, 1, 5), (9.5, 1.5, 1.5, 1.5, 4)]


def headf(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = ring_eye(x - sx * 1.6, y - 10.8, 1.25, variant)
            if e:
                return e
        if visor(x, y - 10.5, 3.4, 2.3):
            return pal["black"], None
        if abs(x) < 0.7 and 8.0 < y < 8.6:                    # a little blue mouth
            return pal["mouth"], None
    return bandage(x, y, z, face, variant, patches=False)


def build() -> Model:
    m = Model("mumpillar")
    top = m.bone("mumpillar", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    tail = m.bone("tail", bd, (0, 4, 1))
    for i, (cz, rx, rz, y0, y1) in enumerate(SEGMENTS):
        m.round_box(bd if i < 2 else tail, 0, cz, rx, rz, y0, y1, bandage, cut=1)
    hd = m.bone("head", bd, (0, 7.5, -3))
    m.round_box(hd, 0, -3.5, 4, 3.5, 7, 14, headf, cut=1)
    chain(m, hd, [(0, 13.6, -3.5), (0.6, 15.8, -3.8), (1.8, 17, -2.8), (1.4, 17.6, -1.2)], [1.2, 1, 1],
          lambda *a, **k: bandage(*a, patches=False, **k))
    feet = [("leg_front_left", -2.6, -3.5), ("leg_front_right", 2.6, -3.5), ("leg_back_left", -2.6, 3.5),
            ("leg_back_right", 2.6, 3.5)]
    for nm, fx, fz in feet:
        leg = m.bone(nm, top, (fx, 1.5, fz))
        m.box(leg, fx - 1, 0, fz - 1, fx + 1, 1.5, fz + 1, black)
    return m
