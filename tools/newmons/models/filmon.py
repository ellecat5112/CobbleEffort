"""Filmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the porcupine fighter. A lean white beast-man with a long pointed snout and blue eyes, a great crest
of golden quills sweeping back from his head and shoulders, bandaged forearms and shins, red claws on his hands and
feet, gold spikes at his joints and dark wing-like quill fans at his back. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean white beast-man with a long pointed snout, a great crest of golden quills, bandaged forearms and shins, "
        "red claws, gold joint spikes and dark quill fans")
BASE = {"white": (240, 240, 246), "white_dark": (170, 172, 190), "gold": (250, 210, 60), "gold_dark": (190, 140, 20),
        "bandage": (236, 230, 216), "bandage_dark": (180, 170, 150), "red": (210, 40, 40), "dark": (40, 40, 50),
        "eye": (60, 120, 220)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "gold": (120, 220, 250), "gold_dark": (40, 140, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "white", dark="white_dark")
BAND = fabric(P, "bandage", "bandage_dark", axis="y", period=1.2)
QUILL = strands(P, "gold", "gold_dark")


def build():
    m = Model("filmon")
    mats = {"skin": SKIN, "chest": SKIN, "abs": SKIN, "pelvis": SKIN, "neck": SKIN, "deltoid": SKIN,
            "upper_arm": SKIN, "forearm": BAND, "hand": SKIN, "finger": SKIN, "claw": solid(P, "red"), "thigh": SKIN,
            "knee": SKIN, "shin": BAND, "calf": BAND, "foot": SKIN, "talon": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.95, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                 name="filmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 3.0, 54.0, 60.0, SKIN, cut=1)
    spike(m, hd, (0, 56.0, -3.0), (0, -0.2, -1), 2.6, 6.0, SKIN, tip=0.6)              # long pointed snout
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.0), 57.6, -3.3, max(sx * 1.0, sx * 2.0), 58.4, -3.0, solid(P, "eye"))
    for row in range(2):                                                              # great crest of golden quills
        for i in range(11):
            ang = math.radians(-75 + i * 15)
            spike(m, hd, (2.2 * math.sin(ang), 58.0 + row * 1.6, 0.6 + row * 1.2),
                  (math.sin(ang) * 0.9, 0.9 - row * 0.3, 0.5 + row * 0.5), 1.6, 13.0 - abs(i - 5) * 0.9 - row * 2.0,
                  QUILL, tip=0.9)
    for sx in (-1, 1):
        for j in range(4):                                                            # shoulder quills
            spike(m, bd, (sx * 5.6, 50.0, j * 1.0), (sx * 0.9, 0.8, 0.4), 1.4, 10.0 - j * 1.5, QUILL, tip=0.8)
        for j in range(3):                                                            # dark quill fans
            spike(m, bd, (sx * 2.0, 44.0 + j * 2.4, 3.6), (sx * 1.0, 0.5 - j * 0.3, 0.4), 1.6, 16.0 - j * 3.0,
                  solid(P, "dark"), tip=0.3)
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                     # gold joint spikes
        anc = a[nm]
        j = anc.get("elbow") or anc.get("knee")
        sx = 1 if j[0] > 0 else -1
        spike(m, anc["bone"], j, (sx, 0.2, 0.6), 1.0, 3.6, solid(P, "gold"), tip=0.25)
    return m
