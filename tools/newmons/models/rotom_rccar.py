"""RC Car Rotom (Electric/Ground), after the user's Rotom doodle sheet (artist not named): Rotom inside a radio-
controlled racing car. A low orange car with a dark windscreen, a black rear spoiler, four big black wheels with teal
hubs, its lens eyes for headlights over a grinning grille, and boost flames at the back.

Front is -z, y is up. 12 units tall, 26 long; about 0.6 blocks tall.
"""
from __future__ import annotations

from _boxmodel import Model
from _rotomform import face_on, palette, solid, tyre, wheel
from _route import tone

P = palette({"aura": (220, 180, 120), "aura_light": (250, 236, 200), "teal": (90, 210, 220), "flame": (250, 150, 50)})
HEIGHT = 12
SCALE = round(0.7 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a low orange RC racing car with headlight eyes, a grinning grille, teal wheel hubs and boost flames"


def cabin(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "east", "west") and y > 7.6:
        return p["charcoal"], None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("rotom_rccar")
    top = m.bone("rotom_rccar", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.box(bd, -5.5, 2.5, -10, 5.5, 6.5, 10, face_on(P, (0, 4.5, -10), eyes=[(-3.2, 0.6, 1.4), (3.2, 0.6, 1.4)],
                                                    mouth=(0, -0.9, 3.4, 1.4, 5)))       # the car
    m.box(bd, -4.5, 6.5, -4, 4.5, 10, 4, cabin)                                          # cabin and windscreen
    m.box(bd, -5.5, 10.5, 7.5, 5.5, 11.5, 10.5, solid(P, "black"))                       # spoiler
    for sx in (-1, 1):
        m.box(bd, 4 * sx - 0.5, 6.5, 8.5, 4 * sx + 0.5, 10.5, 9.5, solid(P, "black"))
        for zc in (-6.5, 6.5):
            x0, x1 = (5.5, 8.5) if sx > 0 else (-8.5, -5.5)
            tyre(m, bd, x0, x1, 3.2, zc, 3.2, wheel(P, hub="teal", centre=(0, 3.2, zc), r=3.2))
    for sx in (-1, 1):                                                                    # boost flames
        m.box(bd, 2.5 * sx - 1, 3.5, 10, 2.5 * sx + 1, 5.5, 13, solid(P, "flame", glow=True))
    return m
