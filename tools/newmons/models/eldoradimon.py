"""El Doradimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the walking city of gold. A colossal tortoise whose shell is a terraced stone city of brick
ramparts and green jungle, rising to a stepped temple-pyramid; its long green scaly neck bears a head masked in gold and
red with a jewelled crest, and its pillar-like legs end in great golden toes. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, gem, metal, riveted, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a colossal tortoise whose shell is a terraced stone city with jungle and a stepped temple-pyramid, a gold-and-"
        "red masked head and great golden toes")
BASE = {"stone": (170, 110, 80), "stone_dark": (100, 60, 40), "stone_light": (220, 170, 130), "jungle": (60, 140, 60),
        "jungle_dark": (20, 70, 24), "jungle_light": (140, 210, 110), "green": (110, 150, 70), "green_dark": (50, 80, 30),
        "green_light": (170, 210, 120), "gold": (250, 210, 60), "gold_dark": (170, 120, 20), "red": (210, 40, 40),
        "red_light": (255, 150, 140), "eye": (250, 220, 60), "mouth": (100, 30, 30), "tooth": (250, 248, 240)}
SHINY = {"stone": (150, 150, 170), "stone_dark": (80, 80, 100), "jungle": (160, 80, 160), "jungle_dark": (80, 30, 80)}


def P(v):
    return pal(BASE, SHINY, v)


BRICK = riveted(P, "stone", "stone_dark", light="stone_light", spacing=1.6)
JUNGLE = fur(P, "jungle", "jungle_dark", tip="jungle_light", length=1.4, density=1.6)
HIDE = scales(P, "green", "green_dark", size=1.4, light="green_light", rim_mix=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("eldoradimon")
    mats = {"skin": HIDE, "belly": BRICK, "neck": HIDE, "head": armour(P, "gold", "gold_dark", trim="red"),
            "snout": GOLD, "jaw": HIDE, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE,
            "leg_lower": BRICK, "paw": GOLD, "claw": GOLD, "tail": HIDE}
    a = quadruped(m, mats, "eldoradimon", length=34.0, body_y=12.0, body_rx=10.0, body_ry=6.0, chest_bulk=1.0,
                  neck=((0, 14, -18), (0, 20, -24), (0, 22, -28)), head_len=8.0, head_w=3.4, head_h=3.6, snout=0.5,
                  mouth_open=8, teeth=2, leg_bulk=2.4, toes=3, tail=((0, 10, 18), (0, 8, 22)), tail_r=(2.0, 1.4))
    bd, hd = a["body"], a["head"]
    for i, (r, h) in enumerate(((14.0, 3.0), (12.0, 3.0), (10.0, 3.0))):             # terraced city shell
        y0 = 14.0 + i * 3.0
        m.round_box(bd, 0, 0, r, r * 1.1, y0, y0 + h, BRICK, cut=max(2, round(r * 0.35)))
        m.round_box(bd, 0, 0, r - 1.0, r * 1.1 - 1.0, y0 + h - 0.6, y0 + h + 0.8, JUNGLE, cut=max(2, round(r * 0.3)))
    for j, w in enumerate((7.0, 5.6, 4.2, 2.8, 1.6)):                                 # stepped temple-pyramid
        m.box(bd, -w, 24.0 + j * 2.4, -w + 2.0, w, 26.4 + j * 2.4, w + 2.0, BRICK)
    spike(m, bd, (0, 36.0, 2.0), (0, 1, 0), 1.6, 4.0, GOLD, tip=0.4)
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye", glow=True))
    m.round_box(hd, 0, ez + 1.0, 2.6, 1.0, ey + 1.0, ey + 4.0, gem(P, "red", "red_light", glow=False), cut=1)   # crest
    return m
