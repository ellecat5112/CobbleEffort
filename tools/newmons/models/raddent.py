"""Raddent, the Radish Rat Pokémon (Grass/Normal), a route-one Pokémon, hand-built from boxes from the user's design.

A rat whose body is a round magenta radish laced with fine green veins: a tan face patch, two little dark eyes, small
round ears, a pointed snout with a dark nose, a white buck tooth and whiskers; it scurries on four stubby feet, and
its leafy radish top sprouts out behind like a tail.

Front is -z, y is up. 13 units tall to its leaves; baseScale 0.42 (0.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _radish import dark, foot, light, nose, radish, snout, tooth, whisker
from _route import leaf_plane

SCALE = 0.42
HITBOX = [1.07, 0.83]
KIND = "quadruped"
K = 5
LOOK = ("a rat whose body is a round magenta radish with green veins, a tan face, a pointed snout, a buck tooth and "
        "whiskers, scurrying on four stubby feet with its leafy top sprouting out behind")


def build() -> Model:
    m = Model("raddent")
    top = m.bone("raddent", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    body = radish("north", 0, 6, 0)
    m.round_box(bd, 0, 0.5, 5, 5.5, 1.5, 10, body, cut=2)
    hd = m.bone("head", bd, (0, 6, -4.5))
    rod(m, hd, (0, 5.2, -4.8), (0, 4.4, -9.4), 2.2, snout)                  # pointed snout
    m.box(hd, -0.7, 3.8, -10.3, 0.7, 5.2, -9.2, nose)
    m.box(hd, -0.5, 3.3, -8.4, 0.5, 4.3, -7.9, tooth)                         # buck tooth
    for sx in (-1, 1):
        for dy in (0.4, -0.3):                                                # whiskers
            rod(m, hd, (sx * 1.0, 4.6 + dy, -8.4), (sx * 4.2, 4.9 + dy * 2, -8.0), 0.3, whisker)
        m.box(hd, sx * 2.8 - 1.2, 9.2, -3.1, sx * 2.8 + 1.2, 11.2, -2.1, body)   # little round ears
    tail = m.bone("tail", bd, (0, 7, 5))
    m.box(tail, 0, 5, 4.5, 0, 13, 12, leaf_plane((6.0, 5.5), (10, 35, 60), 6.5, 1.5, light, dark, axes="zy"))
    m.box(tail, -4, 5, 4.5, 4, 13, 4.5, leaf_plane((0, 5.5), (-35, 0, 35), 6.5, 1.5, light, dark, axes="xy"))
    for nm, (lx, lz) in (("leg_front_left", (-2.5, -2.5)), ("leg_front_right", (2.5, -2.5)),
                         ("leg_back_left", (-2.5, 3)), ("leg_back_right", (2.5, 3))):
        leg = m.bone(nm, top, (lx, 2, lz))
        m.box(leg, lx - 1, 0, lz - 1.5, lx + 1, 2, lz + 1, foot)
    return m
