"""Entmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the rotting tree dragon. A hunched four-legged dragon of gnarled golden-brown wood, its limbs bound with
green vines, a long jagged maw of splinter teeth, two great ragged wings of dead branches heavy with crimson leaves,
root-like claws and a long twisting tail of wood ending in a snapping serpent head. 25 blocks tall.

Front is -z, y is up. 38 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, solid, twisted
from _route import pal, tone

HEIGHT = 38
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hunched four-legged dragon of gnarled golden-brown wood bound with green vines, a jagged splinter-toothed maw, "
        "dead-branch wings heavy with crimson leaves and a serpent-headed tail")
BASE = {"wood": (180, 140, 70), "wood_dark": (100, 70, 30), "wood_light": (230, 200, 130), "vine": (40, 90, 50),
        "vine_dark": (14, 40, 20), "leaf": (170, 30, 40), "leaf_dark": (90, 10, 20), "leaf_tip": (40, 20, 20),
        "mouth": (60, 20, 20), "tooth": (230, 220, 190), "eye": (250, 220, 60)}
SHINY = {"wood": (170, 170, 180), "wood_dark": (90, 90, 100), "leaf": (240, 160, 40), "leaf_dark": (160, 90, 10)}


def P(v):
    return pal(BASE, SHINY, v)


WOOD = twisted(P, "wood", "wood_dark", light="wood_light", period=2.6, angle=0.5)
LEAVES = fur(P, "leaf", "leaf_dark", tip="leaf_tip", length=1.6, density=1.4)


def vinef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and (y + abs(x) * 0.3) % 3.4 < 0.6:
        return tone(p["vine"], face), None
    return WOOD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("entmon")
    mats = {"skin": WOOD, "belly": WOOD, "neck": vinef, "head": WOOD, "snout": WOOD, "jaw": WOOD,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": vinef, "leg_lower": vinef, "paw": WOOD,
            "claw": WOOD, "tail": vinef}
    a = quadruped(m, mats, "entmon", length=32.0, body_y=16.0, body_rx=7.0, body_ry=6.6, chest_bulk=1.3,
                  neck=((0, 18, -16), (0, 18, -22)), head_len=12.0, head_w=4.0, head_h=4.0, snout=0.9, mouth_open=24,
                  teeth=7, leg_bulk=1.6, toes=4,
                  tail=((0, 16, 17), (4, 10, 22), (10, 6, 22), (14, 6, 16), (12, 8, 10)),
                  tail_r=(2.6, 2.0, 1.6, 1.4, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
        for j in range(4):                                                         # branch spikes on the head
            spike(m, hd, (sx * 2.0, ey + 1.0, ez + 2.0 + j * 1.6), (sx * 0.8, 0.6, 0.6), 1.0, 4.0 - j * 0.6, WOOD, tip=0.25)
    e = a["tail_pts"][-1]                                                           # snapping serpent head tail
    m.round_box(a["tail"], e[0], e[2] - 2.0, 1.8, 3.0, e[1] - 1.4, e[1] + 1.4, WOOD, cut=1)
    m.box(a["tail"], e[0] - 1.4, e[1] - 1.8, e[2] - 5.0, e[0] + 1.4, e[1] - 1.2, e[2] - 1.0, solid(P, "mouth"))
    for side in (1, -1):                                                            # dead-branch wings with crimson leaves
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 22.0, -2.0))
        for j in range(4):
            ang = math.radians(25 + j * 18)
            tip = (side * (4.0 + 20.0 * math.cos(ang)), 22.0 + 18.0 * math.sin(ang), 2.0 + j * 3.0)
            mid = ((side * 4.0 + tip[0]) / 2, (22.0 + tip[1]) / 2 + 2.0, (tip[2]) / 2)
            rod(m, wb, (side * 4.0, 22.0, -2.0), mid, 2, WOOD, extend=0.5)
            rod(m, wb, mid, tip, 1, WOOD, extend=0.5)
            m.round_box(wb, tip[0] * 0.9, tip[2], 3.6, 2.4, tip[1] - 5.0, tip[1], LEAVES, cut=1)
    return m
