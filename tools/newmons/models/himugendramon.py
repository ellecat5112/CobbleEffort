"""Hi Mugendramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the anime still on wikimon.net):
the crimson Mugendramon: a colossal red armoured machine-dragon with a small hooded head, a hulking torso of heavy red
plates, a huge black pincer-claw arm, a massive red cannon-fist, and a long armoured lower body. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a colossal red armoured machine-dragon with a small hooded head, heavy red plates, a black pincer-claw and a cannon-fist"
BASE = {"red": (190, 40, 40), "red_dark": (110, 14, 18), "red_light": (240, 110, 100), "black": (40, 38, 44),
        "black_dark": (14, 14, 18), "steel": (180, 184, 196), "steel_dark": (90, 94, 106), "eye": (250, 200, 40)}
SHINY = {"red": (60, 60, 70), "red_dark": (24, 24, 30), "red_light": (130, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "red", "red_dark", light="red_light", trim="black", trim_w=0.3, rivets=True)
BLACK = riveted(P, "black", "black_dark")


def build():
    m = Model("himugendramon")
    top = m.bone("himugendramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 2.0, 9.0, 12.0, 4.0, 22.0, ARM, cut=3)                           # long armoured lower body
    m.round_box(bd, 0, -2.0, 10.0, 7.0, 22.0, 44.0, ARM, cut=3)                          # hulking torso
    hd = m.bone("head", bd, (0, 46, -4))
    m.round_box(hd, 0, -4.0, 3.4, 3.4, 44.0, 52.0, ARM, cut=1)
    m.box(hd, -2.0, 47.6, -7.5, 2.0, 48.4, -7.3, solid(P, "eye", glow=True))
    al = m.bone("arm_left", bd, (10.0, 40.0, -2.0))                                       # black pincer-claw
    rod(m, al, (10.0, 40.0, -2.0), (16.0, 30.0, -10.0), 5, BLACK, extend=0.6)
    for sy in (-1, 1):
        pts = [(16.0, 30.0, -10.0), (19.0, 30.0 + sy * 5.0, -18.0), (17.0, 30.0 + sy * 2.0, -24.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, al, p0, p1, 3, BLACK, extend=0.4)
    ar = m.bone("arm_right", bd, (-10.0, 40.0, -2.0))                                     # cannon-fist
    rod(m, ar, (-10.0, 40.0, -2.0), (-15.0, 28.0, -8.0), 5, ARM, extend=0.6)
    m.round_box(ar, -15.0, -12.0, 5.0, 5.0, 22.0, 32.0, ARM, cut=2)
    rod(m, ar, (-15.0, 27.0, -16.0), (-15.0, 27.0, -22.0), 3, metal(P, "steel", dark="steel_dark"), extend=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 6.0, 0))
        m.round_box(lg, sx * 7.0, 2.0, 3.4, 5.0, 0.0, 8.0, BLACK, cut=1)
    return m
