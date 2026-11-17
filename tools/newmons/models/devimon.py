"""Devimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the fallen angel. A tall, gaunt black figure in skin-tight leather bound with straps and buckles, a
red winged sigil on its chest, long arms reaching to its knees ending in clawed hands, a skull clasp on its belt,
boots with red soles, a pale mask-like face with curling horns, a shock of white hair and great tattered black bat
wings. 15 blocks tall.

Front is -z, y is up. 66 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import cutout, leather, local, metal, noise2, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a tall gaunt black fallen angel in strapped leather with a red chest sigil, long clawed arms, a skull belt "
        "clasp, a pale horned mask face, white hair and great tattered bat wings")
BASE = {"black": (40, 40, 46), "black_dark": (10, 10, 14), "black_light": (110, 110, 124), "strap": (90, 70, 60),
        "strap_dark": (40, 26, 20), "steel": (200, 200, 210), "steel_dark": (100, 100, 110), "red": (220, 40, 40),
        "orange": (250, 140, 40), "mask": (220, 220, 226), "mask_dark": (150, 150, 160), "horn": (180, 170, 150),
        "hair": (240, 240, 244), "hair_dark": (170, 170, 180), "eye": (230, 40, 40), "skull": (240, 236, 226)}
SHINY = {"black": (60, 40, 110), "black_dark": (20, 10, 50), "black_light": (150, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


LEATHER = leather(P, "black", "black_dark", stitch="strap")
HIDE = skin(P, "black", dark="black_dark", light="black_light")


def strapped(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and (y % 4.0) < 0.7:
        return tone(p["strap"], face), None
    return LEATHER(x, y, z, face, variant, box=box, **k)


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 44.0 < y < 49.0:
        t = (y - 44.0) / 5.0
        if abs(abs(x) - 2.6 * t - 0.4) < 0.5 and abs(x) < 3.4:
            return tone(p["red"] if t > 0.4 else p["orange"], face), None       # the winged sigil
    return strapped(x, y, z, face, variant, box=box, **k)


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.0) < 0.6 and abs(y - 59.0) < 0.35:
                return p["eye"], p["eye"]
        if abs(y - 56.4) < 0.25 and abs(x) < 1.4:
            return tone(p["black"], face), None
    return skin(P, "mask", dark="mask_dark")(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    return tone(P(variant)["black"], face), None


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return noise2(u * 0.5, v * 0.5, 31) < 0.78


def build():
    m = Model("devimon")
    mats = {"skin": HIDE, "chest": chestf, "abs": strapped, "pelvis": strapped, "neck": HIDE, "deltoid": strapped,
            "upper_arm": strapped, "forearm": strapped, "hand": HIDE, "finger": HIDE, "claw": solid(P, "black_light"),
            "thigh": strapped, "knee": metal(P, "steel", dark="steel_dark"), "shin": strapped, "calf": strapped,
            "foot": LEATHER, "toe": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.9, claws=True, name="devimon")
    bd = a["body"]
    m.round_box(bd, 0, -3.4, 1.4, 0.6, 31.0, 33.6, solid(P, "skull"), cut=0)            # skull belt clasp
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.8, 54.0, 60.4, maskf, cut=1)
    for sx in (-1, 1):                                                                 # curling horns
        pts = [(sx * 2.2, 59.6, 0.0), (sx * 4.0, 61.0, 1.0), (sx * 5.0, 63.4, 0.0), (sx * 4.0, 65.0, -1.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 if j < 1 else 1, solid(P, "horn"), extend=0.4)
    for i in range(9):                                                                 # white hair
        ang = math.radians(-100 + i * 25)
        rod(m, hd, (2.2 * math.sin(ang), 60.4, 0.8 + math.cos(ang)), (3.4 * math.sin(ang), 54.0, 3.6), 2,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=1)
    for nm in ("arm_left", "arm_right"):                                               # long arms reaching low
        ar = a[nm]
        hx, hy, hz = ar["hand"]
        rod(m, ar["bone"], (hx, hy, hz), (hx, hy - 8.0, hz - 1.0), 3, strapped, extend=0.4)
        m.round_box(ar["bone"], hx, hz - 1.0, 1.8, 1.8, hy - 11.0, hy - 8.0, HIDE, cut=1)
        for j in range(4):
            spike(m, ar["bone"], (hx + (j - 1.5) * 0.9, hy - 11.0, hz - 1.4), (0, -1, -0.2), 0.8, 3.6,
                  solid(P, "black_light"), tip=0.25)
    for side in (1, -1):                                                               # tattered bat wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.6, 50.0, 3.4))
        bat_wing(m, wb, (side * 2.6, 50.0, 3.4), 28.0, 30.0, 4, HIDE, cutout(tatter, wingf), side=side, sweep=20)
    return m
