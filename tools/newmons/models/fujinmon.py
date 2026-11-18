"""Fujinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the wind god of the Three Great Angels' guard. A tall, slender green-armoured android with a
spined green crest-helm sweeping back, digitigrade legs on long splayed claws, a heavy grey wind-gatling on its right
arm spitting fire, a backpack with a glowing red-orange turbine core and a long thin tail. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, local, metal, riveted, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall slender green-armoured android with a spined crest-helm, digitigrade legs on long claws, a heavy grey "
        "wind-gatling spitting fire, a glowing turbine backpack and a thin tail")
BASE = {"green": (60, 190, 90), "green_dark": (20, 100, 40), "green_light": (170, 250, 170), "grey": (180, 184, 196),
        "grey_dark": (90, 94, 106), "black": (34, 32, 38), "black_dark": (14, 14, 18), "core": (250, 120, 40),
        "core_light": (255, 220, 120), "eye": (250, 230, 70), "fire": (255, 120, 50, 210),
        "fire_core": (255, 240, 180, 235)}
SHINY = {"green": (200, 200, 210), "green_dark": (110, 110, 124), "green_light": (250, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = armour(P, "green", "green_dark", light="green_light", trim="black", trim_w=0.25)
GREY = metal(P, "grey", dark="grey_dark")
DARK = riveted(P, "black", "black_dark")


def coref(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["core_light"] if math.hypot(u - W / 2, v - H / 2) < min(W, H) * 0.25 else p["core"]
    return c, c


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.35 else p["fire"]
    return c, c[:3]


def build():
    m = Model("fujinmon")
    mats = {"skin": DARK, "chest": GREEN, "abs": DARK, "pelvis": GREEN, "neck": DARK, "deltoid": GREEN,
            "upper_arm": DARK, "forearm": GREEN, "hand": GREEN, "finger": GREEN, "claw": GREEN, "thigh": GREEN,
            "knee": GREEN, "shin": GREEN, "calf": GREEN, "foot": GREEN, "talon": solid(P, "green_light")}
    a = humanoid(m, mats, bulk=0.78, arm_bulk=0.85, leg_bulk=0.9, claws=True, talons=True, digitigrade=True, toes=3,
                 name="fujinmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.2, 3.0, 53.6, 59.4, GREEN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 56.6, -3.7, max(sx * 0.6, sx * 1.8), 57.2, -3.5, solid(P, "eye", glow=True))
    for j in range(7):                                                                   # spined crest sweeping back
        spike(m, hd, (0, 59.0 - j * 0.4, -1.0 + j * 1.6), (0, 0.6, 1), 1.4, 8.0 - j * 0.5, GREEN, tip=0.25)
    m.round_box(bd, 0, 5.6, 4.6, 2.6, 40.0, 52.0, GREY, cut=1)                           # turbine backpack
    m.round_box(bd, 0, 8.4, 3.0, 0.4, 42.0, 50.0, coref, cut=0)
    for sx in (-1, 1):
        rod(m, bd, (sx * 4.0, 50.0, 6.0), (sx * 7.0, 62.0, 9.0), 1, GREEN, extend=0.2, t2=1)    # backpack antennae
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                               # wind-gatling
    m.round_box(ar, h[0] - 1.0, h[2] - 6.0, 3.0, 9.0, h[1] - 1.0, h[1] + 5.0, GREY, cut=1)
    for j in range(4):
        ang = math.radians(45 + j * 90)
        rod(m, ar, (h[0] - 1.0 + 1.4 * math.cos(ang), h[1] + 2.0 + 1.4 * math.sin(ang), h[2] - 15.0),
            (h[0] - 1.0 + 1.4 * math.cos(ang), h[1] + 2.0 + 1.4 * math.sin(ang), h[2] - 22.0), 1, DARK, extend=0)
    for ang in (0, 90):
        m.box(ar, h[0] - 3.0, h[1] + 0.0, h[2] - 23.0, h[0] + 1.0, h[1] + 4.0, h[2] - 23.0,
              cutout(flame_inside(4, 0.0, 3), firef), rotation=(ang, 0, 0), pivot=(h[0] - 1.0, h[1] + 2.0, h[2] - 23.0))
    tb = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (0, 24.0, 10.0), (2.0, 14.0, 14.0), (4.0, 6.0, 15.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, DARK, extend=0.3, t2=1)
    return m
