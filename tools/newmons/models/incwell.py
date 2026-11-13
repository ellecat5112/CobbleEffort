"""Incwell, the Inkwell Pokémon (Dark/Steel), Incl evolved: a column of ink rising out of a glass inkwell. Its pen
nib, now big, stands point-up on top as its head, with two glowing yellow eyes at its base; two long dripping arms hang
down at its sides, and ink spills over the inkwell's rim.

Front is -z, y is up. 30 units tall to the nib's point; baseScale 0.7 (1.3 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _ink import P, eyef, glassf, inkf, nibf
from _route import tone


def bottlef(x, y, z, face, variant, **k):
    """The inkwell: translucent glass round dark ink."""
    p = P(variant)
    if y > 7.4:
        return tone(p["bottle_cap"], face), None                              # the rim
    return glassf(x, y, z, face, variant)


SCALE = 0.7
HITBOX = [0.8, 1.3]
KIND = "floater"
K = 4
HEIGHT = 30
LOOK = ("a column of glossy ink rising out of a glass inkwell, with a big silver pen nib for a head, glowing yellow "
        "eyes and two long dripping arms")


def build() -> Model:
    m = Model("incwell")
    top = m.bone("incwell", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    # the inkwell: glass walls round a core of ink, a rim on top, ink spilling over
    m.round_box(bd, 0, 0, 4.2, 4.2, 0, 8, bottlef, cut=1.4)
    m.round_box(bd, 0, 0, 3.4, 3.4, 0.4, 7.6, inkf, cut=1.1)
    for a in range(5):
        ang = a * 2 * math.pi / 5 + 0.4
        x, z = 3.6 * math.cos(ang), 3.6 * math.sin(ang)
        rod(m, bd, (x, 8.2, z), (x * 1.15, 4 + a % 2 * 1.5, z * 1.15), 1.2, inkf, extend=0.3)   # drips over the rim
    # the ink column, wider at the shoulders
    m.round_box(bd, 0, 0, 3, 3, 7.5, 14, inkf, cut=1)
    m.round_box(bd, 0, 0, 4.4, 3.4, 13.5, 20.5, inkf, cut=1.4)
    hd = m.bone("head", bd, (0, 20.5, 0))
    m.round_box(hd, 0, -0.2, 3.2, 2.8, 20, 22.6, inkf, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.6 - 0.7, 21.4, -3.15, sx * 1.6 + 0.7, 22.4, -2.9, eyef)
    m.box(hd, -3.4, 21.5, -2.4, 3.4, 30, -2.4, nibf(0, 30, 6.8, 8.5, tip_up=True))   # big nib, point up
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):                           # long dripping arms
        ar = m.bone(nm, bd, (sx * 4.2, 19.5, 0))
        pts = [(sx * 4.2, 19.5, 0), (sx * 6.5, 17.5, -0.4), (sx * 7, 12, -0.6), (sx * 6.6, 7.5, -0.4), (sx * 6.8, 5, 0)]
        for a, b, t in zip(pts, pts[1:], (2.6, 2.4, 2.2, 1.6)):
            rod(m, ar, a, b, t, inkf, extend=0.5)
    return m
