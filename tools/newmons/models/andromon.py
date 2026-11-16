"""Andromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): an android built to be the perfect machine. A chrome skeleton-armour body with ribbed abdomen
plates, red gem-lights in its chest, bundles of red artificial muscle and cable showing at every joint, a skull-like
chrome head with red eyes and a pale face, a huge cylinder on its right forearm (the Gatling Attack drum) and long
steel claw-fingers. 25 blocks tall.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, gem, local, metal, skin, solid, twisted
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a chrome android: ribbed skeleton-armour, red gem-lights in its chest, red artificial muscle at the joints, a "
        "skull-like chrome head with red eyes, a huge drum on its right forearm and long steel claw-fingers")
BASE = {"chrome": (190, 194, 206), "chrome_dark": (70, 74, 86), "chrome_light": (246, 248, 255), "muscle": (200, 80, 90),
        "muscle_dark": (120, 30, 40), "red": (230, 30, 40), "red_light": (255, 150, 150), "face": (230, 210, 200),
        "eye": (255, 40, 40), "black": (30, 30, 36)}
SHINY = {"chrome": (220, 190, 110), "chrome_dark": (130, 100, 40), "chrome_light": (255, 240, 190),
         "muscle": (80, 140, 220), "muscle_dark": (30, 70, 140), "red": (40, 200, 120), "red_light": (170, 255, 210),
         "eye": (40, 230, 120)}


def P(v):
    return pal(BASE, SHINY, v)


CHROME = metal(P, "chrome", dark="chrome_dark", light="chrome_light")
PLATE = armour(P, "chrome", "chrome_dark", light="chrome_light", seams=(1.6,))
MUSCLE = twisted(P, "muscle", "muscle_dark", period=1.6)
GEM = gem(P, "red", "red_light")


def build():
    m = Model("andromon")
    mats = {"skin": MUSCLE, "chest": PLATE, "abs": PLATE, "pelvis": CHROME, "neck": MUSCLE, "deltoid": CHROME,
            "upper_arm": MUSCLE, "forearm": CHROME, "hand": CHROME, "finger": CHROME, "claw": CHROME,
            "thigh": CHROME, "knee": CHROME, "shin": CHROME, "calf": MUSCLE, "foot": CHROME, "toe": CHROME}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.0, leg_bulk=1.0, name="andromon", hand_pose="open", claws=True,
                 chest_depth=0.95)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.6, 2.8, 54.6, 61.0, CHROME, cut=1)
    m.box(hd, -1.6, 54.8, -3.0, 1.6, 58.6, -2.6, skin(P, "face"))                       # pale face
    for sx in (-1, 1):
        m.box(hd, sx * 1.0 - 0.5, 57.4, -3.2, sx * 1.0 + 0.5, 58.2, -2.9, solid(P, "eye", glow=True))
        rod(m, hd, (sx * 2.7, 58.0, 0), (sx * 4.0, 61.0, 0.6), 1, CHROME, extend=0.2)     # antenna bolts
    for j in range(4):                                           # ribbed skull dome
        m.box(hd, -2.7, 59.0 + j * 0.0, -2.4 + j * 1.4, 2.7, 61.6, -1.8 + j * 1.4, PLATE)
    for sx in (-1, 1):                                           # red gem-lights in the chest
        m.round_box(bd, sx * 2.4, -4.6, 0.8, 0.5, 46.0, 47.8, GEM, cut=1)
    m.round_box(bd, 0, -4.4, 0.6, 0.4, 41.0, 42.4, GEM, cut=1)
    for i in range(5):                                           # ribbed abdomen plates
        m.box(bd, -3.6, 35.0 + i * 1.5, -3.8, 3.6, 35.8 + i * 1.5, -2.8, PLATE)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.2, 50.0, 0.3), 3.6, 3.0, CHROME, layers=3)
        for j in range(3):                                       # cable bundles at the elbow
            el = a[nm]["elbow"]
            rod(m, ab, (el[0] + (j - 1) * 0.8, el[1] + 3.0, el[2] + 1.0), (el[0] + (j - 1) * 0.8, el[1] - 3.0,
                el[2] + 1.2), 1, solid(P, "black"), extend=0.2)
    ar = a["arm_right"]                                          # the great forearm drum
    el, wr = ar["elbow"], ar["wrist"]
    mid = tuple((e + w) / 2 for e, w in zip(el, wr))
    m.round_box(ar["bone"], mid[0] - 0.8, mid[2], 3.6, 3.6, mid[1] - 6.0, mid[1] + 5.0, CHROME, cut=1)
    for j in range(3):
        m.round_box(ar["bone"], mid[0] - 0.8, mid[2], 3.9, 3.9, mid[1] - 4.5 + j * 3.6, mid[1] - 3.6 + j * 3.6,
                    PLATE, cut=1)
    m.box(ar["bone"], mid[0] - 2.4, mid[1] - 2.0, mid[2] - 4.2, mid[0] + 0.8, mid[1] + 1.0, mid[2] - 3.6,
          solid(P, "red", glow=True))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg, kn = a[nm]["bone"], a[nm]["knee"]
        dome(m, lg, (kn[0], 17.5, kn[2] - 0.6), 2.4, 2.2, CHROME, layers=2)
        shell(m, lg, (kn[0], 0, 0.6), 2.6, 3.0, 13.0, -90, 90, 5, 1.0, PLATE)
        m.box(lg, kn[0] - 2.4, 0.0, -4.0, kn[0] + 2.4, 3.6, 3.0, CHROME)                 # heavy feet
    return m
