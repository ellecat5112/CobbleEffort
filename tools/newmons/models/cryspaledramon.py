"""Crys Paledramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the crystal ice dragon-man. A crouching dragon-man encased in faceted pale-blue ice
crystal armour over dark blue joints, a white-maned helm, great crystal shards rising from its shoulders like wings,
clawed crystal hands and feet, and a trail of frost. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, gem, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crouching dragon-man encased in faceted pale-blue ice crystal armour, a white-maned helm, great crystal "
        "shards rising from its shoulders and clawed crystal hands")
BASE = {"ice": (170, 210, 250), "ice_light": (240, 250, 255), "ice_dark": (90, 140, 210), "navy": (40, 60, 140),
        "navy_dark": (16, 24, 70), "white": (240, 244, 250), "white_dark": (170, 180, 200), "eye": (250, 230, 90)}
SHINY = {"ice": (250, 190, 220), "ice_light": (255, 240, 250), "ice_dark": (210, 120, 170), "navy": (110, 40, 90)}


def P(v):
    return pal(BASE, SHINY, v)


ICE = gem(P, "ice", "ice_light", glow=False)
ICE_D = gem(P, "ice_dark", "ice", glow=False)
NAVY = armour(P, "navy", "navy_dark")


def build():
    m = Model("cryspaledramon")
    mats = {"skin": NAVY, "chest": ICE, "abs": NAVY, "pelvis": ICE, "deltoid": ICE, "upper_arm": NAVY, "forearm": ICE,
            "hand": ICE, "finger": ICE, "claw": ICE, "thigh": ICE, "knee": ICE_D, "shin": ICE, "calf": NAVY,
            "foot": ICE, "talon": ICE}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.2, digitigrade=True, claws=True, talons=True,
                 name="cryspaledramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.8, 3.0, 54.4, 61.0, ICE, cut=1)
    m.box(hd, -1.8, 54.6, -6.6, 1.8, 57.4, -3.0, ICE)
    m.box(hd, -2.0, 58.0, -3.9, 2.0, 58.6, -3.5, solid(P, "eye", glow=True))
    for i in range(12):                                                          # white mane
        ang = math.radians(-100 + i * 18)
        rod(m, hd, (2.6 * math.sin(ang), 60.0, 0.6), (5.6 * math.sin(ang), 54.0, 8.0), 2,
            strands(P, "white", "white_dark"), extend=0.3, t2=2)
    for sx in (-1, 1):                                                           # crystal shard wings
        for j, (d, ln) in enumerate((((0.4, 1, 0.5), 22.0), ((0.7, 0.9, 0.4), 18.0), ((0.9, 0.6, 0.3), 14.0))):
            spike(m, bd, (sx * 4.0, 50.0 - j * 2.0, 3.6), (sx * d[0], d[1], d[2]), 3.0 - j * 0.4, ln,
                  ICE if j % 2 == 0 else ICE_D, tip=0.6)
        spike(m, bd, (sx * 7.6, 50.0, 0.4), (sx, 0.6, 0), 2.0, 4.0, ICE, tip=0.4)
    for nm in ("leg_left", "leg_right"):                                         # frost spikes on the shins
        lg = a[nm]
        k = lg["knee"]
        spike(m, lg["bone"], (k[0], k[1], k[2] - 1.6), (0, 0.4, -1), 1.6, 3.0, ICE, tip=0.4)
    return m
