"""Cardling, the Cardinal Pokémon (Fairy/Flying), a route-one Pokémon, hand-built from boxes from the user's design.

A cute little round cardinal: a ball of red plumage with a pointed crest, a stubby grey beak in a small black mask, big
shiny black eyes with pink blush beneath, a white belly, white oval spots on its little wings, a short tail and thin
grey legs.

Front is -z, y is up. 12 units tall to its crest; baseScale 0.42 (0.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _cardinal import P, feather, grey, plumage
from _route import dot_eye, tone

SCALE = 0.42
HITBOX = [0.95, 0.83]
KIND = "biped"
K = 6
LOOK = ("a cute round red cardinal with a pointed crest, a stubby grey beak in a little black mask, big shiny eyes, "
        "pink blush, a white belly and white spots on its wings")


def headbody(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = dot_eye(x - sx * 2.1, y - 8.5, 0.7, 0.9)
            if e:
                return e
            if ((x - sx * 2.7) / 0.8) ** 2 + ((y - 7.0) / 0.4) ** 2 < 1:
                return p["blush"], None
        if abs(x) < 1.1 - 0.25 * (y - 5.6) and 5.4 < y < 7.0:
            return p["mask"], None
    return plumage(belly=5.0)(x, y, z, face, variant)


def build() -> Model:
    m = Model("cardling")
    top = m.bone("cardling", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0, 4, 4, 2, 10, headbody, cut=2)                    # one round red ball
    hd = m.bone("head", bd, (0, 7, -2))
    m.box(hd, -0.75, 6, -5.6, 0.75, 7.2, -4, grey)                          # the beak
    chain(m, hd, [(0, 9.6, -1), (0, 11.2, 0.2), (0, 12, 1.8)], [1.6, 1.0], plumage())   # the crest
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 4, 7, 0))
        x0, x1 = sorted((sx * 3.6, sx * 4.8))
        m.box(w, x0, 3.5, -1.5, x1, 7.5, 3, plumage(spots=((sx * 4.5, 5.0, 0.6, 0.9), (sx * 4.5, 4.4, 1.9, 0.6))))
    m.box(bd, -1.5, 4, 3.5, 1.5, 4, 7.5, feather())                         # the tail
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.4, 3, 0))
        rod(m, lg, (sx * 1.4, 3, 0), (sx * 1.4, 0.2, -0.3), 0.6, grey)
        m.box(lg, sx * 1.4 - 0.8, 0, -1.6, sx * 1.4 + 0.8, 0.4, 0.4, grey)
    return m
