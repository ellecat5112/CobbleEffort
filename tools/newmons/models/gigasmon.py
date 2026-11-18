"""Gigasmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Legendary Warrior of earth's beast spirit: a hulking brown giant of rock-hard muscle with no
neck, a small fierce face sunk between its shoulders, cream bands striping its limbs, horn-spikes on its shoulders and
back, enormous fists marked with cream rings and stubby clawed feet. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking neckless brown giant of rock-hard muscle with cream bands, shoulder horn-spikes and enormous "
        "ringed fists")
BASE = {"brown": (170, 120, 80), "brown_dark": (110, 70, 40), "brown_light": (220, 180, 140), "cream": (240, 220, 180),
        "eye": (30, 28, 30), "claw": (240, 236, 220)}
SHINY = {"brown": (120, 130, 150), "brown_dark": (70, 76, 90), "brown_light": (180, 190, 210)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "brown", dark="brown_dark", light="brown_light")


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((y * 0.4 + abs(x) * 0.1) % 2.6 - 1.3) < 0.3:
        return tone(p["cream"], face), None
    return SK(x, y, z, face, variant, box=box, **k)


def fistf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
        if abs(math.hypot(x - cx, y - cy) - 2.4) < 0.5 or math.hypot(x - cx, y - cy) < 0.8:
            return tone(p["cream"], face), None
    return SK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gigasmon")
    top = m.bone("gigasmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0, 9.0, 7.0, 14.0, 32.0, SK, cut=3)                              # hulking torso
    m.round_box(bd, 0, 1.0, 11.0, 8.0, 28.0, 38.0, SK, cut=3)                            # neckless shoulders
    hd = m.bone("head", bd, (0, 34, -6))
    m.round_box(hd, 0, -7.0, 3.0, 1.6, 31.0, 36.0, SK, cut=1)                            # small sunken face
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 34.0, -8.8, max(sx * 0.8, sx * 2.0), 34.8, -8.6, solid(P, "eye"))
    for sx in (-1, 1):
        for j in range(3):                                                             # horn-spikes
            spike(m, bd, (sx * (7.0 + j * 1.6), 37.6, -1.0 + j * 2.4), (sx * 0.4, 1, 0.3), 2.0, 5.0 - j,
                  bandf, tip=0.9)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # enormous fists
        ab = m.bone(nm, bd, (sx * 11.0, 34.0, 0))
        rod(m, ab, (sx * 11.0, 34.0, 0), (sx * 15.0, 22.0, -2.0), 6, bandf, extend=0.8)
        rod(m, ab, (sx * 15.0, 22.0, -2.0), (sx * 15.0, 12.0, -6.0), 6, bandf, extend=0.8)
        m.round_box(ab, sx * 15.0, -7.0, 5.0, 5.0, 2.0, 12.0, fistf, cut=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 14.0, 0))
        rod(m, lg, (sx * 5.0, 15.0, 0), (sx * 6.0, 4.0, 0), 5, bandf, extend=0.6)
        m.round_box(lg, sx * 6.0, -1.4, 3.6, 4.4, 0.0, 4.0, SK, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 6.0 + (j - 1) * 1.8, 0.8, -5.6), (0, -0.2, -1), 1.2, 2.0, solid(P, "claw"), tip=0.8)
    return m
