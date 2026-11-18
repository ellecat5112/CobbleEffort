"""Grace Novamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the sun-and-moon god: a radiant knight in gold, white and red armour with orange
flame-hair streaming from its helm, glowing blue orbs in its gauntlets, a great halo of cyan crystal blades fanning
behind it and a cape of starry night sky. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a radiant knight in gold, white and red armour with streaming flame-hair, glowing blue orbs, a halo of cyan "
        "crystal blades and a starry night cape")
BASE = {"gold": (240, 200, 70), "gold_dark": (160, 120, 20), "gold_light": (255, 240, 170), "white": (246, 246, 250),
        "white_dark": (180, 184, 200), "red": (210, 40, 40), "flame": (250, 150, 40), "flame_dark": (210, 70, 20),
        "orb": (90, 160, 255), "orb_light": (220, 240, 255), "crystal": (90, 220, 255, 200), "night": (30, 26, 70),
        "star": (250, 250, 255), "eye": (90, 220, 255)}
SHINY = {"gold": (200, 200, 220), "gold_dark": (120, 120, 140), "flame": (120, 200, 255), "flame_dark": (60, 120, 220)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="red", trim_w=0.3)
WHITE = armour(P, "white", "white_dark", trim="gold", trim_w=0.25)


def nightf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (int(x * 3.1) * 7 + int(y * 2.7) * 13 + int(z * 2.3) * 3) % 23 == 0:
        return p["star"], p["star"]
    return tone(p["night"], face), None


def crystalf(x, y, z, face, variant, box=None, **k):
    c = P(variant)["crystal"]
    return c, c[:3]


def build():
    m = Model("gracenovamon")
    mats = {"skin": WHITE, "chest": GOLD, "deltoid": GOLD, "forearm": GOLD, "hand": GOLD, "finger": GOLD,
            "knee": GOLD, "shin": GOLD, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.05, leg_bulk=1.0, name="gracenovamon")
    bd = a["body"]
    m.round_box(bd, 0, -4.0, 2.0, 0.8, 42.0, 46.0, gem(P, "orb", "orb_light"), cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 53.6, 60.0, GOLD, cut=1)
    m.box(hd, -2.0, 57.0, -3.5, 2.0, 57.8, -3.3, solid(P, "eye", glow=True))
    spike(m, hd, (0, 59.6, -2.0), (0, 1, -0.3), 1.4, 6.0, GOLD, tip=0.8)
    for i in range(12):                                                                   # streaming flame hair
        ang = math.radians(-120 + i * 22)
        spike(m, hd, (2.4 * math.sin(ang), 59.0, 1.0 + 1.6 * math.cos(ang) + 1.0), (math.sin(ang) * 1.2, 0.6, 0.8),
              1.8, 10.0 + (i % 3) * 3.0, strands(P, "flame", "flame_dark"), tip=0.8)
    for nm in ("arm_left", "arm_right"):                                                  # glowing blue orbs
        h = a[nm]["hand"]
        m.round_box(a[nm]["bone"], h[0], h[2] - 2.0, 2.2, 2.2, h[1] - 1.0, h[1] + 3.4, gem(P, "orb", "orb_light"), cut=1)
    for i in range(9):                                                                     # halo of crystal blades
        ang = math.radians(15 + i * 18.75)
        spike(m, bd, (6.0 * math.cos(ang), 50.0 + 6.0 * math.sin(ang), 6.0), (math.cos(ang), math.sin(ang), 0.2), 2.4,
              18.0 - abs(i - 4) * 1.6, crystalf, tip=1.0)
    cape(m, bd, 52.0, 22.0, 46.0, nightf, z=5.0, flare=1.1)
    return m
