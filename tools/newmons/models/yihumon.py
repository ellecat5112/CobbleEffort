"""Yihumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the winged tiger of legend: a powerful golden tiger beast-man striped black, crouched under a heavy
green fur-trimmed cloak, great feathered wings, a ring of twisted black thorns rising over its head like a halo,
bandaged legs with red claws, and a long striped tail. 35 blocks.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import fabric, feathers, fur, solid
from _route import pal, tone

HEIGHT = 73
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a golden black-striped tiger beast-man under a green fur-trimmed cloak with great feathered wings and a ring of black thorns"
BASE = {"gold": (230, 180, 70), "gold_dark": (160, 110, 30), "black": (30, 28, 30), "green": (60, 110, 90),
        "green_dark": (24, 60, 44), "white": (240, 236, 226), "white_dark": (190, 180, 160), "red": (200, 40, 40),
        "wing": (190, 160, 130), "wing_dark": (110, 80, 60), "trouser": (110, 80, 120), "trouser_dark": (60, 40, 70),
        "eye": (250, 220, 60)}
SHINY = {"gold": (230, 230, 240), "gold_dark": (160, 160, 180), "green": (120, 40, 60), "green_dark": (60, 14, 24)}


def P(v):
    return pal(BASE, SHINY, v)


def tigerf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and (y * 0.7 + math.sin(x * 0.8) * 1.2) % 3.6 < 0.7:
        return tone(p["black"], face), None
    return fur(P, "gold", "gold_dark", length=1.2)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yihumon")
    TR = fabric(P, "trouser", "trouser_dark")
    mats = {"skin": tigerf, "chest": tigerf, "abs": tigerf, "pelvis": TR, "deltoid": tigerf, "upper_arm": tigerf,
            "forearm": tigerf, "hand": tigerf, "finger": tigerf, "claw": solid(P, "red"), "thigh": TR, "knee": TR,
            "shin": fabric(P, "white", "white_dark", axis="x", period=1.2), "calf": fabric(P, "white", "white_dark"),
            "foot": tigerf, "talon": solid(P, "red"), "neck": tigerf}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.4, leg_bulk=1.3, claws=True, talons=True, name="yihumon")
    bd = a["body"]
    for i in range(10):                                                                 # heavy green cloak
        ang = (i - 4.5) * 0.32
        m.box(bd, 7.0 * math.sin(ang) - 2.0, 28.0, 4.0 * math.cos(ang) + 1.0, 7.0 * math.sin(ang) + 2.0, 50.0,
              4.0 * math.cos(ang) + 2.0, fabric(P, "green", "green_dark"), rotation=(0, math.degrees(ang), 0),
              pivot=(7.0 * math.sin(ang), 40.0, 4.0 * math.cos(ang) + 1.5))
    m.round_box(bd, 0, 1.0, 8.0, 6.0, 48.0, 52.4, fur(P, "white", "white_dark", length=1.6), cut=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.6, 4.0, 54.0, 61.0, tigerf, cut=1)
    m.round_box(hd, 0, -5.0, 2.4, 1.6, 54.4, 57.6, fur(P, "white", "white_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.6), 58.4, -4.6, max(sx * 0.8, sx * 2.6), 59.2, -4.2, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.8, 60.4, 0), (sx * 0.4, 1, 0), 1.6, 3.0, tigerf, tip=0.8)
    for i in range(16):                                                                 # ring of black thorns
        ang = i * 2 * math.pi / 16
        cx, cy = 10.0 * math.cos(ang), 64.0 + 8.0 * math.sin(ang)
        m.box(hd, cx - 0.8, cy - 0.8, 3.0, cx + 0.8, cy + 0.8, 3.8, solid(P, "black"))
        spike(m, hd, (cx, cy, 3.4), (math.cos(ang), math.sin(ang), 0), 0.8, 1.6, solid(P, "black"), tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 48.0, 4.0))
        feather_wing(m, wb, (sx * 3.0, 48.0, 4.0), 24.0, 14.0, 3, feathers(P, "wing", "wing_dark"), side=sx, sweep=70,
                     droop=-4.0)
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (6.0, 22.0, 10.0), (12.0, 18.0, 12.0), (16.0, 22.0, 12.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, tigerf, extend=0.4)
    return m
