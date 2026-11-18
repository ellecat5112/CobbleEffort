"""Shared builder for Nefertimon and Nefertimon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the Armor Digimon of light: a white sphinx lying on great clawed paws, a woman's face behind a
golden pharaoh's headdress and mask, silver-and-gold armour on its breast and forelegs set with red gems, great white
feathered wings and a long tail ending in a violet tuft. The X-Antibody ("x"): bronze-and-black armour, a jackal-eared
headdress, black claws and a blue tail tuft.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing, quadruped
from _digidetail import armour, feathers, fur, gem, metal, solid
from _route import pal, tone

BASE = {"white": (244, 244, 250), "white_dark": (180, 182, 200), "gold": (236, 196, 80), "gold_dark": (160, 120, 30),
        "silver": (210, 214, 226), "silver_dark": (110, 116, 130), "red": (210, 40, 70), "violet": (130, 80, 190),
        "black": (40, 36, 44), "bronze": (180, 130, 70), "bronze_dark": (100, 66, 30), "blue": (60, 90, 200),
        "claw": (240, 220, 120), "eye": (60, 50, 70), "mask": (240, 236, 230)}
SHINY = {"white": (60, 60, 72), "white_dark": (24, 24, 30), "gold": (200, 210, 230), "gold_dark": (120, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    PLATE = armour(P, "bronze" if x else "silver", "bronze_dark" if x else "silver_dark", trim="gold", trim_w=0.3)
    GOLD = armour(P, "gold", "gold_dark", trim="black" if x else "gold_dark", trim_w=0.25)
    FUR = fur(P, "white", "white_dark", length=1.0)

    def build():
        m = Model(name)
        mats = {"skin": FUR, "claw": solid(P, "black" if x else "claw")}
        a = quadruped(m, mats, name, length=28.0, body_y=14.0, body_rx=6.0, body_ry=5.4, chest_bulk=1.3,
                      neck=((0, 20, -12), (0, 26, -14)), head_len=6.0, head_w=3.0, head_h=3.6, snout=0.1,
                      mouth_open=0, teeth=0, leg_bulk=1.6, toes=4,
                      tail=((0, 18, 14), (0, 22, 20), (0, 25, 25)), tail_r=(1.0, 0.8, 0.7))
        bd, hd = a["body"], a["head"]
        hc = a["head_c"]
        m.round_box(hd, 0, hc[2] - 1.0, 3.0, 3.0, hc[1] - 3.0, hc[1] + 3.0, solid(P, "mask"), cut=1)  # woman's face
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.6), hc[1] + 0.4, hc[2] - 4.05, max(sx * 0.6, sx * 1.6), hc[1] + 1.0,
                  hc[2] - 3.95, solid(P, "eye"))
            x0, x1 = sorted((sx * 2.4, sx * 4.4))                                       # headdress lappets
            m.box(hd, x0, hc[1] - 8.0, hc[2] - 1.0, x1, hc[1] + 3.0, hc[2] + 2.0, GOLD)
            if x:
                spike(m, hd, (sx * 2.4, hc[1] + 3.0, hc[2]), (sx * 0.2, 1, 0.1), 1.6, 5.0, GOLD, tip=0.8)
        m.round_box(hd, 0, hc[2] + 0.4, 3.6, 3.6, hc[1] + 2.4, hc[1] + 4.4, GOLD, cut=1)
        m.box(hd, -0.6, hc[1] + 3.6, hc[2] - 3.8, 0.6, hc[1] + 4.6, hc[2] - 3.4, gem(P, "red", "white"))
        m.round_box(bd, 0, -9.0, 5.0, 3.0, 12.0, 20.0, PLATE, cut=1)                    # breast armour
        for nm in ("leg_front_left", "leg_front_right"):                                # foreleg armour
            anc = a[nm]
            w = anc.get("wrist") or anc["hip"]
            m.round_box(anc["bone"], w[0], w[2], 2.6, 2.6, w[1] + 1.0, w[1] + 7.0, PLATE, cut=1)
            m.box(anc["bone"], w[0] - 0.6, w[1] + 3.0, w[2] - 2.75, w[0] + 0.6, w[1] + 5.0, w[2] - 2.6,
                  gem(P, "red", "white"))
        tp = a["tail_pts"][-1]
        spike(m, a["tail"], tp, (0, 0.6, 1), 2.0, 4.0, solid(P, "blue" if x else "violet"), tip=0.8)
        for side in (1, -1):                                                            # great feathered wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 19.0, -6.0))
            feather_wing(m, wb, (side * 4.0, 19.0, -6.0), 20.0, 12.0, 6, feathers(P, "white", "white_dark"),
                         side=side, sweep=30, droop=-10.0)
        return m

    return build
