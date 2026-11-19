"""Saber Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the ancient sabre-toothed lion: a powerful yellow beast streaked with red flame-stripes, a wild
mane of fiery red-and-yellow spikes, two huge curved steel sabre fangs, long tendril whiskers, a long whip of a tail
and huge black-steel clawed paws. 35 blocks.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a powerful yellow sabre-toothed lion streaked with red flame stripes, a fiery spiked mane, huge steel fangs and black-steel claws"
BASE = {"yellow": (250, 210, 60), "yellow_dark": (200, 140, 20), "red": (220, 60, 30), "steel": (200, 204, 216),
        "steel_dark": (90, 94, 108), "black": (30, 30, 36), "eye": (60, 100, 200), "mouth": (160, 30, 40)}
SHINY = {"yellow": (220, 220, 230), "yellow_dark": (150, 150, 170), "red": (60, 110, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(z * 0.7 + y * 0.4 + abs(x) * 0.3)) > 0.9:
        return tone(p["red"], face), None
    return fur(P, "yellow", "yellow_dark", length=1.4)(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("saberleomon")
    mats = {"skin": furf, "head": furf, "snout": furf, "jaw": furf, "paw": metal(P, "black"), "claw": STEEL,
            "mouth": solid(P, "mouth")}
    a = quadruped(m, mats, "saberleomon", length=32.0, body_y=20.0, body_rx=8.0, body_ry=8.0, chest_bulk=1.25,
                  neck=((0, 28, -18), (0, 30, -22)), head_len=11.0, head_w=5.0, head_h=5.4, mouth_open=14, teeth=4,
                  tail=((0, 22, 16), (0, 26, 24), (4, 30, 30)), tail_r=(1.6, 1.2, 1.0))
    hd = a["head"]
    for sx in (-1, 1):                                                                   # sabre fangs
        spike(m, hd, (sx * 2.0, 27.6, -27.0), (sx * 0.05, -1, -0.15), 1.4, 11.0, STEEL, tip=0.8)
        x0, x1 = sorted((sx * 4.9, sx * 5.2))
        m.box(hd, x0, 32.0, -27.0, x1, 33.0, -25.6, solid(P, "eye"))
        for j in range(2):                                                               # tendril whiskers
            rod(m, hd, (sx * 3.0, 29.0 + j, -28.0), (sx * 12.0, 30.0 + j * 3.0, -26.0), 1, furf, extend=0.2, t2=1)
    for j in range(14):                                                                  # fiery mane
        ang = math.radians(-100 + j * 15)
        spike(m, hd, (5.0 * math.sin(ang), 32.0 + 4.0 * math.cos(ang), -20.0), (math.sin(ang), math.cos(ang) + 0.2, 0.8),
              2.0, 8.0 + (j % 3) * 2.0, strands(P, "red" if j % 2 else "yellow", "yellow_dark"), tip=0.8)
    spike(m, "tail", (4.0, 30.0, 30.0), (0.4, 0.8, 0.4), 1.4, 5.0, strands(P, "red", "yellow_dark"), tip=0.8)
    return m
