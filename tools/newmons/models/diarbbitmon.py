"""Diarbbitmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the twin-flame rabbit knight. An upright rabbit warrior with tall ears, a calm face, a long
cream officer's coat with gold buttons, a brown belt and pouches, puffed grey breeches, tall gold boots and a big
fluffy cream tail with a dark tip, wielding a sword wreathed in crimson flame in one hand and one wreathed in blue
flame in the other. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, flame_inside, fur, leather, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("an upright rabbit knight with tall ears, a cream officer's coat, puffed grey breeches, gold boots and a fluffy "
        "tail, wielding one sword wreathed in crimson flame and one in blue flame")
BASE = {"fur": (220, 200, 160), "fur_dark": (150, 120, 80), "coat": (236, 226, 196), "coat_dark": (170, 156, 120),
        "gold": (230, 186, 70), "gold_dark": (150, 110, 20), "grey": (130, 132, 150), "grey_dark": (70, 72, 90),
        "brown": (120, 80, 40), "brown_dark": (60, 36, 14), "tip": (60, 50, 40), "eye": (40, 30, 30),
        "red": (230, 60, 70, 220), "red_core": (255, 220, 220, 240), "blue": (90, 150, 255, 220),
        "blue_core": (220, 240, 255, 240), "steel": (220, 224, 236), "steel_dark": (110, 114, 128)}
SHINY = {"fur": (200, 200, 210), "fur_dark": (120, 120, 140), "coat": (60, 60, 80), "coat_dark": (24, 24, 40)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", length=1.0)
COAT = fabric(P, "coat", "coat_dark", axis="y")
GOLD = armour(P, "gold", "gold_dark")
PUFF = fabric(P, "grey", "grey_dark", axis="x", period=1.6)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.5 and (y % 3.0) < 0.8 and y > 38:
        return tone(p["gold"], face), None
    return COAT(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.5 and abs(y - 58.0) < 0.3:
                return tone(p["eye"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def flamef(key, core):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p[core] if abs(u - W / 2) < W * 0.15 else p[key]
        return c, c[:3]
    return s


def build():
    m = Model("diarbbitmon")
    mats = {"skin": FUR, "chest": coatf, "abs": coatf, "pelvis": leather(P, "brown", "brown_dark"), "neck": FUR,
            "deltoid": coatf, "upper_arm": coatf, "forearm": coatf, "hand": FUR, "finger": FUR, "thigh": PUFF,
            "knee": PUFF, "shin": GOLD, "calf": GOLD, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=1.15, name="diarbbitmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 3.0, 54.0, 60.0, headf, cut=1)
    m.round_box(hd, 0, -3.6, 1.2, 1.2, 55.0, 57.0, FUR, cut=0)                          # muzzle
    for sx in (-1, 1):                                                                 # tall ears
        m.round_box(hd, sx * 1.4, 0.4, 0.9, 0.9, 59.6, 70.0, FUR, cut=0)
    cape(m, bd, 50.0, 11.0, 30.0, COAT, z=3.0, flare=0.5)                               # coat tails
    tb = m.bone("tail", bd, (0, 32, 5))
    ball(m, tb, (0, 30.0, 10.0), 5.0, fur(P, "coat", "tip", length=1.6), layers=5)      # fluffy tail
    for nm, key, core in (("arm_right", "red", "red_core"), ("arm_left", "blue", "blue_core")):   # flame swords
        ar = a[nm]
        hx, hy, hz = ar["hand"]
        tip = (hx * 1.6, hy + 22.0, hz - 6.0)
        rod(m, ar["bone"], (hx, hy, hz), tip, 1, metal(P, "steel", dark="steel_dark"), extend=0, t2=2)
        m.box(ar["bone"], hx - 1.6, hy - 0.4, hz - 0.6, hx + 1.6, hy + 0.6, hz + 0.6, GOLD)
        for ang in (0, 90):
            m.box(ar["bone"], hx - 3.0, hy + 2.0, hz - 3.0, hx + 3.0, hy + 24.0, hz - 3.0,
                  cutout(flame_inside(5, 0.1, ang), flamef(key, core)), rotation=(-15, ang, 0),
                  pivot=(hx, hy + 2.0, hz - 3.0))
    return m
