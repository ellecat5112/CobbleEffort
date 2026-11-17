"""Balli Bastemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a stout war-beast in tribal regalia. A barrel body with a leopard-spotted belly, a red-and-blue armoured
bib with a gold border and a red emblem, a crest of red hair under a tall blue blade-helm, big round ears, gold rings
on its arms and legs, red-clawed feet and a tail hung with gold rings. 15 blocks tall.

Front is -z, y is up. 40 units tall; no level known (Adult used).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fur, local, metal, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a stout war-beast: a leopard-spotted belly, a red-and-blue armoured bib with a gold border, red hair under a "
        "tall blue blade-helm, big ears, gold rings on its limbs and tail and red-clawed feet")
BASE = {"hide": (140, 110, 100), "hide_dark": (90, 66, 60), "spot": (240, 210, 140), "spot_ring": (90, 60, 30),
        "red": (190, 40, 40), "red_dark": (110, 14, 20), "blue": (60, 70, 170), "blue_dark": (24, 30, 90),
        "gold": (230, 186, 60), "gold_dark": (150, 110, 30), "hair": (170, 50, 40), "hair_dark": (100, 20, 20),
        "violet": (170, 130, 210), "claw": (200, 40, 50), "eye": (60, 90, 200), "pupil": (16, 16, 30)}
SHINY = {"hide": (120, 120, 150), "hide_dark": (70, 70, 100), "red": (40, 140, 90), "red_dark": (16, 80, 50),
         "hair": (60, 160, 110), "hair_dark": (20, 90, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "hide", dark="hide_dark", var=0.05)
GOLD = metal(P, "gold", dark="gold_dark")


def leopard(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    cu, cv = round(a / 3.0) * 3.0 + (1.5 if round(b / 3.0) % 2 else 0), round(b / 3.0) * 3.0
    d = math.hypot((a - cu) / 1.3, b - cv)
    if 0.75 < d < 1.15:
        return tone(p["spot_ring"], face), None
    return tone(p["spot"], face), None


def bibf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if min(u, W - u, v, H - v) < 0.6:
        return tone(p["gold"], face), None
    if face == "north" and abs(u - W / 2) < 1.4 and abs(v - H * 0.55) < 1.6:
        return tone(p["red"], face), None
    return armour(P, "blue" if abs(u - W / 2) < W * 0.3 else "red", "blue_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ballibastemon")
    top = m.bone("ballibastemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 16.0, 0), 9.0, HIDE, layers=6, ry=8.0)
    m.box(bd, -6.4, 8.0, -9.4, 6.4, 18.0, -7.6, leopard)                                 # spotted belly
    m.box(bd, -6.0, 18.0, -9.8, 6.0, 27.0, -7.6, bibf)                                   # armoured bib
    m.box(bd, -7.6, 16.4, -9.0, 7.6, 18.0, 6.0, GOLD)                                    # gold belt
    hd = m.bone("head", bd, (0, 26, -1))
    m.round_box(hd, 0, -1.0, 4.0, 3.6, 25.0, 32.0, HIDE, cut=1)
    m.box(hd, -2.8, 26.0, -5.2, 2.8, 28.6, -3.8, solid(P, "violet"))                     # mouth plate
    for sx in (-1, 1):
        m.box(hd, sx * 1.6 - 0.6, 29.0, -4.7, sx * 1.6 + 0.6, 30.0, -4.4, solid(P, "eye"))
        m.box(hd, min(sx * 3.6, sx * 8.0), 27.0, -0.4, max(sx * 3.6, sx * 8.0), 33.0, -0.4, HIDE,
              rotation=(0, sx * 20, sx * 10), pivot=(sx * 3.6, 30.0, -0.4))              # big ears
    for i in range(7):                                           # red hair crest
        rod(m, hd, (-1.8 + i * 0.6, 32.0, -1.0), (-2.4 + i * 0.8, 35.0, 1.6), 1, strands(P, "hair", "hair_dark"),
            extend=0.2)
    m.box(hd, -0.6, 32.0, -3.0, 0.6, 40.0, 1.0, armour(P, "blue", "blue_dark"))           # tall blade-helm
    m.box(hd, -0.6, 38.0, -3.0, 0.6, 40.0, -6.0 + 3.0, armour(P, "blue", "blue_dark"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.0, 20.0, 0))
        hand = (sx * 11.0, 10.0, -2.0)
        rod(m, ab, (sx * 8.0, 20.0, 0), hand, 4, HIDE, extend=0.5)
        for j in range(3):
            p = (sx * (8.6 + j), 18.0 - j * 3.0, -0.6 - j * 0.4)
            rod(m, ab, p, (p[0], p[1] - 0.8, p[2]), 5, GOLD, extend=0)
        for f in range(3):
            spike(m, ab, hand, (sx * 0.2 + (f - 1) * 0.3, -1, -0.4), 1.0, 2.4, solid(P, "claw"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 8.0, 0))
        m.round_box(lg, sx * 4.4, 0, 3.0, 3.0, 2.0, 9.0, HIDE, cut=1)
        m.round_box(lg, sx * 4.4, 0, 3.3, 3.3, 4.0, 5.4, GOLD, cut=1)
        m.box(lg, sx * 4.4 - 3.4, 0.0, -4.4, sx * 4.4 + 3.4, 2.2, 2.4, armour(P, "blue", "blue_dark"))
        for f in range(3):
            spike(m, lg, (sx * 4.4 + (f - 1) * 2.0, 1.0, -4.4), (0, -0.2, -1), 1.2, 2.4, solid(P, "claw"))
    tl = m.bone("tail", bd, (0, 12, 7))
    rod(m, tl, (0, 12.0, 7.0), (6.0, 18.0, 13.0), 2, HIDE, extend=0.4)
    for j in range(3):
        p = (2.0 + j * 1.6, 14.0 + j * 1.6, 9.0 + j * 1.6)
        ball(m, tl, p, 1.4, GOLD, layers=2)
    return m
