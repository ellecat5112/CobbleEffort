"""Falcomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little ninja owl. A round brown owl with big teal eyes in a pale mask, a short yellow beak, two black-tipped ear tufts,
a sage-green feathered cloak-wing over each side marked with red chevrons, and big steel talons on its feet. Child
stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, metal, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a round brown ninja owl with big teal eyes in a pale mask, a yellow beak, black-tipped ear tufts, sage-green "
        "cloak-wings with red chevrons and big steel talons")
BASE = {"brown": (120, 90, 70), "brown_dark": (70, 50, 36), "sage": (150, 180, 140), "sage_dark": (90, 120, 90),
        "mask": (240, 236, 220), "eye": (60, 170, 180), "pupil": (16, 16, 20), "beak": (250, 200, 50),
        "black": (30, 28, 30), "red": (200, 40, 40), "steel": (200, 204, 214), "steel_dark": (100, 104, 116)}
SHINY = {"brown": (70, 80, 120), "brown_dark": (30, 36, 70), "sage": (230, 190, 120), "sage_dark": (170, 130, 60)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = feathers(P, "brown", "brown_dark", size=(1.0, 1.6))


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.4, y - 20.0)
            if d < 0.8:
                return tone(p["pupil"], face), None
            if d < 1.8:
                return tone(p["eye"], face), None
            if d < 2.6:
                return tone(p["mask"], face), None
    return BODY(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "north") and abs((y * 0.8) % 3.0 - 1.5 - abs(z) * 0.0) < 0.3 and y < 14.0:
        return tone(p["red"], face), None
    return feathers(P, "sage", "sage_dark", size=(1.2, 2.0))(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("falcomon")
    top = m.bone("falcomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 14.0, 0), 7.0, BODY, layers=6, squash=1.0, ry=8.0)
    hd = m.bone("head", bd, (0, 20, -2))
    m.round_box(hd, 0, -1.0, 5.4, 4.4, 15.0, 24.0, headf, cut=2)
    spike(m, hd, (0, 18.6, -5.4), (0, -0.4, -1), 2.0, 2.6, solid(P, "beak"), tip=0.6)
    for sx in (-1, 1):                                                               # ear tufts
        spike(m, hd, (sx * 3.6, 23.6, 0), (sx * 0.3, 1, 0.2), 1.6, 3.0, BODY, tip=0.4)
        spike(m, hd, (sx * 3.9, 26.0, 0.2), (sx * 0.3, 1, 0.2), 1.0, 1.4, solid(P, "black"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # sage cloak-wings
        ab = m.bone(nm, bd, (sx * 6.0, 16.0, 0))
        x0, x1 = sorted((sx * 5.0, sx * 8.0))
        m.box(ab, x0, 6.0, -5.0, x1, 18.0, 4.0, wingf, rotation=(0, 0, sx * 8), pivot=(sx * 6.0, 16.0, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # big steel talons
        lg = m.bone(nm, top, (sx * 3.0, 5.0, 0))
        rod(m, lg, (sx * 3.0, 6.0, 0), (sx * 3.0, 2.0, -1.0), 2, solid(P, "black"), extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 3.0 + (j - 1) * 1.4, 1.0, -1.6), ((j - 1) * 0.3, -0.3, -1), 1.2, 4.0,
                  metal(P, "steel", dark="steel_dark"), tip=0.3)
    return m
