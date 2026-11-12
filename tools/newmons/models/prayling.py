"""Prayling, the Blind Mantis Pokémon (Grass/Bug), hand-built from boxes from the user's design.

A tiny baby praying mantis in leaf green: a wide triangular head with no eyes at all (a smooth brown band where they
would be) and a little mouth, two leafy feelers, small forelegs folded together as if praying, four thin legs, and a
round abdomen with a brown band ending in a fan of leaves.

Front is -z, y is up. 17.5 units tall to its feelers; baseScale 0.37 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, mix, rod
from _mantis import P, chitin, frond, striped

SCALE = 0.37
HITBOX = [0.45, 0.45]
KIND = "quadruped"
K = 6
LOOK = ("a tiny leaf-green baby mantis with no eyes, a wide triangular head, leafy feelers, little forelegs folded "
        "as if praying, four thin legs and a fan of leaves for a tail")


def headf(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north":
        if 12.0 < y < 13.0:                                       # where eyes would be: a smooth brown band
            return pal["brown"], None
        if abs(y - 10.4) < 0.18 and abs(x) < 0.9 - 0.4 * abs(x):  # a small mouth
            return pal["green_dark"], None
    return chitin(x, y, z, face, variant)


def abdomen(x, y, z, face, variant, **k):
    pal = P(variant)
    if 3.5 < z < 5.0:
        return pal["brown"], None
    c, g = chitin(x, y, z, face, variant)
    return mix(c, pal["green_light"], 0.15 if y > 6.5 else 0), g


def build() -> Model:
    m = Model("prayling")
    top = m.bone("prayling", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.box(bd, -1.5, 5, -1.5, 1.5, 10, 1.5, chitin)                       # thorax, upright
    tail = m.bone("tail", bd, (0, 6, 1.5))
    m.round_box(tail, 0, 4.5, 2.5, 3.5, 4, 8, abdomen, cut=1)
    m.box(tail, -3.5, 6.5, 7, 3.5, 6.5, 14, frond((0, 7.5), (-35, 0, 35), 6.0, 1.3), rotation=(-30, 0, 0), pivot=(0, 6.5, 7.5))
    hd = m.bone("head", bd, (0, 10, -0.5))
    m.box(hd, -3, 11, -2.5, 3, 14, 0.5, headf)
    m.box(hd, -2, 9.5, -2.2, 2, 11.5, 0.2, headf)
    feeler = striped("green", stripes=(), tip=None)
    for sx in (-1, 1):
        chain(m, hd, [(sx * 1, 13.6, -1), (sx * 2.5, 16.3, -2), (sx * 4, 17.3, -0.5)], [1, 1], feeler)
    arm_s = striped("green", stripes=(0.55,), width=0.1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, bd, (sx * 1.5, 9.5, -1.5))
        rod(m, arm, (sx * 1.5, 9.5, -1.5), (sx * 2.1, 7, -3.6), 1.2, arm_s)
        rod(m, arm, (sx * 2.1, 7, -3.6), (sx * 1.1, 10, -4.6), 1.2, striped("green", stripes=(0.45,), width=0.1, tip=0.8))
    leg_s = striped("green_dark", stripes=())
    for nm, hip, foot in (("leg_front_left", (-1.3, 6, -0.8), (-4, 0.5, -2.6)), ("leg_front_right", (1.3, 6, -0.8), (4, 0.5, -2.6)),
                          ("leg_back_left", (-1.3, 6, 1.2), (-4.5, 0.5, 4.5)), ("leg_back_right", (1.3, 6, 1.2), (4.5, 0.5, 4.5))):
        leg = m.bone(nm, top, hip)
        knee = (hip[0] * 2.4, 7.0, (hip[2] + foot[2]) / 2)
        rod(m, leg, hip, knee, 1, leg_s)
        rod(m, leg, knee, foot, 1, leg_s)
    return m
