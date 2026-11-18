"""Rubeusdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a crimson dragon-knight lancer: red plate armour heavily trimmed in gold and edged with
white fur, a golden horned dragon helm streaming a great pink mane, black dragon wings, a long golden lance, a
golden crescent shield and a red crystal-spiked tail. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, fur, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a crimson dragon-knight in gold-trimmed red plate with a golden horned helm, a great pink mane, black wings and a golden lance"
BASE = {"red": (190, 30, 40), "red_dark": (100, 10, 16), "gold": (236, 196, 70), "gold_dark": (150, 110, 20),
        "white": (240, 236, 244), "white_dark": (180, 176, 190), "pink": (240, 140, 160), "pink_dark": (190, 80, 110),
        "black": (30, 28, 34), "black_dark": (10, 10, 12), "crystal": (230, 50, 60), "eye": (90, 220, 240)}
SHINY = {"red": (40, 60, 150), "red_dark": (14, 24, 80), "pink": (140, 200, 250), "pink_dark": (80, 140, 210)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "red", "red_dark", trim="gold", trim_w=0.35)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("rubeusdramon")
    mats = {"skin": PLATE, "neck": metal(P, "black"), "knee": GOLD, "talon": GOLD, "claw": GOLD}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.0, leg_bulk=1.05, talons=True, claws=True, digitigrade=True,
                 name="rubeusdramon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.6, 0, 3.6, 3.8, 46.0, 52.0, PLATE, cut=1)
        m.round_box(bd, sx * 8.6, 0, 3.8, 4.0, 45.0, 46.4, fur(P, "white", "white_dark"), cut=1)
        spike(m, bd, (sx * 10.0, 51.0, 0), (sx * 0.8, 1, 0), 1.6, 6.0, GOLD, tip=0.8)
        bat_wing(m, bd, (sx * 4.0, 50.0, 4.0), 26.0, 14.0, 4, metal(P, "black", dark="black_dark"),
                 skin(P, "black", dark="black_dark"), side=sx, sweep=25)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.8, 3.4, 54.0, 60.0, GOLD, cut=1)
    m.box(hd, -1.8, 57.2, -4.5, 1.8, 58.0, -4.3, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.0, -1.0), (sx * 0.4, 1, 0.3), 1.4, 8.0, solid(P, "red"), tip=0.8)
    for j in range(6):                                                                   # great pink mane
        rod(m, hd, (0, 60.0, 1.0 + j * 0.4), ((j - 2.5) * 2.0, 50.0 - j * 2.0, 10.0 + j * 2.0), 2,
            strands(P, "pink", "pink_dark"), extend=0.4)
    w = a["arm_right"]["wrist"]                                                          # golden lance
    rod(m, a["arm_right"]["bone"], (w[0], w[1] - 14.0, w[2] + 8.0), (w[0], w[1] + 24.0, w[2] - 14.0), 1, GOLD,
        extend=0.2)
    spike(m, a["arm_right"]["bone"], (w[0], w[1] + 24.0, w[2] - 14.0), (0, 0.85, -0.5), 1.6, 6.0, GOLD, tip=0.8)
    w = a["arm_left"]["wrist"]                                                           # crescent shield
    for i in range(7):
        ang = math.radians(-60 + i * 20)
        m.box(a["arm_left"]["bone"], w[0] + 1.0, w[1] + 8.0 * math.sin(ang) - 1.4, w[2] - 2.0 + 6.0 * math.cos(ang) - 1.4,
              w[0] + 2.0, w[1] + 8.0 * math.sin(ang) + 1.4, w[2] - 2.0 + 6.0 * math.cos(ang) + 1.4, GOLD)
    tl = m.bone("tail", bd, (0, 32, 4))
    pts = [(0, 32.0, 4.0), (2.0, 22.0, 12.0), (4.0, 12.0, 18.0), (2.0, 4.0, 24.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - i, PLATE, extend=0.4)
        spike(m, tl, p1, (0, 1, 0.3), 1.2, 3.0, gem(P, "crystal", "white", glow=False), tip=0.8)
    return m
