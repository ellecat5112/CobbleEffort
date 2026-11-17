"""Dinohumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the lizard warrior. A muscular green lizard-man with a darker scaly hide, a shaggy violet-and-pink
feather collar and bracers, a red-and-white checked loincloth, a big steel war hammer slung on its back, a curved
steel blade in one hand, a long steel shield with a spike on the other arm, and clawed feet. 15 blocks tall.

Front is -z, y is up. 62 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, feathers, local, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a muscular green lizard warrior with violet feather collar and bracers, a checked loincloth, a war hammer on its "
        "back, a curved blade and a long spiked shield")
BASE = {"green": (90, 120, 60), "green_dark": (40, 56, 24), "green_light": (150, 180, 110), "violet": (130, 60, 140),
        "violet_dark": (60, 20, 70), "pink": (230, 130, 170), "red": (200, 40, 40), "white": (240, 240, 244),
        "steel": (210, 214, 226), "steel_dark": (100, 104, 116), "wood": (120, 80, 40), "eye": (250, 220, 60),
        "mouth": (100, 20, 30), "claw": (230, 226, 210)}
SHINY = {"green": (140, 100, 70), "green_dark": (70, 44, 24), "green_light": (200, 160, 120), "violet": (50, 110, 170)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.2, light="green_light", rim_mix=0.3)
FEATH = feathers(P, "violet", "violet_dark", size=(1.2, 2.0), tip="pink")
STEEL = metal(P, "steel", dark="steel_dark")


def checkf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (int(x // 1.4) + int(y // 1.4)) % 2 else p["white"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.5 and abs(y - 58.6) < 0.3:
                return p["eye"], p["eye"]
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dinohumon")
    mats = {"skin": HIDE, "chest": HIDE, "abs": HIDE, "pelvis": checkf, "neck": FEATH, "deltoid": HIDE,
            "upper_arm": HIDE, "forearm": FEATH, "hand": HIDE, "finger": HIDE, "claw": solid(P, "claw"),
            "thigh": HIDE, "knee": HIDE, "shin": HIDE, "calf": HIDE, "foot": HIDE, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.25, leg_bulk=1.1, claws=True, talons=True, digitigrade=True,
                 name="dinohumon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.8, 4.0, 54.0, 60.0, headf, cut=1)                     # lizard head
    m.box(hd, -2.0, 54.0, -6.4, 2.0, 55.6, -4.0, HIDE)                                 # snout
    m.box(hd, -1.8, 55.0, -6.6, 1.8, 55.4, -4.0, solid(P, "mouth"))
    for i in range(10):                                                                # shaggy feather collar
        ang = math.radians(i * 36)
        spike(m, bd, (4.4 * math.sin(ang), 52.0, -3.4 * math.cos(ang)), (math.sin(ang), -0.6, -math.cos(ang)),
              2.0, 4.0, FEATH, tip=0.6)
    for sx in (-1, 1):                                                                 # checked loincloth flaps
        m.box(bd, min(sx * 0.4, sx * 3.6), 22.0, -4.0, max(sx * 0.4, sx * 3.6), 31.0, -3.4, checkf)
    hb = m.bone("hammer", bd, (0, 48, 4))                                              # war hammer on the back
    rod(m, hb, (-6.0, 38.0, 4.6), (6.0, 66.0, 4.6), 1, solid(P, "wood"), extend=0)
    m.round_box(hb, 6.4, 4.6, 3.0, 2.4, 64.0, 70.0, STEEL, cut=1)
    al = a["arm_left"]                                                                 # long spiked shield
    h = al["hand"]
    sx = 1 if h[0] > 0 else -1
    m.round_box(al["bone"], h[0] + sx * 1.6, h[2] - 3.0, 0.6, 5.0, h[1] - 14.0, h[1] + 8.0, STEEL, cut=0)
    spike(m, al["bone"], (h[0] + sx * 1.6, h[1] - 14.0, h[2] - 3.0), (0, -1, 0), 2.0, 5.0, STEEL, tip=0.5)
    ar = a["arm_right"]                                                                # curved blade
    h = ar["hand"]
    pts = [(h[0], h[1], h[2]), (h[0] - 1.0, h[1] - 6.0, h[2] - 6.0), (h[0] - 1.0, h[1] - 8.0, h[2] - 13.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, ar["bone"], p0, p1, 1, STEEL, extend=0.4, t2=3)
    return m
