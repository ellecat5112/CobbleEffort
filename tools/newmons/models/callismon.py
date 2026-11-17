"""Callismon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the gunslinger werebear. A hulking violet-furred bear-man with a shaggy mane, glowing eyes and a
scarred snout, a black leather vest crossed by a brown bandolier, black trousers, clawed feet, and a huge four-barrel
rotary cannon in its right hand. 35 blocks tall.

Front is -z, y is up. 62 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, leather, metal, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking violet-furred bear-man with a shaggy mane, a black leather vest and bandolier, black trousers and a "
        "huge four-barrel rotary cannon")
BASE = {"fur": (140, 90, 190), "fur_dark": (70, 40, 110), "fur_tip": (200, 160, 240), "vest": (36, 34, 44),
        "vest_light": (90, 88, 104), "brown": (130, 90, 50), "brown_dark": (80, 50, 24), "steel": (150, 154, 166),
        "steel_dark": (60, 62, 72), "claw": (240, 236, 230), "eye": (250, 220, 90), "brass": (210, 170, 70)}
SHINY = {"fur": (120, 80, 50), "fur_dark": (60, 36, 20), "fur_tip": (190, 150, 110)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_tip", length=1.6)
VEST = leather(P, "vest", "vest_light", stitch="brass")
TROUSER = fabric(P, "vest", "vest_light", axis="y", period=2.4)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("callismon")
    mats = {"skin": FUR, "chest": VEST, "abs": VEST, "pelvis": leather(P, "brown", "brown_dark"), "thigh": TROUSER,
            "knee": TROUSER, "shin": TROUSER, "calf": TROUSER, "foot": FUR, "talon": solid(P, "claw"),
            "claw": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.55, arm_bulk=1.6, leg_bulk=1.4, digitigrade=True, claws=True, talons=True,
                 name="callismon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 53, -2))
    m.round_box(hd, 0, -2.0, 3.4, 3.2, 51.0, 58.4, FUR, cut=1)
    m.box(hd, -2.0, 51.4, -7.6, 2.0, 54.6, -4.6, FUR)                                    # snout
    m.box(hd, -0.9, 53.8, -7.8, 0.9, 54.8, -7.4, solid(P, "vest"))                       # nose
    for sx in (-1, 1):
        m.box(hd, sx * 1.6 - 0.5, 55.6, -5.3, sx * 1.6 + 0.5, 56.2, -5.1, solid(P, "eye", glow=True))
        m.round_box(hd, sx * 2.8, 0.0, 1.2, 1.0, 58.0, 60.0, FUR, cut=1)                # round ears
    for i in range(18):                                                                 # the shaggy mane
        ang = math.radians(-120 + i * 14)
        base = (6.0 * math.sin(ang), 51.0, -1.0 - 4.4 * math.cos(ang))
        spike(m, bd, base, (math.sin(ang) * 0.8, 0.3, -0.5 * math.cos(ang) + 0.3), 3.0, 5.0, FUR, tip=1.0)
    for sx in (-1, 1):                                                                  # vest edges + bandolier
        rod(m, bd, (sx * 6.0, 51.0, -4.4), (-sx * 5.0, 33.0, -4.6), 1, leather(P, "brown", "brown_dark"),
            extend=0.2, t2=2) if sx > 0 else None
    for j in range(6):
        t = j / 5
        x, y = 6.0 - 11.0 * t, 51.0 - 18.0 * t
        m.box(bd, x - 0.5, y - 1.2, -5.6, x + 0.5, y + 1.2, -5.0, solid(P, "brass"))
    # the four-barrel rotary cannon in the right hand
    ar = a["arm_right"]
    h = ar["hand"]
    gb = m.bone("spin_gun", ar["bone"], h)
    m.round_box(gb, h[0], h[2] - 2.0, 3.6, 3.6, h[1] - 3.0, h[1] + 3.0, STEEL, cut=1)
    for i in range(4):
        ang = math.radians(45 + i * 90)
        bx, by = h[0] + 1.8 * math.cos(ang), h[1] + 1.8 * math.sin(ang)
        rod(m, gb, (bx, by, h[2] - 4.0), (bx, by, h[2] - 18.0), 2, STEEL, extend=0)
    for zz in (-8.0, -15.0):
        m.box(gb, h[0] - 3.4, h[1] - 3.4, h[2] + zz - 0.6, h[0] + 3.4, h[1] + 3.4, h[2] + zz + 0.6, solid(P, "steel_dark"))
    return m
