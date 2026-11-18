"""Groundramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the earth dragon: a low, heavy green dragon covered in thick scales, a long-jawed armoured head
with red hooked horns, a row of grey spikes down its back, a spiked mace on its tail tip, a second small head on its
belly-plate and powerful clawed legs. 25 blocks long.

Front is -z, y is up. 30 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import metal, scales, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a low heavy green dragon in thick scales with a long armoured jaw, red hooked horns, grey back spikes and a "
        "spiked mace on its tail")
BASE = {"green": (60, 130, 70), "green_dark": (24, 70, 30), "green_light": (130, 200, 130), "red": (200, 30, 40),
        "grey": (150, 154, 166), "grey_dark": (70, 74, 86), "mouth": (110, 20, 30), "tooth": (250, 250, 240),
        "eye": (250, 220, 60), "claw": (240, 236, 220)}
SHINY = {"green": (150, 110, 60), "green_dark": (90, 60, 24), "green_light": (210, 170, 120)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.8, light="green_light")
GREY = metal(P, "grey", dark="grey_dark")


def build():
    m = Model("groundramon")
    mats = {"skin": HIDE, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "claw")}
    a = quadruped(m, mats, "groundramon", length=34.0, body_y=13.0, body_rx=7.0, body_ry=5.4, chest_bulk=1.2,
                  neck=((0, 17, -16), (0, 18, -21)), head_len=13.0, head_w=3.4, head_h=3.4, snout=1.0, mouth_open=14,
                  teeth=6, leg_bulk=1.4, toes=3, tail=((0, 15, 17), (0, 16, 24), (0, 17, 31)), tail_r=(3.4, 2.4, 1.6))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye", glow=True))
        pts = [(sx * 2.4, ey + 2.4, ez + 1.0), (sx * 4.4, ey + 6.0, ez - 1.0), (sx * 3.6, ey + 8.0, ez - 4.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.3, t2=2)
    for j in range(7):                                                                    # grey back spikes
        spike(m, bd, (0, 18.4, -12.0 + j * 4.0), (0, 1, 0.3), 2.0, 4.0 - abs(j - 3) * 0.4, GREY, tip=0.8)
    e = a["tail_pts"][-1]                                                                  # spiked tail mace
    m.round_box(a["tail"], e[0], e[2], 2.6, 2.6, e[1] - 2.6, e[1] + 2.6, GREY, cut=1)
    for ang in range(0, 360, 60):
        r_ = math.radians(ang)
        spike(m, a["tail"], (e[0] + 2.6 * math.cos(r_), e[1] + 2.6 * math.sin(r_), e[2]), (math.cos(r_), math.sin(r_), 0.3),
              1.0, 2.6, GREY, tip=0.8)
    m.round_box(bd, 0, -14.0, 2.6, 2.0, 7.0, 10.4, HIDE, cut=1)                            # small belly head
    for sx in (-1, 1):
        spike(m, bd, (sx * 1.6, 9.4, -16.0), (sx * 0.3, 0.4, -1), 0.8, 2.0, solid(P, "red"), tip=0.8)
    return m
