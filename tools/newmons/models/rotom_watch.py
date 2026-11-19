"""Watch Rotom (Electric/Psychic), after the user's smartwatch Rotom art (artist not named): Rotom inside a
smartwatch. A round red face with a dark screen where its lens eyes and smile show, a peach bezel trim and two peach
side buttons, a little peach horn on top, and a strap of red segments looping back round below.

Front is -z, y is up. 20 units tall; about 0.9 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _rotomform import bolt_plane, cone, disc_z, palette, rotom_eye, solid
from _route import tone

P = palette({"red": (220, 40, 80), "red_light": (246, 110, 140), "peach": (244, 190, 150), "iris": (90, 200, 240),
             "aura": (250, 140, 170), "aura_light": (255, 220, 230)}, {"red": (60, 120, 230), "red_light": (130, 180, 250)})
HEIGHT = 20
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a red smartwatch whose round screen shows Rotom's lens eyes and smile, with peach buttons and a looped strap"


def face(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 11)
        if d < 4.8:
            for sx in (-1, 1):
                e = rotom_eye(x - 1.8 * sx, y - 11.8, 1.3, p)
                if e:
                    return e
            if 9.0 <= y <= 9.6 and abs(x) <= 1.4:
                return p["white"], p["white"]               # its smile
            return p["charcoal"], None
        if d < 5.6:
            return p["peach"], None
    return tone(p["red"], face), None


def build() -> Model:
    m = Model("rotom_watch")
    top = m.bone("rotom_watch", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    disc_z(m, bd, 0, 11, -2.5, 1.5, 7, face)                              # the watch face
    for i in range(10):                                                   # the strap looping back round below
        a = math.pi * (0.62 + 1.76 * i / 9)
        y, z = 11 + 8.2 * math.cos(a), 5.5 - 6.8 * math.sin(a) * -1
        m.box(bd, -3.6, y - 1.3, z - 1.3, 3.6, y + 1.3, z + 1.3, solid(P, "red" if i % 2 else "red_light"))
    for by in (8.5, 13.5):                                                # side buttons
        m.box(bd, 6.5, by - 0.9, -1.4, 7.8, by + 0.9, 0.4, solid(P, "peach"))
    cone(m, bd, (-4, 17, -0.5), (-0.4, 1, 0), 2.4, 3.5, solid(P, "peach"))
    for x, y, z, w, h, pl, fl in [(-11, 6, -1, 4, 7, "xy", False), (8, 14, -1, 4, 6, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
