"""Keytar Rotom (Electric/Normal), after the user's Rotom doodle sheet (artist not named): Rotom inside a keytar.
A long orange keyboard body with a row of white and black keys along its top, a slim neck and grip, a black strap,
and Rotom's lens eyes and grin at the body's end; purple notes blare from it.

Front is -z, y is up. 16 units tall, 34 long; about 0.7 blocks tall.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import note_plane, palette, rotom_eye, grin, solid
from _route import tone

P = palette({"aura": (170, 80, 230), "aura_light": (230, 200, 255), "iris": (240, 140, 220)})
HEIGHT = 16
SCALE = round(0.7 * 16 / HEIGHT, 3)
HITBOX = [1.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange keytar with a row of keys, a slim neck and Rotom's lens eyes and grin at its end"


def body(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and -8 <= x <= 9 and -2.4 <= z <= 1.6:   # the keys
        u = (x + 8) % 1.4
        if z < -0.2 and int((x + 8) // 1.4) % 7 not in (2, 6) and u > 0.9:
            return p["black"], None
        return (p["white"] if u > 0.18 else p["grey"]), None
    if face == "north":
        for ex in (-12.6, -9.4):
            e = rotom_eye(x - ex, y - 9.4, 1.3, p)
            if e:
                return e
        g = grin(x + 11, y - 7.0, 3.6, 1.0, p, teeth=4)
        if g:
            return g, None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("rotom_keytar")
    top = m.bone("rotom_keytar", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.box(bd, -15, 5.5, -2.5, 10, 11, 2.5, body)                                     # the keyboard body
    m.box(bd, 10, 7, -1.5, 19, 9.5, 1.5, solid(P, "orange_dark"))                    # neck
    m.box(bd, 19, 6.5, -2, 22, 10, 2, solid(P, "black"))                             # grip
    rod(m, bd, (-14, 6, 2.6), (-4, 1, 3), 0.8, solid(P, "black"), extend=0.3)        # the strap
    rod(m, bd, (-4, 1, 3), (8, 6, 3), 0.8, solid(P, "black"), extend=0.3)
    for x, y, z, w, h in [(-21, 12, -1, 4, 5), (12, 13, 0, 3.5, 4.5), (-6, 14, 1, 3, 4)]:
        note_plane(m, bd, x, y, z, w, h, P)
    return m
