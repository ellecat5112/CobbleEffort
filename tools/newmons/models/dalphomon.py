"""Dalphomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the golden war-beast. A long crouching four-legged beast clad in gold armour plates with green gem
studs, a fiery orange-and-red feathered mane, enormous curved claws, bandages and cords wrapping its legs, a jade-
tipped tail, and a bone ring halo floating above it. 35 blocks tall.

Front is -z, y is up. 34 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, feathers, gem, metal, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a long crouching golden war-beast with green gem studs, a fiery feathered mane, enormous curved claws, "
        "wrapped legs and a bone ring halo")
BASE = {"gold": (236, 200, 90), "gold_dark": (160, 120, 30), "gold_light": (255, 240, 170), "orange": (240, 130, 40),
        "red": (210, 50, 30), "green": (70, 200, 100), "green_light": (200, 255, 210), "white": (240, 236, 226),
        "claw": (230, 226, 210), "bone": (220, 216, 200), "bone_dark": (150, 146, 130), "cord": (90, 80, 70),
        "mouth": (130, 30, 30), "tooth": (250, 250, 246), "eye": (60, 220, 120)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 150), "gold_light": (255, 255, 255), "orange": (80, 160, 240),
         "red": (40, 80, 200)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="green", trim_w=0.25)
MANE = feathers(P, "orange", "red", size=(1.4, 2.6), tip="gold_light")


def build():
    m = Model("dalphomon")
    mats = {"skin": GOLD, "belly": GOLD, "neck": MANE, "head": GOLD, "snout": GOLD, "jaw": GOLD,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": GOLD, "leg_lower": solid(P, "white"),
            "paw": GOLD, "claw": solid(P, "claw"), "tail": GOLD}
    a = quadruped(m, mats, "dalphomon", length=40.0, body_y=14.0, body_rx=6.4, body_ry=6.0, chest_bulk=1.3,
                  neck=((0, 18, -22), (0, 20, -27)), head_len=10.0, head_w=4.0, head_h=4.0, snout=0.5, mouth_open=10,
                  teeth=4, leg_bulk=1.6, toes=4, tail=((0, 16, 24), (3, 12, 30), (6, 10, 36)), tail_r=(1.4, 1.0, 0.8))
    bd, hd = a["body"], a["head"]
    for i in range(16):                                                       # fiery feathered mane
        ang = math.radians(i * 22.5)
        spike(m, hd, (4.6 * math.cos(ang), 20.0 + 4.0 * math.sin(ang), -24.0), (math.cos(ang), math.sin(ang) + 0.3, 0.8),
              2.4, 7.0, MANE, tip=0.6)
    for j in range(6):                                                        # gem studs along the back
        m.box(bd, -1.0, 20.0, -14.0 + j * 5.6, 1.0, 21.4, -12.6 + j * 5.6, gem(P, "green", "green_light"))
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        lg = a[nm]
        w = lg["wrist"]
        for j in range(4):                                                    # enormous curved claws
            spike(m, lg["bone"], (w[0] + (j - 1.5) * 1.6, 1.2, w[2] - 3.4), (0, 0.2, -1), 1.6, 5.0, solid(P, "claw"),
                  tip=0.4)
        for j in range(3):                                                    # cords
            m.round_box(lg["bone"], w[0], w[2], 2.4, 2.4, 4.0 + j * 2.4, 4.6 + j * 2.4, solid(P, "cord"), cut=1)
    e = a["tail_pts"][-1]
    spike(m, a["tail"], e, (0.4, 0, 1), 1.6, 3.0, gem(P, "green", "green_light"))
    hb = m.bone("ring_halo", bd, (0, 30, 0))                                  # bone ring halo
    for i in range(12):
        ang = i * math.pi / 6
        p0 = (7.0 * math.cos(ang), 30.0, 7.0 * math.sin(ang))
        p1 = (7.0 * math.cos(ang + math.pi / 6), 30.0, 7.0 * math.sin(ang + math.pi / 6))
        rod(m, hb, p0, p1, 1, metal(P, "bone", dark="bone_dark"), extend=0.4, t2=2)
    return m
