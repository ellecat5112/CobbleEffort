"""Charger Rotom (Electric), after the user's Rotom doodle sheet (artist not named): Rotom inside a wall charger.
An orange plug block with two lens eyes and a little grin, two grey prongs on top, and a long black cable trailing
behind like a tail to a small connector; grey-blue plasma sparks round its prongs.

Front is -z, y is up. 20 units tall; about 0.8 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import bolt_plane, face_on, palette, solid

P = palette({"aura": (170, 190, 220), "aura_light": (235, 245, 255)})
HEIGHT = 20
SCALE = round(0.8 * 16 / HEIGHT, 3)
HITBOX = [0.8, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange wall-charger plug with lens eyes, grey prongs and a long black cable for a tail"


def build() -> Model:
    m = Model("rotom_charger")
    top = m.bone("rotom_charger", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -5, 4, -3.5, 5, 14, 3.5,
          face_on(P, (0, 9, -3.5), eyes=[(-2.0, 1.4, 1.5), (2.0, 1.4, 1.5)], mouth=(0, -1.6, 3.0, 1.0, 4)))
    m.box(bd, -4, 3, -2.5, 4, 4, 2.5, solid(P, "orange_dark"))
    for sx in (-1, 1):
        m.box(bd, 2 * sx - 0.6, 14, -0.8, 2 * sx + 0.6, 18.5, 0.8, solid(P, "grey_light"))   # the prongs
    pts = [(0, 3.5, 1), (0, 1, 4), (-2, 0.5, 9), (-1, 2.5, 13), (2, 1.5, 17), (3, 0.5, 20)]
    tail = m.bone("tail", bd, (0, 3, 2))
    for a, b in zip(pts, pts[1:]):
        rod(m, tail, a, b, 1.3, solid(P, "black"), extend=0.5)                               # the cable
    m.box(tail, 2, -0.5, 20, 4.5, 2, 23, solid(P, "charcoal"))                               # its connector
    for x, y, z, w, h, pl, fl in [(-7, 13, -1, 4, 7, "xy", False), (4, 15, -1, 4, 6, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
