"""Shurimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of sincerity: a ninja plant: a white-bandaged body with baggy white trousers, a
white masked head with a red topknot, two big green leaves sprouting from its back, coiled green spring arms and legs,
and four great blue-steel shuriken for hands and feet. 15 blocks.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a ninja plant with a white masked head and red topknot, two big green leaves, coiled green spring limbs and four blue-steel shuriken"
BASE = {"white": (246, 244, 236), "white_dark": (190, 186, 170), "green": (100, 180, 70), "green_dark": (40, 110, 30),
        "red": (220, 40, 40), "steel": (60, 90, 170), "steel_dark": (20, 34, 90), "silver": (220, 224, 236),
        "eye": (250, 220, 60), "black": (30, 28, 32)}
SHINY = {"green": (220, 140, 60), "green_dark": (150, 80, 20), "steel": (170, 60, 60), "steel_dark": (90, 20, 20)}


def P(v):
    return pal(BASE, SHINY, v)


CLOTH = fabric(P, "white", "white_dark", axis="y", period=1.6)


def springf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green"] if (y + x) % 1.4 < 0.9 else p["green_dark"], face), None


def shuriken(m, bone, c, s):
    for j in range(4):
        ang = math.radians(45 + j * 90)
        spike(m, bone, c, (math.cos(ang), math.sin(ang), 0), 2.4 * s, 6.0 * s, metal(P, "steel", dark="steel_dark"),
              tip=0.8)
    m.round_box(bone, c[0], c[2], 1.6 * s, 0.8, c[1] - 1.6 * s, c[1] + 1.6 * s, metal(P, "silver"), cut=0)


def build():
    m = Model("shurimon")
    top = m.bone("shurimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0, 4.0, 3.0, 16.0, 26.0, CLOTH, cut=1)
    m.round_box(bd, 0, 0, 5.0, 3.6, 12.0, 17.0, CLOTH, cut=1)                               # baggy trousers
    hd = m.bone("head", bd, (0, 26, 0))
    ball(m, hd, (0, 30.0, 0), 3.6, skin(P, "white", dark="white_dark"), layers=3, ry=4.0)
    m.round_box(hd, 0, -3.2, 3.0, 0.6, 29.0, 31.0, solid(P, "black"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 29.6, -3.9, max(sx * 0.6, sx * 1.8), 30.4, -3.7, solid(P, "eye", glow=True))
    for j in range(4):
        spike(m, hd, (0, 33.6, 0.6), ((j - 1.5) * 0.3, 1, 0.3), 1.0, 4.0, strands(P, "red", "red"), tip=0.8)
    for sx in (-1, 1):                                                                   # two big leaves
        m.box(bd, min(sx * 2.0, sx * 12.0), 26.0, 3.0, max(sx * 2.0, sx * 12.0), 34.0, 3.0,
              skin(P, "green", dark="green_dark"), rotation=(0, -sx * 20, sx * 25), pivot=(sx * 2.0, 28.0, 3.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 24.0, 0))
        rod(m, ab, (sx * 4.0, 24.0, 0), (sx * 12.0, 18.0, -1.0), 1, springf, extend=0.2, t2=2)
        shuriken(m, ab, (sx * 14.0, 17.0, -1.0), 1.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 13.0, 0))
        rod(m, lg, (sx * 3.0, 13.0, 0), (sx * 6.0, 6.0, -1.0), 1, springf, extend=0.2, t2=2)
        shuriken(m, lg, (sx * 7.0, 6.0, -1.0), 0.9)
    return m
