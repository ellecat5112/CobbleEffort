"""Clippers Rotom (Electric/Steel), after the user's Rotom doodle sheet (artist not named): Rotom inside a pair of
electric hair clippers. A tall rounded orange body with a worried face (lens eyes, a wobbly mouth), a silver comb
blade with fine teeth on top, and a black cord trailing from its base to a plug; blue plasma crackles round it.

Front is -z, y is up. 24 units tall; about 0.9 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import bolt_plane, face_on, palette, solid
from _route import tone

P = palette({"aura": (90, 160, 240), "aura_light": (200, 230, 255), "iris": (110, 190, 236)})
HEIGHT = 24
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.7, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "tall orange hair clippers with a worried face, a silver comb blade and a black cord"


def blade(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south") and y > 22.6 and int((x + 4) * 2) % 2 == 0:
        return p["grey_dark"], None                          # fine comb teeth
    return tone(p["grey_light"], face), None


def build() -> Model:
    m = Model("rotom_clippers")
    top = m.bone("rotom_clippers", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 3.8, 2.8, 2, 20.5, face_on(P, (0, 13, -2.8), eyes=[(-1.5, 1.4, 1.3), (1.5, 1.4, 1.3)],
                                                     mouth=(0, -1.5, 2.2, 0.8, 3)), cut=1.2)     # the body
    m.box(bd, -4, 20.5, -2.2, 4, 23.5, 2.2, blade)                                               # comb blade
    cord = m.bone("tail", bd, (0, 2, 0))
    pts = [(0, 2.5, 0), (0, -0.5, 1), (-2, -1.5, 5), (1, -1, 9), (4, -1.5, 12)]
    for a, b in zip(pts, pts[1:]):
        rod(m, cord, a, b, 1.1, solid(P, "black"), extend=0.5)
    m.box(cord, 3, -3, 12, 6, 0, 14, solid(P, "charcoal"))                                       # the plug
    for x, y, z, w, h, pl, fl in [(-8, 14, -1, 4, 7, "xy", False), (5, 8, -1, 4, 6, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
