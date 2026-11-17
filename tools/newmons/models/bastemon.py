"""Bastemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a cat-goddess, in her official outfit: a leopard-spotted bodysuit with wide leopard-print trousers,
a red-and-gold top, a violet veil over the lower face, long red hair in a braid, tall cat ears with a gold circlet,
gold bracelets and anklets, pink-tipped claws and a long spotted tail ringed in gold. 25 blocks tall.

Front is -z, y is up. 70 units tall; Perfect stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, local, metal, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a cat-goddess in a leopard-spotted bodysuit and wide leopard trousers, a red-and-gold top, a violet veil, a "
        "long red braid, tall cat ears with a gold circlet, gold bracelets, pink-tipped claws and a spotted tail")
BASE = {"fur": (200, 170, 120), "fur_dark": (140, 110, 70), "spot": (90, 60, 30), "spot_light": (240, 220, 160),
        "red": (200, 40, 50), "red_dark": (110, 14, 24), "gold": (236, 196, 70), "gold_dark": (160, 120, 30),
        "veil": (170, 140, 210), "hair": (190, 60, 50), "hair_dark": (120, 30, 24), "claw": (240, 80, 150),
        "eye": (120, 90, 200)}
SHINY = {"fur": (170, 170, 190), "fur_dark": (110, 110, 130), "spot": (40, 40, 60), "spot_light": (220, 220, 240),
         "red": (40, 140, 160), "red_dark": (16, 80, 90), "hair": (60, 70, 160), "hair_dark": (24, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark")
HAIR = strands(P, "hair", "hair_dark")


def leopard(light=False):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        cu, cv = round(a / 2.0) * 2.0 + (1.0 if round(b / 2.0) % 2 else 0), round(b / 2.0) * 2.0
        d = math.hypot((a - cu) / 1.2, b - cv)
        base = p["spot_light"] if light else p["fur"]
        if 0.45 < d < 0.75:
            return tone(p["spot"], face), None
        return tone(base, face), None
    return s


def build():
    m = Model("bastemon")
    FUR, PANTS = leopard(), leopard(True)
    TOP = armour(P, "red", "red_dark", trim="gold", trim_w=0.4)
    mats = {"skin": FUR, "chest": TOP, "abs": FUR, "pelvis": PANTS, "neck": FUR, "deltoid": FUR, "upper_arm": FUR,
            "forearm": FUR, "hand": FUR, "finger": FUR, "claw": solid(P, "claw"), "thigh": PANTS, "knee": PANTS,
            "shin": PANTS, "calf": PANTS, "foot": FUR, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.78, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="bastemon", hand_pose="open", chest_depth=0.9)
    bd = a["body"]
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):          # wide trousers
        kn = a[nm]["knee"]
        m.round_box(a[nm]["bone"], kn[0], kn[2], 3.4, 3.4, 12.0, 30.0, PANTS, cut=1)
        an = a[nm]["ankle"]
        m.round_box(a[nm]["bone"], an[0], an[2], 1.8, 1.8, 3.6, 5.0, GOLD, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, FUR, cut=1)
    m.box(hd, -2.0, 54.2, -2.7, 2.0, 57.6, -2.3, solid(P, "veil"))                     # violet veil
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.4, 58.0, -2.6, sx * 0.9 + 0.4, 58.6, -2.4, solid(P, "eye"))
        spike(m, hd, (sx * 1.6, 60.2, 0.0), (sx * 0.4, 1, 0.1), 1.8, 6.0, FUR, tip=0.8)   # tall cat ears
    m.box(hd, -2.4, 59.6, -2.6, 2.4, 60.4, 2.6, GOLD)                                   # gold circlet
    hr = m.bone("mane", hd, (0, 59, 2))
    for i in range(7):
        x = -2.4 + i * 0.8
        rod(m, hr, (x, 59.0, 1.6), (x * 1.3, 48.0, 3.6), 2, HAIR, extend=0.3)
    rod(m, hr, (2.0, 54.0, 2.0), (6.0, 30.0, 3.0), 2, HAIR, extend=0.3)                  # the long braid
    m.box(bd, -4.0, 30.4, -3.6, 4.0, 32.0, 3.6, GOLD)                                   # gold belt
    for nm in ("arm_left", "arm_right"):                          # gold bracelets
        w = a[nm]["wrist"]
        for j in range(3):
            rod(m, a[nm]["bone"], (w[0], w[1] + 1.0 + j * 1.3, w[2]), (w[0], w[1] + 1.6 + j * 1.3, w[2]), 3, GOLD,
                extend=0)
    tl = m.bone("tail", bd, (0, 31, 3))
    pts = [(0, 31, 3), (3, 26, 9), (8, 26, 14), (11, 33, 16), (10, 40, 15)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2, FUR, extend=0.3)
    for p in pts[2:4]:
        rod(m, tl, p, (p[0], p[1] + 0.8, p[2]), 3, GOLD, extend=0)
    return m
