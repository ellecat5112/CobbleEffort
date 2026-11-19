"""Unimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a winged unicorn: a white horse body streaked with grey, a red armoured mask-helm with a gold horn and
crest over its face, ragged grey feathered wings, a flowing gold mane and tail, and steel-shod hooves. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing, quadruped
from _digidetail import armour, feathers, fur, metal, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "a white winged unicorn with a red armoured mask-helm and gold horn, ragged grey wings and a flowing gold mane"
BASE = {"white": (246, 246, 250), "white_dark": (180, 184, 200), "red": (210, 40, 40), "red_dark": (120, 14, 14),
        "gold": (240, 200, 60), "gold_dark": (180, 130, 20), "grey": (150, 150, 160), "grey_dark": (70, 70, 80),
        "steel": (90, 94, 106), "eye": (120, 230, 250)}
SHINY = {"white": (60, 60, 70), "white_dark": (20, 20, 26), "red": (60, 140, 220), "red_dark": (20, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fur(P, "white", "white_dark", length=1.0)
HELM = armour(P, "red", "red_dark", trim="gold")


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 1.8:
        return tone(p["steel"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("unimon")
    mats = {"skin": WHITE, "belly": WHITE, "neck": WHITE, "head": HELM, "leg": legf, "paw": legf,
            "claw": solid(P, "steel"), "tail": WHITE}
    a = quadruped(m, mats, "unimon", length=24.0, body_y=16.0, body_rx=5.4, body_ry=5.6, chest_bulk=1.1,
                  neck=((0, 22, -12), (0, 28, -15)), head_len=10.0, head_w=3.4, head_h=4.4, snout=0.6, mouth_open=0,
                  tail=((0, 18, 12),), tail_r=(1.6,), toes=0, claws=False)
    bd, hd = a["body"], a["head"]
    spike(m, hd, (0, 31.0, -17.0), (0, 0.8, -0.6), 1.6, 7.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 3.5), 29.4, -19.0, max(sx * 1.6, sx * 3.5), 30.2, -17.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.4, 31.0, -13.0), (sx * 0.5, 1, 0.6), 1.2, 4.0, metal(P, "gold"), tip=0.8)
    for j in range(8):                                                                 # gold mane
        spike(m, bd, (0, 30.0 - j * 1.4, -14.0 + j * 1.2), (0, 0.4, 1), 1.4, 6.0, strands(P, "gold", "gold_dark"),
              tip=0.8)
    for j in range(4):                                                                 # gold tail
        spike(m, bd, ((j - 1.5) * 0.6, 18.0, 12.0), ((j - 1.5) * 0.2, -0.6, 1), 1.4, 10.0, strands(P, "gold", "gold_dark"),
              tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 4.0, 21.0, -6.0))
        feather_wing(m, wb, (sx * 4.0, 21.0, -6.0), 18.0, 10.0, 3, feathers(P, "grey", "grey_dark"), side=sx, sweep=45,
                     droop=-10.0)
    return m
