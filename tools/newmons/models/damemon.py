"""Damemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the hapless robot. A round silver coiled body like a stack of rings with a red horn on top, a smiling
face panel, a gold-plated limbs with spiked joints, big gold fists, a drill-tipped foot, and a tiny gold figure riding
on its back. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a round silver robot of stacked rings with a red horn and a smiling face panel, gold limbs with spiked joints, "
        "big gold fists and a drill-tipped foot")
BASE = {"silver": (220, 224, 234), "silver_dark": (130, 134, 150), "silver_light": (255, 255, 255), "gold": (240, 200, 50),
        "gold_dark": (170, 120, 10), "red": (220, 40, 40), "black": (30, 30, 36), "eye": (40, 40, 50)}
SHINY = {"silver": (240, 200, 210), "silver_dark": (180, 130, 150), "gold": (90, 200, 230), "gold_dark": (30, 120, 170)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = metal(P, "silver", dark="silver_dark", light="silver_light")
GOLD = armour(P, "gold", "gold_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.6, y - 24.0) < 0.9:
                return tone(p["eye"], face), None
        if abs(y - 21.0 - 0.1 * x * x) < 0.25 and abs(x) < 3.0:
            return tone(p["eye"], face), None
    return SILVER(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("damemon")
    top = m.bone("damemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i, r in enumerate((8.0, 9.0, 9.4, 9.0, 8.0, 6.4)):                          # stacked coil rings
        y0 = 12.0 + i * 3.0
        m.round_box(bd, 0, 0, r, r * 0.86, y0, y0 + 2.8, facef, cut=max(1, round(r * 0.3)))
    hd = m.bone("head", bd, (0, 30, 0))
    spike(m, hd, (0, 30.0, 0), (0, 1, 0), 3.0, 7.0, solid(P, "red"), tip=0.6)        # red horn
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 22.0, 0))
        rod(m, ab, (sx * 9.0, 22.0, 0), (sx * 14.0, 20.0, -2.0), 3, GOLD, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 12.0, 21.0, -1.0), (sx * 0.4, 1 - j, 0.3), 0.8, 2.4, solid(P, "black"))
        m.round_box(ab, sx * 16.0, -3.0, 3.4, 3.4, 16.0, 23.0, GOLD, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 12.0, 0))
        rod(m, lg, (sx * 4.0, 12.0, 0), (sx * 5.0, 3.0, -1.0), 3, GOLD, extend=0.4)
        if sx > 0:
            spike(m, lg, (sx * 5.0, 3.0, -1.0), (0, -1, 0), 2.6, 3.4, SILVER, tip=0.4)  # drill-tipped foot
        else:
            m.box(lg, sx * 5.0 - 2.4, 0.0, -4.0, sx * 5.0 + 2.4, 3.0, 1.6, GOLD)
    rb = m.bone("rider", bd, (0, 32, 6))                                              # tiny gold rider
    m.round_box(rb, 0, 7.0, 1.4, 1.4, 30.0, 33.0, GOLD, cut=1)
    m.round_box(rb, 0, 7.0, 1.2, 1.2, 33.0, 35.0, GOLD, cut=1)
    return m
