"""Chaperomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the hooded wanderer of a dark fairy tale. A small figure in a red riding hood with a stitched
seam, blonde hair, a black dress with a white apron and coloured bows, white stockings and big furry wolf-head
slippers with lolling tongues, carrying a basket with a toothy grin in one hand and a bottle in the other.
25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, local, skin, solid, strands
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a small figure in a red riding hood, a black dress with a white apron, furry wolf-head slippers, a toothy "
        "basket and a bottle")
BASE = {"red": (200, 30, 40), "red_dark": (120, 10, 20), "black": (34, 32, 40), "black_light": (90, 88, 100),
        "white": (246, 246, 250), "white_dark": (190, 194, 206), "hair": (246, 220, 120), "hair_dark": (200, 160, 60),
        "skin": (250, 226, 210), "wolf": (110, 80, 70), "wolf_dark": (60, 40, 34), "tongue": (240, 110, 130),
        "basket": (200, 160, 80), "basket_dark": (130, 96, 40), "bottle": (90, 50, 30), "eye": (220, 30, 40),
        "bow1": (90, 160, 230), "bow2": (100, 200, 120), "tooth": (250, 250, 246)}
SHINY = {"red": (50, 70, 180), "red_dark": (20, 30, 110), "hair": (230, 230, 240), "hair_dark": (170, 170, 190)}


def P(v):
    return pal(BASE, SHINY, v)


HOOD = fabric(P, "red", "red_dark", axis="y", period=2.6)
DRESS = fabric(P, "black", "black_light", axis="y", period=1.8)
WOLF = fur(P, "wolf", "wolf_dark", length=1.0)


def apronf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 4.0 and 26.0 < y < 40.0:
        for bx, by, key in ((-1.6, 37.0, "bow1"), (1.8, 32.0, "bow2")):
            if abs(x - bx) < 0.9 and abs(y - by) < 0.5:
                return tone(p[key], face), None
        return tone(p["white"], face), None
    return DRESS(x, y, z, face, variant, box=box, **k)


def basketf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and box is not None:
        u, v, W, H = local(x, y, z, face, box)
        if abs(v - H * 0.5 - 0.6 * abs(math.sin(u * 1.6))) < 0.5:
            return tone(p["tooth"], face), None
    return tone(p["basket_dark"] if (x + y) % 1.2 < 0.4 else p["basket"], face), None


def build():
    m = Model("chaperomon")
    mats = {"skin": skin(P, "skin"), "chest": DRESS, "abs": apronf, "pelvis": apronf, "deltoid": HOOD,
            "upper_arm": DRESS, "forearm": DRESS, "hand": skin(P, "skin"), "finger": skin(P, "skin"),
            "thigh": solid(P, "white"), "knee": solid(P, "white"), "shin": solid(P, "white"), "calf": solid(P, "white"),
            "foot": WOLF, "toe": WOLF}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.85, name="chaperomon")
    bd = a["body"]
    for i, (r, y0, y1) in enumerate(((5.0, 24.0, 28.0), (6.0, 20.0, 24.0))):       # the skirt
        m.round_box(bd, 0, 0.2, r, r * 0.8, y0, y1, apronf, cut=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.6, 2.8, 54.4, 60.4, skin(P, "skin"), cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.0 - 0.4, 57.0, -3.0, sx * 1.0 + 0.4, 57.6, -2.8, solid(P, "eye"))
        rod(m, hd, (sx * 2.4, 58.0, -1.0), (sx * 3.4, 49.0, 0.0), 2, strands(P, "hair", "hair_dark"), extend=0.3)
    m.box(hd, -2.7, 58.4, -3.0, 2.7, 60.0, -2.6, strands(P, "hair", "hair_dark"))    # fringe
    m.round_box(hd, 0, 0.6, 3.6, 3.6, 56.0, 62.4, HOOD, cut=1)                        # the hood
    spike(m, hd, (0, 62.0, 2.6), (0, 0.6, 1), 2.4, 4.0, HOOD)
    m.box(bd, -3.0, 44.0, 2.6, 3.0, 52.0, 3.4, HOOD)                                 # hood cape on the back
    for nm in ("leg_left", "leg_right"):                                             # wolf-head slippers
        lg = a[nm]
        an = lg["ankle"]
        m.round_box(lg["bone"], an[0], an[2] - 2.6, 2.6, 4.0, 0.0, 4.0, WOLF, cut=1)
        for sx in (-1, 1):
            spike(m, lg["bone"], (an[0] + sx * 1.6, 3.6, an[2] - 1.0), (sx * 0.3, 1, 0.2), 1.0, 2.0, WOLF)
        m.box(lg["bone"], an[0] - 0.8, 0.0, an[2] - 8.0, an[0] + 0.8, 0.6, an[2] - 6.0, solid(P, "tongue"))
    al = a["arm_left"]                                                               # the toothy basket
    h = al["hand"]
    m.box(al["bone"], h[0] - 3.0, h[1] - 7.0, h[2] - 3.0, h[0] + 3.0, h[1] - 2.0, h[2] + 3.0, basketf)
    rod(m, al["bone"], (h[0] - 2.6, h[1] - 2.0, h[2]), (h[0] + 2.6, h[1] - 2.0, h[2]), 1, solid(P, "basket_dark"),
        extend=0)
    ar = a["arm_right"]                                                              # the bottle
    h = ar["hand"]
    m.round_box(ar["bone"], h[0], h[2], 1.2, 1.2, h[1] - 1.0, h[1] + 4.0, solid(P, "bottle"), cut=1)
    return m
