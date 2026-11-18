"""Jumbo Gamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the great armoured turtle: a green crocodile-headed turtle standing upright under a huge red
tortoise shell plated in segments, a giant missile cannon on its back, a drill and a gatling barrel for arms, armoured
green legs with heavy grey tread-plate feet and black claws. 35 blocks tall.

Front is -z, y is up. 46 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 46
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a green crocodile-headed turtle under a huge red segmented shell with a giant missile cannon on its back, a "
        "drill and a gatling arm and heavy tread feet")
BASE = {"green": (60, 140, 60), "green_dark": (20, 70, 20), "green_light": (140, 210, 120), "red": (210, 40, 30),
        "red_dark": (120, 14, 10), "red_light": (250, 130, 110), "steel": (200, 204, 216), "steel_dark": (80, 84, 96),
        "black": (30, 30, 34), "yellow": (250, 210, 60), "eye": (250, 220, 60), "mouth": (180, 40, 50),
        "tooth": (250, 250, 246), "cream": (240, 226, 180)}
SHINY = {"green": (60, 110, 200), "green_dark": (20, 40, 130), "red": (230, 190, 50), "red_dark": (150, 110, 10)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.4, light="green_light")
STEEL = metal(P, "steel", dark="steel_dark")


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (round(y / 4.0) * 4.0 - y) ** 2 < 0.1 or (math.atan2(x, z) * 3.0) % 1.0 < 0.08:
        return tone(p["red_dark"], face), None
    return armour(P, "red", "red_dark", light="red_light")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jumbogamemon")
    top = m.bone("jumbogamemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 24.0, 3.0), 11.0, shellf, layers=7, squash=1.0)                   # huge red shell
    m.round_box(bd, 0, -6.0, 7.0, 3.0, 15.0, 31.0, armour(P, "cream", "cream"), cut=2)  # belly plate
    hd = m.bone("head", bd, (0, 32, -6))
    m.round_box(hd, 0, -8.0, 3.0, 5.0, 31.0, 36.0, HIDE, cut=1)                          # crocodile head
    m.round_box(hd, 0, -11.0, 2.6, 3.4, 28.4, 31.0, HIDE, cut=1)
    m.round_box(hd, 0, -11.0, 2.2, 3.0, 31.0, 31.6, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.6, sx * 3.1), 34.4, -9.0, max(sx * 2.6, sx * 3.1), 35.4, -7.4, solid(P, "eye", glow=True))
        for j in range(3):
            spike(m, hd, (sx * 2.0, 31.0, -13.0 + j * 1.6), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    cb = m.bone("cannon", bd, (6, 32, 8))                                            # giant missile cannon
    rod(m, cb, (6.0, 30.0, 10.0), (10.0, 46.0, 4.0), 4, STEEL, extend=0.8)
    rod(m, cb, (10.0, 44.0, 4.6), (11.0, 48.0, 3.4), 5, armour(P, "red", "red_dark"), extend=0)
    m.round_box(cb, 11.0, 3.4, 2.4, 2.4, 47.6, 48.6, solid(P, "black"), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 27.0, -2.0))
        rod(m, ab, (sx * 9.0, 27.0, -2.0), (sx * 13.0, 22.0, -6.0), 3, HIDE, extend=0.6)
        if sx > 0:                                                                   # drill
            spike(m, ab, (sx * 13.0, 22.0, -6.0), (0.3, -0.1, -1), 3.0, 10.0, STEEL, tip=0.8)
        else:                                                                        # gatling barrel
            rod(m, ab, (sx * 13.0, 22.0, -6.0), (sx * 18.0, 22.0, -16.0), 3, STEEL, extend=0.4)
            m.round_box(ab, sx * 18.4, -16.8, 2.4, 0.8, 19.6, 24.4, solid(P, "black"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 14.0, 0))
        rod(m, lg, (sx * 6.0, 15.0, 0), (sx * 7.0, 5.0, -1.0), 4, HIDE, extend=0.6)
        m.round_box(lg, sx * 7.0, -3.0, 4.0, 6.0, 0.0, 4.0, STEEL, cut=1)               # tread-plate feet
        for j in range(3):
            m.box(lg, sx * 7.0 - 4.2, 0.4 + j * 1.2, -9.2, sx * 7.0 + 4.2, 1.0 + j * 1.2, -8.8, solid(P, "black"))
    return m
