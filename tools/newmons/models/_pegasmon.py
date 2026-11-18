"""Shared builder for Pegasmon and Pegasmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the Armor Digimon of hope: an orange-coated winged horse armoured in gold, a golden horned helm, golden
leg greaves set with violet gems, a long pale mane, great golden-white feathered wings and a flowing tail. The
X-Antibody ("x"): sleeker crystalline gold armour seamed with glowing cyan, wings of blade-like gold and cyan light.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing, quadruped
from _digidetail import armour, feathers, fur, gem, metal, solid, strands
from _route import pal, tone

BASE = {"orange": (240, 150, 50), "orange_dark": (180, 100, 20), "gold": (236, 200, 90), "gold_dark": (160, 120, 30),
        "cream": (250, 240, 200), "cream_dark": (200, 186, 140), "violet": (130, 80, 190), "cyan": (100, 230, 240),
        "eye": (60, 110, 200), "black": (30, 28, 30), "white": (248, 246, 236)}
SHINY = {"orange": (240, 240, 246), "orange_dark": (170, 172, 190), "gold": (190, 200, 230), "gold_dark": (100, 110, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    GOLD = armour(P, "gold", "gold_dark", trim="cyan" if x else "gold_dark", trim_w=0.25)
    COAT = fur(P, "orange", "orange_dark", length=0.8)

    def build():
        m = Model(name)
        mats = {"skin": COAT, "claw": solid(P, "black"), "mouth": solid(P, "black"), "tooth": solid(P, "white")}
        a = quadruped(m, mats, name, length=26.0, body_y=18.0, body_rx=5.2, body_ry=5.2, chest_bulk=1.2,
                      neck=((0, 24, -12), (0, 30, -15)), head_len=9.0, head_w=2.6, head_h=3.0, snout=0.9,
                      mouth_open=4, teeth=0, leg_bulk=1.1, toes=1,
                      tail=((0, 21, 13), (0, 18, 18), (0, 14, 22)), tail_r=(1.4, 1.2, 1.0))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        hc = a["head_c"]
        m.round_box(hd, 0, hc[2], 3.2, 5.0, ey - 1.0, ey + 2.6, GOLD, cut=1)              # golden horned helm
        spike(m, hd, (0, ey + 2.4, hc[2] - 4.0), (0, 0.6, -1), 1.4, 6.0, metal(P, "gold"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 3.2, sx * 3.4), ey, ez - 0.6, max(sx * 3.2, sx * 3.4), ey + 0.8, ez + 0.6,
                  solid(P, "cyan" if x else "eye", glow=x))
            spike(m, hd, (sx * 2.4, ey + 2.4, hc[2] + 2.0), (sx * 0.4, 0.8, 0.6), 1.2, 4.0, GOLD, tip=0.8)
        for j in range(7):                                                             # long pale mane
            spike(m, a["neck"], (0, 31.0 - j * 1.2, -14.0 + j * 0.8), (0, 0.3, 1), 1.6, 7.0,
                  strands(P, "cream", "cream_dark"), tip=0.8)
        for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):   # gem greaves
            anc = a[nm]
            w = anc.get("wrist") or anc.get("ankle")
            if w:
                m.round_box(anc["bone"], w[0], w[2], 2.0, 2.0, w[1] + 1.0, w[1] + 7.0, GOLD, cut=1)
                m.box(anc["bone"], w[0] - 0.6, w[1] + 3.0, w[2] - 2.15, w[0] + 0.6, w[1] + 5.0, w[2] - 2.0,
                      gem(P, "violet", "cream"))
        m.round_box(bd, 0, -8.0, 4.8, 3.0, 16.0, 23.0, GOLD, cut=1)                      # breastplate
        for side in (1, -1):                                                           # wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 23.0, -4.0))
            if x:
                for j in range(5):
                    spike(m, wb, (side * 4.0, 23.0, -4.0), (side * 1, 0.9 - j * 0.3, 0.6), 1.4, 18.0 - j * 2.0,
                          solid(P, "cyan" if j % 2 else "gold", glow=j % 2 == 1), tip=0.8)
            else:
                feather_wing(m, wb, (side * 4.0, 23.0, -4.0), 18.0, 12.0, 6, feathers(P, "white", "cream_dark", tip="gold"),
                             side=side, sweep=25, droop=-10.0)
        tp = a["tail_pts"][-1]
        for j in range(4):
            spike(m, a["tail"], tp, ((j - 1.5) * 0.3, -0.6, 1), 1.2, 6.0, strands(P, "cream", "cream_dark"), tip=0.8)
        return m

    return build
