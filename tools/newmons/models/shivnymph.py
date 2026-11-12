"""Shivnymph, the Shiv Nymph Pokémon (Bug/Steel), a route-one Pokémon, hand-built from boxes from the user's design.

A baby dragonfly nymph, teal on top and brown underneath, with two big orange eyes, two thin feelers, stubby wing buds
and six spindly legs; its tail ends in a little kitchen knife: a black riveted handle and a shiny steel blade held up
behind it.

Front is -z, y is up. 13 units tall to its blade; baseScale 0.42 (0.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _knife import P, blade_plane, body, eyes, handle
from _route import tone

SCALE = 0.42
HITBOX = [0.4, 0.35]
KIND = "quadruped"
K = 6
LOOK = ("a baby teal-and-brown dragonfly nymph with big orange eyes, stubby wing buds, six spindly legs and a little "
        "kitchen knife for a tail")


def legf(x, y, z, face, variant, **k):
    return tone(P(variant)["brown"], face), None


def build() -> Model:
    m = Model("shivnymph")
    top = m.bone("shivnymph", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3.5, 0))
    m.round_box(bd, 0, 0, 2.5, 2.5, 2.5, 6.5, body, cut=1)                # thorax
    tail = m.bone("tail", bd, (0, 4.5, 2.5))
    m.round_box(tail, 0, 4.5, 2, 2.5, 2.8, 6, body, cut=1)                # abdomen
    m.box(tail, -1, 3.4, 7, 1, 5.4, 9.5, handle)                            # the knife's handle
    m.box(tail, 0, 3.5, 9, 0, 7, 16, blade_plane(4.0, 6.6, 15.8, 9.0, axes="zy"),
          rotation=(-28, 0, 0), pivot=(0, 4.4, 9))                          # its blade, tilted up behind
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 0.5, sx * 3.5))
        m.box(bd, x0, 6.2, -0.5, x1, 7.2, 2.5, body)                       # wing buds
    hd = m.bone("head", bd, (0, 5, -2))
    m.round_box(hd, 0, -3.5, 3, 2, 3, 7, eyes(0, 5.3, 1.3, 1.5), cut=1)
    for sx in (-1, 1):
        chain(m, hd, [(sx * 0.8, 6.8, -4.5), (sx * 1.6, 9, -5.4), (sx * 2.4, 10.4, -4.8)], [0.6, 0.6], legf)
    legs = [("leg_front_left", -2, -1.5), ("leg_front_right", 2, -1.5), ("leg_mid_left", -2.2, 0),
            ("leg_mid_right", 2.2, 0), ("leg_back_left", -2.2, 1.5), ("leg_back_right", 2.2, 1.5)]
    for nm, lx, lz in legs:
        sx = 1 if lx > 0 else -1
        leg = m.bone(nm, top, (lx, 3.5, lz))
        knee = (lx + sx * 2.2, 4.8, lz * 1.5)
        rod(m, leg, (lx, 3.5, lz), knee, 0.8, legf)
        rod(m, leg, knee, (lx + sx * 3.5, 0.2, lz * 2.2), 0.8, legf)
    return m
