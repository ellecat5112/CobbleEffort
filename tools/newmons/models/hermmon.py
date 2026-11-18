"""Hermmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the manga sketch on wikimon.net): the
heavy-armoured messenger: a hulking armoured giant in grey plate with a tall pointed crested helm flaring with small
flames, broad layered shoulder plates, banded arms ending in great gauntlets, and segmented armoured legs. 35 blocks.

Front is -z, y is up. 72 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking grey-armoured giant with a tall pointed crested helm, layered shoulder plates and great gauntlets"
BASE = {"grey": (170, 172, 180), "grey_dark": (80, 82, 90), "grey_light": (230, 232, 238), "black": (34, 32, 38),
        "eye": (240, 220, 60), "flame": (255, 160, 60)}
SHINY = {"grey": (210, 180, 90), "grey_dark": (140, 110, 30), "grey_light": (250, 230, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "grey", "grey_dark", light="grey_light", trim="black", trim_w=0.3, rivets=True)


def build():
    m = Model("hermmon")
    mats = {"skin": riveted(P, "black", "grey_dark"), "chest": ARM, "deltoid": ARM, "forearm": ARM, "hand": ARM,
            "finger": ARM, "thigh": ARM, "knee": ARM, "shin": ARM, "calf": ARM, "foot": ARM}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.3, leg_bulk=1.2, name="hermmon")
    bd = a["body"]
    for sx in (-1, 1):
        for j in range(3):
            m.round_box(bd, sx * (8.6 + j * 0.6), 0.4, 3.8 - j * 0.4, 4.4, 50.0 - j * 3.0, 54.0 - j * 3.0, ARM, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.4, 53.4, 60.0, ARM, cut=1)
    m.box(hd, -2.0, 57.0, -4.1, 2.0, 57.8, -3.9, solid(P, "eye", glow=True))
    spike(m, hd, (0, 59.6, 0), (0, 1, 0.15), 3.4, 12.0, ARM, tip=1.2)                    # tall pointed helm
    for j in range(4):
        spike(m, hd, ((j - 1.5) * 1.6, 60.0, 2.0), ((j - 1.5) * 0.4, 1, 0.4), 0.9, 3.0, solid(P, "flame", glow=True),
              tip=0.8)
    for nm in ("arm_left", "arm_right"):
        h = a[nm]["hand"]
        m.round_box(a[nm]["bone"], h[0], h[2] - 0.4, 3.0, 3.0, h[1] - 2.0, h[1] + 3.0, ARM, cut=1)
    return m
