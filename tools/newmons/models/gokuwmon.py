"""Gokuwmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the rebel monkey king of the Saiyu Warriors: a wiry monkey-man with a shock of white hair and beard
under a golden circlet, a dark face, a black leather jacket and trousers hung with chains and red ribbons, big black
gloves, heavy boots, a long monkey tail and a long iron staff with golden ends. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a wiry monkey-man with white hair and beard under a golden circlet, a black leather outfit hung with chains "
        "and red ribbons, a monkey tail and a long iron staff")
BASE = {"leather": (40, 38, 44), "leather_dark": (14, 14, 18), "hair": (240, 240, 244), "hair_dark": (180, 180, 190),
        "face": (110, 80, 60), "face_dark": (70, 50, 36), "gold": (240, 200, 70), "gold_dark": (160, 120, 20),
        "red": (210, 30, 40), "red_dark": (130, 10, 16), "steel": (170, 174, 186), "steel_dark": (80, 84, 96),
        "eye": (250, 220, 60), "fur": (230, 228, 222), "fur_dark": (170, 166, 156)}
SHINY = {"leather": (150, 40, 40), "leather_dark": (80, 14, 14), "hair": (250, 200, 80), "hair_dark": (190, 140, 30)}


def P(v):
    return pal(BASE, SHINY, v)


LEATHER = leather(P, "leather", "leather_dark", stitch="steel")
HAIR = strands(P, "hair", "hair_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("gokuwmon")
    mats = {"skin": LEATHER, "neck": fur(P, "fur", "fur_dark"), "hand": LEATHER, "finger": LEATHER}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.95, name="gokuwmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 53.6, 59.6, skin(P, "face", dark="face_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.4, -3.3, max(sx * 0.6, sx * 1.6), 58.0, -3.1, solid(P, "eye"))
    m.round_box(hd, 0, -0.2, 2.6, 3.0, 58.4, 59.4, metal(P, "gold", dark="gold_dark"), cut=1)      # golden circlet
    for i in range(14):                                                                        # white hair shock
        ang = math.radians(-120 + i * 18)
        spike(m, hd, (2.2 * math.sin(ang), 59.6, 0.4 + 2.0 * math.cos(ang) + 0.8), (math.sin(ang) * 0.8, 0.8, 0.7),
              1.6, 7.0 + (i % 3) * 1.6, HAIR, tip=0.8)
    for j in range(5):                                                                         # white beard
        spike(m, hd, ((j - 2) * 0.8, 54.6, -2.6), (0, -1, -0.2), 1.0, 4.0, HAIR, tip=0.8)
    for j in range(6):                                                                          # chains
        m.round_box(bd, -4.0 + j * 1.6, -3.8, 0.6, 0.4, 32.0 - abs(j - 2.5) * 0.6, 33.0 - abs(j - 2.5) * 0.6, STEEL, cut=0)
    for sx in (-1, 1):                                                                          # red ribbons
        rod(m, bd, (sx * 4.0, 50.0, 2.0), (sx * 10.0, 46.0, 10.0), 1, fabric(P, "red", "red_dark"), extend=0.3, t2=2)
    tb = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (3.0, 24.0, 8.0), (8.0, 20.0, 12.0), (11.0, 24.0, 15.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, fur(P, "fur", "fur_dark"), extend=0.4, t2=2)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                        # iron staff
    rod(m, ar, (h[0] + 10.0, h[1] - 18.0, h[2] + 4.0), (h[0] - 10.0, h[1] + 18.0, h[2] - 4.0), 2, STEEL, extend=0)
    for e in ((h[0] + 10.0, h[1] - 18.0, h[2] + 4.0), (h[0] - 10.0, h[1] + 18.0, h[2] - 4.0)):
        m.round_box(ar, e[0], e[2], 1.4, 1.4, e[1] - 1.4, e[1] + 1.4, metal(P, "gold", dark="gold_dark"), cut=0)
    return m
