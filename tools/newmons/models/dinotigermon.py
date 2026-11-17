"""Dinotigermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the ancient sabre-tooth. A powerful four-legged beast of shaggy blue-and-white fur half clad in
riveted bronze armour plates, a bronze-masked head with green eyes and two huge ivory sabre teeth, red antenna-whips
sweeping back from its head, steel spines along its flanks, cuffs of shaggy fur round its ankles and huge steel
claws. 35 blocks tall.

Front is -z, y is up. 36 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 3.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a powerful four-legged sabre-tooth of shaggy blue-and-white fur half clad in riveted bronze armour, with huge "
        "ivory sabre teeth, red antenna-whips, steel flank spines and steel claws")
BASE = {"fur": (90, 140, 200), "fur_dark": (30, 60, 110), "fur_tip": (230, 240, 250), "bronze": (180, 110, 60),
        "bronze_dark": (100, 50, 20), "bronze_light": (240, 170, 110), "ivory": (240, 236, 220), "ivory_dark": (170, 160, 140),
        "red": (200, 50, 40), "steel": (210, 214, 226), "steel_dark": (100, 104, 116), "eye": (80, 220, 120),
        "mouth": (130, 20, 30), "tooth": (250, 250, 246)}
SHINY = {"fur": (200, 160, 80), "fur_dark": (120, 80, 20), "bronze": (120, 120, 140), "bronze_dark": (50, 50, 66)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_tip", length=2.0, density=1.8)
BRONZE = armour(P, "bronze", "bronze_dark", light="bronze_light", rivets=True)
STEEL = metal(P, "steel", dark="steel_dark")
IVORY = metal(P, "ivory", dark="ivory_dark", streak=4.0)


def build():
    m = Model("dinotigermon")
    mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": BRONZE, "snout": BRONZE, "jaw": BRONZE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": BRONZE, "leg_lower": BRONZE,
            "paw": BRONZE, "claw": STEEL, "tail": FUR}
    a = quadruped(m, mats, "dinotigermon", length=36.0, body_y=18.0, body_rx=7.4, body_ry=7.0, chest_bulk=1.3,
                  neck=((0, 20, -18), (0, 22, -22)), head_len=9.0, head_w=4.0, head_h=4.4, snout=0.4, mouth_open=12,
                  teeth=3, leg_bulk=1.8, toes=4, tail=((0, 20, 18), (0, 22, 24), (2, 24, 29)), tail_r=(3.0, 2.4, 1.8))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye", glow=True))
        sb = a["mouth_y"]
        spike(m, hd, (sx * 2.0, sb, a["snout_front"] + 2.0), (0, -1, -0.15), 1.4, 10.0, IVORY, tip=0.6)   # sabres
        pts = [(sx * 2.0, ey + 2.0, ez + 2.0), (sx * 4.0, ey + 8.0, ez + 10.0), (sx * 5.0, ey + 10.0, ez + 22.0),
               (sx * 6.0, ey + 6.0, ez + 34.0), (sx * 7.0, ey - 2.0, ez + 42.0)]
        for p0, p1 in zip(pts, pts[1:]):                                      # red antenna-whips
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.4)
    for j in range(5):                                                        # bronze back plates
        m.round_box(bd, 0, -10.0 + j * 5.0, 6.0 - abs(j - 2) * 0.6, 2.2, 23.0, 25.6, BRONZE, cut=1)
    for sx in (-1, 1):                                                        # steel flank spines
        for j in range(4):
            spike(m, bd, (sx * 7.0, 18.0 + (j % 2) * 3.0, -2.0 + j * 4.0), (sx, 0.2, 0.8), 1.2, 6.0, STEEL, tip=0.3)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 3.4, 3.4, 3.0, 7.0, FUR, cut=1)            # shaggy ankle cuffs
    return m
