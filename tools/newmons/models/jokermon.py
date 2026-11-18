"""Jokermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the trickster jester: a tall lanky demon-man with a pale grinning face, a red-and-black two-pointed
jester cap with gold bells and a little crown, a purple tailcoat with long tails over a white shirt and green bow,
skin-tight green trousers, pointed purple shoes, white gloves and a long purple cane with a black tip. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a tall lanky jester with a pale grin, a red-and-black jester cap with gold bells, a purple tailcoat, green "
        "trousers, pointed shoes and a long purple cane")
BASE = {"pale": (236, 236, 246), "pale_dark": (170, 170, 190), "purple": (110, 50, 150), "purple_dark": (50, 16, 80),
        "green": (40, 140, 90), "green_dark": (14, 70, 40), "red": (200, 30, 50), "black": (30, 28, 34),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "white": (250, 250, 250), "white_dark": (190, 190, 200),
        "eye": (240, 40, 40), "mouth": (40, 20, 30), "blue": (60, 120, 230)}
SHINY = {"purple": (200, 120, 30), "purple_dark": (120, 60, 10), "green": (60, 80, 180), "green_dark": (20, 30, 110)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "purple", "purple_dark")
PANTS = fabric(P, "green", "green_dark")
SHIRT = fabric(P, "white", "white_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.1) < 0.5 and abs(y - 58.0) < 0.35:
                return tone(p["eye"], face), p["eye"]
        if abs(y - 55.4 - 0.25 * x * x) < 0.25 and abs(x) < 1.8:
            return tone(p["mouth"], face), None
    return skin(P, "pale", dark="pale_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jokermon")
    mats = {"skin": COAT, "chest": SHIRT, "abs": SHIRT, "pelvis": PANTS, "neck": skin(P, "pale", dark="pale_dark"),
            "deltoid": COAT, "upper_arm": COAT, "forearm": COAT, "hand": SHIRT, "finger": SHIRT, "thigh": PANTS,
            "knee": PANTS, "shin": PANTS, "calf": PANTS, "foot": leather(P, "purple", "purple_dark"),
            "toe": solid(P, "purple")}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.8, leg_bulk=0.78, name="jokermon")
    bd = a["body"]
    for sx in (-1, 1):                                                               # tailcoat fronts + tails
        m.round_box(bd, sx * 3.4, -0.2, 1.6, 3.4, 36.0, 51.0, COAT, cut=1)
        rod(m, bd, (sx * 2.0, 36.0, 3.0), (sx * 4.0, 20.0, 8.0), 2, COAT, extend=0.4, t2=1)
    m.round_box(bd, 0, -3.6, 1.6, 0.5, 49.4, 51.0, solid(P, "green"), cut=0)                  # bow
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, facef, cut=1)
    m.round_box(hd, 0, 0, 2.8, 2.8, 59.0, 61.0, solid(P, "red"), cut=1)
    for sx, key in ((1, "red"), (-1, "black")):                                       # two-pointed cap
        pts = [(sx * 1.4, 60.6, 0), (sx * 5.0, 64.0, 1.0), (sx * 8.0, 62.0, 2.0), (sx * 9.0, 58.0, 2.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 - min(j, 1), solid(P, key), extend=0.4)
        m.round_box(hd, sx * 9.0, 2.0, 0.8, 0.8, 56.6, 58.0, metal(P, "gold", dark="gold_dark"), cut=0)
    for j in range(5):                                                               # little crown
        spike(m, hd, ((j - 2) * 0.8, 61.0, -1.6), (0, 1, 0), 0.9, 1.6, metal(P, "gold", dark="gold_dark"), tip=0.8)
    hr = a["arm_right"]                                                              # long cane
    hx, hy, hz = hr["hand"]
    rod(m, hr["bone"], (hx + 8.0, hy + 4.0, hz), (hx - 18.0, hy - 8.0, hz - 4.0), 1, solid(P, "purple"), extend=0, t2=1)
    m.round_box(hr["bone"], hx - 18.4, hz - 4.2, 0.8, 0.8, hy - 9.0, hy - 7.6, solid(P, "black"), cut=0)
    m.round_box(hr["bone"], hx + 8.4, hz, 0.8, 0.8, hy + 3.4, hy + 5.0, solid(P, "blue"), cut=0)
    return m
