"""Lighter Rotom (Electric/Fire), after the user's Rotom doodle sheet (artist not named): Rotom inside a pocket
lighter. An orange body with a black band, a silver top with its spark wheel, a tall pink flame flickering out of
it, and Rotom's golden lens eyes and a tiny w-shaped smile on its front.

Front is -z, y is up. 22 units tall; about 0.7 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _rotomform import face_on, palette, solid
from _route import tone

P = palette({"aura": (240, 80, 200), "aura_light": (255, 210, 240), "iris": (220, 170, 40), "flame": (250, 110, 210)},
            {"flame": (110, 210, 250)})
HEIGHT = 22
SCALE = round(0.7 * 16 / HEIGHT, 3)
HITBOX = [0.6, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange pocket lighter with a black band, a silver top and a tall pink flame"


def body(x, y, z, face, variant, **k):
    p = P(variant)
    if 9.5 <= y <= 11 and face != "up":
        return p["black"], None
    return face_on(P, (0, 6, -2.4), eyes=[(-1.4, 0.8, 1.2), (1.4, 0.8, 1.2)], mouth=(0, -1.2, 1.4, 0.6, 2))(
        x, y, z, face=face, variant=variant)


def build() -> Model:
    m = Model("rotom_lighter")
    top = m.bone("rotom_lighter", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.box(bd, -3.5, 0, -2.4, 3.5, 12, 2.4, body)                                      # the body
    m.box(bd, -3.6, 12, -2.5, 3.6, 15, 2.5, solid(P, "grey_light"))                   # silver top
    m.box(bd, 1, 15, -1, 3.2, 17, 1, solid(P, "grey_dark"))                           # spark wheel
    for i, (w, h, dx) in enumerate([(3.6, 5, 0), (2.8, 9, 0), (1.8, 6, -1.6), (1.8, 5.5, 1.4)]):   # the tall pink flame
        spike(m, bd, (-1.2 + dx, 15, 0), (0.1 + dx * 0.15, 1, 0), w, h,
              solid(P, "flame" if i == 0 else "aura", glow=True), tip=w * 0.45)
    return m
