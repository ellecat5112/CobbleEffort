"""Boarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor boar of courage. A stocky orange boar charging head-down, its shoulders and back a ridge
of red-and-black fur bursting into flame, a steel nose-guard banded with red stripes over its snout, white tusks,
small fierce eyes, grey cloven hooves wreathed in flame and a lean tail ending in a flame. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, cutout, eye, flame_inside, fur, local, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 16}
LOOK = ("a stocky orange boar with a ridge of red-and-black fur bursting into flame, a steel nose-guard banded red, "
        "white tusks, flame-wreathed grey hooves and a flame-tipped tail")
BASE = {"orange": (246, 140, 30), "orange_dark": (190, 80, 10), "orange_light": (255, 200, 110), "red": (210, 40, 30),
        "red_dark": (90, 16, 10), "black": (34, 26, 24), "steel": (190, 194, 206), "steel_dark": (90, 94, 106),
        "hoof": (120, 120, 130), "tusk": (250, 248, 236), "eye": (250, 210, 60), "pupil": (20, 10, 6),
        "white": (255, 255, 255), "mouth": (110, 20, 20), "flame": (255, 170, 40, 220), "flame_core": (255, 240, 160, 240)}
SHINY = {"orange": (90, 150, 240), "orange_dark": (40, 80, 170), "orange_light": (180, 210, 255), "red": (40, 50, 160),
         "red_dark": (14, 18, 70), "flame": (120, 200, 255, 220), "flame_core": (230, 250, 255, 240)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "orange", "orange_dark", tip="orange_light", length=1.2)
RIDGE = fur(P, "red", "red_dark", tip="black", length=1.6)
STEEL = metal(P, "steel", dark="steel_dark")
HOOF = solid(P, "hoof")


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.3 else p["flame"]
    return c, c[:3]


def guardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (z % 2.4) < 0.7:
        return tone(p["red"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def flame(m, bone, c, w, h, rot, seed):
    m.box(bone, c[0] - w / 2, c[1], c[2], c[0] + w / 2, c[1] + h, c[2], cutout(flame_inside(3, 0.15, seed), flamef),
          rotation=rot, pivot=c)


def build():
    m = Model("boarmon")
    mats = {"skin": FUR, "belly": FUR, "neck": RIDGE, "head": RIDGE, "snout": FUR, "jaw": FUR,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tusk"), "leg_upper": FUR, "leg_lower": FUR, "paw": HOOF,
            "claw": HOOF, "tail": FUR}
    a = quadruped(m, mats, "boarmon", length=24.0, body_y=15.0, body_rx=6.2, body_ry=6.6, chest_bulk=1.3,
                  neck=((0, 17, -12), (0, 15, -16)), head_len=11.0, head_w=4.4, head_h=4.6, snout=0.6, mouth_open=8,
                  teeth=0, leg_bulk=1.3, toes=2, claws=False,
                  tail=((0, 20, 14), (0, 18, 18), (0, 21, 21)), tail_r=(1.0, 0.8, 0.6))
    bd, hd = a["body"], a["head"]
    sf = a["snout_front"]
    my = a["mouth_y"]
    # the steel nose-guard over its snout, banded red, with a flat round nose plate
    m.box(hd, -2.8, my, sf - 0.6, 2.8, my + 3.6, sf + 6.0, guardf)
    m.box(hd, -2.2, my + 0.2, sf - 1.2, 2.2, my + 3.0, sf - 0.4, STEEL)
    for sx in (-1, 1):                                                   # tusks
        spike(m, hd, (sx * 2.6, my, sf + 2.0), (sx * 0.4, 1.0, -0.6), 1.0, 3.2, solid(P, "tusk"), tip=0.4)
        m.box(hd, sx * 4.4 - 0.5, 17.6, -16.6, sx * 4.4 + 0.5, 18.6, -16.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 3.2, 20.0, -14.0), (sx * 0.5, 1, 0.5), 1.8, 2.6, RIDGE)                       # ears
    # the burning ridge along its neck and back
    for i in range(10):
        z = -15.0 + i * 3.0
        y = 21.0 + 1.6 * math.sin(i * 0.4) - (0.2 * i if i > 5 else 0)
        spike(m, bd, (0, y - 1.0, z), (0, 1, 0.5), 3.4, 3.6, RIDGE, tip=1.2)
        flame(m, bd, (0, y + 0.6, z), 6.0, 5.0 + (i % 3) * 1.5, (-30, 90, 0), i)
    # flames round its hooves and on the tail tip
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        lg = a[nm]
        w = lg["wrist"]
        for j, ang in enumerate((0, 90)):
            flame(m, lg["bone"], (w[0], 2.2, w[2] + 1.0), 4.0, 4.0, (-30, ang, 0), j + 20)
    e = a["tail_pts"][-1]
    for j, ang in enumerate((0, 90)):
        flame(m, a["tail"], e, 4.0, 6.0, (0, ang, 0), j + 30)
    return m
