"""Koemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
jungle monkey: a little green-furred monkey with a round tan face, big round eyes, red cheek stripes and a tiny fang, a
palm-leaf topknot, a leopard-print vest, a shaggy brown loincloth, big bare feet, a wooden club over its shoulder, a
satchel at its hip and a curling tail. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, leather, skin, solid, strands
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little green monkey with a palm-leaf topknot, a leopard-print vest, a shaggy loincloth, big bare feet and a wooden club"
BASE = {"green": (110, 180, 80), "green_dark": (50, 110, 30), "tan": (240, 210, 170), "tan_dark": (190, 150, 110),
        "yellow": (240, 210, 60), "spot": (70, 50, 30), "brown": (130, 90, 50), "brown_dark": (70, 44, 20),
        "eye": (24, 24, 30), "white": (250, 250, 250), "red": (220, 60, 50), "wood": (170, 120, 60),
        "wood_dark": (110, 70, 30), "leaf": (60, 160, 60), "leaf_dark": (20, 90, 20)}
SHINY = {"green": (230, 160, 70), "green_dark": (160, 90, 20)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "green", "green_dark", length=1.0)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.3, y - 20.4)
            if d < 0.6:
                return tone(p["eye"], face), None
            if d < 1.0:
                return tone(p["white"], face), None
            if abs(x - sx * 2.0) < 0.5 and abs(y - 18.8) < 0.15:
                return tone(p["red"], face), None
        if abs(y - 17.8) < 0.15 and abs(x) < 1.0:
            return tone(p["eye"], face), None
    return skin(P, "tan", dark="tan_dark")(x, y, z, face, variant, box=box, **k)


def vestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (int(x * 1.6) * 3 + int(y * 1.6) * 7) % 5 == 0:
        return tone(p["spot"], face), None
    return tone(p["yellow"], face), None


def build():
    m = Model("koemon")
    top = m.bone("koemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 2.8, 2.2, 6.0, 9.0, fur(P, "brown", "brown_dark"), cut=1)
    m.round_box(bd, 0, 0, 2.6, 2.0, 8.6, 14.0, vestf, cut=1)
    hd = m.bone("head", bd, (0, 14, 0))
    m.round_box(hd, 0, 0, 3.4, 3.0, 14.0, 22.4, FUR, cut=1)
    m.round_box(hd, 0, -2.4, 2.6, 0.8, 16.4, 21.6, facef, cut=1)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.8, 0, 0.8, 1.4, 18.0, 20.6, FUR, cut=0)
    for i in range(7):                                                               # palm-leaf topknot
        ang = math.radians(-90 + i * 30)
        spike(m, hd, (0, 22.4, 0), (math.sin(ang), 0.8, math.cos(ang) * 0.6), 1.2, 4.0, strands(P, "leaf", "leaf_dark"),
              tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.8, 13.0, 0))
        rod(m, ab, (sx * 2.8, 13.0, 0), (sx * 4.4, 8.6, -0.6), 1, FUR, extend=0.3, t2=1)
        m.round_box(ab, sx * 4.6, -0.6, 1.2, 1.2, 7.0, 9.0, skin(P, "tan", dark="tan_dark"), cut=0)
    rod(m, "arm_left", (4.6, 8.0, -0.6), (-2.0, 17.0, 3.0), 2, fur(P, "wood", "wood_dark"), extend=0.4)   # club
    m.round_box(bd, -3.0, 1.6, 1.4, 1.4, 6.4, 9.0, leather(P, "brown", "brown_dark"), cut=0)            # satchel
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 6.0, 0))
        rod(m, lg, (sx * 1.6, 6.4, 0), (sx * 1.8, 1.4, 0), 1, FUR, extend=0.3, t2=2)
        m.round_box(lg, sx * 2.0, -1.4, 1.8, 2.6, 0.0, 1.6, skin(P, "tan", dark="tan_dark"), cut=0)
    tb = m.bone("tail", bd, (0, 7, 2))
    pts = [(0, 7.0, 2.2), (2.0, 7.0, 5.0), (4.0, 10.0, 6.0), (3.6, 13.0, 4.6)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=1)
    return m
