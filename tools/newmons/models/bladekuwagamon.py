"""Blade Kuwagamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a stag beetle that has become a living blade. A long curved white-and-silver blade body
with a gold edge sweeping down from a pointed head, a single red eye ringed in steel, clawed jointed limbs folded
against the blade and a crackle of pale lightning round it. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, eye, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = ("a stag beetle become a living blade: a long curved white-and-silver blade body with a gold edge, a single red "
        "eye ringed in steel, folded clawed limbs and a crackle of pale lightning")
BASE = {"white": (246, 246, 250), "white_dark": (180, 184, 198), "steel": (200, 204, 216), "steel_dark": (90, 94, 106),
        "gold": (236, 196, 60), "gold_dark": (160, 120, 30), "red": (220, 40, 40), "red_light": (255, 160, 160),
        "spark": (200, 220, 255, 170), "eye": (220, 40, 40), "pupil": (40, 10, 10)}
SHINY = {"white": (60, 60, 74), "white_dark": (26, 26, 34), "gold": (220, 60, 220), "gold_dark": (140, 20, 140),
         "red": (60, 220, 120), "red_light": (190, 255, 210)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", seams=(3.0,))
STEEL = metal(P, "steel", dark="steel_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("bladekuwagamon")
    top = m.bone("bladekuwagamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    pts = []
    for i in range(12):                                          # the curved blade body
        t = i / 11
        pts.append((0, 48.0 - 46.0 * t, -6.0 + 14.0 * math.sin(t * math.pi * 0.8)))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        w = 6.0 - i * 0.4
        rod(m, bd, p0, p1, max(1, round(w)), WHITE, extend=0.6, t2=max(1, round(w * 0.4)))
        rod(m, bd, (p0[0] - w * 0.55, p0[1], p0[2]), (p1[0] - w * 0.55 + 0.4, p1[1], p1[2]), 1, GOLD, extend=0.6)
    hd = m.bone("head", bd, pts[0])
    m.box(hd, -3.0, 44.0, -10.0, 3.0, 50.0, -2.0, WHITE)
    spike(m, hd, (0, 48.0, -10.0), (0, 0.3, -1), 3.0, 5.0, WHITE, tip=1.0)
    m.round_box(hd, -3.0, -6.0, 1.0, 2.0, 45.0, 49.0, STEEL, cut=1)
    m.box(hd, -4.1, 46.0, -7.4, -3.9, 48.0, -4.6, gem(P, "red", "red_light"))
    m.round_box(hd, 3.0, -6.0, 1.0, 2.0, 45.0, 49.0, STEEL, cut=1)
    m.box(hd, 3.9, 46.0, -7.4, 4.1, 48.0, -4.6, gem(P, "red", "red_light"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # folded clawed limbs
        ab = m.bone(nm, bd, (sx * 3.0, 38.0, -2.0))
        rod(m, ab, (sx * 3.0, 38.0, -2.0), (sx * 6.0, 32.0, -6.0), 1, STEEL, extend=0.3)
        rod(m, ab, (sx * 6.0, 32.0, -6.0), (sx * 4.0, 26.0, -8.0), 1, STEEL, extend=0.3)
        spike(m, ab, (sx * 4.0, 26.0, -8.0), (0, -1, -0.4), 1.0, 3.0, STEEL)
    sp = m.bone("cap", bd, (0, 30, 2))
    for j in range(6):                                           # crackle of lightning
        a0 = (math.sin(j * 1.7) * 10.0, 14.0 + j * 6.0, 6.0 + math.cos(j) * 4.0)
        a1 = (a0[0] + 4.0, a0[1] + 4.0, a0[2] - 2.0)
        rod(m, sp, a0, a1, 1, lambda x, y, z, face, variant=None, box=None, **k: (P(variant)["spark"],
                                                                                 P(variant)["spark"][:3]), extend=0)
    return m
