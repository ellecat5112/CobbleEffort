"""Invisimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the stealth warrior: a heavy blue-and-silver armoured robot under a hooded violet cloak that
streams behind it in tatters, a dark visor with yellow eyes under the hood, round blue shoulder pods with glowing
lenses, a red-and-white striped waist, a huge blue fist on one arm and on the other a long folding silver blade-shield
with a dark grip, and red-and-yellow boots. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a heavy blue-and-silver armoured robot under a tattered hooded violet cloak, a dark visor with yellow eyes, "
        "round shoulder pods, a huge blue fist and a long silver blade-shield")
BASE = {"blue": (40, 80, 200), "blue_dark": (14, 30, 110), "blue_light": (120, 170, 250), "silver": (210, 214, 224),
        "silver_dark": (100, 104, 116), "red": (220, 40, 40), "white": (246, 246, 250), "yellow": (250, 210, 50),
        "violet": (90, 70, 140), "violet_dark": (40, 30, 80), "black": (30, 30, 40), "lens": (100, 220, 250),
        "lens_light": (220, 250, 255), "eye": (250, 220, 60)}
SHINY = {"blue": (40, 140, 80), "blue_dark": (14, 70, 30), "blue_light": (130, 220, 160), "violet": (140, 40, 50),
         "violet_dark": (70, 14, 20)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = armour(P, "blue", "blue_dark", light="blue_light", trim="silver", trim_w=0.3)
SILVER = metal(P, "silver", dark="silver_dark")


def waistf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y % 1.6) < 0.8 else p["white"], face), None


def build():
    m = Model("invisimon")
    mats = {"skin": BLUE, "chest": BLUE, "abs": SILVER, "pelvis": waistf, "neck": SILVER, "deltoid": BLUE,
            "upper_arm": SILVER, "forearm": BLUE, "hand": BLUE, "finger": BLUE, "thigh": SILVER, "knee": BLUE,
            "shin": armour(P, "red", "red", trim="yellow", trim_w=0.3), "calf": BLUE, "foot": solid(P, "yellow"),
            "toe": solid(P, "red")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.1, name="invisimon")
    bd = a["body"]
    m.round_box(bd, 0, -3.6, 2.0, 0.4, 44.0, 47.0, gem(P, "lens", "lens_light"), cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.0, 60.4, BLUE, cut=1)
    m.round_box(hd, 0, -3.2, 2.2, 0.4, 56.4, 58.8, solid(P, "black"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 57.2, -3.7, max(sx * 0.6, sx * 1.8), 58.0, -3.6, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.8, 59.0, 0), (sx * 0.5, 1, 0.3), 1.0, 3.0, solid(P, "yellow"), tip=0.8)
    m.round_box(hd, 0, 0.8, 4.0, 4.0, 55.0, 62.4, fabric(P, "violet", "violet_dark"), cut=2)  # hood
    for sx in (-1, 1):                                                              # round shoulder pods
        m.round_box(bd, sx * 8.0, 0.0, 3.2, 3.2, 47.0, 53.0, BLUE, cut=2)
        m.round_box(bd, sx * 8.0, -3.4, 1.6, 0.4, 48.6, 51.4, gem(P, "lens", "lens_light"), cut=0)
    cape(m, bd, 53.0, 14.0, 44.0, fabric(P, "violet", "violet_dark"), z=4.0, flare=0.9, panels=8, sweep=(6.0, 4.0))
    hr = a["arm_right"]                                                              # huge fist
    hx, hy, hz = hr["hand"]
    m.round_box(hr["bone"], hx, hz, 3.4, 3.4, hy - 4.0, hy + 2.0, BLUE, cut=2)
    hl = a["arm_left"]                                                               # long silver blade-shield
    hx, hy, hz = hl["hand"]
    for j in range(5):
        m.round_box(hl["bone"], hx + 1.6, hz - 2.0 - j * 0.2, 0.6, 3.6 - j * 0.4, hy - 18.0 + j * 7.0,
                    hy - 10.0 + j * 7.0, SILVER, cut=0)
    spike(m, hl["bone"], (hx + 1.6, hy - 18.0, hz - 2.0), (0, -1, 0), 2.0, 6.0, SILVER, tip=0.8)
    m.round_box(hl["bone"], hx + 2.4, hz - 2.0, 0.6, 1.6, hy - 4.0, hy + 4.0, solid(P, "black"), cut=0)
    return m
