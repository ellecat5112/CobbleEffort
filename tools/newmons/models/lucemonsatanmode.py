"""Lucemon: Satan Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Lucemon as the demon king: a hulking violet dragon-demon crouched over a huge black
swirling orb, a golden horned skull-mask face with a fanged grin, gold claws, spiny violet wings and armour plates,
a long spiked tail and a ring of coloured magic circles above it. 35 blocks tall.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing, theropod
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a hulking violet dragon-demon crouched over a huge black orb, a golden horned skull-mask, gold claws, spiny wings and magic circles"
BASE = {"violet": (90, 60, 130), "violet_dark": (36, 20, 60), "violet_light": (160, 130, 200), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "black": (30, 30, 36), "black_light": (120, 120, 140), "red": (230, 50, 50),
        "blue": (60, 140, 240), "green": (60, 220, 120), "orange": (250, 150, 40), "tooth": (250, 248, 236),
        "eye": (250, 220, 60), "mouth": (140, 30, 40)}
SHINY = {"violet": (150, 40, 50), "violet_dark": (70, 14, 20), "violet_light": (230, 120, 120)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "violet", "violet_dark", size=1.4, light="violet_light")
GOLD = metal(P, "gold", dark="gold_dark")


def orbf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    ang = math.atan2(y - 10.0, x)
    if (ang * 2.0 + math.hypot(x, y - 10.0) * 0.6) % 1.6 < 0.4:
        return tone(p["black_light"], face), None
    return tone(p["black"], face), None


def build():
    m = Model("lucemonsatanmode")
    mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": GOLD, "snout": GOLD, "jaw": GOLD, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": GOLD, "thigh": HIDE, "shin": HIDE, "foot": HIDE,
            "talon": GOLD, "tail": HIDE, "tail_tip": HIDE}
    a = theropod(m, mats, "lucemonsatanmode", hip_y=18.0, chest=(0, 30.0, -4.0), body_r=6.0, chest_r=6.6,
                 neck_top=(0, 36.0, -9.0), head_len=8.0, head_w=3.6, head_h=4.0, mouth_open=18, teeth=6, arm_len=12.0,
                 arm_bulk=1.4, leg_bulk=1.3, stance=5.0,
                 tail=((0, 16, 8), (4, 12, 15), (8, 10, 22), (10, 12, 29)), tail_r=(3.0, 2.2, 1.6, 1.0))
    bd, hd = a["body"], a["head"]
    st = a["skull_top"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
              solid(P, "eye", glow=True))
        pts = [(sx * 2.4, st - 0.4, -8.0), (sx * 5.0, st + 4.0, -7.0), (sx * 4.0, st + 8.0, -4.0)]   # golden horns
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, GOLD, extend=0.3, t2=2)
    ob = m.bone("orb", bd, (0, 10, -10))                                             # huge black orb
    ball(m, ob, (0, 10.0, -12.0), 7.0, orbf, layers=5)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 33.0, 2.0))
        bat_wing(m, wb, (side * 4.0, 33.0, 2.0), 22.0, 16.0, 4, HIDE, scales(P, "violet_dark", "black"), side=side, sweep=25)
    for i in range(8):
        spike(m, bd, (0, 32.0 - i * 1.4, -2.0 + i * 2.0), (0, 1, 0.5), 1.2, 3.0, GOLD, tip=0.8)
    for p in a["tail_pts"][1:]:
        spike(m, a["tail"], p, (0, 1, 0.3), 1.0, 2.6, GOLD, tip=0.8)
    rb = m.bone("ring_circles", bd, (0, 50, 0))                                       # coloured magic circles
    for k_, key in enumerate(("red", "blue", "green", "orange", "gold")):
        ang = 2 * math.pi * k_ / 5
        c = (12.0 * math.cos(ang), 48.0 + 2.0 * math.sin(ang * 2), 12.0 * math.sin(ang))
        for i in range(8):
            a0, a1 = 2 * math.pi * i / 8, 2 * math.pi * (i + 1) / 8
            rod(m, rb, (c[0] + 2.6 * math.cos(a0), c[1], c[2] + 2.6 * math.sin(a0)),
                (c[0] + 2.6 * math.cos(a1), c[1], c[2] + 2.6 * math.sin(a1)), 1, solid(P, key, glow=True), extend=0.1, t2=1)
    return m
