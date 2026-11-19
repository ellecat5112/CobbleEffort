"""Shredder Rotom (Electric/Dark), after the user's Rotom doodle sheet (artist not named): Rotom inside a paper
shredder. An orange bin with Rotom's grumpy face on the front (lens eyes under a frowning brow, a toothy scowl), a
grey cutting head on top swallowing a sheet of paper, and green-tinged strips of shredded paper spilling out.

Front is -z, y is up. 22 units tall; about 0.9 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import face_on, palette, solid

P = palette({"aura": (110, 200, 100), "aura_light": (210, 250, 200), "paper": (240, 246, 236)})
HEIGHT = 22
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange paper shredder with a grumpy face, a grey cutting head swallowing paper and spilling shredded strips"


def build() -> Model:
    m = Model("rotom_shredder")
    top = m.bone("rotom_shredder", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.box(bd, -6, 2, -4, 6, 13, 4, face_on(P, (0, 8, -4), eyes=[(-2.4, 1.6, 1.5), (2.4, 1.6, 1.5)],
                                          mouth=(0, -1.6, 4.0, 1.4, 5)))               # the bin (its face)
    for sx in (-1, 1):
        m.box(bd, 2.4 * sx - 1.8, 11.4, -4.3, 2.4 * sx + 1.8, 12.0, -4.0, solid(P, "black"),
              rotation=(0, 0, -14 * sx), pivot=(2.4 * sx, 11.7, -4.2))                   # frowning brows
    m.box(bd, -6.5, 13, -4.5, 6.5, 16, 4.5, solid(P, "grey_dark"))                     # cutting head
    m.box(bd, -4.5, 15.9, -0.4, 4.5, 16.1, 0.4, solid(P, "black"))                     # slot
    m.box(bd, -4, 16, -0.15, 4, 22, -0.15, solid(P, "paper"))                          # a sheet going in
    for i, x in enumerate((-4.5, -2.5, -0.5, 1.5, 3.5)):                               # shredded strips spilling out
        rod(m, bd, (x, 3, -4.2), (x + (0.6 if i % 2 else -0.6), 0, -6.5 - i % 2), 0.8, solid(P, "paper" if i % 2 else "aura_light"),
            extend=0.2)
    return m
