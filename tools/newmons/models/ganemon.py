"""Ganemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
money Digimon: a big gold coin stamped "10" for a body, with orange eyes under bushy brows, a curling black moustache,
a black top hat with a red band, thin black limbs with white gloves, a wad of banknotes in one hand, a black
briefcase in the other and big brown shoes. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a big gold coin stamped 10 with bushy brows and a curling moustache, a black top hat, white gloves, banknotes, "
        "a briefcase and big brown shoes")
BASE = {"gold": (230, 190, 50), "gold_dark": (160, 120, 20), "gold_light": (255, 236, 140), "black": (30, 28, 32),
        "black_dark": (10, 10, 12), "red": (200, 30, 40), "white": (246, 246, 246), "white_dark": (190, 190, 200),
        "brown": (130, 80, 40), "brown_dark": (80, 46, 20), "eye": (240, 140, 40), "note": (200, 210, 190),
        "note_dark": (110, 130, 110)}
SHINY = {"gold": (200, 204, 216), "gold_dark": (120, 124, 136), "gold_light": (250, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
BLACK = solid(P, "black")


def coinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x, y - 22.0)
        if 9.0 < r < 9.8:
            return tone(p["gold_dark"], face), None
        for sx in (-1, 1):                                                 # eyes + bushy brows
            if math.hypot(x - sx * 3.0, y - 23.0) < 1.0:
                return tone(p["eye"], face), None
            if abs(y - 25.2 + 0.25 * sx * (x - sx * 3.0)) < 0.5 and abs(x - sx * 3.0) < 2.0:
                return tone(p["black"], face), None
        if abs(y - 19.2 - 0.2 * abs(x) ** 1.4) < 0.5 and abs(x) < 4.0:   # moustache
            return tone(p["black"], face), None
        if 2.0 < x < 7.0 and 25.0 < y < 30.0 and (abs(x - 3.4) < 0.4 or abs(math.hypot(x - 5.4, y - 27.5) - 1.6) < 0.35):
            return tone(p["gold_dark"], face), None                        # the stamped "10"
    return GOLD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ganemon")
    top = m.bone("ganemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for j, r in enumerate((6.0, 8.4, 9.8, 10.0, 9.8, 8.4, 6.0)):                 # the coin, a disc of slabs
        y0 = 12.0 + j * 2.9
        w = 10.0 * math.sqrt(max(0.0, 1 - ((y0 + 1.45 - 22.0) / 10.0) ** 2))
        m.box(bd, -w, y0, -1.6, w, y0 + 2.9, 1.6, coinf)
    hd = m.bone("head", bd, (0, 32, 0))
    m.round_box(hd, 0, 0, 5.0, 4.4, 31.4, 32.4, BLACK, cut=2)                       # hat brim
    m.round_box(hd, 0, 0, 3.4, 3.0, 32.4, 39.0, BLACK, cut=1)                       # hat crown
    m.round_box(hd, 0, 0, 3.5, 3.1, 33.0, 34.2, solid(P, "red"), cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.6, 22.0, 0))
        rod(m, ab, (sx * 9.6, 22.0, 0), (sx * 14.0, 16.0, -2.0), 1, BLACK, extend=0.2, t2=1)
        m.round_box(ab, sx * 14.4, -2.4, 1.8, 1.8, 13.4, 16.8, skin(P, "white", dark="white_dark"), cut=1)
    m.round_box("arm_left", 15.0, -3.0, 2.4, 0.8, 16.0, 22.0, solid(P, "note"), cut=0)          # banknotes
    m.box("arm_left", 13.0, 18.0, -3.9, 17.0, 19.0, -3.7, solid(P, "note_dark"))
    m.round_box("arm_right", -14.4, -2.4, 4.0, 1.2, 6.0, 12.6, leather(P, "black", "black_dark"), cut=1)   # briefcase
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 12.0, 0))
        rod(m, lg, (sx * 4.0, 12.6, 0), (sx * 4.6, 3.0, 0), 1, BLACK, extend=0.2, t2=1)
        m.round_box(lg, sx * 4.8, -1.8, 2.8, 4.2, 0.0, 3.6, leather(P, "brown", "brown_dark"), cut=1)  # big shoes
    return m
