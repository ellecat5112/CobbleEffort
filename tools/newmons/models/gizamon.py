"""Gizamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
spiny amphibian: a crouching yellow lizard-fish with a wild mane of red-and-orange fur, blue eyes, a fanged grin, a
row of great black dorsal fin-spikes down its back, and long black claws on its splayed paws. Child stage.

Front is -z, y is up. 22 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a crouching yellow lizard-fish with a wild red mane, blue eyes, a fanged grin, great black fin-spikes and long claws"
BASE = {"yellow": (250, 220, 60), "yellow_dark": (200, 160, 20), "mane": (220, 80, 30), "mane_dark": (150, 30, 14),
        "black": (40, 40, 46), "black_dark": (14, 14, 18), "eye": (60, 120, 220), "white": (250, 250, 250),
        "mouth": (110, 20, 30), "tooth": (250, 250, 240)}
SHINY = {"yellow": (120, 220, 200), "yellow_dark": (40, 150, 130), "mane": (150, 60, 200), "mane_dark": (80, 20, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SK = skin(P, "yellow", dark="yellow_dark")
FIN = metal(P, "black", dark="black_dark")


def build():
    m = Model("gizamon")
    top = m.bone("gizamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 1.0, 5.0, 7.0, 4.0, 13.0, SK, cut=2)
    hd = m.bone("head", bd, (0, 11, -6))
    m.round_box(hd, 0, -9.0, 4.4, 3.6, 6.0, 13.0, SK, cut=2)
    m.box(hd, -3.6, 7.6, -12.8, 3.6, 8.8, -12.5, solid(P, "mouth"))
    for j in range(5):
        spike(m, hd, (-3.0 + j * 1.5, 8.8, -12.6), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
    for sx in (-1, 1):
        m.round_box(hd, sx * 2.0, -12.4, 1.0, 0.3, 10.0, 11.8, solid(P, "white"), cut=0)
        m.box(hd, sx * 2.0 - 0.4, 10.4, -12.9, sx * 2.0 + 0.4, 11.4, -12.7, solid(P, "eye"))
    for i in range(10):                                                                  # wild red mane
        ang = math.radians(-80 + i * 18)
        spike(m, hd, (3.6 * math.sin(ang), 12.4, -6.0 + 2.0 * math.cos(ang)), (math.sin(ang) * 0.8, 0.5, 0.8), 1.6,
              5.0 + (i % 2) * 2.0, strands(P, "mane", "mane_dark"), tip=0.8)
    for j in range(4):                                                                   # black fin-spikes
        spike(m, bd, (0, 13.0, -2.0 + j * 3.4), (0, 1, 0.6), 2.4 - j * 0.3, 7.0 - j, FIN, tip=0.9)
    spike(m, bd, (0, 8.0, 8.0), (0, 0.2, 1), 2.6, 6.0, strands(P, "mane", "mane_dark"), tip=0.8)  # tail fur
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        z = -4.0 if "front" in nm else 4.0
        lg = m.bone(nm, top, (sx * 4.6, 6.0, z))
        rod(m, lg, (sx * 4.6, 7.0, z), (sx * 6.6, 1.4, z - 1.0), 3, SK, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 6.6 + (j - 1) * 1.1, 0.6, z - 2.6), (sx * 0.2, -0.3, -1), 0.9, 4.0, FIN, tip=0.8)
    return m
