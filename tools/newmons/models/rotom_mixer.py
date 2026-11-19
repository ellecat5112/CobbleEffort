"""Mixer Rotom (Electric/Fighting), after the user's Rotom doodle sheet (artist not named): Rotom inside a stand mixer.
A white stand and base, an orange tilt-head with Rotom's face at its front end (lens eyes, a small toothy mouth), two
steel whisks plunging into a purple mixing bowl, and pink plasma crackling round it.

Front is -z, y is up. 24 units tall; about 0.9 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import bolt_plane, face_on, palette, solid

P = palette({"aura": (240, 140, 220), "aura_light": (255, 220, 250), "stand": (236, 234, 240), "bowl": (150, 90, 200)},
            {"bowl": (90, 190, 120)})
HEIGHT = 24
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a stand mixer with a white stand, an orange head with Rotom's face, steel whisks and a purple bowl"


def build() -> Model:
    m = Model("rotom_mixer")
    top = m.bone("rotom_mixer", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -5, 0, -8, 5, 2, 5, solid(P, "stand"))                                  # base
    m.box(bd, -2.5, 2, 1.5, 2.5, 16, 5, solid(P, "stand"))                            # column
    m.round_box(bd, 0, -3.5, 5.0, 5.0, 2, 9, solid(P, "bowl"), cut=1.6)              # the purple bowl
    m.round_box(bd, 0, -3.5, 4.0, 4.0, 8.4, 9.2, solid(P, "charcoal"), cut=1.3)
    hd = m.bone("head", bd, (0, 17, 3))
    m.box(hd, -4, 15, -9, 4, 21, 5.5, face_on(P, (0, 18, -9), eyes=[(-1.8, 0.8, 1.4), (1.8, 0.8, 1.4)],
                                             mouth=(0, -1.6, 2.6, 1.0, 4)))          # the tilt-head (its face)
    for sx in (-1, 1):
        rod(m, hd, (1.4 * sx, 15, -3.5), (1.4 * sx, 7.5, -3.5), 0.8, solid(P, "grey_light"), extend=0.2)   # whisks
        m.round_box(hd, 1.4 * sx, -3.5, 1.2, 1.2, 6.5, 9.5, solid(P, "grey"), cut=0.5)
    for x, y, z, w, h, pl, fl in [(-9, 14, -3, 4, 7, "xy", False), (6, 6, -6, 4, 6, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
