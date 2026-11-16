"""Algomon (Baby II) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a spiky lime-green ball on four thin violet legs that end in spoon-shaped feet. A violet band crosses
its face round one big magenta-and-yellow ringed eye, two stubby horns with yellow-and-red tips stand on top and grey
steel spikes ring its lower half. Tiny.

Front is -z, y is up. 26 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _algo import GREEN, P, STEEL, VIOLET, hornf, ringed_eye
from _digidetail import plane
from _route import tone

HEIGHT = 26
SCALE, HITBOX = sized(0.5, HEIGHT, 0.45)
KIND = "floater"
K = 4
LOOK = ("a spiky lime-green ball on four thin violet spoon-footed legs, a violet band round one big ringed eye, two "
        "yellow-and-red tipped horns and grey steel spikes")
EYE = ringed_eye(0, 13.0, 3.0, outer="iris", iris="eye_y")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = EYE(x, y, z, face, p)
    if c is not None:
        return tone(c, face), None
    a, b = plane(x, y, z, face)
    if abs(b - 13.0) < 0.8 and face != "up":
        return tone(p["violet"], face), None
    if (round(a * 0.6) + round(b * 0.6)) % 3 == 0 and math.hypot(a % 2.6 - 1.3, b % 2.6 - 1.3) < 0.55:
        return tone(p["green_light"], face), None              # pale spots
    return GREEN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("algomonbabyii")
    top = m.bone("algomonbabyii", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    ball(m, bd, (0, 13.0, 0), 7.0, bodyf, layers=7)
    for i in range(10):                                          # steel spikes round the lower half
        ang = math.radians(i * 36 + 18)
        d = (math.sin(ang), -0.7, -math.cos(ang))
        spike(m, bd, (6.0 * math.sin(ang), 9.0, -6.0 * math.cos(ang)), d, 1.4, 2.6, STEEL, tip=0.6)
    for sx in (-1, 1):                                           # horns
        rod(m, bd, (sx * 2.6, 18.6, 0.4), (sx * 3.6, 24.6, 0.8), 2, hornf, extend=0.2)
    for i, (sx, sz) in enumerate(((1, -1), (-1, -1), (1, 1), (-1, 1))):   # thin legs with spoon feet
        nm = f"leg_{'front' if sz < 0 else 'back'}_{'left' if sx > 0 else 'right'}"
        lg = m.bone(nm, top, (sx * 5.0, 9.0, sz * 3.0))
        knee = (sx * 9.0, 7.0, sz * 5.0)
        foot = (sx * 11.0, 1.0, sz * 6.0)
        rod(m, lg, (sx * 5.0, 9.0, sz * 3.0), knee, 1, VIOLET, extend=0.3)
        rod(m, lg, knee, foot, 1, VIOLET, extend=0.3)
        m.round_box(lg, foot[0], foot[2], 1.4, 1.0, 0.0, 1.0, VIOLET, cut=1)
    for sx in (-1, 1):                                           # tiny arms waving up (Baby II's raised hands)
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 6.0, 16.0, 0))
        rod(m, ab, (sx * 6.0, 16.0, 0), (sx * 8.5, 20.0, 0), 1, VIOLET, extend=0.2)
        m.box(ab, sx * 8.5 - 0.8, 20.0, -0.5, sx * 8.5 + 0.8, 21.6, 0.5, VIOLET)
    return m
