"""Lighdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor Digimon of friendship: a sleek black armoured wolf-dragon with blue fins, a long horn and lightning-bolt blades
on its head, a glowing orange core on its chest, yellow-striped joints, a spiked crest down its back and huge silver
claws on its paws. 15 blocks long.

Front is -z, y is up. 32 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 5.4)
KIND = "quadruped"
K = 3
LOOK = "a sleek black armoured wolf-dragon with blue fins, a horn and lightning blades, a glowing orange core and huge silver claws"
BASE = {"black": (40, 40, 48), "black_dark": (12, 12, 16), "black_light": (110, 110, 130), "blue": (60, 140, 230),
        "yellow": (250, 210, 50), "silver": (220, 224, 234), "silver_dark": (110, 114, 126), "orange": (255, 130, 40),
        "orange_light": (255, 220, 140), "eye": (250, 220, 60), "mouth": (160, 40, 40), "tooth": (250, 248, 236)}
SHINY = {"black": (230, 230, 238), "black_dark": (150, 150, 166), "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="yellow", trim_w=0.25)
SIL = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("lighdramon")
    mats = {"skin": ARM, "belly": ARM, "neck": ARM, "head": ARM, "snout": ARM, "jaw": ARM, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "leg_upper": ARM, "leg_lower": ARM, "paw": ARM, "claw": SIL, "tail": ARM}
    a = quadruped(m, mats, "lighdramon", length=26.0, body_y=14.0, body_rx=4.6, body_ry=4.6, chest_bulk=1.3,
                  neck=((0, 18, -12), (0, 20, -16)), head_len=9.0, head_w=3.0, head_h=3.2, snout=1.0, mouth_open=12,
                  teeth=4, leg_bulk=1.3, toes=3, tail=((0, 16, 13), (0, 18, 18)), tail_r=(1.6, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.7, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.7,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, hc[1] + 1.6, hc[2] + 2.0), (sx * 0.5, 0.4, 1), 1.4, 6.0, solid(P, "blue"), tip=0.8)   # fins
        pts = [(sx * 2.0, hc[1] + 3.0, hc[2]), (sx * 4.0, hc[1] + 8.0, hc[2] - 1.0), (sx * 2.6, hc[1] + 9.0, hc[2] + 1.0),
               (sx * 5.0, hc[1] + 14.0, hc[2] - 1.0)]                                  # lightning blades
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "yellow"), extend=0.2, t2=2)
    spike(m, hd, (0, hc[1] + 2.4, hc[2] - 3.0), (0, 1, -0.3), 1.6, 9.0, SIL, tip=0.8)              # long horn
    m.round_box(bd, 0, -10.0, 1.6, 0.6, 15.0, 19.0, gem(P, "orange", "orange_light"), cut=0)         # chest core
    for i in range(6):
        spike(m, bd, (0, 19.0, -8.0 + i * 3.4), (0, 1, 0.6), 1.2, 3.6, ARM, tip=0.8)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        for j in range(3):
            spike(m, a[nm]["bone"], (w[0] + (j - 1) * 1.6, 1.2, w[2] - 2.6), (0, -0.2, -1), 1.4, 4.0, SIL, tip=0.8)
    return m
