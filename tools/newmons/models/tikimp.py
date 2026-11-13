"""Tikimp, the Kickboxing Pokémon (Normal/Fighting), built from boxes after the user's idea and the concept art they
shared: a little kickboxing monkey with skull and tiki looks.

A small black monkey with a crown of spiky black hair, a white skull-like face with red-ringed yellow eyes and a wide
golden grin, white bone stripes down its chest, thin arms ending in huge white mitts with gold fingers and a gold
palm, long legs with white shins and big white feet tipped in gold, and a thin curling tail.

Front is -z, y is up. 18 units tall; baseScale 0.55 (0.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _tiki import P, banded, ribs, skull_face, solid, tiki_fist

SCALE = 0.55
HITBOX = [0.91, 1.09]
KIND = "biped"
K = 5
HEIGHT = 18
LOOK = ("a little black kickboxing monkey with spiky hair, a white skull face with a golden grin, bone stripes and "
        "huge white mitt hands and feet tipped in gold")


def body(x, y, z, face, variant, **k):
    return ribs(x, y, z, face, variant, y0=6.5, y1=10.5)


def build() -> Model:
    m = Model("tikimp")
    top = m.bone("tikimp", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 2.5, 2, 6, 11, body, cut=0.8)
    hd = m.bone("head", bd, (0, 11, -0.5))
    m.round_box(hd, 0, -0.5, 3.2, 3, 10.5, 16, skull_face(13.8, 1.3, 0.9, 1.7), cut=1)
    for i, (dx, dz) in enumerate(((-2.4, 0), (-1.2, -1.5), (0, -2), (1.2, -1.5), (2.4, 0), (0, 1.8), (-1.6, 1.4), (1.6, 1.4))):
        spike(m, hd, (dx, 15.6, dz - 0.5), (dx * 0.3, 1, dz * 0.25), 1.6, 2.5, solid("black"), tip=0.8)   # spiky hair
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                          # thin arms, huge white mitts
        a = m.bone(nm, bd, (sx * 2.4, 10, 0))
        rod(m, a, (sx * 2.4, 10, 0), (sx * 5.5, 8.5, -1), 1, solid("black"))
        m.round_box(a, sx * 7, -1.2, 1.6, 1.0, 6.8, 10.4, tiki_fist(sx * 7, 8.6, -2.2, tiki=False), cut=0.5)
        m.box(a, sx * 7 - 0.6, 8.0, -2.4, sx * 7 + 0.6, 9.2, -2.1, solid("gold"))  # the gold palm
        for dy in (-1.2, 0, 1.2):
            rod(m, a, (sx * 8.3, 8.6 + dy, -1.2), (sx * 9.6, 8.6 + dy * 1.4, -1.2), 0.6, solid("gold"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                          # long legs, big white feet
        lg = m.bone(nm, top, (sx * 1.4, 6.5, 0))
        rod(m, lg, (sx * 1.4, 6.5, 0), (sx * 1.8, 3.2, -0.4), 1.4, solid("black"))
        rod(m, lg, (sx * 1.8, 3.4, -0.4), (sx * 1.8, 1, 0), 1.2, solid("white"))
        m.round_box(lg, sx * 1.8, -1, 1.3, 2.2, 0, 1.4, solid("white"), cut=0.5)
        m.box(lg, sx * 1.8 - 1.2, 0, -3.6, sx * 1.8 + 1.2, 1.2, -2.8, solid("gold"))   # gold toes
    tail = m.bone("tail", bd, (0, 7, 2))
    pts = [(0, 7, 2)] + [(math.sin(a) * 1.8, 7 + a * 1.2, 3 + math.cos(a) * 2.2) for a in (0.6, 1.4, 2.2, 3.0, 3.8)]
    chain(m, tail, pts, [0.8] * (len(pts) - 1), solid("black"))
    return m
