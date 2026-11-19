"""Vacuum Rotom (Electric/Poison), after the user's Rotom doodle sheet (artist not named): Rotom inside a shop vacuum.
A round orange canister with a worried face (lens eyes, a little frown, a bead of sweat) under a black lid, small
black wheels, and a ribbed black hose arching up and over into a grey wand with a floor nozzle; dusty brown plasma
puffs round it.

Front is -z, y is up. 24 units tall; about 1.0 block.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import bolt_plane, face_on, palette, solid

P = palette({"aura": (170, 130, 90), "aura_light": (236, 214, 180), "iris": (120, 190, 236)})
HEIGHT = 24
SCALE = round(1.0 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an orange shop vacuum with a worried face, a black lid and a ribbed hose arching into a floor wand"


def build() -> Model:
    m = Model("rotom_vacuum")
    top = m.bone("rotom_vacuum", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 5.5, 5.5, 2, 12, face_on(P, (0, 7, -5.5), eyes=[(-2.2, 1.2, 1.5), (2.2, 1.2, 1.5)],
                                                   mouth=(0, -1.8, 2.2, 0.8, 3)), cut=1.8)       # the canister
    m.round_box(bd, 0, 0, 5.8, 5.8, 12, 13.5, solid(P, "black"), cut=1.9)                        # lid
    m.box(bd, 4.2, 10, -5.8, 4.8, 11.4, -5.5, solid(P, "aura_light"))                            # a bead of sweat
    for x, z in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        m.box(bd, x - 1, 0.5, z - 1, x + 1, 2.2, z + 1, solid(P, "black"))                       # wheels
    hose = m.bone("tail", bd, (0, 13.5, 2))
    pts = [(0, 13.5, 2), (1, 18, 3), (3, 21.5, 1), (5, 22.5, -2), (7, 21, -4)]
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, hose, a, b, 2.0, solid(P, "black" if i % 2 == 0 else "charcoal"), extend=0.6)     # the ribbed hose
    rod(m, hose, (7, 21, -4), (7.5, 2, -7), 1.2, solid(P, "grey"), extend=0.3)                  # the wand
    m.box(hose, 5, 0, -9, 10, 1.8, -6, solid(P, "black"))                                        # floor nozzle
    for x, y, z, w, h, pl, fl in [(-8, 10, -1, 4, 6, "xy", False), (-7, 2, 1, 4, 5, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
