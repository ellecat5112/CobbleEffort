"""Honeybeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the Armor bee of sincerity: a chunky yellow armoured bee with a big blue-ringed helmet head, a red horn, black joints,
huge clawed yellow fists and feet with white talons and four clear wings. Adult stage, 15 blocks tall.

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a chunky yellow armoured bee with a blue-ringed helmet head, a red horn, huge clawed fists and four clear wings"
BASE = {"yellow": (250, 210, 40), "yellow_dark": (190, 140, 10), "yellow_light": (255, 240, 150), "blue": (60, 100, 200),
        "black": (34, 32, 38), "red": (210, 40, 40), "talon": (240, 240, 240), "eye": (90, 160, 230),
        "wing": (220, 240, 255, 110), "vein": (120, 140, 170, 200)}
SHINY = {"yellow": (90, 200, 120), "yellow_dark": (40, 140, 60), "yellow_light": (170, 250, 190)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "yellow", "yellow_dark", light="yellow_light", trim="black", trim_w=0.3)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west"):
        cy = box.lo[1] + box.size[1] / 2
        for sx in (-1, 1):
            d = math.hypot((x - sx * 2.6) if face == "north" else (z + 2.0), y - cy)
            if (face == "north" or (face == "east") == (sx > 0)) and 1.4 < d < 2.4:
                return tone(p["blue"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 2.6) < 0.25 or abs(v - H * 0.5) < 0.2:
        return p["vein"], None
    return p["wing"], None


def build():
    m = Model("honeybeemon")
    top = m.bone("honeybeemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.6, 6.0, 5.0, 10.0, 24.0, ARM, cut=2)
    m.round_box(bd, 0, 0.6, 6.4, 5.4, 15.0, 16.4, solid(P, "black"), cut=2)
    hd = m.bone("head", bd, (0, 24, -1))
    m.round_box(hd, 0, -1.0, 5.4, 4.6, 23.0, 32.0, headf, cut=2)
    spike(m, hd, (0, 31.6, -2.0), (0, 1, -0.3), 1.6, 4.0, solid(P, "red"), tip=0.8)
    for side in (1, -1):
        for j in range(2):
            x0, x1 = sorted((side * 3.0, side * (16.0 - j * 4.0)))
            m.box(bd, x0, 24.0 - j * 2.0, 5.0 + j, x1, 28.0 - j * 2.0, 5.0 + j, wingf,
                  rotation=(0, side * 20, side * (30 - j * 30)), pivot=(side * 3.0, 26.0 - j * 2.0, 5.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 20.0, 0))
        rod(m, ab, (sx * 6.0, 20.0, 0), (sx * 10.0, 16.0, -3.0), 2, solid(P, "black"), extend=0.4)
        m.round_box(ab, sx * 11.0, -4.0, 3.0, 3.0, 12.0, 18.0, ARM, cut=1)
        for j in range(3):
            spike(m, ab, (sx * 11.0 + (j - 1) * 1.6, 12.0, -6.0), (sx * 0.3, -0.4, -1), 1.0, 3.0, solid(P, "talon"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.4, 10.0, 0))
        rod(m, lg, (sx * 3.4, 10.0, 0), (sx * 4.0, 4.0, 0), 2, solid(P, "black"), extend=0.4)
        m.round_box(lg, sx * 4.0, -1.0, 2.6, 3.4, 0.0, 5.0, ARM, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 4.0 + (j - 1) * 1.4, 1.0, -4.4), (0, -0.2, -1), 0.9, 2.6, solid(P, "talon"), tip=0.8)
    return m
