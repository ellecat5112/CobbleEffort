"""Lucemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Lucemon awakened by the X-Antibody: a tall angel in silver-and-gold armour with long
golden hair and a red halo, and a vast burst of ten tattered golden feathered wings fanning all round him. 35 blocks.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a tall angel in silver-and-gold armour with long golden hair, a red halo and a vast burst of tattered golden wings"
BASE = {"silver": (220, 224, 236), "silver_dark": (120, 126, 146), "gold": (240, 200, 80), "gold_dark": (160, 110, 20),
        "gold_light": (255, 240, 170), "skin": (250, 226, 210), "skin_dark": (210, 170, 150), "red": (230, 50, 50),
        "eye": (60, 130, 230)}
SHINY = {"gold": (220, 220, 240), "gold_dark": (130, 130, 160), "gold_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", trim="gold", trim_w=0.3)
FEATH = feathers(P, "gold", "gold_dark", tip="gold_light", size=(1.6, 3.0))


def build():
    m = Model("lucemonxantibody")
    mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": ARM, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": ARM, "knee": metal(P, "gold", dark="gold_dark"), "shin": ARM,
            "calf": ARM, "foot": ARM, "toe": ARM}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, name="lucemonxantibody")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.box(hd, -1.4, 57.4, -2.9, -0.4, 58.0, -2.8, solid(P, "eye"))
    m.box(hd, 0.4, 57.4, -2.9, 1.4, 58.0, -2.8, solid(P, "eye"))
    for i in range(11):                                                              # long golden hair
        ang = math.radians(-110 + i * 22)
        rod(m, hd, (2.2 * math.sin(ang), 59.6, 0.8 + 1.2 * math.cos(ang)), (3.4 * math.sin(ang), 44.0, 3.6), 1,
            strands(P, "gold", "gold_dark"), extend=0.3, t2=2)
    hb = m.bone("ring_halo", hd, (0, 64, 0))                                         # red halo
    for i in range(12):
        a0, a1 = 2 * math.pi * i / 12, 2 * math.pi * (i + 1) / 12
        rod(m, hb, (3.4 * math.cos(a0), 64.0, 3.4 * math.sin(a0)), (3.4 * math.cos(a1), 64.0, 3.4 * math.sin(a1)), 1,
            solid(P, "red", glow=True), extend=0.2, t2=1)
    for side in (1, -1):                                                             # vast burst of golden wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.6, 48.0, 3.4))
        for j, (dr, sw, sp) in enumerate(((24, 50, 22.0), (8, 25, 28.0), (-8, 10, 30.0), (-24, -5, 26.0), (-40, -20, 20.0))):
            feather_wing(m, wb, (side * 2.6, 48.0, 3.4 + j * 0.4), sp, 6.0, 1, FEATH, side=side, sweep=sw, droop=dr)
    return m
