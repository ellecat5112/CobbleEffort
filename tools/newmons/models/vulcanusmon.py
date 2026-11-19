"""Vulcanusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): one of the Olympos Twelve, the god of the forge: a powerful red-skinned smith with six arms,
his head inside a glass diving-dome helm over flame-red hair, a heavy leather apron and baggy red trousers bound at
the shins, sandalled feet, and his hands full of the tools and arms he forged: swords, a spiked flail, clubs, a big
spanner and a hammer. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a six-armed red-skinned forge god in a glass dome helm and leather apron, his hands full of swords, a flail, clubs and a spanner"
BASE = {"red": (200, 60, 50), "red_dark": (120, 26, 20), "trouser": (190, 40, 40), "trouser_dark": (110, 14, 14),
        "leather": (130, 90, 50), "leather_dark": (70, 44, 20), "glass": (170, 220, 230, 130), "hair": (240, 90, 40),
        "hair_dark": (170, 40, 10), "steel": (200, 204, 216), "steel_dark": (100, 104, 120), "wrap": (220, 200, 160),
        "eye": (255, 230, 100)}
SHINY = {"red": (110, 110, 200), "red_dark": (50, 50, 130)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "red", dark="red_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def tool(m, bone, h, kind, sx):
    x, y, z = h
    if kind == "sword":
        m.box(bone, x - 0.6, y, z - 0.5, x + 0.6, y + 14.0, z + 0.5, STEEL, rotation=(0, 0, -sx * 15), pivot=(x, y, z))
    elif kind == "club":
        rod(m, bone, (x, y, z), (x + sx * 2.0, y + 10.0, z), 2, leather(P, "leather", "leather_dark"), extend=0.0)
    elif kind == "flail":
        rod(m, bone, (x, y, z), (x, y + 5.0, z), 1, leather(P, "leather", "leather_dark"), extend=0.0)
        ball(m, bone, (x + sx * 2.0, y + 8.0, z), 1.6, STEEL, layers=2)
        for j in range(6):
            ang = j * math.pi / 3
            spike(m, bone, (x + sx * 2.0 + 1.4 * math.cos(ang), y + 8.0 + 1.4 * math.sin(ang), z),
                  (math.cos(ang), math.sin(ang), 0), 0.8, 1.4, STEEL, tip=0.8)
    else:                                                                              # spanner
        m.box(bone, x - 0.6, y - 10.0, z - 0.6, x + 0.6, y, z + 0.6, STEEL)
        m.box(bone, x - 2.0, y - 12.0, z - 0.6, x + 2.0, y - 10.0, z + 0.6, STEEL)


def build():
    m = Model("vulcanusmon")
    mats = {"skin": SKIN, "chest": SKIN, "abs": leather(P, "leather", "leather_dark"),
            "pelvis": fabric(P, "trouser", "trouser_dark"), "deltoid": SKIN, "upper_arm": SKIN, "forearm": SKIN,
            "hand": SKIN, "finger": SKIN, "thigh": fabric(P, "trouser", "trouser_dark"),
            "knee": fabric(P, "trouser", "trouser_dark"), "shin": fabric(P, "wrap", "leather", axis="x", period=1.2),
            "calf": fabric(P, "wrap", "leather", axis="x", period=1.2), "foot": leather(P, "leather", "leather_dark"),
            "neck": SKIN}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.25, leg_bulk=1.25, name="vulcanusmon")
    bd = a["body"]
    m.box(bd, -4.6, 26.0, -5.0, 4.6, 46.0, -4.0, leather(P, "leather", "leather_dark"))     # apron
    for nm in ("leg_left", "leg_right"):
        k = a[nm]["knee"]
        m.round_box(a[nm]["bone"], k[0], k[2], 3.4, 3.4, 12.0, 26.0, fabric(P, "trouser", "trouser_dark"), cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, SKIN, cut=1)
    m.round_box(hd, 0, 0.6, 3.0, 2.8, 59.0, 61.6, strands(P, "hair", "hair_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 58.0, -3.3, max(sx * 0.6, sx * 1.8), 58.8, -3.0, solid(P, "eye", glow=True))
    ball(m, hd, (0, 58.4, 0), 5.0, solid(P, "glass"), layers=4)                            # glass dome helm
    m.round_box(hd, 0, 0, 4.6, 4.6, 52.4, 54.0, STEEL, cut=2)
    tool(m, a["arm_left"]["bone"], a["arm_left"]["hand"], "spanner", 1)
    tool(m, a["arm_right"]["bone"], a["arm_right"]["hand"], "club", -1)
    for i, (sx, y, kind) in enumerate(((1, 48.0, "sword"), (-1, 48.0, "sword"), (1, 42.0, "flail"),
                                       (-1, 42.0, "club"))):                            # four extra arms
        nm = "arm_extra_%d" % i
        ab = m.bone(nm, bd, (sx * 6.0, y, 1.0))
        hand = (sx * 15.0, y + 8.0, -1.0)
        rod(m, ab, (sx * 6.0, y, 1.0), (sx * 11.0, y + 2.0, 0), 2, SKIN, extend=0.4)
        rod(m, ab, (sx * 11.0, y + 2.0, 0), hand, 2, SKIN, extend=0.4)
        ball(m, ab, hand, 1.6, SKIN, layers=2)
        tool(m, ab, hand, kind, sx)
    return m
