"""Landramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
sand mound: a great heap of golden sand rising into a crested stone skull-head with a single red eye and a dripping
fanged maw, a ridge of red-tipped spikes down its back, stony red-clawed arms reaching out of the sand and a spiked
tail curling up from the dune behind it. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fur, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a great heap of golden sand rising into a crested stone skull-head with one red eye, a fanged maw, red-tipped spikes and stony claws"
BASE = {"sand": (230, 200, 120), "sand_dark": (170, 140, 70), "sand_light": (250, 230, 170), "stone": (120, 110, 100),
        "stone_dark": (60, 54, 48), "stone_light": (180, 170, 156), "red": (210, 50, 40), "mouth": (40, 30, 26),
        "tooth": (240, 236, 220), "eye": (240, 40, 40)}
SHINY = {"sand": (160, 170, 200), "sand_dark": (100, 110, 140), "sand_light": (210, 220, 240)}


def P(v):
    return pal(BASE, SHINY, v)


SAND = fur(P, "sand", "sand_dark", tip="sand_light", length=0.6, density=3.0)
STONE = armour(P, "stone", "stone_dark", light="stone_light")


def build():
    m = Model("landramon")
    top = m.bone("landramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 0, 0))
    for j in range(7):                                                               # sand mound
        r = 14.0 - j * 1.8
        m.round_box(bd, 0, 2.0, r, r * 0.9, j * 4.0, j * 4.0 + 4.6, SAND, cut=max(1, int(r * 0.35)))
    hd = m.bone("head", bd, (0, 28, -2))
    m.round_box(hd, 0, -2.0, 4.6, 4.4, 28.0, 36.0, STONE, cut=2)                       # stone skull
    m.round_box(hd, 0, -6.4, 3.6, 0.6, 27.0, 31.4, solid(P, "mouth"), cut=0)
    m.box(hd, -0.8, 33.0, -6.6, 0.8, 34.4, -6.4, solid(P, "eye", glow=True))
    for j in range(5):
        spike(m, hd, (-2.8 + j * 1.4, 31.4, -6.6), (0, -1, -0.2), 0.8, 1.8, solid(P, "tooth"), tip=0.8)
    for j in range(6):                                                               # red-tipped crest + back spikes
        spike(m, hd if j < 3 else bd, (0, 35.6 - max(0, j - 2) * 4.0, -3.0 + j * 2.6), (0, 1, 0.5), 1.6, 5.0, STONE, tip=0.8)
        spike(m, hd if j < 3 else bd, (0, 35.6 - max(0, j - 2) * 4.0 + 4.6, -3.0 + j * 2.6 + 2.3), (0, 1, 0.5), 0.9, 1.6,
              solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # stony clawed arms
        ab = m.bone(nm, bd, (sx * 9.0, 14.0, -4.0))
        rod(m, ab, (sx * 9.0, 14.0, -4.0), (sx * 15.0, 16.0, -9.0), 2, STONE, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 15.0, 16.0 + (j - 1) * 1.0, -9.0), (sx * 0.6, (j - 1) * 0.3, -1), 1.0, 3.6, solid(P, "red"), tip=0.8)
    tb = m.bone("tail", bd, (0, 4, 12))                                              # spiked tail
    pts = [(0, 4.0, 14.0), (2.0, 10.0, 20.0), (4.0, 16.0, 20.0), (3.0, 20.0, 16.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 2 - j // 2, STONE, extend=0.4)
        spike(m, tb, p1, (0.6, 0.4, 0.4), 0.9, 2.0, STONE, tip=0.8)
    return m
