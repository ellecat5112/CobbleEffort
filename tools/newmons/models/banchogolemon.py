"""Bancho Golemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the delinquent boss golem. A massive grey stone-armoured body of rounded rock plates
with bronze joints, a lion-maned stone face with a burning orange core in its chest, a tattered violet long coat
flapping from its shoulders and a stone drill-fist. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, dome, humanoid, shell
from _digidetail import armour, cutout, fabric, gem, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("the delinquent boss golem: grey stone-armoured body with bronze joints, a maned stone face, a burning orange "
        "chest core, a tattered violet long coat and a stone drill-fist")
BASE = {"stone": (150, 150, 156), "stone_dark": (80, 80, 88), "stone_light": (210, 210, 216), "bronze": (170, 110, 60),
        "bronze_dark": (100, 60, 30), "violet": (90, 60, 140), "violet_dark": (40, 24, 70), "core": (255, 140, 40),
        "core_light": (255, 230, 150), "mane": (110, 90, 70), "mane_dark": (60, 46, 34), "eye": (255, 200, 60)}
SHINY = {"stone": (190, 160, 110), "stone_dark": (120, 90, 50), "stone_light": (240, 220, 170), "violet": (40, 110, 80),
         "violet_dark": (16, 60, 40), "core": (60, 200, 255), "core_light": (200, 240, 255)}


def P(v):
    return pal(BASE, SHINY, v)


STONE = armour(P, "stone", "stone_dark", light="stone_light", panel=(3.0, 2.6))
BRONZE = metal(P, "bronze", dark="bronze_dark")
COAT = fabric(P, "violet", "violet_dark", axis="y", period=3.0)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.12 * abs(math.sin((box.lo[0] + u) * 1.8)) + 0.03


def build():
    m = Model("banchogolemon")
    mats = {"skin": BRONZE, "chest": STONE, "abs": STONE, "pelvis": STONE, "neck": BRONZE, "deltoid": STONE,
            "upper_arm": BRONZE, "forearm": STONE, "hand": STONE, "finger": STONE, "thigh": STONE, "knee": BRONZE,
            "shin": STONE, "calf": STONE, "foot": STONE, "toe": STONE}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.5, leg_bulk=1.45, name="banchogolemon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.0, 54.4, 61.0, STONE, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.6, 58.0, -3.7, sx * 1.2 + 0.6, 58.8, -3.5, solid(P, "eye", glow=True))
    for i in range(14):                                          # stone lion mane
        ang = math.radians(i * (360 / 14))
        spike(m, hd, (3.0 * math.cos(ang), 58.0 + 3.0 * math.sin(ang), 0.6), (math.cos(ang), math.sin(ang), 0.4),
              2.0, 3.6, strands(P, "mane", "mane_dark"), tip=0.8)
    shell(m, bd, (0, 0, 0.6), 7.2, 41.0, 52.0, -85, 85, 9, 1.4, STONE)
    m.box(bd, -2.0, 44.0, -8.6, 2.0, 48.0, -7.4, gem(P, "core", "core_light"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        ball(m, ab, (sh[0] + sx * 2.0, 50.0, 0.3), 5.6, STONE, layers=4)
    ar = a["arm_right"]                                          # the drill-fist
    h = ar["hand"]
    for j in range(5):
        r = 4.0 - j * 0.7
        m.box(ar["bone"], h[0] - r, h[1] - 3.0 - j * 3.0, h[2] - r, h[0] + r, h[1] - j * 3.0, h[2] + r, STONE,
              rotation=(0, 45 * (j % 2), 0), pivot=(h[0], h[1] - j * 3.0, h[2]))
    cb = m.bone("cap", bd, (0, 52, 5))                           # the tattered violet long coat
    cape(m, cb, 53.0, 24.0, 46.0, cutout(torn, COAT), z=6.0, flare=1.0, panels=10, sweep=(0, 8))
    return m
