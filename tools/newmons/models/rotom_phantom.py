"""Phantom Rotom (Ghost/Dark), after the user's Rotom doodle sheet (artist not named): a Rotom that slipped out of its
appliance and swelled into a shadow. A billowing mass of dark purple wisps with ragged trailing tendrils, Rotom's
orange face peeking out from under a black hood, and the orange cord and plug of the appliance it left behind
trailing as a tail.

Front is -z, y is up. 26 units tall; about 1.2 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _rotomform import ball, face_on, palette, solid

P = palette({"shade": (88, 50, 120), "shade_dark": (50, 28, 72), "aura": (170, 110, 230), "aura_light": (230, 200, 255)},
            {"shade": (40, 90, 140), "shade_dark": (20, 50, 84)})
HEIGHT = 26
SCALE = round(1.2 * 16 / HEIGHT, 3)
HITBOX = [1.0, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a billowing mass of dark purple wisps with Rotom's face peeking from a black hood and an orange cord tail"


def build() -> Model:
    m = Model("rotom_phantom")
    top = m.bone("rotom_phantom", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, 0, 11, 1, 7.0, solid(P, "shade"))                         # the shadow mass
    for i, (a, b) in enumerate([((-5, 6, 0), (-10, -1, 2)), ((5, 6, 0), (11, 0, 1)), ((0, 5, 3), (-2, -3, 6)),
                                ((-6, 12, 3), (-13, 15, 6)), ((6, 13, 3), (13, 18, 5)), ((2, 6, -3), (4, -2, -4))]):
        spike(m, bd, a, tuple(bb - aa for aa, bb in zip(a, b)), 2.6, 7.5, solid(P, "shade_dark" if i % 2 else "shade"), tip=1.0)
    hd = m.bone("head", bd, (0, 15, -4))
    ball(m, hd, 0, 14.5, -4.5, 3.6, face_on(P, (0, 14.5, -8.1), eyes=[(-1.3, 0.5, 1.1), (1.3, 0.5, 1.1)],
                                            mouth=(0, -1.4, 3.0, 1.0, 4)))                # Rotom's face
    m.round_box(hd, 0, -3.8, 4.4, 4.0, 16.6, 20, solid(P, "black"), cut=1.4)                 # the black hood
    m.box(hd, -4.4, 12.5, -3.5, -3.4, 17, 0, solid(P, "black"))
    m.box(hd, 3.4, 12.5, -3.5, 4.4, 17, 0, solid(P, "black"))
    tail = m.bone("tail", bd, (0, 6, 6))
    pts = [(0, 6, 6), (-3, 3, 10), (-7, 4, 13), (-10, 2, 15)]
    for a, b in zip(pts, pts[1:]):
        rod(m, tail, a, b, 1.4, solid(P, "orange"), extend=0.5)                             # the cord
    m.box(tail, -12.5, 0.5, 14.5, -9.5, 3.5, 17, solid(P, "black"))                         # its plug
    return m
