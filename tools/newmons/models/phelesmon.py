"""Phelesmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the devil of temptation: a lean red-skinned devil in a black hooded cowl with swept horn-points,
a black-and-red armoured suit with a fang emblem, red bat wings, a long pointed red tail, curled black boots, clawed
hands, and a long red trident. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean red devil in a black hooded cowl and black-and-red suit, red bat wings, a long pointed tail and a long red trident"
BASE = {"red": (210, 40, 40), "red_dark": (120, 14, 14), "black": (36, 34, 40), "black_dark": (12, 12, 16),
        "gold": (230, 190, 70), "eye": (250, 220, 60), "steel": (200, 204, 216)}
SHINY = {"red": (60, 90, 200), "red_dark": (20, 34, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = armour(P, "black", "black_dark", trim="red", trim_w=0.3)
SKIN = skin(P, "red", dark="red_dark")


def build():
    m = Model("phelesmon")
    mats = {"skin": SUIT, "chest": armour(P, "red", "black", trim="gold", trim_w=0.25), "hand": SKIN, "finger": SKIN,
            "claw": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, claws=True, name="phelesmon")
    bd = a["body"]
    for nm in ("leg_left", "leg_right"):                                                 # curled boots
        ank = a[nm]["ankle"]
        rod(m, a[nm]["bone"], (ank[0], 1.0, ank[2] - 3.0), (ank[0], 3.0, ank[2] - 7.0), 2, SUIT, extend=0.3)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.4, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.2, -2.9, max(sx * 0.6, sx * 1.6), 57.8, -2.8, solid(P, "eye", glow=True))
    m.round_box(hd, 0, 1.4, 3.4, 2.6, 58.0, 61.2, SUIT, cut=1)                             # hooded cowl
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.6, sx * 3.6))
        m.box(hd, x0, 52.0, -2.0, x1, 60.0, 3.0, SUIT)
        spike(m, hd, (sx * 3.0, 60.6, 1.0), (sx * 0.6, 1, 0.6), 1.4, 7.0, SUIT, tip=0.8)
    wb = m.bone("wings", bd, (0, 48, 3))
    for side in (1, -1):
        bat_wing(m, wb, (side * 3.0, 48.0, 3.0), 18.0, 14.0, 3, solid(P, "black"), skin(P, "red", dark="red_dark"),
                 side=side, sweep=15)
    tb = m.bone("tail", bd, (0, 31, 3))
    pts = [(0, 31.0, 3.0), (4.0, 22.0, 8.0), (9.0, 18.0, 6.0), (12.0, 20.0, 3.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, SKIN, extend=0.2)
    spike(m, tb, pts[-1], (0.6, 0.6, -0.4), 1.4, 2.6, SKIN, tip=0.8)
    ar = a["arm_right"]                                                                  # long red trident
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 26.0, h[2]), (h[0], h[1] + 20.0, h[2]), 1, metal(P, "red", dark="red_dark"),
        extend=0.2)
    for sx in (-1, 0, 1):
        spike(m, ar["bone"], (h[0] + sx * 1.6, h[1] + 20.0, h[2]), (sx * 0.15, 1, 0), 1.0, 4.0 - abs(sx),
              metal(P, "red", dark="red_dark"), tip=0.8)
    m.box(ar["bone"], h[0] - 2.0, h[1] + 19.4, h[2] - 0.4, h[0] + 2.0, h[1] + 20.4, h[2] + 0.4, metal(P, "red"))
    return m
