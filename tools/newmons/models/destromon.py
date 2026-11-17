"""Destromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the destroyer machine. A hulking four-legged war dragon in red armour with gold trim and purple
joints, a small horned purple head under a red crest, a battery of long steel cannons and black missile racks rising
from its back, huge curved gold claws on its feet and a long segmented purple tail. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, metal, riveted, scales, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 3.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking four-legged red-armoured war dragon with a horned purple head, a battery of steel cannons and missile "
        "racks on its back, huge gold claws and a segmented purple tail")
BASE = {"red": (200, 40, 40), "red_dark": (100, 10, 14), "red_light": (250, 130, 120), "gold": (240, 196, 60),
        "gold_dark": (160, 110, 20), "purple": (120, 60, 160), "purple_dark": (50, 20, 80), "purple_light": (190, 140, 230),
        "steel": (210, 214, 226), "steel_dark": (100, 104, 116), "black": (40, 40, 46), "black_dark": (12, 12, 16),
        "green": (80, 230, 120), "mouth": (100, 20, 40), "tooth": (250, 250, 246), "stripe": (220, 50, 40)}
SHINY = {"red": (40, 100, 200), "red_dark": (10, 40, 100), "red_light": (130, 180, 250), "purple": (60, 150, 90),
         "purple_dark": (20, 70, 40)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="gold", trim_w=0.3)
PURPLE = scales(P, "purple", "purple_dark", size=1.4, light="purple_light", rim_mix=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def barrelf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y + z * 0.3) % 6.0 < 0.8:
        return tone(p["stripe"], face), None
    return metal(P, "steel", dark="steel_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("destromon")
    mats = {"skin": RED, "belly": PURPLE, "neck": PURPLE, "head": PURPLE, "snout": PURPLE, "jaw": PURPLE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": RED, "leg_lower": PURPLE, "paw": RED,
            "claw": GOLD, "tail": PURPLE}
    a = quadruped(m, mats, "destromon", length=34.0, body_y=16.0, body_rx=8.4, body_ry=7.6, chest_bulk=1.3,
                  neck=((0, 20, -16), (0, 24, -21)), head_len=8.0, head_w=3.4, head_h=3.6, snout=0.4, mouth_open=10,
                  teeth=3, leg_bulk=2.0, toes=3,
                  tail=((0, 16, 17), (4, 12, 24), (9, 8, 28), (14, 6, 30)), tail_r=(2.6, 2.0, 1.6, 1.2))
    bd, hd = a["body"], a["head"]
    spike(m, hd, (0, 26.0, -21.0), (0, 1, 0.6), 2.4, 6.0, RED, tip=0.6)                 # red crest
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 25.0, -20.0), (sx * 0.4, 0.6, 1), 1.0, 4.0, GOLD, tip=0.3)
        ex, ey, ez = a["eye"]
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "green", glow=True))
    m.round_box(bd, 0, 0, 7.0, 8.0, 23.0, 26.0, riveted(P, "black", "black_dark"), cut=2)  # gun deck
    for j in range(4):                                                                 # long steel cannons
        x = -4.5 + j * 3.0
        rod(m, bd, (x, 25.0, 2.0 + j), (x * 1.3, 44.0, -6.0 + j * 2.0), 2, barrelf, extend=0)
    for sx in (-1, 1):                                                                 # missile racks
        m.box(bd, min(sx * 7.0, sx * 11.0), 22.0, -4.0, max(sx * 7.0, sx * 11.0), 27.0, 6.0,
              riveted(P, "black", "black_dark"))
        for j in range(3):
            m.box(bd, min(sx * 7.6, sx * 10.4), 23.0 + j * 1.4, -4.4, max(sx * 7.6, sx * 10.4), 23.8 + j * 1.4, -4.0,
                  solid(P, "red"))
    for p in a["tail_pts"][1:]:
        m.round_box(a["tail"], p[0], p[2], 2.4, 2.4, p[1] - 1.0, p[1] + 1.0, RED, cut=1)
    for nm in ("leg_front_left", "leg_front_right"):                                   # huge gold claws
        w = a[nm]["wrist"]
        for j in range(3):
            pts = [(w[0] + (j - 1) * 1.6, 3.0, w[2] - 2.0)]
            for s in range(1, 4):
                t = s / 3
                pts.append((pts[0][0], 3.0 + 3.0 * math.sin(t * 2.4), w[2] - 2.0 - 7.0 * t))
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, a[nm]["bone"], p0, p1, 1, GOLD, extend=0.4, t2=2)
    return m
