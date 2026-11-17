"""Deltamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the three-headed composite. A crouching blue dinosaur with a pale belly and a fanged red maw, whose
left arm is a long steel crocodile head with a red eye and whose right arm is a great bone-white dinosaur skull with
horns, plus a tail with a bone spike. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import jaws, theropod
from _digidetail import metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crouching blue dinosaur with a fanged red maw, a long steel crocodile head for its left arm and a horned "
        "bone-white dinosaur skull for its right")
BASE = {"blue": (50, 80, 190), "blue_dark": (16, 30, 100), "blue_light": (130, 160, 240), "belly": (230, 236, 246),
        "belly_dark": (170, 180, 200), "steel": (200, 204, 214), "steel_dark": (90, 94, 104), "bone": (240, 232, 210),
        "bone_dark": (170, 160, 130), "mouth": (200, 40, 50), "tooth": (250, 250, 246), "eye": (230, 40, 40),
        "claw": (230, 230, 236)}
SHINY = {"blue": (60, 150, 80), "blue_dark": (20, 70, 30), "blue_light": (150, 220, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "blue", "blue_dark", size=1.4, light="blue_light", rim_mix=0.3)
BELLY = skin(P, "belly", dark="belly_dark", var=0.03)
STEEL = metal(P, "steel", dark="steel_dark")
BONE = skin(P, "bone", dark="bone_dark", var=0.05)


def B(m, bone, x0, y0, z0, x1, y1, z1, sh):
    """A box with its x range sorted (mirrored arm heads)."""
    m.box(bone, min(x0, x1), y0, z0, max(x0, x1), y1, z1, sh)


def build():
    m = Model("deltamon")
    mats = {"skin": HIDE, "belly": BELLY, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": solid(P, "claw"),
            "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": solid(P, "claw"), "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "deltamon", hip_y=12.0, hip_z=3.0, chest=(0, 22.0, -3.0), body_r=6.0, chest_r=6.0,
                 neck_top=(0, 28.0, -5.0), head_len=9.0, head_w=3.6, head_h=4.0, mouth_open=26, teeth=5, arm_len=6.0,
                 arm_bulk=1.4, leg_bulk=1.5, stance=4.6, tail=((0, 12, 9), (0, 9, 16), (0, 6, 22)),
                 tail_r=(3.6, 2.6, 1.6))
    bd = a["body"]
    for sx in (-1, 1):
        ex, ey, ez = a["eye"]
        m.box(a["head"], min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
              ez + 0.6, solid(P, "eye"))
    al = a["arm_right"]                                                      # steel crocodile head (right arm)
    h = al["hand"]
    cb = m.bone("croc", al["bone"], h)
    g = 1 if h[0] > 0 else -1
    m.round_box(cb, h[0] + g * (4.0), h[2] - 2.0, 3.0, 4.0, h[1] - 2.0, h[1] + 2.4, STEEL, cut=1)
    B(m, cb, h[0] + g * (6.0), h[1] - 1.4, h[2] - 3.0, h[0] + g * (18.0), h[1] + 1.4, h[2] + 0.4, STEEL)
    B(m, cb, h[0] + g * (6.0), h[1] - 2.6, h[2] - 3.0, h[0] + g * (18.0), h[1] - 1.6, h[2] + 0.4, solid(P, "mouth"))
    B(m, cb, h[0] + g * (6.0), h[1] - 3.6, h[2] - 3.0, h[0] + g * (17.0), h[1] - 2.6, h[2] + 0.4, STEEL)
    for j in range(6):
        for zz in (h[2] - 3.0, h[2] + 0.2):
            spike(m, cb, (h[0] + g * (7.0 + j * 1.8), h[1] - 1.4, zz), (0, -1, 0), 0.6, 1.0, solid(P, "tooth"))
    B(m, cb, h[0] + g * (6.4), h[1] + 1.4, h[2] - 3.2, h[0] + g * (7.4), h[1] + 2.2, h[2] - 2.6, solid(P, "eye", glow=True))
    ar = a["arm_left"]                                                       # bone skull (left arm)
    h = ar["hand"]
    sb = m.bone("skull", ar["bone"], h)
    g = 1 if h[0] > 0 else -1
    m.round_box(sb, h[0] + g * (4.0), h[2] - 1.0, 4.0, 5.0, h[1] - 2.0, h[1] + 4.6, BONE, cut=2)
    B(m, sb, h[0] + g * (7.0), h[1] - 4.6, h[2] - 5.0, h[0] + g * (1.0), h[1] - 2.0, h[2] + 1.0, BONE)          # lower jaw
    for j in range(4):
        spike(m, sb, (h[0] + g * (6.4 + j * 1.6), h[1] - 2.0, h[2] - 5.4), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"))
    for sx in (-1, 1):
        B(m, sb, h[0] + g * (4.0) + sx * 1.6 - 0.8, h[1] + 1.6, h[2] - 6.2, h[0] + g * (4.0) + sx * 1.6 + 0.8, h[1] + 3.0,
              h[2] - 5.8, solid(P, "mouth"))
    spike(m, sb, (h[0] + g * (4.0), h[1] + 4.0, h[2] + 2.0), (-0.3, 0.6, 1), 1.6, 7.0, BONE, tip=0.5)
    e = a["tail_pts"][-1]
    spike(m, a["tail"], e, (0, 0.2, 1), 1.6, 4.0, BONE, tip=0.4)
    return m
