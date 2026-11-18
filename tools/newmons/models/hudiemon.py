"""Hudiemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
butterfly fairy: a slender fairy in a high-collared blue-and-white bodysuit with a long flowing skirt of petals, long
gloves, a pale face framed by blue hair tied with a ribbon, two long antennae and four great blue butterfly wings
patterned with white eye-spots. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built as officially drawn: fully clothed.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, fabric, local, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a slender butterfly fairy in a blue-and-white bodysuit with a petal skirt, long gloves, blue hair, long antennae "
        "and four great blue butterfly wings with white eye-spots")
BASE = {"blue": (60, 120, 220), "blue_dark": (20, 50, 140), "white": (246, 246, 250), "white_dark": (180, 186, 210),
        "skin": (250, 226, 210), "skin_dark": (210, 170, 150), "hair": (50, 90, 190), "hair_dark": (20, 40, 120),
        "wing": (90, 170, 250, 220), "wing_dark": (30, 70, 170, 230), "spot": (250, 250, 255, 235),
        "eye": (60, 140, 220), "black": (24, 24, 30), "pink": (240, 140, 180)}
SHINY = {"blue": (200, 70, 150), "blue_dark": (120, 20, 80), "hair": (200, 80, 150), "wing": (250, 140, 200, 220),
         "wing_dark": (180, 50, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "blue", "blue_dark", axis="y")
WHITE = fabric(P, "white", "white_dark", axis="y")
SKIN = skin(P, "skin", dark="skin_dark")


def faceF(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.1) < 0.5 and abs(y - 58.0) < 0.5:
                return tone(p["eye"], face), None
        if abs(x) < 0.5 and abs(y - 55.8) < 0.2:
            return tone(p["pink"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def wing_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    return a * a / 0.25 + b * b / 0.25 < 1.0


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    r = math.hypot(a, b)
    if math.hypot(a - 0.1, b - 0.1) < 0.12:
        return p["spot"], None
    c = p["wing_dark"] if r > 0.42 else p["wing"]
    return c, None


def build():
    m = Model("hudiemon")
    mats = {"skin": SKIN, "chest": SUIT, "abs": WHITE, "pelvis": SUIT, "neck": WHITE, "deltoid": SUIT,
            "upper_arm": WHITE, "forearm": SUIT, "hand": SUIT, "finger": SUIT, "thigh": SUIT, "knee": SUIT,
            "shin": SUIT, "calf": SUIT, "foot": solid(P, "blue_dark"), "toe": solid(P, "blue_dark")}
    a = humanoid(m, mats, bulk=0.78, arm_bulk=0.8, leg_bulk=0.82, name="hudiemon")
    bd = a["body"]
    for i in range(10):                                                            # flowing petal skirt
        ang = 2 * math.pi * i / 10
        spike(m, bd, (3.6 * math.cos(ang), 32.0, 3.0 * math.sin(ang)), (math.cos(ang) * 0.3, -1, math.sin(ang) * 0.3),
              2.4, 12.0, WHITE if i % 2 else SUIT, tip=0.8)
    m.round_box(bd, 0, 0.6, 2.6, 2.6, 50.0, 53.0, WHITE, cut=1)                         # high collar
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.4, faceF, cut=1)
    m.round_box(hd, 0, 0.8, 2.8, 2.4, 57.0, 61.4, strands(P, "hair", "hair_dark"), cut=1)
    for i in range(7):                                                             # long hair down the back
        ang = math.radians(-90 + i * 30)
        rod(m, hd, (2.4 * math.sin(ang), 60.0, 1.0 + math.cos(ang)), (3.0 * math.sin(ang), 49.0, 3.4), 1,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    m.round_box(hd, 0, 2.8, 1.6, 0.6, 58.6, 60.4, solid(P, "pink"), cut=0)              # ribbon
    for sx in (-1, 1):                                                              # antennae
        pts = [(sx * 1.0, 61.0, -0.6), (sx * 2.6, 65.0, -1.6), (sx * 4.2, 67.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "black"), extend=0.2, t2=1)
        m.round_box(hd, sx * 4.4, -1.0, 0.6, 0.6, 66.6, 67.8, solid(P, "blue"), cut=0)
    W = cutout(wing_in, wingf)
    for side in (1, -1):                                                            # four butterfly wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.0, 46.0, 3.6))
        x0, x1 = sorted((side * 2.0, side * 22.0))
        m.box(wb, x0, 44.0, 3.8, x1, 64.0, 3.8, W, rotation=(0, side * -20, side * -10), pivot=(side * 2.0, 46.0, 3.8))
        x0, x1 = sorted((side * 2.0, side * 16.0))
        m.box(wb, x0, 30.0, 3.8, x1, 45.0, 3.8, W, rotation=(0, side * -20, side * 15), pivot=(side * 2.0, 44.0, 3.8))
    return m
