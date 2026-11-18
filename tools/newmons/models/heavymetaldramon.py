"""Heavy Metaldramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the wicked metal dragon: a violet-and-silver armoured dragon with a skull-like dragon
head and green mane, great black bat wings tipped with gold claws breathing icy mist, a long violet serpent tail
banded silver underneath ending in a black cable lash, gold-clawed arms and a fanged chest. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digidetail import armour, metal, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "floater"
K = 3
LOOK = ("a violet-and-silver armoured dragon with a skull head and green mane, black bat wings tipped gold, a long "
        "violet serpent tail and gold-clawed arms")
BASE = {"violet": (90, 70, 150), "violet_dark": (40, 30, 90), "violet_light": (150, 130, 210), "silver": (210, 214, 224),
        "silver_dark": (110, 114, 126), "gold": (230, 190, 70), "gold_dark": (150, 110, 20), "black": (30, 28, 34),
        "green": (60, 200, 120), "eye": (240, 40, 60), "ice": (180, 230, 255, 140)}
SHINY = {"violet": (160, 40, 50), "violet_dark": (90, 14, 20), "violet_light": (220, 110, 120)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "violet", "violet_dark", light="violet_light", trim="silver", trim_w=0.3)
SILVER = metal(P, "silver", dark="silver_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def tailf(x, y, z, face, variant, box=None, **k):
    if face in ("down", "north") or (face in ("east", "west") and y < (box.lo[1] + box.size[1] * 0.4)):
        return SILVER(x, y, z, face, variant, box=box, **k)
    return scales(P, "violet", "violet_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("heavymetaldramon")
    top = m.bone("heavymetaldramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 30.0, 46.0, ARM, cut=2)
    for j in range(5):                                                                   # fanged chest
        spike(m, bd, ((j - 2) * 2.0, 38.0, -5.0), (0, -0.6, -1), 1.0, 3.0, SILVER, tip=0.8)
    hd = m.bone("head", bd, (0, 46, -4))
    m.round_box(hd, 0, -6.0, 3.4, 6.0, 46.0, 52.0, SILVER, cut=1)                         # skull dragon head
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.4, sx * 3.6), 49.4, -9.0, max(sx * 3.4, sx * 3.6), 50.4, -7.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.4, 52.0, -3.0), (sx * 0.6, 0.6, 1), 1.4, 7.0, GOLD, tip=0.8)
    for j in range(6):
        spike(m, hd, (0, 51.0, -2.0 + j * 1.6), (0.2 * (j % 2 - 0.5), 0.6, 1), 1.4, 6.0, strands(P, "green", "violet"),
              tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 44.0, 4.0))
        bat_wing(m, wb, (side * 5.0, 44.0, 4.0), 24.0, 16.0, 4, GOLD, skin(P, "black", dark="black"), side=side, sweep=20)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 42.0, -1.0))
        rod(m, ab, (sx * 6.0, 42.0, -1.0), (sx * 11.0, 34.0, -5.0), 3, ARM, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 11.0 + (j - 1) * 1.0, 33.0, -6.0), (sx * 0.3, -0.6, -1), 1.0, 4.0, GOLD, tip=0.8)
    tb = m.bone("tail", bd, (0, 30, 0))                                                   # long serpent tail
    pts = [(0, 30.0, 0), (2.0, 22.0, 4.0), (-3.0, 14.0, 6.0), (2.0, 8.0, 2.0), (8.0, 4.0, 4.0), (14.0, 6.0, 8.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, max(2, 6 - j), tailf, extend=0.6)
    rod(m, tb, pts[-1], (20.0, 2.0, 10.0), 1, solid(P, "black"), extend=0, t2=1)
    return m
