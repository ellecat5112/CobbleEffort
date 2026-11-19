"""Jet Rotom (Electric/Flying), after the user's Rotom doodle sheet (artist not named): Rotom inside a toy jet. A
sleek orange fuselage with Rotom's lens eyes on its nose, swept wings and tail fins, a ring of dark vents round its
exhaust and a roaring plume of red flame behind it.

Front is -z, y is up. 12 units tall, 34 long; about 0.6 blocks tall.
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _rotomform import face_on, palette, solid

P = palette({"aura": (236, 60, 50), "aura_light": (255, 190, 120), "flame": (250, 120, 40)})
HEIGHT = 12
SCALE = round(0.75 * 16 / HEIGHT, 3)
HITBOX = [1.2, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange toy jet with lens eyes on its nose, swept wings and a roaring plume of red flame"


def build() -> Model:
    m = Model("rotom_jet")
    top = m.bone("rotom_jet", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0, 3.0, 9, 3, 9, solid(P, "orange"), cut=1.2)                 # fuselage
    m.box(bd, -2.4, 3.6, -12.5, 2.4, 8.4, -9, face_on(P, (0, 6, -12.5), eyes=[(-1.0, 0.7, 0.95), (1.0, 0.7, 0.95)],
                                                     mouth=(0, -1.2, 2.2, 0.8, 3)))   # the nose (its face)
    for sx in (-1, 1):                                                                 # swept wings and tail fins
        m.box(bd, 3 * sx if sx > 0 else -13, 5, -2, 13 if sx > 0 else -3, 6, 4, solid(P, "orange_light"),
              rotation=(0, -25 * sx, 0), pivot=(3 * sx, 5, -2))
        m.box(bd, 2.5 * sx if sx > 0 else -6.5, 5.5, 6, 6.5 if sx > 0 else -2.5, 6.3, 9, solid(P, "orange_light"))
    m.box(bd, -0.5, 9, 5, 0.5, 13, 9, solid(P, "orange_dark"))                       # tail fin
    m.round_box(bd, 0, 9.6, 3.3, 1.2, 3.2, 8.8, solid(P, "black"), cut=1.0)          # exhaust vents
    for i, (w, h, dy) in enumerate([(5.0, 5.0, 0), (3.6, 9.0, 0), (2.2, 13.0, 0), (2.0, 8.0, 2.2), (2.0, 8.0, -2.2)]):
        spike(m, bd, (0, 6 + dy, 10.6), (0, 0.18 + dy * 0.08, 1), w, h,
              solid(P, "flame" if i == 0 else "aura", glow=True), tip=w * 0.5)          # the roaring flame plume
    return m
