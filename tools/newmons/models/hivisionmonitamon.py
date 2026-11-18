"""Hi-Vision Monitamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the flat-screen ninja: a little black-suited ninja whose head is a big black wide-screen monitor on a
tilted stand, a golden satellite dish on top, a red belt with pouches, a pointing finger and a slingshot. 15 blocks.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, local, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little black-suited ninja whose head is a big wide-screen monitor with a golden satellite dish and a red belt"
BASE = {"black": (34, 32, 40), "black_dark": (12, 12, 16), "screen": (180, 186, 196), "screen_dark": (110, 116, 126),
        "gold": (240, 200, 60), "gold_dark": (160, 120, 20), "red": (200, 30, 40), "violet": (90, 60, 150),
        "white": (240, 240, 240)}
SHINY = {"black": (240, 240, 246), "black_dark": (170, 172, 190), "red": (40, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "black", "black_dark")


def screenf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if face == "north" and 1.0 < u < W - 1.0 and 1.0 < v < H - 1.0:
        return tone(p["screen"] if (u + v * 0.6) % 4.0 > 0.6 else p["screen_dark"], face), None
    return metal(P, "black", dark="black_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hivisionmonitamon")
    top = m.bone("hivisionmonitamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 4.0, 3.4, 8.0, 20.0, SUIT, cut=1)
    m.round_box(bd, 0, 0, 4.2, 3.6, 10.0, 12.0, solid(P, "red"), cut=1)
    hd = m.bone("head", bd, (0, 22, 0))
    m.box(hd, -10.0, 20.0, -3.0, 10.0, 34.0, 1.0, screenf, rotation=(0, 0, -10), pivot=(0, 22.0, 0))
    m.round_box(hd, 0, 4.0, 4.0, 3.0, 22.0, 30.0, metal(P, "black", dark="black_dark"), cut=1)
    rod(m, hd, (2.0, 34.0, 0), (4.0, 38.0, 0), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=1)
    m.round_box(hd, 4.0, 0, 3.0, 0.6, 37.0, 43.0, metal(P, "gold", dark="gold_dark"), cut=0)   # satellite dish
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 18.0, 0))
        rod(m, ab, (sx * 4.0, 18.0, 0), (sx * 9.0, 16.0, -3.0), 2, SUIT, extend=0.4)
        m.round_box(ab, sx * 9.6, -3.4, 1.4, 1.4, 14.6, 17.4, solid(P, "red"), cut=0)
    rod(m, "arm_left", (9.6, 16.0, -3.4), (13.0, 17.0, -4.0), 1, solid(P, "red"), extend=0, t2=1)   # pointing finger
    rod(m, "arm_right", (-9.6, 15.0, -3.4), (-12.0, 20.0, -4.0), 1, metal(P, "gold", dark="gold_dark"), extend=0, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 8.0, 0))
        rod(m, lg, (sx * 2.0, 8.0, 0), (sx * 2.6, 1.4, 0), 2, SUIT, extend=0.4)
        m.round_box(lg, sx * 2.6, -0.6, 1.6, 2.2, 0.0, 1.6, solid(P, "white"), cut=0)
    return m
