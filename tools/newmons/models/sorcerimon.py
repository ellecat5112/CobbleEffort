"""Sorcerimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the ice wizard: a small sorcerer in a pointed white hat with a black band, a pale hidden face with
yellow eyes, a white robe striped green, a dark-blue cloak lined with snowflakes, brown boots, and a staff crowned with
a glowing blue crystal snowflake. 15 blocks.

Front is -z, y is up. 60 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import fabric, leather, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a small ice wizard in a pointed white hat, a green-striped white robe, a snowflake-lined dark-blue cloak and a glowing snowflake staff"
BASE = {"white": (246, 248, 252), "white_dark": (190, 196, 214), "green": (60, 160, 120), "navy": (30, 40, 90),
        "navy_dark": (12, 16, 40), "brown": (120, 80, 50), "brown_dark": (70, 44, 24), "black": (30, 28, 32),
        "eye": (250, 220, 60), "ice": (120, 200, 255), "face": (240, 240, 246)}
SHINY = {"navy": (110, 30, 60), "navy_dark": (50, 10, 24), "green": (200, 120, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def robef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 4.0) < 1.0:
        return tone(p["green"], face), None
    return fabric(P, "white", "white_dark", axis="y")(x, y, z, face, variant, box=box, **k)


def cloakf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(math.sin(x * 1.2) * math.sin(y * 1.1)) > 0.9:
        return tone(p["white"], face), None
    return tone(p["navy"] if face != "north" else p["navy_dark"], face), None


def build():
    m = Model("sorcerimon")
    mats = {"skin": robef, "neck": solid(P, "face"), "hand": solid(P, "white"), "finger": solid(P, "white"),
            "shin": leather(P, "brown", "brown_dark"), "foot": leather(P, "brown", "brown_dark")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="sorcerimon")
    bd = a["body"]
    cape(m, bd, 52.0, 18.0, 44.0, cloakf, z=4.0, flare=2.2, panels=7, seed=8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 59.0, solid(P, "face"), cut=1)
    m.box(hd, -1.8, 56.4, -3.1, -0.6, 57.2, -2.9, solid(P, "eye", glow=True))
    m.box(hd, 0.6, 56.4, -3.1, 1.8, 57.2, -2.9, solid(P, "eye", glow=True))
    m.round_box(hd, 0, 0, 6.0, 6.0, 58.6, 59.6, solid(P, "white"), cut=2)                    # hat brim
    m.round_box(hd, 0, 0, 3.0, 3.0, 59.6, 61.0, solid(P, "black"), cut=1)
    spike(m, hd, (0, 61.0, 0), (0.3, 1, 0.3), 3.0, 9.0, solid(P, "white"), tip=0.8)
    w = a["arm_left"]["wrist"]                                                           # snowflake staff
    rod(m, a["arm_left"]["bone"], (w[0], 4.0, w[2] - 2.0), (w[0], 60.0, w[2] - 2.0), 1, leather(P, "brown", "brown_dark"),
        extend=0.2)
    for j in range(6):
        ang = 2 * math.pi * j / 6
        spike(m, a["arm_left"]["bone"], (w[0], 62.0, w[2] - 2.0), (0, math.sin(ang), math.cos(ang)), 0.9, 3.4,
              solid(P, "ice", glow=True), tip=0.8)
    return m
