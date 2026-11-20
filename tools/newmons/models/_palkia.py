"""A Palkia-shaped body for the Gen 4 paradox Palkias (Proto-Palkia, Iron Expanse): the upright theropod builder with
Palkia's proportions (broad chest, long clawed arms, massive thighs, a long tail) plus the round pearls on its
shoulders and the crest on its head. Materials as theropod's (skin, belly, neck, head, arm, hand, claw, thigh, shin,
foot, talon, tail, tail_tip) plus pearl, mount (the pearls' frames) and crest.

Front is -z. Returns theropod's anchors plus pearls [(x, y, z) per side].
"""
from __future__ import annotations

from _boxmodel import spike
from _digibeast import theropod
from _regi import ellipsoid


def palkia(m, mats, name, pearl_r=2.8):
    def M(k):
        return mats.get(k) or mats["skin"]

    a = theropod(m, mats, name, hip_y=22.0, hip_z=3.0, chest=(0, 38.0, -1.0), body_r=7.0, chest_r=7.4,
                 belly_r=5.2, neck_top=(0, 50.0, -7.0), head_len=11.0, head_w=3.8, head_h=4.2, mouth_open=12,
                 teeth=0, arm_len=15.0, arm_bulk=1.3, fingers=3, leg_bulk=1.5, toes=3, stance=5.6,
                 tail=((0, 20, 13), (0, 15, 21), (0, 10, 28), (0, 6, 34)), tail_r=(5.0, 3.8, 2.6, 1.4))
    bd, hd = a["body"], a["head"]
    pearls = []
    for sx in (-1, 1):                                                           # the shoulder pearls
        c = (sx * 8.8, 40.6, -1.4)
        ellipsoid(m, bd, c[0] + sx * 0.4, c[1], c[2] + 0.6, pearl_r + 0.9, pearl_r + 0.9, pearl_r + 0.6, M("mount"),
                  step=1)
        ellipsoid(m, bd, c[0] + sx * 1.0, c[1], c[2], pearl_r, pearl_r, pearl_r, M("pearl"), step=1)
        pearls.append(c)
    hx, hy, hz = a["head_c"]
    spike(m, hd, (0, a["skull_top"] - 0.4, hz - 2.0), (0, 0.55, 1), 2.4, 7.0, M("crest"), tip=1.2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, a["skull_top"] - 1.6, hz), (sx * 0.4, 0.3, 1), 1.4, 4.0, M("crest"), tip=0.6)
    a["pearls"] = pearls
    return a
