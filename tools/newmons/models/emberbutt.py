"""Emberbutt, the Smoulder Pokémon (Fire), the Nicodex's Fire type (the user's design): a little cylindrical creature
like a smouldering cigarette butt: papery white armour, an orange filter rear, a ring of ash and a glowing orange ember
for a nose trailing smoke, with beady eyes and four stubby legs.

Shiny: a black paper body with a blue ember.

Front is -z, y is up. 10 units tall; baseScale 0.42 (0.27 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _nico import palette, puff, translucent, tube_z
from _route import tone

SHINY = {"paper": (60, 60, 68), "paper_shade": (44, 44, 52), "ember": (80, 160, 255), "ember_hot": (180, 230, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.42
HITBOX = [0.6, 0.62]
KIND = "quadruped"
K = 6
HEIGHT = 10
LOOK = "a little cigarette-butt creature: papery white body, orange filter rear, an ash ring and a glowing ember nose"


def emberf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["ember_hot"] if face == "north" and (abs(x) + abs(y - 4.6)) < 1.4 else p["ember"]
    return c, c


def build() -> Model:
    m = Model("emberbutt")
    top = m.bone("emberbutt", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4.6, 0))
    tube_z(m, bd, 0, 4.6, 3.0, 2.6, 8.0, solid("filter"))                       # the filter
    tube_z(m, bd, 0, 4.6, 3.0, -5.6, 2.6, solid("paper"))                       # papery armour
    tube_z(m, bd, 0, 4.6, 3.0, -6.6, -5.6, solid("ash"))                        # the ash ring
    hd = m.bone("head", bd, (0, 4.6, -6))
    tube_z(m, hd, 0, 4.6, 2.0, -7.8, -6.4, emberf)                              # the glowing ember nose
    for sx in (-1, 1):
        m.box(hd, sx * 1.6 - 0.6, 6.6, -5.4, sx * 1.6 + 0.6, 7.8, -4.4, solid("pupil"))   # beady eyes
    puff(m, hd, (0.6, 9.0, -7.6), 1.0, translucent(P, "smoke"))                 # a wisp of smoke
    puff(m, hd, (1.2, 11.2, -7.2), 0.8, translucent(P, "smoke"))
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -3.4), ("back", 4.8)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 2.0, 2.2, z))
            m.round_box(lb, sx * 2.0, z, 0.9, 0.9, 0.0, 2.6, solid("paper_shade" if role == "front" else "filter_dark"),
                        cut=0.4)
    return m
