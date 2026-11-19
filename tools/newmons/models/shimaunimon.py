"""Shima Unimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a zebra unicorn: a lean white horse striped black, a fiery red-and-orange mane and tail, a grey
armoured head with a long silver-and-red striped horn and a red visor, black hooves, and flames licking its legs.
15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean white zebra unicorn striped black, with a fiery red mane and tail, a grey armoured head and a long striped horn"
BASE = {"white": (246, 246, 250), "white_dark": (190, 190, 200), "black": (30, 30, 34), "red": (220, 60, 30),
        "orange": (250, 150, 40), "grey": (150, 154, 166), "grey_dark": (80, 84, 96), "visor": (220, 40, 40)}
SHINY = {"black": (60, 40, 140), "red": (90, 180, 250), "orange": (180, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def zebraf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(z * 0.9 + y * 0.5 + abs(x) * 0.2)) > 0.75:
        return tone(p["black"], face), None
    return fur(P, "white", "white_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


def hornf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y % 2.0) < 0.8 else p["white"], face), None


def build():
    m = Model("shimaunimon")
    mats = {"skin": zebraf, "head": armour(P, "grey", "grey_dark"), "snout": armour(P, "grey", "grey_dark"),
            "jaw": armour(P, "grey", "grey_dark"), "paw": solid(P, "black"), "claw": solid(P, "black")}
    a = quadruped(m, mats, "shimaunimon", length=26.0, body_y=20.0, body_rx=5.4, body_ry=5.6, neck=((0, 28, -14),
                  (0, 33, -17)), head_len=10.0, head_w=3.4, head_h=4.0, snout=0.5, claws=False,
                  tail=((0, 22, 13), (0, 20, 18), (0, 16, 22)), tail_r=(1.4, 1.2, 1.0))
    hd = a["head"]
    spike(m, hd, (0, 36.0, -19.0), (0, 1, -0.4), 1.4, 10.0, hornf, tip=0.8)                 # striped horn
    m.box(hd, -3.5, 34.0, -21.0, 3.5, 35.0, -19.0, solid(P, "visor", glow=True))
    for j in range(8):                                                                   # fiery mane
        spike(m, a["neck"], (0, 31.0 - j * 1.2, -15.0 + j * 1.6), (0, 0.6, 1), 1.4, 5.0,
              strands(P, "red" if j % 2 else "orange", "red"), tip=0.8)
    for j in range(4):
        spike(m, "tail", (0, 16.0, 22.0), ((j - 1.5) * 0.3, -0.4, 1), 1.4, 6.0, strands(P, "red", "orange"), tip=0.8)
    for sx in (-1, 1):                                                                   # flames at the legs
        for zz in (-9.0, 9.0):
            spike(m, a["body"], (sx * 4.0, 4.0, zz + 1.0), (sx * 0.4, 0.4, 1), 0.9, 3.0, solid(P, "orange", glow=True),
                  tip=0.8)
    return m
