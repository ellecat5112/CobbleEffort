"""Big Mamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an oversized Mamemon. A huge round dark steel ball of a body with a smug half-lidded face and a
crossed bandage plaster, big red boxing-glove fists with bolts, heavy boots with "BIG" on the soles, and tiny
Mamemon floating round it. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, leather, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("an oversized Mamemon: a huge round dark steel ball with a smug face and a crossed plaster, big red boxing-glove "
        "fists with bolts, heavy boots and tiny Mamemon floating round it")
BASE = {"steel": (90, 92, 104), "steel_dark": (36, 36, 44), "steel_light": (190, 192, 206), "red": (210, 30, 40),
        "red_dark": (120, 10, 20), "red_light": (250, 120, 120), "boot": (110, 80, 60), "boot_dark": (60, 40, 26),
        "plaster": (240, 210, 170), "black": (26, 26, 30), "white": (250, 250, 250), "bolt": (200, 204, 216),
        "eye": (240, 60, 60)}
SHINY = {"steel": (200, 170, 100), "steel_dark": (130, 100, 40), "steel_light": (250, 230, 170), "red": (40, 100, 220),
         "red_dark": (16, 50, 140), "red_light": (130, 180, 255)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark", light="steel_light")
RED = armour(P, "red", "red_dark", light="red_light")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(b - 30.0) < 0.5 and abs(a - sx * 3.6) < 1.6:
                return (p["eye"] if abs(b - 29.8) < 0.25 and abs(a - sx * 3.6) < 0.6 else p["black"]), None
        if abs(a) < 1.6 and 25.4 < b < 26.8:
            return p["white"], None                              # buck teeth
        if abs(abs(a) - abs(b - 18.0)) < 0.7 and abs(a) < 2.4:
            return tone(p["plaster"], face), None                # crossed plaster
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bigmamemon")
    top = m.bone("bigmamemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    ball(m, bd, (0, 24.0, 0), 15.0, bodyf, layers=9)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 14.0, 32.0, 0))
        rod(m, ab, (sx * 13.0, 32.0, 0), (sx * 17.0, 38.0, -2.0), 3, STEEL, extend=0.3)
        c = (sx * 19.0, 41.0, -2.0)
        m.round_box(ab, c[0], c[2], 4.0, 3.6, c[1] - 3.6, c[1] + 3.6, RED, cut=1)
        for j in range(3):
            ball(m, ab, (c[0] - sx * 1.0 + (j - 1) * 1.6, c[1] + 3.6, c[2] - 2.0), 0.8, solid(P, "bolt"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):          # heavy boots
        lg = m.bone(nm, top, (sx * 9.0, 10.0, 0))
        rod(m, lg, (sx * 8.0, 11.0, 0), (sx * 12.0, 5.0, -1.0), 3, STEEL, extend=0.3)
        m.round_box(lg, sx * 13.0, -1.0, 4.0, 5.0, 0.0, 6.0, leather(P, "boot", "boot_dark", stitch="black"), cut=1)
    for i, c in enumerate(((-18.0, 44.0, 2.0), (16.0, 8.0, -4.0), (-14.0, 4.0, -6.0))):
        ball(m, bd, c, 1.8, STEEL, layers=2)                     # tiny Mamemon
        for sx in (-1, 1):
            rod(m, bd, (c[0] + sx * 1.6, c[1], c[2]), (c[0] + sx * 3.0, c[1] + 1.0, c[2]), 1, solid(P, "red"),
                extend=0)
    return m
