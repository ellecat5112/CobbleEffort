"""Footmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the striker. A lithe android footballer in a navy-blue bodysuit with red-and-black armour plates, a
red helmet with a green visor-crest and dark dreadlocks spilling from the back, big white gloves, red-and-black
boots with glowing studs, and a black-and-white football at his feet. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a lithe android footballer in a navy bodysuit with red-and-black armour, a red helmet with a green visor-crest "
        "and dreadlocks, big white gloves, studded boots and a football")
BASE = {"navy": (40, 50, 140), "navy_dark": (14, 20, 70), "red": (210, 30, 40), "red_dark": (120, 10, 16),
        "black": (34, 32, 38), "black_dark": (14, 14, 18), "white": (246, 246, 250), "white_dark": (190, 190, 206),
        "green": (60, 210, 110), "dread": (70, 50, 36), "dread_dark": (36, 24, 16), "stud": (255, 230, 90),
        "visor": (40, 220, 140)}
SHINY = {"navy": (240, 240, 246), "navy_dark": (170, 172, 190), "red": (250, 200, 40), "red_dark": (170, 120, 10)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "navy", "navy_dark", axis="y", period=1.6)
RED = armour(P, "red", "red_dark", trim="black", trim_w=0.3)
GLOVE = skin(P, "white", dark="white_dark")


def ballf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a = math.atan2(z + 9.0, x + 2.0)
    on = (int((a + math.pi) * 2.0) + int(y * 0.5)) % 2
    return tone(p["black"] if on else p["white"], face), None


def build():
    m = Model("footmon")
    mats = {"skin": SUIT, "chest": RED, "abs": SUIT, "pelvis": metal(P, "black", dark="black_dark"), "neck": SUIT,
            "deltoid": RED, "upper_arm": SUIT, "forearm": RED, "hand": GLOVE, "finger": GLOVE, "thigh": SUIT,
            "knee": RED, "shin": RED, "calf": RED, "foot": leather(P, "black", "black_dark"), "toe": RED}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.95, name="footmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.6, 3.0, 53.6, 60.4, RED, cut=1)                              # helmet
    m.box(hd, -2.2, 56.4, -3.2, 2.2, 57.8, -2.9, solid(P, "visor", glow=True))
    spike(m, hd, (0, 58.0, -3.0), (0, 1, -0.2), 1.6, 6.0, solid(P, "green"), tip=0.3)    # green crest
    for i in range(9):                                                                   # dreadlocks
        ang = math.radians(-80 + i * 20)
        rod(m, hd, (2.6 * math.sin(ang), 59.0, 1.0 + 1.6 * math.cos(ang) * 0.4 + 1.0),
            (4.4 * math.sin(ang), 48.0, 6.0), 1, strands(P, "dread", "dread_dark"), extend=0.2, t2=1)
    for nm in ("arm_left", "arm_right"):                                                 # big white gloves
        h = a[nm]["hand"]
        m.round_box(a[nm]["bone"], h[0], h[2], 2.0, 2.0, h[1] - 2.0, h[1] + 1.6, GLOVE, cut=1)
    for nm in ("leg_left", "leg_right"):                                                 # glowing studs
        an = a[nm]["ankle"]
        for j in range(3):
            m.box(a[nm]["bone"], an[0] - 0.4 + (j - 1) * 1.0, 0.0, an[2] - 2.0, an[0] + 0.4 + (j - 1) * 1.0, 0.5,
                  an[2] - 1.2, solid(P, "stud", glow=True))
    ball(m, a["leg_right"]["bone"], (-2.0, 4.0, -9.0), 4.0, ballf, layers=4)             # football
    return m
