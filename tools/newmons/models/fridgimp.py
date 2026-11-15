"""Fridgimp, the Frostbite Pokémon (Ice/Dark; the user's art, artist not named, name kept): a crouching little blue
imp with a crest of icy spikes swept back over its head, curled horns, pointed ears, red eyes, a big round red
frostbitten nose and a toothy grin, spiky frost along its back, clawed hands and feet, and a jagged tail.

Front is -z, y is up. 18 units tall; baseScale 0.5 (0.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _snowimp import P, frosty, horn, icicle, slant_eye, solid

SCALE = 0.5
HITBOX = [0.9, 1.15]
KIND = "biped"
K = 6
HEIGHT = 18
LOOK = ("a crouching little blue imp with an icy crest, curled horns, pointed ears, red eyes, a big round red frostbitten "
        "nose, a toothy grin, frosty back spikes and a jagged tail")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = slant_eye(p, x - sx * 1.7, y - 12.6, 1.1, "eye", sx)
            if c is not None:
                return c, None
        if 9.4 < y < 10.4 and abs(x) < 2.4:                           # a toothy grin
            return (p["white"] if (abs(x) * 2.5) % 1 < 0.6 and y > 9.8 else p["mouth"]), None
    return frosty()(x, y, z, face, variant)


def nosef(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "up") and x < -0.2 and y > 11.4:
        return p["red_light"], None                                    # a shine
    return tone(p["red"], face), None


def build() -> Model:
    m = Model("fridgimp")
    top = m.bone("fridgimp", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0.5, 3.0, 2.6, 4.6, 9.6, frosty(), cut=1.0)                 # a small crouched body
    for i, y in enumerate((6.0, 7.6, 9.0)):                                        # frost spikes down its back
        icicle(m, bd, (0, y, 2.8), (0, 0.4, 1), 1.4, 2.4)
    hd = m.bone("head", bd, (0, 9.4, 0))
    m.round_box(hd, 0, -0.3, 3.4, 2.9, 8.6, 9.4, headf, cut=1.2)
    m.round_box(hd, 0, -0.3, 4.0, 3.4, 9.2, 14.6, headf, cut=1.6)
    m.round_box(hd, 0, -0.3, 3.4, 2.9, 14.4, 15.4, headf, cut=1.2)
    m.box(hd, -1.2, 10.2, -5.4, 1.2, 12.6, -3.0, nosef)                            # the big red nose
    for i, (bx, dx, dy, dz, l) in enumerate(((1.2, -0.7, 1.2, 0.8, 7.0), (-0.4, -1.0, 1.0, 0.5, 6.0),
                                             (-1.8, -1.2, 0.7, 0.3, 4.6), (0.4, -0.2, 1.2, 1.2, 4.0))):
        icicle(m, hd, (bx, 14.6, 0.2 + i * 0.3), (dx, dy, dz), 1.8, l)          # the icy crest, swept up and back
    for sx in (-1, 1):
        horn(m, hd, [(sx * 3.4, 13.4, 0.6), (sx * 5.0, 14.4, 1.2), (sx * 5.6, 12.8, 1.6), (sx * 4.8, 11.6, 1.2)], (1.4, 1.1, 0.9))
        spike(m, hd, (sx * 3.8, 11.6, -0.6), (sx * 1, 0.25, 0.3), 1.2, 3.0, solid("blue_dark"), tip=0.6)   # ears
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                            # arms down to the ground
        a = m.bone(nm, bd, (sx * 2.6, 8.4, -0.4))
        rod(m, a, (sx * 2.6, 8.4, -0.4), (sx * 4.2, 5.0, -2.2), 1.3, frosty())
        rod(m, a, (sx * 4.2, 5.0, -2.2), (sx * 4.0, 1.4, -3.2), 1.2, frosty())
        for cx in (-0.5, 0.5):
            spike(m, a, (sx * 4.0 + cx, 1.2, -3.6), (0, -0.4, -1), 0.6, 1.4, solid("ice"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                            # crouched legs
        lg = m.bone(nm, top, (sx * 2.0, 5.0, 0.6))
        rod(m, lg, (sx * 2.0, 5.0, 0.6), (sx * 3.2, 3.4, -1.4), 1.8, frosty())
        rod(m, lg, (sx * 3.2, 3.4, -1.4), (sx * 3.0, 0.6, 0.6), 1.5, frosty())
        m.box(lg, sx * 3.0 - 1.0, 0, -1.4, sx * 3.0 + 1.0, 1.0, 1.4, frosty())
        for cx in (-0.6, 0.6):
            spike(m, lg, (sx * 3.0 + cx, 0.4, -1.4), (0, -0.2, -1), 0.6, 1.2, solid("ice"))
    tl = m.bone("tail", bd, (0, 5.2, 2.4))                                         # a jagged tail
    rod(m, tl, (0, 5.2, 2.4), (0, 4.0, 6.0), 1.2, frosty())
    rod(m, tl, (0, 4.0, 6.0), (0, 6.2, 8.4), 1.0, frosty())
    for p, d in (((0, 4.6, 4.4), (0, 1, 0.3)), ((0, 5.0, 7.2), (0, 1, -0.2))):
        icicle(m, tl, p, d, 1.0, 1.8)
    spike(m, tl, (0, 6.2, 8.4), (0, 0.6, 1), 1.4, 2.0, solid("ice"), tip=0.6)
    return m
