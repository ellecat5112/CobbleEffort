"""Clock Rotom (Electric/Dragon), after the user's Rotom doodle sheet (artist not named): Rotom inside a pendulum wall
clock. A round clock with a blue rim and an orange face where its lens eyes sit above the centre, black hour marks,
two orange hands, and a blue pendulum swinging below.

Front is -z, y is up. 30 units tall; about 1.0 block.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import disc_z, palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (80, 140, 230), "aura_light": (200, 225, 255), "rim": (60, 120, 210), "iris": (90, 170, 240)},
            {"rim": (200, 150, 60)})
HEIGHT = 30
SCALE = round(1.0 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a round pendulum wall clock with a blue rim, lens eyes on its face, orange hands and a blue pendulum"


def face(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 20)
        if d > 7.6:
            return p["rim"], None
        for sx in (-1, 1):
            e = rotom_eye(x - 2.3 * sx, y - 22.4, 1.4, p)
            if e:
                return e
        a = math.atan2(x, y - 20)
        if d > 6.2 and abs(math.sin(a * 6)) < 0.18:
            return p["black"], None                         # hour marks
        return p["white"], None
    return tone(p["rim"], face), None


def build() -> Model:
    m = Model("rotom_clock")
    top = m.bone("rotom_clock", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    disc_z(m, bd, 0, 20, -1.5, 1.5, 8.6, face)                                       # the clock (its face)
    rod(m, bd, (0, 20, -1.8), (0, 24.8, -1.8), 0.9, solid(P, "orange"), extend=0.2)  # hands
    rod(m, bd, (0, 20, -1.9), (3.4, 18.2, -1.9), 0.9, solid(P, "orange_dark"), extend=0.2)
    m.box(bd, -0.7, 19.3, -2.3, 0.7, 20.7, -1.6, solid(P, "black"))
    pend = m.bone("tail", bd, (0, 11.5, 0))
    rod(m, pend, (0, 11.6, 0.5), (0, 2.5, 0.5), 0.9, solid(P, "rim"), extend=0.2)    # the pendulum
    m.round_box(pend, 0, 0.5, 2.2, 0.8, 0, 3, solid(P, "rim"), cut=0.7)
    return m
