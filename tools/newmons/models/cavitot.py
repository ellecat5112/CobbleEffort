"""Cavitot, the Cavity Pokémon (Dark), hand-built from boxes from the user's design.

A single molar about 2'2" tall: a cream crown with four lumpy cusps, the front-right one rotted through into a black
cavity, pale pink diamond eyes with blush and an open, jagged frown; it stands on two stubby roots that go pink
towards their tips.

Front is -z, y is up. 18 units tall; baseScale 0.59 (0.66 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix
from _teeth import P, blush, enamel, root, sad_face

SCALE = 0.59
HITBOX = [0.55, 0.7]
KIND = "biped"
K = 4                                   # texels per model unit
LOOK = ("a single cream molar with a rotten black cavity in its top, pale pink diamond eyes, blush and a jagged "
        "frown, standing on two stubby roots")

CAV = (3.0, -2.5)                       # the cavity's centre (x, z) on top of the front-right cusp
EY, MY = 12.2, 8.4                      # eye and mouth heights on the front face


def crown(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north" and z < -4.9:
        f = sad_face(x, y, pal, EY, MY)
        if f:
            return f
    col = enamel(pal, x, y, z, face, groove=0.0)
    if face == "north" and z < -4.9:
        col = mix(col, pal["blush"], 0.8 * blush(x, y, EY, ex=2.1))
    if y < 6.6:                                            # the neck darkens to pink where the roots start
        col = mix(col, pal["gum"], (6.6 - y) / 1.8 * 0.7)
    d = math.hypot(x - CAV[0], z - CAV[1])                 # rot spreading from the cavity
    if y > 13 and d < 3.4:
        col = mix(col, pal["stain"], (1 - d / 3.4) * (0.4 + 0.2 * (y - 13) / 3))
    if face in ("east", "west") and 9 < y < 12 and abs(z) < 2.6 and abs(z - 0.4 * (y - 10.5)) < 0.15:
        col = mix(col, pal["line"], 0.5)                   # a little crack
    return col


def cusp(x, y, z, face, variant, **k):
    pal = P(variant)
    col = enamel(pal, x, y, z, face)
    d = math.hypot(x - CAV[0], z - CAV[1])
    if d < 1.15:
        return pal["cavity"]
    if d < 1.9:
        return mix(pal["cavity_rim"], pal["cavity"], (y - 16) / 2 * 0.6)
    if d < 3.0:
        return mix(col, pal["stain"], (3.0 - d) / 1.1 * 0.8)
    return col


def roots(x, y, z, face, variant, **k):
    return root(P(variant), y, 3.2)


def build() -> Model:
    m = Model("cavitot")
    top = m.bone("cavitot", None, (0, 0, 0))
    body = m.bone("body", top, (0, 6, 0))
    m.round_box(body, 0, 0, 6, 5, 5, 16, crown, cut=2)
    cx0, cx1, cz0, cz1 = 1, 5, -4.5, -0.5                  # the rotten cusp: a rim round the hole
    for x0, z0, x1, z1 in ((cx0, cz0, cx0 + 1, cz1), (cx1 - 1, cz0, cx1, cz1),
                           (cx0 + 1, cz0, cx1 - 1, cz0 + 1), (cx0 + 1, cz1 - 1, cx1 - 1, cz1)):
        m.box(body, x0, 16, z0, x1, 18, z1, cusp)
    m.box(body, cx0 + 1, 15.5, cz0 + 1, cx1 - 1, 16.5, cz1 - 1, cusp)   # the hole's floor, sunk into the crown
    for x0, z0 in ((-5, -4.5), (-5, 0.5), (1, 0.5)):
        m.box(body, x0, 16, z0, x0 + 4, 18, z0 + 4, cusp)
    for sgn, nm in ((1, "leg_left"), (-1, "leg_right")):
        leg = m.bone(nm, top, (sgn * 2.5, 6, 0))
        m.box(leg, sgn * 2.5 - 1.5, 2, -1.5, sgn * 2.5 + 1.5, 6, 1.5, roots)
        m.box(leg, sgn * 2.5 - 1, 0, -1, sgn * 2.5 + 1, 2, 1, roots)
    return m
