"""Commandramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the little commando dinosaur. A small upright blue dinosaur in a digital-camouflage combat suit
and helmet with a headset and goggles, grey body armour and knee pads, an assault rifle held across its chest, and
steel-clawed feet. Child stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, eye, fbm, metal, scales, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = ("a small upright blue dinosaur in a digital-camouflage combat suit and helmet with a headset, grey body armour "
        "and an assault rifle")
BASE = {"blue": (70, 110, 170), "blue_dark": (30, 54, 110), "blue_light": (140, 170, 220), "camo1": (60, 90, 130),
        "camo2": (40, 60, 90), "camo3": (100, 130, 170), "grey": (100, 104, 116), "grey_dark": (50, 52, 60),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "black": (24, 24, 30), "eye": (250, 170, 40),
        "pupil": (20, 10, 10), "white": (255, 255, 255), "mouth": (200, 50, 60)}
SHINY = {"camo1": (110, 130, 70), "camo2": (70, 90, 40), "camo3": (160, 170, 110), "blue": (200, 120, 60),
         "blue_dark": (130, 70, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def camof(x, y, z, face, variant, box=None, **k):
    """Digital camouflage: blocky pixels of three tones."""
    p = P(variant)
    n = fbm(math.floor(x / 1.2) * 0.6, math.floor(y / 1.2) * 0.6, math.floor(z / 1.2) * 0.6, 6)
    return tone(p["camo2"] if n < 0.4 else p["camo3"] if n > 0.62 else p["camo1"], face), None


SKIN = scales(P, "blue", "blue_dark", size=1.0, light="blue_light")
ARMOUR = armour(P, "grey", "grey_dark", rivets=True)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 2.6, y - 21.4, 1.0, "eye")
        if c is not None:
            return c, None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("commandramon")
    top = m.bone("commandramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 1))
    m.round_box(bd, 0, 1.0, 3.6, 3.2, 7.0, 16.6, camof, cut=1)                       # camo suit
    m.box(bd, -3.4, 10.0, -2.8, 3.4, 15.4, -1.8, ARMOUR)                             # body armour
    hd = m.bone("head", bd, (0, 16.5, -0.5))
    m.round_box(hd, 0, -1.6, 3.2, 3.4, 16.6, 22.6, headf, cut=1)
    m.box(hd, -2.4, 17.2, -8.6, 2.4, 20.0, -4.6, SKIN)                               # snout
    m.box(hd, -2.0, 16.4, -8.0, 2.0, 17.2, -4.6, solid(P, "mouth"))
    m.round_box(hd, 0, -1.0, 3.8, 3.8, 21.6, 25.0, camof, cut=1)                     # helmet
    m.box(hd, -2.8, 23.0, -4.8, 2.8, 24.0, -3.8, metal(P, "steel", dark="steel_dark"))   # goggles
    rod(m, hd, (3.4, 21.0, -1.0), (3.6, 18.0, -4.4), 1, solid(P, "black"), extend=0)     # headset mic
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 14.2, -0.6))
        rod(m, ab, (sx * 3.4, 14.2, -0.6), (sx * 3.0, 11.0, -4.0), 2, camof, extend=0.4)
        m.box(ab, sx * 3.0 - 1.0, 10.0, -5.0, sx * 3.0 + 1.0, 11.6, -3.4, ARMOUR)
    gb = m.bone("rifle", "arm_right", (0, 11, -5))                                   # the assault rifle
    m.box(gb, -5.0, 10.6, -5.6, 5.0, 12.0, -4.6, solid(P, "black"))
    rod(m, gb, (5.0, 11.4, -5.0), (10.0, 11.0, -5.0), 1, solid(P, "black"), extend=0)
    m.box(gb, -1.0, 8.4, -5.4, 0.4, 10.6, -4.8, solid(P, "black"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 8.0, 1.0))
        m.round_box(lg, sx * 2.6, 1.4, 2.1, 2.5, 2.4, 8.6, camof, cut=1)
        m.box(lg, sx * 2.6 - 2.2, 4.0, -1.4, sx * 2.6 + 2.2, 6.0, -0.8, ARMOUR)      # knee pads
        m.box(lg, sx * 2.6 - 2.0, 0, -2.6, sx * 2.6 + 2.0, 2.6, 3.0, solid(P, "grey_dark"))
        for j in range(3):
            spike(m, lg, (sx * 2.6 + (j - 1) * 1.2, 0.8, -2.6), (0, -0.1, -1), 0.9, 2.0, metal(P, "steel", dark="steel_dark"))
    tl = m.bone("tail", bd, (0, 9.5, 4))
    rod(m, tl, (0, 9.5, 3.6), (0, 6.5, 9.0), 3, SKIN, extend=0.6)
    return m
