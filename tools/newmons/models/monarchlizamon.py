"""Monarch Lizamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a cyborg lizard king: a crouching lizard of green scales half armoured in black and
gunmetal plates with red-lit seams, a dark armoured head with a great yellow crescent horn and a violet mane, twin jet
boosters on its back blazing yellow, a gun-blade arm, green claws tipped violet and a spined green tail. 25 blocks
long.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, theropod
from _digidetail import armour, local, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crouching green lizard half armoured in black plates with red-lit seams, a yellow crescent horn, a violet "
        "mane, twin jet boosters, a gun-blade arm and a spined green tail")
BASE = {"green": (60, 180, 60), "green_dark": (20, 100, 24), "black": (50, 50, 60), "black_dark": (16, 16, 22),
        "red": (230, 40, 40), "yellow": (250, 220, 60), "violet": (190, 60, 200), "violet_dark": (100, 20, 120),
        "steel": (190, 196, 210), "steel_dark": (90, 96, 110), "eye": (240, 40, 40), "mouth": (150, 30, 40),
        "tooth": (250, 250, 240), "jet": (255, 240, 120, 200), "jet_core": (255, 255, 230, 235)}
SHINY = {"green": (60, 120, 200), "green_dark": (20, 60, 130), "violet": (240, 160, 40), "violet_dark": (170, 90, 10)}


def P(v):
    return pal(BASE, SHINY, v)


ARM0 = armour(P, "black", "black_dark", trim="steel_dark", trim_w=0.2)
SCALE_ = scales(P, "green", "green_dark", size=1.4)


def armf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(((y * 0.6 + z * 0.3) % 3.0) - 1.5) < 0.1:
        return p["red"], p["red"]
    return ARM0(x, y, z, face, variant, box=box, **k)


def jetf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["jet_core"] if 0.35 < u / max(W, 1e-6) < 0.65 else p["jet"]
    return c, c[:3]


def build():
    m = Model("monarchlizamon")
    mats = {"skin": armf, "belly": SCALE_, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
            "claw": solid(P, "violet"), "talon": solid(P, "violet"), "leg": SCALE_, "tail": SCALE_}
    a = theropod(m, mats, "monarchlizamon", hip_y=16.0, chest=(0, 24.0, -6.0), body_r=6.0, chest_r=6.0,
                 neck_top=(0, 28.0, -12.0), head_len=11.0, head_w=4.0, head_h=4.0, mouth_open=20, teeth=6,
                 arm_len=10.0, arm_bulk=1.2, leg_bulk=1.3,
                 tail=((0, 16, 8), (0, 15, 16), (0, 14, 24), (0, 14, 32)), tail_r=(3.6, 2.8, 2.0, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
              ez + 0.6, solid(P, "eye", glow=True))
    hc = a["head_c"]
    pts = [(0, ey + 2.0, hc[2] - 2.0), (-3.0, ey + 7.0, hc[2] - 4.0), (-4.0, ey + 12.0, hc[2] - 2.0),
           (-3.0, ey + 15.0, hc[2] + 1.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                     # yellow crescent horn
        rod(m, hd, p0, p1, max(1, 3 - j), solid(P, "yellow"), extend=0.3)
    for i in range(8):                                                                   # violet mane
        spike(m, hd, ((i - 3.5) * 0.7, ey + 2.6, hc[2] + 2.0), ((i - 3.5) * 0.3, 0.8, 0.8), 1.4, 6.0,
              strands(P, "violet", "violet_dark"), tip=0.8)
    for sx in (-1, 1):                                                                   # twin jet boosters
        root = (sx * 4.0, 26.0, 0.0)
        tip = (sx * 6.0, 32.0, 10.0)
        rod(m, bd, root, tip, 4, metal(P, "black", dark="black_dark"), extend=0.4)
        for ang in (0, 90):
            m.box(bd, tip[0] - 1.6, tip[1] - 1.6, tip[2], tip[0] + 1.6, tip[1] + 1.6, tip[2] + 8.0, jetf,
                  rotation=(0, 0, ang), pivot=tip)
    for j in range(6):                                                                   # tail spines
        spike(m, a["tail"], a["tail_pts"][min(j // 2, len(a["tail_pts"]) - 1)], (0, 1, 0.4), 1.2, 3.0,
              solid(P, "violet"), tip=0.8)
    ar = a["arm_right"]                                                                  # gun-blade arm
    h = ar["hand"]
    rod(m, ar["bone"], h, (h[0] - 1.0, h[1] - 1.0, h[2] - 8.0), 3, metal(P, "steel", dark="steel_dark"), extend=0.4)
    m.box(ar["bone"], h[0] - 1.4, h[1] - 3.6, h[2] - 10.0, h[0] - 0.8, h[1] - 0.6, h[2] - 2.0, metal(P, "steel"))
    return m
