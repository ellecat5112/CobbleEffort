"""Manticoremon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the demon manticore: a hulking grey beast with a ragged white mane, a fanged maw with a long red
tongue, a crown of curved blue horns, black-banded steel bracers with huge blue claws, a talisman scroll hanging from
its collar, pale spiked wings and a long black segmented scorpion tail ending in a red stinger. 25 blocks long.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fabric, fur, metal, riveted, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
LOOK = "a hulking grey demon manticore with a ragged white mane, blue horns, huge blue claws, pale spiked wings and a black scorpion tail"
BASE = {"grey": (120, 120, 130), "grey_dark": (60, 60, 70), "white": (236, 236, 244), "white_dark": (170, 170, 186),
        "blue": (60, 110, 220), "blue_light": (150, 190, 250), "black": (34, 32, 38), "black_dark": (10, 10, 12),
        "red": (210, 40, 50), "mouth": (160, 30, 40), "tooth": (250, 248, 236), "eye": (250, 220, 60),
        "scroll": (240, 220, 160), "steel": (170, 174, 186), "steel_dark": (80, 84, 96)}
SHINY = {"grey": (150, 110, 60), "grey_dark": (80, 50, 20), "blue": (230, 90, 60), "blue_light": (255, 170, 140)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = fur(P, "grey", "grey_dark", length=1.2)
BLUE = solid(P, "blue")


def build():
    m = Model("manticoremon")
    mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "leg_upper": HIDE, "leg_lower": riveted(P, "black", "black_dark"), "paw": HIDE,
            "claw": BLUE, "tail": HIDE}
    a = quadruped(m, mats, "manticoremon", length=28.0, body_y=16.0, body_rx=6.4, body_ry=6.4, chest_bulk=1.4,
                  neck=((0, 20, -13), (0, 22, -17)), head_len=9.0, head_w=4.0, head_h=4.0, snout=0.7, mouth_open=22,
                  teeth=5, leg_bulk=1.6, toes=3, tail=((0, 20, 15), (0, 22, 18)), tail_r=(2.0, 1.6))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
              solid(P, "eye", glow=True))
    for j in range(7):                                                               # crown of blue horns
        ang = math.radians(-70 + j * 23)
        pts = [(3.0 * math.sin(ang), hc[1] + 3.0, hc[2] + 1.0), (6.0 * math.sin(ang), hc[1] + 8.0, hc[2] + 3.0),
               (5.0 * math.sin(ang), hc[1] + 11.0, hc[2] + 6.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, BLUE, extend=0.2, t2=2)
    for i in range(14):                                                              # ragged white mane
        ang = 2 * math.pi * i / 14
        spike(m, a["neck"], (4.0 * math.cos(ang), 21.0 + 4.0 * math.sin(ang), -15.0), (math.cos(ang), math.sin(ang), 0.5), 2.4,
              6.0, strands(P, "white", "white_dark"), tip=0.8)
    m.round_box(a["neck"], 0, -19.0, 1.6, 0.4, 12.0, 19.0, fabric(P, "scroll", "steel_dark"), cut=0)       # talisman
    for side in (1, -1):                                                             # pale spiked wings
        for j in range(4):
            spike(m, bd, (side * 4.0, 22.0, -2.0 + j * 2.6), (side * 0.8, 0.7, 0.3), 2.0, 14.0 - j * 2.0,
                  fur(P, "white", "white_dark"), tip=0.8)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        for j in range(3):
            spike(m, a[nm]["bone"], (w[0] + (j - 1) * 1.8, 1.4, w[2] - 3.0), (0, -0.3, -1), 1.4, 5.0, BLUE, tip=0.8)
    tb = a["tail"]                                                                   # black scorpion tail
    pts = [(0, 22.0, 18.0), (0, 30.0, 22.0), (0, 38.0, 20.0), (0, 42.0, 14.0), (0, 40.0, 9.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, riveted(P, "black", "black_dark"), extend=0.6)
    spike(m, tb, pts[-1], (0, -0.6, -1), 1.6, 4.0, solid(P, "red"), tip=0.8)
    return m
