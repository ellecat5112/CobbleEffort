"""Asuramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a wrathful guardian deity. Heavily muscled slate-grey skin with veins over its arms and chest, a
crimson mask band across its eyes, a blazing mane of flame, a golden ring-halo behind it, a necklace of white beads,
golden armoured trousers with a crimson sash, flames burning round its fists and feet. 25 blocks tall.

Front is -z, y is up. 70 units tall (the halo); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid, shell
from _digidetail import Bulge, armour, cutout, fabric, flame_inside, local, metal, skin, solid, torso_bulges
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a wrathful guardian deity: muscled slate-grey skin with veins, a crimson mask band, a blazing flame mane, a "
        "gold ring-halo, white bead necklace, golden armoured trousers and flames round its fists and feet")
BASE = {"skin": (110, 112, 122), "skin_dark": (50, 52, 60), "skin_light": (180, 184, 196), "vein": (90, 92, 104),
        "gold": (240, 200, 60), "gold_dark": (170, 120, 30), "gold_light": (255, 240, 170), "red": (200, 30, 40),
        "red_dark": (120, 10, 20), "white": (246, 244, 236), "flame": (255, 140, 40, 220),
        "flame_core": (255, 230, 110, 235), "eye": (255, 230, 80), "violet": (110, 60, 170)}
SHINY = {"skin": (170, 110, 80), "skin_dark": (100, 56, 36), "skin_light": (230, 180, 150), "vein": (140, 86, 60),
         "flame": (90, 170, 255, 220), "flame_core": (200, 240, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


CHEST = skin(P, "skin", dark="skin_dark", light="skin_light", bulges=torso_bulges(0, 51.0, 5.6, abs_rows=4),
             vein_key="vein", vein_rects=(((-6, 34, 6, 51), ("north",), 4),), vein_count=4, vein_width=0.3, var=0.03)
ARM = skin(P, "skin", dark="skin_dark", light="skin_light", vein_key="vein",
           vein_rects=(((-14, 26, 14, 50), ("north", "east", "west"), 6),), vein_count=3, vein_width=0.3,
           bulges=[Bulge("north", sx * 8.8, 42.0, 1.8, 3.6, light=0.35, shadow=0.45) for sx in (-1, 1)], var=0.03)
GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="red")
GOLD_M = metal(P, "gold", dark="gold_dark", light="gold_light")


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
    return c, c[:3]


def build():
    m = Model("asuramon")
    mats = {"skin": ARM, "chest": CHEST, "abs": CHEST, "pelvis": GOLD, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": GOLD, "knee": GOLD, "shin": GOLD, "calf": GOLD,
            "foot": ARM, "toe": ARM}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.35, leg_bulk=1.25, name="asuramon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.6, 60.8, ARM, cut=1)
    m.box(hd, -2.8, 57.0, -3.4, 2.8, 58.8, 2.8, solid(P, "red"))                         # mask band
    for sx in (-1, 1):
        m.box(hd, sx * 1.1 - 0.5, 57.6, -3.5, sx * 1.1 + 0.5, 58.2, -3.4, solid(P, "eye", glow=True))
    m.box(hd, -0.8, 58.8, -3.2, 0.8, 60.4, -2.8, solid(P, "violet"))                      # brow jewel
    fl = m.bone("mane", hd, (0, 61, 0))
    for ang in (0, 45, 90, 135):                                 # blazing flame mane
        m.box(fl, -6.0, 58.0, 0, 6.0, 72.0, 0, cutout(flame_inside(5, 0.0, ang // 45), flamef),
              rotation=(0, ang, 0), pivot=(0, 60, 0))
    halo = m.bone("ring_halo", bd, (0, 60, 6))                   # the gold ring halo
    for i in range(16):
        ang = math.radians(i * 22.5)
        c = (11.0 * math.cos(ang), 60.0 + 11.0 * math.sin(ang), 6.0)
        m.box(halo, c[0] - 0.9, c[1] - 2.2, c[2] - 0.9, c[0] + 0.9, c[1] + 2.2, c[2] + 0.9, GOLD_M,
              rotation=(0, 0, math.degrees(ang)), pivot=c)
    for i in range(14):                                          # white bead necklace
        ang = math.radians(-90 + i * (180 / 13))
        c = (4.4 * math.sin(ang), 51.0 - 4.0 * math.cos(ang) ** 2, -4.6 * math.cos(ang) * 0.9 - 0.2)
        ball(m, bd, c, 0.7, solid(P, "white"), layers=2)
    m.box(bd, -5.4, 30.6, -4.4, 5.4, 33.4, 4.2, fabric(P, "red", "red_dark"))            # crimson sash
    m.box(bd, -1.4, 18.0, -4.8, 1.4, 31.0, -4.2, fabric(P, "red", "red_dark"))
    for nm in ("arm_left", "arm_right"):                         # flames round the fists
        h = a[nm]["hand"]
        for ang in (0, 90):
            m.box(a[nm]["bone"], h[0] - 3.0, h[1] - 2.0, h[2], h[0] + 3.0, h[1] + 8.0, h[2],
                  cutout(flame_inside(3, 0.0, 3), flamef), rotation=(0, ang, 0), pivot=h)
    for nm in ("leg_left", "leg_right"):
        an = a[nm]["ankle"]
        m.box(a[nm]["bone"], an[0] - 3.0, 0.0, an[2] - 2.0, an[0] + 3.0, 9.0, an[2] - 2.0,
              cutout(flame_inside(3, 0.0, 4), flamef))
    return m
