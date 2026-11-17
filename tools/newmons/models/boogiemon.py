"""Boogiemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a gangly red devil. A lean crimson demon-man covered in black swirling tattoos, a long pointed
head with swept horns and a wide toothy leer, violet-webbed bat wings, a whip-thin tail ending in an arrowhead, long
pointed feet and a three-pronged trident. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a lean crimson devil covered in black swirling tattoos, swept horns and a toothy leer, violet bat wings, an "
        "arrow-tipped tail and a trident")
BASE = {"red": (220, 40, 40), "red_dark": (130, 14, 16), "red_light": (255, 120, 110), "tattoo": (40, 16, 30),
        "violet": (140, 70, 180), "violet_dark": (70, 26, 110), "horn": (240, 230, 220), "steel": (200, 204, 216),
        "steel_dark": (90, 94, 106), "tooth": (250, 250, 246), "eye": (250, 240, 120), "mouth": (40, 10, 16)}
SHINY = {"red": (60, 60, 80), "red_dark": (24, 24, 34), "red_light": (140, 140, 170), "tattoo": (230, 60, 60),
         "violet": (220, 60, 60), "violet_dark": (130, 20, 20)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "red", dark="red_dark", light="red_light", var=0.04)


def tattooed(x, y, z, face, variant, box=None, **k):
    """Crimson skin with black swirl tattoos (rings of spirals)."""
    p = P(variant)
    a, b = (x, y) if face in ("north", "south") else (z, y)
    cx, cy = round(a / 6.0) * 6.0, round(b / 6.0) * 6.0
    du, dv = a - cx, b - cy
    r = math.hypot(du, dv)
    th = math.atan2(dv, du)
    if r < 2.6 and abs(((r - th * 0.4) % 1.2) - 0.6) < 0.16:
        return tone(p["tattoo"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.7 and abs(y - 59.2 + sx * 0.0) < 0.35 + 0.2 * (x * sx - 0.6):
                return p["eye"], p["eye"]
        if 55.4 < y < 57.0 and abs(x) < 2.4 - (57.0 - y) * 0.6:
            return tone(p["mouth"] if abs(y - 56.2) < 0.25 else p["tooth"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("boogiemon")
    mats = {"skin": tattooed, "hand": HIDE, "finger": HIDE, "claw": solid(P, "horn"), "foot": HIDE,
            "talon": HIDE}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=0.95, digitigrade=True, claws=True, talons=True,
                 name="boogiemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 2.8, 54.6, 61.0, headf, cut=1)
    m.box(hd, -1.4, 54.6, -4.6, 1.4, 57.0, -3.0, HIDE)                                 # long jaw
    rod(m, hd, (0, 60.6, 0.4), (0, 64.6, 4.0), 2, HIDE, extend=0.3)                     # pointed crown
    for sx in (-1, 1):
        rod(m, hd, (sx * 2.0, 60.4, -0.6), (sx * 5.0, 63.4, 3.4), 1, solid(P, "horn"), extend=0.3, t2=2)
        spike(m, hd, (sx * 2.6, 58.0, 0.6), (sx, 0.3, 0.4), 1.0, 2.4, HIDE)            # pointed ears
    for side in (1, -1):                                                               # bat wings
        bat_wing(m, bd, (side * 2.6, 49.0, 3.4), 18.0, 14.0, 4, solid(P, "red_dark"), solid(P, "violet"),
                 side=side, sweep=22)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32, 3), (2, 26, 8), (5, 22, 13), (9, 22, 17), (13, 24, 19)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, HIDE, extend=0.3)
    spike(m, tl, pts[-1], (1, 0.3, 0.2), 2.4, 2.6, solid(P, "red_dark"), tip=0.4)
    for nm in ("leg_left", "leg_right"):                                               # long pointed feet
        lg = a[nm]
        an = lg["ankle"]
        spike(m, lg["bone"], (an[0], 1.0, an[2] - 2.4), (0, 0.1, -1), 2.0, 5.0, HIDE, tip=0.5)
    ar = a["arm_right"]                                                                # the trident
    h = ar["hand"]
    STEEL = metal(P, "steel", dark="steel_dark")
    tb = m.bone("trident", ar["bone"], h)
    rod(m, tb, (h[0], h[1] - 14.0, h[2]), (h[0], h[1] + 20.0, h[2]), 1, STEEL, extend=0)
    m.box(tb, h[0] - 2.4, h[1] + 19.6, h[2] - 0.5, h[0] + 2.4, h[1] + 20.6, h[2] + 0.5, STEEL)
    for dx in (-2.0, 0.0, 2.0):
        rod(m, tb, (h[0] + dx, h[1] + 20.0, h[2]), (h[0] + dx, h[1] + 24.0, h[2]), 1, STEEL, extend=0)
        spike(m, tb, (h[0] + dx, h[1] + 24.0, h[2]), (0, 1, 0), 1.2, 1.6, STEEL)
    return m
