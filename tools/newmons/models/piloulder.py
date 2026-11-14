"""Piloulder, the Inukshuk Pokémon (Rock; the user's art, artist not named, name kept), Stackoulder evolved: a towering
stone figure like an inukshuk. Legs of stacked stones stand on a mossy green slab; above it its body is a pile of flat
slabs, tilted this way and that, under a broad slab of shoulders and a small grey head with stern eyes. Two tall
standing stones float beside it as arms.

Front is -z, y is up. 44 units tall; baseScale 0.9 (2.5 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _cairn import P, pebble, solid, stern, stone

SCALE = 0.9
HITBOX = [1.9, 2.6]
KIND = "biped"
K = 3
HEIGHT = 44
ANIM = {"leg_amp": 12}
LOOK = ("a towering inukshuk of stones: stacked stone legs on a mossy slab, a body of tilted flat slabs under a broad "
        "slab of shoulders, a small grey head with stern eyes, and two tall standing stones floating beside it as arms")


def head_face(x, y, z, f, p):
    if f == "north":
        for sx in (-1, 1):
            c = stern(p, x - sx * 1.1, y - 33.6, 0.75, 1.1, sx)
            if c is not None:
                return c
    return None


def build() -> Model:
    m = Model("piloulder")
    top = m.bone("piloulder", None, (0, 0, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                  # legs of stacked stones
        lg = m.bone(nm, top, (sx * 5, 13, 0))
        pebble(m, lg, (sx * 5.2, 0, -0.8), 3.4, 4.0, 3.4, stone("grey", seed=sx))
        pebble(m, lg, (sx * 5, 3.2, 0), 2.6, 2.6, 5.0, stone("grey_dark", seed=1 + sx))
        pebble(m, lg, (sx * 5.3, 8.0, 0), 3.0, 3.0, 4.6, stone("grey", seed=2 + sx))
    bd = m.bone("body", top, (0, 13, 0))
    m.round_box(bd, 0, 0, 6.6, 4.2, 12.2, 15.4, stone("moss", seed=3), cut=1.4)          # the mossy slab
    m.round_box(bd, 0.6, 0.3, 7.8, 5.2, 15.2, 19.2, stone("brown", seed=4), cut=1.8)     # tilted slabs
    m.round_box(bd, -0.5, -0.2, 7.0, 5.0, 19.0, 22.8, stone("grey", seed=5), cut=1.8)
    m.round_box(bd, 0.4, 0.2, 7.6, 5.2, 22.6, 26.0, stone("slate", seed=6), cut=1.8)
    m.round_box(bd, 0, 0, 11.6, 5.6, 25.8, 30.0, stone("brown", seed=7), cut=2.0)       # the broad shoulder slab
    hd = m.bone("head", bd, (0, 30, 0))
    pebble(m, hd, (0, 29.8, -0.4), 2.8, 2.6, 6.0, stone("grey", extra=head_face, seed=8))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                  # two standing stones floating beside it
        a = m.bone(nm, bd, (sx * 14, 26, 0))
        x0, x1 = sorted((sx * 12.8, sx * 17.6))
        m.box(a, x0, 3, -2.4, x1, 26, 2.6, stone("slate", seed=9 + sx), rotation=(0, 0, -sx * 7), pivot=(sx * 14, 26, 0))
        x0, x1 = sorted((sx * 13.4, sx * 17.0))
        m.box(a, x0, 25.6, -1.8, x1, 28, 2.0, stone("grey", seed=11 + sx), rotation=(0, 0, -sx * 7), pivot=(sx * 14, 26, 0))
    return m
