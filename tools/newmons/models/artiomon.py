"""Artiomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a bear-beast warrior of the hunt in her official armour. A crimson armoured bodysuit with dark fur
trim at shoulders, wrists, hips and ankles, a bear-eared helm with a star mark over long white hair, a white
streamer sash, bear paws with dark claws and a long spear with a gold leaf-blade. 35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, fabric, fur, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a bear-beast huntress in a crimson armoured bodysuit with dark fur trim, a bear-eared helm over long white hair, "
        "bear paws and a long spear with a gold leaf-blade")
BASE = {"red": (180, 30, 50), "red_dark": (100, 10, 24), "red_light": (240, 100, 110), "fur": (70, 50, 40),
        "fur_dark": (36, 24, 18), "fur_light": (130, 100, 80), "white": (246, 246, 250), "white_dark": (190, 194, 210),
        "gold": (236, 200, 80), "gold_dark": (170, 130, 40), "gold_light": (255, 240, 170), "skin": (110, 90, 100),
        "claw": (40, 30, 30), "eye": (255, 220, 80), "shaft": (120, 90, 60)}
SHINY = {"red": (40, 60, 140), "red_dark": (16, 24, 80), "red_light": (110, 140, 220), "fur": (200, 190, 170),
         "fur_dark": (140, 130, 110)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", seams=(3.0,))
FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=1.2)
HAIR = strands(P, "white", "white_dark")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def leaf(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = u / max(W, 1e-6)
    return abs(v / max(H, 1e-6) - 0.5) < 0.5 * math.sin(math.pi * t) ** 0.8


def build():
    m = Model("artiomon")
    mats = {"skin": RED, "chest": RED, "abs": RED, "pelvis": RED, "neck": RED, "deltoid": RED, "upper_arm": RED,
            "forearm": RED, "hand": skin(P, "skin"), "finger": skin(P, "skin"), "claw": solid(P, "claw"),
            "thigh": RED, "knee": RED, "shin": RED, "calf": RED, "foot": skin(P, "skin"), "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=1.05, name="artiomon", hand_pose="fist", claws=True,
                 talons=True, chest_depth=0.95)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.3, 2.5, 54.6, 60.6, skin(P, "skin"), cut=1)
    m.box(hd, -2.6, 58.4, -2.8, 2.6, 61.4, 2.8, RED)                                     # helm
    m.box(hd, -0.6, 59.4, -3.0, 0.6, 60.6, -2.8, GOLD)                                   # star mark
    for sx in (-1, 1):
        m.box(hd, sx * 1.0 - 0.5, 57.4, -2.7, sx * 1.0 + 0.5, 58.0, -2.5, solid(P, "eye", glow=True))
        m.round_box(hd, sx * 2.2, 0.0, 1.2, 1.0, 61.0, 63.4, FUR, cut=1)                 # bear ears
    hr = m.bone("mane", hd, (0, 59, 2))
    for i in range(9):                                           # long white hair
        x = -3.0 + i * 0.75
        rod(m, hr, (x, 59.0, 1.6), (x * 1.6, 40.0 - (i % 3) * 3, 6.0), 2, HAIR, extend=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # fur trims
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.2, 50.0, 0.3), 3.6, 3.0, FUR, layers=3)
        wr = a[nm]["wrist"]
        rod(m, ab, wr, (wr[0], wr[1] + 2.0, wr[2]), 4, FUR, extend=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg, an = a[nm]["bone"], a[nm]["ankle"]
        m.round_box(lg, an[0], an[2], 2.6, 2.6, 2.4, 5.0, FUR, cut=1)
    m.box(bd, -5.0, 29.0, -4.4, 5.0, 33.0, 4.2, FUR)                                    # fur hip wrap
    sk = m.bone("skirt", bd, (0, 32, 3))
    for j in range(3):                                           # white streamer sash
        rod(m, sk, (-2.0 + j * 2.0, 32.0, 4.0), (-4.0 + j * 4.0, 10.0, 12.0 + j), 2, fabric(P, "white", "white_dark"),
            extend=0.3, t2=1)
    ar = a["arm_right"]                                          # the spear
    h = ar["hand"]
    sp = m.bone("staff", ar["bone"], h)
    rod(m, sp, (h[0] + 6.0, h[1] - 4.0, h[2] + 20.0), (h[0] - 8.0, h[1] + 4.0, h[2] - 26.0), 1, solid(P, "shaft"),
        extend=0)
    tipc = (h[0] - 8.0, h[1] + 4.0, h[2] - 26.0)
    m.box(sp, tipc[0] - 0.3, tipc[1] - 2.0, tipc[2] - 12.0, tipc[0] + 0.3, tipc[1] + 2.0, tipc[2], GOLD)
    return m
