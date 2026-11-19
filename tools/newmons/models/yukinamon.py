"""Yukinamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net; built covered): the spirit of the snowstorm: a slender pale-blue woman in long flowing robes of
violet and lilac with wide sleeves, an ice-crystal crown and a blue gem at her breast, her hair a vast wave of
translucent swirling snow-wind rising behind her. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, gem, skin, solid
from _route import pal, tone

HEIGHT = 79
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a slender pale-blue snowstorm spirit in long violet robes with an ice-crystal crown and a vast wave of swirling snow-wind hair"
BASE = {"skin": (190, 220, 240), "skin_dark": (120, 160, 200), "violet": (150, 110, 190), "violet_dark": (80, 50, 120),
        "lilac": (210, 190, 240), "lilac_dark": (150, 130, 200), "ice": (190, 240, 255), "gem": (60, 110, 220),
        "gem_light": (170, 210, 255), "wind": (170, 220, 250, 150), "eye": (60, 120, 220)}
SHINY = {"violet": (60, 130, 160), "violet_dark": (20, 70, 100), "wind": (230, 230, 255, 150)}


def P(v):
    return pal(BASE, SHINY, v)


ROBE = fabric(P, "violet", "violet_dark")
LILAC = fabric(P, "lilac", "lilac_dark")
SKIN = skin(P, "skin", dark="skin_dark")


def build():
    m = Model("yukinamon")
    mats = {"skin": SKIN, "chest": LILAC, "abs": LILAC, "pelvis": ROBE, "deltoid": ROBE, "upper_arm": ROBE,
            "forearm": ROBE, "hand": SKIN, "thigh": ROBE, "knee": ROBE, "shin": ROBE, "calf": ROBE, "foot": SKIN,
            "neck": SKIN}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.75, leg_bulk=0.85, name="yukinamon")
    bd = a["body"]
    for i in range(10):                                                                 # long flowing robe
        ang = i * 2 * math.pi / 10
        cx, cz = 5.4 * math.sin(ang), 4.4 * math.cos(ang)
        m.box(bd, cx - 2.0, 2.0, cz - 0.5, cx + 2.0, 34.0, cz + 0.5, ROBE if i % 2 else LILAC,
              rotation=(0, math.degrees(ang), 0), pivot=(cx, 18.0, cz))
    for nm in ("arm_left", "arm_right"):                                                # wide sleeves
        w = a[nm]["wrist"]
        m.box(a[nm]["bone"], w[0] - 3.0, w[1] - 8.0, w[2] - 1.0, w[0] + 3.0, w[1] + 4.0, w[2] + 3.0, ROBE)
    ball(m, bd, (0, 46.0, -4.4), 1.4, gem(P, "gem", "gem_light"), layers=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 58.0, -3.2, max(sx * 0.6, sx * 1.8), 58.8, -3.0, solid(P, "eye"))
    for j in range(5):                                                                  # ice-crystal crown
        spike(m, hd, ((j - 2) * 1.0, 61.0, -1.0), ((j - 2) * 0.3, 1, 0), 0.9, 3.0 + (2 - abs(j - 2)) * 1.4,
              solid(P, "ice", glow=True), tip=0.8)
    wb = m.bone("snowhair", hd, (0, 60, 2))                                             # swirling snow-wind hair
    for i in range(12):
        t = i / 11
        ang = t * 3.2
        c = (math.sin(ang) * (6.0 + t * 8.0), 60.0 + t * 14.0, 4.0 + t * 6.0)
        ball(m, wb, c, 3.0 + t * 2.0, solid(P, "wind", glow=True), layers=2)
    return m
