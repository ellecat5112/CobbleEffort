"""Rubraptor, the Red Hawk Pokémon (Fairy/Flying), hand-built from boxes from the user's design.

Cardling grown into a proud red-winged hawk standing tall: a crested red head with a black mask, a hooked grey beak and
a fierce glare, a white breast, folded red wings dotted with white ovals, two long forked tail streamers banded with
pale gold, and strong grey legs with talons.

Front is -z, y is up. 30 units tall to its crest; baseScale 0.62 (1.1 m), its tail streamers reaching far behind.
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _cardinal import P, feather, grey, plumage
from _route import tone

SCALE = 0.62
HITBOX = [0.8, 1.1]
KIND = "biped"
K = 4
LOOK = ("a proud red-winged hawk with a crest, a black mask, a hooked grey beak, a fierce glare, a white breast, "
        "white-spotted wings and two long forked tail streamers banded with gold")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.7, y - 23.6
            if (dx / 0.9) ** 2 + (dy / 0.7) ** 2 < 1:
                if dy > 0.25 - 0.4 * (abs(x) - 1.7):                         # the fierce brow
                    return p["mask"], None
                return ((255, 255, 255) if dx * sx > 0.3 else (30, 26, 30)), None
        if abs(x) < 2.6 and 21.0 < y < 24.0:
            return p["mask"], None
    return plumage()(x, y, z, face, variant)


def build() -> Model:
    m = Model("rubraptor")
    top = m.bone("rubraptor", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 4.5, 4, 9, 19, plumage(belly=17.5), cut=2)       # upright body, white breast
    hd = m.bone("head", bd, (0, 19, -0.5))
    m.round_box(hd, 0, -1, 3.5, 3, 19, 26, headf, cut=1)
    chain(m, hd, [(0, 24.2, -4), (0, 23, -6), (0, 21.6, -6.2)], [1.6, 1.0], grey)           # hooked beak
    chain(m, hd, [(0, 25.5, 0), (0, 28, 1.6), (0, 29.6, 4)], [2, 1.2], plumage())           # the crest
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 4.5, 18, 0))
        x0, x1 = sorted((sx * 4, sx * 5.5))
        m.box(w, x0, 9.5, -3, x1, 18.5, 7, plumage(spots=((sx * 5.2, 15.5, -0.5, 1.3), (sx * 5.2, 13.5, 2.0, 1.0),
                                                            (sx * 5.2, 11.8, 4.2, 0.8))))
    tail = m.bone("tail", bd, (0, 11, 3.5))
    for sx in (-1, 1):                                                         # two long forked streamers
        m.box(tail, sx * 1.0, 9.5, 3.5, sx * 1.0, 11.5, 24, feather(stripes=(16, 17.6, 21)),
              rotation=(-14, sx * 8, 0), pivot=(sx * 1.0, 10.5, 3.5))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2, 10, 0))
        rod(m, lg, (sx * 2, 10, 0), (sx * 2.2, 0.8, -0.5), 2, grey)
        m.box(lg, sx * 2 - 1.5, 5.5, -1.5, sx * 2 + 1.5, 10, 1.5, plumage())   # feathered thighs
        for dx, dz in ((-0.8, -2.2), (0.8, -2.2), (0, 1.0)):                   # talons
            rod(m, lg, (sx * 2.2, 0.6, -0.5), (sx * 2.2 + dx, 0.2, dz - 0.5), 0.7, grey)
    return m
