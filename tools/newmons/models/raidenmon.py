"""Raidenmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a walking fortress: a squat camouflage-green armoured war machine on tank-track feet, a heavy
cannon arm and a jointed hose arm ending in a twin nozzle, a round head turret with one sullen eye, and two great
drum magazines on its back stamped with gold discs. 35 blocks.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, noise2, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 3}
LOOK = "a squat camouflage-green war machine on tank-track feet with a heavy cannon arm, a hose arm and two great drum magazines"
BASE = {"green": (80, 140, 70), "green_dark": (30, 80, 30), "camo": (200, 200, 150), "steel": (150, 154, 160),
        "steel_dark": (70, 74, 80), "gold": (240, 190, 60), "gold_dark": (170, 110, 20), "eye": (220, 40, 40),
        "black": (24, 24, 28), "track": (40, 60, 40)}
SHINY = {"green": (170, 140, 90), "green_dark": (100, 76, 40), "camo": (230, 220, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def camof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    n = noise2(x * 0.25 + z * 0.2, y * 0.25, 9)
    if n > 0.68:
        return tone(p["camo"], face), None
    if n < 0.3:
        return tone(p["green_dark"], face), None
    return armour(P, "green", "green_dark")(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def drumf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and math.hypot(x - (6.0 if x > 0 else -6.0), y - 40.0) < 4.0:
        return tone(p["gold"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("raidenmon")
    top = m.bone("raidenmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 11.0, 9.0, 12.0, 30.0, camof, cut=3)                              # hull
    m.round_box(bd, 0, 0, 9.0, 7.0, 30.0, 34.0, camof, cut=2)
    hd = m.bone("head", bd, (0, 34, -2))
    ball(m, hd, (0, 37.0, -4.0), 5.0, camof, layers=4, ry=4.0)                             # head turret
    m.box(hd, -2.4, 37.0, -9.1, 0.6, 39.0, -8.8, solid(P, "eye", glow=True))
    m.box(hd, -3.0, 39.4, -9.2, 1.2, 40.4, -8.8, solid(P, "green_dark"))
    for sx in (-1, 1):                                                                   # drum magazines
        rod(m, bd, (sx * 6.0, 40.0, 4.0), (sx * 6.0, 40.0, 14.0), 9, drumf, extend=0.2)
    rod(m, bd, (0, 30.0, 6.0), (0, 34.0, 9.0), 3, STEEL, extend=0.2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 11.0, 24.0, 0))
        if sx > 0:                                                                       # heavy cannon arm
            m.round_box(ab, 15.0, -4.0, 4.0, 6.0, 18.0, 26.0, camof, cut=2)
            rod(m, ab, (15.0, 22.0, -8.0), (15.0, 22.0, -22.0), 3, STEEL, extend=0.4)
            m.round_box(ab, 15.0, -22.2, 1.0, 0.4, 21.0, 23.0, solid(P, "black"), cut=0)
        else:                                                                            # jointed hose arm
            pts = [(-11.0, 24.0, 0), (-16.0, 18.0, -2.0), (-18.0, 10.0, -6.0), (-16.0, 6.0, -10.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 3, camof, extend=0.6)
            for dx in (-1.2, 1.2):
                rod(m, ab, (-16.0 + dx, 6.0, -10.0), (-16.0 + dx, 6.0, -14.0), 1, STEEL, extend=0.2, t2=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # tank-track feet
        lg = m.bone(nm, top, (sx * 6.0, 12.0, 0))
        m.round_box(lg, sx * 6.0, 0, 3.6, 3.6, 6.0, 13.0, STEEL, cut=1)
        m.box(lg, sx * 6.0 - 4.4, 0.0, -10.0, sx * 6.0 + 4.4, 7.0, 10.0, solid(P, "track"))
        for j in range(8):
            m.box(lg, sx * 6.0 - 4.6, 0.0, -10.0 + j * 2.6, sx * 6.0 + 4.6, 7.0, -9.0 + j * 2.6, solid(P, "black"))
    return m
