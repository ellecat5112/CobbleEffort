"""Galemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the gale bird-dragon: a lean green dragon with a white-furred collar and cuffs, a pale belly with a
green spiral mark, a sharp beaked head with a red crest, great green wings fading to orange and black at the tips,
a long tail tipped with red feather plumes and red talons. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing, theropod
from _digidetail import feathers, fur, local, scales, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean green bird-dragon with a white fur collar, a pale belly with a spiral mark, a red crest, great green "
        "wings fading to orange and black, a red-plumed tail and red talons")
BASE = {"green": (50, 150, 80), "green_dark": (20, 80, 40), "green_light": (130, 220, 140), "belly": (230, 236, 210),
        "belly_dark": (180, 190, 160), "white": (246, 246, 246), "white_dark": (190, 190, 200), "red": (210, 30, 40),
        "orange": (250, 160, 40), "black": (30, 28, 30), "eye": (250, 220, 60), "mouth": (110, 20, 30),
        "tooth": (250, 250, 246)}
SHINY = {"green": (60, 110, 200), "green_dark": (20, 50, 130), "green_light": (140, 180, 250)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.4, light="green_light")


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x, y - 26.0)
        if r < 3.0 and (math.atan2(y - 26.0, x) + r * 1.4) % 2.4 < 0.6:
            return tone(p["green"], face), None
    return skin(P, "belly", dark="belly_dark")(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = min(1.0, abs(x) / 22.0)
    if t > 0.85:
        return tone(p["black"], face), None
    if t > 0.6:
        return tone(p["orange"], face), None
    return feathers(P, "green", "green_dark", size=(1.2, 2.2))(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("galemon")
    mats = {"skin": HIDE, "belly": bellyf, "neck": HIDE, "head": HIDE, "jaw": HIDE, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": solid(P, "red"), "thigh": HIDE,
            "shin": HIDE, "foot": solid(P, "black"), "talon": solid(P, "red"), "tail": HIDE}
    a = theropod(m, mats, "galemon", hip_y=16.0, chest=(0, 27.0, -2.0), body_r=4.6, chest_r=4.6,
                 neck_top=(0, 35.0, -5.0), head_len=8.0, head_w=2.8, head_h=3.2, mouth_open=10, teeth=4,
                 arm_len=7.0, leg_bulk=0.8, tail=((0, 15, 8), (0, 12, 16), (0, 10, 24), (0, 9, 32)),
                 tail_r=(3.0, 2.2, 1.4, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
    sf = (0, a["mouth_y"] + 1.0, a["snout_front"])
    spike(m, hd, sf, (0, -0.6, -1), 1.6, 2.6, solid(P, "black"), tip=0.8)                # hooked beak tip
    for j in range(3):                                                                    # red crest
        spike(m, hd, (0, ey + 2.4, ez + 1.0 + j * 1.6), (0, 1, 0.7), 1.0, 5.0 - j, solid(P, "red"), tip=0.8)
    m.round_box(bd, 0, -2.0, 5.4, 4.6, 30.0, 33.6, fur(P, "white", "white_dark", length=1.2), cut=2)   # fur collar
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 31.0, 2.0))
        feather_wing(m, wb, (side * 4.0, 31.0, 2.0), 20.0, 9.0, 3, wingf, side=side, sweep=25, droop=2.0)
    e = a["tail_pts"][-1]
    for j in range(3):                                                                    # red tail plumes
        spike(m, a["tail"], e, ((j - 1) * 0.5, 0.2, 1), 1.2, 5.0, solid(P, "red"), tip=0.8)
    return m
