"""Tikilla, the Tiki Brawler Pokémon (Normal/Fighting), built from boxes after the user's idea and the concept art they
shared: Tikimp grown into a big kickboxing ape.

A powerful ape in a fighting stance: a huge white shaggy mane sweeping back over its shoulders, a black head with a
white skull face, glaring red-ringed eyes and a golden grin, a black-and-white body with bone stripes and white
shoulder plates, arms banded black, white and gold ending in enormous white fists carved like tiki masks (red carved
faces, gold knuckles), and long legs with gold knee and ankle joints and big clawed feet.

Front is -z, y is up. 34 units tall; baseScale 0.95 (2.0 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _tiki import P, banded, ribs, skull_face, solid, tiki_fist

SCALE = 0.95
HITBOX = [1.2, 2.0]
KIND = "biped"
K = 4
HEIGHT = 34
LOOK = ("a powerful ape with a huge white shaggy mane, a white skull face with a golden grin, bone stripes and enormous "
        "white fists carved like tiki masks")


def body(x, y, z, face, variant, **k):
    return ribs(x, y, z, face, variant, y0=15, y1=21)


def build() -> Model:
    m = Model("tikilla")
    top = m.bone("tikilla", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0.5, 4.5, 3.5, 13, 24, body, cut=1.5)
    for sx in (-1, 1):                                                            # white shoulder plates
        m.round_box(bd, sx * 5, 0, 2, 2, 21, 25, solid("white"), cut=0.6)
    hd = m.bone("head", bd, (0, 24, -1))
    m.round_box(hd, 0, -1.5, 3, 2.8, 23.5, 29.5, skull_face(27, 1.3, 0.9, 1.6), cut=1)
    for dx in (-2, 0, 2):                                                         # a crest of black hair
        spike(m, hd, (dx, 29.2, -1.5), (dx * 0.3, 1, -0.2), 1.6, 2.5, solid("black"), tip=0.8)
    mane = m.bone("mane", bd, (0, 26, 2))                                         # the huge white shaggy mane
    for i in range(13):
        a = -1.2 + i * 0.2
        base = (math.sin(a) * 3.5, 26 + math.cos(a) * 1.5, 2.5)
        spike(m, mane, base, (math.sin(a) * 1.6, 0.9 - abs(a) * 0.4, 1.0), 3.5, 7 + 2 * math.cos(a), solid("mane"), tip=1.5)
    for i in range(6):
        a = -1.0 + i * 0.4
        spike(m, mane, (math.sin(a) * 4, 21, 3.5), (math.sin(a) * 1.2, -0.6, 1.0), 3, 6, solid("mane_shade"), tip=1.2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                           # banded arms, tiki-mask fists
        a = m.bone(nm, bd, (sx * 5, 23, 0))
        rod(m, a, (sx * 5, 23, 0), (sx * 8, 18.5, -2), 2.2, banded("black", "white"))
        rod(m, a, (sx * 8, 18.5, -2), (sx * 9.5, 14.5, -5), 2, banded("black", "gold"))
        m.round_box(a, sx * 10, -6.5, 2.6, 1.5, 9.5, 17, tiki_fist(sx * 10, 13, -8), cut=1)
        for dx in (-1.4, -0.45, 0.45, 1.4):                                      # gold knuckles
            m.box(a, sx * 10 + dx - 0.4, 8.6, -7.4, sx * 10 + dx + 0.4, 9.8, -5.8, solid("gold"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                           # long legs, gold joints
        lg = m.bone(nm, top, (sx * 2.6, 13.5, 0.5))
        rod(m, lg, (sx * 2.6, 13.5, 0.5), (sx * 4.2, 7.5, -1.2), 2.6, solid("black"))
        m.round_box(lg, sx * 4.2, -1.2, 1.4, 1.4, 6.6, 8.6, solid("gold"), cut=0.5)
        rod(m, lg, (sx * 4.2, 7.5, -1.2), (sx * 4.4, 1.6, 0), 2.2, banded("white", "black"))
        m.round_box(lg, sx * 4.4, 0, 1.2, 1.2, 1.2, 2.6, solid("gold"), cut=0.4)
        m.box(lg, sx * 4.4 - 1.6, 0, -2.6, sx * 4.4 + 1.6, 1.4, 1.6, solid("white"))
        for dx in (-1, 0, 1):
            m.box(lg, sx * 4.4 + dx - 0.4, 0, -3.6, sx * 4.4 + dx + 0.4, 1, -2.6, solid("gold"))
    return m
