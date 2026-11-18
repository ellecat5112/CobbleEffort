"""Kaiser Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Hybrid of darkness united: a great armoured lion of black-bronze plates traced with
gold scrollwork, red gems set in its shoulders and flanks, a heavy lion helm with a gold horn and fanged jaws, a gun
barrel on each shoulder, massive gold-taloned paws and a long segmented armoured tail. 25 blocks long.

Front is -z, y is up. 36 units tall; Perfect stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
LOOK = ("a great armoured lion of black-bronze plates traced with gold, red gems in its shoulders, a horned lion helm, "
        "shoulder gun barrels, gold talons and a segmented tail")
BASE = {"bronze": (70, 50, 40), "bronze_dark": (24, 16, 12), "bronze_light": (150, 110, 80), "gold": (240, 200, 90),
        "gold_dark": (160, 120, 30), "red": (220, 40, 40), "red_light": (255, 160, 140), "steel": (190, 194, 206),
        "steel_dark": (90, 94, 106), "mouth": (160, 30, 30), "tooth": (250, 248, 236), "eye": (240, 60, 40)}
SHINY = {"bronze": (220, 220, 232), "bronze_dark": (130, 134, 150), "bronze_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "bronze", "bronze_dark", light="bronze_light", trim="gold", trim_w=0.35,
            engrave=lambda a, b: abs(math.sin(a * 1.3) + math.cos(b * 1.1)) < 0.22)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("kaiserleomon")
    mats = {"skin": ARM, "belly": ARM, "neck": ARM, "head": ARM, "snout": ARM, "jaw": ARM, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "leg_upper": ARM, "leg_lower": ARM, "paw": ARM, "claw": GOLD, "tail": ARM}
    a = quadruped(m, mats, "kaiserleomon", length=30.0, body_y=17.0, body_rx=6.4, body_ry=6.6, chest_bulk=1.35,
                  neck=((0, 22, -14), (0, 25, -18)), head_len=10.0, head_w=4.0, head_h=4.6, snout=0.7, mouth_open=14,
                  teeth=5, leg_bulk=1.6, toes=3,
                  tail=((0, 20, 15), (2, 24, 21), (4, 26, 27), (5, 24, 32)), tail_r=(1.6, 1.4, 1.2, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
              solid(P, "eye", glow=True))
        m.round_box(bd, sx * 7.4, -9.0, 0.6, 2.0, 19.0, 23.0, gem(P, "red", "red_light"), cut=0)     # shoulder gems
        m.round_box(bd, sx * 7.0, 6.0, 0.6, 1.6, 16.0, 19.0, gem(P, "red", "red_light"), cut=0)      # flank gems
        rod(m, bd, (sx * 4.0, 25.0, -8.0), (sx * 4.6, 27.0, -16.0), 1, metal(P, "steel", dark="steel_dark"), extend=0,
            t2=1)                                                                    # shoulder gun barrels
    hc = a["head_c"]
    spike(m, hd, (0, hc[1] + 3.0, hc[2] - 1.0), (0, 0.6, -1), 1.6, 6.0, GOLD, tip=0.8)                 # gold horn
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        for j in range(3):
            spike(m, a[nm]["bone"], (w[0] + (j - 1) * 1.6, 1.2, w[2] - 2.6), (0, -0.2, -1), 1.2, 4.0, GOLD, tip=0.8)
    for p in a["tail_pts"][1:]:
        m.round_box(a["tail"], p[0], p[2], 1.8, 1.8, p[1] - 0.6, p[1] + 0.6, GOLD, cut=0)
    return m
