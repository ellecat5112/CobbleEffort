"""Ragna Lordmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a dragon-lord knight risen from flame: lean violet-blue armour with crimson dragon-head
pauldrons and a crimson horned dragon helm with a cyan visor, long crimson wing-fins sweeping back, a skirt of fire
pouring down where its legs taper into flame, and a great golden cross-hilted sword held aloft. 35 blocks.

Front is -z, y is up. 74 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, metal, solid
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a lean violet-blue dragon-lord knight with a crimson dragon helm, crimson wing-fins, a skirt of fire and a great golden sword"
BASE = {"blue": (70, 70, 150), "blue_dark": (24, 24, 70), "red": (210, 40, 60), "red_dark": (120, 14, 30),
        "gold": (240, 200, 70), "gold_dark": (160, 110, 20), "visor": (90, 230, 250), "fire": (250, 150, 40, 220),
        "fire_core": (255, 230, 120, 230)}
SHINY = {"blue": (200, 200, 214), "blue_dark": (110, 110, 130), "red": (40, 40, 48), "red_dark": (12, 12, 16)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "blue", "blue_dark", trim="red", trim_w=0.2)
CRIMSON = armour(P, "red", "red_dark", trim="gold", trim_w=0.2)
GOLD = metal(P, "gold", dark="gold_dark")
FIRE = cutout(flame_inside(tongues=4), solid(P, "fire", glow=True))


def build():
    m = Model("ragnalordmon")
    mats = {"skin": PLATE, "knee": CRIMSON, "foot": CRIMSON, "hand": CRIMSON}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.75, talons=True, digitigrade=True, name="ragnalordmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # dragon-head pauldrons
        m.round_box(bd, sx * 8.0, -0.6, 3.0, 3.6, 46.0, 51.0, CRIMSON, cut=1)
        spike(m, bd, (sx * 8.0, 48.0, -4.0), (0, -0.2, -1), 2.0, 3.0, CRIMSON, tip=0.8)
        for j in range(3):                                                               # wing-fins
            spike(m, bd, (sx * 4.0, 50.0 - j * 3.0, 3.0), (sx * 0.6, 0.6 - j * 0.3, 1), 1.6, 16.0 - j * 3.0, CRIMSON,
                  tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, CRIMSON, cut=1)                         # dragon helm
    m.round_box(hd, 0, -4.6, 1.6, 1.4, 54.0, 57.0, CRIMSON, cut=0)
    m.box(hd, -1.8, 57.4, -4.5, 1.8, 58.2, -4.3, solid(P, "visor", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.0, 0), (sx * 0.5, 1, 0.6), 1.4, 7.0, CRIMSON, tip=0.8)
    for j in range(8):                                                                   # skirt of fire
        ang = 2 * math.pi * j / 8
        c = (5.0 * math.cos(ang), 0, 5.0 * math.sin(ang))
        m.box(bd, c[0] - 3.0, 0.0, c[2], c[0] + 3.0, 20.0, c[2], FIRE,
              rotation=(0, -math.degrees(ang) + 90, 0), pivot=(c[0], 10.0, c[2]))
    w = a["arm_right"]["wrist"]                                                          # golden sword aloft
    ab = a["arm_right"]["bone"]
    m.box(ab, w[0] - 0.8, w[1] + 4.0, w[2] - 2.0, w[0] + 0.8, w[1] + 34.0, w[2] - 0.4, GOLD,
          rotation=(-10, 0, 0), pivot=(w[0], w[1], w[2]))
    m.box(ab, w[0] - 3.4, w[1] + 2.6, w[2] - 2.0, w[0] + 3.4, w[1] + 4.0, w[2] - 0.4, GOLD)
    m.round_box(ab, w[0], w[2] - 1.2, 1.0, 1.0, w[1] + 4.0, w[1] + 6.0, solid(P, "red"), cut=0)
    return m
