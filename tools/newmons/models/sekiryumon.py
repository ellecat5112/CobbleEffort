"""Sekiryumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a crimson beast-dragon: a stocky red-scaled dragon with a white chest and belly marked in dark
blue, a golden swept mane, wreaths of pale turquoise spirit-flame round its shoulders and back, a long straight sword
held crosswise in its jaws, a thick braided rope collar and white claws. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import cutout, flame_inside, metal, scales, skin, solid, strands, twisted
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a stocky crimson beast-dragon with a white belly, a golden mane, turquoise spirit flames and a long sword held in its jaws"
BASE = {"red": (200, 40, 40), "red_dark": (120, 14, 14), "white": (246, 244, 236), "white_dark": (190, 186, 170),
        "navy": (40, 50, 110), "gold": (240, 200, 90), "gold_dark": (170, 120, 30), "flame": (140, 240, 220, 200),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 120), "rope": (210, 170, 110), "rope_dark": (140, 100, 50),
        "claw": (240, 240, 236), "eye": (60, 160, 90), "mouth": (150, 30, 40), "tooth": (250, 250, 240)}
SHINY = {"red": (60, 60, 70), "red_dark": (20, 20, 26), "flame": (250, 160, 220, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(abs(x) - (y % 5.0) * 0.6) < 0.3:
        return tone(p["navy"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


FLAME = cutout(flame_inside(tongues=3), solid(P, "flame", glow=True))


def build():
    m = Model("sekiryumon")
    mats = {"skin": scales(P, "red", "red_dark", size=1.4), "belly": bellyf, "snout": bellyf, "jaw": bellyf,
            "claw": solid(P, "claw"), "talon": solid(P, "claw"), "tooth": solid(P, "tooth"), "mouth": solid(P, "mouth")}
    a = theropod(m, mats, "sekiryumon", chest=(0, 30.0, -1.0), body_r=7.0, chest_r=6.6, neck_top=(0, 36.0, -4.0),
                 head_len=10.0, head_w=4.0, head_h=4.4, mouth_open=6, arm_len=9.0, arm_bulk=1.4, leg_bulk=1.4,
                 tail=((0, 16, 8), (4, 10, 14), (8, 6, 18)), tail_r=(4.6, 3.4, 2.0))
    hd = a["head"]
    e = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * e[0], sx * (e[0] + 0.2)), e[1] - 0.5, e[2] - 0.8, max(sx * e[0], sx * (e[0] + 0.2)),
              e[1] + 0.5, e[2] + 0.8, solid(P, "eye"))
    st = a["skull_top"]
    z0, z1 = a["skull_z"]
    for j in range(6):                                                                   # golden swept mane
        spike(m, hd, ((j - 2.5) * 0.8, st, z1 - 1.0 + j * 0.3), ((j - 2.5) * 0.2, 0.6, 1), 1.2, 7.0,
              strands(P, "gold", "gold_dark"), tip=0.8)
    my = a["mouth_y"]                                                                    # sword in its jaws
    m.box(hd, -14.0, my - 0.3, z0 + 2.0, 14.0, my + 0.6, z0 + 3.2, metal(P, "steel", dark="steel_dark"))
    m.box(hd, -16.0, my - 0.6, z0 + 2.0, -14.0, my + 0.9, z0 + 3.2, solid(P, "gold"))
    m.round_box(a["body"], 0, -0.4, 6.8, 5.6, 34.0, 36.0, twisted(P, "rope", "rope_dark"), cut=2)   # rope collar
    fb = m.bone("flames", a["body"], (0, 34, 2))                                          # spirit flames
    for j in range(7):
        ang = math.radians(-80 + j * 27)
        c = (8.0 * math.sin(ang), 30.0 + 3.0 * math.cos(ang), 3.0)
        m.box(fb, c[0] - 2.6, c[1], c[2], c[0] + 2.6, c[1] + 9.0, c[2], FLAME,
              rotation=(10, 0, -math.degrees(ang) * 0.5), pivot=c)
    return m
