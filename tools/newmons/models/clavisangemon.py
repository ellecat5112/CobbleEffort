"""Clavis Angemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the angel of the key. A white-and-gold armoured angel with a red-crested helm and visor, a long
red scarf streaming behind, round white pauldrons with gold rings, six great white wings, and a huge golden key held
like a lance. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid
from _digidetail import armour, fabric, feathers, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a white-and-gold armoured angel with a red-crested helm, a long red scarf, round pauldrons, six great white "
        "wings and a huge golden key held like a lance")
BASE = {"white": (240, 242, 250), "white_dark": (170, 176, 200), "gold": (240, 196, 60), "gold_dark": (170, 120, 20),
        "gold_light": (255, 240, 160), "red": (200, 30, 40), "red_dark": (120, 10, 20), "visor": (60, 150, 240),
        "under": (60, 60, 80), "wing": (246, 248, 255), "wing_dark": (200, 206, 224)}
SHINY = {"white": (40, 44, 60), "white_dark": (16, 18, 26), "red": (40, 140, 220), "red_dark": (14, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="gold", trim_w=0.35)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
SCARF = fabric(P, "red", "red_dark", axis="x", period=2.0)


def build():
    m = Model("clavisangemon")
    mats = {"skin": solid(P, "under"), "chest": WHITE, "abs": WHITE, "pelvis": WHITE, "deltoid": WHITE,
            "upper_arm": solid(P, "under"), "forearm": WHITE, "hand": GOLD, "finger": GOLD, "thigh": WHITE,
            "knee": GOLD, "shin": WHITE, "calf": WHITE, "foot": WHITE, "toe": GOLD}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.05, name="clavisangemon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.8, 3.0, 54.0, 61.0, WHITE, cut=1)
    m.box(hd, -2.2, 56.8, -3.4, 2.2, 58.2, -3.0, solid(P, "visor", glow=True))
    for i in range(5):
        spike(m, hd, (0, 60.6, -2.0 + i * 1.2), (0, 1, 0.4 + 0.1 * i), 1.4, 3.6 - 0.3 * abs(i - 2), solid(P, "red"))
    m.round_box(bd, 0, -0.2, 3.2, 3.2, 50.4, 53.6, SCARF, cut=1)                     # the red scarf
    for sx in (-1, 1):
        pts = [(sx * 2.0, 52.0, 3.0), (sx * 5.0, 46.0, 10.0), (sx * 8.0, 40.0, 16.0), (sx * 12.0, 38.0, 22.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, SCARF, extend=0.3, t2=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # round pauldrons, gold rings
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 1.8, 49.0, 0.3), 4.6, 4.2, WHITE, layers=4)
        m.round_box(a[nm]["bone"], sh[0] + sx * 1.8, 0.3, 4.8, 4.8, 48.4, 49.2, GOLD, cut=2)
    wb = m.bone("wings", bd, (0, 50, 4))                                              # six great white wings
    WING = feathers(P, "wing", "wing_dark", size=(1.6, 3.2), flow=(0, 1))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.0, sx * 28.0))
        for j, ang in enumerate((40, 15, -15)):
            m.box(wb, x0, 47.0, 4.0 + j * 0.6, x1, 53.0, 4.0 + j * 0.6, WING, rotation=(0, sx * 15, sx * ang),
                  pivot=(sx * 3.0, 50.0, 4.0 + j * 0.6))
    ar = a["arm_right"]                                                               # the golden key-lance
    h = ar["hand"]
    kb = m.bone("key", ar["bone"], h)
    rod(m, kb, (h[0], h[1] + 4.0, h[2] + 8.0), (h[0], h[1] - 2.0, h[2] - 26.0), 2, GOLD, extend=0)
    for i in range(6):                                                                # bow ring
        ang = i * math.pi / 3
        p0 = (h[0], h[1] + 4.0 + 3.0 * math.sin(ang), h[2] + 10.0 + 3.0 * math.cos(ang))
        p1 = (h[0], h[1] + 4.0 + 3.0 * math.sin(ang + math.pi / 3), h[2] + 10.0 + 3.0 * math.cos(ang + math.pi / 3))
        rod(m, kb, p0, p1, 1, GOLD, extend=0.3)
    for j in range(3):                                                                # key bit
        m.box(kb, h[0] - 0.6, h[1] - 6.0 + (j % 2) * 1.6, h[2] - 24.0 + j * 2.4, h[0] + 0.6, h[1] - 2.0,
              h[2] - 22.6 + j * 2.4, GOLD)
    return m
