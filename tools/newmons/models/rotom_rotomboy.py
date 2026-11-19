"""Rotom Boy (Electric/Ghost), after CaligoMilites' art: Rotom haunting an old handheld game console. An orange
console with Rotom's horn on top, two yellow-ringed lens eyes and a fanged grin above a dark screen showing a yellow
bolt, a D-pad and A/B buttons below; round it glows the translucent yellow ghost of a Pikachu it once played as,
hugging the console, ears up, its bolt-shaped tail crackling.

Front is -z, y is up. 34 units tall; about 1.4 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import bolt_shape, cone, grin, palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (255, 230, 90), "aura_light": (255, 250, 210), "iris": (250, 210, 60), "screen": (40, 44, 50),
             "ghost": (255, 236, 110, 150)}, {"ghost": (130, 220, 255, 150)})
HEIGHT = 34
SCALE = round(1.4 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange handheld game console with lens eyes and a fanged grin, hugged by the glowing ghost of a Pikachu"


def console(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = rotom_eye(x - 3.6 * sx, y - 19.6, 1.7, p)
            if e:
                return e
        g = grin(x, y - 18.0, 3.2, 1.1, p, teeth=4)
        if g:
            return g, None
        if 9 <= y <= 16 and abs(x) <= 5.4:                 # the screen and its bezel
            if 9.6 <= y <= 15.4 and abs(x) <= 4.6:
                u, v = (x + 4.6) / 9.2, (y - 9.6) / 5.8
                if 0.25 < u < 0.75 and bolt_shape((u - 0.25) * 2, v):
                    return p["iris"], p["iris"]
                return p["screen"], None
            return p["charcoal"], None
        if 2.5 <= y <= 6.5 and -5.5 <= x <= -1.5 and (abs(x + 3.5) < 0.7 or abs(y - 4.5) < 0.7):
            return p["black"], None                         # D-pad
        for bx, by in ((3.0, 4.0), (4.8, 5.6)):
            if math.hypot(x - bx, y - by) < 0.9:
                return p["black"], None                     # A and B
    return tone(p["orange"], face), None


def ghost(x, y, z, face, variant, **k):
    c = P(variant)["ghost"]
    return c, c[:3]


def build() -> Model:
    m = Model("rotom_rotomboy")
    top = m.bone("rotom_rotomboy", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.box(bd, -6.5, 0, -2.5, 6.5, 22, 2.5, console)                      # the console
    m.box(bd, -5.5, -1, -2, 5.5, 0, 2, solid(P, "orange_dark"))
    cone(m, bd, (0, 22, 0), (0, 1, 0.1), 4.0, 5.0, solid(P, "orange"))    # Rotom's horn
    gh = m.bone("head", bd, (0, 22, 3))
    m.round_box(gh, 0, 5, 7.5, 4.0, 18, 29, ghost, cut=2.4)              # the ghost Pikachu's head behind it
    for sx in (-1, 1):
        rod(m, gh, (4.5 * sx, 27, 5), (8.5 * sx, 35, 6), 2.2, ghost, extend=0.4)            # its ears
        rod(m, bd, (7 * sx, 14, 3), (8 * sx, 7, -1), 2.4, ghost, extend=0.5)               # arms hugging the console
        rod(m, bd, (8 * sx, 7, -1), (5 * sx, 6, -3.5), 2.2, ghost, extend=0.5)
    tail = m.bone("tail", bd, (6, 8, 4))
    for a, b, t in (((6, 8, 4), (12, 13, 5), 2.2), ((12, 13, 5), (10, 16, 5), 2.0), ((10, 16, 5), (16, 22, 6), 2.6)):
        rod(m, tail, a, b, t, ghost, extend=0.5)                          # the bolt-shaped tail
    return m
