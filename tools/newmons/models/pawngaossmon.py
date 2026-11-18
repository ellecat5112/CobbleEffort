"""Pawn Gaossmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net): Gaossmon
drafted as a pawn soldier: a stocky violet dinosaur with a huge toothy jaw and red claws, a white underbelly, wearing a
battered gold pawn helmet with a spiked brim and a gold collar. 1 block tall.

Front is -z, y is up. 28 units tall; Child stage (no level on wikimon).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a stocky violet dinosaur with a huge toothy jaw and red claws, wearing a battered gold pawn helmet and collar"
BASE = {"violet": (110, 100, 180), "violet_dark": (50, 40, 110), "white": (236, 236, 244), "red": (190, 40, 40),
        "gold": (200, 160, 70), "gold_dark": (130, 96, 30), "mouth": (180, 40, 60), "tooth": (250, 250, 240),
        "eye": (200, 40, 40), "steel": (180, 184, 196)}
SHINY = {"violet": (90, 160, 120), "violet_dark": (30, 100, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("pawngaossmon")
    mats = {"skin": scales(P, "violet", "violet_dark", size=1.2), "belly": scales(P, "white", "violet_dark"),
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "red"), "talon": solid(P, "red")}
    a = theropod(m, mats, "pawngaossmon", hip_y=8.0, chest=(0, 13.0, -2.0), body_r=4.0, chest_r=4.0,
                 neck_top=(0, 17.0, -4.0), head_len=10.0, head_w=4.0, head_h=4.0, mouth_open=26, teeth=7,
                 arm_len=4.0, leg_bulk=1.2, tail=((0, 8, 5), (0, 6, 10), (0, 4, 14)), tail_r=(2.6, 1.8, 1.0))
    hd = a["head"]
    hc = a["head_c"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
    m.round_box(hd, 0, hc[2] + 1.0, 4.6, 4.6, ey + 1.2, ey + 3.0, armour(P, "gold", "gold_dark"), cut=1)   # pawn helmet
    m.round_box(hd, 0, hc[2] + 1.0, 3.0, 3.0, ey + 3.0, ey + 4.4, armour(P, "gold", "gold_dark"), cut=1)
    spike(m, hd, (0, ey + 2.0, hc[2] - 3.6), (0, 0, -1), 1.4, 4.0, metal(P, "steel"), tip=0.8)
    m.round_box(a["body"], 0, -2.0, 3.6, 3.6, 15.0, 16.4, armour(P, "gold", "gold_dark"), cut=1)
    return m
