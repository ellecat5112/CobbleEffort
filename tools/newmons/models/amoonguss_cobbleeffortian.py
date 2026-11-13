"""The CobbleEffort Amoonguss (Grass/Steel), the CobbleEffort Foongus evolved: a big screw mushroom. Its broad steel
cap is a Phillips screw head (a cross slot on top, notches, a ring of rivets) over a hex nut collar; under it a stout
white body with swirly eyes and a wide grin, steely hair at the back, two long threaded screw arms, and copper feet.

Front is -z, y is up. 22 units tall; baseScale 0.6 (0.9 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _screw import P, capf, copperf, facef, hairf, screw, steelf

SCALE = 0.6
HITBOX = [1.9, 1.5]
KIND = "biped"
K = 4
HEIGHT = 22
LOOK = ("a big screw mushroom: a broad steel Phillips-head cap over a hex nut collar, a stout white body with swirly "
        "eyes and a wide grin, two long threaded screw arms and copper feet")


def build() -> Model:
    m = Model("amoonguss_cobbleeffortian")
    top = m.bone("amoonguss_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 4.4, 4.0, 1.6, 13.4, facef(1.8, 10.0, 1.35, 7.4, 1.6, -4.0), cut=1.8)   # stout white body
    for i in range(6):                                                         # the hex nut collar
        a = i * math.pi / 3
        x, z = 4.3 * math.cos(a), 4.3 * math.sin(a)
        w = 5.0
        m.box(bd, x - w / 2, 13.0, z - 0.6, x + w / 2, 14.8, z + 0.6, steelf,
              rotation=(0, -math.degrees(a) + 90, 0), pivot=(x, 13.9, z))
    hd = m.bone("head", bd, (0, 14.5, 0))
    cap = capf(0, 0, 15.6, 22.0, 0.7)
    m.round_box(hd, 0, 0, 9.0, 9.0, 14.6, 17.2, cap, cut=2.6)                  # broad screw head: rim
    m.round_box(hd, 0, 0, 7.4, 7.4, 17.0, 20.6, cap, cut=2.1)                  # a smooth dome
    m.round_box(hd, 0, 0, 4.8, 4.8, 20.4, 22.0, cap, cut=1.4)
    for i, (x, z) in enumerate(((1.0, 3.6), (-1.2, 3.4), (2.6, 2.4), (-2.8, 2.0), (0, 4.0), (3.4, 0.8), (-3.4, 0.6))):
        spike(m, hd, (x, 14.0, z), (x * 0.3, -0.7, 1), 1.2, 2.4 + (i % 2) * 0.8, hairf)   # steely hair at the back
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                        # two long threaded screw arms
        ar = m.bone(nm, bd, (sx * 4.2, 8.6, 0))
        screw(m, ar, (sx * 3.8, 8.6, -0.2), (sx, -0.25, -0.35), 10.5, 3.2, pitch=1.2)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, top, (sx * 1.8, 2, 0))
        m.round_box(lg, sx * 1.8, -0.6, 1.4, 1.8, 0, 2.2, copperf, cut=0.6)     # copper feet
    return m
