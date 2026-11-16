"""Assaultmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a cyborg soldier in a heavy grey mech-suit. A gas-masked face under a pink helmet, riveted grey
armour with rounded shoulder pods, a six-barrel gatling cannon for a left arm, a heavy claw arm on the right, ammo
belts and hoses looped over its shoulders, a backpack generator, a shaggy grey tail and three-clawed steel feet.
25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import dome, humanoid, shell
from _digidetail import armour, fur, local, metal, riveted, solid, twisted
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a cyborg soldier in a heavy grey mech-suit: a gas-masked face under a pink helmet, riveted armour, a gatling "
        "cannon arm, a claw arm, ammo belts, a backpack and three-clawed steel feet")
BASE = {"grey": (130, 134, 146), "grey_dark": (60, 62, 72), "grey_light": (200, 204, 216), "pink": (210, 100, 130),
        "pink_dark": (140, 50, 80), "olive": (170, 170, 90), "olive_dark": (110, 110, 50), "brass": (220, 170, 80),
        "brass_dark": (150, 100, 40), "lens": (40, 40, 48), "fur": (200, 200, 206), "fur_dark": (130, 130, 140),
        "black": (30, 30, 36)}
SHINY = {"grey": (110, 120, 80), "grey_dark": (50, 56, 30), "grey_light": (180, 190, 140), "pink": (60, 130, 200),
         "pink_dark": (24, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


ARMOUR = riveted(P, "grey", "grey_dark", light="grey_light")
PLATE = armour(P, "grey", "grey_dark", light="grey_light", seams=(3.0,))
STEEL = metal(P, "grey", dark="grey_dark", light="grey_light")
BELT = twisted(P, "brass", "brass_dark", period=1.2)


def build():
    m = Model("assaultmon")
    mats = {"skin": PLATE, "chest": ARMOUR, "abs": PLATE, "pelvis": ARMOUR, "neck": solid(P, "olive"),
            "deltoid": ARMOUR, "upper_arm": PLATE, "forearm": ARMOUR, "hand": STEEL, "finger": STEEL, "claw": STEEL,
            "thigh": ARMOUR, "knee": STEEL, "shin": ARMOUR, "calf": PLATE, "foot": STEEL, "talon": STEEL}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.3, leg_bulk=1.4, digitigrade=True, talons=True, toes=3,
                 name="assaultmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.6, 59.8, solid(P, "olive"), cut=1)
    dome(m, hd, (0, 59.0, 0), 3.2, 3.0, armour(P, "pink", "pink_dark"), layers=3)       # pink helmet
    m.box(hd, -2.0, 54.4, -3.6, 2.0, 57.6, -2.4, STEEL)                                  # gas mask
    for sx in (-1, 1):
        ball(m, hd, (sx * 1.1, 58.0, -2.9), 0.8, solid(P, "lens"), layers=2)
        m.box(hd, sx * 1.8 - 0.9, 53.6, -3.9, sx * 1.8 + 0.9, 55.6, -2.1, STEEL)                     # filter canisters
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        ball(m, ab, (sh[0] + sx * 2.0, 49.0, 0.3), 4.6, ARMOUR, layers=4)
    al = a["arm_left"]                                           # the gatling cannon
    el, wr = al["elbow"], al["wrist"]
    gb = m.bone("spin_gun", al["bone"], wr)
    m.round_box(gb, wr[0], wr[2], 3.2, 3.2, wr[1] - 4.0, wr[1] + 2.0, PLATE, cut=1)
    for i in range(6):
        ang = math.radians(i * 60)
        x, z = wr[0] + 1.8 * math.cos(ang), wr[2] + 1.8 * math.sin(ang)
        rod(m, gb, (x, wr[1] - 3.0, z), (x, wr[1] - 16.0, z - 3.0), 1, STEEL, extend=0)
    ar = a["arm_right"]                                          # the claw arm
    h = ar["hand"]
    for j in range(3):
        ang = math.radians(-40 + j * 40)
        spike(m, ar["bone"], (h[0], h[1] - 1.0, h[2]), (math.sin(ang) * 0.6, -1, -0.6), 1.4, 4.4, STEEL, tip=0.6)
    for sx in (-1, 1):                                           # ammo belts crossing the chest
        rod(m, bd, (sx * 5.0, 51.0, -3.6), (-sx * 4.0, 36.0, -4.4), 2, BELT, extend=0.3, t2=1)
    m.box(bd, -4.6, 38.0, 4.0, 4.6, 50.0, 8.0, ARMOUR)                                   # backpack
    for sx in (-1, 1):
        rod(m, bd, (sx * 3.0, 50.0, 6.0), (sx * 6.0, 47.0, -2.0), 1, solid(P, "black"), extend=0.3)   # hoses
    tl = m.bone("tail", bd, (0, 31, 4))
    pts = [(0, 31, 4), (2, 26, 11), (5, 22, 17)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 3, fur(P, "fur", "fur_dark"), extend=0.4)
    return m
