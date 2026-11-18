"""Grottomon (Grottemon on wikimon) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official
art on wikimon.net): the Legendary Warrior of earth's human spirit: a stocky, big-armed goblin with a pale face and a
long pointed nose, a brown hood with a spiked mace swinging from its tip, violet spiked armour on its shoulders and
knees, huge tan fists marked with a symbol, and spiked violet boots. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a stocky big-armed goblin with a pale face and long nose, a brown hood with a spiked mace on its tip, violet "
        "spiked armour and huge tan fists")
BASE = {"tan": (230, 200, 140), "tan_dark": (180, 140, 80), "face": (210, 220, 180), "face_dark": (150, 160, 120),
        "hood": (150, 100, 60), "hood_dark": (90, 56, 24), "violet": (150, 130, 200), "violet_dark": (80, 60, 130),
        "violet_light": (210, 200, 240), "red": (200, 50, 40), "eye": (60, 120, 50), "steel": (140, 120, 190)}
SHINY = {"violet": (200, 160, 60), "violet_dark": (130, 90, 20), "violet_light": (250, 220, 140), "hood": (60, 80, 140)}


def P(v):
    return pal(BASE, SHINY, v)


TAN = skin(P, "tan", dark="tan_dark")
VIO = armour(P, "violet", "violet_dark", light="violet_light")


def fistf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(abs(x) - 11.0) < 0.3 and 14.0 < y < 20.0:
        return tone(p["red"], face), None
    return TAN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("grottomon")
    top = m.bone("grottomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0.6, 7.0, 5.6, 14.0, 30.0, fabric(P, "hood", "hood_dark"), cut=2)
    hd = m.bone("head", bd, (0, 30, -1))
    m.round_box(hd, 0, -1.0, 4.4, 4.0, 28.0, 36.0, fabric(P, "hood", "hood_dark"), cut=2)    # hood
    m.round_box(hd, 0, -4.6, 3.0, 1.0, 29.0, 34.0, skin(P, "face", dark="face_dark"), cut=1)
    spike(m, hd, (0, 31.0, -5.6), (0, -0.4, -1), 1.4, 4.0, skin(P, "face", dark="face_dark"), tip=0.8)   # long nose
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 32.6, -5.7, max(sx * 0.8, sx * 2.0), 33.4, -5.5, solid(P, "eye"))
    pts = [(0, 36.0, 0), (4.0, 38.0, 4.0), (9.0, 34.0, 7.0), (12.0, 30.0, 6.0)]            # hood tip + mace
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, max(1, 3 - j), fabric(P, "hood", "hood_dark"), extend=0.4)
    m.round_box(hd, 12.0, 6.0, 1.6, 1.6, 28.4, 31.6, VIO, cut=1)
    for ang in range(0, 360, 72):
        r_ = math.radians(ang)
        spike(m, hd, (12.0 + 1.6 * math.cos(r_), 30.0 + 1.6 * math.sin(r_), 6.0), (math.cos(r_), math.sin(r_), 0), 0.8,
              1.6, VIO)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        spike(m, bd, (sx * 7.0, 29.0, 0), (sx * 0.6, 1, 0), 3.0, 6.0, VIO, tip=1.0)            # spiked shoulders
        ab = m.bone(nm, bd, (sx * 7.0, 27.0, 0))
        rod(m, ab, (sx * 7.0, 27.0, 0), (sx * 11.0, 20.0, -3.0), 4, TAN, extend=0.6)
        m.round_box(ab, sx * 11.0, -4.0, 4.0, 4.0, 12.0, 20.0, fistf, cut=2)                    # huge fists
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 14.0, 0))
        rod(m, lg, (sx * 4.0, 14.0, 0), (sx * 5.0, 6.0, 0), 3, TAN, extend=0.4)
        m.round_box(lg, sx * 5.0, -1.0, 3.4, 4.4, 0.0, 6.0, VIO, cut=1)                       # spiked boots
        spike(m, lg, (sx * 5.0, 6.0, -3.0), (0, 0.4, -1), 2.0, 3.0, VIO, tip=0.8)
    return m
