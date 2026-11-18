"""Goatmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor Digimon of the scroll: a grey goat with a long white beard, a silver helm with a red gem over its face, huge
golden ram horns curling up and back with an unrolled scroll of characters between them, gold and silver bands round
its legs and violet hooves. Adult stage, 15 blocks tall.

Front is -z, y is up. 36 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fabric, fur, gem, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a grey goat with a long white beard, a silver helm with a red gem, huge golden ram horns holding an unrolled "
        "scroll, gold leg bands and violet hooves")
BASE = {"grey": (110, 110, 118), "grey_dark": (60, 60, 66), "white": (240, 240, 236), "white_dark": (180, 180, 176),
        "silver": (214, 218, 228), "silver_dark": (110, 114, 126), "gold": (240, 200, 60), "gold_dark": (160, 120, 20),
        "gem": (220, 30, 50), "gem_light": (255, 150, 160), "hoof": (110, 110, 200), "scroll": (246, 244, 236),
        "ink": (40, 36, 40), "eye": (60, 180, 120)}
SHINY = {"grey": (180, 140, 100), "grey_dark": (120, 80, 50)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "grey", "grey_dark", length=1.0, density=2.0)
GOLD = metal(P, "gold", dark="gold_dark")


def scrollf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 1.6) < 0.8 and (v % 1.4) < 0.7 and 0.5 < v < H - 0.5:
        return tone(p["ink"], face), None
    return tone(p["scroll"], face), None


def build():
    m = Model("goatmon")
    mats = {"skin": FUR, "paw": solid(P, "hoof"), "claw": solid(P, "hoof")}
    a = quadruped(m, mats, "goatmon", length=24.0, body_y=16.0, body_rx=5.0, body_ry=5.4, chest_bulk=1.2,
                  neck=((0, 20, -11), (0, 24, -14)), head_len=7.0, head_w=2.8, head_h=3.4, snout=0.6, mouth_open=2,
                  teeth=0, leg_bulk=1.1, toes=2, tail=((0, 19, 12), (0, 22, 14)), tail_r=(1.2, 0.8))
    hd = a["head"]
    hc = a["head_c"]
    m.round_box(hd, hc[0], hc[2] - 1.0, 3.4, 4.6, hc[1] - 1.0, hc[1] + 3.6, metal(P, "silver", dark="silver_dark"), cut=1)
    m.round_box(hd, hc[0], hc[2] - 5.8, 0.8, 0.3, hc[1] + 1.0, hc[1] + 2.4, gem(P, "gem", "gem_light"), cut=0)
    for j in range(5):                                                                     # long white beard
        spike(m, hd, ((j - 2) * 0.8, hc[1] - 2.0, hc[2] - 3.0), (0, -1, 0.2), 1.2, 8.0, strands(P, "white", "white_dark"),
              tip=0.8)
    for sx in (-1, 1):                                                                     # golden ram horns
        pts = [(sx * 2.4, hc[1] + 3.0, hc[2]), (sx * 4.0, hc[1] + 10.0, hc[2] + 3.0),
               (sx * 4.6, hc[1] + 14.0, hc[2] + 9.0), (sx * 4.4, hc[1] + 10.0, hc[2] + 14.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2, GOLD, extend=0.4, t2=3)
    m.box(hd, -4.0, hc[1] + 4.0, hc[2] + 6.0, 4.0, hc[1] + 13.0, hc[2] + 6.4, scrollf)       # unrolled scroll
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 2.2, 2.2, w[1], w[1] + 2.0,
                    GOLD if "front" in nm else metal(P, "silver", dark="silver_dark"), cut=1)
    return m
