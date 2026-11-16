"""Ariemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a sea sorceress in her official robes. Pale-blue skin, a wide-sleeved pink robe dotted with white
water drops and frilled at the hems in pale blue, a broad shell hat with a pink panel and pearl, a long staff topped
with a spiral shell, a pearl and a green ribbon, and a fish tail with a crescent fluke. 35 blocks tall.

Front is -z, y is up. 70 units tall (the staff); Ultimate stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, local, metal, mix, plane, skin, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "floater"
K = 3
LOOK = ("a sea sorceress: pale-blue skin, a wide-sleeved pink robe dotted with water drops and frilled in pale blue, a "
        "broad shell hat with a pearl, a spiral-shell staff with a green ribbon and a fish tail")
BASE = {"pink": (226, 90, 160), "pink_dark": (150, 40, 100), "frill": (190, 230, 246), "frill_dark": (130, 180, 210),
        "skin": (120, 190, 220), "skin_dark": (70, 130, 170), "shell": (200, 200, 214), "shell_dark": (110, 110, 126),
        "pearl": (240, 236, 250), "green": (60, 190, 140), "green_dark": (20, 120, 80), "white": (250, 250, 252),
        "eye": (240, 60, 120)}
SHINY = {"pink": (90, 70, 190), "pink_dark": (40, 26, 120), "skin": (230, 200, 170), "skin_dark": (180, 140, 110),
         "green": (240, 180, 60), "green_dark": (180, 120, 20)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark", var=0.03)
SHELL = armour(P, "shell", "shell_dark", seams=(1.4,))
FRILL = fabric(P, "frill", "frill_dark", axis="x", period=1.2)


def robef(x, y, z, face, variant, box=None, **k):
    """Pink robe dotted with white water drops."""
    p = P(variant)
    a, b = plane(x, y, z, face)
    cu, cv = round(a / 3.0) * 3.0 + (1.5 if round(b / 3.4) % 2 else 0), round(b / 3.4) * 3.4
    du, dv = a - cu, b - cv
    if du * du / 0.5 + (dv + 0.4) ** 2 / 0.9 < 1 and dv < 0.8 - abs(du) * 0.6 + 0.6:
        return tone(p["white"], face), None
    return fabric(P, "pink", "pink_dark", axis="y", period=2.6)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ariemon")
    mats = {"skin": SKIN, "chest": robef, "abs": robef, "pelvis": robef, "neck": SKIN, "deltoid": robef,
            "upper_arm": robef, "forearm": robef, "hand": SKIN, "finger": SKIN, "thigh": SKIN, "knee": SKIN,
            "shin": SKIN, "calf": SKIN, "foot": SKIN, "toe": SKIN}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.8, name="ariemon", hand_pose="open", chest_depth=0.9)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, SKIN, cut=1)
    m.box(hd, -0.5, 59.0, -2.6, 0.5, 60.0, -2.3, solid(P, "eye", glow=True))            # brow jewel
    m.round_box(hd, 0, 0.6, 7.0, 6.0, 60.4, 62.0, SHELL, cut=2)                          # the broad shell hat
    m.round_box(hd, 0, 0.6, 3.6, 3.6, 62.0, 66.0, SHELL, cut=1)
    m.box(hd, -2.0, 62.6, -3.8, 2.0, 65.4, -3.0, solid(P, "pink"))
    ball(m, hd, (0, 64.0, -4.0), 0.9, solid(P, "pearl"), layers=2)
    for i in range(5):
        spike(m, hd, (-3.0 + i * 1.5, 65.6, 0.6), (0, 1, 0.3), 1.0, 2.0, SHELL)
    sk = m.bone("skirt", bd, (0, 34, 0))
    for i in range(12):                                          # the robe flaring out, frilled hem
        ang = math.radians(-165 + i * 30)
        c = (4.4 * math.sin(ang), 34.0, -3.8 * math.cos(ang))
        m.box(sk, c[0] - 1.8, 6.0, c[2], c[0] + 1.8, 34.0, c[2] + 0.8, robef,
              rotation=(-14 * math.cos(ang), -math.degrees(ang), -12 * math.sin(ang)), pivot=c)
        m.box(sk, c[0] - 2.0, 2.0, c[2] - 0.1, c[0] + 2.0, 6.4, c[2] + 0.9, FRILL,
              rotation=(-14 * math.cos(ang), -math.degrees(ang), -12 * math.sin(ang)), pivot=c)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # wide hanging sleeves
        el = a[nm]["elbow"]
        m.box(a[nm]["bone"], el[0] - 3.0, el[1] - 14.0, el[2] - 3.0, el[0] + 3.0, el[1] + 2.0, el[2] + 3.0, robef)
        m.box(a[nm]["bone"], el[0] - 3.2, el[1] - 16.0, el[2] - 3.2, el[0] + 3.2, el[1] - 13.6, el[2] + 3.2, FRILL)
    tl = m.bone("tail", bd, (0, 8, 2))                           # fish tail under the robe
    rod(m, tl, (0, 8.0, 2.0), (2.0, 2.0, 6.0), 3, SKIN, extend=0.4)
    for sx in (-1, 1):
        rod(m, tl, (2.0, 2.0, 6.0), (2.0 + sx * 4.0, 0.6, 9.0), 2, SKIN, extend=0.3, t2=1)
    ar = a["arm_right"]                                          # the shell staff
    h = ar["hand"]
    st = m.bone("staff", ar["bone"], h)
    rod(m, st, (h[0], h[1] - 24.0, h[2]), (h[0], h[1] + 36.0, h[2]), 1, SHELL, extend=0)
    for i in range(4):
        r = 3.0 - i * 0.6
        m.round_box(st, h[0], h[2], r, r, h[1] + 36.0 + i * 1.8, h[1] + 38.0 + i * 1.8, SHELL, cut=1)
    ball(m, st, (h[0], h[1] + 34.0, h[2] - 1.0), 1.2, solid(P, "pearl"), layers=2)
    for j in range(4):
        rod(m, st, (h[0], h[1] + 33.0, h[2]), (h[0] + (j - 1.5) * 1.6, h[1] + 24.0 - j * 2, h[2] + 0.6), 1,
            fabric(P, "green", "green_dark"), extend=0.2, t2=2)
    return m
