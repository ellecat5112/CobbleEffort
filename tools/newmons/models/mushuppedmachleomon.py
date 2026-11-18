"""Mush-Upped Mach Leomon (a Digimon of the CobbleEffort: Digital crossover; after the manga panel on wikimon.net):
Mach Leomon overgrown by spores: the lean lion warrior's body gone a sickly grey-green, its long mane matted and pale,
and fat purple mushroom caps ringed yellow sprouting from its shoulders, head, back and arms. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage (no level on wikimon; Mach Leomon's). Mach Leomon's body
(_leomon.make) with its own colours, mushrooms added.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, solid
from _route import pal, tone
from _variant import clone

_L = clone("_leomon", "mushuppedmachleomon",
           base={"tan": (160, 170, 140), "tan_dark": (90, 100, 76), "mane": (220, 216, 200), "mane_dark": (150, 146, 130),
                 "black": (120, 110, 130), "black_dark": (70, 60, 80)},
           shiny={"tan": (200, 160, 190), "mane": (240, 230, 160)})
HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("Mach Leomon overgrown by spores: a sickly grey-green lion warrior with a matted pale mane and fat purple "
        "mushroom caps ringed yellow sprouting all over it")
_M = {"cap": (130, 70, 170), "cap_dark": (70, 30, 100), "ring": (240, 220, 80), "stem": (240, 236, 210)}


def P(v):
    return pal(_M, {"cap": (220, 80, 60), "cap_dark": (130, 30, 20)}, v)


def capf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up":
        u, v, W, H = local(x, y, z, face, box)
        r = math.hypot(u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5)
        if abs(r - 0.28) < 0.07:
            return tone(p["ring"], face), None
    return tone(p["cap"], face), None


def mushroom(m, bone, c, s, d=(0, 1, 0)):
    tip = (c[0] + d[0] * 2.0 * s, c[1] + d[1] * 2.0 * s, c[2] + d[2] * 2.0 * s)
    rod(m, bone, c, tip, max(1, round(s)), solid(P, "stem"), extend=0.2)
    m.round_box(bone, tip[0], tip[2], 2.2 * s, 2.2 * s, tip[1], tip[1] + 1.4 * s, capf, cut=max(1, round(s * 0.7)))


_body = _L.make("mushuppedmachleomon", x=False)


def build():
    m = _body()
    names = {b["name"] for b in m.bones}
    head = "head" if "head" in names else "body"
    for sx in (-1, 1):
        mushroom(m, "body", (sx * 6.0, 51.0, 0.0), 1.6)                                  # shoulders
        mushroom(m, "body", (sx * 3.0, 44.0, 3.8), 1.2, (sx * 0.5, 0.6, 1))              # back
        mushroom(m, "arm_left" if sx > 0 else "arm_right", (sx * 9.0, 38.0, 0.0), 1.0, (sx, 0.5, 0))
    mushroom(m, head, (1.0, 60.0, 0.0), 1.8)                                             # head
    mushroom(m, head, (-2.0, 59.0, 1.0), 1.0, (-0.6, 1, 0.3))
    mushroom(m, "body", (0, 38.0, -3.6), 0.9, (0, 0.4, -1))
    return m
