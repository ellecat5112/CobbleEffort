"""Ganvivormon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the nurse-cat in a capsule: a yellow cat with a nurse's cap, round glasses, a bell collar and white gloves, riding in a
big red-and-white medicine capsule numbered 63 whose white top half is a toothy, horned lid like an open jaw, with a
heart-shaped lollipop in its paw. 1 block tall.

Front is -z, y is up. 30 units tall (no level on wikimon: sized as a Child).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = ("a yellow nurse-cat with glasses and a bell riding in a big red-and-white medicine capsule whose white top is a "
        "toothy horned lid")
BASE = {"red": (210, 30, 40), "red_dark": (130, 10, 18), "white": (246, 246, 250), "white_dark": (190, 192, 206),
        "yellow": (250, 220, 70), "yellow_dark": (200, 160, 30), "eye": (70, 170, 90), "glass": (40, 40, 44),
        "cross": (60, 90, 220), "bell": (240, 200, 60), "tooth": (250, 250, 246), "inner": (170, 20, 30),
        "pink": (250, 170, 200), "black": (30, 28, 32)}
SHINY = {"red": (40, 90, 210), "red_dark": (14, 40, 130), "yellow": (240, 240, 246), "yellow_dark": (180, 180, 196)}


def P(v):
    return pal(BASE, SHINY, v)


CAT = fur(P, "yellow", "yellow_dark", length=0.6, density=2.0)
WHITE = skin(P, "white", dark="white_dark")


def capsf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 4.0 < y < 8.0 and -3.0 < x < 3.0:
        if abs(x + 1.6) < 0.35 or (abs(x - 1.4) < 1.2 and (abs(y - 4.4) < 0.35 or abs(y - 6.0) < 0.35 or
                                                        abs(y - 7.6) < 0.35) and x > 0.2):
            return tone(p["white"], face), None
    return tone(p["red"] if y > 2.0 or True else p["red_dark"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.4, y - 17.6)
            if 1.0 < d < 1.3:
                return tone(p["glass"], face), None
            if d < 0.7:
                return tone(p["eye"], face), None
    return CAT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ganvivormon")
    top = m.bone("ganvivormon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 5.0, 5.0, 2.0, 12.0, capsf, cut=2)                       # red capsule half
    m.round_box(bd, 0, 0, 5.4, 5.4, 11.0, 12.4, solid(P, "white"), cut=2)
    for j in range(8):
        ang = 2 * math.pi * j / 8
        spike(m, bd, (5.0 * math.cos(ang), 12.4, 5.0 * math.sin(ang)), (0, 1, 0), 1.0, 1.6, solid(P, "tooth"))
    lid = m.bone("lid", bd, (0, 12, 4))                                             # toothy horned lid, flipped open
    m.round_box(lid, 0, 7.0, 5.0, 3.0, 12.0, 22.0, WHITE, cut=2)
    m.box(lid, -4.0, 14.0, 3.8, 4.0, 20.0, 4.0, solid(P, "inner"))
    spike(m, lid, (0, 18.0, 10.0), (0, 0.3, 1), 1.8, 4.0, WHITE, tip=0.8)
    for sx in (-1, 1):
        m.round_box(lid, sx * 2.4, 9.6, 1.0, 0.4, 18.0, 19.6, solid(P, "black"), cut=0)
    hd = m.bone("head", bd, (0, 16, -1))                                            # the nurse cat
    m.round_box(bd, 0, -0.6, 2.6, 2.2, 11.0, 15.0, CAT, cut=1)
    m.round_box(hd, 0, -1.0, 3.4, 3.0, 14.6, 20.4, headf, cut=2)
    m.round_box(hd, 0, -0.6, 2.2, 0.8, 13.8, 15.0, solid(P, "bell"), cut=0)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 20.0, -0.4), (sx * 0.3, 1, 0), 1.6, 2.4, CAT, tip=0.8)
    m.round_box(hd, 0, -0.6, 2.4, 2.2, 20.2, 22.8, solid(P, "white"), cut=1)         # nurse's cap
    m.box(hd, -0.4, 20.8, -2.9, 0.4, 22.2, -2.7, solid(P, "cross"))
    m.box(hd, -0.9, 21.3, -2.9, 0.9, 21.7, -2.7, solid(P, "cross"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.6, 13.0, -1.0))
        rod(m, ab, (sx * 2.6, 13.0, -1.0), (sx * 5.0, 15.0, -3.0), 1, CAT, extend=0.3, t2=1)
        m.round_box(ab, sx * 5.4, -3.4, 1.2, 1.2, 14.6, 16.8, WHITE, cut=0)
    rod(m, "arm_right", (-5.6, 15.0, -3.6), (-6.4, 21.0, -3.6), 1, solid(P, "white"), extend=0, t2=1)  # lollipop
    m.round_box("arm_right", -6.6, -3.6, 2.0, 0.4, 20.6, 24.4, solid(P, "pink"), cut=0)
    return m
