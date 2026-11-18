"""Igamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the Iga
ninja: a round red head-body with a pointed hood, big orange eyes and a toothy grin, a long red scarf streaming behind,
a ninjato strapped across its back, a spiked iron ball on its shoulder, mesh-armoured arms with white bandaged cuffs,
red legs and a great four-pointed iron shuriken under its feet. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a round red ninja with a pointed hood, big orange eyes, a long red scarf, a ninjato on its back, a spiked iron "
        "ball, mesh-armoured arms and a great iron shuriken under its feet")
BASE = {"red": (220, 40, 40), "red_dark": (130, 14, 18), "red_light": (250, 130, 110), "orange": (250, 150, 40),
        "pupil": (24, 20, 20), "tooth": (250, 250, 250), "mouth": (80, 20, 24), "mesh": (130, 134, 146),
        "mesh_dark": (60, 62, 72), "white": (246, 244, 236), "white_dark": (180, 176, 160), "steel": (200, 204, 216),
        "steel_dark": (80, 84, 96), "blue": (40, 60, 160), "yellow": (240, 200, 60), "brown": (140, 90, 50)}
SHINY = {"red": (40, 40, 50), "red_dark": (14, 14, 20), "red_light": (120, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark", light="red_light")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.6, y - 27.4)
            if d < 0.7:
                return tone(p["pupil"], face), None
            if d < 1.6:
                return tone(p["orange"], face), None
        if 21.6 < y < 23.4 and abs(x) < 4.6 - (23.4 - y):
            if (x + 6.0) % 1.4 < 0.9:
                return tone(p["tooth"], face), None
            return tone(p["mouth"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def meshf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a = (x + y) % 1.2 < 0.25 or (x - y + z) % 1.2 < 0.25
    return tone(p["mesh_dark"] if a else p["mesh"], face), None


def build():
    m = Model("igamon")
    top = m.bone("igamon", None, (0, 0, 0))
    STEEL = metal(P, "steel", dark="steel_dark")
    for i in range(4):                                                              # great iron shuriken
        ang = math.pi / 2 * i + math.pi / 4
        spike(m, top, (0, 0.6, 0), (math.cos(ang), 0, math.sin(ang)), 3.6, 11.0, STEEL, tip=0.8)
    m.round_box(top, 0, 0, 3.0, 3.0, 0.0, 1.4, STEEL, cut=1)
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0, 3.6, 3.0, 13.0, 19.0, meshf, cut=1)
    hd = m.bone("head", bd, (0, 19, 0))
    ball(m, hd, (0, 25.0, 0), 7.0, headf, layers=6)
    spike(m, hd, (0, 30.0, 0.6), (0, 1, 0.5), 5.0, 6.0, RED, tip=0.8)                      # pointed hood
    sc = m.bone("scarf", hd, (0, 22, 5))
    pts = [(0, 21.0, 5.0), (4.0, 24.0, 10.0), (8.0, 28.0, 13.0), (12.0, 31.0, 14.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, sc, p0, p1, 2, fabric(P, "red", "red_dark"), extend=0.4, t2=1)
    rod(m, bd, (-6.0, 15.0, 6.0), (6.0, 33.0, 6.0), 1, solid(P, "blue"), extend=0, t2=1)      # ninjato
    rod(m, bd, (5.0, 31.6, 6.0), (7.0, 34.6, 6.0), 1, solid(P, "yellow"), extend=0, t2=1)
    ball(m, bd, (6.4, 31.0, 1.0), 2.2, STEEL, layers=3)                                      # spiked iron ball
    for j in range(6):
        ang = 2 * math.pi * j / 6
        spike(m, bd, (6.4 + 2.0 * math.cos(ang), 31.0 + 2.0 * math.sin(ang), 1.0), (math.cos(ang), math.sin(ang), 0),
              0.9, 1.6, STEEL, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 18.0, 0))
        rod(m, ab, (sx * 4.0, 18.0, 0), (sx * 8.0, 13.0, -2.0), 2, meshf, extend=0.4)
        m.round_box(ab, sx * 8.6, -2.4, 1.6, 1.6, 11.6, 14.0, fabric(P, "white", "white_dark", period=1.0), cut=0)
        m.round_box(ab, sx * 9.0, -2.8, 1.8, 1.8, 9.2, 11.8, RED, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 13.0, 0))
        rod(m, lg, (sx * 2.0, 13.4, 0), (sx * 2.6, 6.0, -1.0), 2, RED, extend=0.4)
        rod(m, lg, (sx * 2.6, 6.0, -1.0), (sx * 2.6, 2.0, 0), 2, meshf, extend=0.4)
        m.round_box(lg, sx * 2.6, -0.8, 1.6, 2.4, 1.4, 3.0, RED, cut=0)
    return m
