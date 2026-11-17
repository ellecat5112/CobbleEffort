"""Cannondramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the walking artillery dragon. A low four-legged orange dinosaur clad in gold plate, a steel
helmet with red and blue lights over its snout, two long cannons and a missile pod mounted on its back on blue
hydraulic mounts, ribbed steel hoses, a long tail ending in a segmented steel blade, and white claws. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a low four-legged orange dinosaur in gold plate with a steel helmet, two long back cannons and a missile pod "
        "on blue mounts, ribbed hoses and a steel-bladed tail")
BASE = {"orange": (246, 150, 50), "orange_dark": (190, 90, 20), "orange_light": (255, 210, 140), "gold": (230, 190, 70),
        "gold_dark": (150, 110, 20), "steel": (200, 204, 216), "steel_dark": (90, 94, 106), "blue": (50, 80, 190),
        "blue_dark": (20, 34, 110), "red": (220, 40, 40), "claw": (246, 246, 246), "mouth": (120, 30, 30),
        "tooth": (250, 250, 246), "eye": (250, 220, 60)}
SHINY = {"orange": (110, 170, 90), "orange_dark": (50, 100, 40), "orange_light": (190, 230, 170), "gold": (210, 214, 226),
         "gold_dark": (120, 124, 140)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "orange", "orange_dark", size=1.6, light="orange_light", rim_mix=0.3)
GOLD = armour(P, "gold", "gold_dark", trim="steel", trim_w=0.3, rivets=True)
STEEL = metal(P, "steel", dark="steel_dark")
BLUE = armour(P, "blue", "blue_dark")


def hosef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["steel_dark"] if (x + y + z) % 1.2 < 0.4 else p["steel"], face), None


def build():
    m = Model("cannondramon")
    mats = {"skin": GOLD, "belly": HIDE, "neck": HIDE, "head": STEEL, "snout": STEEL, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": GOLD, "leg_lower": HIDE,
            "paw": GOLD, "claw": solid(P, "claw"), "tail": HIDE}
    a = quadruped(m, mats, "cannondramon", length=30.0, body_y=17.0, body_rx=7.4, body_ry=7.0, chest_bulk=1.2,
                  neck=((0, 22, -17), (0, 25, -22)), head_len=12.0, head_w=4.4, head_h=4.4, snout=0.6, mouth_open=14,
                  teeth=5, leg_bulk=1.6, toes=3,
                  tail=((0, 20, 20), (4, 22, 27), (10, 26, 31), (15, 32, 31)), tail_r=(3.0, 2.2, 1.6, 1.0))
    bd, hd = a["body"], a["head"]
    for sx in (-1, 1):                                                         # helmet lights
        m.box(hd, sx * 4.5 - 0.3, 26.0, -26.0, sx * 4.5 + 0.3, 27.4, -24.0, solid(P, "red" if sx > 0 else "blue"))
        m.box(hd, sx * 2.6 - 0.5, 27.6, -27.3, sx * 2.6 + 0.5, 28.2, -27.0, solid(P, "eye", glow=True))
    spike(m, hd, (0, 29.0, -24.0), (0, 0.6, 1), 1.6, 4.0, STEEL)
    # back mounts with two long cannons and a missile pod
    for sx in (-1, 1):
        m.box(bd, sx * 3.4 - 1.6, 24.0, -6.0, sx * 3.4 + 1.6, 28.0, 4.0, BLUE)
        rod(m, bd, (sx * 3.4, 29.0, 2.0), (sx * 3.4, 33.0, -26.0), 3, STEEL, extend=0)
        rod(m, bd, (sx * 3.4, 33.0, -26.0), (sx * 3.4, 33.6, -30.0), 2, solid(P, "steel_dark"), extend=0)
        m.box(bd, sx * 3.4 - 1.8, 27.0, 0.0, sx * 3.4 + 1.8, 31.0, 6.0, GOLD)
    m.box(bd, -3.0, 24.0, 6.0, 3.0, 30.0, 14.0, BLUE)                          # missile pod
    for i in range(4):
        m.box(bd, -2.4 + (i % 2) * 2.8, 25.0 + (i // 2) * 2.6, 5.6, -0.2 + (i % 2) * 2.8, 27.0 + (i // 2) * 2.6, 6.0,
              solid(P, "red"))
    for sx in (-1, 1):                                                         # ribbed hoses
        rod(m, bd, (sx * 6.0, 22.0, -8.0), (sx * 7.0, 14.0, -14.0), 2, hosef, extend=0.4)
        rod(m, bd, (sx * 6.0, 22.0, 8.0), (sx * 7.4, 14.0, 12.0), 2, hosef, extend=0.4)
    e = a["tail_pts"][-1]                                                      # segmented tail blade
    for j in range(4):
        spike(m, a["tail"], (e[0] - j * 1.2, e[1] - j * 1.6, e[2] + j * 0.4), (0.4, 1, -0.4), 2.0 - j * 0.3, 3.0,
              STEEL)
    return m
