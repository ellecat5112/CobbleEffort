"""Dinobeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the dragon wasp. A crouching insect-dragon with a blue scaled body and arms, dark green armour plates
over its chest and legs, a green helmeted insect head with orange compound eyes and a blue horn, silver spiked
shoulder plates, long clear veined wings, steel claws, a striped thorax and a pointed tail stinger. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, local, metal, scales, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crouching blue insect-dragon in dark green armour with a helmeted insect head, orange compound eyes, silver "
        "spiked shoulders, long clear veined wings and a pointed tail stinger")
BASE = {"blue": (50, 80, 190), "blue_dark": (16, 30, 100), "blue_light": (130, 160, 240), "green": (40, 110, 60),
        "green_dark": (12, 50, 20), "green_light": (110, 190, 120), "silver": (210, 214, 226), "silver_dark": (110, 114, 128),
        "orange": (250, 130, 40), "red": (200, 50, 40), "wing": (230, 240, 255, 120), "vein": (120, 130, 150, 200),
        "mouth": (120, 30, 40), "tooth": (250, 250, 246)}
SHINY = {"blue": (160, 60, 160), "blue_dark": (70, 20, 80), "green": (200, 150, 40), "green_dark": (110, 70, 10)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "blue", "blue_dark", size=1.2, light="blue_light", rim_mix=0.3)
PLATE = armour(P, "green", "green_dark", light="green_light", trim="silver", trim_w=0.25)
SILVER = metal(P, "silver", dark="silver_dark")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 2.6) < 0.25 or abs(v - H * 0.5) < 0.2:
        return p["vein"], None
    return p["wing"], None


def build():
    m = Model("dinobeemon")
    mats = {"skin": HIDE, "belly": PLATE, "neck": HIDE, "head": PLATE, "snout": PLATE, "jaw": PLATE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": SILVER,
            "thigh": PLATE, "shin": PLATE, "foot": HIDE, "talon": SILVER, "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "dinobeemon", hip_y=16.0, hip_z=3.0, chest=(0, 28.0, -3.0), body_r=6.0, chest_r=6.4,
                 neck_top=(0, 34.0, -6.0), head_len=8.0, head_w=4.0, head_h=4.4, mouth_open=10, teeth=3, arm_len=12.0,
                 arm_bulk=1.4, leg_bulk=1.4, stance=4.6, tail=((0, 16, 8), (0, 14, 15), (2, 15, 22)),
                 tail_r=(3.4, 2.4, 1.4))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):                                                     # orange compound eyes
        m.round_box(hd, sx * (ex + 0.2), ez, 0.8, 1.4, ey - 1.2, ey + 1.2, solid(P, "orange", glow=True), cut=0)
    spike(m, hd, (0, ey + 2.0, ez - 2.0), (0, 0.6, -1), 1.6, 5.0, solid(P, "blue"), tip=0.5)   # blue horn
    for sx in (-1, 1):                                                     # spiked shoulder plates
        m.round_box(bd, sx * 6.4, -2.0, 3.0, 3.0, 29.0, 33.0, SILVER, cut=1)
        for j in range(3):
            spike(m, bd, (sx * 7.0, 32.0, -3.0 + j * 1.6), (sx * 0.6, 1, 0.2), 1.0, 3.6, SILVER, tip=0.25)
    for j in range(4):                                                     # striped thorax bands
        m.round_box(bd, 0, 6.0 + j * 2.0, 4.4 - j * 0.4, 1.0, 17.0 + j * 0.6, 19.0 + j * 0.6,
                    solid(P, "red" if j % 2 else "green"), cut=1)
    e = a["tail_pts"][-1]
    spike(m, a["tail"], e, (0.3, 0.4, 1), 2.0, 6.0, SILVER, tip=0.5)        # tail stinger
    for side in (1, -1):                                                   # long clear veined wings
        for j in range(2):
            x0, x1 = sorted((side * 2.0, side * (26.0 - j * 6.0)))
            m.box(bd, x0, 30.0 - j * 3.0, 4.0 + j, x1, 36.0 - j * 3.0, 4.0 + j, wingf,
                  rotation=(0, side * (25 + j * 10), side * (18 - j * 18)), pivot=(side * 2.0, 32.0, 4.0))
    return m
