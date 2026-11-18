"""Karatenmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the crow tengu: a lean warrior in a violet ninja hood and mask with one glaring eye, violet arm
guards, a dark kimono over a grey hakama skirt tied with a red sash, great black feathered wings, yellow bird talons,
and two short jutte-like swords in its hands. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import fabric, feathers, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean crow tengu in a violet ninja hood and mask, a dark kimono and grey hakama, great black wings, yellow talons and two short swords"
BASE = {"violet": (100, 60, 160), "violet_dark": (40, 20, 80), "black": (40, 38, 46), "black_dark": (12, 12, 16),
        "grey": (200, 196, 186), "grey_dark": (130, 126, 116), "red": (200, 40, 40), "yellow": (240, 200, 60),
        "yellow_dark": (180, 130, 20), "eye": (250, 220, 60), "steel": (210, 214, 224), "steel_dark": (100, 104, 116),
        "gold": (220, 180, 60)}
SHINY = {"violet": (40, 120, 140), "violet_dark": (14, 60, 70), "black": (230, 230, 236), "black_dark": (150, 150, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HOOD = fabric(P, "violet", "violet_dark")
KIMONO = fabric(P, "black", "black_dark")
HAKAMA = fabric(P, "grey", "grey_dark", period=1.6)


def hoodf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x - 0.8, y - 57.8) < 0.7:
        return tone(p["eye"], face), p["eye"]
    return HOOD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("karatenmon")
    mats = {"skin": KIMONO, "chest": KIMONO, "abs": KIMONO, "pelvis": HAKAMA, "neck": HOOD, "deltoid": HOOD,
            "upper_arm": KIMONO, "forearm": leather(P, "violet", "violet_dark"), "hand": KIMONO, "finger": KIMONO,
            "thigh": HAKAMA, "knee": HAKAMA, "shin": skin(P, "yellow", dark="yellow_dark"),
            "calf": skin(P, "yellow", dark="yellow_dark"), "foot": skin(P, "yellow", dark="yellow_dark"),
            "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.88, leg_bulk=0.85, talons=True, digitigrade=True, name="karatenmon")
    bd = a["body"]
    m.round_box(bd, 0, 0.2, 4.4, 3.4, 33.6, 35.6, solid(P, "red"), cut=1)                   # red sash
    for j in range(6):                                                               # hakama skirt
        ang = math.radians(-75 + j * 30)
        spike(m, bd, (3.8 * math.sin(ang), 33.6, -3.0 * math.cos(ang)), (math.sin(ang) * 0.3, -1, -math.cos(ang) * 0.3),
              3.0, 12.0, HAKAMA, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, hoodf, cut=1)
    spike(m, hd, (0, 56.6, -3.2), (0, -0.4, -1), 1.6, 3.6, solid(P, "black"), tip=0.8)       # crow beak-mask
    for side in (1, -1):                                                              # great black wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 3.4))
        feather_wing(m, wb, (side * 3.0, 50.0, 3.4), 30.0, 14.0, 3, feathers(P, "black", "black_dark", tip="violet"),
                     side=side, sweep=15, droop=12.0)
    for nm in ("arm_left", "arm_right"):                                              # two short swords
        hx, hy, hz = a[nm]["hand"]
        sx = 1 if hx > 0 else -1
        rod(m, a[nm]["bone"], (hx, hy - 1.0, hz + 1.0), (hx + sx * 2.0, hy - 1.0, hz - 14.0), 1,
            metal(P, "steel", dark="steel_dark"), extend=0, t2=1)
        m.round_box(a[nm]["bone"], hx, hz, 1.6, 0.6, hy - 1.6, hy - 0.4, solid(P, "gold"), cut=0)
    return m
