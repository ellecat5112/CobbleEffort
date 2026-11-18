"""Hakubamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
white holy horse: a lean white horse with red tiger-stripe flashes, a golden mane flowing in flame-like curls, a gold
mask with a single horn, a necklace of big red prayer beads, gold cross-hatched leg wraps, black hooves and a long
golden curling tail. Adult stage, 15 blocks tall.

Front is -z, y is up. 38 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 38
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a lean white horse with red stripe flashes, a flowing golden mane, a horned gold mask, a necklace of red prayer "
        "beads and a long golden curling tail")
BASE = {"white": (246, 246, 250), "white_dark": (190, 192, 206), "red": (210, 40, 40), "gold": (250, 210, 90),
        "gold_dark": (200, 150, 40), "bead": (210, 50, 40), "bead_light": (250, 140, 120), "hoof": (30, 28, 32),
        "eye": (40, 40, 44)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "gold": (150, 210, 250), "gold_dark": (80, 150, 220)}


def P(v):
    return pal(BASE, SHINY, v)


COAT0 = skin(P, "white", dark="white_dark")
MANE = strands(P, "gold", "gold_dark")


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs((z * 0.6) % 4.0 - 2.0) < 0.3 and y > 18.0:
        return tone(p["red"], face), None
    return COAT0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hakubamon")
    mats = {"skin": coatf, "paw": solid(P, "hoof"), "claw": solid(P, "hoof"),
            "leg_lower": metal(P, "gold", dark="gold_dark")}
    a = quadruped(m, mats, "hakubamon", length=28.0, body_y=19.0, body_rx=4.4, body_ry=4.6, chest_bulk=1.2,
                  neck=((0, 24, -12), (0, 30, -16)), head_len=9.0, head_w=2.4, head_h=3.0, snout=0.9, mouth_open=2,
                  teeth=0, leg_bulk=0.9, toes=1, tail=((0, 22, 14), (2, 26, 20), (5, 28, 24), (7, 26, 26)),
                  tail_r=(1.4, 1.6, 1.8, 1.4))
    bd, hd = a["body"], a["head"]
    hc = a["head_c"]
    m.round_box(hd, hc[0], hc[2] - 1.0, 2.6, 4.0, hc[1] - 0.4, hc[1] + 2.4, metal(P, "gold", dark="gold_dark"), cut=1)
    spike(m, hd, (0, hc[1] + 2.0, hc[2] - 3.0), (0, 0.8, -1), 1.2, 6.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for j in range(8):                                                                   # flowing golden mane
        t = j / 7
        p0 = (0, 25.0 + t * 7.0, -10.0 - t * 5.0)
        spike(m, bd, p0, (0.6 * (j % 2 - 0.5), 0.5, 1), 1.8, 6.0, MANE, tip=0.9)
    for j in range(10):                                                                  # red prayer beads
        ang = math.pi * (0.1 + 0.8 * j / 9)
        m.round_box(bd, 3.8 * math.cos(ang), -13.0 - 2.0 * math.sin(ang), 1.0, 1.0, 22.0 - 2.6 * math.sin(ang),
                    24.0 - 2.6 * math.sin(ang), metal(P, "bead", dark="red"), cut=0)
    e = a["tail_pts"][-1]
    for j in range(4):
        spike(m, a["tail"], e, (0.3 * (j - 1.5), -0.4, 0.6), 1.6, 5.0, MANE, tip=0.8)
    return m
