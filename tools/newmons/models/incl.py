"""Incl, the Ink Blot Pokémon (Water/Steel): a small blob of ink with a calligraphy pen nib for a face. A glossy
purple-black teardrop of ink with two glowing yellow eyes, a little droplet floating above its tip, and a silver nib,
point down, below its eyes like a face and chin.

Front is -z, y is up. 14 units tall; baseScale 0.5 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _ink import P, eyef, inkf, nibf

SCALE = 0.5
HITBOX = [0.5, 0.5]
KIND = "floater"
K = 6
HEIGHT = 14
LOOK = "a small glossy blob of ink with glowing yellow eyes and a silver calligraphy pen nib for a face"


def build() -> Model:
    m = Model("incl")
    top = m.bone("incl", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 3.4, 3.2, 5.5, 10.5, inkf, cut=1.2)                    # the ink blob
    m.round_box(bd, 0, 0, 2.2, 2.0, 10.2, 12, inkf, cut=0.8)                    # its teardrop tip
    m.box(bd, -0.5, 13, -0.5, 0.5, 14, 0.5, inkf)                                 # a droplet floating above
    hd = m.bone("head", bd, (0, 6, -3))
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.7, 6.6, -3.35, sx * 1.4 + 0.7, 7.8, -3.1, eyef)    # glowing eyes
    m.box(hd, -3, 0.5, -3.4, 3, 7, -3.4, nibf(0, 0.5, 6, 6.5, tip_up=False))  # pen-nib face, point down
    return m
